from django.contrib import admin
from django.urls import include, path
from campanias.views import prueba_herencia
#from reforestasv.views import inicio

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', inicio, name='inicio'),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('campanias/',prueba_herencia, name='campanias'),
    path('mantenimientos/', include('mantenimientos.urls')),
]
