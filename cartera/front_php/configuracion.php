<?php
/**
 * Configuración Global del Sistema de Procesamiento de Cartera
 * Grupo Planeta - Sistema de Análisis Financiero
 * Versión: 2.0.1
 * 
 * Configuración mejorada para integración con el nuevo sistema Python modular
 */

// =============================================================================
// CONFIGURACIÓN DE PYTHON
// =============================================================================

// Detección automática de Python
function detectarPython() {
    $rutas_posibles = [
        'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe',
        'C:\\Python313\\python.exe',
        'C:\\Python312\\python.exe',
        'C:\\Python311\\python.exe',
        'C:\\Python310\\python.exe',
        'C:\\Python39\\python.exe',
        'C:\\Python38\\python.exe',
        'python.exe',
        'python3.exe',
        'python'
    ];
    
    foreach ($rutas_posibles as $ruta) {
        if (file_exists($ruta)) {
            $output = shell_exec("\"$ruta\" --version 2>&1");
            if (strpos($output, 'Python') !== false) {
                return $ruta;
            }
        }
    }
    
    // Intentar con PATH
    $output = shell_exec('python --version 2>&1');
    if (strpos($output, 'Python') !== false) {
        return 'python';
    }
    
    $output = shell_exec('python3 --version 2>&1');
    if (strpos($output, 'Python') !== false) {
        return 'python3';
    }
    
    return null;
}

// Configuración de Python
define('PYTHON_EXE', detectarPython() ?: 'python');
define('PYTHON_DIR', __DIR__ . '/../PROVCA/');
define('ORQUESTADOR_PRINCIPAL', PYTHON_DIR . 'orquestador_principal.py');

// =============================================================================
// CONFIGURACIÓN DEL SISTEMA
// =============================================================================

define('MAX_FILE_SIZE', 50 * 1024 * 1024); // 50MB
define('ALLOWED_EXTENSIONS', ['xlsx', 'xls', 'csv']);
define('SYSTEM_VERSION', '2.0.1');

// =============================================================================
// CONFIGURACIÓN DE DIRECTORIOS
// =============================================================================

define('BASE_DIR', __DIR__ . '/../');
define('PROCESSED_DIR', BASE_DIR . 'resultados/');
define('TEMP_DIR', BASE_DIR . 'temp/');
define('LOGS_DIR', BASE_DIR . 'logs/');
define('PYTHON_LOGS_DIR', PYTHON_DIR . 'logs/');

// =============================================================================
// CONFIGURACIÓN DE PROCESAMIENTO
// =============================================================================

define('TIPOS_PROCESAMIENTO', [
    'cartera' => 'Procesamiento de Cartera',
    'acumulado' => 'Procesamiento de Acumulado',
    'balance' => 'Procesamiento de Balance',
    'formato_deuda' => 'Formato de Deuda',
    'anticipos' => 'Procesamiento de Anticipos',
    'balance_especifico' => 'Balance Específico',
    'situacion_especifico' => 'Situación Específica',
    'focus_especifico' => 'Focus Específico',
    'dotacion_mes' => 'Dotación por Mes',
    'tipos_cambio' => 'Tipos de Cambio'
]);

// =============================================================================
// FUNCIONES DE UTILIDAD
// =============================================================================

/**
 * Verificar permisos y configuración del sistema
 */
function checkPermissions() {
    $errors = [];
    
    // Verificar Python
    if (!detectarPython()) {
        $errors[] = 'Python no está disponible. Verifique la instalación.';
    }
    
    // Verificar directorios
    $directorios = [PROCESSED_DIR, TEMP_DIR, LOGS_DIR, PYTHON_LOGS_DIR];
    foreach ($directorios as $dir) {
        if (!is_dir($dir)) {
            if (!mkdir($dir, 0755, true)) {
                $errors[] = "No se pudo crear el directorio: $dir";
            }
        } elseif (!is_writable($dir)) {
            $errors[] = "El directorio no tiene permisos de escritura: $dir";
        }
    }
    
    // Verificar orquestador principal
    if (!file_exists(ORQUESTADOR_PRINCIPAL)) {
        $errors[] = 'No se encontró el orquestador principal de Python';
    }
    
    // Verificar dependencias Python
    $requirements_file = PYTHON_DIR . 'requirements.txt';
    if (file_exists($requirements_file)) {
        $output = shell_exec(PYTHON_EXE . ' -c "import pandas, numpy, openpyxl" 2>&1');
        if (strpos($output, 'ImportError') !== false || strpos($output, 'ModuleNotFoundError') !== false) {
            $errors[] = 'Faltan dependencias de Python. Ejecute: pip install -r requirements.txt';
        }
    }
    
    return $errors;
}

/**
 * Limpiar archivos temporales
 */
function cleanupTempFiles() {
    if (!is_dir(TEMP_DIR)) {
        mkdir(TEMP_DIR, 0755, true);
    }
    
    $temp_files = glob(TEMP_DIR . '/*.*');
    foreach ($temp_files as $file) {
        $age = time() - filemtime($file);
        if ($age > 3600) { // Eliminar archivos más antiguos de 1 hora
            @unlink($file);
        }
    }
}

