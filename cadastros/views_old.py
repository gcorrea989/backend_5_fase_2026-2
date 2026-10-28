from django.shortcuts import render, redirect
from .models import Categoria, Produto, Cliente
from .forms import ProdutoForm # Importe o formulário criado
from icecream import ic

def demonstracao_orm(request):
    print("\n" + "="*40)
    print("NOVA REQUISIÇÃO HTTP:")
    print("="*40)

    # 1. O básico usando print normal
    print("MÉTODO HTTP:", request.method) # Vai imprimir GET
    print("CAMINHO ACESSADO:", request.path) # Vai imprimir /cadastros/orm/
    
    # Explicando os Headers (Cabeçalhos HTTP)
    print("NAVEGADOR DO USUÁRIO:", request.META.get('HTTP_USER_AGENT'))

    # 2. O modo Pro usando IceCream
    print("\n--- Analisando com IceCream ---")
    
    # O ic() imprime o nome da variável, o número da linha e o valor formatado
    ic(request.GET)  # Dicionário com os parâmetros da URL (ex: ?busca=teste)
    ic(request.user) # Mostra se o usuário está logado (AnonymousUser ou o admin)
    ic(request.user.is_authenticated) # Retorna True ou False
    
    print("="*40 + "\n")

    # 1. Equivalente a: SELECT * FROM produto;
    todos = Produto.objects.all()

    # 2. Equivalente a: SELECT * FROM produto WHERE quantidade_estoque > 0;
    # Explique o uso dos dois underlines (__) para chamar operadores 
    # como 'gt' (Greater Than = Maior que)
    em_estoque = Produto.objects.filter(quantidade_estoque__gt=0)

    # 3. Equivalente a: SELECT * FROM produto WHERE preco <= 50.00;
    # 'lte' (Less Than or Equal = Menor ou igual)
    baratos = Produto.objects.filter(preco__lte=50.00)

    # 4. Equivalente a: SELECT * FROM produto WHERE nome ILIKE '%teclado%';
    # 'icontains' faz uma busca por texto ignorando maiúsculas e minúsculas
    busca_texto = Produto.objects.filter(nome__icontains='teclado')

    # 5. O PODER DO ORM (JOIN Implícito)
    # Equivalente a: SELECT p.* FROM produto p INNER JOIN categoria c 
    # ON p.categoria_id = c.id WHERE c.nome = 'Eletrônicos';
    # Navegamos da tabela Produto para a tabela Categoria usando dois underlines!
    por_categoria = Produto.objects.filter(categoria__nome='Eletrônicos')

    # Dicionário de contexto: enviando as variáveis do Python para o HTML
    contexto = {
        'todos': todos,
        'em_estoque': em_estoque,
        'baratos': baratos,
        'busca_texto': busca_texto,
        'por_categoria': por_categoria,
        'titulo_pagina': 'Demonstração Na unha do ORM Django',
    }

    return render(request, 'demonstracao_orm.html', contexto) 


def listagem_clientes(request):
    # buscamos todos os clientes ativos do banco de dados
    # (lembre de importar os clientes no começo do arquivo)
    clientes_ativos = Cliente.objects.filter(situacao=True)
    contexto = {
        'clientes': clientes_ativos
    }
    # Renderiza o novo arquivo HTML
    return render(request, 'cadastros/listagem_clientes.html', contexto)


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


def cadastrar_produto(request):
    if request.method == 'POST':
        # Se o usuário enviou dados, preenchemos o formulário com o POST
        form = ProdutoForm(request.POST)
        
        # O Django executa todos os métodos clean_() e clean() aqui:
        if form.is_valid():
            form.save()
            # Redireciona para o dashboard ou lista de produtos após salvar
            return redirect('cadastros:home_dashboard') 
    else:
        # Se for um GET (acesso normal à página), cria um formulário em branco
        form = ProdutoForm()

    contexto = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Produto',
    }
    return render(request, 'cadastros/cadastrar_produto.html', contexto)

