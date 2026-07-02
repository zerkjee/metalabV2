from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Cupom(models.Model):
    class Tipo(models.TextChoices):
        PERCENTUAL = "PERCENTUAL", "Percentual (%)"
        VALOR_FIXO = "VALOR_FIXO", "Valor fixo (R$)"
        FRETE_GRATIS = "FRETE_GRATIS", "Frete grátis"

    codigo = models.CharField("código", max_length=40, unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    ativo = models.BooleanField(default=True)
    data_inicio = models.DateTimeField("início", null=True, blank=True)
    data_fim = models.DateTimeField("fim", null=True, blank=True)
    uso_maximo = models.PositiveIntegerField(null=True, blank=True)
    usos_realizados = models.PositiveIntegerField(default=0)
    valor_minimo_pedido = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)]
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "cupom"
        verbose_name_plural = "cupons"

    def __str__(self):
        return self.codigo

    def save(self, *args, **kwargs):
        self.codigo = self.codigo.strip().upper()
        super().save(*args, **kwargs)

    # ─── Validação de uso ────────────────────────────────────────────────────

    def validar(self, subtotal):
        """
        Verifica se o cupom pode ser aplicado a um pedido com este subtotal.
        Retorna (valido: bool, mensagem_de_erro: str).
        """
        agora = timezone.now()
        if not self.ativo:
            return False, "Este cupom não está mais ativo."
        if self.data_inicio and agora < self.data_inicio:
            return False, "Este cupom ainda não está válido."
        if self.data_fim and agora > self.data_fim:
            return False, "Este cupom expirou."
        if self.uso_maximo is not None and self.usos_realizados >= self.uso_maximo:
            return False, "Este cupom atingiu o limite de usos."
        if self.valor_minimo_pedido and subtotal < self.valor_minimo_pedido:
            return False, (
                f"Este cupom exige pedido mínimo de R$ {self.valor_minimo_pedido:.2f}."
            )
        return True, ""

    def calcular_desconto(self, subtotal):
        """Desconto sobre o subtotal. Nunca maior que o próprio subtotal."""
        if self.tipo == self.Tipo.PERCENTUAL:
            desconto = subtotal * self.valor / Decimal("100")
        elif self.tipo == self.Tipo.VALOR_FIXO:
            desconto = self.valor
        else:  # FRETE_GRATIS não desconta do subtotal
            desconto = Decimal("0")
        return min(subtotal, desconto).quantize(Decimal("0.01"))

    @property
    def frete_gratis(self):
        return self.tipo == self.Tipo.FRETE_GRATIS
