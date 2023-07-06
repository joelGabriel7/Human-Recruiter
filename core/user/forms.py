from django.forms import *
from datetime import datetime
from core.user.models import *


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields['image'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'image', 'groups'
        labels = {
            'groups': 'Perfil de usuario'
        }
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombre',
                    'class': 'form-control',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellido',
                    'class': 'form-control',

                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese su Email',
                    'class': 'form-control',

                }
            ),

            'username': TextInput(
                attrs={
                    'placeholder': 'Crea un Nombre de Usuario',
                    'class': 'form-control',
                }
            ),

            'password': PasswordInput(render_value=True,
                                      attrs={
                                          'placeholder': 'Crea una Contraseña',
                                          'class': 'form-control',
                                      }
                                      ),
            'groups': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                "multiple": "multiple",

            }),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                password_cleaned = self.cleaned_data['password']
                user_created=form.save(commit=False)
                if user_created.pk is None:
                    user_created.set_password(password_cleaned)
                else:
                    user = User.objects.get(pk=user_created.pk)
                    if user.password != password_cleaned:
                        user_created.set_password(password_cleaned)
                user_created.save()
                user_created.groups.clear()
                for group in self.cleaned_data['groups']:
                    user_created.groups.add(group)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields['image'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'image'
        labels = {
            'groups': 'Perfil de usuario'
        }
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombre',
                    'class': 'form-control',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellido',
                    'class': 'form-control',

                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese su Email',
                    'class': 'form-control',

                }
            ),

            'username': TextInput(
                attrs={
                    'placeholder': 'Crea un Nombre de Usuario',
                    'class': 'form-control',
                }
            ),

            'password': PasswordInput(render_value=True,
                                      attrs={
                                          'placeholder': 'Crea una Contraseña',
                                          'class': 'form-control',
                                      }
                                      ),

        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff','groups']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                password_cleaned = self.cleaned_data['password']
                user_created=form.save(commit=False)
                if user_created.pk is None:
                    user_created.set_password(password_cleaned)
                else:
                    user = User.objects.get(pk=user_created.pk)
                    if user.password != password_cleaned:
                        user_created.set_password(password_cleaned)
                user_created.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data