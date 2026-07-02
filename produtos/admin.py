from django.contrib import admin

from .models import Categoria, ImagemProduto, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nome", "slug", "ativa", "ordem"]
    list_editable = ["ativa", "ordem"]
    search_fields = ["nome"]
    prepopulated_fields = {"slug": ["nome"]}


class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 0


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["nome", "sku", "categoria", "preco", "preco_promocional",
                    "estoque", "ativo", "destaque"]
    list_filter = ["ativo", "destaque", "categoria"]
    list_editable = ["ativo", "destaque"]
    search_fields = ["nome", "sku", "marca"]
    prepopulated_fields = {"slug": ["nome"]}
    inlines = [ImagemProdutoInline]
