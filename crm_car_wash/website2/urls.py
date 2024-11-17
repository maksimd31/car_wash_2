from . import views
from .views import add_random_client, delete_random_client, update_random_client

from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('add_client/', views.add_client, name='add_client'),
    path('client_home', views.client_home, name='client_home'),  # представление к клиентам.
    path('client/<int:client_id>/', views.customer_client, name='client'),
    path('delete_client/<int:client_id>', views.delete_client, name='delete_client'),
    path('update_client/<int:client_id>', views.update_client, name='update_client'),
    path('add_random_client/', add_random_client, name='add_random_client'),
    path('delete_random_client/', delete_random_client, name='delete_random_client'),
    path('update_random_client/', update_random_client, name='update_random_client'),
    path('weather', views.weather_view, name='weather'),
    path('delete_weather/', views.delete_weather, name='delete_weather'),
    # path('save_weather/', views.save_weather, name='save_weather'),
    path('new_order/', views.new_order, name='new_order'),
    path('search_clients/', views.search_clients, name='search_clients'),
    # path('registr_time/', views.registr_time, name='registr_time'),

]
