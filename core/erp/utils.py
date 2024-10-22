from config.wsgi import *
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from datetime import time
from datetime import date
from django.utils.crypto import get_random_string
from core.erp.models import *
from core.user.models import User
from faker import Faker


group = Group.objects.create(name='Administrador')
group.permissions.set(Permission.objects.all())
group.save()



# Agregar datos en el modelo Candidatos
def crear_candidatos(num_registros):
    fake = Faker()
    gender_choices = ['Male', 'Female']

    for _ in range(num_registros):
        cedula_numero = fake.unique.random_number(digits=12)
        cedula_str = str(cedula_numero)
        cedula_con_formato = f"{cedula_str[:3]}-{cedula_str[3:11]}-{cedula_str[11:12]}"

        candidato = Candidatos(
            cedula=cedula_con_formato,
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            birthdate=fake.date_of_birth(minimum_age=18, maximum_age=80),
            gender=fake.random_element(elements=gender_choices),
            phone=fake.phone_number(),
            email=fake.email(),
            address=fake.address(),
        )
        candidato.save()


if __name__ == "__main__":
    num_registros = 20
    crear_candidatos(num_registros)
    print(f"Se han creado {num_registros} registros en el modelo Candidatos.")

# Agregar datos en el modelo Departments

turn_data = [
    {'name': 'Matutino', 'start_time': time(7, 0), 'end_time': time(12, 0)},
    {'name': 'Vespertino', 'start_time': time(14, 0), 'end_time': time(18, 0)},
    {'name': '12H', 'start_time': time(7, 0), 'end_time': time(19, 0)},
    {'name': '24H', 'start_time': time(0, 0), 'end_time': time(0, 0)},
]

for turn_info in turn_data:
    EmployeeTurn.objects.create(
        name=turn_info['name'],
        start_turn=turn_info['start_time'],
        end_turn=turn_info['end_time']
    )

departments_data = [
    'GERENCIA INDUSTRIAL', 'EMBARQUE', 'DESPOSTADA', 'PCP', 'GRASERIA', 'CONTROL DE STOCK',
    'CONTABILIDAD', 'AUDITORIA', 'SALA DE MAQUINAS', 'AREA TECNICA', 'CONTROL DE CALIDAD', 'ASUNCION',
    'APARTADOS', 'LAVADERO', 'IVO', 'TRIPERIA', 'ELECTRICA', 'LIMPIEZA INDUSTRIAL', 'EMPAQUE SECUNDARIO', 'FAENA',
    'FORMACIÓN PROFESIONAL FAENA', 'LAVANDERIA', 'SALA DE CUARTEO', 'CORRAL', 'SALA DE CUERO', 'MENUDENCIAS',
    'MONDONGUERIA', 'COMEDOR', 'BIENESTAR ANIMAL', 'FORMACIÓN PROFESIONAL DESPOSTADA', 'CALDERA',
    'EMPAQUE PRIMARIO', 'PTE', 'Aux  Producion', 'Limpiador', 'PATIO', 'INFORMATICA', 'COMPRAS', 'PTA',
    'MECANICO', 'CIVIL',
    'RECURSOS HUMANOS - 52', 'GERENCIA INDUSTRIAL - 20', 'DESPOSTADA - 30', 'EMBARQUE - 34',
    'EMPAQUE PRIMARIO - 31', 'MENUDENCIAS - 27', 'LIMPIEZA INDUSTRIAL - 15', 'SALA DE CUARTEO - 29', 'FAENA - 26',
    'PCP - 45', 'GRASERIA - 41', 'FINANCIERO - 47', 'LIMPIEZA ADMINISTRATIVA - 46', 'RECEPCION - 72',
    'COMPRAS - 38',
    'CONTROL DE STOCK - 71', 'CONTABILIDAD - 48', 'AUDITORIA - 50', 'AREA TECNICA - 57', 'ELECTRICA - 58',
    'CIVIL - 59', 'MECANICO - 60', 'SALA DE MAQUINAS - 61', 'UTILIDADES - 83', 'PATIO - 62', 'PTE - 43',
    'CALDERA - 40', 'DEPARTAMENTO MEDICO - 53', 'SEGURIDAD OCUPACIONAL - 54', 'TRANSPORTE - 51', 'PORTERIA - 21',
    'EMPAQUE SECUNDARIO - 32', 'MONDONGUERIA - 28', 'PTA - 44', 'INFORMATICA - 64', 'CONTROL DE CALIDAD - 39',
    'LABORATORIO - 42', 'LAVANDERIA - 16', 'COMEDOR - 19', 'ASUNCION - 67', 'SALA DE ROLDANA - 84',
    'FORMACIÓN PROFESIONAL DESPOSTADA - 81', 'CORRAL - 24', 'LAVADERO - 23', 'SALA DE CUERO - 76',
    'APARTADOS - 79',
    'FORMACIÓN PROFESIONAL FAENA - 80', 'IVO - 66', 'REUBICACION LAVANDERIA - 85', 'EMPAQUE PRIMARIO - 31 ',
    'BIENESTAR ANIMAL - 82', 'TRIPERIA - 56', 'DESPOSTADA - 30 ', 'MENUDENCIAS - 27 ', 'CARNICERIA - 63',
    'Reubicación Despostada - 86'
]

