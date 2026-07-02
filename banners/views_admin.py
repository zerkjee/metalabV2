"""CRUD administrativo de banners (/admin/banners/)."""

from core.admin_views import BaseCreateView, BaseDeleteView, BaseListView, BaseUpdateView

from .forms import BannerForm
from .models import Banner


class Listagem(BaseListView):
    model = Banner
    template_name = "admin_dashboard/banners/listagem.html"
    namespace_url = "banners_admin"
    ordering = ("ordem", "-criado_em")
    search_fields = []


class Novo(BaseCreateView):
    form_class = BannerForm
    template_name = "admin_dashboard/banners/form.html"
    namespace_url = "banners_admin"
    titulo_novo = "Novo banner"


class Editar(BaseUpdateView):
    form_class = BannerForm
    template_name = "admin_dashboard/banners/form.html"
    namespace_url = "banners_admin"
    titulo_editar_prefix = "Editar"


class Excluir(BaseDeleteView):
    model = Banner
    namespace_url = "banners_admin"
    success_message = "excluído"
    soft_delete_message = "não pode ser desativado automaticamente"
    protected_relations = []
