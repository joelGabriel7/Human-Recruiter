# Generated by Django 4.1.7 on 2023-05-05 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0019_alter_attendance_observation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeturn',
            name='end_turn',
            field=models.TimeField(verbose_name='Fin del turno'),
        ),
        migrations.AlterField(
            model_name='employeeturn',
            name='start_turn',
            field=models.TimeField(verbose_name='Inicio del turno'),
        ),
    ]
