# # from config.wsgi import *
# # from core.erp.models import Departments,EmployeePositions
# # # import random
# # #
# # # data = ['Leche y derivados', 'Carnes, pescados y huevos', 'Patatas, legumbres, frutos secos',
# # #         'Verduras y Hortalizas', 'Frutas', 'Cereales y derivados, azúcar y dulces',
# # #         'Grasas, aceite y mantequilla']
# # #
# # # # delete from public.erp_category;
# # # # ALTER SEQUENCE erp_category_id_seq RESTART WITH 1;
# # #
# # # letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
# # #            'u', 'v', 'w', 'x', 'y', 'z']
# # #
# # # for i in range(1, 10000):
# # #     name = ''.join(random.choices(letters, k=5))
# # #     while Departments.objects.filter(name=name).exists():
# # #         name = ''.join(random.choices(letters, k=5))
# # #     Departments(name=name).save()
# # # print('Regitros guardado')
# #
# # import datetime
# #
# # t = datetime.datetime.today().strftime('%I:%M:%S:%p')
# # print(t)
# # import random
# #
# # import string
# #
# #
# # def generate_employee_code():
# #     letters = string.ascii_uppercase
# #     numbers = string.digits
# #     code = ''.join(random.choice(letters)
# #                    for i in range(3)) + ''.join(random.choice(numbers) for i in range(3))
# #     return code
# #
# #
# # # employe_code = generate_employee_code()
# # # print(f'Codigo  generado: {employe_code}')
# #
# #
# # import random
# #
# #
# #
# #
# #
# # # print(generar_numero_cuenta())
# # #
# # # employe_account_number = generar_numero_cuenta()
# # # print(f'Numero de cuenta generado: {employe_account_number}')
# #
# # # Definimos los datos de la empresa
# # # nombre_empresa = "Mi Empresa S.A."
# # # direccion_empresa = "Calle Principal #123"
# # # telefono_empresa = "809-555-5555"
# # #
# # # # Definimos los datos de los empleados
# # # empleados = [
# # #     {"nombre": "Juan Perez", "salario": 25000, "puesto": "Gerente"},
# # #     {"nombre": "Maria Garcia", "salario": 15000, "puesto": "Supervisor"},
# # #     {"nombre": "Pedro Diaz", "salario": 10000, "puesto": "Asistente"},
# # # ]
# # #
# # # # Calculamos la nómina de cada empleado
# # # for empleado in empleados:
# # #     salario_mensual = empleado["salario"]
# # #     salario_quincenal = salario_mensual / 2
# # #     salario_diario = salario_mensual / 30
# # #     salario_hora = salario_diario / 8
# # #
# # #     print("Nombre: " + empleado["nombre"])
# # #     print("Puesto: " + empleado["puesto"])
# # #     print("Salario Mensual: " + str(salario_mensual))
# # #     print("Salario Quincenal: " + str(salario_quincenal))
# # #     print("Salario Diario: " + str(salario_diario))
# # #     print("Salario por Hora: " + str(salario_hora))
# # #     print("--------------------")
# # #
# # # # Calculamos el total de la nómina
# # # total_nomina = sum([empleado["salario"] for empleado in empleados])
# # #
# # # # Imprimimos el total de la nómina
# # # print("Total de la nómina: " + str(total_nomina))
# #
# #
# # # Creamos una lista con algunos datos de ejemplo
# # data = [
# #     {'name': 'Finanzas', 'description': 'Departamento de finanzas'},
# #     {'name': 'Ventas', 'description': 'Departamento de ventas'},
# #     {'name': 'Marketing', 'description': 'Departamento de marketing'},
# #     {'name': 'Recursos Humanos', 'description': 'Departamento de recursos humanos'},
# #     {'name': 'Tecnología', 'description': 'Departamento de tecnología'},
# #     {'name': 'Operaciones', 'description': 'Departamento de operaciones'},
# #     {'name': 'Logística', 'description': 'Departamento de logística'},
# #     {'name': 'Compras', 'description': 'Departamento de compras'},
# #     {'name': 'Legal', 'description': 'Departamento legal'},
# #     {'name': 'Investigación y Desarrollo', 'description': 'Departamento de investigación y desarrollo'}
# # ]
# #
# # # Recorremos la lista y creamos los objetos de Departments
# # # for item in data:
# # #     department = Departments.objects.create(
# # #         name=item['name'],
# # #         description=item['description']
# # #     )
# # #     department.save()
# # #     print('Registro guardado')
# #
#
# import random
#
# # Lista con nombres de posiciones acordes al departamento
# posiciones = {
#     'Finanzas': ['Contador', 'Analista financiero', 'Tesorero', 'Especialista en impuestos'],
#     'Ventas': ['Ejecutivo de ventas', 'Gerente de ventas', 'Coordinador de eventos', 'Especialista en mercadeo'],
#     'Marketing': ['Especialista en redes sociales', 'Gerente de marketing', 'Coordinador de publicidad'],
#     'Recursos Humanos': ['Gerente de recursos humanos', 'Especialista en nóminas', 'Reclutador', 'Especialista en capacitación'],
#     'Tecnología': ['Desarrollador de software', 'Ingeniero de sistemas', 'Especialista en seguridad informática', 'Gerente de TI'],
#     'Operaciones': ['Gerente de operaciones', 'Supervisor de producción', 'Especialista en calidad', 'Coordinador de mantenimiento'],
#     'Logística': ['Gerente de logística', 'Coordinador de almacén', 'Especialista en transporte'],
#     'Compras': ['Gerente de compras', 'Comprador', 'Especialista en adquisiciones', 'Coordinador de suministros'],
#     'Legal': ['Abogado corporativo', 'Especialista en propiedad intelectual', 'Gerente legal'],
#     'Investigación y Desarrollo': ['Investigador', 'Desarrollador de producto', 'Especialista en diseño']
# }
#
# # Lista con nombres aleatorios para las posiciones
# nombres = ['Analista', 'Ejecutivo', 'Gerente', 'Especialista', 'Coordinador']
#
# # Obtenemos todos los departamentos existentes
# departamentos = Departments.objects.all()
#
# # Recorremos los departamentos y creamos 2 posiciones aleatorias para cada uno
# for departamento in departamentos:
#     nombres_posiciones = random.sample(posiciones[departamento.name], 2)
#     for nombre_posicion in nombres_posiciones:
#         nombre_completo = f'{random.choice(nombres)} de {nombre_posicion}'
#         posicion = EmployeePositions.objects.create(
#             name=nombre_completo,
#             description=f'Posición de {nombre_posicion}',
#             departament=departamento
#         )
#         posicion.save()
#     print(f'Guardado')