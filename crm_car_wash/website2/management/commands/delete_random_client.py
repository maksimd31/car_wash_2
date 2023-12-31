# delete_random_clients.py

from django.core.management.base import BaseCommand
from random import randint
from website2.models import Client


class Command(BaseCommand):
    """Команда для удаления случайных клиентов из таблицы Client."""

    help = 'Удаление случайных клиентов из таблицы Client'

    def handle(self, *args, **options):
        """Обработчик команды."""

        quantity = options.get('quantity', 1)

        for _ in range(quantity):
            total_clients = Client.objects.count()
            if total_clients > 0:
                random_index = randint(0, total_clients - 1)
                random_client = Client.objects.all()[random_index]
                random_client.delete()
                self.stdout.write(self.style.SUCCESS(f'Клиент {random_client.full_name} успешно удален.'))
            else:
                self.stdout.write(self.style.WARNING('В таблице Client нет клиентов для удаления.'))
