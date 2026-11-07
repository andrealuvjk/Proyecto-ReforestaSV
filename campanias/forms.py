from django import forms
from .models import Campania
from .models import Ubicacion, Campania
from django.core.exceptions import ValidationError
import re

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
            'zona': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Zona A o Zona 1'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Apopa'}),
        }

    def clean_zona(self):
        zona = self.cleaned_data.get('zona', '').strip()
        
        if len(zona) < 2:
            raise ValidationError("La zona debe tener al menos 2 caracteres.")

        # Validar que contenga al menos una letra (evita que sean solo números o símbolos)
        if not any(c.isalpha() for c in zona):
            raise ValidationError("La zona debe contener al menos una letra.")
            
        # Evitar spam de letras repetidas (ej. "jjjjjj")
        if re.search(r'(.)\1{4,}', zona):
            raise ValidationError("La zona contiene demasiados caracteres repetidos consecutivos.")
            
        # Bloquear caracteres especiales extraños (permite letras, números, espacios y guiones)
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ0-9\s-]+$', zona):
            raise ValidationError("La zona no debe contener caracteres especiales.")
            
        return zona

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion', '').strip()
        
        if len(ubicacion) < 3:
            raise ValidationError("La ubicación debe tener al menos 3 caracteres.")
            
        # Evitar spam de letras repetidas
        if re.search(r'(.)\1{4,}', ubicacion):
            raise ValidationError("La ubicación contiene demasiados caracteres repetidos consecutivos.")
            
        # Bloquear caracteres especiales no permitidos en la dirección
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ0-9\s,\.-]+$', ubicacion):
            raise ValidationError("La ubicación contiene caracteres especiales no permitidos.")
            
        return ubicacion

    def clean(self):
        cleaned_data = super().clean()
        zona = cleaned_data.get('zona')
        ubicacion = cleaned_data.get('ubicacion')

        # Validar duplicados por la COMBINACIÓN exacta de Zona + Ubicación (ignorando mayúsculas/minúsculas)
        if zona and ubicacion:
            query = Ubicacion.objects.filter(zona__iexact=zona, ubicacion__iexact=ubicacion)
            
            # Si estamos editando, excluimos el registro actual para que no choque consigo mismo
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
                
            if query.exists():
                # Vinculamos el error directamente al campo 'zona' para que se muestre en rojo en la interfaz
                self.add_error('zona', "Ya existe un registro con esta misma combinación de zona y ubicación.")

        return cleaned_data