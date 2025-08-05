# Procesador de Balance - Grupo Planeta

## Descripción
El Procesador de Balance es una herramienta que analiza datos financieros de tres archivos principales: BALANCE, SITUACIÓN y FOCUS, realizando cálculos específicos según las especificaciones del negocio.

## Archivos Requeridos

### 1. Archivo BALANCE
- **Formato**: CSV, XLSX o XLS
- **Columnas requeridas**:
  - Columna con nombre "Saldo AAF variación"
  - Columna de "cuenta objeto"

#### Cuentas Objeto a Procesar:
- **43001** - Total cuenta objeto
- **43008** - Total cuenta objeto  
- **43042** - Total cuenta objeto

#### Subcuentas Específicas:
- 0080.43002.20
- 0080.43002.21
- 0080.43002.15
- 0080.43002.28
- 0080.43002.31
- 0080.43002.63

### 2. Archivo SITUACIÓN
- **Formato**: CSV, XLSX o XLS
- **Datos requeridos**:
  - Columna "SALDOS MES"
  - Valor de TOTAL 01010

### 3. Archivo FOCUS
- **Formato**: CSV, XLSX o XLS (formato España)
- **Datos requeridos**:
  - Datos de vencimientos (archivo número 2)
  - Tipos de cambio
  - Información de deuda bruta
  - Dotaciones acumuladas

## Cálculos Realizados

### 1. Tipos de Cambio
- Cambio del mes de cierre
- Actualización de tasas de cambio

### 2. Deuda Bruta NO Grupo
- **Inicial** = Deuda bruta NO Grupo (Final)

### 3. Dotaciones Acumuladas
- **Inicial** = '+/- Provisión acumulada (Final)

### 4. Cobros del Mes
- **Vencida** = Deuda bruta NO Grupo (Inicial) Vencidas - Total vencido de 60 días en adelante / 1000
- **Total Deuda** = COBROS SITUACION (SALDO MES) / -1000
- **No Vencida** = Cobro total deuda - Cobro vencida

### 5. Vencidos en el Mes
- **Vencido** = VENCIDO MES 30 días (signo positivo)
- **No vencido** = Valor del cobro no vencido
- **Total deuda** = No vencido - Vencido

### 6. Facturación del Mes
- **Vencida** = 0
- **No vencida** = Deuda bruta NO Grupo (Final) - total deuda

### 7. Dotación del Mes
- Se calcula desde el archivo de datos de la provisión del mes Interco RESTO
- **Fórmula**: - Dotaciones Acumuladas (Inicial) - Provisión del mes

### 8. Acumulado
Los valores se copian desde el archivo formato acumulado Focus:
- **- Cobros**: -377.486
- **+ Facturación**: 9.308.786
- **+/- Vencidos**: 390.143
- **DOTACIÓN**: -560.370

## Cómo Usar

1. **Acceder al Procesador**:
   - Ve a la página principal del sistema
   - Haz clic en "Procesador Balance"

2. **Cargar Archivos**:
   - Selecciona el archivo BALANCE
   - Selecciona el archivo SITUACIÓN
   - Selecciona el archivo FOCUS
   - Haz clic en "Calcular Balance"

3. **Ver Resultados**:
   - Los resultados se mostrarán organizados por secciones
   - Todos los cálculos se realizan automáticamente
   - Los valores se formatean con separadores de miles

## Estructura de Resultados

### Archivo BALANCE - Totales por Cuenta Objeto
- Total cuenta objeto 43001
- Total cuenta objeto 43008
- Total cuenta objeto 43042

### Subcuentas Específicas
- Valores individuales para cada subcuenta especificada

### Archivo SITUACIÓN
- TOTAL 01010 (SALDOS MES)

### Cálculos FOCUS
- Deuda bruta NO Grupo (Inicial/Final)
- Dotaciones Acumuladas (Inicial)
- +/- Provisión acumulada (Final)

### Cálculos de Cobros
- Cobro de mes - Vencida
- Cobro mes - Total Deuda
- Cobros del mes - No Vencida

### Vencidos en el Mes
- +/- Vencidos en el mes – vencido
- +/- Vencidos en el mes – No vencido
- +/- Vencidos en el mes – Total deuda

### Facturación del Mes
- + Facturación del mes – vencida
- + Facturación del mes – no vencida

### Dotación del Mes
- Dotación del mes

### Acumulado
- - Cobros
- + Facturación
- +/- Vencidos
- DOTACIÓN

## Notas Técnicas

- **Formato de números**: Los resultados se muestran con formato español (comas como separadores de miles, puntos como separadores decimales)
- **Manejo de errores**: El sistema valida que todos los archivos requeridos estén presentes y en el formato correcto
- **Compatibilidad**: Soporta archivos CSV, XLSX y XLS
- **Procesamiento**: Los cálculos se realizan en tiempo real sin necesidad de guardar archivos intermedios

## Requisitos del Sistema

- PHP 7.4 o superior
- Extensión PHP para manejo de archivos CSV
- Navegador web moderno con soporte para JavaScript ES6
- Conexión a internet para cargar las fuentes y iconos

## Soporte

Para problemas técnicos o consultas sobre el procesador de balance, contacta al equipo de desarrollo del Grupo Planeta. 