from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from core.security import page_get

from .models import Categoria, Produto


def _paginar(request, queryset, por_pagina=12):
    paginator = Paginator(queryset, por_pagina)
    return paginator.get_page(request.GET.get("page"))


@page_get
def listagem(request):
    produtos = Produto.objects.publicos().select_related("categoria")
    return render(request, "produtos/listagem.html", {
        "pagina": _paginar(request, produtos),
        "titulo": "Todos os produtos",
    })


@page_get
def detalhe(request, slug):
    produto = get_object_or_404(
        Produto.objects.select_related("categoria"), slug=slug, ativo=True
    )
    relacionados = (
        Produto.objects.publicos()
        .filter(categoria=produto.categoria)
        .exclude(pk=produto.pk)[:4]
    )
    return render(request, "produtos/detalhe.html", {
        "produto": produto,
        "relacionados": relacionados,
    })


@page_get
def categoria(request, slug):
    cat = get_object_or_404(Categoria, slug=slug, ativa=True)
    produtos = Produto.objects.publicos().filter(categoria=cat)
    return render(request, "produtos/listagem.html", {
        "pagina": _paginar(request, produtos),
        "titulo": cat.nome,
        "categoria_atual": cat,
    })


@page_get
def busca(request):
    termo = (request.GET.get("q") or "").strip()
    produtos = Produto.objects.none()
    if termo:
        produtos = Produto.objects.publicos().filter(
            Q(nome__icontains=termo)
            | Q(descricao_curta__icontains=termo)
            | Q(sku__iexact=termo)
            | Q(marca__icontains=termo)
        )
    return render(request, "produtos/listagem.html", {
        "pagina": _paginar(request, produtos),
        "titulo": f'Busca por "{termo}"' if termo else "Busca",
        "termo_busca": termo,
    })
