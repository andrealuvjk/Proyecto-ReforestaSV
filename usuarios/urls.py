from django.urls import path
from . import views
app_name = 'usuarios'

urlpatterns = [
    # Rutas para Especies
    path('', views.usuarios_list, name='usuarios'),
    path('usuario/nuevo/', views.crear_usuario, name='crear_usuario'),
   path('editar/<int:pk>/', views.editar_usuario, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar'),
 
]