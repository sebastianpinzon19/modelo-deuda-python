# 🚀 Sistema de Procesamiento de Cartera - Grupo Planeta

## 📋 Descripción General

Este sistema implementa un procesamiento completo de archivos financieros según las reglas de negocio específicas del Grupo Planeta. El sistema está compuesto por **7 procesadores específicos** y **1 unificador final**.

## 🏗️ Arquitectura del Sistema

### **7 Procesadores Específicos:**

1. **`procesador_balance_especifico.py`** - Procesa archivo BALANCE
   - Suma la columna "Saldo AAF variación" para cuentas específicas
   - Cuentas: 43001, 0080.43002.20, 0080.43002.21, 0080.43002.15, 0080.43002.28, 0080.43002.31, 0080.43002.63, 43008, 43042

2. **`procesador_situacion_especifico.py`** - Procesa archivo SITUACIÓN
   - Extrae el valor de TOTAL 01010 de la columna SALDOS MES

3. **`procesador_focus_especifico.py`** - Procesa archivo FOCUS
   - Toma datos de vencimientos del archivo número 2 (formato España)
   - Procesa vencimientos por rangos de días (30, 60, 90, 180, 365)

4. **`procesador_dotacion_mes.py`** - Calcula dotación del mes
   - Fórmula: Interco RESTO - Dotaciones Acumuladas (Inicial) - Provisión del mes

5. **`procesador_acumulado.py`** - Procesa acumulados
   - Copia fórmulas de B54 a F54 del archivo formato acumulado Focus prueba
   - Procesa datos específicos: Cobros, Facturación, Vencidos, Provision, Dotacion

6. **`procesador_tipos_cambio.py`** - Actualiza tipos de cambio
   - Cambia el mes de cierre y actualiza tasas de cambio
   - Maneja USD/COP, EUR/COP, USD/EUR, etc.

7. **`procesador_anticipos.py`** - Procesa anticipos (existente)
   - Procesamiento de archivos de anticipos con análisis detallado

### **1 Unificador Final:**

8. **`unificador_final.py`** - Une todos los resultados
   - Crea un Excel con hojas separadas para cada procesamiento
   - Incluye hoja de RESUMEN y hoja de FORMULAS
   - Aplica fórmulas de negocio cruzadas

## 📁 Estructura de Archivos

```
PROVCA/
├── utilidades_cartera.py              # Funciones auxiliares
├── procesador_balance_especifico.py   # Balance específico
├── procesador_situacion_especifico.py # Situación específico
├── procesador_focus_especifico.py     # Focus específico
├── procesador_dotacion_mes.py         # Dotación del mes
├── procesador_acumulado.py            # Acumulado
├── procesador_tipos_cambio.py         # Tipos de cambio
├── procesador_anticipos.py            # Anticipos
├── unificador_final.py                # Unificador final
├── prueba_sistema_completo.py         # Prueba completa
└── pruebas_simples.py                 # Pruebas básicas
```

## 🔧 Fórmulas de Negocio Implementadas

### **Fórmulas Principales:**

1. **Deuda bruta NO Grupo (Inicial) = Deuda bruta NO Grupo (Final)**
2. **- Dotaciones Acumuladas (Inicial) = '+/- Provisión acumulada (Final)**
3. **Cobro de mes - Vencida = Deuda bruta NO Grupo (Inicial) Vencidas - Total vencido de 60 días en adelante / 1000**
4. **Cobro mes - Total Deuda = COBROS SITUACION (SALDO MES) / -1000**
5. **Cobros del mes - No Vencida = H15-D15**
6. **+/- Vencidos en el mes – vencido = VENCIDO MES 30 días signo positivo**
7. **+/- Vencidos en el mes – No vencido = D17**
8. **'+/- Vencidos en el mes – Total deuda = D17 - F17**
9. **+ Facturación del mes – vencida = 0**
10. **+ Facturación del mes – no vencida = +Q22-H22**
11. **Dotación del mes = Interco RESTO - Dotaciones Acumuladas (Inicial) - Provisión del mes**

## 🚀 Cómo Usar el Sistema

### **1. Procesamiento Individual:**

```bash
# Procesar Balance Específico
python procesador_balance_especifico.py archivo_balance.xlsx

# Procesar Situación Específico
python procesador_situacion_especifico.py archivo_situacion.xlsx

# Procesar Focus Específico
python procesador_focus_especifico.py archivo_focus.xlsx

# Procesar Dotación del Mes
python procesador_dotacion_mes.py archivo_dotacion.xlsx

# Procesar Acumulado
python procesador_acumulado.py archivo_acumulado.xlsx

# Procesar Tipos de Cambio
python procesador_tipos_cambio.py archivo_tipos_cambio.xlsx
```

