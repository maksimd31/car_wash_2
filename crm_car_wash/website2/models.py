from datetime import timezone

from django.db import models

# Create your models here.
# filename model.py
from django.db import models


class Client(models.Model):
    """
    class client BD client сущность клиенты
    """
    license_plate = models.CharField(max_length=20, unique=True, verbose_name='Государственный номер')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    phone_number = models.CharField(max_length=50, verbose_name='Номер телефона')
    email = models.EmailField(max_length=50, verbose_name='email')
    car_model = models.CharField(max_length=50, verbose_name='Марка и модель автомобиля')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')

    def __str__(self):
        return f'{self.license_plate} {self.full_name} {self.phone_number} {self.car_model} ' \
               f'{self.created_at}'

    def __repr__(self):
        return f'{self.pk} {self.license_plate} {self.full_name} {self.phone_number} {self.car_model} ' \
               f'{self.created_at}'


class Order(models.Model):
    """
    class order DB order сущность заказы
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    # created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', default=timezone.now)
    work_type = models.CharField(max_length=100, verbose_name='Вид работы')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    employee = models.CharField(max_length=100, verbose_name='Сотрудник выполневший работу')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        """
        return f"Заказ #{self.pk} это id который инкриминируется с каждым новым заказом
        """
        return f"Заказ #{self.pk} - {self.client.full_name}"

    def __repr__(self):
        return f'{self.pk} {self.client} {self.created_at} {self.work_type} {self.cost} ' \
               f'{self.employee} {self.comment}'


class Employee(models.Model):
    """
    class Employee DB Employee сущность сотрудники
    """
    full_name = models.CharField(max_length=100, verbose_name='ФИО сотрудника')
    position = models.CharField(max_length=100, verbose_name='Должность сотрудника')
    employment_date = models.DateField(verbose_name='Дата устройства на работу')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона сотрудника')
    registration_address = models.CharField(max_length=150, verbose_name='Адрес регистрации')
    residential_address = models.CharField(max_length=150, verbose_name='Адрес проживания')

    def __str__(self):
        return f'{self.full_name} {self.position} {self.employment_date} {self.phone_number}' \
               f'{self.registration_address} {self.residential_address}'

    def __repr__(self):
        return f'{self.pk} {self.full_name} {self.position} {self.employment_date} {self.phone_number}' \
               f'{self.registration_address} {self.residential_address}'
