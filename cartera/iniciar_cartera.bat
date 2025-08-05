@echo off
REM Cambia al directorio del backend (ajusta la ruta si es necesario)
cd /d C:\wamp64\www\cartera

REM (Opcional) Inicia el servidor embebido de PHP si no usas Apache/WAMP
REM php -S localhost:8000

REM Espera 2 segundos para asegurarse de que el servidor arranque (si usas el embebido)
REM timeout /t 2 >nul

REM Abre el navegador en la página principal del sistema
start "" http://localhost/cartera/

REM Mensaje opcional
echo Sistema de Cartera iniciado. Puedes cerrar esta ventana.