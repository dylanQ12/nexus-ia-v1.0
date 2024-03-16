#from django.contrib.auth.decorators import login_required
from .models import Contacto

def cantidad_mensajes(request):
    return {'cantidad_mensajes': Contacto.objects.count()}