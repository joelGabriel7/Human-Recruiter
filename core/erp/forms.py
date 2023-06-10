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
        self.fields['departament'].widget.attrs['class'] = 'form-control select2'

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
                    'class': 'form-control select2',
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


class CandidateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = 'form-control '
            form.field.widget.attrs["autocomplete"] = 'off'
        self.fields['firstname'].widget.attrs['autofocus'] = True

    class Meta:
        model = Candidatos
        fields = '__all__'
        # labels = {
        #     'firstname': '',
        #     'cedula': '',
        #     'lastname': '',
        #     'birthdate': '',
        #     'gender': '',
        #     'phone': '',
        #     'email': '',
        #     'address': '',
        #
        # }
        widgets = {
            'firstname': TextInput(
                attrs={
                    'placeholder': 'Escriba su nombre',
                }
            ),

            'cedula': TextInput(
                attrs={
                    'placeholder': 'Escriba su cedula'
                }
            ),
            'lastname': TextInput(
                attrs={
                    'placeholder': 'Escriba su apellido',
                }
            ),
            'birthdate': DateInput(
                format='%Y-%m-%d',
                attrs={
                    # 'class': 'form-control',
                    # 'value': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': ' input-group timepicker-input',
                    'id': 'birthdate',
                    'data-target': '#birthdate',
                    'data-toggle': 'datetimepicker'

                }
            ),
            'gender': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'phone': TextInput(
                attrs={
                    'placeholder': 'Escriba su número telefonico'
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Escriba su email'
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Escriba su direccion'
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


class VacantsForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = 'form-control '
            form.field.widget.attrs["autocomplete"] = 'off'
        self.fields['posicion'].widget.attrs['class'] = 'form-control select2'

    class Meta:
        model = Vacants
        fields = '__all__'
        widgets = {

            'description': Textarea(
                attrs={
                    'placeholder': 'Informe de la vacante',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'min_salary': NumberInput(
                attrs={
                    'default': 0.00
                }
            ),
            'max_salary': NumberInput(
                attrs={
                    'default': 0.00
                }
            ),
            'posicion': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
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
            data['data'] = str(e)
        return data


class SelectionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['person'].widget.attrs['class'] = 'form-control select2'
        self.fields['vacants'].widget.attrs['class'] = 'form-control select2'

    class Meta:
        model = Selection
        fields = '__all__'
        widgets = {
            'person': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),
            'vacants': Select(
                attrs={
                    'class': 'form-control select2',
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
            data['data'] = str(e)
        return data


class AccountsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = 'form-control'
            form.field.widget.attrs["autocomplete"] = 'off'
        self.fields['type'].widget.attrs['autofocus'] = True

    class Meta:
        model = AccountsBank
        fields = '__all__'
        widgets = {
            'number': TextInput(
                attrs={
                    # 'class': 'form-control',
                    'placeholder': 'Ingrese un nombre',
                    # 'autocomplete': 'off'
                }
            ),
            'type': TextInput(
                attrs={
                    # 'class': 'form-control',
                    'placeholder': 'Ingrese el tipo de cuenta',
                    # 'autocomplete': 'off',
                }
            ),
            'bank': Select(
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


class EmployeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['person'].widget.attrs['class'] = ' form-control select2 '
        self.fields['person'].widget.attrs['style'] = 'width: 100%'
        # self.fields['person'].widget.attrs['autofocus'] = True

    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'codigo': TextInput(
                attrs={
                    'class': 'form-control ',
                    'placeholder': 'Ingrese el codigo empleado'
                }
            ),
            'person': Select(
                attrs={
                    'class': 'form-control  select2',
                    'style': 'width: 100%'
                }
            ),

            'position': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),
            'department': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),
            'turn': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),

            'accounts': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),
            'estado': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),
            'salary': NumberInput(
                attrs={
                    'class': 'form-control'
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


class AttendanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'employee': Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date',
                'value': datetime.datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date',

            }),
        }

    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Buscar por rango de fechas')
