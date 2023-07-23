# Generated by Django 4.1.7 on 2023-07-21 16:50

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('time_joined', models.TimeField(default=datetime.datetime.now)),
                ('ip_address', models.CharField(blank=True, max_length=100, null=True)),
                ('http_user_agent', models.CharField(blank=True, max_length=150, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Acceso de Usuario',
                'verbose_name_plural': 'Acceso de Usuarios',
                'permissions': (('view_user_access', 'Can view Acceso del usuario'), ('delete_user_access', 'Can delete Acceso del usuario')),
                'default_permissions': (),
            },
        ),
    ]
