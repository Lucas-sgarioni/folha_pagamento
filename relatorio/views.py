from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from lancamento.models import LancamentoHora
from lancamento.forms import FiltroLancamentoForm
from cadastro.models import Cadastro
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce

from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML


def relatorio_funcionario_mensal(request):
    # Arrumar essa parte
    form = FiltroLancamentoForm(request.GET or None)
    funcionario = None

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

        context = {
            'funcionario': funcionario,
            'registros': registros,
            'ano': ano,
            'mes': mes,
            'total_extras': totais['total_extras'] or 0,
            'total_atrasos': totais['total_atraso'] or 0,
        }

        return render(request, 'funcionario_mensal.html', context)


def relatorio_mensal_consolidado(request, ano, mes):
    funcionarios_com_lancamento = Cadastro.objects.filter(
        lancamentohora__data__year=ano,
        lancamentohora__data__month=mes
    ).annotate(
        total_horas_extras=Coalesce(Sum('lancamentohora__horas_extras'), 0),
    ).annotate(
        valor_total=ExpressionWrapper(
            F('total_horas_extras') * F('valor_hora_extra'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    context = {
        'ano': ano,
        'mes': mes,
        'funcionarios': funcionarios_com_lancamento,
    }

    return render(request, 'consolidado_mensal.html', context)


def relatorio_consolidado_pdf(request, ano, mes):
    response_html = relatorio_mensal_consolidado(request, ano, mes)
    html_string = response_html.content.decode()

    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=relatorio-consolidado-{mes}-{ano}.pdf'
    return response