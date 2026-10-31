from django import forms
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

        # Sobrescribimos el comportamiento de los select para cambiar el texto por defecto
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['especie'].empty_label = "Seleccione una especie..."
        self.fields['campania'].empty_label = "Seleccione una campaña..."
        self.fields['ubicacion'].empty_label = "Seleccione una ubicación..."
        self.fields['usuario'].empty_label = "Seleccione un usuario..."