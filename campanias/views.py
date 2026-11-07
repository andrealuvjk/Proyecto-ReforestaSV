from usuarios.decorators import rol_requerido
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from django.db import IntegrityError
from .models import Campania
from .forms import CampaniaForm

@rol_requerido('ADMIN', 'RESPONSABLE')
def ver_campanias(request):
    campanias = Campania.objects.all()
    return render(request, 'campanias/campania_list.html', {
        'campanias': campanias
    })

@rol_requerido('ADMIN', 'RESPONSABLE')
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

@rol_requerido('ADMIN', 'RESPONSABLE')
def editar_campania(request, pk):
    campania = get_object_or_404(Campania, pk=pk)
    if request.method == 'POST':
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
        'campania': campania
    })

@rol_requerido('ADMIN', 'RESPONSABLE')
def eliminar_campania(request, pk):
    campania = get_object_or_404(Campania, pk=pk)

    # Restricción: No eliminar si la campaña tiene inventarios vinculados
    if hasattr(campania, 'inventarios') and campania.inventarios.exists():
        messages.error(request, 'No se puede eliminar esta campaña porque ya tiene registros de inventario asociados.')
        return redirect('campanias:listado_campanias')

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
    
