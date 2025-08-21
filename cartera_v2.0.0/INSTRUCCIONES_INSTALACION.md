# 🚀 Instalación del Sistema de Gestión de Cartera v2.0.0

## 📋 Requisitos Previos

### Sistema Operativo
- **Windows 10/11** (Recomendado)
- **Windows 8.1** (Compatible)
- **Windows 7** (Limitado)

### Software Requerido
- **Python 3.8 o superior**
- **pip** (incluido con Python)
- **Navegador web moderno** (Chrome, Firefox, Edge)

## 🔧 Instalación Paso a Paso

### Paso 1: Instalar Python

1. **Descargar Python**:
   - Ve a: https://python.org/downloads/
   - Descarga la versión más reciente (3.8+)

2. **Instalar Python**:
   - Ejecuta el instalador descargado
   - **IMPORTANTE**: Marca la casilla "Add Python to PATH"
   - Selecciona "Install Now" (instalación estándar)

3. **Verificar instalación**:
   - Abre PowerShell o CMD
   - Ejecuta: `python --version`
   - Deberías ver algo como: `Python 3.11.0`

### Paso 2: Instalar el Sistema

#### Opción A: Instalación Automática (Recomendada)

1. **Descargar el sistema**:
   - Copia todos los archivos a una carpeta
   - Ejemplo: `C:\SistemaCartera\`

2. **Ejecutar instalador**:
   - Haz doble clic en `instalar_sistema.bat`
   - Espera a que termine la instalación
   - El script hará todo automáticamente

3. **Verificar instalación**:
   - Deberías ver: "🎉 INSTALACION COMPLETADA EXITOSAMENTE"

#### Opción B: Instalación Manual

1. **Abrir terminal**:
   - Presiona `Win + R`
   - Escribe `cmd` y presiona Enter

2. **Navegar al directorio**:
   ```cmd
   cd C:\ruta\al\sistema
   ```

3. **Instalar dependencias**:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Ejecutar pruebas**:
   ```cmd
   python test_sistema.py
   ```

## 🚀 Iniciar el Sistema

### Método 1: Script Automático
```cmd
iniciar_sistema.bat
```

### Método 2: Manual
```cmd
python app.py
```

### Verificar que Funciona
1. Abre tu navegador
2. Ve a: `http://localhost:5000`
3. Deberías ver la interfaz del sistema

## 📁 Estructura del Sistema

```
cartera_v2.0.0/
├── app.py                    # Aplicación principal
├── config.py                 # Configuración
├── utils.py                  # Utilidades
├── requirements.txt          # Dependencias
├── instalar_sistema.bat      # Instalador automático
├── iniciar_sistema.bat       # Iniciador automático
├── test_sistema.py           # Pruebas del sistema
├── templates/
│   └── index.html           # Interfaz web
├── uploads/                  # Archivos temporales
├── outputs/                  # Archivos procesados
└── PROVCA/                   # Módulos de procesamiento
    ├── procesador_cartera.py
    ├── procesador_anticipos.py
    ├── modelo_deuda.py
    ├── procesador_unificado.py
    └── trm_config.py
```

## 🔧 Configuración

### Variables de Entorno (Opcional)
```cmd
set FLASK_CONFIG=production
set FLASK_PORT=8080
```

### Configuración TRM
Las tasas de cambio se guardan automáticamente en:
```
PROVCA/trm_config.json
```

## 🐛 Solución de Problemas

### Error: "Python no está instalado"
**Solución**:
1. Instala Python desde https://python.org
2. Asegúrate de marcar "Add Python to PATH"
3. Reinicia la terminal

### Error: "No se pudieron instalar las dependencias"
**Soluciones**:
1. **Actualizar pip**:
   ```cmd
   python -m pip install --upgrade pip
   ```

2. **Ejecutar como administrador**:
   - Clic derecho en CMD/PowerShell
   - "Ejecutar como administrador"

3. **Verificar conexión a internet**

### Error: "Puerto 5000 en uso"
**Soluciones**:
1. **Cambiar puerto**:
   ```cmd
   set FLASK_PORT=8080
   python app.py
   ```

2. **Matar proceso**:
   ```cmd
   netstat -ano | findstr :5000
   taskkill /PID [PID] /F
   ```

### Error: "Módulo no encontrado"
**Solución**:
1. Verificar que estás en el directorio correcto
2. Ejecutar: `python test_sistema.py`
3. Reinstalar dependencias: `pip install -r requirements.txt`

## 📞 Soporte Técnico

### Logs del Sistema
Los logs se muestran en la consola donde ejecutas la aplicación:
```
🚀 Iniciando Sistema de Gestión de Cartera - Grupo Planeta
📊 Versión 2.0.0 - Aplicación Web Python
🌐 Servidor disponible en: http://localhost:5000
```

### Información de Debug
- **Archivo de configuración**: `config.py`
- **Logs detallados**: Consola de la aplicación
- **Archivos temporales**: Carpeta `uploads/`
- **Archivos procesados**: Carpeta `outputs/`

## 🔄 Actualizaciones

### Actualizar el Sistema
1. Descargar nueva versión
2. Reemplazar archivos
3. Ejecutar: `pip install -r requirements.txt`
4. Reiniciar aplicación

### Actualizar Dependencias
```cmd
pip install --upgrade -r requirements.txt
```

## 🚀 Despliegue en Producción

### Usando Gunicorn (Recomendado)
```cmd
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Usando Waitress (Windows)
```cmd
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## ✅ Verificación Final

Después de la instalación, ejecuta:
```cmd
python test_sistema.py
```

Deberías ver:
```
🎉 ¡Todas las pruebas pasaron exitosamente!
✅ El sistema está listo para usar
```

## 📚 Documentación Adicional

- **README_SISTEMA_PYTHON.md**: Documentación completa del sistema
- **test_sistema.py**: Pruebas automatizadas
- **config.py**: Configuración del sistema
- **utils.py**: Funciones auxiliares

---

**¡El sistema está listo para usar! 🎉**

Para cualquier problema, revisa los logs en la consola y consulta esta documentación.
