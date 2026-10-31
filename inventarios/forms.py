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
                'placeholder': 'Ej. Ceiba, Maquilíshuat...'
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Especie.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Esta especie ya se encuentra registrada en el sistema.")
        return nombre