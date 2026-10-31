from django import forms
from .models import Mantenimiento, ArbolPlantado


class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = ['fecha', 'descripcion', 'arbol_plantado']
        widgets = {
            'fecha': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M',
            ),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'arbol_plantado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].input_formats = ['%Y-%m-%dT%H:%M']

class ArbolPlantadoForm(forms.ModelForm):
    class Meta:
        model = ArbolPlantado
        fields = ['fecha', 'estado', 'inventario']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'inventario': forms.Select(attrs={
                'class': 'form-select'
            }),
        }