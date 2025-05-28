from django.shortcuts import render
from cadastro.forms import CadastrarForm, EditarForm


def cadastrar(request):
    contexto = {'sucesso' : False}
    forms = CadastrarForm(request.POST or None)
    if forms.is_valid():
        forms.save()
        contexto['sucesso'] = True
    contexto['form'] = forms
    return render(request, 'cadastro.html', contexto)

def editar(request):
    contexto = {'sucesso' : False}
    forms = EditarForm(request.POST or None)
    if forms.is_valid():
        forms.save()
        contexto['sucesso'] = True
    contexto['form'] = forms
    return render(request, 'editar.html', contexto)