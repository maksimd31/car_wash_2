import random

from django.core.management import BaseCommand
from faker import Faker

from web_car_wash_crm.models import Employee

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
