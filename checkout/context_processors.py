from .cart import Carrinho


def carrinho(request):
    """Deixa a contagem de itens do carrinho disponível em todos os templates."""
    cart = Carrinho(request)
    return {"carrinho_qtd": cart.quantidade_total()}
