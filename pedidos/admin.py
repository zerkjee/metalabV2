from django.contrib import admin

from .models import HistoricoStatus, ItemPedido, Pedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ["nome_produto_snapshot", "sku_snapshot", "preco_unitario", "subtotal"]


class HistoricoStatusInline(admin.TabularInline):
    model = HistoricoStatus
    extra = 0
    readonly_fields = ["status_anterior", "status_novo", "usuario", "observacao", "criado_em"]
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["codigo", "comprador_nome", "status", "status_pagamento",
                    "total", "criado_em"]
    list_filter = ["status", "status_pagamento", "metodo_pagamento"]
    search_fields = ["codigo", "comprador_nome", "comprador_email"]
    readonly_fields = ["codigo", "subtotal", "desconto", "frete", "total", "criado_em"]
    inlines = [ItemPedidoInline, HistoricoStatusInline]
