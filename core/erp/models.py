import datetime
import random

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


class Banks(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nombre')
    description = models.CharField(max_length=512, null=True, blank=True, verbose_name='descripción')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        # ordering = [id]


class AccountsBank(models.Model):
    number = models.CharField(max_length=64, default=generar_numero_cuenta)
    type = models.CharField(max_length=32)
    bank = models.ForeignKey(Banks, on_delete=models.CASCADE)

    def __str__(self):
        return f'Numero de cuenta: {self.number} Cuenta: {self.bank.name}'

    def toJSON(self):
        item = model_to_dict(self)
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
    min_salary = models.DecimalField(default=0.00, max_digits=8, decimal_places=2, null=True, blank=True,verbose_name='Mínimo salario')
    max_salary = models.DecimalField(default=0.00, max_digits=8, decimal_places=2, null=True, blank=True,verbose_name='Máximo salario')

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
    person = models.OneToOneField(Candidatos, on_delete=models.CASCADE, verbose_name='Empleado')
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, verbose_name='Departamento')
    position = models.ForeignKey(EmployeePositions, on_delete=models.CASCADE, verbose_name='Posición')
    turn = models.ForeignKey(EmployeeTurn, on_delete=models.CASCADE, verbose_name='Turno')
    salary = models.DecimalField(max_digits=8, decimal_places=2, null=False, verbose_name='Salario')
    accounts = models.ForeignKey(AccountsBank, on_delete=models.CASCADE, verbose_name='Cuenta de banco')
    address = models.CharField(max_length=64, null=True, blank=True, verbose_name='Direcciones')

    def __str__(self):
        return f'{self.person.firstname} {self.person.lastname}'

    def toJSON(self):
        item = model_to_dict(self)
        item['person'] = self.person.toJSON()
        item['department'] = self.department.toJSON()
        item['position'] = self.position.toJSON()
        item['turn'] = self.turn.toJSON()
        item['accounts'] = self.accounts.toJSON()
        return item

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        # ordering = [id]


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Empleado')
    observation = models.CharField(max_length=512, null=True, blank=True, verbose_name='Observacion')
    date = models.DateField(default=timezone.now, verbose_name='Fecha')
    attendance = models.BooleanField(default=True, verbose_name='Asistencia')

    def __str__(self):
        return f'{self.employee.person.firstname}, {self.date}'

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        # ordering = [id]
