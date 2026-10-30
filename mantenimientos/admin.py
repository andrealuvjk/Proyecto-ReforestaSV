from django.contrib import admin

from .models import ArbolPlantado, Mantenimiento

@admin.register(ArbolPlantado)
class ArbolPlantadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado', 'fecha', 'inventario')
    list_filter = ('estado',)

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'arbol_plantado', 'descripcion')