from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('agregar/', views.agregar, name='agregar'),
    path('insertar/',views.insertar, name='insertar'),
    path('recuperar/', views.recuperar, name='recuperar'),
    path('cambiar_password/', views.cambiar_pass, name='cambiar_password'),
    
]