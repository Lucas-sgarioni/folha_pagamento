import calendar
from datetime import date

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