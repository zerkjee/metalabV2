from django.shortcuts import render

from accounts.decorators import staff_required

from . import services


@staff_required
def dashboard(request):
    return render(request, "admin_dashboard/dashboard.html", {
        "resumo": services.resumo_dashboard(),
        "por_status": services.pedidos_por_status(),
        "pedidos_recentes": services.pedidos_recentes(),
        "baixo_estoque": services.produtos_baixo_estoque(5),
    })


@staff_required
def relatorios(request):
    return render(request, "admin_dashboard/relatorios.html", {
        "resumo": services.resumo_dashboard(),
        "por_status": services.pedidos_por_status(),
        "mais_vendidos": services.produtos_mais_vendidos(),
        "baixo_estoque": services.produtos_baixo_estoque(),
    })
