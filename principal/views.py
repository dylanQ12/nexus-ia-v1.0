from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from dashboard.models import Servicio, Proyecto, Contacto


# Función para obtener lista de servicios por estado Activo 
def list_services():
    services = Servicio.objects.filter(estado=True)
    data = {'services': services}
    return data


# Función para obtener lista de proyectos por estado Activo
def list_projects():
    projects = Proyecto.objects.filter(estado=True)
    data = {'projects': projects}
    return data


# Vista principal Home.
def home(request):
    services = list_services()
    projects = list_projects()
    context = {**services, **projects}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        
        if nombre and apellido and email and mensaje:
    
            contact = Contacto(
                nombre=nombre,
                apellido=apellido,
                email=email,
                mensaje=mensaje
            )
            contact.save()
            messages.success(request, '¡Mensaje enviado correctamente!')
            return redirect('/#contact')
    
    return render(request, "sections/home.html", context)

