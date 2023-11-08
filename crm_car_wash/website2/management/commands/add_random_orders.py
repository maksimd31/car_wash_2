# filename add_random_orders.py

from django.core.management.base import BaseCommand
from car_wash.models import Order, Client
import random


class Command(BaseCommand):
    help = 'Добавить случайные данные в таблицу Order'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=int, help='Количество заказов для добавления')

    def handle(self, *args, **options):
        count = options['count'][0]
        clients = Client.objects.all()
        work_types = ['Ремонт', 'Обслуживание', 'Замена детали']
        employees = ['Иванов', 'Петров', 'Сидоров']

        for _ in range(count):
            client = random.choice(clients)
            work_type = random.choice(work_types)
            cost = random.randint(1000, 10000)
            employee = random.choice(employees)

            order = Order(client=client, work_type=work_type, cost=cost, employee=employee)
            order.save()

        self.stdout.write(self.style.SUCCESS(f'Успешно добавлено {count} случайных заказов.'))
