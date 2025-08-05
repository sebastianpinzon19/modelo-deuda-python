# Sistema de Procesamiento de Cartera - Estructura Final

## 📁 Estructura del Proyecto

```
cartera/
├── front_php/                    # Interfaz web PHP
│   ├── dashboard.php            # Página principal del sistema
│   ├── procesar_cartera.php     # Procesador principal de cartera
│   ├── procesar.php             # Procesador de anticipos
│   ├── modelo_deuda.php         # Generador de modelo de deuda
│   ├── descargar_resultado.php  # Descarga segura de archivos
│   ├── configuracion.php        # Configuración global del sistema
│   ├── styles.css               # Estilos CSS del sistema
│   ├── planetacargando.gif      # Imagen de carga
│   ├── Logo grupo planeta color transparente.jpg
│   ├── README.md                # Documentación general
│   └── README_PROCESADOR_COMPLETO.md
├── PROVCA/                      # Backend Python
│   ├── procesador_cartera.py    # Procesador principal de cartera
│   └── utilidades_cartera.py    # Funciones auxiliares
├── temp/                        # Archivos temporales de carga
├── resultados/                  # Archivos procesados generados
└── README_FINAL.md             # Este archivo
```

## 🔄 Flujo del Sistema

### 1. Interfaz Web (PHP)
- **dashboard.php**: Página principal con acceso a todas las funcionalidades
- **procesar_cartera.php**: Maneja la carga de archivos Excel (BALANCE, SITUACIÓN, FOCUS)
- **procesar.php**: Procesa archivos de anticipos
- **modelo_deuda.php**: Genera modelos de deuda
- **descargar_resultado.php**: Descarga segura de archivos procesados

### 2. Procesamiento (Python)
- **procesador_cartera.py**: Script principal que procesa los archivos Excel
- **utilidades_cartera.py**: Funciones auxiliares para el procesamiento

### 3. Directorios de Trabajo
- **temp/**: Archivos temporales de carga (se limpian automáticamente)
- **resultados/**: Archivos procesados generados por el sistema

## 🚀 Funcionalidades Principales

### Procesador de Cartera
- Carga de archivos Excel (BALANCE, SITUACIÓN, FOCUS)
- Procesamiento automático con Python
- Cálculos de vencimientos, dotaciones y mora
- Generación de reportes en Excel
- Descarga segura de resultados

### Procesador de Anticipos
- Procesamiento de archivos CSV de anticipos
- Generación de reportes de análisis

### Modelo de Deuda
- Generación de modelos de deuda
- Análisis de cartera

## ⚙️ Configuración

### Requisitos del Sistema
- WAMP/XAMPP con PHP 7.4+
- Python 3.8+ con las siguientes librerías:
  - pandas
  - openpyxl
  - numpy
  - datetime

### Configuración de Rutas
- Python path configurado en `front_php/configuracion.php`
- Directorios temporales: `temp/` y `resultados/`

## 📋 Archivos Eliminados (Limpieza)

### Archivos PHP Eliminados:
- `procesar_balance.php` (duplicado)
- `balance.php` (duplicado)
- `cartera.php` (duplicado)
- `anticipos.php` (duplicado)
- `modelo.php` (duplicado)
- `preview_excel.php` (no esencial)
- `python_config.php` (redundante)
- `iniciar_cartera.bat` (no web)
- `README_BALANCE.md` (redundante)
- `README_CSS.md` (redundante)
- `CAMPO_FECHA_FIN_PERIODO.md` (específico)

### Archivos Python Eliminados:
- `procesador_balance.py` (duplicado)
- `procesador_anticipos.py` (integrado)
- `preview_excel.py` (no esencial)
- `main.py` (no necesario)
- `modelo_deuda.py` (funcionalidad en PHP)
- Archivos duplicados de recursos

### Directorios Eliminados:
- `PROVCA_PROCESADOS/` (reemplazado por `resultados/`)
- `AN/` (archivos de ejemplo)

## 🎯 Resultado Final

El sistema ahora está completamente organizado con:
- ✅ Separación clara entre frontend (PHP) y backend (Python)
- ✅ Nombres de archivos profesionales y descriptivos
- ✅ Eliminación de archivos redundantes y de prueba
- ✅ Estructura de directorios limpia y lógica
- ✅ Documentación actualizada
- ✅ Flujo de trabajo optimizado

## 🔧 Mantenimiento

- Los archivos temporales se limpian automáticamente
- Los resultados se guardan en `resultados/`
- La configuración está centralizada en `configuracion.php`
- El sistema es escalable y mantenible 