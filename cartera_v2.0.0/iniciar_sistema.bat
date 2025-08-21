@echo off
echo ========================================
echo Sistema de Gestion de Cartera - Grupo Planeta
echo Version 2.0.0 - Aplicacion Web Python
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

echo Python encontrado. Verificando dependencias...
echo.

echo Instalando dependencias de Flask...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo Dependencias instaladas correctamente.
echo.

echo Iniciando servidor web...
echo.
echo ========================================
echo Servidor disponible en: http://localhost:5000
echo Presiona Ctrl+C para detener el servidor
echo ========================================
echo.

python app.py

pause
