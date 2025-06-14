from django.shortcuts import render, redirect
from .forms import FiltroLancamentoForm
from .models import LancamentoHora
from cadastro.models import Cadastro  # Importa o modelo correto de funcionários
from .utils import gerar_dias_do_mes
from datetime import datetime

def lancamento(request):
    form = FiltroLancamentoForm(request.GET or None)
    registros = []

    if request.method == 'GET' and form.is_valid():
        funcionario = form.cleaned_data['nome']
        mes = int(form.cleaned_data['mes'])
        ano = int(form.cleaned_data['ano'])

        dias = gerar_dias_do_mes(ano, mes)

        for dia in dias:
            lancamento, _ = LancamentoHora.objects.get_or_create(
                nome=funcionario,
                data=dia['data']
            )
            registros.append({
                'dia': dia['data'],
                'dia_semana': dia['dia_semana'],
                'lancamento': lancamento,
            })

    elif request.method == 'POST':
        funcionario_id = request.POST.get('nome')
        mes = int(request.POST.get('mes'))
        ano = int(request.POST.get('ano'))

        funcionario = Cadastro.objects.get(id=funcionario_id)
        dias = gerar_dias_do_mes(ano, mes)

        for dia in dias:
            data = dia['data']
            lancamento, _ = LancamentoHora.objects.get_or_create(
                nome=funcionario,
                data=data
            )
            prefix = data.strftime('%Y-%m-%d')
            lancamento.entrada_manha = request.POST.get(f'{prefix}_entrada_manha') or None
            lancamento.saida_manha = request.POST.get(f'{prefix}_saida_manha') or None
            lancamento.entrada_tarde = request.POST.get(f'{prefix}_entrada_tarde') or None
            lancamento.saida_tarde = request.POST.get(f'{prefix}_saida_tarde') or None
            lancamento.save()

        return redirect('lancamento')

    return render(request, 'lancamento.html', {
        'form': form,
        'registros': registros,
        'funcionario_id': funcionario.id if request.method == 'GET' and form.is_valid() else '',
        'mes': mes if request.method == 'GET' and form.is_valid() else '',
        'ano': ano if request.method == 'GET' and form.is_valid() else '',
    })