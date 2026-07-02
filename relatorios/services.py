"""
Métricas do dashboard e relatórios.

Regra central: pedidos CANCELADOS nunca contam como faturamento.
Queries usam annotations/aggregations do ORM (sem loops em Python).
"""

from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, F, Sum
from django.utils import timezone

from clientes.models import Cliente
from pedidos.models import ItemPedido, Pedido
from produtos.models import Produto


def _pedidos_validos():
    return Pedido.objects.exclude(status=Pedido.Status.CANCELADO)


def resumo_dashboard():
    agora = timezone.now()
    inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    sete_dias = agora - timedelta(days=7)
    validos = _pedidos_validos()

    return {
        "total_pedidos": Pedido.objects.count(),
        "total_vendido": validos.aggregate(v=Sum("total"))["v"] or Decimal("0"),
        "faturamento_mes": validos.filter(criado_em__gte=inicio_mes)
            .aggregate(v=Sum("total"))["v"] or Decimal("0"),
        "faturamento_7_dias": validos.filter(criado_em__gte=sete_dias)
            .aggregate(v=Sum("total"))["v"] or Decimal("0"),
        "clientes_cadastrados": Cliente.objects.count(),
        "produtos_ativos": Produto.objects.filter(ativo=True).count(),
    }


def pedidos_por_status():
    contagem = dict(
        Pedido.objects.values_list("status").annotate(qtd=Count("id"))
    )
    return [
        {"status": valor, "label": rotulo, "quantidade": contagem.get(valor, 0)}
        for valor, rotulo in Pedido.Status.choices
    ]


def produtos_mais_vendidos(limite=10):
    return (
        ItemPedido.objects.exclude(pedido__status=Pedido.Status.CANCELADO)
        .values("nome_produto_snapshot", "sku_snapshot")
        .annotate(vendidos=Sum("quantidade"), receita=Sum("subtotal"))
        .order_by("-vendidos")[:limite]
    )


def produtos_baixo_estoque(limite=10):
    return (
        Produto.objects.filter(ativo=True, estoque__lte=F("estoque_minimo"))
        .order_by("estoque")[:limite]
    )


def pedidos_recentes(limite=10):
    return Pedido.objects.select_related("cliente")[:limite]
