# delete_random_clients.py

from django.core.management.base import BaseCommand
from random import randint
from car_wash.models import Client


class Command(BaseCommand):
    help = 'Удаление случайных клиентов из таблицы Client'

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, default=1, help='Количество клиентов для удаления (по умолчанию 1)')

    def handle(self, *args, **options):
        quantity = options['quantity']

        for _ in range(quantity):
            total_clients = Client.objects.count()
            if total_clients > 0:
                random_index = randint(0, total_clients - 1)
                random_client = Client.objects.all()[random_index]
                random_client.delete()
                self.stdout.write(self.style.SUCCESS(f'Клиент {random_client.full_name} успешно удален.'))
            else:
                self.stdout.write(self.style.WARNING('В таблице Client нет клиентов для удаления.'))
