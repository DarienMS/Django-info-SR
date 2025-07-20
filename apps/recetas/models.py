from django.db import models
from apps.usuarios.models import Usuario

class Categoria(models.Model):
	nombre = models.CharField(max_length=60)

	def __str__(self):
		return self.nombre

class Receta(models.Model):  # Cambiado a singular

	titulo = models.CharField(max_length=150)
	cuerpo = models.TextField()
	imagen = models.ImageField(upload_to='recetas')
	categoria_receta = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Cambiado
	fecha = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.titulo

class Comentario(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	texto = models.TextField(max_length=1500)
	receta = models.ForeignKey(Receta, on_delete=models.CASCADE)  # Cambiado
	fecha = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.receta} -> {self.texto}"  # Cambiado