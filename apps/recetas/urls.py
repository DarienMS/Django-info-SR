from django.urls import path
from . import views
from .views import RecetaCreateView 
app_name = 'recetas'

urlpatterns = [
    path('', views.listar_recetas, name='listar'), 
    path('Detalle/<int:pk>/', views.detalle_receta, name='detalle'),
    path('Comentario/', views.comentar_receta, name='comentar'),
    path('agregar/', RecetaCreateView.as_view(), name='agregar_receta'), 
]