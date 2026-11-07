from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from django.db import IntegrityError
from .models import Campania, Ubicacion
from .forms import CampaniaForm, UbicacionForm

# Create your views here.
from .models import Campania

def prueba_herencia(request):
    # Consultar todas las campañas optimizando la carga del usuario responsable
   # campanias = Campania.objects.select_related('responsable').all()
    campanias = Campania.objects.all()
    
    return render(request, 'campanias/campania_list.html', {
        'campanias': campanias
    })

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


# Vista para editar una campaña existente
def editar_campania(request, pk):
    campania = get_object_or_404(Campania, pk=pk)
    if request.method == 'POST':
        # Pasamos 'instance=campania' para que el formulario se llene con los datos actuales y los sobrescriba
        form = CampaniaForm(request.POST, instance=campania)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaña actualizada exitosamente.')
            return redirect('campanias:listado_campanias')
        else:
            messages.error(request, 'Ocurrió un error al actualizar la campaña.')
    else:
        form = CampaniaForm(instance=campania)

    return render(request, 'campanias/campania_form.html', {
        'form': form,
        'campania': campania # Lo usamos para saber si estamos editando
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

# --- VISTAS DE UBICACIONES ---

def ubicacion_list(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'ubicacion/ubicacion_list.html', {'ubicaciones': ubicaciones})

def ubicacion_create(request):
    if request.method == 'POST':
        form = UbicacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Ubicación registrada exitosamente!')
            return redirect('campanias:ubicacion_list')
    else:
        form = UbicacionForm()
    return render(request, 'ubicacion/ubicacion_form.html', {'form': form})

def ubicacion_update(request, pk):
    ubicacion = get_object_or_404(Ubicacion, pk=pk)
    if request.method == 'POST':
        form = UbicacionForm(request.POST, instance=ubicacion)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Ubicación actualizada correctamente!')
            return redirect('campanias:ubicacion_list')
    else:
        form = UbicacionForm(instance=ubicacion)
    return render(request, 'ubicacion/ubicacion_form.html', {'form': form, 'editando': True})

def ubicacion_delete(request, pk):
    ubicacion = get_object_or_404(Ubicacion, pk=pk)
    
    if request.method == 'POST':
        # Verificamos si la ubicación ya está siendo usada en inventarios o campañas
        if ubicacion.inventarios.exists(): # Asumiendo related_name='inventarios'
            messages.error(request, 'No se puede eliminar esta ubicación porque ya está asignada a uno o más inventarios.')
            return redirect('campanias:ubicacion_list')
            
        try:
            ubicacion.delete()
            messages.success(request, '¡Ubicación eliminada correctamente!')
        except (ProtectedError, IntegrityError):
            messages.error(request, 'No se puede eliminar esta ubicación porque tiene registros vinculados.')
            
        return redirect('campanias:ubicacion_list')
        
    return render(request, 'ubicacion/ubicacion_confirm_delete.html', {'ubicacion': ubicacion})
