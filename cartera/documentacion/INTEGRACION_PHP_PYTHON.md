# Integración PHP-Python - Sistema de Cartera Grupo Planeta

## 📋 Descripción General

Este documento describe la integración mejorada entre el frontend PHP y el backend Python del Sistema de Procesamiento de Cartera. La nueva arquitectura proporciona una comunicación más robusta, mejor manejo de errores y una experiencia de usuario mejorada.

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
front_php/
├── configuracion.php          # Configuración centralizada
├── api_procesamiento.php      # API para comunicación con Python
├── procesar_cartera.php       # Interfaz de procesamiento de cartera
├── descargar_resultado.php    # Descarga de archivos de resultados
├── estado_sistema.php         # Monitoreo del estado del sistema
└── dashboard.php              # Panel principal

PROVCA/
├── orquestador_principal.py   # Orquestador central de Python
├── config.py                  # Configuración de Python
├── logger.py                  # Sistema de logging
├── utilidades_cartera.py      # Utilidades compartidas
└── procesador_*.py            # Procesadores específicos
```

## ⚙️ Configuración

### 1. Configuración PHP (`configuracion.php`)

La configuración centralizada incluye:

- **Detección automática de Python**: Busca Python en múltiples ubicaciones
- **Configuración de directorios**: Rutas centralizadas para archivos y logs
- **Validación de permisos**: Verificación automática de permisos del sistema
- **Logging de actividad**: Registro de todas las operaciones

```php
// Detección automática de Python
define('PYTHON_EXE', detectarPython() ?: 'python');
define('PYTHON_DIR', __DIR__ . '/../PROVCA/');
define('ORQUESTADOR_PRINCIPAL', PYTHON_DIR . 'orquestador_principal.py');
```

### 2. Configuración de Directorios

```php
define('BASE_DIR', __DIR__ . '/../');
define('PROCESSED_DIR', BASE_DIR . 'resultados/');
define('TEMP_DIR', BASE_DIR . 'temp/');
define('LOGS_DIR', BASE_DIR . 'logs/');
define('PYTHON_LOGS_DIR', PYTHON_DIR . 'logs/');
```

## 🔄 Comunicación PHP-Python

### 1. Método Principal: Orquestador

El sistema utiliza el `orquestador_principal.py` como punto central de comunicación:

```php
function executePythonOrchestrator($tipo_procesamiento, $archivos = [], $opciones = []) {
    $cmd = PYTHON_EXE . ' ' . escapeshellarg(ORQUESTADOR_PRINCIPAL);
    $cmd .= ' --tipo ' . escapeshellarg($tipo_procesamiento);
    
    // Agregar archivos y opciones
    foreach ($archivos as $archivo) {
        $cmd .= ' --archivo ' . escapeshellarg($archivo);
    }
    
    $cmd .= ' --formato json 2>&1';
    
    $output = shell_exec($cmd);
    // Parsear respuesta JSON
    return json_decode($output, true);
}
```

### 2. API REST (`api_procesamiento.php`)

Endpoint para comunicación programática:

```bash
POST /api_procesamiento.php
Content-Type: application/json

{
    "tipo_procesamiento": "cartera",
    "archivos": ["archivo1.xlsx", "archivo2.xlsx"],
    "opciones": {
        "balance_file": "/ruta/balance.xlsx",
        "situacion_file": "/ruta/situacion.xlsx"
    }
}
```

## 📊 Monitoreo del Sistema

### 1. Estado del Sistema (`estado_sistema.php`)

Página web que muestra:

- **Configuración Python**: Versión, ruta, dependencias
- **Estado de archivos**: Existencia y permisos de archivos importantes
- **Estado de directorios**: Permisos y accesibilidad
- **Configuración PHP**: Límites y configuración del servidor
- **Estadísticas**: Archivos temporales, logs, etc.

### 2. Logging de Actividad

Todos los eventos se registran en `logs/php_activity.log`:

```json
{
    "timestamp": "2024-01-15 10:30:45",
    "action": "procesar_cartera_start",
    "user_ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "details": {
        "tipo": "cartera",
        "archivos": ["balance.xlsx", "situacion.xlsx"]
    }
}
```

## 🚀 Uso del Sistema

### 1. Procesamiento de Cartera

1. **Acceder al dashboard**: `http://localhost/front_php/dashboard.php`
2. **Seleccionar "Procesador de Cartera"**
3. **Subir archivos**: Balance, Situación y Focus
4. **Ejecutar procesamiento**: El sistema usa el orquestador Python
5. **Descargar resultados**: Archivos procesados disponibles para descarga

