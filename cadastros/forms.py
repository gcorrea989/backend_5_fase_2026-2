from django import forms
from django.core.exceptions import ValidationError
from .models import Produto

class ProdutoForm(forms.ModelForm):
    error_css_class = 'tem-erro'
    required_css_class = 'eh-obrigatorio'
    class Meta:
        model = Produto
        fields = ['slug', 'nome', 'preco', 'quantidade_estoque', 'situacao', 'categoria']
        
        # 1. WIDGETS: Controle do HTML renderizado (classes CSS, placeholders, atributos)
        widgets = {
            'slug': forms.TextInput(attrs={
                'class': 'campo__input', 
                'placeholder': 'ex: teclado-mecanico',
                'autofocus': True, # Foca automaticamente ao abrir a página
            }),
            'nome': forms.TextInput(attrs={
                'class': 'campo__input',
                'placeholder': 'Digite o nome completo do produto',
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'campo__input campo__input--numerico',
                'step': '0.01', # Permite casas decimais no front-end
                'min': '0.01',  # Validação HTML5 no front-end
                'placeholder': '0.00',
            }),
            'quantidade_estoque': forms.NumberInput(attrs={
                'class': 'campo__input campo__input--numerico',
                'min': '0',
                'placeholder': '0',
            }),
            'situacao': forms.CheckboxInput(attrs={
                'class': 'campo__checkbox',
            }),
            'categoria': forms.Select(attrs={
                'class': 'campo__select',
            }),
        }

        # 2. LABELS: Nomes amigáveis para os rótulos (<label>)
        labels = {
            'slug': 'Código de URL (Slug)',
            'nome': 'Nome do Produto',
            'preco': 'Preço de Venda (R$)',
            'quantidade_estoque': 'Estoque Atual',
            'situacao': 'Produto Ativo no Sistema?',
            'categoria': 'Categoria',
        }

        # 3. ERROR_MESSAGES: Mensagens de erro padrão do Django sobrescritas
        error_messages = {
            'slug': {
                'required': 'O código (slug) é obrigatório.',
                'invalid': 'O slug deve conter apenas letras, números, hifens ou sublinhados.',
            },
            'nome': {
                'required': 'Por favor, informe o nome do produto.',
            },
            'categoria': {
                'required': 'Selecione uma categoria válida.',
            }
        }

    # =========================================================================
    # VALIDAÇÕES DE BACK-END (As mesmas de antes, garantindo a segurança)
    # =========================================================================

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco is not None and preco <= 0:
            raise ValidationError("O preço do produto deve ser maior que zero.")
        return preco

    def clean_quantidade_estoque(self):
        estoque = self.cleaned_data.get('quantidade_estoque')
        if estoque is not None and estoque < 0:
            raise ValidationError("A quantidade em estoque não pode ser negativa.")
        return estoque

    def clean(self):
        cleaned_data = super().clean()
        situacao = cleaned_data.get('situacao')
        estoque = cleaned_data.get('quantidade_estoque')

        # Regra de negócio: Produto não pode ser ativado se não tiver estoque
        if situacao and estoque is not None and estoque <= 0:
            raise ValidationError(
                "Um produto não pode ser marcado como 'Ativo' se o estoque for zero."
            )
            
        return cleaned_data