# apps/recetas/views.py
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecetaForm
from .models import Receta, Categoria
from django.db.models import Q

# Vista para crear una nueva receta
class RecetaCreateView(LoginRequiredMixin, CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'recetas/agregar_receta.html'
    success_url = reverse_lazy('recetas:listar') # Redirigimos al listado general

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class RecetaListView(ListView):
    model = Receta
    template_name = 'recetas/listar.html' # Usamos tu plantilla 'listar.html'
    context_object_name = 'recetas'
    ordering = ['-fecha']
    paginate_by = 10 # Opcional

    def get_context_data(self, **kwargs):
        # Llama a la implementación base para obtener un contexto
        context = super().get_context_data(**kwargs)
        # Agrega las categorías al contexto
        context['categorias'] = Categoria.objects.all().order_by('nombre')

        # Si hay un filtro por categoría en la URL (ej. ?id=1)
        categoria_id = self.request.GET.get('id')
        if categoria_id:
            try:
                categoria = Categoria.objects.get(pk=categoria_id)
                context['recetas'] = Receta.objects.filter(categoria_receta=categoria).order_by('-fecha')
                context['categoria_actual'] = categoria # Para mostrar qué categoría está filtrada
            except Categoria.DoesNotExist:
                pass # Manejar si la categoría no existe

        return context

# Vista para listar SOLO las recetas del usuario logueado
class MisRecetasListView(LoginRequiredMixin, ListView):
    model = Receta
    template_name = 'recetas/mis_recetas.html' # Nueva plantilla para mis recetas
    context_object_name = 'mis_recetas'
    ordering = ['-fecha']
    paginate_by = 10

    def get_queryset(self):
        return Receta.objects.filter(autor=self.request.user).order_by('-fecha')

# Vista de detalle de una receta
class RecetaDetailView(DetailView):
    model = Receta
    template_name = 'recetas/detalle_receta.html' # Asume que tienes esta plantilla
    context_object_name = 'receta'