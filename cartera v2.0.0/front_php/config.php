<?php
// Configuración global del sistema
define('PYTHON_EXE', 'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'); // Ruta completa de Python
define('MAX_FILE_SIZE', 10 * 1024 * 1024); // 10MB
define('ALLOWED_EXTENSIONS', ['xlsx', 'xls', 'csv']);

// Configuración de directorios
define('PROCESSED_DIR', __DIR__ . '/PROVCA_PROCESADOS/');
define('TEMP_DIR', __DIR__ . '/temp/');

// Función para verificar permisos
function checkPermissions() {
    $errors = [];
    
    // Verificar directorio de archivos procesados
    if (!is_dir(PROCESSED_DIR)) {
        if (!mkdir(PROCESSED_DIR, 0755, true)) {
            $errors[] = 'No se pudo crear el directorio de archivos procesados';
        }
    } elseif (!is_writable(PROCESSED_DIR)) {
        $errors[] = 'El directorio de archivos procesados no tiene permisos de escritura';
    }
    
    // Verificar directorio temporal
    if (!is_writable(TEMP_DIR)) {
        $errors[] = 'El directorio temporal no tiene permisos de escritura';
    }
    
    // Verificar si Python está disponible
    $python_check = shell_exec(PYTHON_EXE . ' --version 2>&1');
    if (strpos($python_check, 'Python') === false) {
        $errors[] = 'Python no está disponible o no está en el PATH';
    }
    
    return $errors;
}

// Función para limpiar archivos temporales
function cleanupTempFiles() {
    if (!is_dir(TEMP_DIR)) {
        mkdir(TEMP_DIR, 0755, true);
    }
    
    $temp_files = glob(TEMP_DIR . '/*.xlsx');
    $temp_files = array_merge($temp_files, glob(TEMP_DIR . '/*.xls'));
    $temp_files = array_merge($temp_files, glob(TEMP_DIR . '/*.csv'));
    
    foreach ($temp_files as $file) {
        $age = time() - filemtime($file);
        if ($age > 3600) { // Eliminar archivos más antiguos de 1 hora
            @unlink($file);
        }
    }
}

// Función para validar archivo
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

// Función para formatear tamaño de archivo
function formatFileSize($bytes) {
    $units = ['B', 'KB', 'MB', 'GB'];
    $bytes = max($bytes, 0);
    $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
    $pow = min($pow, count($units) - 1);
    
    $bytes /= pow(1024, $pow);
    
    return round($bytes, 2) . ' ' . $units[$pow];
}

// Función para ejecutar comando Python de forma segura
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

// Función para crear respuesta JSON
function jsonResponse($data, $status_code = 200) {
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

// Función para manejar errores
function handleError($error, $status_code = 500) {
    echo json_encode(['error' => $error]);
    exit;
}

// Inicialización
cleanupTempFiles();
?> 