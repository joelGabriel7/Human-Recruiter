from django.forms import *
from datetime import datetime
from core.erp.models import *


class DepartmentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = 'form-control'
            form.field.widget.attrs["autocomplete"] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Departments
        fields = '__all__'
        labels = {
            'name': 'Nombre',
            'description': 'Descripción'
        }
        widgets = {
            'name': TextInput(
                attrs={
                    # 'class': 'form-control',
                    'placeholder': 'Ingrese un nombre',
                    # 'autocomplete': 'off'
                }
            ),
            'description': Textarea(
                attrs={
                    # 'class': 'form-control',
                    'placeholder': 'Ingrese un nombre',
                    # 'autocomplete': 'off',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }

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


class PositionsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = 'form-control'
            form.field.widget.attrs["autocomplete"] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = EmployeePositions
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'description': Textarea(
                attrs={
                    'rows': 3,
                    'cols': 3,
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'departament': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            )
        }

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


class EmployeeTurnForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            # form.field.widget.attrs["class"] = 'form-control'
            form.field.widget.attrs["autocomplete"] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    # Forma 2
    #     self.fields['start_turn'].widget.attrs{
    #         'class': 'form-control'
    #     }

    class Meta:
        model = EmployeeTurn
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Nombre de Turno',
                    'autocomplete': 'off',
                    'class': 'form-control'
                }
            ),

            'start_turn': TimeInput(
                format='%I:%M %p',
                attrs={
                    'autocomplete': 'off',
                    'class': 'form-control input-group timepicker-input',
                    'id': 'start_turn',
                    'data-target': '#start_turn',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'end_turn': TimeInput(
                format='%I:%M %p',
                attrs={
                    'autocomplete': 'off',
                    'class': 'form-control input-group timepicker-input',
                    'id': 'end_turn',
                    'data-target': '#end_turn',
                    'data-toggle': 'datetimepicker'
                }
            )

        }



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
