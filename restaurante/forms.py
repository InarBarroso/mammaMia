from django import forms
from .models import Pizza, TipoMasa, Ingrediente, User


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        error_messages={
            'required': 'Introduce tu email.',
            'invalid': 'Introduce un email válido.',
        },
    )

    password = forms.CharField(
        label='Contraseña',
        max_length=100,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required': 'Introduce tu contraseña.',
        },
    )


class addPizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['titulo', 'descripcion', 'precio', 'foto', 'tipo', 'ingredientes']

        widgets = {
            'titulo': forms.TextInput(attrs={'id': 'nombre'}),
            'descripcion': forms.Textarea(attrs={'id': 'detalles'}),
            'precio': forms.NumberInput(attrs={'id': 'precio'}),
            'tipo': forms.Select(attrs={'id': 'tipoMasa'}),
            'ingredientes': forms.CheckboxSelectMultiple(),
        }


class CompraPizzaForm(forms.Form):
    # formulario para comprar una pizza desde su detalle: solo pide cuántas se quieren
    cantidad = forms.IntegerField(
        label='Cantidad',
        min_value=1,  # no se puede comprar 0 ni un número negativo
        initial=1,    # al entrar en la página el campo sale con un 1
        error_messages={
            'required': 'Indica cuántas pizzas quieres.',
            'invalid': 'Introduce un número entero.',
            'min_value': 'Como mínimo tienes que comprar 1 pizza.',
        },
    )