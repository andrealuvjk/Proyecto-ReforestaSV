from django.contrib import admin

# Register your models here.

from .models import Usuario, Admin,Voluntario,Responsable

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display=('username','nombre','rol','email','telefono')
    list_filter = ('rol',)
    search_fields = ('username','nombre','email')

    admin.site.register(Admin)
    admin.site.register(Voluntario)
    admin.site.register(Responsable)

