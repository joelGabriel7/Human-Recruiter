
# Human-Recruiter

## Human Recruiter es un sistema de gestion de recursos humanos que cuenta con varias funcionalidades
### Funcionamientos

* Recursos Humanos
* Reclutadores
* Seguridad
  
## Recursos Humanos 
### modulos:
  * Gestion de empleados
  * Asistencias
  * Departamentos
  * Puesto de trabajo
  * Horarios
  * Items de descuentos
  * Los salarios o nomina.

## Reclutadores 
### modulos:
 * Gestion de vacantes
 * Gestion de personas
 * Gestion de candidatos que esta ultima esta relacionada con la de vacantes y personas, cabe mencionar que personas esta relacionada con empleados, es decir para crear un empleado primero debe estar en personas.

## Seguridad
### modulos:
* Gestion de usuarios lo que signifca, lo usuarios que tendran acceso al sistema,
* Control de acceso , este se encargaran de registrar todos los dispositivos que ingresan al sistemas
  
## funcionamientos Extras 
* Editar perfil de usuario
* Editar contraseña,
* Entidad compañia donde la compañia o empresa que adquiera el sisteam podra editar su propia informacion

# Arquitectura del proyecto
La arquitectura usada para ese proyecto es la basica que utiliza django que es MVT lo que significa Model View Template!

# Tecnologias

* Django
* HTML
* CSS
* JS
* JQUERY

# Plugins

* Datatable
* Select2
* SweetAlert
* Jquery Confirm
* AdminLTE3

# Bases de datos
## Es compatible con las siguientes Bases de datos

* PostgreSQL
* MySQL
  
# Guia de Instalación

##### 1) Descomprimir el proyecto en una carpeta de tu sistema operativo

##### 2) Crear un entorno virtual para posteriormente instalar las librerias del proyecto

Para windows:

```bash
python3 -m venv venv 
```
##### 3) Activar el entorno virtual de nuestro proyecto

Para windows:

```bash
cd venv\Scripts\activate.bat 
```

##### 4) Instalar todas las librerias del proyecto que se encuentran en el archivo de requirements.txt

```bash
pip install -r requirements.txt
```

##### 5) Iniciar el servidor del proyecto

```bash
python manage.py runserver 
```
