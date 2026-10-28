# O __init__.py transforma a pasta 'views' em um módulo Python válido.
# Importamos todas as funções dos arquivos separados para que fiquem
# acessíveis diretamente através do namespace 'views'.

from .dashboard import home_dashboard
from .clientes import listagem_clientes
from .produtos import cadastrar_produto
from .orm import demonstracao_orm
from .cadastrar_clientes import registrar_cliente