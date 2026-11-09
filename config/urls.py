from django.contrib import admin
from django.urls import include, path
from campanias.views import ver_campanias

from django.conf import settings
from django.conf.urls.static import static
from .views import home_redirect
#from reforestasv.views import inicio

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', inicio, name='inicio'),
# ]

urlpatterns = [
    path('',home_redirect,name='home'),
    path('admin/', admin.site.urls),
    path('campanias/',include('campanias.urls')),

    #Url para la vista de inventarios
   path('inventarios/', include('inventarios.urls')),
    path('mantenimientos/', include('mantenimientos.urls')),
    #URL Usuarios
    path('usuarios/', include('usuarios.urls')),
   ##  path('inventarios/', include('inventarios.urls')),

   # Rutas por defecto para login, logout, cambio de contraseña, etc.
    path('accounts/', include('django.contrib.auth.urls')),
]

#se agrego para servir archivos multimedia durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
