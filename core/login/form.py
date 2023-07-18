from django.contrib.auth.models import AbstractUser
from django import forms
from django.forms import *

from core.user.models import User


# from core.user.models import *

class ResetPasswordForm(forms.Form):
    username = CharField(widget=TextInput(attrs={
        'placeholder': 'Ingrese su Usuario',
        # 'class': 'form-control',
        'autocomplete': 'off',
        'autofocus': 'True'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            self._errors['error'] = self.errors.get('error', self.error_class([]))
            self._errors['error'].append('El usuario no exite')
            # raise forms.ValidationError('El usuario no existe')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class ChangePasswordForm(forms.Form):
    password = CharField(widget=PasswordInput(attrs={
        'placeholder': 'Ingrese su nueva contraseña',
        # 'class': 'form-control',
        'autocomplete': 'off',
        'autofocus': 'True'
    }))

    confirm_password = CharField(widget=PasswordInput(attrs={
        'placeholder': 'Repita su nueva contraseña',
        # 'class': 'form-control',
        'autocomplete': 'off',
        'autofocus': 'True'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirm_password = cleaned['confirm_password']

        if password != confirm_password:
            self._errors['error'] = self.errors.get('error', self.error_class([]))
            self._errors['error'].append('Las contraseñas no coinciden, deben ser iguales')
            # raise forms.ValidationError('El usuario no existe')
        return cleaned
