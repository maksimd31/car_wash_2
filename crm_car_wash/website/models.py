from django.db import models

# Create your models here.
from django.db import models


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")


class Client(models.Model):
    """
    class client BD client сущность клиенты
    """
    license_plate = models.CharField(max_length=20, unique=True, verbose_name='Государственный номер')
    # full_name = models.CharField(max_length=100, verbose_name='ФИО')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    car_model = models.CharField(max_length=50, verbose_name='Марка и модель автомобиля')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')

    def __str__(self):
        return f'{self.license_plate} {self.last_name} {self.first_name} {self.phone_number} {self.car_model} ' \
               f'{self.created_at}'

    def __repr__(self):
        return f'{self.pk} {self.license_plate} {self.last_name} {self.first_name} {self.phone_number} ' \
               f'{self.car_model} {self.created_at}'
