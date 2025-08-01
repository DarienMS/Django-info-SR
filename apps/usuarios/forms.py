# usuarios/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MensajeDirecto, Usuario

class   RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta): # heredar la Meta de UserCreationForm(esto ya es propio de django)
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
       
        self.fields['email'].required = True 
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        # aca cambiamos despues los label si queremos
        self.fields['username'].label = 'Nombre de Usuario'
        self.fields['email'].label = 'Correo Electrónico'
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
class MensajeForm(forms.ModelForm):
    class Meta:
        model = MensajeDirecto
        fields = ['motivo', 'mensaje']
        widgets = {
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

# Formulario para que el admin pueda responder un mensaje
class MensajeRespuestaForm(forms.ModelForm):
    class Meta:
        model = MensajeDirecto
        fields = ['respuesta']
        widgets = {
            'respuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }