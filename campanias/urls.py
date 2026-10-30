from django.urls import path
from . import views

app_name = 'campanias'

urlpatterns = [
    # Mantiene tu vista actual prueba_herencia para cargar el listado
    path('listado/', views.prueba_herencia, name='listado_campanias'),
    path('crear/', views.crear_campania, name='crear_campania'),
    path('eliminar/<int:pk>/', views.eliminar_campania, name='eliminar_campania'),
]
