# Generated by Django 4.1.7 on 2023-05-04 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0016_alter_employeeturn_end_turn_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeturn',
            name='end_turn',
            field=models.DateField(verbose_name='Fin del turno'),
        ),
        migrations.AlterField(
            model_name='employeeturn',
            name='start_turn',
            field=models.DateField(verbose_name='Incio del turno'),
        ),
    ]
