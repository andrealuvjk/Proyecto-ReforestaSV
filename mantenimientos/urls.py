from django.urls import path

from . import views

app_name = 'mantenimientos'

urlpatterns = [
    path('', views.mantenimiento_list, name='lista'),
    path('nuevo/', views.mantenimiento_crear, name='crear'),
    path('<int:pk>/editar/', views.mantenimiento_editar, name='editar'),
    path('<int:pk>/eliminar/', views.mantenimiento_eliminar, name='eliminar'),
]