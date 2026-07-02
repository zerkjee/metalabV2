"""Proteção das rotas do painel administrativo customizado."""

from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse


def staff_required(view_func):
    """Exige usuário autenticado com is_staff=True; senão redireciona ao login."""
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url="accounts:login",
    )(view_func)


def api_staff_required(view_func):
    """Exige staff em endpoints JSON sem redirecionar para HTML."""
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"detail": "Autenticacao obrigatoria."}, status=401)
        if not user.is_staff:
            return JsonResponse({"detail": "Permissao negada."}, status=403)
        return view_func(request, *args, **kwargs)

    return wrapper
