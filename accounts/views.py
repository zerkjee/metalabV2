from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from core.security import safe_redirect_target


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, "Login realizado com sucesso.")
            proximo = request.GET.get("next") or request.POST.get("next")
            destino = safe_redirect_target(request, proximo, "")
            if destino:
                return redirect(destino)
            if request.user.is_staff:
                return redirect("relatorios:dashboard")
            return redirect("core:home")
        messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "accounts/login.html", {"form": form})


@require_POST
def logout_view(request):
    auth_logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("core:home")


@login_required
def minha_conta(request):
    pedidos = []
    cliente = getattr(request.user, "cliente", None)
    if cliente:
        pedidos = cliente.pedidos.all()[:20]
    return render(request, "accounts/minha_conta.html", {
        "cliente": cliente,
        "pedidos": pedidos,
    })
