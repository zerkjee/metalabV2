from django.urls import path

from . import views

app_name = "relatorios"

urlpatterns = [
    path("", views.dashboard, name="painel"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("relatorios/", views.relatorios, name="relatorios"),
]
