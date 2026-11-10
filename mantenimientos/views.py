from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from usuarios.decorators import rol_requerido
from .models import Mantenimiento, ArbolPlantado
from .forms import MantenimientoForm, ArbolPlantadoForm


def mantenimiento_list(request):
    mantenimientos = Mantenimiento.objects.select_related('arbol_plantado').order_by('-fecha')

    fecha = request.GET.get('fecha')
    inventario_id = request.GET.get('inventario')
    if fecha:
        mantenimientos = mantenimientos.filter(fecha__date=fecha)

    if inventario_id:
        # Filtramos los mantenimientos cuyos árboles pertenezcan a este inventario específico
        mantenimientos = mantenimientos.filter(arbol_plantado__inventario_id=inventario_id)

    return render(request, 'mantenimientos/mantenimientos.html', {
        'mantenimientos': mantenimientos,
        'fecha': fecha,
        'inventario_id': inventario_id,
    })


def mantenimiento_crear(request):
    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Mantenimiento registrado exitosamente!')
            return redirect('mantenimientos:lista')
        else:
            messages.error(request, 'Ocurrió un error al registrar el mantenimiento. Verifique los datos.')
    else:
        form = MantenimientoForm()

    return render(request, 'mantenimientos/mantenimiento_form.html', {'form': form})

    return render(request, 'mantenimientos/mantenimiento_form.html', {'form': form})

def arbol_crear(request):
    if request.method == 'POST':
        form = ArbolPlantadoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, '¡Árbol plantado registrado correctamente!')
            return redirect('mantenimientos:arboles_lista')
        else:
            messages.error(request, 'Ocurrió un error al registrar el árbol plantado.')
    else:
        form = ArbolPlantadoForm()

    return render(
        request,
        'arboles-plantados/arboles_plantados.html',
        {'form': form}
    )

def arbol_editar(request, id):
    arbol = get_object_or_404(ArbolPlantado, id=id)

    if request.method == 'POST':
        form = ArbolPlantadoForm(request.POST, instance=arbol)

        if form.is_valid():
            form.save()
            messages.success(request, '¡Árbol plantado actualizado correctamente!')
            return redirect('mantenimientos:arboles_lista')
        else:
            messages.error(request, 'Ocurrió un error al actualizar el árbol plantado.')
    else:
        form = ArbolPlantadoForm(instance=arbol)

    return render(
        request,
        'arboles-plantados/arboles_plantados.html',
        {'form': form}
    )

def arboles_lista(request):
    arboles = ArbolPlantado.objects.select_related(
        'inventario'
    ).prefetch_related(
        'mantenimientos'
    ).all().order_by('-fecha')

    estado = request.GET.get('estado')

    if estado:
        arboles = arboles.filter(estado=estado)

    return render(
        request,
        'arboles-plantados/arboles_lista.html',
        {
            'arboles': arboles,
            'estado_seleccionado': estado
        }
    )


@rol_requerido('ADMIN', 'RESPONSABLE')
def arbol_eliminar(request, id):
    if request.method == 'POST':
        arbol = get_object_or_404(ArbolPlantado, id=id)
        messages.success(request, '¡Árbol plantado eliminado correctamente!')
        arbol.delete()

    return redirect('mantenimientos:arboles_lista')

@rol_requerido('ADMIN', 'RESPONSABLE','VOLUNTARIO')
def mantenimiento_editar(request, pk):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    if request.method == 'POST':
        form = MantenimientoForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Mantenimiento actualizado exitosamente!')
            return redirect('mantenimientos:lista')
        else:
            messages.error(request, 'Ocurrió un error al actualizar el mantenimiento.')
    else:
        form = MantenimientoForm(instance=mantenimiento)

    return render(request, 'mantenimientos/mantenimiento_form.html', {
        'form': form,
        'mantenimiento': mantenimiento,
    })

@rol_requerido('ADMIN', 'RESPONSABLE')
def mantenimiento_eliminar(request, pk):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    if request.method == 'POST':
        messages.success(request, '¡Mantenimiento eliminado correctamente!')
        mantenimiento.delete()
        return redirect('mantenimientos:lista')

    return render(request, 'mantenimientos/mantenimiento_confirmar_eliminar.html', {
        'mantenimiento': mantenimiento,
    })