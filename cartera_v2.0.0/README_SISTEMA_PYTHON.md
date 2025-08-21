# Sistema de Gestión de Cartera - Grupo Planeta v2.0.0

## 🚀 Aplicación Web Python Completa

Este sistema reemplaza completamente la funcionalidad PHP con una aplicación web moderna desarrollada en Python usando Flask.

## 📋 Características

- **Interfaz Web Moderna**: Diseño responsive con CSS moderno y JavaScript
- **Procesamiento de Archivos**: Cartera, Anticipos, Modelo de Deuda y Balance
- **Gestión TRM**: Configuración de tasas de cambio USD/EUR
- **Descarga de Archivos**: Generación y descarga automática de resultados
- **Validaciones**: Control de errores y validación de archivos
- **Logging**: Sistema de logs para debugging

## 🛠️ Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 📦 Instalación

### Opción 1: Instalación Automática (Recomendada)

1. **Ejecutar el script de inicio**:
   ```bash
   # En Windows (PowerShell o CMD)
   iniciar_sistema.bat
   ```

2. **El script automáticamente**:
   - Verifica que Python esté instalado
   - Instala todas las dependencias
   - Inicia el servidor web

### Opción 2: Instalación Manual

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```

## 🌐 Uso del Sistema

1. **Abrir navegador** en: `http://localhost:5000`

2. **Seleccionar proceso**:
   - **Cartera**: Procesar archivos CSV de cartera
   - **Anticipos**: Procesar archivos Excel de anticipos
   - **Modelo Deuda**: Generar modelo combinando cartera y anticipos
   - **Balance**: Procesar archivos de balance

3. **Configurar TRM** (opcional):
   - Ingresar tasas de cambio USD/COP y EUR/COP
   - Guardar configuración

4. **Subir archivos** y procesar

5. **Descargar resultados** generados

## 📁 Estructura del Proyecto

```
cartera_v2.0.0/
├── app.py                          # Aplicación principal Flask
├── requirements.txt                # Dependencias Python
├── iniciar_sistema.bat            # Script de inicio Windows
├── templates/
│   └── index.html                 # Interfaz web principal
├── uploads/                       # Archivos temporales subidos
├── outputs/                       # Archivos procesados
└── PROVCA/                        # Módulos de procesamiento
    ├── procesador_cartera.py
    ├── procesador_anticipos.py
    ├── modelo_deuda.py
    ├── procesador_balance_completo.py
    ├── trm_config.py
    └── ...
```

## 🔧 Configuración

### Variables de Entorno (Opcional)

```bash
# Configurar puerto personalizado
set FLASK_PORT=8080

# Configurar modo debug
set FLASK_DEBUG=True
```

### Configuración TRM

Las tasas de cambio se guardan en `PROVCA/trm_config.json`:

```json
{
    "trm_usd": 4000.0,
    "trm_eur": 4700.0
}
```

## 📊 Funcionalidades por Proceso

### 1. Cartera (Provisión)
- **Entrada**: Archivo CSV
- **Parámetros**: Moneda, Fecha de cierre
- **Salida**: Excel procesado con provisiones

### 2. Anticipos
- **Entrada**: Archivo Excel
- **Salida**: Excel procesado de anticipos

### 3. Modelo Deuda
- **Entrada**: Archivos Excel de cartera y anticipos
- **Salida**: Modelo de deuda consolidado

### 4. Balance
- **Entrada**: Archivo Excel de balance
- **Salida**: Balance procesado y analizado

## 🔍 API Endpoints

### TRM Management
- `GET /api/trm` - Obtener configuración TRM
- `POST /api/trm` - Guardar configuración TRM

### File Processing
- `POST /api/procesar/cartera` - Procesar cartera
- `POST /api/procesar/anticipos` - Procesar anticipos
- `POST /api/procesar/modelo` - Procesar modelo
- `POST /api/procesar/balance` - Procesar balance

### File Download
- `GET /descargar/<filename>` - Descargar archivo procesado

### System Status
- `GET /api/status` - Estado del sistema

## 🐛 Troubleshooting

### Error: "Python no está instalado"
- Instalar Python desde: https://python.org
- Asegurar que esté en el PATH del sistema

### Error: "No se pudieron instalar las dependencias"
- Verificar conexión a internet
- Actualizar pip: `python -m pip install --upgrade pip`
- Instalar manualmente: `pip install -r requirements.txt`

### Error: "Puerto 5000 en uso"
- Cambiar puerto en `app.py` línea final
- O matar proceso que use el puerto

### Error: "Archivo no encontrado"
- Verificar que el archivo existe en la carpeta `outputs/`
- Revisar logs en consola

## 📝 Logs

Los logs se muestran en la consola donde se ejecuta la aplicación:

```
🚀 Iniciando Sistema de Gestión de Cartera - Grupo Planeta
📊 Versión 2.0.0 - Aplicación Web Python
🌐 Servidor disponible en: http://localhost:5000
```

## 🔒 Seguridad

- Validación de tipos de archivo
- Sanitización de nombres de archivo
- Límite de tamaño de archivo (50MB)
- Manejo seguro de rutas

## 🚀 Despliegue en Producción

Para producción, usar WSGI server como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📞 Soporte

Para problemas técnicos:
1. Revisar logs en consola
2. Verificar archivos de entrada
3. Comprobar configuración TRM
4. Revisar permisos de carpetas

## 🔄 Migración desde PHP

Este sistema reemplaza completamente:
- `front_php/index.php` → `templates/index.html`
- `front_php/runner.php` → `app.py` (endpoints API)
- `front_php/*.php` → Módulos Python en `PROVCA/`

**Ventajas de la migración**:
- Mejor rendimiento
- Código más mantenible
- Interfaz moderna
- Mejor manejo de errores
- Logs detallados
