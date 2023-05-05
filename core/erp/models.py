from django.db import models
import datetime
from django.utils import timezone
from django.forms import model_to_dict


# Create your models here.

class Address(models.Model):
    country = models.CharField(max_length=64, verbose_name='País')
    municipality = models.CharField(max_length=32, verbose_name='Municipio')
    province = models.CharField(max_length=32, verbose_name='Provincia')
    street = models.CharField(max_length=64, null=True, blank=True, verbose_name='Calle')
    local_number = models.IntegerField(null=True, blank=True, verbose_name='Número de casa')
    postal_code = models.IntegerField(null=True, blank=True, verbose_name='Código postal')
    description = models.CharField(max_length=512, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return f' {self.province} {self.country} {self.municipality} {self.street}  '

    class Meta:
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'
        # ordering = [id]


class People(models.Model):
    gender_choiches = (
        (1, 'Masculino'),
        (2, 'Femenino')
    )

    cedula = models.CharField(max_length=64, null=False, unique=True)
    firstname = models.CharField(max_length=64, verbose_name='Nombre')
    lastname = models.CharField(max_length=64, verbose_name='Apellido')
    birthdate = models.DateField(default=timezone.now, verbose_name='Fecha de nacimiento')
    gender = models.CharField(max_length=10, choices=gender_choiches, default='Masculino')
    phone = models.CharField(max_length=64, null=True, blank=True, verbose_name='Teléfono')
    email = models.CharField(max_length=64, null=True, blank=True, verbose_name='Email')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'

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
    number = models.CharField(max_length=64)
    type = models.CharField(max_length=32)
    bank = models.ForeignKey(Banks, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        # ordering = [id]


class Vacants(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nombre')
    person = models.ForeignKey(People, on_delete=models.CASCADE, verbose_name='Persona')
    description = models.CharField(max_length=512, null=True, blank=True)
    min_salary = models.DecimalField(default=0.00, max_digits=8, decimal_places=2, null=True, blank=True,
                                     verbose_name='Mínimo salario')
    max_salary = models.DecimalField(default=0.00, max_digits=8, decimal_places=2, null=True, blank=True,
                                     verbose_name='Máximo salario')

    class Meta:
        verbose_name = 'Vacante'
        verbose_name_plural = 'Vacantes'
        # ordering = [id]

    def __str(self):
        return self.name


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
    person = models.OneToOneField(People, on_delete=models.CASCADE, verbose_name='Empleado')
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, verbose_name='Departamento')
    position = models.ForeignKey(EmployeePositions, on_delete=models.CASCADE, verbose_name='Posición')
    turn = models.ForeignKey(EmployeeTurn, on_delete=models.CASCADE, verbose_name='Turno')
    salary = models.DecimalField(max_digits=8, decimal_places=2, null=False, verbose_name='Salario')
    accounts = models.ForeignKey(AccountsBank, on_delete=models.CASCADE, verbose_name='Cuenta de banco')

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        # ordering = [id]

    def __str(self):
        return self.person


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Empleado')
    observation = models.CharField(max_length=512, null=True, blank=True, verbose_name='Observacion')
    date = models.DateField(default=timezone.now, verbose_name='Fecha')
    attendance = models.BooleanField(default=True, verbose_name='Asistencia')

    def __str(self):
        return self.date

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        # ordering = [id]
