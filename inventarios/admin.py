from django.contrib import admin

# Register your models here.
from .models import Especie, Inventario

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin): ##cambiar a usuario 
    list_display = ('id', 'especie', 'cantidad', 'campania', 'usuario')