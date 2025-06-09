from django.shortcuts import render

from django.urls import reverse

def inicio(request):
    dados = []
    # Cada item dado aqui gerará um quadro no template inicial.
    dados.append({
        'titulo': 'Cadastro de funcionários',
        'botoes': [
            {'nome': 'Cadastrar', 'link': reverse('cadastro')},
            {'nome': 'Editar', 'link': reverse('buscar_funcionario')}
        ]
    })

    dados.append({
        'titulo': 'Lançamento de horas',
        'descricao': 'Realizar o lançamento de horas trabalhadas ou editar horários lançados',
        'botoes': [
            {'nome': 'Lançar Horas', 'link': reverse('lancamento')}
        ]
    })

    dados.append({
        'titulo': 'Relatórios',
        'descricao': 'Gerar o relatório de horas trabalhadas e horas extras a receber',
        'botoes': [
            {'nome': 'Ver Relatórios', 'link': reverse('relatorio')}
        ]
    })
    
    contexto = {
        'dados' : dados
    }
    return render(request, 'inicio.html', contexto)
