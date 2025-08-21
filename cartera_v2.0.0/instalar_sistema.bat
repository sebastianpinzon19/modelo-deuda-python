@echo off
echo ========================================
echo Sistema de Gestion de Cartera - Grupo Planeta
echo Version 2.0.0 - Instalacion Completa
echo ========================================
echo.

echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no esta instalado o no esta en el PATH
    echo.
    echo Por favor instala Python 3.8 o superior desde:
    echo https://python.org/downloads/
    echo.
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python encontrado: %PYTHON_VERSION%
echo.

echo [2/5] Actualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠ ADVERTENCIA: No se pudo actualizar pip, continuando...
    echo.
)

echo [3/5] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: No se pudieron instalar las dependencias
    echo.
    echo Posibles soluciones:
    echo 1. Verificar conexion a internet
    echo 2. Ejecutar como administrador
    echo 3. Actualizar pip manualmente: python -m pip install --upgrade pip
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente
echo.

echo [4/5] Ejecutando pruebas del sistema...
python test_sistema.py
if errorlevel 1 (
    echo ❌ ERROR: Las pruebas del sistema fallaron
    echo.
    echo Revisa los errores antes de continuar
    pause
    exit /b 1
)

echo ✅ Pruebas del sistema exitosas
echo.

echo [5/5] Creando carpetas necesarias...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs
if not exist "logs" mkdir logs

echo ✅ Carpetas creadas correctamente
echo.

echo ========================================
echo 🎉 INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Para iniciar el sistema:
echo 1. Ejecuta: iniciar_sistema.bat
echo 2. O manualmente: python app.py
echo.
echo El sistema estara disponible en:
echo http://localhost:5000
echo.
echo Para detener el servidor: Ctrl+C
echo ========================================
echo.

pause
