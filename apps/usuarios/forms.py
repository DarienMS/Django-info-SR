# usuarios/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario # Tu modelo de usuario personalizado

class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta): # Opcional: heredar la Meta de UserCreationForm
        model = Usuario
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            # 'password' es el nombre del campo en el modelo,
            # UserCreationForm se encarga de renderizar password1 y password2
        ]
      
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Personalizar labels o widgets si lo necesitas,
        # pero para los campos que ya existen, Django toma el label del modelo.
        self.fields['email'].required = True # Asegura que el email sea requerido, aunque tu modelo ya lo dice
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        # Personalizar labels si quieres que sean diferentes a los del modelo
        self.fields['username'].label = 'Nombre de Usuario'
        self.fields['email'].label = 'Correo Electrónico'
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'