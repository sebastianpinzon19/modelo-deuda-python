<?php
session_start();
header('Content-Type: application/json');
require_once '../config.php';

try {
    if (!isset($_FILES['archivo']) || $_FILES['archivo']['error'] !== UPLOAD_ERR_OK) {
        throw new Exception('No se ha subido ningún archivo o hubo un error en la subida.');
    }

    $archivo = $_FILES['archivo'];
    $nombreOriginal = $archivo['name'];
    $extension = strtolower(pathinfo($nombreOriginal, PATHINFO_EXTENSION));

    if (!in_array($extension, ['xlsx', 'xls', 'csv'])) {
        throw new Exception('Formato de archivo no válido. Solo se permiten archivos Excel (.xlsx, .xls) y CSV.');
    }

    $nombreUnico = generarNombreUnico('focus_especifico', $extension);
    $rutaDestino = DIR_TEMP . $nombreUnico;

    if (!move_uploaded_file($archivo['tmp_name'], $rutaDestino)) {
        throw new Exception('Error al mover el archivo subido.');
    }

    escribirLog("Archivo focus específico subido: $nombreOriginal -> $nombreUnico");

    $output = ejecutarScriptPython(SCRIPT_FOCUS_ESPECIFICO, $rutaDestino);
    
    if ($output['success']) {
        escribirLog("Focus específico procesado exitosamente: " . $output['message']);
        
        echo json_encode([
            'success' => true,
            'message' => 'Archivo de Focus procesado exitosamente. ' . $output['message'],
            'data' => [
                'archivo_original' => $nombreOriginal,
                'archivo_procesado' => $nombreUnico,
                'tipo' => 'focus_especifico'
            ]
        ]);
    } else {
        throw new Exception('Error en el procesamiento: ' . $output['message']);
    }

} catch (Exception $e) {
    escribirLog("Error en procesar_focus_especifico.php: " . $e->getMessage());
    
    echo json_encode([
        'success' => false,
        'message' => 'Error al procesar el archivo: ' . $e->getMessage()
    ]);
}
?> 