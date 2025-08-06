# Sistema de Procesamiento de Cartera - Grupo Planeta

## 📋 Descripción

Sistema completo para el procesamiento y análisis de archivos de cartera, desarrollado en PHP y Python. El sistema incluye procesadores específicos para diferentes tipos de archivos (BALANCE, SITUACIÓN, FOCUS) y genera reportes consolidados en Excel.

## 🏗️ Arquitectura del Sistema

### Estructura de Directorios
```
cartera/
├── config.php                 # Configuración centralizada
├── index.php                  # Interfaz principal
├── procesadores/              # Procesadores PHP
│   ├── procesar_balance_especifico.php
│   ├── procesar_situacion_especifico.php
│   ├── procesar_focus_especifico.php
│   ├── procesar_dotacion_mes.php
│   ├── procesar_acumulado.php
│   └── procesar_tipos_cambio.php
├── utilidades/                # Utilidades del sistema
│   ├── descargar_archivos.php
│   ├── diagnostico_python.php
│   ├── limpiar_archivos.php
│   ├── limpiar_cache.php
│   └── test_sistema.php
├── PROVCA/                    # Scripts Python
│   ├── utilidades_cartera.py
│   ├── procesador_balance_especifico.py
│   ├── procesador_situacion_especifico.py
│   ├── procesador_focus_especifico.py
│   ├── procesador_dotacion_mes.py
│   ├── procesador_acumulado.py
│   ├── procesador_tipos_cambio.py
│   └── unificador_final.py
├── documentacion/             # Documentación del sistema
├── temp/                      # Archivos temporales
├── resultados/                # Archivos de salida
└── logs/                      # Logs del sistema
```

## 🚀 Instalación

### Requisitos Previos

1. **WAMP Server** (o similar)
   - PHP 8.0 o superior
   - Apache/Nginx

2. **Python 3.8+**
   - pandas
   - openpyxl
   - xlrd

### Instalación de Dependencias Python

```bash
pip install pandas openpyxl xlrd
```

### Configuración

1. Clonar el repositorio en el directorio web:
```bash
git clone [URL_DEL_REPOSITORIO] /ruta/a/wamp/www/
```

2. Verificar que Python esté en el PATH o configurar la ruta en `config.php`

3. Crear directorios necesarios:
```bash
mkdir temp resultados logs
chmod 755 temp resultados logs
```

## 📊 Funcionalidades

### Procesadores Específicos

1. **Balance Específico**
   - Procesa archivos BALANCE
   - Suma columnas "Saldo AAF variación" para cuentas específicas
   - Genera reporte consolidado

2. **Situación Específico**
   - Extrae "TOTAL 01010" de "SALDOS MES"
   - Procesa archivos de situación

3. **Focus Específico**
   - Procesa datos de vencimientos del archivo 2
   - Aplica rangos de días específicos

4. **Dotación del Mes**
   - Calcula: Interco RESTO - Dotaciones Acumuladas (Inicial) - Provisión del mes

5. **Acumulado**
   - Copia fórmulas de B54 a F54
   - Procesa datos específicos de acumulados

6. **Tipos de Cambio**
   - Cambia mes de cierre
   - Actualiza tasas de cambio

### Unificador Final

Consolida todos los archivos procesados en un único archivo Excel con:
- Hojas separadas para cada tipo de procesamiento
- Hoja de resumen
- Hoja de fórmulas
- Fórmulas cruzadas entre hojas

## 🔧 Uso

### Interfaz Web

1. Acceder a `index.php` en el navegador
2. Seleccionar el tipo de procesamiento
3. Subir el archivo correspondiente
4. El sistema procesará automáticamente y generará el resultado

### Línea de Comandos

```bash
# Procesar archivo específico
php procesadores/procesar_balance_especifico.php archivo.xlsx

# Ejecutar limpieza automática
php utilidades/limpiar_archivos.php

# Diagnosticar Python
php utilidades/diagnostico_python.php
```

## 🛠️ Mantenimiento

### Limpieza Automática

El sistema incluye limpieza automática de archivos temporales:
- Archivos temporales: 7 días
- Archivos de resultados: 7 días
- Logs: 30 días

### Logs

- `logs/sistema.log`: Actividad general del sistema
- `logs/errores.log`: Errores específicos
- `logs/limpieza.log`: Actividad de limpieza

## 🔍 Diagnóstico

### Verificar Python

```bash
php utilidades/diagnostico_python.php
```

### Test del Sistema

```bash
php utilidades/test_sistema.php
```

## 📝 Reglas de Negocio

### Balance
- Cuentas objeto: 43001, 43008, 43042
- Subcuentas específicas: 0080.43002.20, 0080.43002.21, etc.
- Suma columna "Saldo AAF variación"

### Situación
- Extrae "TOTAL 01010" de "SALDOS MES"

### Focus
- Datos de vencimientos del archivo 2
- Procesamiento por rangos de días

### Fórmulas Cruzadas
- Deuda bruta NO Grupo (Inicial) = Deuda bruta NO Grupo (Final)
- Cobro de mes - Vencida = Deuda bruta NO Grupo (Inicial) Vencidas - Total vencido de 60 días en adelante / 1000
- Y otras fórmulas específicas del negocio

## 🚨 Solución de Problemas

### Python no encontrado
1. Verificar instalación: `python --version`
2. Agregar Python al PATH del sistema
3. Usar `utilidades/diagnostico_python.php`

### Errores de permisos
1. Verificar permisos de directorios temp/, resultados/, logs/
2. Ejecutar como administrador si es necesario

### Archivos no procesados
1. Verificar formato del archivo (xlsx, xls, csv)
2. Revisar logs en `logs/errores.log`
3. Usar `utilidades/test_sistema.php`

## 📞 Soporte

Para problemas técnicos o consultas sobre el sistema, revisar:
1. Logs del sistema
2. Documentación en `documentacion/`
3. Test del sistema en `utilidades/test_sistema.php`

## 🔄 Control de Versiones

- **v2.0**: Sistema modular con procesadores específicos
- **v1.0**: Sistema básico de procesamiento

## 📄 Licencia

Sistema desarrollado para Grupo Planeta. Uso interno. 