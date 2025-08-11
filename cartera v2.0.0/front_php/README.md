# Sistema de Procesamiento de Cartera y Anticipos - Grupo Planeta

## Descripción General

Esta aplicación permite procesar archivos de cartera (provisión) y anticipos generados por el sistema Pisa, generando reportes detallados en Excel con cálculos, validaciones y formatos requeridos por el área financiera. Incluye un modelo de deuda avanzado que genera archivos Excel con tres hojas separadas.

## Requisitos del Sistema

- **Python**: 3.8 o superior
- **Paquetes Python**: pandas, openpyxl, numpy
- **Servidor Web**: WAMP/XAMPP (para interfaz web)
- **PHP**: 7.4 o superior (para interfaz web)

### Instalación de Dependencias

```bash
pip install pandas openpyxl numpy
```

## Estructura del Proyecto

```
cartera/
├── index.php                          # Interfaz web principal
├── procesar.php                       # Procesamiento de cartera y anticipos
├── modelo_deuda.php                   # Procesamiento del modelo de deuda
├── descargar.php                      # Descarga de archivos generados
├── PROVCA/
│   ├── procesador_cartera.py          # Procesador de cartera
│   ├── procesador_anticipos.py        # Procesador de anticipos
│   ├── modelo_deuda.py                # Modelo de deuda avanzado
│   ├── utilidades.py                  # Funciones auxiliares
│   ├── PROVCA.CSV                     # Archivo de cartera de ejemplo
│   └── ANTICI.CSV                     # Archivo de anticipos de ejemplo
├── PROVCA_PROCESADOS/                 # Carpeta de archivos generados
└── temp/                              # Carpeta temporal
```

## Funcionalidades Principales

### 1. Procesamiento de Cartera (Provisión)

**Archivos de entrada**: `PROVCA.CSV` o archivos similares en formato CSV/Excel

**Proceso realizado**:
- Renombra los campos según el mapeo oficial
- Elimina la columna PCIMCO y filas de empresa PL30 con saldo -614.000
- Unifica nombres de clientes en una sola columna
- Convierte fechas a formato `dd/mm/yyyy` y crea columnas separadas
- Calcula días vencidos, días por vencer, saldo vencido
- Calcula % dotación (100% si >=180 días vencido), valor dotación, mora total
- Crea columnas de vencimientos por rango de días
- Crea columna de deuda incobrable
- Aplica formato colombiano a los números
- Valida que la suma de mora total + valor por vencer sea igual al saldo

### 2. Procesamiento de Anticipos

**Archivos de entrada**: `ANTICI.CSV` o `ANTICI.xlsx`

**Proceso realizado**:
- Renombra los campos según el mapeo oficial
- Multiplica el valor de anticipo por -1 (deben ser negativos)
- Convierte la fecha de anticipo a formato `dd/mm/yyyy`
- Aplica formato colombiano a los números

### 3. Modelo de Deuda Avanzado

**Funcionalidad**: Genera un archivo Excel con tres hojas separadas que procesa datos de cartera y anticipos según especificaciones detalladas.

#### Hoja 1: PESOS
Contiene registros de líneas de venta en pesos colombianos:

**Líneas CT:**
- CT 80 - TINTA-CLUB DEL LIBRO SAS

**Líneas ED:**
- ED 41 - PLANETA CREDI. ELITE 2000
- ED 44 - PLANETA VENTA DIGITAL
- ED 47 - EVENTOS FERIA CREDITO

**Líneas PL:**
- PL 10 - MERMA GRANDES SUPERFICIES
- PL 15 - MARKETING DIRECTO - WEB
- PL 20 - LIBRERIAS (PLANETA)
- PL 21 - LIBRERIA GDES SUPERFICIES
- PL 23 - EVENTOS FERIAS LIBRERIA 1
- PL 25 - DISTRIBUIDORA - PLANETA
- PL 28 - VENTA SALDOS LIBRERIAS
- PL 29 - VENTA SALDOS DISTR/BDORA
- PL 31 - PLACISMO - COLOMBIANA
- PL 32 - DISTRIBUCION DE TERCEROS
- PL 53 - FERIA PLANETA LECTOR
- PL 56 - VENTA DIGITAL LIBRERIAS
- PL 60 - VENTA INSTITUCIONAL
- PL 62 - NEGOCIO PERIODICOS
- PL 63 - CANAL PROMOCION ESCOLAR
- PL 64 - NEGOCIO LICITACIONES
- PL 65 - VENTA CLIENTES ESPECIALES
- PL 66 - AULA PLANETA
- PL 69 - VENTA AUTORES SIN DERECHO

