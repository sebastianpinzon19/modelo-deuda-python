<?php
/**
 * Configuración centralizada del Sistema de Procesamiento de Cartera
 * Grupo Planeta
 */

// Configuración general
define('SISTEMA_NOMBRE', 'Sistema de Procesamiento de Cartera');
define('SISTEMA_VERSION', '2.0');
define('SISTEMA_EMPRESA', 'Grupo Planeta');

// Configuración de directorios
define('DIR_TEMP', 'temp/');
define('DIR_RESULTADOS', 'resultados/');
define('DIR_LOGS', 'logs/');
define('DIR_PYTHON', 'PROVCA/');

// Configuración de archivos
define('MAX_FILE_SIZE', 50 * 1024 * 1024); // 50MB
define('ALLOWED_EXTENSIONS', ['xlsx', 'xls', 'csv']);
define('RETENTION_DAYS', 7);

// Configuración de Python
define('PYTHON_PATH', 'C:\Users\USPRBA\AppData\Local\Programs\Python\Python313\python.exe');
define('PYTHON_PATH_ALT', 'python');

// Scripts de Python
define('SCRIPT_FORMATO_DEUDA', DIR_PYTHON . 'procesador_formato_deuda.py');
define('SCRIPT_BALANCE', DIR_PYTHON . 'procesador_balance_completo.py');
define('SCRIPT_CARTERA', DIR_PYTHON . 'procesador_cartera.py');
define('SCRIPT_ANTICIPOS', DIR_PYTHON . 'procesador_anticipos.py');

// Configuración de seguridad
define('SECURE_UPLOAD', true);
define('ALLOWED_MIME_TYPES', [
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/csv',
    'application/csv'
]);

// Configuración de notificaciones
define('NOTIFICATION_DURATION', 5000); // 5 segundos
define('SHOW_PROGRESS', true);

// Configuración de logs
define('LOG_ENABLED', true);
define('LOG_FILE', DIR_LOGS . 'sistema.log');
define('ERROR_LOG_FILE', DIR_LOGS . 'errores.log');

// Configuración de limpieza automática
define('AUTO_CLEANUP_ENABLED', true);
define('CLEANUP_LOG_FILE', DIR_LOGS . 'limpieza.log');

// Función para crear directorios necesarios
function crearDirectoriosNecesarios() {
    $directorios = [DIR_TEMP, DIR_RESULTADOS, DIR_LOGS];
    
    foreach ($directorios as $directorio) {
        if (!is_dir($directorio)) {
            if (!mkdir($directorio, 0755, true)) {
                throw new Exception("No se pudo crear el directorio: $directorio");
            }
            escribirLog("Directorio creado: $directorio");
        }
    }
}

// Función para validar archivo con manejo detallado de errores
function validarArchivo($archivo) {
    $errores = [];
    
    // Verificar si se recibió un archivo
    if (!isset($archivo)) {
        $errores[] = 'No se recibió ningún archivo';
        escribirErrorLog('Error de validación: No se recibió archivo');
        return $errores;
    }
    
    // Verificar errores de subida
    if ($archivo['error'] !== UPLOAD_ERR_OK) {
        $errorMessages = [
            UPLOAD_ERR_INI_SIZE => 'El archivo excede el tamaño máximo permitido por PHP',
            UPLOAD_ERR_FORM_SIZE => 'El archivo excede el tamaño máximo permitido por el formulario',
            UPLOAD_ERR_PARTIAL => 'El archivo se subió parcialmente',
            UPLOAD_ERR_NO_FILE => 'No se subió ningún archivo',
            UPLOAD_ERR_NO_TMP_DIR => 'Falta el directorio temporal',
            UPLOAD_ERR_CANT_WRITE => 'Error al escribir el archivo en disco',
            UPLOAD_ERR_EXTENSION => 'Una extensión de PHP detuvo la subida del archivo'
        ];
        
        $errorMsg = isset($errorMessages[$archivo['error']]) 
            ? $errorMessages[$archivo['error']] 
            : 'Error desconocido en la subida del archivo';
        
        $errores[] = $errorMsg;
        escribirErrorLog("Error de subida: {$archivo['error']} - $errorMsg");
        return $errores;
    }
    
    // Validar que el archivo temporal existe
    if (!file_exists($archivo['tmp_name'])) {
        $errores[] = 'El archivo temporal no existe';
        escribirErrorLog('Error de validación: Archivo temporal no existe');
        return $errores;
    }
    
    // Validar tamaño
    if ($archivo['size'] > MAX_FILE_SIZE) {
        $errores[] = 'El archivo es demasiado grande. El tamaño máximo permitido es ' . formatBytes(MAX_FILE_SIZE);
        escribirErrorLog("Error de validación: Archivo demasiado grande - " . formatBytes($archivo['size']));
    }
    
    // Validar extensión
    $extension = strtolower(pathinfo($archivo['name'], PATHINFO_EXTENSION));
    if (!in_array($extension, ALLOWED_EXTENSIONS)) {
        $errores[] = 'Tipo de archivo no permitido. Solo se aceptan archivos Excel (.xlsx, .xls) y CSV (.csv)';
        escribirErrorLog("Error de validación: Extensión no permitida - $extension");
    }
    
    // Validar tipo MIME (si está habilitado)
    if (SECURE_UPLOAD && !in_array($archivo['type'], ALLOWED_MIME_TYPES)) {
        $errores[] = 'Tipo de archivo no válido según el servidor';
        escribirErrorLog("Error de validación: Tipo MIME no permitido - {$archivo['type']}");
    }
    
    // Validar que el archivo no esté vacío
    if ($archivo['size'] === 0) {
        $errores[] = 'El archivo está vacío';
        escribirErrorLog('Error de validación: Archivo vacío');
    }
    
    return $errores;
}

