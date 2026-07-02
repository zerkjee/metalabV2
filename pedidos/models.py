import secrets

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from clientes.models import Cliente
from cupons.models import Cupom
from produtos.models import Produto


def gerar_codigo_pedido():
    """Código curto, único e legível, ex.: MLB-4F7A2C."""
    return f"MLB-{secrets.token_hex(3).upper()}"


def gerar_idempotency_token():
    """Token por checkout: evita pedidos duplicados em duplo-clique."""
    return secrets.token_urlsafe(24)


def gerar_token_recibo():
    """Token público longo para URL de recibo, sem expor código enumerável."""
    return secrets.token_urlsafe(32)


class Pedido(models.Model):
    class Status(models.TextChoices):
        NOVO = "NOVO", "Novo"
        CONFIRMADO = "CONFIRMADO", "Confirmado"
        EM_SEPARACAO = "EM_SEPARACAO", "Em separação"
        ENVIADO = "ENVIADO", "Enviado"
        ENTREGUE = "ENTREGUE", "Entregue"
        CANCELADO = "CANCELADO", "Cancelado"

    class StatusPagamento(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        PAGO = "PAGO", "Pago"
        RECUSADO = "RECUSADO", "Recusado"
        ESTORNADO = "ESTORNADO", "Estornado"
        CANCELADO = "CANCELADO", "Cancelado"

    class MetodoPagamento(models.TextChoices):
        PIX_MANUAL = "PIX_MANUAL", "PIX"
        CARTAO_MANUAL = "CARTAO_MANUAL", "Cartão"
        BOLETO_MANUAL = "BOLETO_MANUAL", "Boleto"

    codigo = models.CharField("código", max_length=20, unique=True, default=gerar_codigo_pedido)
    idempotency_token = models.CharField(
        max_length=64, unique=True, default=gerar_idempotency_token
    )
    recibo_token = models.CharField(max_length=96, unique=True, default=gerar_token_recibo)
    cliente = models.ForeignKey(
        Cliente, null=True, blank=True, on_delete=models.SET_NULL, related_name="pedidos"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOVO)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    cupom = models.ForeignKey(
        Cupom, null=True, blank=True, on_delete=models.SET_NULL, related_name="pedidos"
    )
    metodo_pagamento = models.CharField(
        "método de pagamento", max_length=20, choices=MetodoPagamento.choices, blank=True
    )
    status_pagamento = models.CharField(
        max_length=20, choices=StatusPagamento.choices, default=StatusPagamento.PENDENTE
    )
    observacoes = models.TextField("observações", blank=True)

    # Snapshot do comprador/endereço no momento da compra (como na origem)
    comprador_nome = models.CharField(max_length=200, blank=True)
    comprador_email = models.EmailField(blank=True)
    comprador_telefone = models.CharField(max_length=20, blank=True)
    endereco_entrega = models.TextField("endereço de entrega", blank=True)

    # Baixa de estoque já realizada? (evita baixar/devolver duas vezes)
    estoque_baixado = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["status_pagamento"]),
            models.Index(fields=["comprador_email"]),
        ]

    def __str__(self):
        return self.codigo

    # ─── Cálculos ────────────────────────────────────────────────────────────

    def recalcular_totais(self, salvar=True):
        """Subtotal = soma dos itens; total = subtotal - desconto + frete (nunca negativo)."""
        self.subtotal = sum((item.subtotal for item in self.itens.all()), start=0)
        self.total = max(self.subtotal - self.desconto + self.frete, 0)
        if salvar:
            self.save(update_fields=["subtotal", "total", "atualizado_em"])

    @property
    def cancelado(self):
        return self.status == self.Status.CANCELADO

    @property
    def conta_como_faturamento(self):
        """Pedidos cancelados não contam como faturamento."""
        return not self.cancelado


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(
        Produto, null=True, on_delete=models.SET_NULL, related_name="itens_pedido"
    )
    # Snapshot: alterar o produto depois não altera pedidos antigos
    nome_produto_snapshot = models.CharField(max_length=200)
    sku_snapshot = models.CharField(max_length=60)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "item do pedido"
        verbose_name_plural = "itens do pedido"

    def __str__(self):
        return f"{self.quantidade}x {self.nome_produto_snapshot}"

    def save(self, *args, **kwargs):
        self.subtotal = self.preco_unitario * self.quantidade
        super().save(*args, **kwargs)


class HistoricoStatus(models.Model):
    """Histórico simples de alterações de status do pedido."""

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="historico")
    status_anterior = models.CharField(max_length=20, blank=True)
    status_novo = models.CharField(max_length=20)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    observacao = models.CharField("observação", max_length=300, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "histórico de status"
        verbose_name_plural = "históricos de status"

    def __str__(self):
        return f"{self.pedido.codigo}: {self.status_anterior} → {self.status_novo}"
