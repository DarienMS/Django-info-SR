from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Receta, Categoria, Comentario
from django.urls import reverse_lazy
from django.contrib import auth

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

def logout_view(request):
    auth.logout(request)
    return redirect('/') 




LOGOUT_REDIRECT_URL = '/'