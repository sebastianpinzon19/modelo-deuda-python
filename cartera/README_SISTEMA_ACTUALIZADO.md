# Sistema de Procesamiento de Cartera - Grupo Planeta
## Versión 2.0.1 - Sistema PHP-Python Integrado

### 🎯 Estado Actual del Sistema

El sistema ha sido completamente refactorizado y modernizado. Ahora cuenta con:

#### ✅ **Python Backend (Completamente Funcional)**
- **Arquitectura Modular**: Código organizado en clases y módulos reutilizables
- **Orquestador Principal**: `orquestador_principal.py` - Punto central de control
- **Procesadores Disponibles**:
  - `ProcesadorCartera` - Procesamiento de cartera
  - `ProcesadorAcumulado` - Procesamiento de acumulado
  - `ProcesadorFormatoDeuda` - Formato de deuda
  - `ProcesadorAnticipos` - Procesamiento de anticipos
- **Sistema de Logging Avanzado**: Logs detallados y estructurados
- **Configuración Centralizada**: `config.py` con todas las configuraciones
- **Utilidades Compartidas**: `utilidades_cartera.py` con funciones comunes

#### ✅ **PHP Frontend (Completamente Integrado)**
- **Configuración Mejorada**: `configuracion.php` con detección automática de Python
- **Dashboard Moderno**: Interfaz web actualizada y funcional
- **API de Procesamiento**: `api_procesamiento.php` para comunicación programática
- **Sistema de Logs**: Registro de actividades y errores
- **Validación de Archivos**: Verificación automática de archivos subidos
- **Descarga de Resultados**: Sistema de descarga de archivos procesados

#### ✅ **Integración PHP-Python (Funcionando)**
- **Comunicación Bidireccional**: PHP llama a Python y recibe respuestas JSON
- **Manejo de Errores**: Sistema robusto de manejo de errores
- **Logs Unificados**: Logs tanto en PHP como en Python
- **Configuración Automática**: Detección automática de Python y configuración

### 🚀 Cómo Usar el Sistema

#### 1. **Acceso al Sistema**
```
http://localhost/modelo-deuda-python/cartera/
```

#### 2. **Test del Sistema**
```
http://localhost/modelo-deuda-python/cartera/test_sistema_simple.php
```
Este archivo te mostrará el estado completo del sistema.

#### 3. **Dashboard Principal**
```
http://localhost/modelo-deuda-python/cartera/front_php/dashboard.php
```

#### 4. **Procesamiento de Archivos**
- **Cartera**: `front_php/procesar_cartera.php`
- **Balance**: `front_php/procesar_balance.php`
- **Modelo de Deuda**: `front_php/modelo_deuda.php`
- **Estado del Sistema**: `front_php/estado_sistema.php`

### 📁 Estructura de Archivos

```
cartera/
├── PROVCA/                          # Backend Python
│   ├── orquestador_principal.py     # Orquestador central
│   ├── config.py                    # Configuración Python
│   ├── logger.py                    # Sistema de logging
│   ├── utilidades_cartera.py        # Utilidades compartidas
│   ├── procesador_cartera.py        # Procesador de cartera
│   ├── procesador_acumulado.py      # Procesador de acumulado
│   ├── procesador_formato_deuda.py  # Procesador de formato deuda
│   ├── procesador_anticipos.py      # Procesador de anticipos
│   ├── requirements.txt             # Dependencias Python
│   └── README.md                    # Documentación Python
├── front_php/                       # Frontend PHP
│   ├── configuracion.php            # Configuración PHP
│   ├── dashboard.php                # Dashboard principal
│   ├── procesar_cartera.php         # Procesamiento de cartera
│   ├── api_procesamiento.php        # API de procesamiento
│   ├── descargar_resultado.php      # Descarga de resultados
│   └── estado_sistema.php           # Estado del sistema
├── documentacion/                   # Documentación
│   ├── integracion_php_python.md    # Guía de integración
│   └── README_SISTEMA_COMPLETO.md   # Documentación completa
├── utilidades/                      # Utilidades del sistema
│   └── test_integracion.php         # Test de integración
├── logs/                           # Logs del sistema
├── resultados/                     # Archivos procesados
├── temp/                          # Archivos temporales
└── test_sistema_simple.php        # Test simple del sistema
```

### 🔧 Comandos Python Disponibles

#### Orquestador Principal
```bash
cd PROVCA

# Ver ayuda
python orquestador_principal.py --help

# Procesar archivo
python orquestador_principal.py procesar archivo.xlsx --tipo cartera

# Ver estadísticas
python orquestador_principal.py estadisticas

# Limpiar archivos antiguos
python orquestador_principal.py limpiar --dias 30

# Generar reporte
python orquestador_principal.py reporte
```

#### Procesadores Individuales
```bash
# Procesador de cartera
python procesador_cartera.py archivo.xlsx

# Procesador de acumulado
python procesador_acumulado.py archivo.xlsx

# Procesador de formato deuda
python procesador_formato_deuda.py archivo.xlsx

# Procesador de anticipos
python procesador_anticipos.py archivo.xlsx
```

### 📊 Tipos de Procesamiento Disponibles

1. **cartera** - Procesamiento completo de cartera (balance, situación, focus)
2. **acumulado** - Procesamiento de datos acumulados
3. **formato_deuda** - Formato específico de deuda
4. **anticipos** - Procesamiento de anticipos

### 🔍 Monitoreo y Logs

#### Logs PHP
- Ubicación: `logs/`
- Archivos: `php_activity.log`, `php_errors.log`

#### Logs Python
- Ubicación: `PROVCA/logs/`
- Archivos: `procesamiento.log`, `orquestador.log`

#### Estado del Sistema
- URL: `front_php/estado_sistema.php`
- Muestra: Configuración, Python, directorios, permisos

### 🛠️ Solución de Problemas

#### 1. **Python no detectado**
- Verificar que Python esté instalado
- Verificar que esté en el PATH
- Revisar `configuracion.php` para rutas personalizadas

#### 2. **Errores de permisos**
- Verificar permisos de escritura en `logs/`, `temp/`, `resultados/`
- Ejecutar como administrador si es necesario

#### 3. **Archivos no encontrados**
- Verificar que todos los archivos Python estén en `PROVCA/`
- Verificar que las dependencias estén instaladas: `pip install -r requirements.txt`

#### 4. **Errores de procesamiento**
- Revisar logs en `logs/` y `PROVCA/logs/`
- Verificar formato de archivos de entrada
- Usar `test_sistema_simple.php` para diagnóstico

### 📈 Próximas Mejoras

#### Procesadores Pendientes
- `ProcesadorBalanceCompleto`
- `ProcesadorBalanceEspecifico`
- `ProcesadorSituacionEspecifico`
- `ProcesadorFocusEspecifico`

#### Funcionalidades Futuras
- Interfaz web más avanzada
- Reportes automáticos
- Integración con bases de datos
- API REST completa

### 📞 Soporte

Para reportar problemas o solicitar mejoras:
1. Revisar los logs del sistema
2. Usar `test_sistema_simple.php` para diagnóstico
3. Verificar la documentación en `documentacion/`

---

**Sistema de Cartera Grupo Planeta v2.0.1**  
*Desarrollado con Python 3.x y PHP 7.x+*
