from django.shortcuts import render
from cadastros.models import Categoria, Produto, Cliente

def home_dashboard(request):
    # Contamos apenas os ativos para os indicadores
    total_clientes = Cliente.objects.filter(situacao=True).count()
    total_produtos = Produto.objects.filter(situacao=True).count()
    total_categorias = Categoria.objects.count()

    contexto = {
        'total_clientes': total_clientes,
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
    }
    return render(request, 'cadastros/dashboard.html', contexto)