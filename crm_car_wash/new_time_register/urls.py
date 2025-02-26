# from .views import add_random_client, delete_random_client, update_random_client

from django.urls import path

from . import views
# from crm_car_wash.new_time_register import views

urlpatterns = [
    path('home/', views.home_registr, name='home_registr'),
    path('register/', views.register_user, name='register_reg'),
    path('logout/', views.logout_user, name='logout'),
    # path('tim/', views.timer_view, name='tim'),
    # path('timer/', views.time_interval_view, name='time_interval'),
    path('timer/', views.time_interval_view, name='time_interval_view'),

    path('timer/<str:date>/', views.intervals_for_date, name='intervals_for_date')
    # path('time-interval/create/', views.create_time_interval, name='create_time_interval'),  # Путь для создания

]

