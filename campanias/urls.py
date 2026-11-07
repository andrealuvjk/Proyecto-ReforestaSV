from django.urls import path
from . import views

app_name = 'campanias'

urlpatterns = [
    # Mantiene tu vista actual prueba_herencia para cargar el listado
    path('listado/', views.prueba_herencia, name='listado_campanias'),
    path('crear/', views.crear_campania, name='crear_campania'),
    path('editar/<int:pk>/', views.editar_campania, name='editar_campania'), 
    path('eliminar/<int:pk>/', views.eliminar_campania, name='eliminar_campania'),

    # NUEVAS URLs de Ubicaciones
    path('ubicaciones/', views.ubicacion_list, name='ubicacion_list'),
    path('ubicaciones/crear/', views.ubicacion_create, name='ubicacion_create'),
    path('ubicaciones/editar/<int:pk>/', views.ubicacion_update, name='ubicacion_update'),
    path('ubicaciones/eliminar/<int:pk>/', views.ubicacion_delete, name='ubicacion_delete')
]
