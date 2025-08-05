# Sistema de Procesamiento de Cartera - Grupo Planeta

## 🚀 Versión 2.0 - Sistema Completo e Interactivo

### 📋 Descripción General

El Sistema de Procesamiento de Cartera es una plataforma integral desarrollada para el Grupo Planeta que permite procesar archivos financieros de manera individual, con alertas de éxito, limpieza automática y una interfaz moderna e interactiva.

### ✨ Características Principales

#### 🎯 **Subida Individual de Archivos**
- **Formato Deuda**: Procesamiento completo con provisión, anticipos, balance y focus
- **Balance Completo**: Análisis de archivos de balance, situación y focus
- **Cartera**: Procesamiento de archivos de cartera con validaciones
- **Anticipos**: Análisis detallado de archivos de anticipos

#### 🔔 **Sistema de Alertas y Notificaciones**
- Notificaciones en tiempo real de éxito/error
- Barra de progreso animada durante el procesamiento
- Alertas visuales con iconos y colores diferenciados
- Duración configurable de notificaciones (5 segundos por defecto)

#### 🧹 **Limpieza Automática**
- Eliminación automática de archivos después de 7 días
- Script de limpieza programable (cron job)
- Logs detallados de limpieza
- Liberación automática de espacio en disco

#### 🎨 **Interfaz Moderna e Interactiva**
- Diseño responsive y moderno
- Animaciones suaves y transiciones
- Paleta de colores corporativa
- Iconografía FontAwesome
- Efectos hover y feedback visual

### 📁 Estructura del Proyecto

```
cartera/
├── index.php                          # Página principal con nueva interfaz
├── config.php                         # Configuración centralizada
├── limpiar_archivos.php              # Script de limpieza automática
├── procesar_formato_deuda.php        # Procesador de formato deuda
├── procesar_balance.php              # Procesador de balance
├── procesar_cartera.php              # Procesador de cartera
├── procesar_anticipos.php            # Procesador de anticipos
├── front_php/                        # Archivos de interfaz
│   ├── styles.css                    # Estilos CSS modernos
│   ├── dashboard.php                 # Dashboard administrativo
│   └── configuracion.php            # Configuración del sistema
├── PROVCA/                          # Scripts de Python
│   ├── procesador_formato_deuda.py
│   ├── procesador_balance_completo.py
│   ├── procesador_cartera.py
│   └── procesador_anticipos.py
├── temp/                            # Archivos temporales
├── resultados/                      # Archivos procesados
├── logs/                           # Logs del sistema
└── AN/                             # Documentación y archivos de ejemplo
```

### 🛠️ Instalación y Configuración

#### Requisitos del Sistema
- **PHP**: 7.4 o superior
- **Python**: 3.7 o superior
- **Servidor Web**: Apache/Nginx
- **Extensiones PHP**: fileinfo, json, mbstring

#### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd cartera
   ```

2. **Configurar permisos**
   ```bash
   chmod 755 temp/
   chmod 755 resultados/
   chmod 755 logs/
   ```

3. **Instalar dependencias de Python**
   ```bash
   cd PROVCA
   pip install -r requirements.txt
   ```

4. **Configurar limpieza automática (opcional)**
   ```bash
   # Agregar al crontab para ejecutar diariamente a las 2:00 AM
   0 2 * * * /usr/bin/php /ruta/al/proyecto/limpiar_archivos.php
   ```

### 🎮 Uso del Sistema

#### 1. **Acceso al Sistema**
- Abrir el navegador y dirigirse a `http://localhost/cartera/`
- La interfaz principal muestra las opciones de procesamiento

#### 2. **Procesamiento de Archivos**

**Formato Deuda:**
- Hacer clic en "Seleccionar Archivo" en la tarjeta de Formato Deuda
- Elegir archivo Excel o CSV
- Hacer clic en "Procesar Formato Deuda"
- Esperar la notificación de éxito

**Balance Completo:**
- Hacer clic en "Seleccionar Archivo" en la tarjeta de Balance
- Elegir archivo de balance, situación o focus
- Hacer clic en "Procesar Balance"
- Recibir notificación de procesamiento exitoso

**Cartera:**
- Seleccionar archivo de cartera
- Procesar con validaciones automáticas
- Recibir resultado procesado

**Anticipos:**
- Subir archivo de anticipos
- Procesar con análisis detallado
- Obtener reporte final

