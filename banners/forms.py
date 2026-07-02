from django import forms

from core.forms import BootstrapFormMixin
from core.security import validate_image_upload

from .models import Banner


class BannerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Banner
        fields = ["titulo", "subtitulo", "imagem", "link", "texto_botao", "ativo", "ordem"]

    def clean_imagem(self):
        return validate_image_upload(self.cleaned_data.get("imagem"))
