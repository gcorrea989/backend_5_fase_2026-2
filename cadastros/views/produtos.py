from django.shortcuts import render, redirect
from cadastros.forms import ProdutoForm
from django.contrib.admin.views.decorators import staff_member_required
#from cadastros.decorators import login_obrigatorio_custom

@staff_member_required(login_url='cadastros:home_dashboard')
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastros:home_dashboard') 
    else:
        form = ProdutoForm()

    contexto = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Produto',
    }
    return render(request, 'cadastros/cadastrar_produto.html', contexto)