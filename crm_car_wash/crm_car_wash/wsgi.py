"""
WSGI config for crm_car_wash project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import time

os.environ["TZ"] = "Europe/Moscow"
time.tzset()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_car_wash.settings')

application = get_wsgi_application()

