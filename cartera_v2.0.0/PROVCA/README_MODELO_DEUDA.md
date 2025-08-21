# Modelo de Deuda - Sistema de Procesamiento

## Descripción
El Modelo de Deuda es un sistema que procesa archivos de provisión y anticipos para generar reportes consolidados de deuda según el formato especificado en FORMATO DEUDA.docx.

## Características Principales

### 1. Hoja PESOS
- **Líneas en pesos procesadas:**
  - CT80: TINTA-CLUB DEL LIBRO SAS
  - ED41: PLANETA CREDI. ELITE 2000
  - ED44: PLANETA VENTA DIGITAL
  - ED47: EVENTOS FERIA CREDITO
  - PL10: MERMA GRANDES SUPERFICIES
  - PL15: MARKETING DIRECTO - WEB
  - PL20: LIBRERIAS (PLANETA)
  - PL21: LIBRERIA GDES SUPERFICIES
  - PL23: EVENTOS FERIAS LIBRERIA 1
  - PL25: DISTRIBUIDORA - PLANETA
  - PL28: VENTA SALDOS LIBRERIAS
  - PL29: VENTA SALDOS DISTR/BDORA
  - PL31: PLACISMO - COLOMBIANA
  - PL32: DISTRIBUCION DE TERCEROS
  - PL53: FERIA PLANETA LECTOR
  - PL56: VENTA DIGITAL LIBRERIAS
  - PL60: VENTA INSTITUCIONAL
  - PL62: NEGOCIO PERIODICOS
  - PL63: CANAL PROMOCION ESCOLAR
  - PL64: NEGOCIO LICITACIONES
  - PL65: VENTA CLIENTES ESPECIALES
  - PL66: AULA PLANETA
  - PL69: VENTA AUTORES SIN DERECHO

- **Anticipos:** Se agregan al final con estructura adaptada

### 2. Hoja DIVISAS
- **Líneas en divisas procesadas:**
  - PL11: TERCEROS DOLARES N.E.
  - PL18: COLOMBIANA TERCEROS DOLARES
  - PL57: COLOMBIANA AULA PLANETA DOLARES
  - PL41: COLOMBIANA TERCEROS EURO N.E.

- **Conversión TRM:** Se aplica la tasa de cambio del último día del mes anterior
- **Totales:** Se generan totales por moneda (USD y EUR)

### 3. Hoja VENCIMIENTO
- **Estructura de datos:**
  - País: Colombia
  - Negocio: Según tabla de mapeo
  - Canal: Según tabla de mapeo
  - Cobro/Pago: CLIENTE
  - Moneda: PESOS COL, DÓLAR, EURO
  - Cliente: Denominación comercial
  - Saldos y vencimientos por rangos de días

- **Tabla Negocio-Canal:**
  - E-COMMERCE: PL15
  - LIBRERIAS 1: PL20, PL25
  - LIBRERIAS 2: PL10, PL21
  - LIBRERIAS 3: PL53, PL63
  - OTOS DIGITAL: PL66
  - OTROS: PL60, PL64, PL65
  - SALDOS: PL28, PL29, PL31
  - EXPORTACION: PL18, PL11
  - AULA: PL57
  - OTR: PL41
  - TINTA CLUB DEL LIBRO: CT80

## Archivos de Entrada Requeridos

### 1. Archivo de Provisión
- Formato: Excel (.xlsx)
- Debe contener las columnas de saldos y vencimientos
- Debe incluir campos: EMPRESA, ACTIVIDAD, MONEDA, DENOMINACION COMERCIAL

### 2. Archivo de Anticipos
- Formato: Excel (.xlsx)
- Debe contener: NOMBRE COMERCIAL, VALOR ANTICIPO

## Configuración TRM

El sistema requiere configurar las tasas de cambio:
- **TRM Dólar:** Tasa de cambio USD/COP del último día del mes anterior
- **TRM Euro:** Tasa de cambio EUR/COP del último día del mes anterior

## Formato de Salida

### Archivo Excel con 3 hojas:
1. **PESOS:** Datos en pesos colombianos
2. **DIVISAS:** Datos en divisas con conversión TRM
3. **VENCIMIENTO:** Consolidado por cliente con totales por moneda

### Formato numérico:
- Separador de miles: punto (.)
- Separador decimal: coma (,)
- Valores cero se muestran como "-"

## Instrucciones de Uso

### Opción 1: Ejecución directa
```bash
python modelo_deuda.py "ruta_archivo_cartera.xlsx" "ruta_archivo_anticipos.xlsx" TRM_DOLAR TRM_EURO
```

### Opción 2: Ejecución interactiva
```bash
python modelo_deuda.py
```
Seguir las instrucciones en pantalla para ingresar:
- Ruta del archivo de cartera
- Ruta del archivo de anticipos
- TRM Dólar
- TRM Euro

## Ejemplo de Uso

```bash
python modelo_deuda.py "PROVCA_PROCESADO.xlsx" "ANTICIPO_PROCESADO.xlsx" 4000 4300
```

## Archivos de Salida

Los archivos generados se guardan en la carpeta `PROVCA_PROCESADOS` con el formato:
`1_Modelo_Deuda_YYYY-MM-DD_HH-MM-SS.xlsx`

## Dependencias

- pandas
- xlsxwriter
- openpyxl
- Python 3.7+

## Notas Importantes

1. **TRM:** Las tasas de cambio se guardan automáticamente para uso futuro
2. **Formato:** El sistema detecta automáticamente el formato de los números de entrada
3. **Validación:** Se valida que los archivos de entrada existan y tengan el formato correcto
4. **Anticipos:** Los anticipos se procesan automáticamente y se agregan a las hojas correspondientes
5. **Totales:** Se generan totales automáticamente por moneda en todas las hojas

## Solución de Problemas

### Error: "No se encontró archivo"
- Verificar que las rutas de los archivos sean correctas
- Usar rutas absolutas si es necesario

### Error: "TRM inválida"
- Ingresar solo números (ejemplo: 4000 o 4000.50)
- Usar punto como separador decimal

### Archivo de salida no generado
- Verificar permisos de escritura en la carpeta de salida
- Revisar que haya suficiente espacio en disco
