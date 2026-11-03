from rest_framework import serializers
from .models import Produto, Pedido

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['slug', 'nome', 'preco', 'quantidade_estoque', 'situacao']

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'produto', 'quantidade', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']