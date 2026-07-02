from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nome", "email", "telefone_formatado", "cidade", "estado", "criado_em"]
    search_fields = ["nome", "email", "cpf", "telefone"]
    list_filter = ["estado"]
