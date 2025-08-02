from django.urls import path

from . import views
from django.contrib.auth.decorators import login_required
app_name = 'usuarios'

urlpatterns = [
    
    path('registro/', views.Registro.as_view(), name = 'registro'),

   path('lista/', login_required(views.UsuarioListView.as_view()), name='lista_usuarios'),
 path('desactivar/<int:pk>/', login_required(views.UsuarioDesactivarView.as_view()), name='desactivar_usuario'),
    path('activar/<int:pk>/', login_required(views.UsuarioActivarView.as_view()), name='activar_usuario'),
     path('editar/<int:pk>/', login_required(views.UsuarioUpdateView.as_view()), name='editar_usuario'),
      path('crear/', login_required(views.UsuarioCreateView.as_view()), name='crear_usuario'),
path('mensajes/enviar/', views.MensajeCreateView.as_view(), name='enviar_mensaje'),
    # URL para ver los mensajes del usuario (la crearemos después)
    path('mensajes/mis-mensajes/', views.MisMensajesListView.as_view(), name='mis_mensajes'),
     path('mensajes/admin/', views.MensajeAdminListView.as_view(), name='lista_mensajes_admin'),
     path('mensajes/admin/responder/', views.MensajeResponderView.as_view(), name='responder_mensaje_admin'),
  path('perfil/', views.perfil_usuario_view, name='perfil'),
  
]