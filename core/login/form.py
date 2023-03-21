from django.contrib.auth.models import AbstractUser
from django.forms import *


# from core.user.models import *

class UserForm(ModelForm):

    def __int__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AbstractUser
        fields = 'username', 'password'
        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Usuario',
                    'autocomplete':'off'

                }
            ),

            'password': PasswordInput(render_value=True,
                                      attrs={
                                          'placeholder': 'Contraseña',
                                          'class': 'box-input'

                                      }
                                      ),
        }
