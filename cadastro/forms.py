from django import forms
from cadastro.models import Cadastro
from cadastro.fields import MoneyFormField

class CadastrarForm(forms.ModelForm):
    valor_hora = MoneyFormField(label='Valor Hora')
    salario_base = MoneyFormField(label='Salário Base')
    valor_cartao = MoneyFormField(label='Valor Cartão')

    class Meta:
        model = Cadastro
        fields = [
            'nome',
            'cpf',
            'salario_base',
            'valor_hora',
            'valor_cartao',
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
