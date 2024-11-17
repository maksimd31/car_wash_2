# from .views import add_random_client, delete_random_client, update_random_client

from django.urls import path

from crm_car_wash.new_time_register import views

# from crm_car_wash.new_time_register import views

urlpatterns = [
    path('home/', views.home_registr, name='home_registr'),
    path('register/', views.register_user, name='register_reg'),
    path('logout/', views.logout_user, name='logout'),
]
