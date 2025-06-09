from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import *

# Create your views here.
def home(request):
    tareas = []
    estados = []
    estado_id = request.GET.get('estado')

    if request.user.is_authenticated:
        estados = EstadoTarea.objects.all()
        tareas = Tarea.objects.filter(usuario=request.user)

        if estado_id:
            tareas = tareas.filter(estado_id=estado_id)

    data = {
        'tareas': tareas,
        'estados': estados,
        'estado_seleccionado': estado_id,
    }
    return render(request, "home.html",data)

def iniciar_session(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige al home o donde quieras
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')

    return render(request, "login.html")

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está en uso.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('home')
    return render(request, "registro.html")

def cerrar_session(request):
    logout(request)
    return redirect('home')

@login_required
def crear_tarea(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        vencimiento = request.POST.get('vencimiento')

        estado = EstadoTarea.objects.filter(nombre='Pendiente').first()

        Tarea.objects.create(
            usuario=request.user,
            titulo=titulo,
            descripcion=descripcion,
            vencimiento=vencimiento,
            estado=estado
        )
        return redirect('home')

    return redirect('home')

@login_required
def iniciar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    en_proceso = EstadoTarea.objects.get(nombre='En proceso')
    tarea.estado = en_proceso
    tarea.save()
    return redirect('home')  

@login_required
def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    completada  = EstadoTarea.objects.get(nombre='Completada')
    tarea.estado = completada
    tarea.save()
    return redirect('home')  

@login_required
@require_POST
def actualizar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id, usuario=request.user)
    titulo = request.POST.get('titulo')
    descripcion = request.POST.get('descripcion')
    vencimiento = request.POST.get('vencimiento')
    estado_id = request.POST.get('estado')

    if titulo:
        tarea.titulo = titulo
    if descripcion:
        tarea.descripcion = descripcion
    if vencimiento:
        tarea.vencimiento = vencimiento
    if estado_id:
        from .models import EstadoTarea
        estado = EstadoTarea.objects.filter(id=estado_id).first()
        if estado:
            tarea.estado = estado
    tarea.save()
    return redirect('home') 

@login_required
def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('home')
    return redirect('home')