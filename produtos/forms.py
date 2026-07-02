from django import forms

from core.forms import BootstrapFormMixin
from core.security import validate_image_upload

from .models import Categoria, Produto


class ProdutoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome", "sku", "marca", "categoria", "descricao_curta",
            "descricao_completa", "composicao", "modo_uso", "aviso_legal",
            "preco", "preco_promocional", "estoque", "estoque_minimo",
            "peso", "altura", "largura", "comprimento",
            "cor_principal", "cor_secundaria", "meta_titulo", "meta_descricao",
            "imagem_principal", "imagem_2", "imagem_3", "imagem_4",
            "ativo", "destaque",
        ]
        widgets = {
            "cor_principal": forms.TextInput(attrs={"type": "color"}),
            "cor_secundaria": forms.TextInput(attrs={"type": "color"}),
        }

    def clean_imagem_principal(self):
        return validate_image_upload(self.cleaned_data.get("imagem_principal"))

    def clean_imagem_2(self):
        return validate_image_upload(self.cleaned_data.get("imagem_2"))

    def clean_imagem_3(self):
        return validate_image_upload(self.cleaned_data.get("imagem_3"))

    def clean_imagem_4(self):
        return validate_image_upload(self.cleaned_data.get("imagem_4"))


class CategoriaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome", "descricao", "ativa", "ordem"]
