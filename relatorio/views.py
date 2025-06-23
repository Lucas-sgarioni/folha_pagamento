from django.shortcuts import render

def relatorio(request):
    return render(request, 'relatorio.html')


def buscar_relatorio(request):
    return render(request, 'buscar_relatorio.html')