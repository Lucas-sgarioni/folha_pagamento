from django.shortcuts import render, redirect
from .forms import FiltroLancamentoForm
from .models import LancamentoHora
from cadastro.models import Cadastro
from .utils import gerar_dias_do_mes
from datetime import datetime
from decimal import Decimal


def parse_time(valor):
    try:
        return datetime.strptime(valor, "%H:%M").time()
    except (ValueError, TypeError):
        return None


def lancamento(request):
    form = FiltroLancamentoForm(request.GET or None)
    registros = []
    funcionario = None

    if request.method == 'GET' and form.is_valid():
        funcionario = form.cleaned_data['nome']
        mes = int(form.cleaned_data['mes'])
        ano = int(form.cleaned_data['ano'])

        dias = gerar_dias_do_mes(ano, mes)

        for dia in dias:
            lancamento = LancamentoHora.objects.filter(
                nome=funcionario,
                data=dia['data']
            ).first()

            registros.append({
                'dia_semana': dia['dia_semana'],
                'dia': dia['data'],
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
            prefix = data.strftime('%Y-%m-%d')

            entrada_manha = parse_time(request.POST.get(f'{prefix}_entrada_manha'))
            saida_manha = parse_time(request.POST.get(f'{prefix}_saida_manha'))
            entrada_tarde = parse_time(request.POST.get(f'{prefix}_entrada_tarde'))
            saida_tarde = parse_time(request.POST.get(f'{prefix}_saida_tarde'))

            # Verifica checkbox "dia todo como hora extra"
            hora_extra_total = request.POST.get(f'{prefix}_hora_extra_total') == 'on'

            if entrada_manha or saida_manha or entrada_tarde or saida_tarde or hora_extra_total:
                lancamento, created = LancamentoHora.objects.get_or_create(
                    nome=funcionario,
                    data=data
                )
                lancamento.entrada_manha = entrada_manha
                lancamento.saida_manha = saida_manha
                lancamento.entrada_tarde = entrada_tarde
                lancamento.saida_tarde = saida_tarde

                if hora_extra_total:
                    total_minutos = 0
                    for h1, h2 in [(entrada_manha, saida_manha), (entrada_tarde, saida_tarde)]:
                        if h1 and h2:
                            delta = (datetime.combine(data, h2) - datetime.combine(data, h1)).total_seconds() / 60
                            total_minutos += delta

                    lancamento.horas_extras = Decimal(round(total_minutos / 60, 2))
                    lancamento.horas_atraso = Decimal(0)
                    # Salva sem recalcular para usar o valor manual
                    lancamento.save()
                else:
                    # Salva normalmente, disparando o cálculo do save()
                    lancamento.save()

        return redirect('lancamento')

    return render(request, 'lancamento.html', {
        'form': form,
        'registros': registros,
        'funcionario_id': funcionario.id if funcionario else '',
        'mes': mes if request.method == 'GET' and form.is_valid() else '',
        'ano': ano if request.method == 'GET' and form.is_valid() else '',
    })
