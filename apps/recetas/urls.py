from django.urls import path
from . import views

app_name = 'recetas'

urlpatterns = [
    path('', views.listar_recetas, name='listar'),
    path('Detalle/<int:pk>', views.detalle_receta, name='detalle'),
    path('Comentario/', views.comentar_receta, name='comentar'),
]