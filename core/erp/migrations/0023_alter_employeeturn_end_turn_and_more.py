# Generated by Django 4.1.7 on 2023-05-05 19:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0022_alter_employeeturn_end_turn_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeturn',
            name='end_turn',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name='Fin del turno'),
        ),
        migrations.AlterField(
            model_name='employeeturn',
            name='start_turn',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name='Inicio del turno'),
        ),
    ]