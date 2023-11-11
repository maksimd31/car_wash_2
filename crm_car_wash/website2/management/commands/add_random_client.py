# filename add_random_client
import random

from faker import Faker
from django.core.management.base import BaseCommand

from website2.models import Client




class Command(BaseCommand):
    help = 'Заполнить таблицу Client данными'

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(1):  # Добавим 10 рандомных записей
            client = Client(
                license_plate=fake.license_plate(),  # Государственный номер
                full_name=fake.name(),  # ФИО
                phone_number=fake.phone_number(),  # Номер телефона
                email=fake.email(),  # Email
                car_model=fake.word(),  # Марка и модель автомобиля
            )
            client.save()

        self.stdout.write(self.style.SUCCESS('Успешно заполнена таблица клиенты со случайными данными'))