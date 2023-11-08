# filename delete_random_employee.py
from django.core.management.base import BaseCommand
from random import randint

from car_wash.models import Employee


class Command(BaseCommand):
    help = 'Удаляет случайные записи о сотрудниках'

    def handle(self, *args, **options):
        total_employees = Employee.objects.count()

        if total_employees > 0:
            random_index = randint(0, total_employees - 1)
            random_employee = Employee.objects.all()[random_index]
            random_employee.delete()
            self.stdout.write(self.style.SUCCESS(f'Сотрудник успешно удален : {random_employee}'))
        else:
            self.stdout.write(self.style.NOTICE('Сотрудник не найден'))
