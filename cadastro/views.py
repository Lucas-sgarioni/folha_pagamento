from django.shortcuts import render, get_object_or_404, redirect
from cadastro.forms import CadastrarForm
from cadastro.models import Cadastro


def cadastrar(request):
    contexto = {'sucesso' : False}
    forms = CadastrarForm(request.POST or None)
    if forms.is_valid():
        forms.save()
        contexto['sucesso'] = True
    contexto['form'] = forms
    return render(request, 'cadastro.html', contexto)

def buscar_funcionario(request):
    query = request.GET.get('q')
    resultado = None
    if query:
        resultado = Cadastro.objects.filter(nome__icontains=query) | Cadastro.objects.filter(cpf__icontains=query)
    return render(request, 'buscar_funcionario.html', {'resultado': resultado})

def editar_funcionario(request, pk):
    funcionario = get_object_or_404(Cadastro, pk=pk)
    if request.method == 'POST':
        form = CadastrarForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('buscar_funcionario')  # redireciona para a busca novamente
    else:
        form = CadastrarForm(instance=funcionario)
    return render(request, 'editar_funcionario.html', {'form': form, 'funcionario': funcionario})