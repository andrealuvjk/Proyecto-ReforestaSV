from django.shortcuts import render, redirect, get_object_or_404
from .models import Mantenimiento, ArbolPlantado
from .forms import MantenimientoForm, ArbolPlantadoForm


def mantenimiento_list(request):
    mantenimientos = Mantenimiento.objects.select_related('arbol_plantado').order_by('-fecha')

    fecha = request.GET.get('fecha')
    if fecha:
        mantenimientos = mantenimientos.filter(fecha__date=fecha)

    return render(request, 'mantenimientos/mantenimientos.html', {
        'mantenimientos': mantenimientos,
        'fecha': fecha,
    })


def mantenimiento_crear(request):
    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mantenimientos:lista')
    else:
        form = MantenimientoForm()

    return render(request, 'mantenimientos/mantenimiento_form.html', {'form': form})

def arbol_crear(request):
    if request.method == 'POST':
        form = ArbolPlantadoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('mantenimientos:arboles_lista')
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
            return redirect('mantenimientos:arboles_lista')
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
    ).all().order_by('-fecha')

    return render(
        request,
        'arboles-plantados/arboles_lista.html',
        {'arboles': arboles}
    )

def arbol_eliminar(request, id):
    if request.method == 'POST':
        arbol = get_object_or_404(ArbolPlantado, id=id)
        arbol.delete()

    return redirect('mantenimientos:arboles_lista')

def mantenimiento_editar(request, pk):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    if request.method == 'POST':
        form = MantenimientoForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            form.save()
            return redirect('mantenimientos:lista')
    else:
        form = MantenimientoForm(instance=mantenimiento)

    return render(request, 'mantenimientos/mantenimiento_form.html', {
        'form': form,
        'mantenimiento': mantenimiento,
    })


def mantenimiento_eliminar(request, pk):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    if request.method == 'POST':
        mantenimiento.delete()
        return redirect('mantenimientos:lista')

    return render(request, 'mantenimientos/mantenimiento_confirmar_eliminar.html', {
        'mantenimiento': mantenimiento,
    })