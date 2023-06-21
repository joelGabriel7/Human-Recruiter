import datetime
import random
import string
from core.erp.choice import *
from django.db import models
from django.forms import model_to_dict
from django.utils import timezone


# from core.test import generar_numero_cuenta
def generar_numero_cuenta():
    prefijo = "960"
    sufijo = "".join([str(random.randint(0, 8)) for i in range(6)])
    digito_verificador = str(random.randint(0, 8))
    numero_cuenta = prefijo + sufijo + digito_verificador
    return numero_cuenta


def generate_employee_code():
    letters = string.ascii_uppercase
    numbers = string.digits
    code = ''.join(random.choice(letters) for i in range(6)) + ''.join(random.choice(numbers) for i in range(3))
    return code


# #
# #
employe_code = generate_employee_code()


# Create your models here.
class Candidatos(models.Model):
    gender_choiches = (
        ('Male', 'Masculino'),
        ('Female', 'Femenino')
    )

    cedula = models.CharField(max_length=64, null=False, unique=True)
    firstname = models.CharField(max_length=64, verbose_name='Nombre')
    lastname = models.CharField(max_length=64, verbose_name='Apellido')
    birthdate = models.DateField(verbose_name='Fecha de nacimiento')
    gender = models.CharField(max_length=10, choices=gender_choiches, default='male')
    phone = models.CharField(max_length=64, null=True, blank=True, verbose_name='Teléfono')
    email = models.CharField(max_length=64, null=True, blank=True, verbose_name='Email')
    address = models.CharField(max_length=64, null=True, blank=True, verbose_name='Direcciones')

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['fullname'] = self.firstname + ' ' + self.lastname
        return item

    class Meta:
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'
        # ordering = [id]


# self.min_salary, '.2f'

class AccountsBank(models.Model):
    choices = (
        ('Banreservas', 'Banreservas'),
        ('Banco Popular', 'Banco Popular'),
        ('BHD León', 'BHD León'),
        ('Scotiabank', 'Scotiabank'),
    )

    number = models.CharField(max_length=64, default=generar_numero_cuenta, verbose_name='Numeros de cuenta')
    type = models.CharField(max_length=32, verbose_name='Tipo de cuenta')
    bank = models.CharField(max_length=32, choices=choices, null=False, default='Banreservas', verbose_name='Banco')

    def __str__(self):
        return f'Tipo de cuenta: {self.type}'

    def toJSON(self):
        item = model_to_dict(self)
        item['bank'] = {'id': self.bank, 'name': self.bank}
        return item

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        # ordering = [id]


class Departments(models.Model):
    name = models.CharField(max_length=32, unique=True, )
    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        # ordering = [id]


