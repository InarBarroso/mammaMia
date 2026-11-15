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