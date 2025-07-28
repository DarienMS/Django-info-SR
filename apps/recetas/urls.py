# apps/recetas/urls.py
from django.urls import path
from . import views # Importamos todas las vistas como 'views.NombreDeLaVista'

app_name = 'recetas'

urlpatterns = [
    # URL para el listado general de recetas (RecetaListView)
    path('', views.RecetaListView.as_view(), name='listar'),

    # URL para el detalle de una receta (RecetaDetailView)
    # Importante: Asegúrate que tu RecetaDetailView maneje el <int:pk>
    path('detalle/<int:pk>/', views.RecetaDetailView.as_view(), name='detalle'),

    # URL para agregar una nueva receta (RecetaCreateView)
    path('agregar/', views.RecetaCreateView.as_view(), name='agregar_receta'),

    # URL para listar las recetas del usuario logueado (MisRecetasListView)
    path('mis-recetas/', views.MisRecetasListView.as_view(), name='mis_recetas'),

    # La URL de comentario:
    # Como no tienes 'comentar_receta' en views.py, tienes 2 opciones:
    # OPCION A (Si NO VAS A IMPLEMENTAR COMENTARIOS AHORA):
    # Comenta o elimina la línea de comentario:
    # # path('Comentario/', views.comentar_receta, name='comentar'),

    # OPCION B (Si VAS A IMPLEMENTAR COMENTARIOS, pero necesitas crear la vista):
    # La dejaremos comentada por ahora y luego la agregaremos cuando tengas la vista.
    # Por el momento, la solución más directa es que no esté definida si no existe.
]