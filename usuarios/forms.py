
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Usuario


class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username','localidad','institucion','telefono', 'email', 'nombre', 'rol']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hace que no sean obligatorios en la validación del formulario de Django
        self.fields['institucion'].required = False
        self.fields['localidad'].required = False  

class UsuarioEditarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'email', 'telefono', 'rol', 'institucion', 'localidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institucion'].required = False
        self.fields['localidad'].required = False