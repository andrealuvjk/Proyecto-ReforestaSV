from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventario
from .forms import InventarioForm
from campanias.models import Campania

def inventario_list(view_request):
    """Vista para listar los inventarios existentes con sus relaciones."""
    inventarios = Inventario.objects.all()
    campanias = Campania.objects.all()  # Obtenemos todas las campañas para llenar el select
    campania_id = view_request.GET.get('campania')
    
    if campania_id:
        # Filtramos los inventarios que coincidan con la campaña seleccionada
        inventarios = inventarios.filter(campania_id=campania_id)
        
    context = {
        'inventarios': inventarios,
        'campanias': campanias,
        'campania_seleccionada': campania_id,  # Para mantener la opción seleccionada en el select
    }
    return render(view_request, 'inventarios/inventario_list.html', context)

def inventario_create(view_request):
    if view_request.method == 'POST':
        # Ojo: request.FILES es obligatorio para capturar la foto del dispositivo
        form = InventarioForm(view_request.POST, view_request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventarios:inventario_list')
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
            return redirect('inventarios:inventario_list')
    else:
        form = InventarioForm(instance=inventario)
    
    return render(request, 'inventarios/inventario_form.html', {'form': form, 'editando': True})

def inventario_delete(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        inventario.delete() # Método nativo de Django para borrar de la base de datos
        return redirect('inventarios:inventario_list')
    
    return render(request, 'inventarios/inventario_confirm_delete.html', {'inventario': inventario})
