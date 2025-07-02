from django.shortcuts import render
from lancamento.models import LancamentoHora
from cadastro.models import Cadastro
from .forms import FiltroRelatorioForm
from django.db.models import Sum
from decimal import Decimal

def relatorio_mensal_consolidado(request):
    form = FiltroRelatorioForm(request.GET or None)
    resultados = []

    if form.is_valid():
        mes = int(form.cleaned_data['mes'])
        ano = int(form.cleaned_data['ano'])

        funcionarios = Cadastro.objects.filter(situacao_cadastro='AT')

        for funcionario in funcionarios:
            lancamentos = LancamentoHora.objects.filter(
                nome=funcionario,
                data__year=ano,
                data__month=mes
            )

            total_horas = lancamentos.aggregate(soma=Sum('horas_extras'))['soma'] or Decimal('0.00')
            valor_hora = funcionario.valor_hora or Decimal('0.00')
            total_receber = total_horas * valor_hora

            resultados.append({
                'funcionario': funcionario.nome,
                'valor_hora': valor_hora,
                'total_horas': total_horas,
                'total_receber': total_receber
            })

    return render(request, 'consolidado_mensal.html', {
        'form': form,
        'resultados': resultados
    })



def relatorio_funcionario_mensal(request):
    form = FiltroLancamentoForm(request.GET or None)
    registros = []
    funcionario = None
    total_extras = 0
    total_atrasos = 0
    ano = mes = None

    if request.method == 'GET' and form.is_valid():
        funcionario = form.cleaned_data['nome']
        mes = int(form.cleaned_data['mes'])
        ano = int(form.cleaned_data['ano'])

        registros = LancamentoHora.objects.filter(
            nome=funcionario,
            data__year=ano,
            data__month=mes
        ).order_by('data')

        totais = registros.aggregate(
            total_extras=Sum('horas_extras'),
            total_atrasos=Sum('horas_atraso')
        )

        total_extras = totais['total_extras'] or 0
        total_atrasos = totais['total_atrasos'] or 0

    context = {
        'form': form,
        'funcionario': funcionario,
        'registros': registros,
        'ano': ano,
        'mes': mes,
        'total_extras': total_extras,
        'total_atrasos': total_atrasos,
    }

    return render(request, 'funcionario_mensal.html', context)


def relatorio_consolidado_pdf(request, ano, mes):
    response_html = relatorio_mensal_consolidado(request, ano, mes)
    html_string = response_html.content.decode()

    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=relatorio-consolidado-{mes}-{ano}.pdf'
    return response