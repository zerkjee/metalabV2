"""CRUD administrativo de produtos (painel customizado /admin/produtos/)."""

from core.admin_views import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseToggleAtivoView,
    BaseUpdateView,
)

from .forms import ProdutoForm
from .models import Produto


class Listagem(BaseListView):
    model = Produto
    template_name = "admin_dashboard/produtos/listagem.html"
    namespace_url = "produtos_admin"
    ordering = "nome"
    search_fields = ["nome", "sku", "marca"]
    select_related = ["categoria"]


class Novo(BaseCreateView):
    form_class = ProdutoForm
    template_name = "admin_dashboard/produtos/form.html"
    namespace_url = "produtos_admin"
    titulo_novo = "Novo produto"


class Editar(BaseUpdateView):
    form_class = ProdutoForm
    template_name = "admin_dashboard/produtos/form.html"
    namespace_url = "produtos_admin"
    titulo_editar_prefix = "Editar"


class Excluir(BaseDeleteView):
    model = Produto
    namespace_url = "produtos_admin"
    success_message = "excluído"
    soft_delete_message = "tem pedidos vinculados; foi desativado em vez de excluído"
    protected_relations = ["itens_pedido"]


class Ativar(BaseToggleAtivoView):
    model = Produto
    namespace_url = "produtos_admin"

    def post(self, request, pk):
        self.kwargs["ativar"] = True
        return super().post(request, pk)


class Desativar(BaseToggleAtivoView):
    model = Produto
    namespace_url = "produtos_admin"

    def post(self, request, pk):
        self.kwargs["ativar"] = False
        return super().post(request, pk)
