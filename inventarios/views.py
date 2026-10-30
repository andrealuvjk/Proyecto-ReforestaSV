from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventario
from .forms import InventarioForm

def inventario_list(view_request):
    """Vista para listar los inventarios existentes con sus relaciones."""
    inventarios = Inventario.objects.all()
    return render(view_request, 'inventarios/inventario_list.html', {'inventarios': inventarios})

def inventario_create(view_request):
    if view_request.method == 'POST':
        # Ojo: request.FILES es obligatorio para capturar la foto del dispositivo
        form = InventarioForm(view_request.POST, view_request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventario_list')
    else:
        form = InventarioForm()
    
    return render(view_request, 'inventarios/inventario_form.html', {'form': form})

def inventario_update(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        # Pasamos instance=inventario para que cargue los datos actuales en el formulario
        form = InventarioForm(request.POST, request.FILES, instance=inventario)
        if form.is_valid():
            form.save()
            return redirect('inventario_list')
    else:
        form = InventarioForm(instance=inventario)
    
    return render(request, 'inventarios/inventario_form.html', {'form': form, 'editando': True})

def inventario_delete(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        inventario.delete() # Método nativo de Django para borrar de la base de datos
        return redirect('inventario_list')
    
    return render(request, 'inventarios/inventario_confirm_delete.html', {'inventario': inventario})
