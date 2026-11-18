from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from cadastros.models import Produto, Cliente

class PedidoAPITest(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.usuario = User.objects.create_user(username='api_user', password='123')
        self.token = Token.objects.create(user=self.usuario)
        
        self.cliente_db = Cliente.objects.create(cnpj='111', nome='Empresa X', email='x@x.com')
        self.produto_db = Produto.objects.create(slug='hd', nome='HD', preco=100.00, situacao=True)
        self.url = reverse('cadastros:api_pedidos')

    def test_api_deve_rejeitar_pedido_sem_token(self):
        dados = {'cliente': '111', 'produto': 'hd', 'quantidade': 2}
        resposta = self.api_client.post(self.url, dados, format='json')
        self.assertEqual(resposta.status_code, 401)

    def test_api_deve_criar_pedido_com_token(self):
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        dados = {'cliente': '111', 'produto': 'hd', 'quantidade': 2}
        resposta = self.api_client.post(self.url, dados, format='json')
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.data['produto'], 'hd')