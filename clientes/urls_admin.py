from django.urls import path

from . import views_admin

app_name = "clientes_admin"

urlpatterns = [
    path("", views_admin.Listagem.as_view(), name="listagem"),
    path("novo/", views_admin.Novo.as_view(), name="novo"),
    path("<int:pk>/", views_admin.Detalhe.as_view(), name="detalhe"),
    path("<int:pk>/editar/", views_admin.Editar.as_view(), name="editar"),
    path("<int:pk>/excluir/", views_admin.Excluir.as_view(), name="excluir"),
]
