from datetime import datetime, time

from django import forms
from django.conf import settings
from django.utils import timezone
import re

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

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']

        if len(descripcion) < 3:
            raise forms.ValidationError(
                'La descripción debe tener al menos 3 caracteres.'
            )
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 ]+', descripcion):
            raise forms.ValidationError(
                'La descripción no puede contener caracteres especiales.'
            )
        if len(set(descripcion.replace(' ', '').lower())) == 1:
            raise forms.ValidationError(
                'La descripción no puede ser una sola letra repetida.'
            )
        return descripcion

    def clean(self):
        cleaned_data = super().clean()
        arbol = cleaned_data.get('arbol_plantado')
        fecha = cleaned_data.get('fecha')
        descripcion = cleaned_data.get('descripcion')
        estado = cleaned_data.get('estado')

        if arbol and fecha and descripcion and estado:
            duplicados = Mantenimiento.objects.filter(
                arbol_plantado=arbol,
                fecha__date=fecha.date(),
                descripcion__iexact=descripcion,
            )
            if self.instance.pk:
                duplicados = duplicados.exclude(pk=self.instance.pk)

            if duplicados.exists() and arbol.estado == estado:
                self.add_error(
                    'descripcion',
                    'Ya existe un mantenimiento igual para este árbol en esta fecha. '
                    'Cambia la descripción o el estado.'
                )
        return cleaned_data

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
    