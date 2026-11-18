from django.test import TestCase
from cadastros.models import Categoria
from cadastros.forms import ProdutoForm

class ProdutoFormTest(TestCase):
    def test_nao_deve_permitir_preco_zero_ou_negativo(self):
        dados = {
            'slug': 'teclado', 'nome': 'Teclado', 
            'preco': 0, 
            'quantidade_estoque': 10, 'situacao': True
        }
        form = ProdutoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('preco', form.errors)

    def test_nao_deve_ativar_produto_com_estoque_zero(self):
        dados = {
            'slug': 'mouse', 'nome': 'Mouse', 
            'preco': 50.00, 'quantidade_estoque': 0, 'situacao': True
        }
        form = ProdutoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_deve_aceitar_produto_valido(self):
        categoria = Categoria.objects.create(nome="Periféricos")
        dados = {
            'slug': 'monitor', 'nome': 'Monitor', 
            'preco': 800.00, 'quantidade_estoque': 5, 
            'situacao': True, 'categoria': categoria.id
        }
        form = ProdutoForm(data=dados)
        self.assertTrue(form.is_valid())