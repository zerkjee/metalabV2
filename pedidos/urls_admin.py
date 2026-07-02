from django.urls import path

from . import views_admin

app_name = "pedidos_admin"

urlpatterns = [
    path("", views_admin.listagem, name="listagem"),
    path("<int:pk>/", views_admin.detalhe, name="detalhe"),
    path("<int:pk>/status/", views_admin.alterar_status, name="status"),
    path("<int:pk>/cancelar/", views_admin.cancelar, name="cancelar"),
    path("<int:pk>/marcar-pago/", views_admin.marcar_pago, name="marcar_pago"),
    path("<int:pk>/marcar-enviado/", views_admin.marcar_enviado, name="marcar_enviado"),
    path("<int:pk>/marcar-entregue/", views_admin.marcar_entregue, name="marcar_entregue"),
]