# Insertar departamentos sin duplicados
unique_departments = set(departments_data)
for department_name in unique_departments:
    departments = Departments.objects.filter(name=department_name.capitalize())
    if departments.exists():
        department = departments.first()
    else:
        department = Departments.objects.create(name=department_name.capitalize())
print(f"Se creó el departamento")

positions_data = [
    'Analista de ByS', 'Gerente Industrial', 'Coordinador', 'Supervisor', 'Encargado de PCP', 'Contador',
    'Auditoria', 'Auxi.Sala de Maquina', 'Operador', 'Gerente G de Calidad', 'ASISTENTE DIRECTORIO',
    'Cuchillero 1', 'Aux  Producion', 'Asistente de RRHH', 'Balancero 1', 'Cuchillero Faena 2',
    'Cuchillero Faena 1', 'Auxi/lavanderia',
    'Entrenador', 'Corrallero', 'Cuchillero 2', 'Cuchillero/Menuden 2', 'Clasificador', 'Serruchero',
    'Lombador A', 'Auxi/Cocina', 'Despostador 2', 'Limpiador', 'Cocinera 3', 'Balancero  2', 'Cocinera 1',
    'LIDER BIENESTAR ANIM', 'Despostador 1', 'Operador 2', 'Recibidor', 'Operador 1', 'Planillero/A', 'Chofer',
    'LIMPIADORA',
    'Auxi.Control/Calidad', 'Lider 2', 'Analista de Salarios', 'GRASERIA', 'LIMPIEZA INDUSTRIAL', 'EMBARQUE',
    'DESPOSTADA', 'EMPAQUE SECUNDARIO', 'Aux Caldera', 'Aux de informatica', 'Lider 1', 'Asistente de PCP',
    'Analista de PCP', 'Mecanico', 'Albanil-Pedreiro', 'TRACTORISTA', 'Electricista', 'Analista de ByS - 182',
    'Analista RR.HH - 10', 'Gerente Industrial - 158', 'Coordinador - 159', 'Supervisor 2 - 202',
    'Supervisor 1 - 9', 'Supervisor 3 - 203', 'Lider 3 - 188', 'Gerente Financero - 96', 'Copera - 214',
    'RECEPCIONISTA - 171', 'Cuchillero 2 - 122', 'Encargado de Consumo', 'Analista de Contabil - 212',
    'Auditoria - 168',
    'Aux Trazabilidad - 206', 'PCM - 209', 'Lider 1 - 119', 'Electricista - 156', 'Albanil-Pedreiro - 157',
    'Mecanico - 130', 'Operador Sala de Maq - 205', 'TRACTORISTA - 172', 'Operador 3 - 114', 'Aux Caldera - 95',
    'Auxiliar - 91', 'MEDICO - 170', 'Enfermera - 183', 'Planillero/A - 134', 'Chofer - 153',
    'Auxiliar de Báscula - 191',
    'Clasificador - 160', 'Gerente de Compras - 195', 'Operador Caldera - 204', 'Aux de informatica - 184',
    'Gerente G de Calidad - 178', 'Lider 2 - 120', 'Cocinera 1 - 180', 'Portero - 196',
    'Encargado de Compras - 94', 'ASISTENTE DIRECTORIO - 167', 'Encargado Contabilid - 211',
    'Lider Deposito - 210', 'Balancero  2 - 97',
    'Balancero 1 - 98', 'Balancero 3 - 115', 'Limpiador - 129', 'Operador 1 - 116', 'Operador 2 - 117',
    'Analist Trazabilidad - 161', 'Cuchillero Faena 2 - 137', 'Cuchillero Faena 1 - 92', 'Corralero - 132',
    'Cuchillero/Menuden 1 - 135', 'Cuchillero 1 - 121', 'Despostador 2 - 145', 'Cocinera 2 - 179', 'Monitor 2 - 127',
    'Recibidor 1 - 176', 'Despostador 1 - 99', 'Lombador 2 - 181', 'Serruchero 4 - 201', 'Cuchillero Faena  1',
    'Serruchero/faena 2 - 142', 'Lider 4 - 198', 'Asist de Laboratorio - 197', 'Auxi.Control/Calidad - 125',
    'Etiquetero - 186', 'Asistente de PCP - 190', 'Montacarguista 1 - 133', 'Serruchero 2 - 200', 'Recibidor 2 - 207',
    'Camarista - 199', 'Auxiliar IVO 2 - 215', 'Serruchero 1 - 177', 'Montacarguista 2 - 217',
    'Auxiliar IVO 1 - 218', 'Asistente de RRHH - 93', 'Conferente - 189', 'Analista de PCP - 208',
    'Gerente mantenimient - 194', 'Aux. Cuchillera/o - 219', 'Monitor 1 - 126', 'Auxiliar Despostador - 220',
    'AUX. FINANCIERO - 174',
    'Supervisor Informat - 213', 'Analista de Salarios - 193', 'Auxiliar - 91 ', 'Encargado Carnicería - 162',
    'Vendedor - 7', 'Montacarguista - 133', 'Auxiliar IVO - 215', 'Entrenador - 192', 'Aux. produccion - 216',
    'Encargado de Consumo - 221', 'Balancero 2'
]

