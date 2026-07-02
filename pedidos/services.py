"""
Regras de negócio de pedidos: mudança de status, baixa e devolução de estoque.

Regras principais (ver MIGRATION_REPORT.md):
- Ao confirmar pedido, reduzir estoque (uma única vez).
- Ao cancelar pedido confirmado, devolver estoque.
- Pedido cancelado não conta como faturamento.
- Toda mudança de status gera registro em HistoricoStatus.
"""

from django.db import transaction
from django.db.models import F

from .models import HistoricoStatus, Pedido


class TransicaoInvalida(Exception):
    """Mudança de status não permitida."""


class EstoqueInsuficiente(Exception):
    """Estoque acabou entre a validação do carrinho e a baixa atômica."""

    def __init__(self, produto, disponivel):
        self.produto = produto
        self.disponivel = disponivel
        super().__init__(
            f"Estoque insuficiente para {produto.nome} (disponível: {disponivel})."
        )


# De cada status, para quais é permitido ir
TRANSICOES_VALIDAS = {
    Pedido.Status.NOVO: {Pedido.Status.CONFIRMADO, Pedido.Status.CANCELADO},
    Pedido.Status.CONFIRMADO: {Pedido.Status.EM_SEPARACAO, Pedido.Status.ENVIADO, Pedido.Status.CANCELADO},
    Pedido.Status.EM_SEPARACAO: {Pedido.Status.ENVIADO, Pedido.Status.CANCELADO},
    Pedido.Status.ENVIADO: {Pedido.Status.ENTREGUE},
    Pedido.Status.ENTREGUE: set(),
    Pedido.Status.CANCELADO: set(),
}


def _baixar_estoque(pedido):
    """Reduz o estoque de cada item. Usa F() para evitar condição de corrida."""
    if pedido.estoque_baixado:
        return
    for item in pedido.itens.select_related("produto"):
        if item.produto_id:
            atualizados = item.produto.__class__.objects.filter(
                pk=item.produto_id, estoque__gte=item.quantidade
            ).update(estoque=F("estoque") - item.quantidade)
            if atualizados == 0:
                item.produto.refresh_from_db(fields=["estoque"])
                raise EstoqueInsuficiente(item.produto, item.produto.estoque)
    pedido.estoque_baixado = True
    pedido.save(update_fields=["estoque_baixado", "atualizado_em"])


def _devolver_estoque(pedido):
    """Devolve o estoque dos itens de um pedido que já teve baixa."""
    if not pedido.estoque_baixado:
        return
    for item in pedido.itens.select_related("produto"):
        if item.produto_id:
            item.produto.__class__.objects.filter(pk=item.produto_id).update(
                estoque=F("estoque") + item.quantidade
            )
    pedido.estoque_baixado = False
    pedido.save(update_fields=["estoque_baixado", "atualizado_em"])


@transaction.atomic
def alterar_status(pedido, novo_status, usuario=None, observacao=""):
    """
    Altera o status do pedido validando a transição e cuidando do estoque.
    Levanta TransicaoInvalida quando a mudança não é permitida.
    """
    # Visitantes (checkout sem login) não entram no histórico como usuário
    if usuario is not None and not getattr(usuario, "is_authenticated", False):
        usuario = None

    atual = pedido.status
    if novo_status == atual:
        return pedido
    if novo_status not in TRANSICOES_VALIDAS.get(atual, set()):
        raise TransicaoInvalida(
            f"Não é possível mudar de {pedido.get_status_display()} para "
            f"{Pedido.Status(novo_status).label}."
        )

    if novo_status == Pedido.Status.CONFIRMADO:
        _baixar_estoque(pedido)
    elif novo_status == Pedido.Status.CANCELADO:
        _devolver_estoque(pedido)
        if pedido.status_pagamento == Pedido.StatusPagamento.PAGO:
            pedido.status_pagamento = Pedido.StatusPagamento.ESTORNADO
        else:
            pedido.status_pagamento = Pedido.StatusPagamento.CANCELADO
        pedido.save(update_fields=["status_pagamento", "atualizado_em"])

    pedido.status = novo_status
    pedido.save(update_fields=["status", "atualizado_em"])
    HistoricoStatus.objects.create(
        pedido=pedido,
        status_anterior=atual,
        status_novo=novo_status,
        usuario=usuario,
        observacao=observacao,
    )
    return pedido


def marcar_pago(pedido, usuario=None):
    pedido.status_pagamento = Pedido.StatusPagamento.PAGO
    pedido.save(update_fields=["status_pagamento", "atualizado_em"])
    # Pagamento aprovado confirma o pedido automaticamente
    if pedido.status == Pedido.Status.NOVO:
        alterar_status(pedido, Pedido.Status.CONFIRMADO, usuario, "Pagamento confirmado")
    return pedido


def cancelar(pedido, usuario=None, observacao=""):
    return alterar_status(pedido, Pedido.Status.CANCELADO, usuario, observacao)
