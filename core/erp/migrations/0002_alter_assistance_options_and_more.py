# Generated by Django 4.1.7 on 2023-07-05 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assistance',
            options={'verbose_name': 'Asistencia', 'verbose_name_plural': 'Asistencias'},
        ),
        migrations.AlterModelOptions(
            name='assistancedetail',
            options={'verbose_name': 'Detalle de Asistencia', 'verbose_name_plural': 'Detalles de Asistencia'},
        ),
        migrations.AlterModelOptions(
            name='salary',
            options={'verbose_name': 'Salario', 'verbose_name_plural': 'Salarios'},
        ),
        migrations.AlterModelOptions(
            name='salarydetail',
            options={'verbose_name': 'Salario Detalle', 'verbose_name_plural': 'Salario Detalles'},
        ),
        migrations.AlterModelOptions(
            name='salaryheadings',
            options={'verbose_name': 'Detalle de Salario', 'verbose_name_plural': 'Detalle de Salarios'},
        ),
    ]