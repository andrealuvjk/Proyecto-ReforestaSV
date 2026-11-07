from django import forms
from .models import Campania
from .models import Ubicacion, Campania

class CampaniaForm(forms.ModelForm):
    class Meta:
        model = Campania
        fields = ['titulo', 'descripcion', 'responsable', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }




class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['zona', 'ubicacion']
        labels = {
            'zona': 'Zona geográfica',
            'ubicacion': 'Dirección o descripción de ubicación',
        }
        widgets = {
            'zona': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Zona Paracentral'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Parque Nacional El Boquerón'}),
        }