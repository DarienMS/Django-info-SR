from django.shortcuts import render
from apps.recetas.models import Receta
#request 'es un diccionario que continuamente se va pasando entre el navegador y el servidor'

def Home(request):
    """
    Vista para la página de inicio que muestra las últimas 3 recetas.
    """
    # Obtener las últimas 3 recetas activas (no dadas de baja)
    # y ordenarlas por fecha descendente
    recetas_recientes = Receta.objects.filter(fecha_baja__isnull=True).order_by('-fecha')[:3]

    context = {
        'recetas_recientes': recetas_recientes,
        'titulo': 'Inicio' # Opcional: pasar un título a la plantilla
    }
    return render(request, 't_home.html', context)

def Nosotros(request):

	return render(request, 't_nosotros.html')