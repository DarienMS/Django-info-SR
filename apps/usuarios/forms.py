# usuarios/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MensajeDirecto, Usuario
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


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


        # para que el usuario se autogestione
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# Nuevo formulario combinado para la edición de perfil y contraseña
class PerfilCompletoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)
    
    # Campos para el cambio de contraseña
    old_password = forms.CharField(widget=forms.PasswordInput, label="Contraseña Actual", required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Nueva Contraseña", required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Nueva Contraseña", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if old_password and not self.instance.check_password(old_password):
            raise forms.ValidationError("La contraseña actual es incorrecta.")
        return old_password

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        if new_password1:
            try:
                validate_password(new_password1, self.instance)
            except ValidationError as error:
                self.add_error('new_password1', error)
        return new_password1

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        old_password = cleaned_data.get("old_password")

       
        if new_password1 or new_password2 or old_password:
            if not old_password:
                self.add_error('old_password', "Debes ingresar tu contraseña actual para cambiarla.")
            if new_password1 != new_password2:
                self.add_error('new_password2', "Las nuevas contraseñas no coinciden.")
        return cleaned_data