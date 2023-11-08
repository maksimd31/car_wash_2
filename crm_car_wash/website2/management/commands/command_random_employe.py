import random

from django.core.management import BaseCommand
from faker import Faker

from car_wash.models import Employee

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Генерация случайных записей
        for _ in range(10):  # Задайте нужное количество записей
            employee = Employee(
                name=fake.name(),
                position=fake.job(),
                hire_date=fake.date_between(start_date='-5y', end_date='today'),
                phone_number=fake.phone_number(),
                registration_address=fake.address(),
                residence_address=fake.address()
            )
            employee.save()

# Для создания случайных записей в таблице Employee вы можете использовать модуль faker,
# который генерирует реалистичные случайные данные.
# Вот пример команды для заполнения таблицы Employee с помощью faker:
# В этом примере мы используем модуль faker для генерации случайных данных. Мы создаем 10 записей в цикле for,
# используя методы модели Employee и методы faker для генерации случайных значений. Затем мы сохраняем каждую запись с
# помощью метода save().
# Обратите внимание, что перед использованием модуля faker вы должны установить его в
# вашей среде выполнения. Вы можете установить его с помощью pip
# Также не забудьте импортировать модуль faker и определить класс Employee в вашем коде перед выполнением этой команды.