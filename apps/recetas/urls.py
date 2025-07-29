# apps/recetas/urls.py
from django.urls import path
from . import views # Importamos todas las vistas como 'views.NombreDeLaVista'

app_name = 'recetas'

urlpatterns = [
    path('', views.RecetaListView.as_view(), name='listar'),
    path('agregar/', views.RecetaCreateView.as_view(), name='agregar_receta'),
    path('mis-recetas/', views.MisRecetasListView.as_view(), name='mis_recetas'),

    # ¡ESTA ES LA LÍNEA QUE DEBE ESTAR AHÍ!
   path('receta/<int:pk>/', views.RecetaDetailView.as_view(), name='detalle'),

    path('comentar/', views.ComentarRecetaView.as_view(), name='comentar'),
    path('receta/editar/<int:pk>/', views.RecetaUpdateView.as_view(), name='receta_editar'),
    path('receta/eliminar/<int:pk>/', views.RecetaDeleteView.as_view(), name='receta_eliminar'), 
    path('receta/habilitar/<int:pk>/', views.RecetaReactivateView.as_view(), name='receta_habilitar'),

   
  path('comentario/editar/<int:pk>/', views.ComentarioUpdateView.as_view(), name='comentario_editar'),
    path('comentario/eliminar/<int:pk>/', views.ComentarioDeleteView.as_view(), name='comentario_eliminar'),
    
]