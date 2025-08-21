# Sistema de Tasas de Cambio (TRM) - Documentación

## Descripción General

El sistema de TRM permite a los usuarios ingresar manualmente las tasas de cambio para el Dólar (USD/COP) y Euro (EUR/COP) para realizar conversiones de moneda en los procesos de análisis de cartera y modelo de deuda.

## Características Principales

### 1. Interfaz de Usuario Mejorada
- **Diseño moderno**: Interfaz con gradientes y efectos visuales
- **Validación en tiempo real**: Los campos validan automáticamente los valores ingresados
- **Feedback visual**: Mensajes de estado con colores diferenciados
- **Responsive**: Se adapta a diferentes tamaños de pantalla

### 2. Funcionalidades
- **Ingreso manual**: Los usuarios pueden ingresar las tasas de cambio manualmente
- **Guardado persistente**: Las TRM se guardan en un archivo JSON para uso futuro
- **Carga automática**: Al abrir el sistema, se cargan las últimas TRM guardadas
- **Validación robusta**: Verifica que los valores sean números válidos mayores a 0

### 3. Ubicaciones de Implementación

#### Frontend Principal (`index.php`)
- Interfaz unificada para todos los procesos
- Campos de TRM que aparecen solo cuando se selecciona "Modelo Deuda"
- Botón para guardar TRM independientemente del procesamiento

#### Página de Modelo (`modelo.php`)
- Formulario específico para el modelo de deuda
- Campos de TRM integrados en el formulario principal
- Validación antes del envío

## Estructura de Archivos

### Archivos Modificados/Creados:

1. **`front_php/index.php`**
   - Nueva interfaz de TRM con diseño mejorado
   - Funciones JavaScript para manejo de TRM
   - Validación en tiempo real

2. **`front_php/modelo.php`**
   - Campos de TRM integrados en el formulario
   - Validación mejorada

3. **`front_php/runner.php`**
   - Nueva acción `guardar_trm` para persistir las TRM
   - Manejo de TRM en el procesamiento

4. **`front_php/styles.css`**
   - Nuevas clases CSS para el diseño de TRM
   - Estilos responsivos y efectos visuales

5. **`PROVCA/trm_config.py`**
   - Funciones para cargar y guardar TRM
   - Manejo de archivo JSON de configuración

## Flujo de Trabajo

### 1. Carga Inicial
1. El usuario selecciona "Modelo Deuda" en el dropdown
2. Se cargan automáticamente las últimas TRM guardadas
3. Se muestran los campos de TRM con valores predefinidos

### 2. Ingreso de TRM
1. El usuario ingresa las tasas de cambio en los campos correspondientes
2. La validación en tiempo real verifica los valores
3. Se muestra el estado actual de la configuración

### 3. Guardado de TRM
1. El usuario hace clic en "Guardar TRM"
2. Se validan los valores ingresados
3. Se guardan en el archivo `trm_config.json`
4. Se muestra confirmación de guardado exitoso

### 4. Procesamiento
1. Al ejecutar el modelo de deuda, se usan las TRM configuradas
2. Se pueden usar TRM guardadas o ingresadas en el momento
3. Los valores se pasan al script Python para las conversiones

## Validaciones Implementadas

### Frontend (JavaScript)
- **Campos requeridos**: Al menos una TRM debe estar configurada
- **Valores numéricos**: Solo se aceptan números válidos
- **Valores positivos**: Las TRM deben ser mayores a 0
- **Formato decimal**: Se aceptan valores con decimales (step="0.01")

### Backend (PHP)
- **Validación de tipos**: Verifica que los valores sean numéricos
- **Sanitización**: Limpia los valores antes de procesarlos
- **Persistencia**: Guarda los valores en formato JSON

## Archivo de Configuración

### Estructura del JSON (`trm_config.json`)
```json
{
  "usd": 4000.0,
  "eur": 4700.0,
  "updated_at": "2025-01-20 10:30:00"
}
```

### Campos:
- **`usd`**: Tasa de cambio Dólar/Peso Colombiano
- **`eur`**: Tasa de cambio Euro/Peso Colombiano
- **`updated_at`**: Timestamp de la última actualización

## Uso en Python

### Carga de TRM
```python
from trm_config import load_trm

trm_data = load_trm()
usd_rate = trm_data['usd']  # 4000.0
eur_rate = trm_data['eur']  # 4700.0
```

### Guardado de TRM
```python
from trm_config import save_trm

save_trm(usd=4000.0, eur=4700.0)
```

## Ejemplos de Uso

### Conversión de Monedas
```python
# Ejemplo de conversión
def convertir_a_cop(valor_usd, valor_eur, trm_usd, trm_eur):
    if valor_usd:
        return valor_usd * trm_usd
    elif valor_eur:
        return valor_eur * trm_eur
    return 0
```

### Validación de TRM
```python
def validar_trm(usd, eur):
    if usd is not None and (not isinstance(usd, (int, float)) or usd <= 0):
        raise ValueError("TRM USD debe ser un número positivo")
    if eur is not None and (not isinstance(eur, (int, float)) or eur <= 0):
        raise ValueError("TRM EUR debe ser un número positivo")
    return True
```

## Consideraciones Técnicas

### Seguridad
- Validación tanto en frontend como backend
- Sanitización de inputs
- Manejo de errores robusto

### Rendimiento
- Carga asíncrona de TRM
- Validación en tiempo real sin bloqueos
- Persistencia eficiente en JSON

### Usabilidad
- Interfaz intuitiva y moderna
- Feedback visual inmediato
- Mensajes de error claros y específicos

## Mantenimiento

### Actualización de TRM
- Los usuarios pueden actualizar las TRM en cualquier momento
- No es necesario reiniciar el sistema
- Los cambios se aplican inmediatamente

### Backup de Configuración
- El archivo `trm_config.json` se puede respaldar
- Contiene timestamp de última actualización
- Formato JSON estándar para fácil manipulación

## Troubleshooting

### Problemas Comunes

1. **TRM no se guarda**
   - Verificar permisos de escritura en el directorio
   - Revisar logs de error en consola del navegador

2. **Valores no válidos**
   - Asegurar que los valores sean números positivos
   - Verificar formato decimal (usar punto, no coma)

3. **Interfaz no responde**
   - Verificar conexión JavaScript
   - Revisar errores en consola del navegador

### Logs de Debug
- Los errores se registran en la consola del navegador
- El backend registra errores en los logs del servidor
- Se pueden habilitar logs adicionales modificando el código
