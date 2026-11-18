from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class ViewsProtegidasTest(TestCase):
    def setUp(self):
        self.cliente_comum = User.objects.create_user(username='comum', password='123', is_staff=False)
        self.admin = User.objects.create_user(username='admin', password='123', is_staff=True)
        self.url = reverse('cadastros:cadastrar_produto')

    def test_usuario_anonimo_deve_ser_redirecionado(self):
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 302) 

    def test_cliente_comum_deve_ser_redirecionado(self):
        self.client.login(username='comum', password='123')
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 302)

    def test_admin_deve_acessar_tela_de_cadastro(self):
        self.client.login(username='admin', password='123')
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'cadastros/cadastrar_produto.html')