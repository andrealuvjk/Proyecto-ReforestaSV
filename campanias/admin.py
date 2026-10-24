from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Ubicacion, Campania

@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('zona', 'ubicacion')

@admin.register(Campania)
class CampaniaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'responsable', 'fecha_inicio', 'fecha_fin')
    list_filter = ('fecha_inicio',)