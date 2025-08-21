# RESUMEN EJECUTIVO - MODELO DE DEUDA

## 🎯 OBJETIVO
El Sistema de Modelo de Deuda es una solución automatizada que procesa archivos de provisión y anticipos para generar reportes consolidados de deuda según el formato especificado en FORMATO DEUDA.docx.

## 🚀 FUNCIONALIDADES PRINCIPALES

### 1. Procesamiento Automatizado
- **Filtrado inteligente** de líneas de venta según criterios predefinidos
- **Integración automática** de archivos de provisión y anticipos
- **Conversión automática** de divisas usando TRM configurable

### 2. Generación de Reportes
- **Hoja PESOS:** Líneas en pesos colombianos + anticipos
- **Hoja DIVISAS:** Líneas en dólares/euros con conversión TRM
- **Hoja VENCIMIENTO:** Consolidado por cliente con totales por moneda

### 3. Gestión de TRM
- **Configuración manual** de tasas de cambio
- **Almacenamiento automático** para reutilización
- **Validación de datos** para evitar errores de entrada

## 📊 LÍNEAS DE VENTA PROCESADAS

### Pesos Colombianos (25 líneas)
- **CT80:** TINTA-CLUB DEL LIBRO SAS
- **ED41-47:** PLANETA CREDITO, VENTA DIGITAL, EVENTOS
- **PL10-69:** LIBRERIAS, MARKETING, DISTRIBUCION, VENTAS ESPECIALES

### Divisas (4 líneas)
- **PL11, PL18, PL57:** Dólares (TERCEROS, COLOMBIANA, AULA PLANETA)
- **PL41:** Euros (COLOMBIANA TERCEROS)

## 🔧 ARQUITECTURA TÉCNICA

### Tecnologías Utilizadas
- **Python 3.7+** - Lenguaje principal
- **Pandas** - Procesamiento de datos
- **XlsxWriter** - Generación de Excel
- **OpenPyXL** - Formateo avanzado

### Estructura del Sistema
```
modelo_deuda.py          # Motor principal del sistema
trm_config.py            # Gestión de tasas de cambio
utilidades.py            # Funciones auxiliares
ejecutar_modelo_deuda.py # Interfaz simplificada
ejecutar_modelo_deuda.bat # Script Windows
```

## 📁 FLUJO DE TRABAJO

### Entrada
1. **Archivo de Provisión** (.xlsx) - Datos de cartera procesados
2. **Archivo de Anticipos** (.xlsx) - Anticipos procesados
3. **TRM Dólar y Euro** - Tasas de cambio del mes anterior

### Procesamiento
1. **Filtrado** por líneas de venta específicas
2. **Conversión** de divisas a pesos colombianos
3. **Integración** de anticipos en estructura unificada
4. **Agrupación** por cliente y moneda

### Salida
1. **Archivo Excel** con 3 hojas especializadas
2. **Formato colombiano** (puntos miles, comas decimales)
3. **Totales automáticos** por moneda y consolidados

## 💰 CARACTERÍSTICAS FINANCIERAS

### Conversión de Monedas
- **Automática** según TRM configurada
- **Precisa** con redondeo a pesos enteros
- **Trazable** con columnas de conversión

### Consolidación de Saldos
- **Por cliente** y línea de negocio
- **Por moneda** con totales separados
- **Por vencimiento** en rangos de días

## 🎨 INTERFAZ DE USUARIO

### Opciones de Ejecución
1. **Línea de comandos** - Para automatización
2. **Interactiva** - Para uso manual
3. **Windows Batch** - Para usuarios Windows

### Validaciones
- **Archivos de entrada** - Existencia y formato
- **TRM** - Valores numéricos válidos
- **Dependencias** - Verificación automática

## 📈 BENEFICIOS DEL SISTEMA

### Eficiencia
- **Reducción de tiempo** de procesamiento manual
- **Eliminación de errores** de cálculo manual
- **Consistencia** en formato de salida

### Flexibilidad
- **Configuración TRM** personalizable
- **Múltiples formatos** de entrada
- **Adaptación automática** a estructuras de datos

### Trazabilidad
- **Logs detallados** de procesamiento
- **Validación** de datos de entrada
- **Formato estándar** de salida

## 🔍 CASOS DE USO

### Mensual
- **Cierre contable** con TRM actualizada
- **Reportes de deuda** para stakeholders
- **Análisis de cartera** por línea de negocio

### Trimestral
- **Revisión de tendencias** de deuda
- **Análisis de vencimientos** por moneda
- **Consolidación** para reportes ejecutivos

### Anual
- **Auditoría** de cartera de deuda
- **Planificación** de cobranzas
- **Análisis estratégico** de líneas de negocio

## 🚨 CONSIDERACIONES IMPORTANTES

### Requisitos Previos
- **Archivos procesados** - No procesa archivos raw
- **TRM actualizada** - Del último día del mes anterior
- **Dependencias Python** - Instaladas y verificadas

### Limitaciones
- **Formato Excel** - Solo archivos .xlsx
- **Estructura específica** - Requiere campos predefinidos
- **Monedas soportadas** - Solo COP, USD, EUR

## 📋 PLAN DE IMPLEMENTACIÓN

### Fase 1: Preparación
- [x] Desarrollo del sistema base
- [x] Documentación técnica
- [x] Scripts de ejecución

### Fase 2: Pruebas
- [ ] Validación con datos reales
- [ ] Pruebas de rendimiento
- [ ] Validación de formatos

### Fase 3: Despliegue
- [ ] Instalación en ambiente de producción
- [ ] Capacitación de usuarios
- [ ] Monitoreo y soporte

## 🎯 PRÓXIMOS PASOS

1. **Validar** archivos de entrada existentes
2. **Configurar** TRM iniciales
3. **Ejecutar** primera prueba del sistema
4. **Ajustar** parámetros según resultados
5. **Implementar** en flujo de trabajo regular

---

**Desarrollado por:** Sistema Python de Modelo de Deuda  
**Versión:** 2.0.0  
**Fecha:** Agosto 2025  
**Estado:** Listo para implementación
