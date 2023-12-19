# filename add_random_client
import random

from faker import Faker
from django.core.management.base import BaseCommand

from website2.models import Client


class Command(BaseCommand):
    """Команда для заполнения таблицы Client случайными данными."""

    help = 'Заполнить таблицу Client данными'

    def handle(self, *args, **options):
        """Обработка команды."""
        fake = Faker()
        for _ in range(1):
            client = Client(
                license_plate=fake.license_plate(),
                full_name=fake.name(),
                phone_number=fake.phone_number(),
                email=fake.email(),
                car_model=fake.word(),
            )
            client.save()

        self.stdout.write(self.style.SUCCESS('Успешно заполнена таблица клиенты со случайными данными'))
