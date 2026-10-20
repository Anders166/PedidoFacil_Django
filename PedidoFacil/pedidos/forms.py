from django import forms

from pedidofacil.forms_mixins import BootstrapFormMixin
from .models import Pedido


class PedidoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["numero_pedido", "cliente", "descripcion", "valor_total", "estado"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3, "maxlength": 500}),
            "valor_total": forms.NumberInput(attrs={"step": "0.01"}),
        }
        error_messages = {
            "numero_pedido": {"unique": "Ya existe un pedido con ese número."},
        }

    def clean_numero_pedido(self):
        return self.cleaned_data["numero_pedido"].strip()

    def clean_cliente(self):
        cliente = self.cleaned_data["cliente"].strip()
        if not cliente:
            raise forms.ValidationError("El nombre del cliente es obligatorio.")
        return cliente

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()
        if not descripcion:
            raise forms.ValidationError("La descripción del pedido es obligatoria.")
        return descripcion

    def clean_valor_total(self):
        valor = self.cleaned_data["valor_total"]
        if valor <= 0:
            raise forms.ValidationError("El valor total debe ser mayor que cero.")
        return valor


class EstadoForm(forms.Form):
    estado = forms.ChoiceField(choices=Pedido.ESTADOS)
