# Generated by Django 4.1.7 on 2023-07-25 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0002_remove_accessuser_http_user_agent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accessuser',
            options={'default_permissions': (), 'ordering': ['id'], 'permissions': (('view_user_access', 'Can view Acceso del usuario'), ('delete_user_access', 'Can delete Acceso del usuario')), 'verbose_name': 'Acceso de Usuario', 'verbose_name_plural': 'Acceso de Usuarios'},
        ),
    ]