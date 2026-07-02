"""Gestão administrativa de pedidos (/admin/pedidos/).

Pedidos têm regras de transição e snapshots: continuam como function
views para deixar as transições de status óbvias no código.
"""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import staff_required

from . import services
from .models import Pedido


@staff_required
def listagem(request):
    pedidos = Pedido.objects.select_related("cliente").all()
    status = request.GET.get("status") or ""
    termo = (request.GET.get("q") or "").strip()
    if status:
        pedidos = pedidos.filter(status=status)
    if termo:
        pedidos = pedidos.filter(
            Q(codigo__icontains=termo)
            | Q(comprador_nome__icontains=termo)
            | Q(comprador_email__icontains=termo)
        )
    pagina = Paginator(pedidos, 20).get_page(request.GET.get("page"))
    return render(request, "admin_dashboard/pedidos/listagem.html", {
        "pagina": pagina,
        "termo": termo,
        "status_atual": status,
        "status_choices": Pedido.Status.choices,
    })


@staff_required
def detalhe(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente", "cupom").prefetch_related(
            "itens", "historico"
        ),
        pk=pk,
    )
    return render(request, "admin_dashboard/pedidos/detalhe.html", {
        "pedido": pedido,
        "status_choices": Pedido.Status.choices,
    })


def _mudar_status(request, pk, novo_status, mensagem_ok):
    pedido = get_object_or_404(Pedido, pk=pk)
    try:
        services.alterar_status(pedido, novo_status, request.user)
        messages.success(request, mensagem_ok.format(codigo=pedido.codigo))
    except services.TransicaoInvalida as e:
        messages.error(request, str(e))
    return redirect("pedidos_admin:detalhe", pk=pk)


@staff_required
@require_POST
def alterar_status(request, pk):
    novo = request.POST.get("status", "")
    if novo not in Pedido.Status.values:
        messages.error(request, "Status inválido.")
        return redirect("pedidos_admin:detalhe", pk=pk)
    return _mudar_status(request, pk, novo, "Status do pedido {codigo} atualizado.")


@staff_required
@require_POST
def cancelar(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    try:
        services.cancelar(pedido, request.user, request.POST.get("observacao", ""))
        messages.success(request, f"Pedido {pedido.codigo} cancelado.")
    except services.TransicaoInvalida as e:
        messages.error(request, str(e))
    return redirect("pedidos_admin:detalhe", pk=pk)


@staff_required
@require_POST
def marcar_pago(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    services.marcar_pago(pedido, request.user)
    messages.success(request, f"Pedido {pedido.codigo} marcado como pago.")
    return redirect("pedidos_admin:detalhe", pk=pk)


@staff_required
@require_POST
def marcar_enviado(request, pk):
    return _mudar_status(
        request, pk, Pedido.Status.ENVIADO, "Pedido {codigo} marcado como enviado."
    )


@staff_required
@require_POST
def marcar_entregue(request, pk):
    return _mudar_status(
        request, pk, Pedido.Status.ENTREGUE, "Pedido {codigo} marcado como entregue."
    )
