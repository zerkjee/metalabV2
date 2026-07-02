from django.urls import path

from . import views

app_name = "checkout"

urlpatterns = [
    path("carrinho/", views.ver_carrinho, name="carrinho"),
    path("carrinho/adicionar/<int:produto_id>/", views.adicionar, name="adicionar"),
    path("carrinho/remover/<int:produto_id>/", views.remover, name="remover"),
    path("carrinho/atualizar/<int:produto_id>/", views.atualizar, name="atualizar"),
    path("carrinho/limpar/", views.limpar, name="limpar"),
    path("carrinho/aplicar-cupom/", views.aplicar_cupom, name="aplicar_cupom"),
    path("carrinho/remover-cupom/", views.remover_cupom, name="remover_cupom"),
    path("checkout/", views.checkout, name="checkout"),
    path("pedido/sucesso/<str:token>/", views.sucesso, name="sucesso"),
]
