# recetas/forms.py
from django import forms
from .models import Receta, Categoria # Importamos ambos modelos

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        # Aquí listamos los campos que queremos que el usuario complete en el formulario
        fields = [
            'titulo',
            'cuerpo',
            'imagen',
            'categoria_receta', # Este campo se renderizará como un dropdown con la jerarquía
        ]
        
        labels = {
            'titulo': 'Título de la Receta',
            'cuerpo': 'Ingredientes e Instrucciones',
            'imagen': 'Imagen de la Receta',
            'categoria_receta': 'Categoría',
        }
        
        widgets = {
            'cuerpo': forms.Textarea(attrs={'rows': 8}), # Un textarea con 8 filas de alto
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
  
        self.fields['categoria_receta'].queryset = Categoria.objects.all().order_by('nombre')
      