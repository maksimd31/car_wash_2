from django.core.management.base import BaseCommand
from car_wash.models import Client
from random import choice


class Command(BaseCommand):
    help = 'Случайное изменение данных клиентов в таблице Client'

    def handle(self, *args, **kwargs):
        clients = Client.objects.all()

        for client in clients:
            fields = ['full_name', 'phone_number', 'car_model']
            random_field = choice(fields)

            if random_field == 'full_name':
                client.full_name = 'Новое имя'
            elif random_field == 'phone_number':
                client.phone_number = 'Новый номер'
            elif random_field == 'car_model':
                client.car_model = 'Новая модель'

            client.save()
            self.stdout.write(self.style.SUCCESS(f'Данные клиента {client.full_name} изменены: {random_field}'))


