
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
import re
from .models import Usuario


class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username','localidad','institucion','telefono', 'email', 'nombre', 'rol',]
        widgets = {
                    'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. juanperez'}),
                    'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reubicación #1'}),
                    'institucion': forms.TextInput(attrs={'class': 'form-control',}, ),
                    'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 1234567890'}),
                    'email': forms.EmailInput(attrs={'class': 'form-control'}),
                    'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Pérez'}),
                    'rol': forms.Select(attrs={'class': 'form-select'}),
                
                    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hace que no sean obligatorios en la validación del formulario de Django
        self.fields['institucion'].required = False
        self.fields['localidad'].required = False 
        self.fields['telefono'].required = False 
        
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repita la contraseña'})

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise ValidationError("El nombre de usuario es obligatorio.")
        
        # Validar que no existan usernames duplicados (ignorando mayúsculas/minúsculas)
        if Usuario.objects.filter(username__iexact=username).exists():
            raise ValidationError("Ya existe un usuario registrado con este nombre de usuario.")
        return username

    def clean_nombre(self):
        # Normalizamos espacios para evitar dobles espacios que provoquen falsos diferentes
        nombre_raw = self.cleaned_data.get('nombre', '')
        nombre = ' '.join(nombre_raw.split()).strip()
        
        if not nombre:
            raise ValidationError("El campo nombre es obligatorio.")
            
        if len(nombre) > 200:
            raise ValidationError("El nombre no puede exceder los 200 caracteres.")
            
        letras_count = sum(c.isalpha() for c in nombre)
        if letras_count < 3:
            raise ValidationError("El nombre debe contener al menos 3 letras.")
            
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise ValidationError("El nombre no debe contener números ni caracteres especiales.")
            
        palabras = nombre.split()
        if len(palabras) < 2:
            raise ValidationError("Debe ingresar al menos un nombre y un apellido.")

        # Validar duplicados exactos del nombre completo (ignorando mayúsculas/minúsculas)
        query = Usuario.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
            
        if query.exists():
            raise ValidationError("Ya existe un usuario registrado con este mismo nombre y apellido.")
            
        return nombre

class UsuarioEditarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'email', 'telefono', 'rol', 'institucion', 'localidad',]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. juanperez'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reubicación #1'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control',}, ),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 1234567890'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Pérez'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
           
            }
    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise ValidationError("El nombre de usuario es obligatorio.")
        
        query = Usuario.objects.filter(username__iexact=username)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
            
        if query.exists():
            raise ValidationError("Ya existe otro usuario registrado con este nombre de usuario.")
        return username

    def clean_nombre(self):
        nombre_raw = self.cleaned_data.get('nombre', '')
        nombre = ' '.join(nombre_raw.split()).strip()
        
        if not nombre:
            raise ValidationError("El campo nombre es obligatorio.")
            
        if len(nombre) > 200:
            raise ValidationError("El nombre no puede exceder los 200 caracteres.")
            
        letras_count = sum(c.isalpha() for c in nombre)
        if letras_count < 3:
            raise ValidationError("El nombre debe contener al menos 3 letras.")
            
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise ValidationError("El nombre no debe contener números ni caracteres especiales.")
            
        palabras = nombre.split()
        if len(palabras) < 2:
            raise ValidationError("Debe ingresar al menos un nombre y un apellido.")

        # Validar duplicados exactos del nombre completo en edición
        query = Usuario.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
            
        if query.exists():
            raise ValidationError("Ya existe otro usuario registrado con este mismo nombre y apellido.")
            
        return nombre

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institucion'].required = False
        self.fields['localidad'].required = False