from django.shortcuts import render
from cadastros.models import Cliente

def listagem_clientes(request):
    # buscamos todos os clientes ativos do banco de dados
    clientes_ativos = Cliente.objects.filter(situacao=True)
    contexto = {
        'clientes': clientes_ativos
    }
    return render(request, 'cadastros/listagem_clientes.html', contexto)