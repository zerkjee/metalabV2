from django.conf import settings

from produtos.models import Categoria


def loja(request):
    """Dados globais: nome da loja e categorias ativas para o menu."""
    return {
        "LOJA_NOME": settings.LOJA_NOME,
        "categorias_menu": Categoria.objects.filter(ativa=True),
    }
