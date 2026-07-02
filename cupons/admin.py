from django.contrib import admin

from .models import Cupom


@admin.register(Cupom)
class CupomAdmin(admin.ModelAdmin):
    list_display = ["codigo", "tipo", "valor", "ativo", "data_inicio", "data_fim",
                    "usos_realizados", "uso_maximo"]
    list_filter = ["tipo", "ativo"]
    search_fields = ["codigo"]
