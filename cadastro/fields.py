from django import forms
from decimal import Decimal, InvalidOperation
import re

class MoneyFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', forms.TextInput(attrs={
            'class': 'form-control money-mask',
            'placeholder': 'R$ 0,00',
        }))
        kwargs.setdefault('label', 'Valor em Reais')
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        # Remove tudo que não for número ou vírgula
        valor = re.sub(r'[^\d,]', '', value)
        valor = valor.replace(',', '.')
        try:
            return Decimal(valor)
        except (InvalidOperation, ValueError):
            raise forms.ValidationError('Digite um valor válido em reais.')