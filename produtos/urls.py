from django.urls import path

from . import views

app_name = "produtos"

urlpatterns = [
    path("produtos/", views.listagem, name="listagem"),
    path("produtos/<slug:slug>/", views.detalhe, name="detalhe"),
    path("categoria/<slug:slug>/", views.categoria, name="categoria"),
    path("busca/", views.busca, name="busca"),
]
