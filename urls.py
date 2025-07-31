from django.contrib import admin
from django.urls import path, include
from apps.recetas.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # <-- ESTA LÍNEA ES LA QUE MUESTRA EL HOME
    path('Recetas/', include('apps.recetas.urls', namespace='recetas')),
    # ...otros includes...
]

def home(request):
    recetas_recientes = Receta.objects.filter(fecha_baja__isnull=True).order_by('-fecha')[:6]
    print("RECETAS ENCONTRADAS:", recetas_recientes)
    return render(request, 't_home.html', {'recetas_recientes': recetas_recientes})