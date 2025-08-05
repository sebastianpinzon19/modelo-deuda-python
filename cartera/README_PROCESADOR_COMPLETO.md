# Procesador Completo de Balance - Grupo Planeta

## Descripción General

Este sistema integrado procesa tres archivos Excel principales para realizar análisis financieros completos:

1. **Archivo BALANCE** - Contiene datos de cuentas objeto y saldos
2. **Archivo SITUACIÓN** - Contiene datos de cobros y saldos mensuales
3. **Archivo FOCUS** - Contiene datos de vencimientos y dotaciones

## Estructura del Proyecto

```
cartera/
├── PROVCA/
│   ├── procesador_balance_completo.py    # Procesador Python principal
│   └── requirements.txt                  # Dependencias Python
├── procesar_balance_completo.php         # Interfaz web principal
├── test_procesador_completo.php          # Archivo de prueba
├── temp/                                 # Directorio temporal
└── AN/                                   # Archivos de datos
    ├── 06 BALANCE COLOMBIANA JUNIO.xlsx
    ├── Colombiana - Situación cuentas AT por División - Junio de 2025.xlsx
    ├── FOCUS JUNIO 2025 TRABAJO.xlsx
    └── formato acumuladado FOCUS prueba.xls
```

## Especificaciones de Procesamiento

### 1. Archivo BALANCE

**Cuentas objeto a procesar:**
- Total cuenta objeto 43001
- Total cuenta objeto 43008  
- Total cuenta objeto 43042
- Subcuentas específicas:
  - 0080.43002.20
  - 0080.43002.21
  - 0080.43002.15
  - 0080.43002.28
  - 0080.43002.31
  - 0080.43002.63

**Columna requerida:** "Saldo AAF variación"

### 2. Archivo SITUACIÓN

**Dato a extraer:** Valor de TOTAL 01010 en la columna "SALDOS MES"

### 3. Archivo FOCUS

**Datos de vencimientos:** Se toman del archivo número 2 de formato España

## Cálculos Financieros

### 1. Tipos de Cambio
- Cambiar el mes de cierre y actualizar tasas de cambio

### 2. Deuda Bruta NO Grupo
- **Inicial** = Deuda bruta NO Grupo (Final)

### 3. Dotaciones Acumuladas
- **Inicial** = '+/- Provisión acumulada (Final)

### 4. Cobros del Mes
- **Vencida** = Deuda bruta NO Grupo (Inicial) Vencidas - Total vencido de 60 días en adelante / 1000
- **Total Deuda** = COBROS SITUACION (SALDO MES) / -1000
- **No Vencida** = Cobro total - Cobro vencida

### 5. Vencidos en el Mes
- **Vencido** = VENCIDO MES 30 días (signo positivo)
- **No vencido** = Mismo valor que vencido
- **Total deuda** = Vencido - No vencido

### 6. Facturación del Mes
- **Vencida** = 0
- **No vencida** = Deuda bruta NO Grupo (Final) - total deuda

### 7. Dotación del Mes
- Del archivo de datos de la provisión del mes Interco RESTO
- **Dotación** = Dotaciones Acumuladas (Inicial) - Provisión del mes

## Formato de Salida

El sistema genera un reporte estructurado con las siguientes secciones:

### Resumen de Cálculos
```
- Cobros          [Vencida] [No Vencida]
+ Facturación     [Vencida] [No Vencida]  
+/- Vencidos      [Vencida] [No Vencida]
Subtotal          [Vencida] [No Vencida]
```

### Provisión y Dotación
```
PROVISION         [Valor]
DOTACION          [Valor]
- Dotaciones      [Valor]
+ Desdotaciones   [Valor]
```

### Acumulado
```
Deuda bruta NO Grupo (inicial)  [Vencida] [No Vencida]
- Cobros                        [Vencida] [No Vencida]
+ Facturación                   [Vencida] [No Vencida]
+/- Vencidos                    [Vencida] [No Vencida]
```

### Deuda Final
```
Deuda bruta NO Grupo (Final)    [Valor]
- Dotaciones Acumuladas (Inicial) [Valor]
- Dotaciones                    [Valor]
+ Desdotaciones                 [Valor]
```

## Instalación y Configuración

### Requisitos del Sistema

1. **Python 3.8+** con las siguientes librerías:
   ```bash
   pip install pandas numpy openpyxl
   ```

2. **PHP 7.4+** con extensiones:
   - fileinfo
   - json
   - session

3. **Servidor Web** (Apache/Nginx) con soporte para PHP

### Configuración

1. **Ruta de Python:** Editar la variable `$python_path` en `procesar_balance_completo.php`
   ```php
   $python_path = 'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe';
   ```

2. **Permisos:** Asegurar que el directorio `temp/` tenga permisos de escritura

3. **Límite de archivos:** Configurar `upload_max_filesize` y `post_max_size` en php.ini

## Uso del Sistema

### Interfaz Web

1. Acceder a `procesar_balance_completo.php`
2. Subir los tres archivos Excel requeridos
3. Hacer clic en "Procesar Archivos"
4. Revisar los resultados en la interfaz

### Línea de Comandos

```bash
python PROVCA/procesador_balance_completo.py archivo_balance.xlsx archivo_situacion.xlsx archivo_focus.xlsx
```

### Archivo de Prueba

Para verificar el funcionamiento:
```bash
php test_procesador_completo.php
```

## Estructura de Archivos Excel

### Archivo BALANCE
| Cuenta objeto | Saldo AAF variación |
|---------------|-------------------|
| 43001         | 1000000           |
| 43008         | 2000000           |
| 43042         | 3000000           |
| 0080.43002.20 | 500000            |
| ...           | ...               |

### Archivo SITUACIÓN
| TOTAL 01010 | SALDOS MES |
|-------------|------------|
| 01010       | 5000000    |

### Archivo FOCUS
| Concepto | Periodo | Valor |
|----------|---------|-------|
| Deuda bruta NO Grupo | Inicial | 10000000 |
| Deuda bruta NO Grupo | Final | 12000000 |
| Dotaciones Acumuladas | Inicial | 2000000 |
| ... | ... | ... |

## Manejo de Errores

El sistema incluye validaciones para:

- **Formato de archivos:** Solo acepta archivos Excel (.xlsx, .xls)
- **Tamaño de archivos:** Límite de 50MB por archivo
- **Columnas requeridas:** Verifica la existencia de columnas específicas
- **Datos faltantes:** Maneja valores nulos o vacíos
- **Errores de procesamiento:** Logs detallados de errores

## Logs y Debugging

### Logs de Python
Los logs se guardan en el archivo `log_python.txt` con información detallada del procesamiento.

### Debugging
Para activar el modo debug, modificar el nivel de logging en `procesador_balance_completo.py`:
```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

## Mantenimiento

### Limpieza de Archivos Temporales
El sistema automáticamente limpia los archivos temporales después del procesamiento.

### Backup de Resultados
Los resultados se guardan en `resultados_balance_completo.json` con timestamp.

### Actualización de Dependencias
```bash
pip install --upgrade pandas numpy openpyxl
```

## Soporte Técnico

Para reportar problemas o solicitar mejoras:

1. Revisar los logs de error
2. Verificar la configuración del sistema
3. Probar con archivos de ejemplo
4. Contactar al equipo de desarrollo

## Versiones

- **v1.0** - Versión inicial con procesamiento básico
- **v1.1** - Mejoras en la interfaz web y validaciones
- **v1.2** - Cálculos financieros completos implementados

## Licencia

Este software es propiedad de Grupo Planeta y está destinado para uso interno. 