### **2. Unificación Final:**

```bash
# Unificar todos los resultados
python unificador_final.py
```

### **3. Prueba Completa del Sistema:**

```bash
# Ejecutar prueba completa
python prueba_sistema_completo.py
```

## 📊 Archivos de Salida

### **Archivos Individuales:**
- `balance_especifico_procesado_YYYYMMDD_HHMMSS.xlsx`
- `situacion_especifico_procesado_YYYYMMDD_HHMMSS.xlsx`
- `focus_especifico_procesado_YYYYMMDD_HHMMSS.xlsx`
- `dotacion_mes_procesado_YYYYMMDD_HHMMSS.xlsx`
- `acumulado_procesado_YYYYMMDD_HHMMSS.xlsx`
- `tipos_cambio_procesado_YYYYMMDD_HHMMSS.xlsx`

### **Archivo Final Unificado:**
- `reporte_final_unificado_YYYYMMDD_HHMMSS.xlsx`

**Contenido del archivo final:**
- Hoja **RESUMEN**: Estadísticas generales de todos los procesamientos
- Hoja **BALANCE**: Resultados del procesamiento de balance
- Hoja **SITUACION**: Resultados del procesamiento de situación
- Hoja **FOCUS**: Resultados del procesamiento de focus
- Hoja **DOTACION MES**: Resultados del procesamiento de dotación
- Hoja **ACUMULADO**: Resultados del procesamiento de acumulado
- Hoja **TIPOS CAMBIO**: Resultados del procesamiento de tipos de cambio
- Hoja **FORMULAS**: Cálculos cruzados según fórmulas de negocio

## 🔍 Validaciones y Manejo de Errores

### **Validaciones Implementadas:**
- ✅ Verificación de existencia de archivos
- ✅ Validación de formatos de archivo (.xlsx, .xls, .csv)
- ✅ Verificación de columnas requeridas
- ✅ Manejo de errores de Python
- ✅ Logging detallado de operaciones
- ✅ Limpieza automática de archivos temporales

### **Manejo de Errores:**
- **Archivo no encontrado**: Error descriptivo con sugerencias
- **Columnas faltantes**: Lista de columnas requeridas
- **Datos inválidos**: Conversión automática cuando es posible
- **Errores de Python**: Captura y reporte detallado

## 📈 Logging y Monitoreo

### **Archivos de Log:**
- `logs/sistema.log`: Log general del sistema
- `logs/errores.log`: Log específico de errores
- `logs/procesamiento.log`: Log de procesamiento Python

### **Información Registrada:**
- Fecha y hora de procesamiento
- Archivo original y procesado
- Estadísticas de procesamiento
- Errores y advertencias
- Tiempo de ejecución

## 🛠️ Requisitos del Sistema

### **Python:**
- Python 3.7 o superior
- pandas
- numpy
- openpyxl
- logging

### **PHP:**
- PHP 7.4 o superior
- Extensión fileinfo
- Permisos de escritura en directorios

### **Sistema:**
- Espacio en disco: 100MB mínimo
- Memoria RAM: 512MB recomendado
- Permisos de ejecución en scripts Python

## 🔧 Configuración

### **Variables de Entorno:**
```php
// En config.php
define('DIR_TEMP', 'temp/');
define('DIR_RESULTADOS', 'resultados/');
define('DIR_LOGS', 'logs/');
define('DIR_PYTHON', 'PROVCA/');
```

### **Scripts Python:**
```php
define('SCRIPT_BALANCE_ESPECIFICO', DIR_PYTHON . 'procesador_balance_especifico.py');
define('SCRIPT_SITUACION_ESPECIFICO', DIR_PYTHON . 'procesador_situacion_especifico.py');
// ... etc
```

## 📞 Soporte y Mantenimiento

### **Para Reportar Problemas:**
1. Revisar logs en `logs/errores.log`
2. Ejecutar `python prueba_sistema_completo.py`
3. Verificar que Python esté instalado correctamente
4. Confirmar permisos de archivos y directorios

### **Mantenimiento Regular:**
- Limpieza automática de archivos temporales (7 días)
- Rotación de logs (30 días)
- Verificación de espacio en disco
- Actualización de tipos de cambio

## 🎯 Resultados Esperados

### **Al finalizar el procesamiento:**
1. ✅ Todos los archivos individuales procesados
2. ✅ Archivo Excel final con hojas separadas
3. ✅ Fórmulas de negocio aplicadas correctamente
4. ✅ Logs detallados de todas las operaciones
5. ✅ Limpieza automática de archivos temporales

---

**Desarrollado para Grupo Planeta**  
**Versión:** 2.0  
**Fecha:** 2025  
**Mantenido por:** Equipo de Desarrollo 