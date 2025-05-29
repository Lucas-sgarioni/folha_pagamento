from django.shortcuts import render

def relatorio(request):
    return render(request, 'relatorio.html')