"""Views base para os CRUDs do painel administrativo customizado.

Centraliza o padrão repetido em produtos/cupons/banners/clientes:
  - listagem com paginação e busca simples (q)
  - criação e edição
  - exclusão com soft-delete (desativa) quando há vínculos
  - toggle ativar/desativar

Use as classes via `as_view()` em urls_admin.py. Para casos com
regras próprias (clientes que checam pedido mínimo, banners com imagem
obrigatória etc.), basta sobrescrever `form_valid` ou `get_queryset`.
"""

from urllib.parse import urlencode

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST

from accounts.decorators import staff_required

from .templatetags import paginate_url as _paginate_url_module  # noqa: F401




def _staff(method):
    return method_decorator(staff_required, name="dispatch")(method)


class BaseListView(View):
    """Listagem paginada com busca opcional (?q=).

    Subclasses devem definir:
      - model, template_name, namespace_url (ex: "produtos_admin")
      - search_fields: lista de campos para Q icontains (OR)
      - por_pagina (default 20)
    """

    model = None
    template_name = ""
    namespace_url = ""
    search_fields: list[str] = []
    por_pagina: int = 20
    extra_context: dict = {}
    select_related: list[str] = []
    ordering: str | tuple = "nome"

    def get_queryset(self):
        qs = self.model.objects.all()
        if self.select_related:
            qs = qs.select_related(*self.select_related)
        if self.ordering:
            qs = qs.order_by(*([self.ordering] if isinstance(self.ordering, str) else self.ordering))
        termo = (self.request.GET.get("q") or "").strip()
        if termo and self.search_fields:
            cond = Q()
            for campo in self.search_fields:
                cond |= Q(**{f"{campo}__icontains": termo})
            qs = qs.filter(cond)
        return qs

    @_staff
    def get(self, request):
        qs = self.get_queryset()
        pagina = Paginator(qs, self.por_pagina).get_page(request.GET.get("page"))
        ctx = {
            "pagina": pagina,
            "termo": request.GET.get("q") or "",
        }
        ctx.update(self.extra_context)
        return render(request, self.template_name, ctx)


class _FormContextMixin:
    """Resolve título e nome do objeto para os templates de form."""

    titulo_novo: str = "Novo"
    titulo_editar_prefix: str = "Editar"

    def get_titulo(self, instance=None):
        if instance and instance.pk:
            return f"{self.titulo_editar_prefix}: {instance}"
        return self.titulo_novo

    def get_form_kwargs(self):  # noqa: D401
        kwargs = super().get_form_kwargs()
        if self.request.method in ("POST", "PUT"):
            kwargs.setdefault("files", self.request.FILES)
        return kwargs

    def get_success_url(self):
        return reverse(f"{self.namespace_url}:listagem")


class _CreateOrUpdateBase:
    model = None
    form_class = None
    template_name = ""
    namespace_url = ""
    titulo_novo: str = "Novo"
    titulo_editar_prefix: str = "Editar"


@method_decorator(staff_required, name="dispatch")
class BaseCreateView(_CreateOrUpdateBase, View):
    """View de criação."""

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {
            "form": form, "titulo": self.titulo_novo,
        })

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"“{obj}” criado.")
            return redirect(self.get_success_url())
        return render(request, self.template_name, {
            "form": form, "titulo": self.titulo_novo,
        })


@method_decorator(staff_required, name="dispatch")
class BaseUpdateView(_CreateOrUpdateBase, View):
    """View de edição."""

    def _get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs["pk"])

    def get(self, request, pk):
        obj = self._get_object()
        form = self.form_class(instance=obj)
        return render(request, self.template_name, {
            "form": form, "titulo": f"{self.titulo_editar_prefix}: {obj}", "object": obj,
        })

    def post(self, request, pk):
        obj = self._get_object()
        form = self.form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"“{obj}” atualizado.")
            return redirect(self.get_success_url())
        return render(request, self.template_name, {
            "form": form, "titulo": f"{self.titulo_editar_prefix}: {obj}", "object": obj,
        })


@method_decorator([staff_required, require_POST], name="dispatch")
class BaseDeleteView(View):
    """Exclusão com soft-delete (desativa) quando há FKs protegidas.

    Subclasses devem definir `protected_relations`, lista de reverse accessors
    (ex: "pedidos"). O sufixo legado "__exists" ainda é aceito.
    O objeto é desativado (campo `ativo`) em vez de deletado se qualquer
    relação tiver registros.
    """

    model = None
    namespace_url = ""
    success_message: str = "excluído"
    soft_delete_message: str = "tem registros vinculados; foi desativado em vez de excluído"
    protected_relations: list[str] = []

    def _get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs["pk"])

    def _has_relations(self, obj) -> bool:
        for rel in self.protected_relations:
            rel = rel.removesuffix("__exists")
            related = getattr(obj, rel, None)
            if related is not None and hasattr(related, "exists"):
                if related.exists():
                    return True
                continue
            if obj.__class__.objects.filter(pk=obj.pk).filter(
                **{f"{rel}__isnull": False}
            ).exists():
                return True
        return False

    def post(self, request, pk):
        obj = self._get_object()
        label = str(obj)
        if self.protected_relations and self._has_relations(obj):
            obj.ativo = False
            obj.save(update_fields=["ativo"])
            messages.warning(request, f"“{label}” {self.soft_delete_message}.")
        else:
            obj.delete()
            messages.success(request, f"“{label}” {self.success_message}.")
        return redirect(f"{self.namespace_url}:listagem")


@method_decorator([staff_required, require_POST], name="dispatch")
class BaseToggleAtivoView(View):
    """Ativa/desativa um objeto. Use duas URLs distintas com flag `ativar`."""

    model = None
    namespace_url = ""

    def post(self, request, pk):
        ativar = self.kwargs.get("ativar", True)
        obj = get_object_or_404(self.model, pk=pk)
        obj.ativo = ativar
        obj.save(update_fields=["ativo"])
        estado = "ativado" if ativar else "desativado"
        messages.success(request, f"“{obj}” {estado}.")
        return redirect(f"{self.namespace_url}:listagem")