/**
 * Validar archivo subido
 */
function validateFile($file) {
    $errors = [];
    
    if (!isset($file['tmp_name']) || !is_uploaded_file($file['tmp_name'])) {
        $errors[] = 'Archivo no válido';
        return $errors;
    }
    
    $extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    if (!in_array($extension, ALLOWED_EXTENSIONS)) {
        $errors[] = 'Tipo de archivo no permitido. Solo se permiten: ' . implode(', ', ALLOWED_EXTENSIONS);
    }
    
    if ($file['size'] > MAX_FILE_SIZE) {
        $errors[] = 'El archivo es demasiado grande. Máximo ' . formatFileSize(MAX_FILE_SIZE);
    }
    
    return $errors;
}

/**
 * Formatear tamaño de archivo
 */
function formatFileSize($bytes) {
    $units = ['B', 'KB', 'MB', 'GB'];
    $bytes = max($bytes, 0);
    $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
    $pow = min($pow, count($units) - 1);
    
    $bytes /= pow(1024, $pow);
    
    return round($bytes, 2) . ' ' . $units[$pow];
}

/**
 * Ejecutar comando Python usando el orquestador principal
 */
function executePythonOrchestrator($tipo_procesamiento, $archivos = [], $opciones = []) {
    $cmd = PYTHON_EXE . ' ' . escapeshellarg(ORQUESTADOR_PRINCIPAL);
    $cmd .= ' --tipo ' . escapeshellarg($tipo_procesamiento);
    
    // Agregar archivos
    foreach ($archivos as $archivo) {
        $cmd .= ' --archivo ' . escapeshellarg($archivo);
    }
    
    // Agregar opciones
    foreach ($opciones as $key => $value) {
        $cmd .= ' --' . escapeshellarg($key) . ' ' . escapeshellarg($value);
    }
    
    $cmd .= ' --formato json 2>&1';
    
    $output = shell_exec($cmd);
    
    if ($output === null) {
        throw new Exception('Error al ejecutar el orquestador Python');
    }
    
    // Intentar parsear JSON
    $json_start = strpos($output, '{');
    if ($json_start !== false) {
        $json_output = substr($output, $json_start);
        $result = json_decode($json_output, true);
        if ($result !== null) {
            return $result;
        }
    }
    
    // Si no es JSON válido, devolver el output completo
    return [
        'success' => false,
        'output' => $output,
        'error' => 'No se pudo parsear la respuesta JSON'
    ];
}

/**
 * Ejecutar script Python específico (método legacy)
 */
function executePythonScript($script_path, $args = []) {
    $cmd = PYTHON_EXE . ' ' . escapeshellarg($script_path);
    
    foreach ($args as $arg) {
        $cmd .= ' ' . escapeshellarg($arg);
    }
    
    $cmd .= ' 2>&1';
    
    $output = shell_exec($cmd);
    
    if ($output === null) {
        throw new Exception('Error al ejecutar el script Python');
    }
    
    return $output;
}

/**
 * Crear respuesta JSON
 */
function jsonResponse($data, $status_code = 200) {
    http_response_code($status_code);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

/**
 * Manejar errores
 */
function handleError($error, $status_code = 500) {
    $response = [
        'success' => false,
        'error' => $error,
        'timestamp' => date('Y-m-d H:i:s'),
        'version' => SYSTEM_VERSION
    ];
    
    jsonResponse($response, $status_code);
}

/**
 * Obtener información del sistema
 */
function getSystemInfo() {
    return [
        'version' => SYSTEM_VERSION,
        'python_path' => PYTHON_EXE,
        'python_version' => shell_exec(PYTHON_EXE . ' --version 2>&1'),
        'orquestador_exists' => file_exists(ORQUESTADOR_PRINCIPAL),
        'directories' => [
            'base' => BASE_DIR,
            'python' => PYTHON_DIR,
            'processed' => PROCESSED_DIR,
            'temp' => TEMP_DIR,
            'logs' => LOGS_DIR
        ],
        'permissions' => checkPermissions()
    ];
}

/**
 * Log de actividad
 */
function logActivity($action, $details = []) {
    $log_file = LOGS_DIR . 'php_activity.log';
    $timestamp = date('Y-m-d H:i:s');
    $user_ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';
    
    $log_entry = [
        'timestamp' => $timestamp,
        'action' => $action,
        'user_ip' => $user_ip,
        'user_agent' => $user_agent,
        'details' => $details
    ];
    
    $log_line = json_encode($log_entry, JSON_UNESCAPED_UNICODE) . "\n";
    file_put_contents($log_file, $log_line, FILE_APPEND | LOCK_EX);
}

// =============================================================================
// INICIALIZACIÓN
// =============================================================================

// Crear directorios necesarios
$directorios = [PROCESSED_DIR, TEMP_DIR, LOGS_DIR, PYTHON_LOGS_DIR];
foreach ($directorios as $dir) {
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }
}

// Limpiar archivos temporales
cleanupTempFiles();

// Log de inicialización
logActivity('system_init', ['version' => SYSTEM_VERSION]);
?> 