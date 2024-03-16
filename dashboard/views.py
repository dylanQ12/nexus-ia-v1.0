from django.shortcuts import redirect, render, get_object_or_404
from .models import Servicio, Proyecto, Contacto
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


# Vista del Login para iniciar sesión.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('usuario')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo {user.first_name}!')
            return redirect('servicios')
        else:
            messages.error(request, '¡Usuario o contraseña incorrectos!')
            return redirect('login')
    
    return render(request, 'login.html')


# Vista del Logout para cerrar sesión.
def logout_view(request):
    logout(request)
    return redirect('login')


# Vista de la plantilla principal Dashboard.
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "Dashboard/dashboard.html")


# Formulario del Perfil del usuario.
@login_required
def perfil(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password')
        
        if email and new_password:
            usuario = request.user
            usuario.email = email
            usuario.set_password(new_password)
            usuario.save()
            
            update_session_auth_hash(request, usuario)
            
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('perfil')
        else:
            messages.error(request, 'La nueva contraseña no puede estar vacía.')
        
    return render(request, 'perfil.html')


# Vista de lista de Servicios.
@login_required
def services(request):
    services = Servicio.objects.filter(estado=True).order_by('fecha_creacion')
    data = {'services': services}
    return render(request, "services/list-services.html", data)


# Vista de lista de Proyectos.
@login_required
def projects(request):
    projects = Proyecto.objects.filter(estado=True).order_by("fecha_creacion")
    data = {'projects': projects}
    return render(request, "projects/list-projects.html", data)

# Vista de Mensajes.
@login_required
def mensajes(request):
    mensajes = Contacto.objects.all().order_by("enviado")
    
    paginator = Paginator(mensajes, 5) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
   
    return render(request, "mensajes.html", context)


# Obtener la cantidad de mensajes.
@login_required
def get_count_messages(request):
     cantidad_mensajes = Contacto.objects.count()
     return JsonResponse({'cantidad_mensajes': cantidad_mensajes})
    

# Eliminar un mensaje.
@login_required
def eliminar_mensaje(request, id):
    if request.method == 'POST':
        mensaje = get_object_or_404(Contacto, pk=id)
        mensaje.delete()
        messages.success(request, "¡Mensaje eliminado correctamente!")
        return redirect(reverse('mensajes'))
    

# Borrar todos los Mensajes.
@login_required
def borrar_todos_los_mensajes(request):
    if request.method == 'POST':
        # Verificar si hay mensajes para borrar
        if Contacto.objects.exists():  # Esto comprueba si hay al menos un mensaje en la base de datos
            Contacto.objects.all().delete()
            messages.success(request, "¡Todos los mensajes se borraron correctamente!")
        else:
            # Si no hay mensajes, enviar un mensaje informativo
            messages.info(request, "¡No hay mensajes disponibles para borrar!")
        return redirect('mensajes')
    return render(request, 'mensajes.html')


# Vistas de creación de Formularios.

# Formulario de Servicios
@login_required
def create_service(request):
     if request.method == 'POST':
        foto = request.FILES.get('foto') if 'foto' in request.FILES else None
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('desc')
        
        if titulo and descripcion:
            service = Servicio(
                foto=foto, 
                titulo=titulo, 
                descripcion=descripcion,
            )
            service.save()
            messages.success(request, '¡Servicio guardado correctamente!')
            return redirect(reverse('servicios'))
     
     return render(request, "services/create-service.html")
 
 
# Formulario de Proyectos. 
@login_required
def create_project(request):
    if request.method == 'POST':
        foto = request.FILES.get('foto') if 'foto' in request.FILES else None
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('desc')
        enlace = request.POST.get('enlace')
        
        if titulo and descripcion:
            project = Proyecto(
                foto=foto, 
                titulo=titulo,
                enlace=enlace, 
                descripcion=descripcion
            )
            project.save()
            messages.success(request, '¡Proyecto guardado correctamente!')
            return redirect(reverse('proyectos'))

    return render(request, "projects/create-project.html")


# Vistas de Edición.

# Formulario de Servicio.
@login_required
def edit_service(request, id):
    service = get_object_or_404(Servicio, pk=id)
    data = {'service': service}
    
    # Actualizar servicios
    if request.method == 'POST':
       service.foto = request.FILES['foto'] if 'foto' in request.FILES else service.foto
       service.titulo = request.POST.get('titulo')
       service.descripcion = request.POST.get('desc')
       service.estado = request.POST.get('estado', '') == 'on'
    
       service.save() 
       messages.success(request, '¡Servicio actualizado correctamente!')
       return redirect(reverse('servicios'))
       
    return render(request, "services/edit-service.html", data)


# Formulario de Proyectos.
@login_required
def edit_project(request, id):
    project = get_object_or_404(Proyecto, pk=id)
    data = {'project': project}
    
    # Actualizar  proyectos
    if request.method == 'POST':
       project.foto = request.FILES['foto'] if 'foto' in request.FILES else project.foto
       project.titulo = request.POST.get('titulo')
       project.enlace = request.POST.get('enlace')
       project.descripcion = request.POST.get('desc')
       project.estado = request.POST.get('estado', '') == 'on'
       
       project.save()
       messages.success(request, '¡Proyecto actualizado correctamente!')
       return redirect(reverse('proyectos'))
       
    return render(request, 'projects/edit-project.html', data)


# Vista de Servicios Inactivos
@login_required
def inactive_services(request):
    services = Servicio.objects.filter(estado=False).order_by("fecha_creacion")
    data = {'services': services}
    return render(request, "services/inactive-services.html", data)


# Vista de Proyectos Inactivos.
@login_required
def inactive_projects(request):
    projects = Proyecto.objects.filter(estado=False).order_by("fecha_creacion")
    data = {'projects': projects}
    return render(request, "projects/inactive-projects.html", data)


# Activar Servicio.
@login_required
def activar_servicio(request, id):
    if request.method == 'POST':
      service = get_object_or_404(Servicio, pk=id)
      service.estado = True
      service.save()
      messages.success(request, '¡Servicio activado correctamente!')
      return redirect(reverse('servicios'))  


# Activar Proyecto.
@login_required
def activar_proyecto(request, id):
    if request.method == 'POST':
      project = get_object_or_404(Proyecto, pk=id)
      project.estado = True
      project.save()
      messages.success(request, '¡Proyecto activado correctamente!')
      return redirect(reverse('proyectos'))
    
    
# Eliminar servicio inactivo.    
@login_required
def eliminar_servicio(request, id):
    if request.method == 'POST':
        service = get_object_or_404(Servicio, pk=id)
        service.delete()
        messages.success(request, "¡Servicio eliminado correctamente!")
        return redirect(reverse('servicios-inactivos'))
        

# Eliminar proyecto inactivo.
@login_required
def eliminar_proyecto(request, id):
    if request.method == 'POST':
        project = get_object_or_404(Proyecto, pk=id)
        project.delete()
        messages.success(request, "¡Proyecto eliminado correctamente!")
        return redirect(reverse('proyectos-inactivos'))