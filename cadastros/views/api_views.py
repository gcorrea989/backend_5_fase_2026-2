from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from cadastros.models import Produto, Pedido
from cadastros.serializers import ProdutoSerializer, PedidoSerializer

# Lista de Produtos (Público, apenas leitura)
class ProdutoListAPI(generics.ListAPIView):
    queryset = Produto.objects.filter(situacao=True)
    serializer_class = ProdutoSerializer

# Criação de Pedidos (Protegido via Token)
class PedidoCreateAPI(generics.CreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated] # Exige chave de API no cabeçalho