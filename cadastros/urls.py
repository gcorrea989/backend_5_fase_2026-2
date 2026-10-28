from django.urls import path
from . import views

# desta forma criamos um namespace para o app cadastros,
#  evitando conflitos de nomes com outros apps do projeto
app_name = 'cadastros' 

urlpatterns = [
    path('orm/', views.demonstracao_orm, name='demo_orm'),
    #vamos aproveitar e já criar mais uma rota para a view de listagem de clientes
    path('clientes/', views.listagem_clientes, name='listagem_clientes'),
    path('produtos/novo/', views.cadastrar_produto, name='cadastrar_produto'),
]
