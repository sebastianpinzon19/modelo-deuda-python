@echo off
chcp 65001 >nul
title Modelo de Deuda - Sistema de Procesamiento

echo.
echo ========================================
echo    MODELO DE DEUDA - SISTEMA PYTHON
echo ========================================
echo.

cd /d "%~dp0"

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo Por favor instale Python 3.7 o superior
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

echo Verificando dependencias...
python -c "import pandas, xlsxwriter, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Faltan dependencias de Python
    echo Ejecutando instalación automática...
    pip install pandas xlsxwriter openpyxl
    if errorlevel 1 (
        echo ❌ ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

echo ✅ Dependencias verificadas
echo.

echo ========================================
echo    INSTRUCCIONES DE USO
echo ========================================
echo.
echo El sistema requiere:
echo 1. Archivo de provisión procesado (.xlsx)
echo 2. Archivo de anticipos procesado (.xlsx)
echo 3. TRM Dólar (ejemplo: 4000)
echo 4. TRM Euro (ejemplo: 4300)
echo.

echo ¿Desea ejecutar el modelo de deuda? (S/N)
set /p continuar=

if /i "%continuar%"=="S" (
    echo.
    echo Ejecutando modelo de deuda...
    python modelo_deuda.py
) else (
    echo.
    echo Ejecución cancelada por el usuario
)

echo.
echo Presione cualquier tecla para salir...
pause >nul