// Función para generar nombre único de archivo
function generarNombreUnico($tipo, $extension) {
    $timestamp = date('Y-m-d_H-i-s');
    $uniqueId = uniqid();
    return $tipo . '_' . $timestamp . '_' . $uniqueId . '.' . $extension;
}

// Función para ejecutar script de Python con mejor manejo de errores
function ejecutarScriptPython($script, $archivo) {
    // Verificar que el script existe
    if (!file_exists($script)) {
        throw new Exception("El script de Python no existe: $script");
    }
    
    // Verificar que el archivo existe
    if (!file_exists($archivo)) {
        throw new Exception("El archivo a procesar no existe: $archivo");
    }
    
    // Verificar permisos de ejecución
    if (!is_executable($script)) {
        chmod($script, 0755);
    }
    
    $comando = PYTHON_PATH . " \"$script\" \"$archivo\" 2>&1";
    escribirLog("Ejecutando comando: $comando");
    
    $output = [];
    $returnCode = 0;
    exec($comando, $output, $returnCode);
    
    if ($returnCode !== 0) {
        // Intentar con python3 si falla
        $comando = PYTHON_PATH_ALT . " \"$script\" \"$archivo\" 2>&1";
        escribirLog("Reintentando con python3: $comando");
        exec($comando, $output, $returnCode);
        
        if ($returnCode !== 0) {
            $errorOutput = implode("\n", $output);
            escribirErrorLog("Error en script Python: $errorOutput");
            throw new Exception('Error al procesar el archivo con Python: ' . $errorOutput);
        }
    }
    
    escribirLog("Script Python ejecutado exitosamente");
    return $output;
}

// Función para formatear bytes
function formatBytes($bytes, $precision = 2) {
    $units = array('B', 'KB', 'MB', 'GB', 'TB');
    
    for ($i = 0; $bytes > 1024 && $i < count($units) - 1; $i++) {
        $bytes /= 1024;
    }
    
    return round($bytes, $precision) . ' ' . $units[$i];
}

// Función para escribir log con timestamp
function escribirLog($mensaje, $tipo = 'INFO') {
    if (!LOG_ENABLED) return;
    
    $timestamp = date('Y-m-d H:i:s');
    $logEntry = "[$timestamp] [$tipo] $mensaje\n";
    
    if (!file_put_contents(LOG_FILE, $logEntry, FILE_APPEND | LOCK_EX)) {
        error_log("Error al escribir en el log: $mensaje");
    }
}

// Función para escribir log de errores con información detallada
function escribirErrorLog($mensaje, $excepcion = null) {
    if (!LOG_ENABLED) return;
    
    $timestamp = date('Y-m-d H:i:s');
    $logEntry = "[$timestamp] [ERROR] $mensaje";
    
    if ($excepcion) {
        $logEntry .= "\nExcepción: " . $excepcion->getMessage();
        $logEntry .= "\nArchivo: " . $excepcion->getFile() . ":" . $excepcion->getLine();
        $logEntry .= "\nTrace: " . $excepcion->getTraceAsString();
    }
    
    $logEntry .= "\n";
    
    if (!file_put_contents(ERROR_LOG_FILE, $logEntry, FILE_APPEND | LOCK_EX)) {
        error_log("Error al escribir en el log de errores: $mensaje");
    }
}

