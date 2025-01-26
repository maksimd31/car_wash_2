# your_app/tasks.py
from celery import shared_task
from .models import TimeInterval
from django.utils import timezone


@shared_task
def reset_intervals():
    # Получаем текущую дату
    today = timezone.now().date()

    # Удаляем все интервалы для всех пользователей
    TimeInterval.objects.filter(start_time__date=today).delete()

    return f'Интервалы за {today} обнулены.'
