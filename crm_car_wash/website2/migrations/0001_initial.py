# Generated by Django 4.2.6 on 2023-11-08 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(max_length=20, unique=True, verbose_name='Государственный номер')),
                ('full_name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('car_model', models.CharField(max_length=50, verbose_name='Марка и модель автомобиля')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='ФИО сотрудника')),
                ('position', models.CharField(max_length=100, verbose_name='Должность сотрудника')),
                ('employment_date', models.DateField(verbose_name='Дата устройства на работу')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Номер телефона сотрудника')),
                ('registration_address', models.CharField(max_length=150, verbose_name='Адрес регистрации')),
                ('residential_address', models.CharField(max_length=150, verbose_name='Адрес проживания')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('work_type', models.CharField(max_length=100, verbose_name='Вид работы')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
                ('employee', models.CharField(max_length=100, verbose_name='Сотрудник выполневший работу')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website2.client', verbose_name='Клиент')),
            ],
        ),
    ]
