# Generated by Django 4.2.6 on 2023-11-08 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website2', '0002_client_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(max_length=50, verbose_name='Номер телефона'),
        ),
    ]
