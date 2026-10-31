from django.urls import path
from . import views

app_name = 'inventarios'

urlpatterns = [
    # Rutas para Especies
    path('especies/', views.especie_list, name='especie_list'),
    path('especies/nueva/', views.especie_crear, name='especie_crear'),
    path('especies/<int:pk>/editar/', views.especie_editar, name='especie_editar'),
    path('especies/<int:pk>/eliminar/', views.especie_eliminar, name='especie_eliminar'),
]