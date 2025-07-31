from django.shortcuts import render,redirect
from django.views.generic import CreateView,UpdateView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import UserPassesTestMixin 
from .forms import RegistroForm
from .forms import Usuario
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


class Registro(CreateView):
	
	form_class = RegistroForm
	success_url = reverse_lazy('login')
	template_name = 'usuarios/registro.html'


class UsuarioListView(UserPassesTestMixin, ListView):
    model = Usuario 
    template_name = 'usuarios/lista_usuarios.html'
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('home')
    
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