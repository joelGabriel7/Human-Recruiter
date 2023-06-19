# Generated by Django 4.1.7 on 2023-06-17 21:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0002_alter_employee_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assistance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de asistencia')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(choices=[('', '-----------'), (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')], default=0)),
                ('day', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Asistencia',
                'verbose_name_plural': 'Asistencias',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='AssistanceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('state', models.BooleanField(default=False)),
                ('assistance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.assistance')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.employee', verbose_name='Empleado')),
            ],
            options={
                'verbose_name': 'Detalle de Asistencia',
                'verbose_name_plural': 'Detalles de Asistencia',
                'default_permissions': (),
            },
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]