# filename add_random_employee.py
from django.core.management.base import BaseCommand
from faker import Faker

from car_wash.models import Employee


class Command(BaseCommand):
    help = 'Заполнить таблицу Employee данными, сгенерированными с использованием Faker'

    def handle(self, *args, **options):
        fake = Faker()

        for _ in range(10):  # Здесь можно указать нужное количество записей
            employee = Employee(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                position=fake.job(),
                department=fake.random_element(elements=('IT', 'HR', 'Sales', 'Finance'))
            )
            employee.save()

        self.stdout.write(self.style.SUCCESS('Таблица Employee успешно заполнена'))
