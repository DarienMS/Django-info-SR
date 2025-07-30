# apps/recetas/models.py
from django.db import models
from django.conf import settings 
from django.utils import timezone
from django.urls import reverse

class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True) 


    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Categoría Padre'
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
        return ' > '.join(full_path[::-1])

    def is_top_level(self):
        return self.parent is None


# Modelo para Recetas
class Receta(models.Model):
    titulo = models.CharField(max_length=150)
    cuerpo = models.TextField()
    ingredientes = models.TextField(
        blank=True, 
        help_text="Lista de ingredientes, separados por comas, puntos o en líneas diferentes."
    )
    imagen = models.ImageField(upload_to='recetas_imagenes/', blank=True, null=True)

    categoria_receta = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recetas'
    )

    fecha = models.DateTimeField(auto_now_add=True) 
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Última Modificación') # <<-- Se actualiza en cada save
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mis_recetas',
        verbose_name='Autor'
    )
    
    fecha_baja = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Baja')
    usuario_baja = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recetas_dadas_de_baja',
        verbose_name='Usuario de Baja'
    )

    def __str__(self):
        return self.titulo
    def get_absolute_url(self):
         return reverse('recetas:detalle', kwargs={'pk': self.pk})

class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')
    texto = models.TextField(max_length=1500)
    receta = models.ForeignKey('Receta', on_delete=models.CASCADE, related_name='comentarios')

    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Publicación')


    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Última Modificación') 
    fecha_baja = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Baja')
    usuario_baja = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='comentarios_dados_de_baja',
        verbose_name='Usuario de Baja'
    )
    # -------------------------------------------------

    def __str__(self):
        return f"Comentario de {self.usuario.username} en '{self.receta.titulo}'"

    class Meta:
        ordering = ['fecha'] 
        verbose_name_plural = "Comentarios" 

   
    def is_active(self):
        return self.fecha_baja is None