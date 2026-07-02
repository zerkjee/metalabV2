from django.shortcuts import render
from django.http import HttpResponseForbidden

from banners.models import Banner
from core.security import page_get
from produtos.models import Produto


@page_get
def home(request):
    banners = Banner.objects.filter(ativo=True)
    destaques = Produto.objects.destaques().select_related("categoria")[:8]
    novidades = Produto.objects.publicos().order_by("-criado_em")[:8]
    inovitann = (
        Produto.objects.publicos()
        .filter(marca="Inovitann Clinical")
        .exclude(imagem_principal="")
        .exclude(nome__istartswith="kit")[:4]
    )
    return render(request, "home.html", {
        "banners": banners,
        "destaques": destaques,
        "novidades": novidades,
        "inovitann": inovitann,
    })


@page_get
def sobre(request):
    return render(request, "core/sobre.html")


@page_get
def contato(request):
    return render(request, "core/contato.html")


def erro_404(request, exception):
    return render(request, "404.html", status=404)


def erro_500(request):
    return render(request, "500.html", status=500)


def csrf_failure(request, reason=""):
    return HttpResponseForbidden("Requisicao bloqueada por seguranca.")
