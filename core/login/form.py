from django.contrib.auth.models import AbstractUser
from django import forms
from django.forms import *


# from core.user.models import *

class ResetPasswordForm(forms.Form):
    username = CharField(widget=TextInput(attrs={
        'placeholder': 'Ingrese su usuario',
        'class': 'form-control',
        'autocomplete': 'off'
    }))