### 2. Monitoreo del Estado

1. **Acceder a "Estado del Sistema"** desde el dashboard
2. **Verificar configuración**: Python, dependencias, permisos
3. **Revisar errores**: Si hay problemas de configuración
4. **Actualizar estado**: Botón de actualización en tiempo real

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Python no detectado

**Síntomas**: Error "Python no está disponible"

**Solución**:
```bash
# Verificar instalación de Python
python --version
python3 --version

# Agregar Python al PATH si es necesario
# O actualizar la ruta en configuracion.php
```

#### 2. Dependencias Python faltantes

**Síntomas**: Error "Faltan dependencias de Python"

**Solución**:
```bash
cd PROVCA
pip install -r requirements.txt
```

#### 3. Permisos de directorios

**Síntomas**: Error "Directorio no tiene permisos de escritura"

**Solución**:
```bash
# Dar permisos de escritura
chmod 755 resultados/
chmod 755 temp/
chmod 755 logs/
```

#### 4. Orquestador no funciona

**Síntomas**: Error "No se encontró el orquestador principal"

**Solución**:
```bash
# Verificar que existe el archivo
ls -la PROVCA/orquestador_principal.py

# Verificar permisos de ejecución
chmod +x PROVCA/orquestador_principal.py

# Probar ejecución manual
python PROVCA/orquestador_principal.py --help
```

### Logs de Debugging

#### Logs PHP
- **Ubicación**: `logs/php_activity.log`
- **Contenido**: Todas las operaciones del sistema
- **Formato**: JSON estructurado

#### Logs Python
- **Ubicación**: `PROVCA/logs/`
- **Contenido**: Logs específicos de cada procesador
- **Formato**: Logs estructurados con timestamps

## 🔒 Seguridad

### Validaciones Implementadas

1. **Validación de archivos**: Tipo, tamaño, contenido
2. **Validación de rutas**: Solo acceso a directorios permitidos
3. **Sanitización de comandos**: Escape de parámetros shell
4. **Logging de actividad**: Registro de todas las operaciones
5. **Límites de tamaño**: Máximo 50MB por archivo

### Mejores Prácticas

- Mantener actualizadas las dependencias
- Revisar logs regularmente
- Monitorear el estado del sistema
- Hacer backup de configuraciones importantes

## 📈 Mejoras Futuras

### Funcionalidades Planificadas

1. **Procesamiento asíncrono**: Cola de trabajos en background
2. **API REST completa**: Endpoints para todas las operaciones
3. **Dashboard en tiempo real**: Actualizaciones automáticas
4. **Notificaciones**: Email/SMS al completar procesamiento
5. **Métricas avanzadas**: Estadísticas de uso y rendimiento

### Optimizaciones Técnicas

1. **Caché de resultados**: Evitar reprocesamiento
2. **Compresión de archivos**: Reducir tamaño de transferencia
3. **Validación incremental**: Verificar archivos en chunks
4. **Pool de conexiones**: Mejorar rendimiento de Python

## 📞 Soporte

### Información de Contacto

- **Sistema**: Grupo Planeta - Sistema de Análisis Financiero
- **Versión**: 2.0.1
- **Fecha**: Enero 2024

### Recursos Adicionales

- [README del Sistema Python](PROVCA/README.md)
- [Documentación de Configuración](PROVCA/config.py)
- [Guía de Troubleshooting](documentacion/TROUBLESHOOTING.md)

---

**Nota**: Este documento se actualiza regularmente. Para la versión más reciente, consulte el repositorio del proyecto.
