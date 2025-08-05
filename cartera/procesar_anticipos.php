<?php
session_start();
header('Content-Type: application/json');

// Incluir configuración centralizada
require_once 'config.php';

try {
    // Limpiar archivos antiguos
    limpiarArchivosAntiguos(DIR_TEMP);
    limpiarArchivosAntiguos(DIR_RESULTADOS);
    
    // Verificar si se recibió un archivo
    if (!isset($_FILES['archivo'])) {
        throw new Exception('No se recibió ningún archivo');
    }

    $archivo = $_FILES['archivo'];
    
    // Validar archivo usando la función mejorada
    $errores = validarArchivo($archivo);
    if (!empty($errores)) {
        throw new Exception(implode('; ', $errores));
    }

    $nombreOriginal = $archivo['name'];
    $tamanoArchivo = $archivo['size'];
    $archivoTemporal = $archivo['tmp_name'];
    $extension = strtolower(pathinfo($nombreOriginal, PATHINFO_EXTENSION));

    // Generar nombre único para el archivo
    $nombreUnico = generarNombreUnico('anticipos', $extension);
    $rutaDestino = DIR_TEMP . $nombreUnico;

    // Mover archivo subido al directorio temporal
    if (!move_uploaded_file($archivoTemporal, $rutaDestino)) {
        escribirErrorLog("Error al mover archivo: $archivoTemporal a $rutaDestino");
        throw new Exception('Error al guardar el archivo en el servidor');
    }

    escribirLog("Archivo anticipos subido: $nombreOriginal -> $rutaDestino");

    // Ejecutar script de Python para procesar anticipos
    try {
        $output = ejecutarScriptPython(SCRIPT_ANTICIPOS, $rutaDestino);
        escribirLog("Procesamiento de anticipos completado para: $nombreOriginal");
    } catch (Exception $e) {
        // Limpiar archivo temporal en caso de error
        if (file_exists($rutaDestino)) {
            unlink($rutaDestino);
        }
        throw $e;
    }

    // Buscar archivo de resultado generado
    $timestamp = date('Y-m-d_H-i-s');
    $archivosResultado = glob(DIR_RESULTADOS . '*anticipos*' . $timestamp . '*');
    $archivoResultado = null;
    
    if (!empty($archivosResultado)) {
        $archivoResultado = $archivosResultado[0];
        escribirLog("Archivo de resultado encontrado: " . basename($archivoResultado));
    } else {
        escribirLog("No se encontró archivo de resultado para: $nombreOriginal");
    }

    // Preparar respuesta de éxito
    $respuesta = [
        'success' => true,
        'message' => 'Archivo de anticipos procesado exitosamente',
        'data' => [
            'archivo_original' => $nombreOriginal,
            'archivo_procesado' => $archivoResultado ? basename($archivoResultado) : null,
            'tamano_archivo' => formatBytes($tamanoArchivo),
            'timestamp' => $timestamp,
            'tipo_procesamiento' => 'Anticipos',
            'ruta_resultado' => $archivoResultado ? $archivoResultado : null
        ]
    ];

    // Limpiar archivo temporal después de procesar
    if (file_exists($rutaDestino)) {
        if (unlink($rutaDestino)) {
            escribirLog("Archivo temporal eliminado: $rutaDestino");
        } else {
            escribirErrorLog("No se pudo eliminar archivo temporal: $rutaDestino");
        }
    }

    echo json_encode($respuesta);

} catch (Exception $e) {
    escribirErrorLog("Error en procesamiento de anticipos: " . $e->getMessage(), $e);
    
    $respuesta = [
        'success' => false,
        'message' => $e->getMessage(),
        'error' => true,
        'error_type' => 'processing_error'
    ];
    
    echo json_encode($respuesta);
}
?> 