class EmployeePositions(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nombre')
    description = models.CharField(max_length=512, null=True, blank=True, verbose_name='Descripcion')
    departament = models.ForeignKey(Departments, on_delete=models.CASCADE, verbose_name='Departamentos')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Posición'
        verbose_name_plural = 'Posiciones'
        # ordering = [id]

    def toJSON(self):
        item = model_to_dict(self)
        item['departament'] = self.departament.toJSON()
        return item


class Vacants(models.Model):
    posicion = models.ForeignKey(EmployeePositions, on_delete=models.CASCADE, verbose_name='Posiciones')
    description = models.CharField(max_length=512, null=True, blank=True)
    min_salary = models.DecimalField(default=0.00, max_digits=8, decimal_places=2, null=True, blank=True,
                                     verbose_name='Mínimo salario')
    max_salary = models.DecimalField(default=0.00, max_digits=8, decimal_places=2, null=True, blank=True,
                                     verbose_name='Máximo salario')

    def __str__(self):
        return self.posicion.name

    def toJSON(self):
        item = model_to_dict(self)
        item['posicion'] = self.posicion.toJSON()
        item['min_salary'] = format(self.min_salary, '.2f')
        item['max_salary'] = format(self.max_salary, '.2f')
        return item

    class Meta:
        verbose_name = 'Vacante'
        verbose_name_plural = 'Vacantes'
        # ordering = [id]


class Selection(models.Model):
    person = models.ForeignKey(Candidatos, on_delete=models.CASCADE, verbose_name='Candidatos')
    vacants = models.ForeignKey(Vacants, on_delete=models.CASCADE, verbose_name='Vacantes')

    def __str__(self):
        return self.person.firstname

    def toJSON(self):
        item = model_to_dict(self)
        item['person'] = self.person.toJSON()
        item['vacants'] = self.vacants.toJSON()
        return item

    class Meta:
        verbose_name = 'Seleccion'
        verbose_name_plural = 'Selecciones'
        # ordering = [id]


class EmployeeTurn(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nombre')
    start_turn = models.TimeField(verbose_name='Inicio del turno', default=datetime.time(0, 0))
    end_turn = models.TimeField(verbose_name='Fin del turno', default=datetime.time(0, 0))

    def __str__(self):
        return f'{self.name}'

    def toJSON(self):
        item = model_to_dict(self)
        if item['start_turn'] is not None:
            item['start_turn'] = item['start_turn'].strftime('%I:%M %p')
        else:
            item['start_turn'] = ''

        if item['end_turn'] is not None:
            item['end_turn'] = item['end_turn'].strftime('%I:%M %p')
        else:
            item['end_turn'] = ''

        return item

        # item['end_turn'] = item['end_turn'].strftime('%H:%M:%S')

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        # ordering = [id]

    #


class Employee(models.Model):
    estado_choiches = (
        ('Contratado', 'Contratado'),
        ('Despedido', 'Despedido')
    )

    codigo = models.CharField(max_length=64, default=generate_employee_code, verbose_name='Codigo Empleado')
    person = models.ForeignKey(Candidatos, on_delete=models.CASCADE, verbose_name='Empleado')
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, verbose_name='Departamento')
    position = models.ForeignKey(EmployeePositions, on_delete=models.CASCADE, verbose_name='Posición')
    turn = models.ForeignKey(EmployeeTurn, on_delete=models.CASCADE, verbose_name='Turno')
    salary = models.DecimalField(max_digits=8, default=0.00, decimal_places=2, null=False, verbose_name='Salario')
    accounts = models.ForeignKey(AccountsBank, on_delete=models.CASCADE, verbose_name='Cuenta de banco')
    estado = models.CharField(max_length=64, null=True, blank=True, choices=estado_choiches, verbose_name='Estado')
    hiring_date = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name='Fecha de contratación')

    def __str__(self):
        return f'{self.person.firstname} {self.person.lastname}'

    def get_full_name(self):
        return f'{self.person.firstname} {self.person.lastname}'

    def hiring_date_format(self):
        return self.hiring_date.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['person'] = self.person.toJSON()
        item['estado'] = {'id': self.estado, 'name': self.estado}
        item['fullname'] = self.person.firstname + ' ' + self.person.lastname
        item['department'] = self.department.toJSON()
        item['position'] = self.position.toJSON()
        item['hiring_date'] = self.hiring_date.strftime('%Y-%m-%d')
        item['turn'] = self.turn.toJSON()
        item['accounts'] = self.accounts.toJSON()
        return item

    # self.firstname + ' ' + self.lastname
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        # ordering = [id]


