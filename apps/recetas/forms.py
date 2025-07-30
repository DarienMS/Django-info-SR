# apps/recetas/forms.py
from django import forms
from .models import Receta, Categoria, Comentario 


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = [
            'titulo',
            'cuerpo',
            'ingredientes',
            'imagen',
            'categoria_receta',
          
        ]


        labels = {
            'titulo': 'Título de la Receta',
            'cuerpo': 'Instrucciones',
             'ingredientes': 'Ingredientes Necesarios',
            'imagen': 'Imagen de la Receta',
            'categoria_receta': 'Categoría',
        }

        widgets = {
             'ingredientes': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Ej: 2 tazas de harina, 1 huevo, 1/2 litro de leche...'}),
            'cuerpo': forms.Textarea(attrs={'rows': 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria_receta'].queryset = Categoria.objects.all().order_by('nombre')
        
        for field_name, field in self.fields.items():
             if field_name != 'imagen': 
                 field.widget.attrs.update({'class': 'form-control'})


class ComentarioForm(forms.ModelForm): 
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario aquí...'}),
        }