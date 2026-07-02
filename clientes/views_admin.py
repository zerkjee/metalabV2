"""CRUD administrativo de clientes (/admin/clientes/)."""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View

from accounts.decorators import staff_required
from core.admin_views import (
    BaseCreateView,
    BaseListView,
    BaseUpdateView,
)

from .forms import ClienteForm
from .models import Cliente


class Listagem(BaseListView):
    model = Cliente
    template_name = "admin_dashboard/clientes/listagem.html"
    namespace_url = "clientes_admin"
    ordering = "nome"
    search_fields = ["nome", "email", "cpf", "telefone"]


class Novo(BaseCreateView):
    form_class = ClienteForm
    template_name = "admin_dashboard/clientes/form.html"
    namespace_url = "clientes_admin"
    titulo_novo = "Novo cliente"


class Editar(BaseUpdateView):
    form_class = ClienteForm
    template_name = "admin_dashboard/clientes/form.html"
    namespace_url = "clientes_admin"
    titulo_editar_prefix = "Editar"


@method_decorator([staff_required], name="dispatch")
class Detalhe(View):
    """Tela de detalhe não tem soft-delete (precisa de proteção custom)."""

    def get(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        return render(request, "admin_dashboard/clientes/detalhe.html", {
            "cliente": cliente,
            "pedidos": cliente.pedidos.all()[:50],
        })


@method_decorator([staff_required], name="dispatch")
class Excluir(View):
    """Clientes com pedidos não podem ser excluídos (regra explícita)."""

    def post(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        if cliente.pedidos.exists():
            messages.error(
                request,
                f"“{cliente.nome}” tem pedidos e não pode ser excluído.",
            )
            return redirect_to_detalhe(request, cliente.pk)
        cliente.delete()
        messages.success(request, f"“{cliente.nome}” excluído.")
        from django.shortcuts import redirect
        return redirect("clientes_admin:listagem")


def redirect_to_detalhe(request, pk):
    from django.shortcuts import redirect
    return redirect("clientes_admin:detalhe", pk=pk)
