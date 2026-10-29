from django.shortcuts import get_object_or_404, redirect, render

from .forms import MantenimientoForm
from .models import Mantenimiento


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