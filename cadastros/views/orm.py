from django.shortcuts import render
from cadastros.models import Produto
from icecream import ic

def demonstracao_orm(request):
    print("\n" + "="*40)
    print("NOVA REQUISIÇÃO HTTP:")
    print("="*40)

    print("MÉTODO HTTP:", request.method) 
    print("CAMINHO ACESSADO:", request.path) 
    print("NAVEGADOR DO USUÁRIO:", request.META.get('HTTP_USER_AGENT'))

    print("\n--- Analisando com IceCream ---")
    ic(request.GET)  
    ic(request.user) 
    ic(request.user.is_authenticated) 
    print("="*40 + "\n")

    todos = Produto.objects.all()
    em_estoque = Produto.objects.filter(quantidade_estoque__gt=0)
    baratos = Produto.objects.filter(preco__lte=50.00)
    busca_texto = Produto.objects.filter(nome__icontains='teclado')
    por_categoria = Produto.objects.filter(categoria__nome='Eletrônicos')

    contexto = {
        'todos': todos,
        'em_estoque': em_estoque,
        'baratos': baratos,
        'busca_texto': busca_texto,
        'por_categoria': por_categoria,
        'titulo_pagina': 'Demonstração Na unha do ORM Django',
    }

    return render(request, 'demonstracao_orm.html', contexto)