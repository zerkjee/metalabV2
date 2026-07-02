from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("produtos/", views.produtos_lista, name="produtos"),
    path("produtos/<int:pk>/", views.produto_detalhe, name="produto"),
    path("pedidos/", views.pedidos_lista, name="pedidos"),
    path("pedidos/<int:pk>/", views.pedido_detalhe, name="pedido"),
    path("clientes/", views.clientes_lista, name="clientes"),
    path("dashboard/resumo/", views.dashboard_resumo, name="dashboard_resumo"),
]
