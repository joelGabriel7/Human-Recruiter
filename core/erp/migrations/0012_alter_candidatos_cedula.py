# Generated by Django 4.2.7 on 2023-11-04 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0011_vacations_reminder_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatos',
            name='cedula',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]