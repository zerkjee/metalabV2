from django import forms

from clientes.models import ESTADOS_BR, somente_digitos
from core.forms import BootstrapFormMixin
from pedidos.models import Pedido


class CheckoutForm(BootstrapFormMixin, forms.Form):
    nome = forms.CharField(max_length=200)
    email = forms.EmailField()
    telefone = forms.CharField(max_length=20)
    cpf = forms.CharField(max_length=14)
    cep = forms.CharField(max_length=9)
    rua = forms.CharField(max_length=200)
    numero = forms.CharField(max_length=20)
    complemento = forms.CharField(max_length=100, required=False)
    bairro = forms.CharField(max_length=100)
    cidade = forms.CharField(max_length=100)
    estado = forms.ChoiceField(choices=ESTADOS_BR)
    metodo_pagamento = forms.ChoiceField(
        choices=Pedido.MetodoPagamento.choices, widget=forms.RadioSelect,
        initial=Pedido.MetodoPagamento.PIX_MANUAL,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # RadioSelect de pagamento não recebe as classes Bootstrap padrão
        self.fields["metodo_pagamento"].widget.attrs.pop("class", None)

    def clean_cpf(self):
        cpf = somente_digitos(self.cleaned_data["cpf"])
        if len(cpf) != 11:
            raise forms.ValidationError("CPF deve ter 11 dígitos.")
        return cpf

    def clean_cep(self):
        cep = somente_digitos(self.cleaned_data["cep"])
        if len(cep) != 8:
            raise forms.ValidationError("CEP deve ter 8 dígitos.")
        return cep

    def clean_telefone(self):
        tel = somente_digitos(self.cleaned_data["telefone"])
        if len(tel) < 10:
            raise forms.ValidationError("Telefone incompleto (inclua o DDD).")
        return tel
