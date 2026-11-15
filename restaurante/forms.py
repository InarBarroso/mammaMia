from django import forms


class LoginForm(forms.Form):
    # Crea un <input type="email"> con su label; Django comprueba que el formato sea de email
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        error_messages={
            'required': 'Introduce tu email.',
            'invalid': 'Introduce un email válido.',
        },
    )
    # Crea un <input type="password"> para que no se vea lo que se escribe
    password = forms.CharField(
        label='Contraseña',
        max_length=100,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required': 'Introduce tu contraseña.',
        },
    )
