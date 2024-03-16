from django.urls import path
from . import views

urlpatterns = [
    
    # Vistas de listados.
    path('', views.services, name='servicios'),
    path('projects/', views.projects, name='proyectos'),
    
    # Vistas de formulario de registro.
    path('create-service/', views.create_service, name='crear-servicio'),
    path('create-project/', views.create_project, name='crear-proyecto'),
    
    # Vistas de formulario de edición.
    path('edit-service/<int:id>/', views.edit_service, name='editar-servicio'),
    path('edit-project/<int:id>/', views.edit_project, name='editar-proyecto'),
    
    # Vista de Inactivos.
    path('inactives-services', views.inactive_services, name='servicios-inactivos'),
    path('inactives-projects/', views.inactive_projects, name='proyectos-inactivos'),
    path('active-service/<int:id>/', views.activar_servicio, name='activar-servicio'),
    path('active-project/<int:id>/', views.activar_proyecto, name='activar-proyecto'),
    path('delete-service/<int:id>/', views.eliminar_servicio, name='eliminar-servicio'),
    path('delete-project/<int:id>/', views.eliminar_proyecto, name='eliminar-proyecto'),
    
    # Vista de Mensajes.
    path('mensajes/', views.mensajes, name='mensajes'),
    path('borrar-mensajes/', views.borrar_todos_los_mensajes, name='borrar-mensajes'),
    path('eliminar-mensaje/<int:id>/', views.eliminar_mensaje, name='eliminar-mensaje'),
    
    # Endpoint para obtener la cantidad de mensajes.
    path('api/cantidad-mensajes/', views.get_count_messages, name='cantidad-mensajes'),
    
    # Vista del perfil de usuario.
    path('perfil/', views.perfil, name='perfil'),
    
    
    

    
    
]
