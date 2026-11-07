from django import forms
from .models import Campania

class CampaniaForm(forms.ModelForm):
    class Meta:
        model = Campania
        fields = ['titulo', 'descripcion', 'responsable', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '150'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'maxlength': '200'
            }),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# Validar que la fecha final no sea menor a la de inicio
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                self.add_error('fecha_fin', 'La fecha final no puede ser menor a la fecha de inicio.')

        return cleaned_data
        
