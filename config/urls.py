from django.contrib import admin
from django.urls import include, path
from campanias.views import prueba_herencia

from django.conf import settings
from django.conf.urls.static import static
#from reforestasv.views import inicio

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', inicio, name='inicio'),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('campanias/',prueba_herencia, name='campanias'),

    #Url para la vista de inventarios
   path('inventarios/', include('inventarios.urls'))
]

#se agrego para servir archivos multimedia durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
