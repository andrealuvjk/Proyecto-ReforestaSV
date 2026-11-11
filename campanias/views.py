
from usuarios.decorators import rol_requerido
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count, Q
from django.contrib import messages
from django.db.models import ProtectedError
from django.db import IntegrityError
from .models import Campania, Ubicacion
from .forms import CampaniaForm, UbicacionForm
from inventarios.models import Inventario, Especie
from mantenimientos.models import ArbolPlantado, Mantenimiento

# Create your views here.
from .models import Campania

def prueba_herencia(request):
    # Consultar todas las campañas optimizando la carga del usuario responsable
   # campanias = Campania.objects.select_related('responsable').all()
    campanias = Campania.objects.all()
    
    return render(request, 'campanias/campania_list.html', {
        'campanias': campanias
    })


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

def detalle_campania(request, pk):
    campania = get_object_or_404(Campania, pk=pk)
    
    # 1. Obtener los inventarios vinculados a esta campaña
    inventarios_list = campania.inventarios.select_related('especie', 'ubicacion', 'usuario').all()
    
    # 2. Conteo de inventarios y suma total de árboles
    total_inventarios = inventarios_list.count()
    total_arboles = inventarios_list.aggregate(total=Sum('cantidad'))['total'] or 0
    
    # 3. Métricas de salud de árboles creados para esta campaña
    arboles_stats = ArbolPlantado.objects.filter(
        inventario__campania=campania
    ).aggregate(
        sanos=Count('id', filter=Q(estado__iexact='SANO')),
        deteriorados=Count('id', filter=Q(estado__iexact='DETERIORADO')),
        perdidos=Count('id', filter=Q(estado__iexact='PERDIDO'))
    )
    
    # 4. Total de mantenimientos registrados en los árboles de esta campaña
    total_mantenimientos = Mantenimiento.objects.filter(
        arbol_plantado__inventario__campania=campania
    ).count()

    # 5. Agrupación y suma de ejemplares por especie dentro de esta campaña
    especies_desglose = Especie.objects.filter(
        inventarios__campania=campania
    ).annotate(
        total_sembrado=Sum('inventarios__cantidad', filter=Q(inventarios__campania=campania))
    ).distinct().order_by('-total_sembrado')

    context = {
        'campania': campania,
        'inventarios_list': inventarios_list,
        'total_inventarios': total_inventarios,
        'total_arboles': total_arboles,
        'arboles_stats': arboles_stats,
        'total_mantenimientos': total_mantenimientos,
        'especies_desglose': especies_desglose,
    }
    return render(request, 'campanias/detalle_campania.html', context)

# --- VISTAS DE UBICACIONES ---
@rol_requerido('ADMIN', 'RESPONSABLE','VOLUNTARIO')
def ubicacion_list(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'ubicacion/ubicacion_list.html', {'ubicaciones': ubicaciones})

@rol_requerido('ADMIN', 'RESPONSABLE')
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
@rol_requerido('ADMIN', 'RESPONSABLE')
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

@rol_requerido('ADMIN')
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

