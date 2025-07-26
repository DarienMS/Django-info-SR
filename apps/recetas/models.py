
from django.db import models

from django.conf import settings # Necesario si tu modelo de usuario es personalizado y lo vinculas más adelante

# Modelo para Categorías de Recetas (con jerarquía)
class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True) # unique=True para evitar categorías con el mismo nombre

    # parent será una clave foránea a otra Categoria.
    # null=True y blank=True significa que una categoría puede no tener un padre (ser de nivel superior).
    # related_name='children' nos permite acceder a las categorías hijas desde una categoría padre.
    parent = models.ForeignKey(
        'self', # Se refiere a la misma clase Categoria
        on_delete=models.SET_NULL, # Si se borra la categoría padre, las hijas se quedan sin padre
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Categoría Padre' # Nombre legible en el admin
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
       
        ordering = ['parent__nombre', 'nombre'] 

    def __str__(self):
        
        full_path = [self.nombre]
        k = self.parent
        while k is not None:
            full_path.append(k.nombre)
            k = k.parent
        return ' > '.join(full_path[::-1]) # Invertir la lista para ir de padre a hijo

    # Método opcional para saber si es de nivel superior (no tiene padre)
    def is_top_level(self):
        return self.parent is None


# Modelo para Recetas
class Receta(models.Model):
    titulo = models.CharField(max_length=150)
    cuerpo = models.TextField() # Asumo que este es el campo 'cuerpo' que incluye ingredientes e instrucciones
    imagen = models.ImageField(upload_to='recetas_imagenes/') # 'upload_to' es la carpeta dentro de MEDIA_ROOT

    # Aquí el cambio importante: SET_NULL y null/blank True
    categoria_receta = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True, # Permite que el campo sea nulo en la base de datos
        blank=True, # Permite que el campo esté vacío en los formularios
        related_name='recetas' # Permite acceder a recetas desde una categoría: categoria.recetas.all()
    )

    fecha = models.DateTimeField(auto_now_add=True)

    # vemos mas adelante
    # autor = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, # Usa el modelo de usuario definido en settings.py
    #     on_delete=models.CASCADE,
    #     related_name='mis_recetas',
    #     verbose_name='Autor'
    # )

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Usar settings.AUTH_USER_MODEL es más robusto
    texto = models.TextField(max_length=1500)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receta.titulo} -> {self.texto[:50]}..." # Mostrar algo más legible