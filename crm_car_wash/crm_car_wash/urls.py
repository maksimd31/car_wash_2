"""
URL configuration for crm_car_wash project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('1hfhthtshsth/', include('website.urls')),
    path('', include('website2.urls')),

]

# hendler404 = 'handlers.page_not_found'
# handler400 = 'handlers.handle_bad_request'
# handler403 = 'handlers.handle_forbidden'
# handler404 = 'handlers.handle_not_found'
# handler500 = 'handlers.handle_server_error'
