<?php
/**
 * Script de limpieza automática de archivos
 * 
 * Este script elimina archivos antiguos (más de 7 días) de los directorios
 * temp/ y resultados/ para mantener el sistema limpio.
 * 
 * Se puede ejecutar manualmente o configurar como cron job:
 * 0 2 * * * /usr/bin/php /ruta/al/proyecto/limpiar_archivos.php
 */

// Configuración
$diasRetencion = 7;
$directorios = ['temp', 'resultados'];
$logFile = 'logs/limpieza.log';

// Crear directorio de logs si no existe
if (!is_dir('logs')) {
    mkdir('logs', 0755, true);
}

// Función para escribir logs
function escribirLog($mensaje) {
    global $logFile;
    $timestamp = date('Y-m-d H:i:s');
    $logEntry = "[$timestamp] $mensaje\n";
    file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
}

// Función para limpiar archivos antiguos
function limpiarArchivosAntiguos($directorio, $dias = 7) {
    if (!is_dir($directorio)) {
        escribirLog("Directorio $directorio no existe");
        return 0;
    }
    
    $archivos = glob($directorio . '/*');
    $tiempoLimite = time() - ($dias * 24 * 60 * 60);
    $archivosEliminados = 0;
    $espacioLiberado = 0;
    
    foreach ($archivos as $archivo) {
        if (is_file($archivo) && filemtime($archivo) < $tiempoLimite) {
            $tamanoArchivo = filesize($archivo);
            if (unlink($archivo)) {
                $archivosEliminados++;
                $espacioLiberado += $tamanoArchivo;
                escribirLog("Eliminado: $archivo (" . formatBytes($tamanoArchivo) . ")");
            } else {
                escribirLog("Error al eliminar: $archivo");
            }
        }
    }
    
    return ['archivos' => $archivosEliminados, 'espacio' => $espacioLiberado];
}

// Función para formatear bytes
function formatBytes($bytes, $precision = 2) {
    $units = array('B', 'KB', 'MB', 'GB', 'TB');
    
    for ($i = 0; $bytes > 1024 && $i < count($units) - 1; $i++) {
        $bytes /= 1024;
    }
    
    return round($bytes, $precision) . ' ' . $units[$i];
}

// Iniciar proceso de limpieza
escribirLog("=== Iniciando proceso de limpieza automática ===");

$totalArchivosEliminados = 0;
$totalEspacioLiberado = 0;

foreach ($directorios as $directorio) {
    escribirLog("Procesando directorio: $directorio");
    
    $resultado = limpiarArchivosAntiguos($directorio, $diasRetencion);
    $totalArchivosEliminados += $resultado['archivos'];
    $totalEspacioLiberado += $resultado['espacio'];
    
    escribirLog("Directorio $directorio: {$resultado['archivos']} archivos eliminados, " . formatBytes($resultado['espacio']) . " liberados");
}

escribirLog("=== Resumen de limpieza ===");
escribirLog("Total archivos eliminados: $totalArchivosEliminados");
escribirLog("Total espacio liberado: " . formatBytes($totalEspacioLiberado));
escribirLog("=== Proceso de limpieza completado ===\n");

// Si se ejecuta desde línea de comandos, mostrar resumen
if (php_sapi_name() === 'cli') {
    echo "=== LIMPIEZA AUTOMÁTICA COMPLETADA ===\n";
    echo "Archivos eliminados: $totalArchivosEliminados\n";
    echo "Espacio liberado: " . formatBytes($totalEspacioLiberado) . "\n";
    echo "Log guardado en: $logFile\n";
}

// Si se ejecuta desde web, devolver JSON
if (isset($_SERVER['HTTP_HOST'])) {
    header('Content-Type: application/json');
    echo json_encode([
        'success' => true,
        'message' => 'Limpieza automática completada',
        'data' => [
            'archivos_eliminados' => $totalArchivosEliminados,
            'espacio_liberado' => formatBytes($totalEspacioLiberado),
            'fecha_ejecucion' => date('Y-m-d H:i:s')
        ]
    ]);
}
?> 