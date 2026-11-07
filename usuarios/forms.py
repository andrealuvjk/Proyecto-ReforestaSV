
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Usuario


class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username','localidad','institucion','telefono', 'email', 'nombre', 'rol',]
        widgets = {
                    'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. juanperez'}),
                    'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reubicación #1'}),
                    'institucion': forms.TextInput(attrs={'class': 'form-control',}, ),
                    'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 1234567890'}),
                    'email': forms.EmailInput(attrs={'class': 'form-control'}),
                    'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Pérez'}),
                    'rol': forms.Select(attrs={'class': 'form-select'}),
                
                    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hace que no sean obligatorios en la validación del formulario de Django
        self.fields['institucion'].required = False
        self.fields['localidad'].required = False  
        
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repita la contraseña'})

class UsuarioEditarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'email', 'telefono', 'rol', 'institucion', 'localidad',]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. juanperez'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reubicación #1'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control',}, ),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 1234567890'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Pérez'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
           
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institucion'].required = False
        self.fields['localidad'].required = False