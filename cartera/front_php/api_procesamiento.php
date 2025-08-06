<?php
/**
 * API de Procesamiento - Sistema de Cartera Grupo Planeta
 * Versión: 2.0.1
 * 
 * Endpoint para comunicación con el orquestador Python
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Manejar preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Incluir configuración
require_once 'configuracion.php';

// Log de actividad
logActivity('api_request', [
    'method' => $_SERVER['REQUEST_METHOD'],
    'endpoint' => $_SERVER['REQUEST_URI']
]);

try {
    // Verificar método HTTP
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        throw new Exception('Método no permitido. Solo se acepta POST.');
    }
    
    // Obtener datos JSON
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    
    if ($data === null) {
        throw new Exception('Datos JSON inválidos');
    }
    
    // Validar datos requeridos
    if (!isset($data['tipo_procesamiento'])) {
        throw new Exception('Tipo de procesamiento requerido');
    }
    
    $tipo_procesamiento = $data['tipo_procesamiento'];
    $archivos = $data['archivos'] ?? [];
    $opciones = $data['opciones'] ?? [];
    
    // Validar tipo de procesamiento
    if (!array_key_exists($tipo_procesamiento, TIPOS_PROCESAMIENTO)) {
        throw new Exception('Tipo de procesamiento no válido: ' . $tipo_procesamiento);
    }
    
    // Verificar permisos del sistema
    $errores_sistema = checkPermissions();
    if (!empty($errores_sistema)) {
        throw new Exception('Errores de configuración: ' . implode(', ', $errores_sistema));
    }
    
    // Procesar archivos subidos si los hay
    if (!empty($_FILES)) {
        foreach ($_FILES as $key => $file) {
            $errores_validacion = validateFile($file);
            if (!empty($errores_validacion)) {
                throw new Exception("Error en archivo $key: " . implode(", ", $errores_validacion));
            }
            
            $nombre_archivo = $key . '_' . date('Y-m-d_H-i-s') . '.' . pathinfo($file['name'], PATHINFO_EXTENSION);
            $ruta_archivo = TEMP_DIR . $nombre_archivo;
            
            if (!move_uploaded_file($file['tmp_name'], $ruta_archivo)) {
                throw new Exception("Error al guardar el archivo $key");
            }
            
            $archivos[] = $ruta_archivo;
        }
    }
    
    // Ejecutar procesamiento
    logActivity('api_procesamiento_start', [
        'tipo' => $tipo_procesamiento,
        'archivos' => $archivos,
        'opciones' => $opciones
    ]);
    
    $resultado = executePythonOrchestrator($tipo_procesamiento, $archivos, $opciones);
    
    // Log del resultado
    logActivity('api_procesamiento_complete', [
        'tipo' => $tipo_procesamiento,
        'success' => $resultado['success'] ?? false
    ]);
    
    // Preparar respuesta
    $response = [
        'success' => true,
        'timestamp' => date('Y-m-d H:i:s'),
        'version' => SYSTEM_VERSION,
        'tipo_procesamiento' => $tipo_procesamiento,
        'resultado' => $resultado
    ];
    
    jsonResponse($response);
    
} catch (Exception $e) {
    logActivity('api_error', [
        'error' => $e->getMessage(),
        'trace' => $e->getTraceAsString()
    ]);
    
    handleError($e->getMessage(), 400);
}
?>
