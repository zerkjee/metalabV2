"""Serviço de aplicação de cupom (usado pelo carrinho e pelo checkout)."""

from django.db.models import F

from .models import Cupom


class CupomIndisponivel(Exception):
    """Cupom deixou de estar disponivel durante a finalizacao do pedido."""


def buscar_cupom_valido(codigo, subtotal):
    """
    Busca o cupom pelo código e valida contra o subtotal.
    Retorna (cupom | None, mensagem_de_erro: str).
    """
    codigo = (codigo or "").strip().upper()
    if not codigo:
        return None, "Informe o código do cupom."
    try:
        cupom = Cupom.objects.get(codigo=codigo)
    except Cupom.DoesNotExist:
        return None, "Cupom não encontrado."
    valido, erro = cupom.validar(subtotal)
    if not valido:
        return None, erro
    return cupom, ""


def registrar_uso(cupom):
    """Incrementa usos_realizados de forma atômica ao criar um pedido."""
    qs = Cupom.objects.filter(pk=cupom.pk, ativo=True)
    if cupom.uso_maximo is not None:
        qs = qs.filter(usos_realizados__lt=F("uso_maximo"))
    atualizados = qs.update(usos_realizados=F("usos_realizados") + 1)
    if atualizados == 0:
        raise CupomIndisponivel("Este cupom atingiu o limite de usos.")
