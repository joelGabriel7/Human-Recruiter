# Generated by Django 4.1.7 on 2023-05-04 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0012_employeepositions_departament'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeepositions',
            name='departament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.departments', verbose_name='Departamentos'),
        ),
    ]