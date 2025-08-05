<?php
// Configurar headers para evitar problemas de caché
header('Cache-Control: no-cache, must-revalidate');
header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');

$archivo = isset($_GET['file']) ? $_GET['file'] : '';

// Log para debugging
error_log("Descarga solicitada para archivo: " . $archivo);

if ($archivo && file_exists($archivo)) {
    // Verificar que el archivo es un Excel válido
    $extension = strtolower(pathinfo($archivo, PATHINFO_EXTENSION));
    if ($extension !== 'xlsx') {
        echo "Error: El archivo no es un archivo Excel válido (.xlsx)";
        error_log("Error: Archivo no es Excel - " . $archivo);
        exit;
    }
    
    // Verificar que el archivo está en la carpeta correcta
    $ruta_permitida = __DIR__ . "/PROVCA_PROCESADOS/";
    if (strpos($archivo, $ruta_permitida) !== 0) {
        echo "Error: Acceso no permitido al archivo";
        error_log("Error: Acceso no permitido - " . $archivo);
        exit;
    }
    
    // Verificar que el archivo no esté vacío
    $tamano_archivo = filesize($archivo);
    if ($tamano_archivo === 0) {
        echo "Error: El archivo está vacío";
        error_log("Error: Archivo vacío - " . $archivo);
        exit;
    }
    
    // Verificar que el archivo sea legible
    if (!is_readable($archivo)) {
        echo "Error: No se puede leer el archivo";
        error_log("Error: Archivo no legible - " . $archivo);
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
    
    // Configurar headers para descarga segura
    header('Content-Description: File Transfer');
    header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
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
    exit;
} else {
    echo "El archivo no existe: " . htmlspecialchars($archivo);
    error_log("Error: Archivo no existe - " . $archivo);
}
?> 