import calendar
from datetime import date, datetime
from cadastro.models import Cadastro
from .models import LancamentoHora


def gerar_dias_do_mes(ano, mes):
    num_dias = calendar.monthrange(ano, mes)[1]
    dias = []
    for dia in range(1, num_dias + 1):
        d = date(ano, mes, dia)
        dias.append({
            'data': d,
            'dia_semana': d.strftime('%A'),
        })
    return dias


def diferencas_por_ponto(self):
    pontos = [
        ('Entrada manhã', self.JORNADA_ENTRADA_MANHA, self.entrada_manha),
        ('Saída manhã', self.JORNADA_SAIDA_MANHA, self.saida_manha),
        ('Entrada tarde', self.JORNADA_ENTRADA_TARDE, self.entrada_tarde),
        ('Saída tarde', self.JORNADA_SAIDA_TARDE, self.saida_tarde),
    ]

    resultado = []

    for label, previsto, real in pontos:
        if real is None:
            resultado.append({
                'horario': label,
                'previsto': previsto.strftime('%H:%M'),
                'real': '---',
                'diferenca': '---',
                'tipo': 'Sem registro'
            })
            continue

        dt_real = datetime.combine(self.data, real)
        dt_previsto = datetime.combine(self.data, previsto)
        diff = int((dt_real - dt_previsto).total_seconds() // 60)

        tipo = 'Hora extra' if diff < 0 else 'Atraso' if diff > 0 else 'Pontual'
        sinal = '+' if diff > 0 else '-' if diff < 0 else ''
        resultado.append({
            'horario': label,
            'previsto': previsto.strftime('%H:%M'),
            'real': real.strftime('%H:%M'),
            'diferenca': f'{sinal}{abs(diff)} min',
            'tipo': tipo,
        })

    return resultado