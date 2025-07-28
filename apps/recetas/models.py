# apps/recetas/models.py
from django.db import models
from django.conf import settings # Necesario si tu modelo de usuario es personalizado y lo vinculas más adelante
from django.utils import timezone # Añadido por mi para fecha, pero no estaba en tu original con auto_now_add

# Modelo para Categorías de Recetas (con jerarquía)
class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True) # unique=True para evitar categorías con el mismo nombre

    # parent será una clave foránea a otra Categoria.
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
    imagen = models.ImageField(upload_to='recetas_imagenes/', blank=True, null=True)

    categoria_receta = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recetas'
    )

    fecha = models.DateTimeField(auto_now_add=True) # <-- Usas auto_now_add=True

    # autor comentado, lo agregaremos ahora.
    # autor = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name='mis_recetas',
    #     verbose_name='Autor'
    # )

    def __str__(self):
        return self.titulo

# Modelo Comentario, tal cual lo tenías funcionando antes
class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField(max_length=1500)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True) # <-- Usas auto_now_add=True

    def __str__(self):
        return f"{self.receta.titulo} -> {self.texto[:50]}..."