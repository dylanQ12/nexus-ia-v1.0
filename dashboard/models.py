from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Servicio(models.Model):
    foto = models.ImageField(upload_to='services/', null=True)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(max_length=580)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    
class Proyecto(models.Model):
    foto = models.ImageField(upload_to='projects/', null=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=580)
    enlace = models.URLField(max_length=300, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    
class Contacto(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    email = models.EmailField(max_length=255)
    mensaje =models.TextField(max_length=555, null=False)
    enviado = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f'{self.mensaje} - {str(self.enviado)}'
    