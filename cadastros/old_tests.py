from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from cadastros.models import Produto, Cliente, Categoria
from cadastros.forms import ProdutoForm
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class ProdutoFormTest(TestCase):
    
    # 1. O Caminho Triste (Testando falhas esperadas)
    def test_nao_deve_permitir_preco_zero_ou_negativo(self):
        # Simulamos os dados vindos de um formulário HTML
        dados = {
            'slug': 'teclado', 'nome': 'Teclado', 
            'preco': 0, # Erro intencional
            'quantidade_estoque': 10, 'situacao': True
        }
        form = ProdutoForm(data=dados)
        
        # O formulário NÃO deve ser válido
        self.assertFalse(form.is_valid())
        # A mensagem de erro deve estar no campo preço
        self.assertIn('preco', form.errors)

    def test_nao_deve_ativar_produto_com_estoque_zero(self):
        dados = {
            'slug': 'mouse', 'nome': 'Mouse', 
            'preco': 50.00, 
            'quantidade_estoque': 0, # Sem estoque
            'situacao': True         # Tentando ativar
        }
        form = ProdutoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors) # Erro global do método clean()

    # 2. O Caminho Feliz (Testando o sucesso)
    def test_deve_aceitar_produto_valido(self):
        # Precisamos de uma categoria pois o model exige
        categoria = Categoria.objects.create(nome="Periféricos")
        
        dados = {
            'slug': 'monitor', 'nome': 'Monitor', 
            'preco': 800.00, 'quantidade_estoque': 5, 
            'situacao': True, 'categoria': categoria.id
        }
        form = ProdutoForm(data=dados)
        self.assertTrue(form.is_valid())

class ViewsProtegidasTest(TestCase):
    def setUp(self):
        # setUp roda antes de CADA teste para preparar o ambiente
        self.cliente_comum = User.objects.create_user(username='comum', password='123', is_staff=False)
        self.admin = User.objects.create_user(username='admin', password='123', is_staff=True)
        self.url = reverse('cadastros:cadastrar_produto') # Busca a URL pelo nome configurado

    # Caminho Triste
    def test_usuario_anonimo_deve_ser_redirecionado(self):
        resposta = self.client.get(self.url)
        # 302 é o código HTTP para redirecionamento
        self.assertEqual(resposta.status_code, 302) 

    def test_cliente_comum_deve_ser_redirecionado(self):
        self.client.login(username='comum', password='123')
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 302)

    # Caminho Feliz
    def test_admin_deve_acessar_tela_de_cadastro(self):
        self.client.login(username='admin', password='123')
        resposta = self.client.get(self.url)
        # 200 é o código HTTP para sucesso (página carregada)
        self.assertEqual(resposta.status_code, 200)
        # Verifica se o formulário foi renderizado no HTML
        self.assertTemplateUsed(resposta, 'cadastros/cadastrar_produto.html')


class PedidoAPITest(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.usuario = User.objects.create_user(username='api_user', password='123')
        self.token = Token.objects.create(user=self.usuario)
        
        # Criando dados dependentes
        self.cliente_db = Cliente.objects.create(cnpj='111', nome='Empresa X', email='x@x.com')
        self.produto_db = Produto.objects.create(slug='hd', nome='HD', preco=100.00, situacao=True)
        self.url = reverse('cadastros:api_pedidos')

    # Caminho Triste
    def test_api_deve_rejeitar_pedido_sem_token(self):
        dados = {'cliente': '111', 'produto': 'hd', 'quantidade': 2}
        resposta = self.api_client.post(self.url, dados, format='json')
        # 401 Unauthorized
        self.assertEqual(resposta.status_code, 401)

    # Caminho Feliz
    def test_api_deve_criar_pedido_com_token(self):
        # Injeta o token no cabeçalho
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        dados = {'cliente': '111', 'produto': 'hd', 'quantidade': 2}
        resposta = self.api_client.post(self.url, dados, format='json')
        
        # 201 Created
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.data['produto'], 'hd')

        