for position, department_name in zip(positions_data, departments_data):
    department = Departments.objects.get(name=department_name.capitalize())
    EmployeePositions.objects.create(name=position.capitalize(), departament=department)
print(f"Se creó la posición")

# # Agregar datos en el modelo Vacants
positions = EmployeePositions.objects.all()
for _ in range(10):
    position = random.choice(positions)
    description = get_random_string(length=20)
    min_salary = round(random.uniform(1000, 2000), 2)
    max_salary = round(min_salary + random.uniform(100, 500), 2)
    Vacants.objects.create(
        posicion=position,
        description=positions,
        min_salary=min_salary,
        max_salary=max_salary
    )
print('guardados')
candidates = Candidatos.objects.all()
vacants = Vacants.objects.all()
for _ in range(10):
    person = random.choice(candidates)
    vacant = random.choice(vacants)
    Selection.objects.create(
        person=person,
        vacants=vacant
    )
print('guardados')

candidates = Candidatos.objects.all()
departments = Departments.objects.all()
positions = EmployeePositions.objects.all()
turns = EmployeeTurn.objects.all()

for _ in range(20):
    person = random.choice(candidates)
    department = random.choice(departments)
    position = random.choice(positions)
    turn = random.choice(turns)
    salary = round(random.uniform(1000, 5000), 2)
    estado = random.choice(['Contratado', 'Despedido', 'Vacaciones', 'Licencia'])
    hiring_date = date(random.randint(2000, 2022), random.randint(1, 12), random.randint(1, 28))
    if not Employee.objects.filter(person=person).exists():
        Employee.objects.create(
            person=person,
            department=department,
            position=position,
            turn=turn,
            salary=salary,
            estado=estado,
            hiring_date=hiring_date
        )
print('Guardados')

User = get_user_model()
def create_users_from_employees():
    employees = Employee.objects.all()
    group_id = 1
    group = Group.objects.get(id=group_id)

    for employee in employees:
        if not User.objects.filter(username=employee.get_full_name()).exists():
            user = User.objects.create_user(
                username=employee.person.cedula,
                password=employee.person.cedula,
                employee=employee,
            )
            user.groups.set([group])
            print(f'Se creó el usuario para {employee.get_full_name()}')
        else:
            print(f'El usuario para {employee.get_full_name()} ya existe')
if __name__ == "__main__":
    create_users_from_employees()
    print('User created')

# Remuneraciones
Headings.objects.create(name='Salario', type='remuneracion', order=1, has_quantity=True)
Headings.objects.create(name='Reembolso', type='remuneracion', order=2, has_quantity=False)
Headings.objects.create(name='Movilizacion', type='remuneracion', order=3, has_quantity=False)
Headings.objects.create(name='Decimo Tercero Mensual', type='remuneracion', order=4, has_quantity=False)
Headings.objects.create(name='Decimo Cuarto Mensual', type='remuneracion', order=5, has_quantity=False)
Headings.objects.create(name='Bonificacion', type='remuneracion', order=6, has_quantity=False)

# Descuentos
Headings.objects.create(name='Prestamo a la Empresa', type='descuentos', order=1, has_quantity=False)
Headings.objects.create(name='Prestamo Hipotecario', type='descuentos', order=2, has_quantity=False)
Headings.objects.create(name='Prestamo Quirografario', type='descuentos', order=3, has_quantity=False)
Headings.objects.create(name='Otros Descuentos', type='descuentos', order=4, has_quantity=False)
Headings.objects.create(name='Prestamo Banco', type='descuentos', order=5, has_quantity=False)
Headings.objects.create(name='Extension de Salud', type='descuentos', order=6, has_quantity=False)

current_date = datetime.datetime.now().date()
number_list = [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]

for day in range(1, 30):
    date_joined = datetime.datetime.strptime(f'{current_date.year}-{current_date.month}-{day}', '%Y-%m-%d')
    assistance = Assistance()
    assistance.year = current_date.year
    assistance.month = current_date.month
    assistance.day = day
    assistance.date_joined = date_joined
    assistance.save()
    for employee in Employee.objects.filter(estado='Contratado'):
        detail = AssistanceDetail()
        detail.assistance_id = assistance.id
        detail.employee = employee
        detail.state = random.choice(number_list)
        detail.description = '' if detail.state else 'No asistio al trabajo'
        detail.save()
print('Guardado')
