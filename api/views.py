"""
API interna em JSON puro (sem DRF), para futuras integrações.

/api/health/ é pública; as demais exigem usuário staff autenticado.
"""

from django.conf import settings
from django.core.paginator import Paginator
from django.db import connection
from django.http import JsonResponse

from accounts.decorators import api_staff_required
from clientes.models import Cliente
from core.security import json_get
from pedidos.models import Pedido
from produtos.models import Produto
from relatorios import services as relatorios_services


@json_get
def health(request):
    data = {"status": "ok"}
    if settings.HEALTHCHECK_INCLUDE_DATABASE:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            data["database"] = "connected"
        except Exception:
            data["database"] = "error"
    return JsonResponse(data)


def _paginate(request, items, key):
    try:
        per_page = min(max(int(request.GET.get("per_page", 50)), 1), 100)
    except (TypeError, ValueError):
        per_page = 50
    paginator = Paginator(list(items), per_page)
    page = paginator.get_page(request.GET.get("page"))
    return JsonResponse({
        "count": paginator.count,
        "page": page.number,
        "per_page": per_page,
        "num_pages": paginator.num_pages,
        key: list(page.object_list),
    })


def _not_found():
    return JsonResponse({"detail": "Nao encontrado."}, status=404)


def _produto_json(p, detalhado=False):
    dados = {
        "id": p.pk,
        "nome": p.nome,
        "slug": p.slug,
        "sku": p.sku,
        "categoria": p.categoria.nome if p.categoria else None,
        "preco": str(p.preco),
        "preco_promocional": str(p.preco_promocional) if p.preco_promocional else None,
        "estoque": p.estoque,
        "ativo": p.ativo,
        "destaque": p.destaque,
    }
    if detalhado:
        dados.update({
            "marca": p.marca,
            "descricao_curta": p.descricao_curta,
            "imagem_principal": p.imagem_principal.url if p.imagem_principal else None,
        })
    return dados


@json_get
@api_staff_required
def produtos_lista(request):
    produtos = (
        _produto_json(p)
        for p in Produto.objects.select_related("categoria").all()
    )
    return _paginate(request, produtos, "produtos")


@json_get
@api_staff_required
def produto_detalhe(request, pk):
    try:
        produto = Produto.objects.select_related("categoria").get(pk=pk)
    except Produto.DoesNotExist:
        return _not_found()
    return JsonResponse(_produto_json(produto, detalhado=True))


def _pedido_json(p, detalhado=False):
    dados = {
        "id": p.pk,
        "codigo": p.codigo,
        "status": p.status,
        "status_pagamento": p.status_pagamento,
        "total": str(p.total),
        "comprador": p.comprador_nome,
        "criado_em": p.criado_em.isoformat(),
    }
    if detalhado:
        dados.update({
            "subtotal": str(p.subtotal),
            "desconto": str(p.desconto),
            "frete": str(p.frete),
            "metodo_pagamento": p.metodo_pagamento,
            "itens": [
                {
                    "produto": i.nome_produto_snapshot,
                    "sku": i.sku_snapshot,
                    "quantidade": i.quantidade,
                    "preco_unitario": str(i.preco_unitario),
                    "subtotal": str(i.subtotal),
                }
                for i in p.itens.all()
            ],
        })
    return dados


@json_get
@api_staff_required
def pedidos_lista(request):
    pedidos = (_pedido_json(p) for p in Pedido.objects.all())
    return _paginate(request, pedidos, "pedidos")


@json_get
@api_staff_required
def pedido_detalhe(request, pk):
    try:
        pedido = Pedido.objects.prefetch_related("itens").get(pk=pk)
    except Pedido.DoesNotExist:
        return _not_found()
    return JsonResponse(_pedido_json(pedido, detalhado=True))


@json_get
@api_staff_required
def clientes_lista(request):
    clientes = (
        {"id": c.pk, "nome": c.nome, "email": c.email, "cidade": c.cidade,
         "estado": c.estado, "criado_em": c.criado_em.isoformat()}
        for c in Cliente.objects.all()
    )
    return _paginate(request, clientes, "clientes")


@json_get
@api_staff_required
def dashboard_resumo(request):
    resumo = relatorios_services.resumo_dashboard()
    return JsonResponse({
        "total_pedidos": resumo["total_pedidos"],
        "total_vendido": str(resumo["total_vendido"]),
        "faturamento_mes": str(resumo["faturamento_mes"]),
        "faturamento_7_dias": str(resumo["faturamento_7_dias"]),
        "clientes_cadastrados": resumo["clientes_cadastrados"],
        "produtos_ativos": resumo["produtos_ativos"],
    })
