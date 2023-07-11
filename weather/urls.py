from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('weather/<str:city>',views.weather, name="weather"),
    path('city',views.city, name="city"),
]