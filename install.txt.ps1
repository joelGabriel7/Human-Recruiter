# install.ps1

# Obtener la ruta del directorio del script actual
$scriptPath = $PSScriptRoot

# Crear un entorno virtual
Write-Host "Creando entorno virtual..."
python -m venv venv

# Activar el entorno virtual
Write-Host "Activando entorno virtual..."
.\venv\Scripts\Activate

# Instalar dependencias del proyecto
Write-Host "Instalando dependencias del proyecto en el entorno virtual..."
pip install -r requirements.txt

Write-Host "Abriendo el servidor..."
python manage.py runserver