#### 3. **Visualización de Resultados**
- Los archivos procesados se guardan en `resultados/`
- Acceder a "Ver Resultados" desde la interfaz
- Descargar archivos procesados

### ⚙️ Configuración Avanzada

#### Archivo `config.php`
```php
// Configuración de archivos
define('MAX_FILE_SIZE', 50 * 1024 * 1024); // 50MB
define('RETENTION_DAYS', 7); // Días de retención

// Configuración de Python
define('PYTHON_PATH', 'python');
define('PYTHON_PATH_ALT', 'python3');
```

#### Personalización de Estilos
- Editar `front_php/styles.css` para cambiar colores y estilos
- Variables CSS disponibles para personalización
- Diseño responsive incluido

### 📊 Monitoreo y Logs

#### Logs del Sistema
- **Log principal**: `logs/sistema.log`
- **Log de errores**: `logs/errores.log`
- **Log de limpieza**: `logs/limpieza.log`

#### Estadísticas en Tiempo Real
- Total de archivos en el sistema
- Archivos procesados en las últimas 24 horas
- Espacio utilizado en directorios
- Estado de limpieza automática

### 🔒 Seguridad

#### Validaciones Implementadas
- **Tipo de archivo**: Solo Excel (.xlsx, .xls) y CSV (.csv)
- **Tamaño máximo**: 50MB por archivo
- **Validación MIME**: Verificación de tipo de archivo
- **Sanitización**: Nombres de archivo únicos y seguros

#### Medidas de Seguridad
- Limpieza automática de archivos temporales
- Logs de auditoría de todas las operaciones
- Validación de permisos de escritura
- Manejo seguro de errores

### 🚀 Características Técnicas

#### Frontend
- **HTML5** semántico
- **CSS3** con variables personalizadas
- **JavaScript** vanilla para interactividad
- **FontAwesome** para iconografía
- **Responsive Design** para todos los dispositivos

#### Backend
- **PHP 7.4+** para procesamiento
- **Python 3.7+** para análisis de datos
- **JSON** para comunicación AJAX
- **Sistema de logs** integrado

#### Procesamiento
- **Validación en tiempo real**
- **Progreso visual** durante procesamiento
- **Manejo de errores** robusto
- **Limpieza automática** de archivos

### 📈 Mejoras en la Versión 2.0

#### Nuevas Funcionalidades
- ✅ Subida individual de archivos
- ✅ Alertas de éxito en tiempo real
- ✅ Sistema de limpieza automática (7 días)
- ✅ Interfaz moderna e interactiva
- ✅ Estadísticas en tiempo real
- ✅ Logs detallados del sistema
- ✅ Configuración centralizada
- ✅ Validaciones mejoradas

#### Mejoras de UX/UI
- ✅ Diseño responsive completo
- ✅ Animaciones suaves
- ✅ Feedback visual inmediato
- ✅ Notificaciones elegantes
- ✅ Paleta de colores corporativa
- ✅ Iconografía moderna

### 🛠️ Mantenimiento

#### Limpieza Manual
```bash
# Ejecutar limpieza manual
php limpiar_archivos.php
```

#### Verificación de Logs
```bash
# Ver logs del sistema
tail -f logs/sistema.log

# Ver logs de errores
tail -f logs/errores.log
```

#### Monitoreo de Espacio
- El sistema muestra estadísticas de uso
- Limpieza automática cada 7 días
- Logs de espacio liberado

### 📞 Soporte

#### Información de Contacto
- **Empresa**: Grupo Planeta
- **Sistema**: Procesamiento de Cartera v2.0
- **Soporte Técnico**: [Contacto del equipo de desarrollo]

#### Documentación Adicional
- `SISTEMA_FORMATO_DEUDA_COMPLETO.md` - Documentación técnica
- `PROVCA/README_INTEGRACION.md` - Guía de integración
- `AN/RESUMEN_DOCUMENTOS_AN.md` - Análisis de documentos

### 🔄 Actualizaciones Futuras

#### Próximas Mejoras Planificadas
- [ ] Dashboard administrativo avanzado
- [ ] Reportes automáticos por email
- [ ] Integración con sistemas externos
- [ ] API REST para integraciones
- [ ] Múltiples formatos de salida
- [ ] Procesamiento en lote

---

**© 2025 Grupo Planeta. Todos los derechos reservados.**

*Sistema de Procesamiento de Cartera - Versión 2.0* 