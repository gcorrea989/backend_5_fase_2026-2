from django.contrib import admin
from .models import Categoria, Produto, Cliente

# Modo 1: Registro simples (Padrão)
admin.site.register(Categoria)

# Modo 2: Registro customizado (Para deixar a tela mais rica)
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Define quais colunas vão aparecer na lista
    list_display = ('nome', 'categoria', 'preco', 'quantidade_estoque')
    # Adiciona um filtro lateral
    list_filter = ('categoria',)
    # Adiciona uma barra de pesquisa
    search_fields = ('nome',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'situacao')
    list_filter = ('situacao',)
    search_fields = ('nome', 'email')
    list_editable = ('situacao',)  # Permite editar a situação diretamente na lista