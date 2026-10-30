from django.shortcuts import render

# Create your views here.
from .models import Campania

def prueba_herencia(request):
    # Consultar todas las campañas optimizando la carga del usuario responsable
   # campanias = Campania.objects.select_related('responsable').all()
    campanias = Campania.objects.all()
    
    return render(request, 'campanias/campania_list.html', {
        'campanias': campanias
    })