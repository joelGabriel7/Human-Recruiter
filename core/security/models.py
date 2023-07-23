from datetime import datetime

from crum import get_current_request
from django.db import models
from django.forms import model_to_dict
from core.user.models import User


# Create your models here.


class AccessUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    time_joined = models.TimeField(default=datetime.now)
    ip_address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.ip_address

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJson()
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['time_joined'] = self.time_joined.strftime('%H:%M:%p')
        return item

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        request = get_current_request()
        self.ip_address = request.META['REMOTE_ADDR']
        print(request.META['REMOTE_HOST'])
        super(AccessUser,self).save()

    class Meta:
        verbose_name = 'Acceso de Usuario'
        verbose_name_plural = 'Acceso de Usuarios'
        default_permissions = ()
        permissions = (
            ('view_user_access', 'Can view Acceso del usuario'),
            ('delete_user_access', 'Can delete Acceso del usuario'),
        )
        ordering = ['id']