// Función para limpiar archivos antiguos con logging
function limpiarArchivosAntiguos($directorio, $dias = RETENTION_DAYS) {
    if (!is_dir($directorio)) {
        escribirLog("Directorio no existe para limpieza: $directorio");
        return 0;
    }
    
    $archivos = glob($directorio . '/*');
    $tiempoLimite = time() - ($dias * 24 * 60 * 60);
    $archivosEliminados = 0;
    $espacioLiberado = 0;
    
    foreach ($archivos as $archivo) {
        if (is_file($archivo) && filemtime($archivo) < $tiempoLimite) {
            $tamanio = filesize($archivo);
            if (unlink($archivo)) {
                $archivosEliminados++;
                $espacioLiberado += $tamanio;
                escribirLog("Archivo eliminado: $archivo (" . formatBytes($tamanio) . ")");
            } else {
                escribirErrorLog("No se pudo eliminar el archivo: $archivo");
            }
        }
    }
    
    if ($archivosEliminados > 0) {
        escribirLog("Limpieza completada: $archivosEliminados archivos eliminados, " . formatBytes($espacioLiberado) . " liberados");
    }
    
    return $archivosEliminados;
}

// Función para obtener estadísticas del sistema con validación
function obtenerEstadisticasSistema() {
    $stats = [
        'total_archivos' => 0,
        'archivos_recientes' => 0,
        'espacio_temp' => '0 B',
        'espacio_resultados' => '0 B',
        'archivos_temp' => 0,
        'archivos_resultados' => 0
    ];
    
    // Contar archivos en temp
    if (is_dir(DIR_TEMP)) {
        $archivosTemp = glob(DIR_TEMP . '*');
        $stats['archivos_temp'] = count($archivosTemp);
        $stats['total_archivos'] += $stats['archivos_temp'];
        $stats['espacio_temp'] = formatBytes(calcularTamanioDirectorio(DIR_TEMP));
    }
    
    // Contar archivos en resultados
    if (is_dir(DIR_RESULTADOS)) {
        $archivosResultados = glob(DIR_RESULTADOS . '*');
        $stats['archivos_resultados'] = count($archivosResultados);
        $stats['total_archivos'] += $stats['archivos_resultados'];
        $stats['espacio_resultados'] = formatBytes(calcularTamanioDirectorio(DIR_RESULTADOS));
    }
    
    // Contar archivos recientes
    $archivos = array_merge(glob(DIR_TEMP . '*'), glob(DIR_RESULTADOS . '*'));
    foreach ($archivos as $archivo) {
        if (is_file($archivo) && filemtime($archivo) > (time() - 24 * 60 * 60)) {
            $stats['archivos_recientes']++;
        }
    }
    
    return $stats;
}

// Función para calcular tamaño de directorio
function calcularTamanioDirectorio($directorio) {
    if (!is_dir($directorio)) return 0;
    
    $tamanio = 0;
    $archivos = glob($directorio . '/*');
    
    foreach ($archivos as $archivo) {
        if (is_file($archivo)) {
            $tamanio += filesize($archivo);
        }
    }
    
    return $tamanio;
}

// Función para verificar la salud del sistema
function verificarSaludSistema() {
    $problemas = [];
    
    // Verificar directorios
    $directorios = [DIR_TEMP, DIR_RESULTADOS, DIR_LOGS];
    foreach ($directorios as $directorio) {
        if (!is_dir($directorio)) {
            $problemas[] = "Directorio faltante: $directorio";
        } elseif (!is_writable($directorio)) {
            $problemas[] = "Directorio sin permisos de escritura: $directorio";
        }
    }
    
    // Verificar scripts de Python
    $scripts = [SCRIPT_FORMATO_DEUDA, SCRIPT_BALANCE, SCRIPT_CARTERA, SCRIPT_ANTICIPOS];
    foreach ($scripts as $script) {
        if (!file_exists($script)) {
            $problemas[] = "Script faltante: $script";
        }
    }
    
    // Verificar comandos de Python
    $pythonComandos = [PYTHON_PATH, PYTHON_PATH_ALT];
    $pythonDisponible = false;
    foreach ($pythonComandos as $comando) {
        exec("$comando --version 2>&1", $output, $returnCode);
        if ($returnCode === 0) {
            $pythonDisponible = true;
            break;
        }
    }
    
    if (!$pythonDisponible) {
        $problemas[] = "Python no está disponible en el sistema";
    }
    
    return $problemas;
}

// Crear directorios necesarios al cargar la configuración
try {
    crearDirectoriosNecesarios();
} catch (Exception $e) {
    error_log("Error al crear directorios: " . $e->getMessage());
}
?> 