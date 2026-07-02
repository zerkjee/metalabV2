"""Mixins e utilidades de formulário compartilhadas no painel admin.

Centraliza o padrão de aplicar classes Bootstrap aos widgets e evita
duplicação entre os forms dos apps (produtos, cupons, banners, clientes).
"""

from django import forms


class BootstrapFormMixin:
    """Aplica classes Bootstrap 5 aos widgets declarados em fields.

    - Checkbox/Switch -> form-check-input
    - Select          -> form-select
    - Demais          -> form-control

    Use como primeiro mixin em classes ModelForm/Form. Pode ser sobrescrito
    campo a campo nos forms concretos caso precise de widgets customizados.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            widget = campo.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs.setdefault("class", "form-select")
            else:
                widget.attrs.setdefault("class", "form-control")
