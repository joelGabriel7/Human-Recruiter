from django.forms import *
from datetime import datetime
from core.user.models import *


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            # form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'image', 'groups'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un nombre',
                    'autocomplete': 'off'
                }
            ),
             'last_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un apellido',
                    'autocomplete': 'off'
                }
            ),
              'email': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un email',
                    'autocomplete': 'off'
                }
            ),

             'username': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un username',
                    'autocomplete': 'off'
                }
            ),
            'password': PasswordInput( render_value=True,
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un password',
                    'autocomplete': 'off'
                }
            ),
            # 'image': FileInput(
            #     attrs={
            #         'class': 'form-control',
               
            #     }
            # ),
           
           
        }
        exclude = ['date_joined','is_active', 'is_staff','is_superuser' ,'user_permissions', 'groups', 'last_login']
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
