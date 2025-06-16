from django import forms
from cadastro.models import Cadastro  # importa da app correta
from datetime import datetime

MESES_CHOICES = [
    ('1', 'Janeiro'),
    ('2', 'Fevereiro'),
    ('3', 'Março'),
    ('4', 'Abril'),
    ('5', 'Maio'),
    ('6', 'Junho'),
    ('7', 'Julho'),
    ('8', 'Agosto'),
    ('9', 'Setembro'),
    ('10', 'Outubro'),
    ('11', 'Novembro'),
    ('12', 'Dezembro'),
]

ANO_CHOICES = [
    (a, str(a)) for a in range(datetime.now().year, 2020, -1)
]

class FiltroLancamentoForm(forms.Form):
    nome = forms.ModelChoiceField(queryset=Cadastro.objects.order_by('nome'), label='Funcionário')
    mes = forms.ChoiceField(choices=MESES_CHOICES, label='Mês')
    ano = forms.ChoiceField(choices=ANO_CHOICES, label='Ano')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].queryset = Cadastro.objects.filter(situacao_cadastro='AT').order_by('nome')