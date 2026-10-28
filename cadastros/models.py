from django.db import models

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100, help_text="Nome da categoria")
    descricao = models.TextField(blank=True, null=True, help_text="Descrição opcional")

    def __str__(self):
        return self.nome

class Produto(models.Model):
    # Usamos SlugField: ele é ideal para URLs, pois só aceita letras, números, hifens e sublinhados (ex: mouse_gamer)
    slug = models.SlugField(max_length=150, primary_key=True, help_text="Ex: nome-do-produto")
    nome = models.CharField(max_length=150)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.IntegerField(default=0)
    situacao = models.BooleanField(default=True, help_text="Indica se o produto está ativo ou inativo")
    # A Chave Estrangeira (Relacionamento)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="produtos")

    def __str__(self):
        return f"{self.nome} (Estoque: {self.quantidade_estoque})"

class Cliente(models.Model):
    # Adicionamos o CNPJ temporariamente permitindo nulos
    cnpj = models.CharField(max_length=14, primary_key=True, help_text="Apenas números")
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    situacao = models.BooleanField(default=True, help_text="Indica se o cliente está ativo ou inativo")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="clientes")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome