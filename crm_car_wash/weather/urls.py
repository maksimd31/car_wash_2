from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('weather_urls/', views.index, name='weather_urls'),
]