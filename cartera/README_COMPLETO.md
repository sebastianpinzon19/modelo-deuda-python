# 🏢 SISTEMA FORMATO DEUDA - GRUPO PLANETA

## 📋 ÍNDICE
1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Funcionalidades Principales](#funcionalidades-principales)
5. [Scripts Python](#scripts-python)
6. [Interfaces PHP](#interfaces-php)
7. [Pruebas del Sistema](#pruebas-del-sistema)
8. [Guía de Uso](#guía-de-uso)
9. [Troubleshooting](#troubleshooting)
10. [Documentación Técnica](#documentación-técnica)

---

## 🎯 DESCRIPCIÓN GENERAL

El **Sistema Formato Deuda** es una plataforma integral desarrollada para el área de cartera de Grupo Planeta, diseñada para procesar y transformar datos financieros del sistema Pisa en reportes estructurados requeridos por la casa matriz.

### 🎯 Objetivos
- ✅ Procesar archivos de provisión (PROVCA) y anticipos (ANTICI)
- ✅ Generar formato de deuda completo con múltiples hojas Excel
- ✅ Aplicar cálculos financieros complejos y validaciones
- ✅ Integrar datos de balance, situación y focus
- ✅ Proporcionar interfaz web moderna y responsive

### 🏗️ Tecnologías Utilizadas
- **Backend**: Python 3.13 con Pandas, NumPy, OpenPyXL
- **Frontend**: PHP 8.0+ con HTML5, CSS3, JavaScript
- **Base de Datos**: Archivos CSV/Excel (sistema de archivos)
- **Servidor Web**: WAMP/XAMPP

---

## 🏛️ ARQUITECTURA DEL SISTEMA

```
📁 cartera/
├── 📁 PROVCA/                    # Scripts Python principales
│   ├── procesador_formato_deuda.py      # Procesador principal
│   ├── procesador_cartera.py            # Procesamiento de provisión
│   ├── procesador_anticipos.py          # Procesamiento de anticipos
│   ├── procesador_balance_completo.py   # Procesamiento de balance
│   ├── utilidades_cartera.py            # Funciones utilitarias
│   └── requirements.txt                 # Dependencias Python
├── 📁 front_php/                 # Interfaces web PHP
│   ├── index.php                        # Dashboard principal
│   ├── procesar_formato_deuda.php       # Interfaz formato deuda
│   ├── procesar_balance.php             # Interfaz balance
│   ├── procesar.php                     # Procesador general
│   └── styles.css                       # Estilos CSS
├── 📁 resultados/                # Archivos generados
├── 📁 temp/                      # Archivos temporales
└── 📁 AN/                        # Documentos de análisis
```

---

## ⚙️ INSTALACIÓN Y CONFIGURACIÓN

### 📋 Requisitos Previos
- **Python 3.13+** con pip
- **PHP 8.0+** con extensiones habilitadas
- **Servidor web** (WAMP/XAMPP/Apache)
- **Navegador web** moderno

### 🔧 Instalación

#### 1. Clonar/Descargar el Proyecto
```bash
# Navegar al directorio del servidor web
cd C:\wamp64\www\
# Descargar el proyecto en la carpeta 'cartera'
```

#### 2. Instalar Dependencias Python
```bash
cd cartera/PROVCA
pip install -r requirements.txt
```

#### 3. Configurar Permisos
```bash
# Crear directorios necesarios
mkdir resultados
mkdir temp
# Asignar permisos de escritura
chmod 755 resultados temp
```

#### 4. Verificar Configuración
```bash
# Ejecutar pruebas del sistema
cd PROVCA
python pruebas_simples.py
```

### ⚙️ Configuración PHP
Editar `front_php/configuracion.php`:
```php
// Ruta al ejecutable de Python
$python_path = 'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe';

// Configuraciones de archivos
$max_file_size = 100 * 1024 * 1024; // 100MB
$allowed_extensions = ['csv', 'xlsx', 'xls'];
```

---

## 🚀 FUNCIONALIDADES PRINCIPALES

### 📊 1. Formato Deuda Completo
**Archivo**: `procesar_formato_deuda.php`

**Funcionalidades**:
- ✅ Procesamiento de archivo de provisión (PROVCA)
- ✅ Procesamiento de archivo de anticipos (ANTICI)
- ✅ Generación de modelo de deuda con hojas:
  - **PESOS**: Deuda en pesos colombianos
  - **DIVISAS**: Deuda en divisas (USD, EUR)
  - **VENCIMIENTOS**: Análisis de vencimientos por rango
- ✅ Integración de archivos adicionales (balance, situación, focus)
- ✅ Cálculos financieros complejos
- ✅ Validaciones de datos
- ✅ Formato colombiano de números

### 📈 2. Balance Completo
**Archivo**: `procesar_balance.php`

**Funcionalidades**:
- ✅ Procesamiento de archivo de balance
- ✅ Procesamiento de archivo de situación
- ✅ Procesamiento de archivo focus
- ✅ Generación de reporte consolidado
- ✅ Análisis financiero detallado

### 🔄 3. Procesador General
**Archivo**: `procesar.php`

**Funcionalidades**:
- ✅ Procesamiento flexible de cartera
- ✅ Procesamiento de anticipos
- ✅ Opciones de configuración
- ✅ Validaciones automáticas

### 📊 4. Dashboard Principal
**Archivo**: `index.php`

**Funcionalidades**:
- ✅ Vista general del sistema
- ✅ Estado de componentes
- ✅ Enlaces rápidos a funcionalidades
- ✅ Información del sistema
- ✅ Documentación integrada

---

## 🐍 SCRIPTS PYTHON

### 📁 PROVCA/procesador_formato_deuda.py
**Procesador principal del sistema**

#### Funciones Principales:
```python
def procesar_formato_deuda_completo(
    archivo_provision, archivo_anticipos, 
    archivo_balance=None, archivo_situacion=None, 
    archivo_focus=None, fecha_cierre_str=None, 
    output_path=None
):
    """
    Función principal que orquesta todo el proceso de formato deuda
    """
```

#### Características:
- ✅ Procesamiento completo según especificaciones Word
- ✅ Integración de múltiples fuentes de datos
- ✅ Generación de Excel multi-hoja
- ✅ Validaciones y cálculos financieros
- ✅ Manejo de errores robusto

### 📁 PROVCA/procesador_cartera.py
**Procesamiento de archivos de provisión**

#### Funciones Principales:
```python
def procesar_archivo_provision(archivo_provision, fecha_cierre_str=None):
    """Procesa archivo de provisión con 15 pasos detallados"""

def limpiar_y_validar_datos(df):
    """Limpia y valida datos del DataFrame"""

def calcular_dias_vencidos(df, fecha_cierre_str=None):
    """Calcula días vencidos y por vencer"""

def calcular_vencimientos_por_rango(df):
    """Calcula vencimientos por rangos de días"""
```

#### Proceso de 15 Pasos:
1. **Renombrar campos** según mapeo oficial
2. **Eliminar columna PCIMCO**
3. **Eliminar empresa PL30** con valor -614.000
4. **Unificar nombres** de clientes
5. **Convertir fechas** y crear columnas separadas
6. **Calcular días vencidos** y por vencer
7. **Calcular saldos** y dotaciones
8. **Crear vencimientos históricos** (6 meses)
9. **Calcular vencimiento 180 días**
10. **Calcular valores por vencer** (3 meses)
11. **Calcular mayor a 90 días**
12. **Validar suma** de mora + por vencer = saldo
13. **Crear columnas** de vencimientos por rango
14. **Crear columna** de deuda incobrable
15. **Aplicar formato** colombiano

### 📁 PROVCA/procesador_anticipos.py
**Procesamiento de archivos de anticipos**

#### Funciones Principales:
```python
def procesar_anticipos(input_path, output_path=None, fecha_cierre_str=None):
    """Procesa archivo de anticipos completo"""

def limpiar_y_validar_datos(df):
    """Limpia y valida datos de anticipos"""

def calcular_saldos_anticipos(df):
    """Calcula saldos y dotaciones de anticipos"""
```

#### Características:
- ✅ Procesamiento específico de anticipos
- ✅ Multiplicación de valores por -1
- ✅ Cálculos de vencimientos
- ✅ Validaciones de negocio

### 📁 PROVCA/procesador_balance_completo.py
**Procesamiento de archivos de balance**

#### Funciones Principales:
```python
def procesar_balance_completo(
    archivo_balance, archivo_situacion, archivo_focus, 
    output_path=None
):
    """Procesa los tres archivos de balance simultáneamente"""
```

#### Características:
- ✅ Procesamiento simultáneo de 3 archivos
- ✅ Extracción de datos específicos
- ✅ Consolidación de información
- ✅ Generación de reportes

### 📁 PROVCA/utilidades_cartera.py
**Funciones utilitarias compartidas**

#### Funciones Principales:
```python
def convertir_fecha(fecha_str):
    """Convierte fechas de múltiples formatos"""

def convertir_valor(valor_str):
    """Convierte valores numéricos con formato colombiano"""

def formatear_numero_colombiano(valor, es_porcentaje=False):
    """Aplica formato colombiano a números"""

def aplicar_formato_colombiano_dataframe(df, columnas_numericas=None):
    """Aplica formato colombiano a DataFrames completos"""
```

---

## 🌐 INTERFACES PHP

### 📁 front_php/index.php
**Dashboard principal del sistema**

#### Características:
- ✅ Interfaz moderna y responsive
- ✅ Estado del sistema en tiempo real
- ✅ Enlaces rápidos a funcionalidades
- ✅ Información técnica del sistema
- ✅ Documentación integrada

#### Componentes:
```php
// Verificación de estado del sistema
$python_path = 'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe';
$python_ok = file_exists($python_path);
$directorios_ok = is_dir('resultados') && is_dir('temp');
$permisos_ok = is_writable('.');
```

### 📁 front_php/procesar_formato_deuda.php
**Interfaz para formato deuda completo**

#### Funcionalidades:
- ✅ Upload de archivos múltiples
- ✅ Validación de archivos
- ✅ Configuración de fecha de cierre
- ✅ Ejecución de procesamiento Python
- ✅ Visualización de resultados
- ✅ Descarga de archivos generados

#### Estructura:
```php
// Configuración
$python_path = 'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe';
$python_script = 'PROVCA/procesador_formato_deuda.py';

// Validación de archivos
$archivos_requeridos = ['provision', 'anticipos'];
$archivos_opcionales = ['balance', 'situacion', 'focus'];

// Ejecución Python
$comando = "\"$python_path\" \"$python_script\" \"{$archivos_subidos['provision']}\" \"{$archivos_subidos['anticipos']}\"";
```

### 📁 front_php/procesar_balance.php
**Interfaz para procesamiento de balance**

#### Funcionalidades:
- ✅ Upload de archivos de balance
- ✅ Procesamiento simultáneo
- ✅ Generación de reportes
- ✅ Validaciones automáticas

### 📁 front_php/procesar.php
**Procesador general**

#### Funcionalidades:
- ✅ Selección de tipo de procesamiento
- ✅ Upload de archivos
- ✅ Configuraciones flexibles
- ✅ Resultados dinámicos

### 📁 front_php/configuracion.php
**Configuración centralizada**

#### Funciones:
```php
function verificar_directorios() {
    // Verifica existencia y permisos de directorios
}

function limpiar_archivos_temporales() {
    // Limpia archivos temporales
}

function validar_archivo_subido($archivo) {
    // Valida archivos subidos
}

function ejecutar_script_python($comando) {
    // Ejecuta scripts Python de forma segura
}
```

---

## 🧪 PRUEBAS DEL SISTEMA

### 📁 PROVCA/pruebas_simples.py
**Script de pruebas básicas**

#### Pruebas Incluidas:
1. **Estructura de archivos** - Verifica que existan todos los archivos
2. **Dependencias** - Verifica instalación de pandas, numpy, openpyxl
3. **Importaciones** - Verifica que se puedan importar todos los módulos
4. **Funciones utilidades** - Prueba funciones básicas
5. **DataFrames** - Prueba manipulación de datos
6. **Lectura CSV** - Verifica lectura de archivos de prueba

#### Ejecución:
```bash
cd PROVCA
python pruebas_simples.py
```

#### Resultado Esperado:
```
🎉 ¡TODAS LAS PRUEBAS PASARON!
✅ El sistema está listo para funcionar
```

### 📁 PROVCA/ejecutar_pruebas.py
**Script de pruebas completas (avanzado)**

#### Pruebas Incluidas:
1. **Utilidades completas** - Todas las funciones de utilidades
2. **Procesamiento provisión** - Procesamiento completo de provisión
3. **Procesamiento anticipos** - Procesamiento completo de anticipos
4. **Formato deuda completo** - Procesamiento integral
5. **Lectura Excel** - Verificación de archivos generados

---

## 📖 GUÍA DE USO

### 🚀 Inicio Rápido

#### 1. Acceder al Sistema
```
http://localhost/cartera/
```

#### 2. Seleccionar Funcionalidad
- **Formato Deuda Completo**: Para procesamiento principal
- **Balance Completo**: Para archivos de balance
- **Procesador General**: Para procesamiento flexible

#### 3. Subir Archivos
- **Archivos requeridos**: Provisión (PROVCA) y Anticipos (ANTICI)
- **Archivos opcionales**: Balance, Situación, Focus
- **Fecha de cierre**: Configurable (opcional)

#### 4. Procesar y Descargar
- Hacer clic en "Procesar"
- Esperar procesamiento
- Descargar archivo Excel generado

### 📊 Formato Deuda Completo

#### Archivos de Entrada:
1. **PROVCA.csv** - Archivo de provisión del sistema Pisa
2. **ANTICI.csv** - Archivo de anticipos del sistema Pisa
3. **Balance.xlsx** - Archivo de balance (opcional)
4. **Situacion.xlsx** - Archivo de situación (opcional)
5. **Focus.xlsx** - Archivo focus (opcional)

#### Archivo de Salida:
- **FORMATO_DEUDA_COMPLETO.xlsx** con hojas:
  - **PESOS**: Deuda en pesos colombianos
  - **DIVISAS**: Deuda en divisas
  - **VENCIMIENTOS**: Análisis de vencimientos

### 📈 Balance Completo

#### Archivos de Entrada:
1. **Balance.xlsx** - Archivo principal de balance
2. **Situacion.xlsx** - Archivo de situación
3. **Focus.xlsx** - Archivo focus

#### Archivo de Salida:
- **BALANCE_COMPLETO.xlsx** con análisis consolidado

---

## 🔧 TROUBLESHOOTING

### ❌ Problemas Comunes

#### 1. Error: "Python no encontrado"
**Solución**:
```php
// Verificar ruta en configuracion.php
$python_path = 'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe';
```

#### 2. Error: "Módulo no encontrado"
**Solución**:
```bash
cd PROVCA
pip install -r requirements.txt
```

#### 3. Error: "Permisos denegados"
**Solución**:
```bash
# Verificar permisos de directorios
chmod 755 resultados temp
```

#### 4. Error: "Archivo no válido"
**Solución**:
- Verificar formato de archivo (CSV/Excel)
- Verificar tamaño máximo (100MB)
- Verificar codificación (UTF-8)

#### 5. Error: "Procesamiento falló"
**Solución**:
```bash
# Ejecutar pruebas para diagnosticar
cd PROVCA
python pruebas_simples.py
```

### 🔍 Diagnóstico

#### Verificar Estado del Sistema:
1. Acceder a `http://localhost/cartera/`
2. Revisar "Estado del Sistema"
3. Verificar todos los componentes

#### Logs de Error:
- Revisar logs de PHP en `C:\wamp64\logs\`
- Revisar logs de Python en consola
- Verificar permisos de archivos

---

## 📚 DOCUMENTACIÓN TÉCNICA

### 📁 SISTEMA_FORMATO_DEUDA_COMPLETO.md
**Documentación completa del sistema principal**

### 📁 PROVCA/README_INTEGRACION.md
**Documentación técnica de integración Python-PHP**

### 📁 AN/RESUMEN_DOCUMENTOS_AN.md
**Análisis de documentos de especificación**

### 📁 front_php/README.md
**Documentación de interfaces PHP**

### 📁 README_BALANCE.md
**Documentación específica de balance**

### 📁 README_CSS.md
**Documentación de estilos CSS**

---

## 🎯 CARACTERÍSTICAS TÉCNICAS

### 🔒 Seguridad
- ✅ Validación de archivos subidos
- ✅ Sanitización de entradas
- ✅ Ejecución segura de comandos Python
- ✅ Limpieza automática de archivos temporales

### ⚡ Rendimiento
- ✅ Procesamiento optimizado con Pandas
- ✅ Manejo eficiente de memoria
- ✅ Procesamiento por lotes
- ✅ Caché de resultados

### 🔄 Mantenibilidad
- ✅ Código modular y reutilizable
- ✅ Documentación completa
- ✅ Pruebas automatizadas
- ✅ Configuración centralizada

### 📱 Usabilidad
- ✅ Interfaz responsive
- ✅ Feedback visual en tiempo real
- ✅ Manejo de errores amigable
- ✅ Guías de uso integradas

---

## 📞 SOPORTE

### 🆘 Contacto
- **Desarrollador**: Sistema de Procesamiento de Cartera
- **Empresa**: Grupo Planeta
- **Versión**: 2.0
- **Fecha**: Agosto 2025

### 📋 Checklist de Verificación
- [ ] Python 3.13+ instalado
- [ ] Dependencias Python instaladas
- [ ] PHP 8.0+ configurado
- [ ] Servidor web funcionando
- [ ] Permisos de directorios correctos
- [ ] Pruebas del sistema pasando
- [ ] Archivos de configuración actualizados

### 🔄 Actualizaciones
- **v2.0**: Sistema completo de formato deuda
- **v1.5**: Integración Python-PHP
- **v1.0**: Procesadores básicos

---

## 📄 LICENCIA

Este sistema es propiedad de **Grupo Planeta** y está diseñado específicamente para el procesamiento de datos financieros del área de cartera.

**© 2025 Grupo Planeta. Todos los derechos reservados.**

---

*Documentación generada automáticamente - Sistema Formato Deuda v2.0* 