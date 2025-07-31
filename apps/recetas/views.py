# apps/recetas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RecetaForm
from .models import Receta, Categoria, Comentario
from django.db.models import Q
from django.views import View
from django.contrib import messages
from django.utils import timezone
from .forms import ComentarioForm
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    template_name = 'recetas/listar.html'
    context_object_name = 'recetas'
    ordering = ['-fecha'] 
    paginate_by = 10

    def get_queryset(self):
        
        queryset = Receta.objects.filter(fecha_baja__isnull=True)

       
        categoria_id = self.request.GET.get('id')
        if categoria_id:
            try:
            
                queryset = queryset.filter(categoria_receta__pk=categoria_id)
            except ValueError:
               
                pass
            except Categoria.DoesNotExist:
                
                pass

      
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
       
        context['categorias'] = Categoria.objects.all().order_by('nombre')

       
        categoria_id = self.request.GET.get('id')
        if categoria_id:
            try:
                categoria = Categoria.objects.get(pk=categoria_id)
                context['categoria_actual'] = categoria 
            except Categoria.DoesNotExist:
                pass 

        return context

class MisRecetasListView(LoginRequiredMixin, ListView):
    model = Receta
    template_name = 'recetas/mis_recetas.html' 
    context_object_name = 'mis_recetas'
    ordering = ['-fecha']
    paginate_by = 10
    def dispatch(self, request, *args, **kwargs):
        
        response = super().dispatch(request, *args, **kwargs)
        
       
        user_recipes_count = Receta.objects.filter(autor=request.user).count()

        if user_recipes_count == 0:
          
            messages.info(request, "Aún no tienes recetas publicadas. ¡Crea tu primera receta para verla aquí!")
         
            return redirect(reverse_lazy('recetas:listar'))
        
        
        return response 
    
    def get_queryset(self):
        return Receta.objects.filter(autor=self.request.user).order_by('-fecha')

# Vista de detalle de una receta
class RecetaDetailView(DetailView):
    model = Receta
    template_name = 'recetas/detalle.html' 
    context_object_name = 'receta'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receta = self.get_object() 
        context['receta'] = receta 

      
        comentarios_de_receta = receta.comentarios.filter(fecha_baja__isnull=True)
        context['comentarios'] = comentarios_de_receta 
       

      
        print(f"\n--- Depuración para RecetaDetailView ---")
        print(f"Receta actual: {receta.titulo} (ID: {receta.pk})")
        print(f"Número de comentarios cargados para esta receta: {comentarios_de_receta.count()}")
        if comentarios_de_receta.exists():
            for c in comentarios_de_receta:
                print(f"   - Comentario ID: {c.pk}, Texto: '{c.texto}', Usuario: {c.usuario.username}, Fecha: {c.fecha}")
        else:
            print("   No se encontraron comentarios asociados a esta receta en la base de datos.")
        print(f"--- Fin Depuración ---\n")
       

       
        if 'comentario_form' not in context: 
            context['comentario_form'] = ComentarioForm()

        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        form = ComentarioForm(request.POST)

        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.receta = self.object  
      
            comentario.usuario = request.user  
           
            comentario.save() 

            messages.success(request, "Tu comentario ha sido añadido con éxito.")
            return HttpResponseRedirect(reverse('recetas:detalle', kwargs={'pk': self.object.pk}))

        else:
            context = self.get_context_data(**kwargs)
            context['comentario_form'] = form 
            messages.error(request, "Error al añadir el comentario. Por favor, revisa el formulario.")
            return self.render_to_response(context)
        
        
        
class ComentarRecetaView(View):
    def post(self, request):
        if request.user.is_authenticated:
            receta_id = request.POST.get('receta_id')
            comentario_texto = request.POST.get('comentario')

            if receta_id and comentario_texto:
                try:
               
                    receta = get_object_or_404(Receta, pk=receta_id)

                   
                    Comentario.objects.create(
                        receta=receta,
                        usuario=request.user,
                        texto=comentario_texto
                    )
                    messages.success(request, "¡Comentario añadido con éxito!") 

                    
                    return redirect('recetas:detalle', pk=receta_id)

                except Exception as e:
                    messages.error(request, f"Ocurrió un error al añadir el comentario: {e}")
                    print(f"Error al guardar comentario: {e}") 
                    return redirect('recetas:detalle', pk=receta_id) 

            else:
                messages.warning(request, "No se pudo añadir el comentario. Asegúrate de escribir algo.")

                if receta_id:
                     return redirect('recetas:detalle', pk=receta_id)
                else:
                     return redirect('recetas:listar') 

        else:
            messages.info(request, "Necesitas iniciar sesión para comentar.")
            return redirect('login')
        
class RecetaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Receta
    form_class = RecetaForm 
    template_name = 'recetas/agregar_receta.html' 
    context_object_name = 'receta'
    success_url = reverse_lazy('recetas:mis_recetas')

    def test_func(self):
        receta = self.get_object()
        return receta.autor == self.request.user

    def form_valid(self, form):
       
        messages.success(self.request, "Receta actualizada con éxito.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar la receta. Por favor, revisa los campos.")
        return super().form_invalid(form)



class RecetaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # <<-- ¡CAMBIO CRÍTICO AQUÍ!
    model = Receta
    template_name = 'recetas/receta_confirm_delete.html' # Puedes comentarla si usas el modal customizado
    success_url = reverse_lazy('recetas:mis_recetas')

    

    def test_func(self):
       
        receta = self.get_object() 
        return receta.autor == self.request.user


    def post(self, request, *args, **kwargs):
        """
        Marca la receta como de baja en lugar de eliminarla.
        """
        self.object = self.get_object() 
        self.object.fecha_baja = timezone.now()
        self.object.usuario_baja = request.user
        self.object.save() 

        messages.success(self.request, f"La receta '{self.object.titulo}' ha sido dada de baja.")
        return redirect(self.success_url)

class RecetaReactivateView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Receta
    success_url = reverse_lazy('recetas:mis_recetas')

    def get_object(self):
       
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def test_func(self):
      
        receta = self.get_object()
        return receta.autor == self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.fecha_baja = None    
        self.object.usuario_baja = None 
        self.object.save()               

        messages.success(self.request, f"La receta '{self.object.titulo}' ha sido habilitada nuevamente.")
        return redirect(self.success_url)

    
    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)
    
class ComentarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'recetas/comentario_form.html' 
    context_object_name = 'comentario'

    def get_success_url(self):
      
        return reverse_lazy('recetas:detalle', kwargs={'pk': self.object.receta.pk})

    def test_func(self):

        comentario = self.get_object()
        return self.request.user == comentario.usuario

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para editar este comentario.")
        return redirect(self.get_success_url()) 

class ComentarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, View): 
    def dispatch(self, request, *args, **kwargs):

        self.comentario = get_object_or_404(Comentario, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
     
        return self.request.user == self.comentario.usuario or self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
       
        comentario = self.comentario

        
        comentario.fecha_baja = timezone.now() 
        comentario.usuario_baja = request.user 
        comentario.save() 

        messages.success(request, "Comentario eliminado lógicamente.")
       
        return redirect(reverse_lazy('recetas:detalle', kwargs={'pk': comentario.receta.pk}))

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para eliminar este comentario.")
       
        return redirect(reverse_lazy('recetas:detalle', kwargs={'pk': self.comentario.receta.pk}))
    


class RecetasAdminListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Receta
    template_name = 'recetas/recetas_lista.html'
    context_object_name = 'recetas'

    # Método de UserPassesTestMixin para verificar si el usuario es superusuario
    def test_func(self):
        return self.request.user.is_superuser
    
    # Este método sobrescribe el comportamiento por defecto para obtener todas las recetas,
    # incluyendo las inactivas, para el panel de administración.
    def get_queryset(self):
        return Receta.objects.all().order_by('-fecha')
    
    
class ComentariosAdminListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Comentario
    template_name = 'recetas/lista_comentarios.html'
    context_object_name = 'comentarios'

    def test_func(self):
        # Solo los superusuarios pueden ver este panel
        return self.request.user.is_superuser
    
    def get_queryset(self):
        # Obtiene todos los comentarios, ordenados por los más recientes
        # La tabla de tu modelo Comentario tiene un campo 'fecha'
        return Comentario.objects.all().order_by('-fecha')