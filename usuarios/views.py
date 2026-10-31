# usuarios/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import UsuarioForm,UsuarioEditarForm
from .models import Usuario

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente!')  # Corregido género
            return redirect('usuarios:usuarios')
    else:
        form = UsuarioForm()
        
    return render(request, 'usuarios/usuario_form.html', {
        'form': form, 
        'titulo': 'Nuevo Usuario'
    })


def usuarios_list(request):
    tipo_rol = request.GET.get('tipo', '')
    
    usuarios = Usuario.objects.all()
    if tipo_rol:
        usuarios = usuarios.filter(rol=tipo_rol)

    return render(request, 'usuarios/usuarios.html', {
        'usuarios': usuarios,
    })

# Vista de Edición
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente!')
            return redirect('usuarios:usuarios')
    else:
        form = UsuarioEditarForm(instance=usuario)

    return render(request, 'usuarios/usuario_form.html', {
        'form': form,
        'usuario': usuario
    })

# Vista de Eliminación
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente!')
        return redirect('usuarios:usuarios')
    
    return render(request, 'usuarios/usuario_confirm_delete.html', {'usuario': usuario})