class Headings(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    code = models.CharField(max_length=30, unique=True, verbose_name='Referencia')
    type = models.CharField(max_length=15, choices=TYPE_HEADINGS, default='Remuneraciones', verbose_name='Tipo')
    state = models.BooleanField(default=True, verbose_name='Estado')
    order = models.IntegerField(default=0, verbose_name='Posición')
    has_quantity = models.BooleanField(default=False, verbose_name='¿Posee cantidad?')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        return item

    def get_number(self):
        return f'{self.id:04d}'

    def get_amount_detail_salary(self, employee, year, month):
        queryset = self.salaryheadings_set.filter(salary_detail__employee_id=employee, salary_detail__salary__year=year,
                                                  salary_detail__salary__month=month)
        if queryset.exists():
            return queryset[0]
        return None

    def convert_name_to_code(self):
        excludes = [' ', '.', '%']
        code = self.name.lower()
        for i in excludes:
            code = code.replace(i, '_')
        if code[-1] == '_':
            code = code[0:-1]
        return code

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.code = self.convert_name_to_code()
        super(Headings, self).save()

    class Meta:
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'


class Salary(models.Model):
    payment_date = models.DateField(default=timezone.now, verbose_name='Fecha de pago')
    year = models.IntegerField(verbose_name='Año')
    month = models.IntegerField(choices=MONTHS, default=0, verbose_name='Mes')

    def __str__(self):
        return self.payment_date.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['payment_date'] = self.payment_date.strftime('%Y-%m-%d')
        item['month'] = {'id': self.month, 'name': self.get_month_display()}
        return item

    class Meta:
        verbose_name = 'Salario'
        verbose_name_plural = 'Salarios'
        default_permissions = ()
        # permissions = (
        #     ('view_salary', 'Can view Salario | Admin'),
        #     ('add_salary', 'Can add Salario | Admin'),
        #     ('change_salary', 'Can change Salario | Admin'),
        #     ('delete_salary', 'Can delete Salario | Admin'),
        #     ('view_employee_salary', 'Can view Salario | Empleado'),
        # )


class SalaryDetail(models.Model):
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    income = models.FloatField(default=0.00)
    expenses = models.FloatField(default=0.00)
    total_amount = models.FloatField(default=0.00)

    def __str__(self):
        return self.employee.get_full_name()

    def get_income(self):
        return self.salaryheadings_set.filter(headings__type='remuneracion', valor__gt=0).order_by('headings__order')

    def get_expenses(self):
        return self.salaryheadings_set.filter(headings__type='descuentos', valor__gt=0).order_by('headings__order')

    def format_decimal(self, valor):
        return '{:,}'.format(round(valor)).replace(',', '.')

    def get_income_format(self):
        return self.format_decimal(self.income)

    def get_expenses_format(self):
        return self.format_decimal(self.expenses)

    def get_total_amount_format(self):
        return self.format_decimal(self.total_amount)

    def toJSON(self):
        item = model_to_dict(self)
        item['salary'] = self.salary.toJSON()
        item['employee'] = self.employee.toJSON()
        item['income'] = self.get_income_format()
        item['expenses'] = self.get_expenses_format()
        item['total_amount'] = self.get_total_amount_format()
        return item

    class Meta:
        verbose_name = 'Salario Detalle'
        verbose_name_plural = 'Salario Detalles'
        default_permissions = ()


class SalaryHeadings(models.Model):
    salary_detail = models.ForeignKey(SalaryDetail, on_delete=models.CASCADE)
    headings = models.ForeignKey(Headings, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    valor = models.FloatField(default=0.00)

    def __str__(self):
        return self.salary_detail.employee.get_full_name()

    def get_cant(self):
        if self.headings.has_quantity:
            return self.cant
        return ' '

    def format_decimal(self, valor):
        return '{:,}'.format(round(valor)).replace(',', '.')

    def get_valor_format(self):
        return self.format_decimal(self.valor)

    def toJSON(self):
        item = model_to_dict(self, exclude=['salary'])
        item['valor'] = self.get_valor_format()
        return item

    class Meta:
        verbose_name = 'Detalle de Salario'
        verbose_name_plural = 'Detalle de Salarios'
        default_permissions = ()


class Assistance(models.Model):
    date_joined = models.DateField(default=datetime.datetime.now, verbose_name='Fecha de asistencia')
    year = models.IntegerField()
    month = models.IntegerField(choices=MONTHS, default=0)
    day = models.IntegerField()

    def __str__(self):
        return self.get_month_display()

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self, exclude=['history'])
        item['date_joined'] = self.date_joined_format()
        item['month'] = {'id': self.month, 'name': self.get_month_display()}
        return item

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        default_permissions = ()
        # permissions = (
        #     ('view_assistance', 'Can view Asistencia | Admin'),
        #     ('add_assistance', 'Can add Asistencia | Admin'),
        #     ('change_assistance', 'Can change Asistencia | Admin'),
        #     ('delete_assistance', 'Can delete Asistencia | Admin'),
        #     ('view_employee_assistance', 'Can view Asistencia | Empleado'),
        # )


class AssistanceDetail(models.Model):
    assistance = models.ForeignKey(Assistance, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    description = models.CharField(max_length=500, null=True, blank=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.employee.get_full_name()

    def toJSON(self):
        item = model_to_dict(self)
        item['assistance'] = self.assistance.toJSON()
        item['employee'] = self.employee.toJSON()
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.description is None:
            self.description = 's/n'
        elif len(self.description) == 0:
            self.description = 's/n'
        super(AssistanceDetail, self).save()

    class Meta:
        verbose_name = 'Detalle de Asistencia'
        verbose_name_plural = 'Detalles de Asistencia'
        default_permissions = ()
