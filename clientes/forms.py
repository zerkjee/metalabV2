from django import forms

from core.forms import BootstrapFormMixin

from .models import Cliente, somente_digitos


class ClienteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "email", "telefone", "cpf", "data_nascimento",
                  "cep", "rua", "numero", "complemento", "bairro", "cidade", "estado"]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if email:
            existe = Cliente.objects.filter(email=email).exclude(pk=self.instance.pk)
            if existe.exists():
                raise forms.ValidationError("Já existe um cliente com este e-mail.")
        return email

    def clean_cpf(self):
        cpf = somente_digitos(self.cleaned_data.get("cpf"))
        if cpf:
            if len(cpf) != 11:
                raise forms.ValidationError("CPF deve ter 11 dígitos.")
            existe = Cliente.objects.filter(cpf=cpf).exclude(pk=self.instance.pk)
            if existe.exists():
                raise forms.ValidationError("Já existe um cliente com este CPF.")
        return cpf
