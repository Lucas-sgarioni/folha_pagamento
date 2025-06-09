from django import forms
from cadastro.models import Cadastro

from decimal import Decimal
import re

class CadastrarForm(forms.ModelForm):
    valor_hora = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control money-mask',
            'placeholder': 'R$ 00,00'
        }),
        label='Valor Hora'
    )

    class Meta:
        model = Cadastro
        fields = [
            'nome',
            'cpf',
            'valor_hora',
            'modalidade_contrato',
            'situacao_cadastro',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite aqui seu nome'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control cpf-mask',
                'placeholder': '000.000.000-00'
            }),
            'modalidade_contrato': forms.Select(attrs={
                'class': 'form-select',
            }),
            'situacao_cadastro': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def clean_valor_hora(self):
        valor_str = self.cleaned_data.get('valor_hora', '')

        # Remove R$, espaços e pontos
        valor_str = re.sub(r'[^\d,]', '', valor_str)

        # Substitui vírgula por ponto
        valor_str = valor_str.replace(',', '.')

        try:
            return Decimal(valor_str)
        except Exception:
            raise forms.ValidationError('Digite um valor válido em reais.')

