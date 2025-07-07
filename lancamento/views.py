from django.shortcuts import render
from .forms import FiltroLancamentoForm
from .models import LancamentoHora
from cadastro.models import Cadastro
from .utils import gerar_dias_do_mes
from datetime import datetime
from decimal import Decimal

def is_final_de_semana(data):
    return data.weekday() in (5, 6)

def parse_time(valor):
    try:
        return datetime.strptime(valor, "%H:%M").time()
    except (ValueError, TypeError):
        return None

# 🔹 Nova função auxiliar
def carregar_registros(funcionario, ano, mes):
    dias = gerar_dias_do_mes(ano, mes)
    registros = []

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

    return registros

# 🔹 View principal refatorada
def lancamento(request):
    form = FiltroLancamentoForm(request.GET or None)
    registros = []
    funcionario = None
    mes = ano = None

    if request.method == 'GET' and form.is_valid():
        funcionario = form.cleaned_data['nome']
        mes = int(form.cleaned_data['mes'])
        ano = int(form.cleaned_data['ano'])
        registros = carregar_registros(funcionario, ano, mes)

    elif request.method == 'POST':
        funcionario_id = request.POST.get('nome')
        mes_str = request.POST.get('mes')
        ano_str = request.POST.get('ano')

        if not funcionario_id or not mes_str or not ano_str:
            return render(request, 'lancamento.html', {
                'form': form,
                'registros': [],
                'funcionario_id': '',
                'mes': '',
                'ano': '',
                'erro': 'Funcionário, mês e ano são obrigatórios.'
            })

        mes = int(mes_str)
        ano = int(ano_str)
        funcionario = Cadastro.objects.get(id=funcionario_id)
        dias = gerar_dias_do_mes(ano, mes)

        for dia in dias:
            data = dia['data']
            prefix = data.strftime('%Y-%m-%d')

            entrada_manha = parse_time(request.POST.get(f'{prefix}_entrada_manha'))
            saida_manha = parse_time(request.POST.get(f'{prefix}_saida_manha'))
            entrada_tarde = parse_time(request.POST.get(f'{prefix}_entrada_tarde'))
            saida_tarde = parse_time(request.POST.get(f'{prefix}_saida_tarde'))

            hora_extra_total_checkbox = request.POST.get(f'{prefix}_hora_extra_total') == 'on'
            hora_extra_total = is_final_de_semana(data) or hora_extra_total_checkbox

            if entrada_manha or saida_manha or entrada_tarde or saida_tarde or hora_extra_total:
                lancamento, _ = LancamentoHora.objects.get_or_create(
                    nome=funcionario,
                    data=data
                )
                lancamento.entrada_manha = entrada_manha
                lancamento.saida_manha = saida_manha
                lancamento.entrada_tarde = entrada_tarde
                lancamento.saida_tarde = saida_tarde

                if hora_extra_total:
                    def calcular_periodo(h1, h2):
                        if h1 and h2:
                            return (datetime.combine(data, h2) - datetime.combine(data, h1)).total_seconds() / 60
                        return 0

                    total_minutos = (
                        calcular_periodo(entrada_manha, saida_manha)
                        + calcular_periodo(entrada_tarde, saida_tarde)
                    )
                    lancamento.horas_extras = Decimal(round(total_minutos / 60, 2))
                    lancamento.horas_atraso = Decimal(0)
                else:
                    extra, atraso = lancamento.calcular_horas()
                    lancamento.horas_extras = Decimal(extra)
                    lancamento.horas_atraso = Decimal(atraso)

                lancamento.save()

        registros = carregar_registros(funcionario, ano, mes)
        form = FiltroLancamentoForm(initial={
            'nome': funcionario.id,
            'mes': mes,
            'ano': ano,
        })

    return render(request, 'lancamento.html', {
        'form': form,
        'registros': registros,
        'funcionario_id': funcionario.id if funcionario else '',
        'mes': mes,
        'ano': ano,
    })