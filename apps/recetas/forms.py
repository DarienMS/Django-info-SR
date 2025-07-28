# apps/recetas/forms.py
from django import forms
from .models import Receta, Categoria

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = [
            'titulo',
            'cuerpo',
            'imagen',
            'categoria_receta',
            # 'autor', # NO INCLUIR 'autor' aquí, se asigna automáticamente en la vista
        ]
        # O también puedes usar:
        # exclude = ['autor', 'fecha'] # Si no quieres que 'fecha' sea editable tampoco

        labels = {
            'titulo': 'Título de la Receta',
            'cuerpo': 'Ingredientes e Instrucciones',
            'imagen': 'Imagen de la Receta',
            'categoria_receta': 'Categoría',
        }

        widgets = {
            'cuerpo': forms.Textarea(attrs={'rows': 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria_receta'].queryset = Categoria.objects.all().order_by('nombre')
        # Puedes seguir añadiendo las clases de Bootstrap aquí, por ejemplo:
        for field_name, field in self.fields.items():
             if field_name != 'imagen': # Las imágenes o archivos a veces no necesitan 'form-control'
                 field.widget.attrs.update({'class': 'form-control'})