#### Hoja 2: DIVISAS
Contiene registros de líneas en dólares y euros:

**Dólares:**
- PL 11 - TERCEROS DOLARES N.E.
- PL 18 - COLOMBIANA TERCEROS DOLARES
- PL 57 - COLOMBIANA AULA PLANETA DOLARES

**Euros:**
- PL 41 - COLOMBIANA TERCEROS EURO N.E.

**Nota**: Los valores en divisas se multiplican por la TRM (Tasa de Cambio Representativa del Mercado) del último día del mes anterior.

#### Hoja 3: VENCIMIENTO
Contiene totales por cliente con la siguiente estructura:

| Campo | Descripción | Valor |
|-------|-------------|-------|
| PAIS | País de origen | Colombia |
| NEGOCIO | Tipo de negocio | Según tabla de correspondencia |
| CANAL | Canal de venta | Según tabla de correspondencia |
| COBRO/PAGO | Tipo de operación | CLIENTE |
| MONEDA | Tipo de moneda | PESOS COL / DOLAR / EURO |
| CLIENTE | Nombre del cliente | Nombre del cliente |
| SALDO TOTAL | Total de saldo | Valor numérico |
| Saldo No vencido | Saldo por vencer | Valor numérico |
| Vencido 30 | Vencido hasta 30 días | Valor numérico |
| Vencido 60 | Vencido 31-60 días | Valor numérico |
| Vencido 90 | Vencido 61-90 días | Valor numérico |
| Vencido 180 | Vencido 91-180 días | Valor numérico |
| Vencido 360 | Vencido 181-360 días | Valor numérico |
| Vencido + 360 | Vencido más de 360 días | Valor numérico |
| DEUDA INCOBRABLE | Deuda incobrable | Valor numérico |

**Totalización**: Al final de la hoja se incluyen totales por moneda (Moneda Local, Dólar, Euro) y un total general.

**Ejemplo de Totalización**:

| MONEDA | CLIENTE | SALDO TOTAL | Saldo No vencido | Vencido 30 | Vencido 60 |
|--------|---------|-------------|------------------|------------|------------|
| Moneda Local | | 11.569.275.051,00 | 10.622.734.919,00 | 49.957.868,00 | 232.747.642,00 |
| Dólar | | 4.069,67 | 5.010.037.251,00 | 4.777.289.609,00 | 232.747.642,00 |
| Euro | | 4.777,18 | 4.777.180,00 | - | 4.777.180,00 |
| Totales | | 16.584.089.482,00 | 15.400.024.528,00 | 287.482.690,00 | 470.272.464,00 |

## Tabla de Correspondencia Negocio-Canal

| Código | NEGOCIO | CANAL | Descripción |
|--------|---------|-------|-------------|
| 15 | E-COMMERCE | PL15 | Marketing Directo - Web |
| 20 | LIBRERIAS 1 | PL20 | Librerías (Planeta) |
| 25 | LIBRERIAS 2 | PL25 | Distribuidora - Planeta |
| 10 | LIBRERIAS 2 | PL10 | Merma Grandes Superficies |
| 21 | LIBRERIAS 3 | PL21 | Librería Gdes Superficies |
| 53 | LIBRERIAS 3 | PL53 | Feria Planeta Lector |
| 63 | LIBRERIAS 3 | PL63 | Canal Promoción Escolar |
| 66 | OTOS DIGITAL | PL66 | Aula Planeta |
| 60 | OTROS | PL60 | Venta Institucional |
| 64 | OTROS | PL64 | Negocio Licitaciones |
| 65 | OTROS | PL65 | Venta Clientes Especiales |
| 28 | SALDOS | PL28 | Venta Saldos Librerías |
| 29 | SALDOS | PL29 | Venta Saldos Distr/Bdora |
| 31 | SALDOS | PL31 | Placismo - Colombiana |
| 18 | EXPORTACION | PL18 | Colombiana Terceros Dólares |
| 11 | EXPORTACION | PL11 | Terceros Dólares N.E. |
| 57 | AULA | PL57 | Colombiana Aula Planeta Dólares |
| 41 | OTR | PL41 | Colombiana Terceros Euro N.E. |
| 80 | TINTA CLUB DEL LIBRO | CT80 | Tinta-Club del Libro SAS |

## Mapeo de Columnas

### Cartera (Provisión)

