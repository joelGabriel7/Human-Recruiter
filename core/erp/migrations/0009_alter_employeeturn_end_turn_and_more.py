# Generated by Django 4.1.7 on 2023-04-06 04:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0008_alter_attendance_date_alter_employeeturn_end_turn_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeturn',
            name='end_turn',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Incio del turno'),
        ),
        migrations.AlterField(
            model_name='employeeturn',
            name='start_turn',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Incio del turno'),
        ),
    ]
