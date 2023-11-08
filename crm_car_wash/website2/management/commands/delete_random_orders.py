# filename delete_random_orders.py

from django.core.management.base import BaseCommand
from car_wash.models import Order
import random


class Command(BaseCommand):
    help = 'Удалить случайные данные из таблицы Order'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=int, help='Количество заказов для удаления')

    def handle(self, *args, **options):
        count = options['count'][0]
        orders = Order.objects.all()

        if count > len(orders):
            count = len(orders)

        randomly_selected_orders = random.sample(list(orders), count)

        for order in randomly_selected_orders:
            order.delete()

        self.stdout.write(self.style.SUCCESS(f'Успешно удалено {count} случайных заказов.'))