| Campo Original | Campo Procesado | Descripción |
|----------------|-----------------|-------------|
| PCCDEM | EMPRESA | Código de empresa |
| PCCDAC | ACTIVIDAD | Código de actividad |
| PCDEAC | EMPRESA | Empresa |
| PCCDAG | CODIGO AGENTE | Código del agente |
| PCNMAG | AGENTE | Nombre del agente |
| PCCDCO | CODIGO COBRADOR | Código del cobrador |
| PCNMCO | COBRADOR | Nombre del cobrador |
| PCCDCL | CODIGO CLIENTE | Código del cliente |
| PCCDDN | IDENTIFICACION | Número de identificación |
| PCNMCL | NOMBRE | Nombre del cliente |
| PCNMCM | DENOMINACION COMERCIAL | Denominación comercial |
| PCNMDO | DIRECCION | Dirección del cliente |
| PCTLF1 | TELEFONO | Teléfono del cliente |
| PCNMPO | CIUDAD | Ciudad del cliente |
| PCNUFC | NUMERO FACTURA | Número de factura |
| PCORPD | TIPO | Tipo de documento |
| PCFEFA | FECHA | Fecha de factura |
| PCFEVE | FECHA VTO | Fecha de vencimiento |
| PCVAFA | VALOR | Valor de la factura |
| PCSALD | SALDO | Saldo pendiente |

### Anticipos

| Campo Original | Campo Procesado | Descripción |
|----------------|-----------------|-------------|
| NCCDEM | EMPRESA | Código de empresa |
| NCCDAC | ACTIVIDAD | Código de actividad |
| NCCDCL | CODIGO CLIENTE | Código del cliente |
| WWNIT | NIT/CEDULA | NIT o cédula del cliente |
| WWNMCL | NOMBRE COMERCIAL | Nombre comercial del cliente |
| WWNMDO | DIRECCION | Dirección del cliente |
| WWTLF1 | TELEFONO | Teléfono del cliente |
| WWNMPO | POBLACION | Población del cliente |
| CCCDFB | CODIGO AGENTE | Código del agente |
| BDNMNM | NOMBRE AGENTE | Nombre del agente |
| BDNMPA | APELLIDO AGENTE | Apellido del agente |
| NCMOMO | TIPO ANTICIPO | Tipo de anticipo |
| NCCDR3 | NRO ANTICIPO | Número de anticipo |
| NCIMAN | VALOR ANTICIPO | Valor del anticipo |
| NCFEGR | FECHA ANTICIPO | Fecha del anticipo |

## Cómo Usar

### Opción 1: Interfaz Web (Recomendado)

1. **Acceder a la aplicación**:
   - Abrir el navegador y dirigirse a `http://localhost/cartera/`
   - Se mostrará la interfaz principal con tres secciones

2. **Procesar Cartera**:
   - Seleccionar "Cartera (Provisión)"
   - Subir archivo `PROVCA.CSV` o similar
   - Hacer clic en "Procesar Cartera"
   - Descargar el archivo procesado

3. **Procesar Anticipos**:
   - Seleccionar "Anticipos"
   - Subir archivo `ANTICI.CSV` o `ANTICI.xlsx`
   - Hacer clic en "Procesar Anticipos"
   - Descargar el archivo procesado

4. **Generar Modelo de Deuda**:
   - Seleccionar "Modelo Deuda"
   - Subir archivo de cartera procesada
   - Subir archivo de anticipos procesados
   - Ingresar la TRM del último día del mes anterior
   - Hacer clic en "Generar Modelo Deuda"
   - Descargar el archivo Excel con tres hojas

### Opción 2: Línea de Comandos

#### Procesar Cartera
```bash
cd PROVCA
python procesador_cartera.py PROVCA.CSV
```

#### Procesar Anticipos
```bash
cd PROVCA
python procesador_anticipos.py ANTICI.CSV
```

#### Generar Modelo de Deuda
```bash
cd PROVCA
python modelo_deuda.py "ruta_archivo_cartera.xlsx" "ruta_archivo_anticipos.xlsx" "TRM"
```

**Ejemplo**:
```bash
python modelo_deuda.py "PROVCA_PROCESADOS/CARTERA_PROCESADA_2025-01-15.xlsx" "PROVCA_PROCESADOS/ANTICIPOS_PROCESADOS_2025-01-15.xlsx" "4000.50"
```

## Archivos de Entrada Requeridos

### Archivo de Cartera Procesada
Debe contener las siguientes columnas:

| Campo | Descripción | Tipo |
|-------|-------------|------|
| EMPRESA | Código de empresa | Texto |
| ACTIVIDAD | Código de actividad | Texto |
| DENOMINACION COMERCIAL | Nombre del cliente | Texto |
| SALDO | Saldo total | Numérico |
| SALDO VENCIDO | Saldo vencido | Numérico |
| SALDO NO VENCIDO | Saldo por vencer | Numérico |
| VENCIDO 30 | Vencido hasta 30 días | Numérico |
| VENCIDO 60 | Vencido 31-60 días | Numérico |
| VENCIDO 90 | Vencido 61-90 días | Numérico |
| VENCIDO 180 | Vencido 91-180 días | Numérico |
| VENCIDO 360 | Vencido 181-360 días | Numérico |
| VENCIDO + 360 | Vencido más de 360 días | Numérico |
| DEUDA INCOBRABLE | Deuda incobrable | Numérico |
| MONEDA | Tipo de moneda | Texto |

