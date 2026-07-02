from django.contrib import admin

from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["__str__", "ativo", "ordem", "criado_em"]
    list_editable = ["ativo", "ordem"]
