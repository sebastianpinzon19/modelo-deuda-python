<?php
/**
 * Descarga de Resultados - Sistema de Cartera Grupo Planeta
 * Versión: 2.0.1
 */

// Incluir configuración
require_once 'configuracion.php';

// Log de actividad
logActivity('descarga_solicitada', [
    'archivo' => $_GET['archivo'] ?? 'no especificado',
    'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown'
]);

// Configurar headers para evitar problemas de caché
header('Cache-Control: no-cache, must-revalidate');
header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');

$archivo = isset($_GET['archivo']) ? $_GET['archivo'] : '';

// Log para debugging
error_log("Descarga solicitada para archivo: " . $archivo);

if ($archivo && file_exists($archivo)) {
    // Verificar que el archivo es un Excel válido
    $extension = strtolower(pathinfo($archivo, PATHINFO_EXTENSION));
    $extensiones_permitidas = ['xlsx', 'xls', 'csv'];
    
    if (!in_array($extension, $extensiones_permitidas)) {
        echo "Error: El archivo no es un formato válido. Solo se permiten: " . implode(', ', $extensiones_permitidas);
        error_log("Error: Archivo formato no permitido - " . $archivo);
        logActivity('descarga_error', ['error' => 'formato_no_permitido', 'archivo' => $archivo]);
        exit;
    }
    
    // Verificar que el archivo está en una carpeta permitida
    $rutas_permitidas = [
        PROCESSED_DIR,
        TEMP_DIR,
        PYTHON_DIR . 'resultados/'
    ];
    
    $archivo_permitido = false;
    foreach ($rutas_permitidas as $ruta_permitida) {
        if (strpos($archivo, $ruta_permitida) === 0) {
            $archivo_permitido = true;
            break;
        }
    }
    
    if (!$archivo_permitido) {
        echo "Error: Acceso no permitido al archivo";
        error_log("Error: Acceso no permitido - " . $archivo);
        logActivity('descarga_error', ['error' => 'acceso_no_permitido', 'archivo' => $archivo]);
        exit;
    }
    
    // Verificar que el archivo no esté vacío
    $tamano_archivo = filesize($archivo);
    if ($tamano_archivo === 0) {
        echo "Error: El archivo está vacío";
        error_log("Error: Archivo vacío - " . $archivo);
        logActivity('descarga_error', ['error' => 'archivo_vacio', 'archivo' => $archivo]);
        exit;
    }
    
    // Verificar que el archivo sea legible
    if (!is_readable($archivo)) {
        echo "Error: No se puede leer el archivo";
        error_log("Error: Archivo no legible - " . $archivo);
        logActivity('descarga_error', ['error' => 'archivo_no_legible', 'archivo' => $archivo]);
        exit;
    }
    
    // Limpiar cualquier salida previa
    while (ob_get_level()) {
        ob_end_clean();
    }
    
    // Obtener el nombre real del archivo
    $nombre_archivo = basename($archivo);
    
    // Log del archivo que se va a descargar
    error_log("Descargando archivo: " . $nombre_archivo . " desde: " . $archivo . " (tamaño: " . $tamano_archivo . " bytes)");
    
    // Configurar Content-Type según la extensión
    $content_types = [
        'xlsx' => 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'xls' => 'application/vnd.ms-excel',
        'csv' => 'text/csv'
    ];
    
    $content_type = $content_types[$extension] ?? 'application/octet-stream';
    
    // Configurar headers para descarga segura
    header('Content-Description: File Transfer');
    header('Content-Type: ' . $content_type);
    header('Content-Disposition: attachment; filename="' . $nombre_archivo . '"');
    header('Expires: 0');
    header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
    header('Pragma: public');
    header('Content-Length: ' . $tamano_archivo);
    header('Content-Transfer-Encoding: binary');
    
    // Leer y enviar el archivo en chunks para evitar problemas de memoria
    $handle = fopen($archivo, 'rb');
    if ($handle === false) {
        echo "Error: No se pudo abrir el archivo para lectura";
        error_log("Error: No se pudo abrir archivo - " . $archivo);
        logActivity('descarga_error', ['error' => 'no_se_pudo_abrir', 'archivo' => $archivo]);
        exit;
    }
    
    // Enviar archivo en chunks de 8KB
    $chunk_size = 8192;
    $bytes_sent = 0;
    
    while (!feof($handle)) {
        $chunk = fread($handle, $chunk_size);
        if ($chunk === false) {
            echo "Error: Error al leer el archivo";
            error_log("Error: Error al leer archivo - " . $archivo);
            logActivity('descarga_error', ['error' => 'error_al_leer', 'archivo' => $archivo]);
            fclose($handle);
            exit;
        }
        
        echo $chunk;
        $bytes_sent += strlen($chunk);
        
        // Flush para asegurar que los datos se envíen inmediatamente
        if (ob_get_level()) {
            ob_flush();
        }
        flush();
    }
    
    fclose($handle);
    
    // Verificar que se enviaron todos los bytes
    if ($bytes_sent !== $tamano_archivo) {
        error_log("Advertencia: Bytes enviados ($bytes_sent) no coinciden con tamaño del archivo ($tamano_archivo)");
    }
    
    // Log de descarga exitosa
    error_log("Descarga exitosa: " . $nombre_archivo . " - Bytes enviados: " . $bytes_sent);
    logActivity('descarga_exitosa', [
        'archivo' => $archivo,
        'bytes_enviados' => $bytes_sent,
        'tamano_archivo' => $tamano_archivo
    ]);
    exit;
} else {
    echo "El archivo no existe: " . htmlspecialchars($archivo);
    error_log("Error: Archivo no existe - " . $archivo);
    logActivity('descarga_error', ['error' => 'archivo_no_existe', 'archivo' => $archivo]);
}
?> 