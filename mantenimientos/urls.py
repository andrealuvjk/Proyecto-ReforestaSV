from django.urls import path

from . import views

app_name = 'mantenimientos'

urlpatterns = [
    path('', views.mantenimiento_list, name='lista'),
    path('nuevo/', views.mantenimiento_crear, name='crear'),
    path('<int:pk>/editar/', views.mantenimiento_editar, name='editar'),
    path('<int:pk>/eliminar/', views.mantenimiento_eliminar, name='eliminar'),
    path('arboles/', views.arboles_lista, name='arboles_lista'),
    path('arboles/nuevo/', views.arbol_crear, name='arbol_crear'),
    path('arboles/<int:id>/editar/', views.arbol_editar, name='arbol_editar'),
    path('arboles/<int:id>/eliminar/', views.arbol_eliminar, name='arbol_eliminar'),
]