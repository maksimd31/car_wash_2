# Generated by Django 4.2.6 on 2023-11-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(default='', max_length=50, verbose_name='email'),
            preserve_default=False,
        ),
    ]
