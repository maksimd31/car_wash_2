# random_edit_employee_data
import random
from django.core.management.base import BaseCommand

from car_wash.models import Employee


class Command(BaseCommand):
    help = 'Рандомно е редактирование таблицы Employee'

    def handle(self, *args, **options):
        # Получить все записи из таблицы Employee
        employees = Employee.objects.all()

        # Перебрать каждую запись и отредактировать случайное поле
        for employee in employees:
            # Сгенерировать случайное значение
            new_value = random.choice(["John", "Jane", "Michael", "Emily"])

            # Редактировать случайное поле (например, first_name)
            employee.first_name = new_value
            employee.save()

        self.stdout.write(self.style.SUCCESS('Данные о сотрудниках успешно отредактированы'))
