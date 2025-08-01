from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Asegúrate de que esta línea exista
from django.utils import timezone

class Usuario(AbstractUser):
	pass

class MensajeDirecto(models.Model):
    # Campos del mensaje enviado por el usuario
    remitente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_enviados')
    motivo = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    
    # Campos para la respuesta del admin
    respuesta = models.TextField(blank=True, null=True)
    usuario_respuesta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='mensajes_respondidos')
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    
    # Campo para manejar el estado del mensaje
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('respondido', 'Respondido'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Mensaje de {self.remitente.username} - {self.motivo}"
        
    class Meta:
        ordering = ['-fecha_envio']
        verbose_name = 'Mensaje Directo'
        verbose_name_plural = 'Mensajes Directos'