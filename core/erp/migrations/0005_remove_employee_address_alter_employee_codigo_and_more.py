# Generated by Django 4.1.7 on 2023-05-27 23:32

import core.erp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0004_employee_estado_alter_employee_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='address',
        ),
        migrations.AlterField(
            model_name='employee',
            name='codigo',
            field=models.CharField(default=core.erp.models.generate_employee_code, max_length=64, verbose_name='Codigo Empleado'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Salario'),
        ),
    ]