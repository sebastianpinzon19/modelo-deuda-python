# RESUMEN DE DOCUMENTOS AN - GRUPO PLANETA

## 📋 DOCUMENTOS ENCONTRADOS

### 📄 Documentos de Formato (Word)
1. **FORMATO DEUDA.docx** (37.4 KB)
   - Documento de Word con especificaciones de formato para deuda
   - Probablemente contiene las reglas y estructura para el procesamiento de datos de deuda

2. **FORMATO DEUDA 1.docx** (36.7 KB)
   - Documento de Word similar al anterior
   - Posiblemente una versión actualizada o alternativa del formato

### 📊 Archivos de Datos (Excel)

#### 1. **06 BALANCE COLOMBIANA JUNIO.xlsx** (169.8 KB)
**Propósito**: Archivo principal de balance contable de Colombiana para junio de 2025

**Estructura**:
- **Filas**: 3,151 registros
- **Columnas**: 13 campos
- **Tipo**: Balance contable con saldos y ajustes

**Columnas principales**:
1. `Número cuenta` - Código de cuenta contable
2. `Descripción cuenta` - Nombre de la cuenta
3. `Libro mayor Saldo periodo` - Saldo del período actual
4. `AJUSTES DE GESTION Saldo periodo` - Ajustes de gestión del período
5. `Saldo periodo desviación` - Desviaciones del período
6. `Libro mayor Saldo` - Saldo actual del libro mayor
7. `AJUSTES DE GESTION Saldo` - Ajustes de gestión actuales
8. `Saldo AAF variación` - Variación del saldo AAF
9. `Nivel detalle` - Nivel de detalle de la cuenta
10. `Cd edición contzn` - Código de edición contable

**Características**:
- Contiene datos financieros con valores desde -9,042 millones hasta 13,497 millones
- Incluye cuentas de clientes, cobros y saldos contables
- Datos estructurados por niveles de cuenta contable

#### 2. **Colombiana - Situación cuentas AT por División - Junio de 2025.xlsx** (33.0 KB)
**Propósito**: Reporte de situación de cuentas por división y categorías

**Estructura**:
- **Filas**: 151 registros
- **Columnas**: 12 campos
- **Tipo**: Reporte de situación por división

**Columnas principales**:
1. `COMPAÑÍA` - Código de compañía (00080)
2. `DIVISIÓN` - División de la empresa
3. `COD.CATEGORÍA 4` - Categoría 4 (ej: T01 - VARIACION PNT)
4. `COD.CATEGORÍA 3` - Categoría 3 (ej: T03 - FREE CASH-FLOW)
5. `COD.CATEGORÍA 1` - Categoría 1 (ej: S01 - COBROS DE CLIENTES)
6. `CUENTA OBJETO` - Cuenta objeto contable
7. `SUBCUENTA` - Subcuenta específica
8. `DESCRIPCIÓN DE CUENTA` - Descripción de la cuenta
9. `SALDO MES` - Saldo del mes actual
10. `SALDO MES -1` - Saldo del mes anterior
11. `SALDO MES -2` - Saldo de hace dos meses
12. `SALDO ACUMULADO` - Saldo acumulado

**Características**:
- Organizado por categorías contables y divisiones
- Incluye comparación de saldos por períodos
- Valores desde -4,670 millones hasta 5,016 millones
- Enfoque en cobros de clientes y flujo de caja

#### 3. **FOCUS JUNIO 2025 TRABAJO.xlsx** (66.2 KB)
**Propósito**: Reporte FOCUS de deuda no grupo para junio de 2025

**Estructura**:
- **Filas**: 63,383 registros
- **Columnas**: 20 campos
- **Tipo**: Reporte detallado de deuda

**Características**:
- Archivo con estructura compleja y múltiples hojas
- Columnas sin nombres específicos (Unnamed)
- Contiene datos de "RESUMEN DEUDA NO GRUPO (datos en Miles)"
- Fecha de cierre: 2025-06-30
- Valor euros al cierre: 4,777.18
- Enfoque en LIBRERÍAS COLOMBIA

**Datos clave**:
- Fecha euros al cierre mes: 2025-06-30 00:00:00
- Valor euros al cierre mes: 4777.18
- Período: Junio

#### 4. **formato acumuladado FOCUS prueba.xls** (665.1 KB)
**Propósito**: Formato acumulado de prueba para reportes FOCUS

**Estructura**:
- **Filas**: 64,871 registros
- **Columnas**: 14 campos
- **Tipo**: Formato acumulado de prueba para FOCUS

**Características**:
- Archivo más grande de todos (665 KB)
- Estructura similar al FOCUS JUNIO 2025 pero con más datos
- Contiene datos de "RESUMEN DEUDA NO GRUPO (datos en Miles)"
- Enfoque en LIBRERÍAS COLOMBIA
- Período: Enero (datos de prueba)
- Columnas sin nombres específicos (Unnamed)
- Alternancia entre columnas numéricas y de texto

**Datos clave**:
- Formato de prueba para validar el procesamiento
- Datos acumulados para diferentes períodos
- Estructura base para el procesamiento FOCUS

## 🔍 ANÁLISIS GENERAL

### 📈 Patrones Identificados
1. **Período de Datos**: Todos los archivos corresponden a junio de 2025
2. **Entidad**: Enfoque en LIBRERÍAS COLOMBIA (Colombiana)
3. **Tipo de Información**: Datos financieros, contables y de deuda
4. **Estructura**: Datos organizados por cuentas, divisiones y categorías

### 🎯 Propósito de los Documentos
Estos documentos parecen ser la **fuente de datos principal** para el procesamiento de:
- **Balance contable** (06 BALANCE COLOMBIANA)
- **Situación por división** (Colombiana - Situación)
- **Reportes FOCUS** (FOCUS JUNIO 2025)
- **Formatos de prueba** (formato acumuladado FOCUS)

### 🔗 Relación con el Sistema
Estos archivos corresponden exactamente a los **tres tipos de entrada** que requiere el `procesador_balance_completo.py`:
1. **Archivo BALANCE** → `06 BALANCE COLOMBIANA JUNIO.xlsx`
2. **Archivo SITUACIÓN** → `Colombiana - Situación cuentas AT por División - Junio de 2025.xlsx`
3. **Archivo FOCUS** → `FOCUS JUNIO 2025 TRABAJO.xlsx`

### 📋 Próximos Pasos Recomendados
1. ✅ **Instalar dependencia faltante**: `pip install xlrd>=2.0.1` (COMPLETADO)
2. ✅ **Analizar el archivo .xls** para completar el análisis (COMPLETADO)
3. **Revisar documentos Word** para entender las especificaciones de formato
4. **Probar el procesamiento** con estos archivos reales
5. **Validar resultados** contra las especificaciones de negocio

## 📊 Estadísticas de Datos

| Archivo | Registros | Columnas | Tamaño | Tipo Principal |
|---------|-----------|----------|--------|----------------|
| 06 BALANCE COLOMBIANA | 3,151 | 13 | 169.8 KB | Balance Contable |
| Colombiana - Situación | 151 | 12 | 33.0 KB | Situación por División |
| FOCUS JUNIO 2025 | 63,383 | 20 | 66.2 KB | Reporte de Deuda |
| formato acumuladado FOCUS | 64,871 | 14 | 665.1 KB | Formato de Prueba |

---
*Análisis realizado el 05/08/2025*
*Sistema de Procesamiento de Cartera - Grupo Planeta* 