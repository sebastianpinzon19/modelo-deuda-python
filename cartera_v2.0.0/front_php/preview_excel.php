<?php
require_once 'config.php';

// Verificar permisos del sistema
$permission_errors = checkPermissions();
if (!empty($permission_errors)) {
    handleError('Problemas de configuración: ' . implode(', ', $permission_errors));
}

// Verificar que se recibió un archivo
if (!isset($_FILES['archivo']) || $_FILES['archivo']['error'] !== UPLOAD_ERR_OK) {
    handleError('No se recibió el archivo correctamente');
}

$archivo = $_FILES['archivo'];

// Validar archivo
$validation_errors = validateFile($archivo);
if (!empty($validation_errors)) {
    handleError(implode(', ', $validation_errors));
}

try {
    // Asegurar que el directorio temporal existe
    if (!is_dir(TEMP_DIR)) {
        mkdir(TEMP_DIR, 0755, true);
    }
    
    // Usar directorio temporal del proyecto
    $ruta_temporal = TEMP_DIR . uniqid() . "_" . $archivo['name'];
    
    // Log para debugging
    error_log("Preview: Archivo temporal: " . $ruta_temporal);
    
    if (!move_uploaded_file($archivo['tmp_name'], $ruta_temporal)) {
        throw new Exception('Error al mover el archivo temporal');
    }

    // Ejecutar script Python para previsualización
    $python_script = __DIR__ . "/PROVCA/preview_excel.py";
    error_log("Preview: Script Python: " . $python_script);
    
    $output = executePythonScript($python_script, [$ruta_temporal]);
    error_log("Preview: Salida Python: " . substr($output, 0, 500));

    // Limpiar archivo temporal
    if (file_exists($ruta_temporal)) {
        unlink($ruta_temporal);
    }

    // Decodificar respuesta JSON del script Python
    $resultado = json_decode($output, true);
    
    if ($resultado === null) {
        throw new Exception('Error al procesar la previsualización: ' . $output);
    }

    jsonResponse($resultado);

} catch (Exception $e) {
    handleError('Error: ' . $e->getMessage());
}
?> 