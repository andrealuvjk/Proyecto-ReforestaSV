from datetime import datetime, time

from django import forms
from django.conf import settings
from django.utils import timezone

from .models import Mantenimiento, ArbolPlantado


class MantenimientoForm(forms.ModelForm):
    fecha = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d',
        ),
    )
    estado = forms.ChoiceField(
        label='Estado del árbol',
        choices=[('', 'Seleccione el estado')] + list(ArbolPlantado._meta.get_field('estado').choices),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Mantenimiento
        fields = ['fecha', 'descripcion', 'arbol_plantado']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'arbol_plantado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['arbol_plantado'].error_messages['required'] = (
            'Por favor, selecciona el árbol plantado.'
        )
        self.fields['fecha'].error_messages['required'] = (
            'Por favor, ingresa la fecha del mantenimiento.'
        )
        self.fields['descripcion'].error_messages['required'] = (
            'Por favor, ingresa la descripción del mantenimiento.'
        )
        self.fields['estado'].error_messages['required'] = (
            'Por favor, selecciona el estado del árbol.'
        )

        if self.instance.pk:
            fecha = self.instance.fecha
            if timezone.is_aware(fecha):
                fecha = timezone.localtime(fecha)
            self.initial['fecha'] = fecha.date()
            self.initial['estado'] = self.instance.arbol_plantado.estado

    def clean_fecha(self):
        valor = datetime.combine(self.cleaned_data['fecha'], time.min)
        if settings.USE_TZ:
            valor = timezone.make_aware(valor)
        return valor

    def save(self, commit=True):
        mantenimiento = super().save(commit=commit)
        if commit:
            mantenimiento.arbol_plantado.cambiar_estado(self.cleaned_data['estado'])
        return mantenimiento

class ArbolPlantadoForm(forms.ModelForm):

    class Meta:
        model = ArbolPlantado
        fields = ['fecha', 'estado', 'inventario']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'inventario': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['fecha'].error_messages['required'] = (
            'Por favor, ingresa la fecha del árbol.'
        )
        self.fields['estado'].error_messages['required'] = (
            'Por favor, selecciona el estado del árbol.'
        )
        self.fields['inventario'].error_messages['required'] = (
            'Por favor, selecciona un inventario.'
        )
    