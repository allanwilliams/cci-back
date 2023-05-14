from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('buscar-imovel', views.buscar_imovel, name = 'buscar_imovel'),
]