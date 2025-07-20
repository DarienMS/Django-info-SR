from django.contrib import admin
from .models import Receta, Categoria, Comentario  # Agrega los modelos

admin.site.register(Receta)
admin.site.register(Categoria)
admin.site.register(Comentario)
