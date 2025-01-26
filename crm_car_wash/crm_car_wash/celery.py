# your_project/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_car_wash.settings')

app = Celery('crm_car_wash')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
