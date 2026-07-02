from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.security import page_get, safe_redirect_target
from pedidos.models import Pedido, gerar_idempotency_token
from produtos.models import Produto

from .cart import Carrinho
from .forms import CheckoutForm
from .services import EstoqueInsuficiente, criar_pedido

SESSAO_CHECKOUT_TOKEN = "checkout_idempotency_token"


def _checkout_token(request):
    token = request.session.get(SESSAO_CHECKOUT_TOKEN)
    if not token:
        token = gerar_idempotency_token()
        request.session[SESSAO_CHECKOUT_TOKEN] = token
        request.session.modified = True
    return token

# ─── Carrinho ────────────────────────────────────────────────────────────────


def ver_carrinho(request):
    cart = Carrinho(request)
    return render(request, "checkout/carrinho.html", {
        "itens": cart.itens(),
        "totais": cart.totais(),
    })


@require_POST
def adicionar(request, produto_id):
    cart = Carrinho(request)
    produto = get_object_or_404(Produto, pk=produto_id)
    quantidade = request.POST.get("quantidade", 1)
    ok, erro = cart.adicionar(produto, quantidade)
    if ok:
        messages.success(request, f"“{produto.nome}” adicionado ao carrinho.")
    else:
        messages.error(request, erro)
    return redirect(safe_redirect_target(request, request.POST.get("next"), "/carrinho/"))


@require_POST
def remover(request, produto_id):
    cart = Carrinho(request)
    produto = get_object_or_404(Produto, pk=produto_id)
    cart.remover(produto)
    messages.info(request, f"“{produto.nome}” removido do carrinho.")
    return redirect("checkout:carrinho")


@require_POST
def atualizar(request, produto_id):
    cart = Carrinho(request)
    produto = get_object_or_404(Produto, pk=produto_id)
    ok, erro = cart.atualizar(produto, request.POST.get("quantidade", 1))
    if not ok:
        messages.error(request, erro)
    return redirect("checkout:carrinho")


@require_POST
def limpar(request):
    Carrinho(request).limpar()
    messages.info(request, "Carrinho esvaziado.")
    return redirect("checkout:carrinho")


@require_POST
def aplicar_cupom(request):
    cart = Carrinho(request)
    ok, erro = cart.aplicar_cupom(request.POST.get("codigo", ""))
    if ok:
        messages.success(request, "Cupom aplicado!")
    else:
        messages.error(request, erro)
    return redirect("checkout:carrinho")


@require_POST
def remover_cupom(request):
    Carrinho(request).remover_cupom()
    messages.info(request, "Cupom removido.")
    return redirect("checkout:carrinho")


# ─── Checkout ────────────────────────────────────────────────────────────────


def checkout(request):
    cart = Carrinho(request)
    if cart.vazio():
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect("produtos:listagem")

    inicial = {}
    cliente = getattr(request.user, "cliente", None) if request.user.is_authenticated else None
    if cliente:
        inicial = {
            "nome": cliente.nome, "email": cliente.email, "telefone": cliente.telefone,
            "cpf": cliente.cpf, "cep": cliente.cep, "rua": cliente.rua,
            "numero": cliente.numero, "complemento": cliente.complemento,
            "bairro": cliente.bairro, "cidade": cliente.cidade, "estado": cliente.estado,
        }
    elif request.user.is_authenticated:
        inicial = {"nome": request.user.get_full_name(), "email": request.user.email}

    token = _checkout_token(request)
    form = CheckoutForm(request.POST or None, initial=inicial)
    if request.method == "POST" and form.is_valid():
        token = request.POST.get("idempotency_token") or token
        try:
            pedido = criar_pedido(cart, form.cleaned_data, request.user, token)
        except EstoqueInsuficiente as e:
            messages.error(request, str(e))
            return redirect("checkout:carrinho")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("checkout:carrinho")
        cart.limpar()
        request.session.pop(SESSAO_CHECKOUT_TOKEN, None)
        return redirect("checkout:sucesso", token=pedido.recibo_token)

    return render(request, "checkout/checkout.html", {
        "form": form,
        "itens": cart.itens(),
        "totais": cart.totais(),
        "idempotency_token": token,
    })


@page_get
def sucesso(request, token):
    pedido = get_object_or_404(Pedido, recibo_token=token)
    return render(request, "checkout/sucesso.html", {"pedido": pedido})
