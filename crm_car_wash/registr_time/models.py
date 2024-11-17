


from django.db import models
from django.utils import timezone

class Time(models.Model):
    """
    Класс для хранения информации о клиентах и времени.
    """

    start_date = models.DateTimeField(verbose_name='Дата начала', default=timezone.now)
    end_date = models.DateTimeField(verbose_name='Дата конца', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')

    def duration(self):
        """Возвращает разницу между началом и концом в виде timedelta."""
        if self.end_date:
            return self.end_date - self.start_date
        return None

    def __str__(self):
        return f'{self.license_plate} {self.full_name} {self.phone_number} {self.car_model} ' \
               f'{self.created_at}'

    def __repr__(self):
        return f'{self.pk} {self.license_plate} {self.full_name} {self.phone_number} {self.car_model} ' \
               f'{self.created_at}'
