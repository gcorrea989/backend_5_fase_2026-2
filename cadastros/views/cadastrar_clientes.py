from django.shortcuts import render, redirect
#Fiz um ajuste no formulário, criando um padronizado para
#aplicar o CSS padrão do projeto
#from django.contrib.auth.forms import UserCreationForm
from cadastros.forms import RegistroClienteForm
from django.contrib import messages

def registrar_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save() # Cria o usuário comum (is_staff=False)
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect('login')
    else:
        form = RegistroClienteForm()
    
    return render(request, 'registration/registro.html', {'form': form})