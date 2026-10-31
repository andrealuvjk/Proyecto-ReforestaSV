from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventario
from .forms import InventarioForm
from campanias.models import Campania

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
