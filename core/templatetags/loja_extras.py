"""Filtros de exibição de preço (parcelamento e desconto, estilo Vitafor)."""

from decimal import ROUND_HALF_UP, Decimal

from django import template

register = template.Library()


@register.filter
def parcela(preco, vezes=3):
    """Valor de cada parcela: {{ produto.preco_atual|parcela:3 }}."""
    try:
        return (Decimal(preco) / int(vezes)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    except Exception:
        return preco


@register.filter
def desconto_pct(produto):
    """Percentual de desconto do preço promocional sobre o preço cheio."""
    try:
        if not produto.em_promocao or not produto.preco:
            return 0
        pct = (1 - produto.preco_promocional / produto.preco) * 100
        return int(pct.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    except Exception:
        return 0
