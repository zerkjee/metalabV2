"""
Rotas principais do projeto.

Convenção:
    /                → páginas públicas (core, produtos, checkout)
    /admin/          → painel administrativo customizado (staff)
    /django-admin/   → Django Admin nativo
    /api/            → API interna JSON
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin nativo
    path("django-admin/", admin.site.urls),
    # Públicas
    path("", include("core.urls")),
    path("", include("accounts.urls")),
    path("", include("produtos.urls")),
    path("", include("checkout.urls")),
    # Painel administrativo customizado
    path("admin/", include("relatorios.urls")),          # /admin/ e /admin/dashboard/ e /admin/relatorios/
    path("admin/produtos/", include("produtos.urls_admin")),
    path("admin/pedidos/", include("pedidos.urls_admin")),
    path("admin/clientes/", include("clientes.urls_admin")),
    path("admin/cupons/", include("cupons.urls_admin")),
    path("admin/banners/", include("banners.urls_admin")),
    # API interna
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.erro_404"
handler500 = "core.views.erro_500"
