from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventario_list, name='inventario_list'),
    path('crear/', views.inventario_create, name='inventario_create'),
    path('editar/<int:pk>/', views.inventario_update, name='inventario_update'),
    path('eliminar/<int:pk>/', views.inventario_delete, name='inventario_delete'),
]