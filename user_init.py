from config.wsgi import *
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

def setup_admin_user():
    group_name = "admin"  # Puedes cambiar el nombre a "pruebas" si prefieres
    username = "root"
    password = "root"
    email = "root@example.com"

    
    admin_group, created = Group.objects.get_or_create(name=group_name)
    if created:
        print(f"Grupo '{group_name}' creado.")
    else:
        print(f"Grupo '{group_name}' ya existe.")

   
    permissions = Permission.objects.all()
    admin_group.permissions.set(permissions)
    admin_group.save()
    print(f"Permisos asignados al grupo '{group_name}'.")

    User = get_user_model()

 
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username, email, password)
        user.groups.add(admin_group)
        user.save()
        print(f"Usuario '{username}' creado y asignado al grupo '{group_name}'.")
    else:
        print(f"Usuario '{username}' ya existe.")

if __name__ == "__main__":
    setup_admin_user()
