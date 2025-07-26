from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Receta, Categoria, Comentario
from django.urls import reverse_lazy
from django.contrib import auth
from django.views.generic import CreateView, ListView, DetailView # Agregado ListView, DetailView para referencia
from django.contrib.auth.mixins import LoginRequiredMixin # Importa LoginRequiredMixin
from .forms import RecetaForm
@login_required
def listar_recetas(request):
    contexto = {}
    id_categoria = request.GET.get('id', None)
    if id_categoria:
        recetas = Receta.objects.filter(categoria_receta=id_categoria)
    else:
        recetas = Receta.objects.all()
    contexto['recetas'] = recetas
    contexto['categorias'] = Categoria.objects.all().order_by('nombre')
    return render(request, 'recetas/listar.html', contexto)

@login_required
def detalle_receta(request, pk):
    contexto = {}
    receta = Receta.objects.get(pk=pk)
    contexto['receta'] = receta
    comentarios = Comentario.objects.filter(receta=receta)
    contexto['comentarios'] = comentarios
    return render(request, 'recetas/detalle.html', contexto)

@login_required
def comentar_receta(request):
    com = request.POST.get('comentario', None)
    usu = request.user
    receta_id = request.POST.get('id_receta', None)
    receta = Receta.objects.get(pk=receta_id)
    Comentario.objects.create(usuario=usu, receta=receta, texto=com)
    return redirect(reverse_lazy('recetas:detalle', kwargs={'pk': receta_id}))

   
class RecetaCreateView(LoginRequiredMixin, CreateView):
    model = Receta
    form_class = RecetaForm # Usamos el formulario que creamos en recetas/forms.py
    template_name = 'recetas/agregar_receta.html' # La plantilla donde estará el formulario

   
    success_url = reverse_lazy('recetas:listar_recetas') 

  
    def form_valid(self, form):
     
        return super().form_valid(form) # Llama al método original para guardar el formulario




LOGOUT_REDIRECT_URL = '/'