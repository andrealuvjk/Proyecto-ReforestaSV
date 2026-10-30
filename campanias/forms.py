from django import forms
from .models import Campania

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