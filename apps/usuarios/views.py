from django.shortcuts import render,redirect
from django.views.generic import CreateView,UpdateView
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import UserPassesTestMixin 
from .forms import RegistroForm
from .forms import Usuario
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import MensajeDirecto
from .forms import MensajeForm, MensajeRespuestaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone 
from django.db.models import Q
class Registro(CreateView):
	
	form_class = RegistroForm
	success_url = reverse_lazy('login')
	template_name = 'usuarios/registro.html'


class UsuarioListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'usuarios/lista_usuarios.html'
    context_object_name = 'usuarios'
    ordering = ['username']

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('home')

    def get_queryset(self):
        queryset = super().get_queryset()
        
        search_query = self.request.GET.get('q')
        status_filter = self.request.GET.get('status')

        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        if status_filter:
            if status_filter == 'active':
                queryset = queryset.filter(is_active=True)
            elif status_filter == 'inactive':
                queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context
    
class UsuarioDesactivarView(UserPassesTestMixin, UpdateView):
    model = Usuario
    fields = ['is_active']
    success_url = reverse_lazy('usuarios:lista_usuarios')

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object == self.request.user:
            messages.error(request, 'No puedes desactivar tu propia cuenta.')
            return redirect(self.success_url)

        self.object.is_active = False 
        self.object.save()
        messages.success(request, f'Usuario "{self.object.username}" deshabilitado exitosamente.')
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        messages.error(request, 'Acceso inválido. Por favor, desactive usuarios usando el botón correspondiente.')
        return redirect(self.success_url)
    
class UsuarioActivarView(UserPassesTestMixin, UpdateView):
    model = Usuario
    fields = ['is_active']
    success_url = reverse_lazy('usuarios:lista_usuarios')

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True 
        self.object.save()
        messages.success(request, f'Usuario "{self.object.username}" habilitado exitosamente.')
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        messages.error(request, 'Acceso inválido. Por favor, active usuarios usando el botón correspondiente.')
        return redirect(self.success_url)
    
class UsuarioUpdateView(UserPassesTestMixin, UpdateView):
    model = Usuario
    
    # CORRECCIÓN: Quitamos 'is_superuser' de la lista de campos
    fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active']
    
    template_name = 'usuarios/usuario_editar.html'
    success_url = reverse_lazy('usuarios:lista_usuarios')

    def test_func(self):
        # Permite la edición solo a superusuarios
        return self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(self.request, f'Usuario "{form.instance.username}" actualizado exitosamente.')
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para editar usuarios.')
        return redirect('home')
    
class UsuarioCreateView(UserPassesTestMixin, CreateView):
    model = Usuario
    form_class = RegistroForm 
    template_name = 'usuarios/usuario_crear.html'
    success_url = reverse_lazy('usuarios:lista_usuarios')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f'Usuario "{user.username}" creado exitosamente.')
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para crear usuarios.')
        return redirect('home')
    
# Vista para CREAR un nuevo mensaje (formulario)
# Vista para CREAR un nuevo mensaje (formulario)
class MensajeCreateView(LoginRequiredMixin, CreateView):
    model = MensajeDirecto
    form_class = MensajeForm
    template_name = 'usuarios/enviar_mensaje.html'
    success_url = reverse_lazy('usuarios:mis_mensajes')

    def form_valid(self, form):
        """Asocia el mensaje con el usuario logueado antes de guardarlo."""
        form.instance.remitente = self.request.user
        messages.success(self.request, "Tu mensaje ha sido enviado al equipo de soporte.")
        return super().form_valid(form)

# Vista para LISTAR los mensajes del usuario
class MisMensajesListView(LoginRequiredMixin, ListView):
    """
    Vista para que un usuario vea la lista de sus propios mensajes enviados.
    """
    model = MensajeDirecto
    template_name = 'usuarios/mis_mensajes.html'
    context_object_name = 'mensajes'

    def get_queryset(self):
        """
        Retorna solo los mensajes enviados por el usuario logueado.
        """
        return MensajeDirecto.objects.filter(remitente=self.request.user)
    
    
class MensajeAdminListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Vista para que los administradores vean todos los mensajes enviados por los usuarios.
    """
    model = MensajeDirecto
    template_name = 'usuarios/lista_mensajes_admin.html'
    context_object_name = 'mensajes_admin'
    
    def get_queryset(self):
  
        queryset = super().get_queryset().order_by('estado', '-fecha_envio')

      
        
        search_query = self.request.GET.get('q')
        remitente_id = self.request.GET.get('remitente')
        estado_status = self.request.GET.get('estado')

        if search_query:
            
            queryset = queryset.filter(Q(mensaje__icontains=search_query) | Q(motivo__icontains=search_query))

        if remitente_id:
          
            queryset = queryset.filter(remitente_id=remitente_id)

        if estado_status:
            
            queryset = queryset.filter(estado=estado_status)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
       
        context['search_query'] = self.request.GET.get('q', '')
        context['remitente_id'] = self.request.GET.get('remitente', '')
        context['estado_status'] = self.request.GET.get('estado', '')

       
        context['usuarios'] = Usuario.objects.all()
        
        return context

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para ver esta página.')
        return redirect('home')
    
class MensajeResponderView(UserPassesTestMixin, View):
    """
    Vista para procesar el formulario de respuesta del administrador.
    No renderiza una plantilla, solo maneja el POST.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        # Obtiene el ID del mensaje desde el formulario del modal
        mensaje_id = request.POST.get('mensaje_id')
        respuesta = request.POST.get('respuesta')
        
        try:
            mensaje = MensajeDirecto.objects.get(id=mensaje_id)
            form = MensajeRespuestaForm({'respuesta': respuesta}, instance=mensaje)
            
            if form.is_valid():
                form.instance.usuario_respuesta = request.user
                form.instance.fecha_respuesta = timezone.now()
                form.instance.estado = 'respondido'
                form.save()
                messages.success(request, "La respuesta ha sido enviada y el mensaje se ha marcado como respondido.")
            else:
                messages.error(request, "Error al enviar la respuesta. Por favor, inténtalo de nuevo.")

        except MensajeDirecto.DoesNotExist:
            messages.error(request, "El mensaje no existe.")
        
        # Redirige siempre de vuelta a la lista de mensajes
        return redirect('usuarios:lista_mensajes_admin')