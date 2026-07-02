from django import forms

from core.forms import BootstrapFormMixin

from .models import Cupom


class CupomForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Cupom
        fields = ["codigo", "tipo", "valor", "ativo", "data_inicio", "data_fim",
                  "uso_maximo", "valor_minimo_pedido"]
        widgets = {
            "data_inicio": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "data_fim": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        dados = super().clean()
        tipo, valor = dados.get("tipo"), dados.get("valor")
        if tipo == Cupom.Tipo.PERCENTUAL and valor is not None and valor > 100:
            self.add_error("valor", "Desconto percentual não pode passar de 100%.")
        if tipo in (Cupom.Tipo.PERCENTUAL, Cupom.Tipo.VALOR_FIXO) and not valor:
            self.add_error("valor", "Informe o valor do desconto.")
        inicio, fim = dados.get("data_inicio"), dados.get("data_fim")
        if inicio and fim and inicio >= fim:
            self.add_error("data_fim", "A data final deve ser depois da inicial.")
        return dados
