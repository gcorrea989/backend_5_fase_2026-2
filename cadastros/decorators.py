from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def login_obrigatorio_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Sem permissão. Faça login para acessar a tela de cadastro.")
            return redirect('home') # Certifique-se de que 'home' é o name da sua rota inicial
        return view_func(request, *args, **kwargs)
    return _wrapped_view