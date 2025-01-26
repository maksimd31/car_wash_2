# your_project/__init__.py
from crm_car_wash.celery import app as celery_app

__all__ = ('celery_app',)
