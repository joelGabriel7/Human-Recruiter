# Human-Recruiter

**Human-Recruiter** es un sistema de gestión de recursos humanos que ofrece una amplia gama de funcionalidades para optimizar el manejo de empleados, reclutadores y seguridad.

## Funcionalidades

### Recursos Humanos
- **Gestión de empleados**
- **Asistencias**
- **Departamentos**
- **Puestos de trabajo**
- **Horarios**
- **Items de descuentos**
- **Salarios o nómina**

### Reclutadores
- **Gestión de vacantes**
- **Gestión de personas**: Relacionado con la gestión de candidatos y empleados. Para crear un empleado, primero debe estar registrado en el módulo de personas.
- **Gestión de candidatos**: Integrado con vacantes y personas.

### Seguridad
- **Gestión de usuarios**: Controla los usuarios que tendrán acceso al sistema.
- **Control de acceso**: Registra todos los dispositivos que ingresan al sistema.

### Funcionalidades Extras
- **Editar perfil de usuario**
- **Cambiar contraseña**
- **Entidad compañía**: Permite que la empresa editora pueda modificar su propia información.

## Arquitectura del Proyecto

El proyecto sigue la arquitectura MVT (Model-View-Template) de Django, proporcionando una estructura organizada para el desarrollo.

## Tecnologías

- **Django**
- **HTML**
- **CSS**
- **JavaScript**
- **jQuery**

## Plugins

- **Datatable**
- **Select2**
- **SweetAlert**
- **jQuery Confirm**
- **AdminLTE3**

## Bases de Datos

El proyecto usa **SQLite** por defecto. Para usar otras bases de datos como **PostgreSQL** o **MySQL**, realiza los siguientes pasos:

1. **Configura la base de datos**: Modifica `db.py` en la carpeta de configuración.
2. **Actualiza el archivo de configuración**: Cambia `sqlite` por la base de datos que elijas en el archivo `settings.py`.
3. **Llena los datos necesarios** para tu nueva base de datos.
4. **Aplique las migraciones correspondientes y cree un superusuario**

## Instalación y Configuración

Siga estos pasos para configurar el proyecto en su entorno local:

1. **Clonar o Descargar el repositorio**:
   ```
   git clone [URL del repositorio]
   cd [nombre del directorio]
   ```

2. **Crear y activar un entorno virtual**:
   ```
   python -m venv venv
   source venv/bin/activate  
   # En Windows para activar `venv\Scripts\activate`
   ```

3. **Instalar las dependencias**:
   ```
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**:
   - Por defecto, el proyecto está configurado para usar SQLite. 
   - Si desea usar PostgreSQL o MySQL debera realizar los siguientes pasos:

    1. **Configura la base de datos**: Modifica `db.py` en la carpeta de configuración.
    2. **Actualiza el archivo de configuración**: Cambia `sqlite` por la base de datos que elijas en el archivo `settings.py`.
    3. **Llena los datos necesarios** para tu nueva base de datos.
    

5. **Crear y aplicar las migraciones**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6.**Configura el superusuario automáticamente:**

    Hemos creado un script que automatiza la creación de un superusuario y la asignación de permisos. Ejecuta el siguiente comando para configurar el usuario administrador:

    ```bash
         python  user_init.py
    ```

    Este comando creará un usuario con el nombre de usuario `root` y la contraseña `root`!


7. **Ejecutar el servidor de desarrollo**:
   ```
   python manage.py runserver
   ```
