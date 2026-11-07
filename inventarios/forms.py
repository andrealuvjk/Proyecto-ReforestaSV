import re
from django import forms
from .models import Especie

class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la especie',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Ceiba, Maquilíshuat...',
                'maxlength': '100',
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        
        if not nombre:
            raise forms.ValidationError("El nombre de la especie es obligatorio.")
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo debe contener letras y espacios, sin números ni caracteres especiales.")
        
        if Especie.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Esta especie ya se encuentra registrada en el sistema.")
            
        return nombre
from .models import Inventario

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['especie', 'cantidad', 'campania', 'ubicacion', 'usuario', 'imagen']  # <-- Aquí se cambió de 'img_url' a 'imagen'

        labels = {
            'especie': 'Especie de árbol',
            'cantidad': 'Cantidad',
            'campania': 'Campaña de reforestación',
           'imagen': 'Imagen de referencia',  # <-- Aquí personalizas el texto
            'ubicacion': 'Ubicación',
            'usuario': 'Usuario responsable o voluntario',
        }

        widgets = {
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 50'}),
            'campania': forms.Select(attrs={'class': 'form-select',}, ),
            #'img_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com/imagen.jpg'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
        }


        error_messages = {
            'especie': {
                'required': 'Debe seleccionar una especie obligatoriamente.',
                'invalid_choice': 'Seleccione una especie válida.',
            },
            'cantidad': {
                'required': 'La cantidad de árboles es un campo obligatorio.',
                'invalid': 'Por favor, ingrese un número entero válido.',
            },
            'campania': {
                'required': 'Debe asociar el inventario a una campaña.',
            },
            'ubicacion': {
                'required': 'La ubicación es obligatoria para este lote.',
            },
            'usuario': {
                'required': 'Debe asignar un usuario responsable o voluntario.',
            }
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise forms.ValidationError('La cantidad de ejemplares no puede ser un número negativo.')
        return cantidad

        # Sobrescribimos el comportamiento de los select para cambiar el texto por defecto
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['especie'].empty_label = "Seleccione una especie..."
        self.fields['campania'].empty_label = "Seleccione una campaña..."
        self.fields['ubicacion'].empty_label = "Seleccione una ubicación..."
        self.fields['usuario'].empty_label = "Seleccione un usuario..."