### Archivo de Anticipos Procesados
Debe contener las siguientes columnas:

| Campo | Descripción | Tipo |
|-------|-------------|------|
| EMPRESA | Código de empresa | Texto |
| ACTIVIDAD | Código de actividad | Texto |
| NOMBRE COMERCIAL | Nombre del cliente | Texto |
| VALOR ANTICIPO | Valor del anticipo | Numérico |

## Archivos de Salida

### Procesamiento Individual
- **Cartera**: `CARTERA_PROCESADA_YYYY-MM-DD_HH-MM-SS.xlsx`
- **Anticipos**: `ANTICIPO_PROCESADO_YYYY-MM-DD_HH-MM-SS.xlsx`

### Modelo de Deuda
- **Archivo**: `1_Modelo_Deuda_YYYY-MM-DD_HH-MM-SS.xlsx`
- **Ubicación**: Carpeta `PROVCA_PROCESADOS/`

## Características Especiales

### 1. Procesamiento de Anticipos
Los datos de anticipos se agregan al final de cada hoja según la estructura de la cartera.

### 2. Aplicación de TRM
Los valores en divisas se multiplican automáticamente por la TRM proporcionada.

### 3. Totalización por Moneda
La hoja de vencimiento incluye totales separados por moneda y un total general.

### 4. Formato Colombiano y Contable
Los números se formatean con separadores de miles y decimales según el formato colombiano. Se aplican las siguientes reglas de formato:

- **Números**: Formato contable colombiano (#,##0.00)
- **Ceros**: Se muestran como "-" en lugar de "0"
- **Porcentajes**: Se formatean correctamente con símbolo "%"
- **Alineación**: Números a la derecha, textos a la izquierda
- **Encabezados**: Formato profesional con color azul y negrita
- **Bordes**: Todas las celdas tienen bordes para mejor legibilidad
- **Ancho de columnas**: Se ajusta automáticamente al contenido

### 5. Validación de Datos
El sistema valida la existencia de columnas necesarias y maneja errores de forma robusta. Incluye validaciones específicas para el modelo de deuda:

- **Columnas requeridas**: Verifica que existan todas las columnas necesarias
- **Líneas de venta**: Valida que las líneas de venta estén presentes
- **Monedas**: Verifica que las monedas sean válidas (PESOS COL, DOLAR, EURO)
- **Valores numéricos**: Detecta valores negativos o inconsistentes
- **Estructura de datos**: Valida la integridad de los datos de entrada

### 6. Tres Hojas Separadas
El archivo Excel del modelo de deuda contiene tres hojas independientes: PESOS, DIVISAS y VENCIMIENTO.

### 7. Descarga Segura
Sistema de descarga de archivos con validaciones de seguridad y manejo de errores.

## Notas Importantes

- Asegúrese de que los archivos de entrada estén en formato Excel (.xlsx) o CSV
- La TRM debe ser un número válido (ejemplo: 4000.50)
- El proceso puede tomar varios minutos dependiendo del tamaño de los archivos
- Los archivos generados se sobrescriben si ya existen con el mismo nombre
- Todos los números tienen formato colombiano y alineación a la derecha
- Si tiene problemas con la lectura de archivos, revise el separador (debe ser `;` para CSV)

## Solución de Problemas

### Error de Descarga
Si no aparece el botón de descarga:
1. Verificar que el archivo se generó correctamente
2. Revisar la consola del navegador (F12) para errores
3. Verificar permisos de escritura en la carpeta `PROVCA_PROCESADOS/`

### Error de Procesamiento
Si el procesamiento falla:
1. Verificar que los archivos de entrada tengan el formato correcto
2. Revisar que las columnas requeridas estén presentes
3. Verificar que la TRM sea un número válido

### Error de Totalización
Si la totalización no aparece correctamente:
1. Verificar que el archivo de cartera tenga datos válidos
2. Revisar que las columnas de moneda estén correctamente identificadas
3. Verificar que las líneas de venta estén en el formato esperado

## Soporte

Para dudas, mejoras o reporte de errores, contacte al desarrollador del sistema.

---

**Versión**: 1.0  
**Última actualización**: Enero 2025  
**Desarrollado para**: Grupo Planeta 