"""CRUD administrativo de cupons (/admin/cupons/).

Reaproveita as views base de core.admin_views para evitar duplicação.
"""

from core.admin_views import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseToggleAtivoView,
    BaseUpdateView,
)

from .forms import CupomForm
from .models import Cupom


class Listagem(BaseListView):
    model = Cupom
    template_name = "admin_dashboard/cupons/listagem.html"
    namespace_url = "cupons_admin"
    ordering = "-criado_em"
    search_fields: list = []
    extra_context = {}


class Novo(BaseCreateView):
    form_class = CupomForm
    template_name = "admin_dashboard/cupons/form.html"
    namespace_url = "cupons_admin"
    titulo_novo = "Novo cupom"


class Editar(BaseUpdateView):
    form_class = CupomForm
    template_name = "admin_dashboard/cupons/form.html"
    namespace_url = "cupons_admin"
    titulo_editar_prefix = "Editar"


class Excluir(BaseDeleteView):
    model = Cupom
    namespace_url = "cupons_admin"
    success_message = "excluído"
    soft_delete_message = "tem pedidos vinculados; foi desativado"
    protected_relations = ["pedidos"]


class Ativar(BaseToggleAtivoView):
    model = Cupom
    namespace_url = "cupons_admin"

    def post(self, request, pk):
        self.kwargs["ativar"] = True
        return super().post(request, pk)


class Desativar(BaseToggleAtivoView):
    model = Cupom
    namespace_url = "cupons_admin"

    def post(self, request, pk):
        self.kwargs["ativar"] = False
        return super().post(request, pk)
