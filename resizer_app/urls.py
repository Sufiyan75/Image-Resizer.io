from django.contrib import admin
from django.urls import path
from resizer_app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('singleimage/', views.singleimage, name='singleimage'),
    path('multipleimage/', views.multipleimage, name='multipleimage')
]