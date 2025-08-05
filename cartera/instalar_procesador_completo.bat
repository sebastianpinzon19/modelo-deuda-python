@echo off
echo ========================================
echo Instalador del Procesador Completo de Balance
echo Grupo Planeta
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instale Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo Python encontrado. Instalando dependencias...
echo.

cd /d "%~dp0"

echo Instalando librerias Python...
pip install -r PROVCA/requirements.txt

if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias de Python
    pause
    exit /b 1
)

echo.
echo Creando directorio temporal...
if not exist "temp" mkdir temp

echo.
echo Verificando permisos de escritura...
echo test > temp\test.txt
if not exist "temp\test.txt" (
    echo ERROR: No se pueden crear archivos en el directorio temp
    echo Verifique los permisos del directorio
    pause
    exit /b 1
)
del temp\test.txt

echo.
echo ========================================
echo Instalacion completada exitosamente!
echo ========================================
echo.
echo Para usar el sistema:
echo 1. Acceda a procesar_balance_completo.php en su navegador
echo 2. Suba los archivos Excel requeridos
echo 3. Haga clic en "Procesar Archivos"
echo.
echo Para probar el sistema:
echo php test_procesador_completo.php
echo.
pause 