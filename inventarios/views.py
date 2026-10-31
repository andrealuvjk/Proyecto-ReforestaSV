from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Especie
from .forms import EspecieForm

# 1. Listar especies
def especie_list(request):
    especies = Especie.objects.all()
    return render(request, 'especies/especie_list.html', {'especies': especies})

# 2. Crear nueva especie
def especie_crear(request):
    if request.method == 'POST':
        form = EspecieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Especie guardada correctamente!')
            return redirect('inventarios:especie_list')
    else:
        form = EspecieForm()
    return render(request, 'especies/especie_form.html', {'form': form, 'titulo': 'Nueva Especie'})

# 3. Editar especie
def especie_editar(request, pk):
    especie = get_object_or_404(Especie, pk=pk)
    if request.method == 'POST':
        form = EspecieForm(request.POST, instance=especie)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Especie actualizada correctamente!')
            return redirect('inventarios:especie_list')
    else:
        form = EspecieForm(instance=especie)
    return render(request, 'especies/especie_form.html', {'form': form, 'titulo': 'Editar Especie'})

# 4. Eliminar especie
def especie_eliminar(request, pk):
    especie = get_object_or_404(Especie, pk=pk)
    
    if especie.inventarios.exists():
        messages.error(
            request, 
            f"No se puede eliminar la especie '{especie.nombre}' porque está asignada a uno o más inventarios."
        )
        return redirect('inventarios:especie_list')
        
    if request.method == 'POST':
        especie.delete()
        messages.success(request, 'Especie eliminada correctamente.')
        return redirect('inventarios:especie_list')
        
    return render(request, 'especies/especie_confirm_delete.html', {'especie': especie})