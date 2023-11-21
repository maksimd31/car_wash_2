from django.urls import path
from . import views
from .views import add_random_client, delete_random_client, update_random_client,weather_forecast

urlpatterns = [
    path('', views.home, name='home'),
    # # path('create/', create_new_client, name='create_new_client'),
    # path('add_client', views.add_client, name='add_client'),
    # # path('/add_client/', views.add_client, name='add_client'),
    # path('delete', views.delete_client, name='delete_client'),
    # # path('client/<str:license_plate>/update/', views.update_client, name='update_client'),
    # path('order/create/', views.create_order, name='create_order'),
    # path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    # path('order/<int:order_id>/update/', views.update_order, name='update_order'),
    # path('order/list/', views.order_list, name='order_list'),
    # path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    # path('employee/<int:employee_id>/edit/', views.edit_employee, name='edit_employee'),

    # path('result/', result_page, name='result_page'),
    path('register/', views.register_user, name='register'),
    # Путь входа
    path('logout/', views.logout_user, name='logout'),
    # путь регистрации

    # path('record/<int:pk>', views.customer_record, name='record'),
    #
    # path('record_first_name/<str:pk>', views.customer_record_first_name, name='record_first_name'),
    #
    # path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    #
    path('add_client/', views.add_client, name='add_client'),
    #
    # path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('client_home', views.client_home, name='client_home'),  # представление к клиентам.
    path('client/<int:client_id>/', views.customer_client, name='client'),

    # path('record_first_name/<str:pk>', views.customer_record_first_name, name='record_first_name'),
    path('delete_client/<int:client_id>', views.delete_client, name='delete_client'),
    path('update_client/<int:client_id>', views.update_client, name='update_client'),

    path('add_random_client/', add_random_client, name='add_random_client'),
    path('delete_random_client/', delete_random_client, name='delete_random_client'),
    path('update_random_client/', update_random_client, name='update_random_client'),

    path('weather_forecast/', weather_forecast, name='weather_forecast'),
    path('weather/', views.weather, name='weather'),

]

