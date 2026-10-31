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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from django.db import IntegrityError
from .models import Campania
from .forms import CampaniaForm

# Tu vista para mostrar la lista
def prueba_herencia(request):
    campanias = Campania.objects.all()
    return render(request, 'campanias/campania_list.html', {
        'campanias': campanias
    })

# Vista para guardar el formulario de nueva campaña
def crear_campania(request):
    if request.method == 'POST':
        form = CampaniaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaña guardada exitosamente.')
            return redirect('campanias:listado_campanias')
        else:
            messages.error(request, 'Ocurrió un error al guardar la campaña.')
    else:
        form = CampaniaForm()

    return render(request, 'campanias/campania_form.html', {
        'form': form
    })

# Vista para borrar protegiendo la integridad referencial
def eliminar_campania(request, pk):
    campania = get_object_or_404(Campania, pk=pk)
    if request.method == 'POST':
        try:
            campania.delete()
            messages.success(request, 'Campaña eliminada correctamente.')
        except (ProtectedError, IntegrityError):
            messages.error(request, 'No se puede eliminar esta campaña porque tiene registros vinculados.')
        return redirect('campanias:listado_campanias')

    return render(request, 'campanias/campania_confirm_delete.html', {
        'campania': campania
    })
