from django import forms
from datetime import datetime

MESES = [(str(i), nome) for i, nome in enumerate([
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
], 1)]

ANOS = [(ano, ano) for ano in range(datetime.now().year, 2020, -1)]

class FiltroRelatorioForm(forms.Form):
    mes = forms.ChoiceField(choices=MESES, label="Mês")
    ano = forms.ChoiceField(choices=ANOS, label="Ano")