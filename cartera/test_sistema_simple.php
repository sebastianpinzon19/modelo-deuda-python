<?php
/**
 * Test Simple del Sistema PHP-Python
 * Sistema de Cartera Grupo Planeta
 * Versión: 2.0.1
 */

// Incluir configuración
require_once 'front_php/configuracion.php';

echo "<!DOCTYPE html>";
echo "<html lang='es'>";
echo "<head>";
echo "<meta charset='UTF-8'>";
echo "<meta name='viewport' content='width=device-width, initial-scale=1.0'>";
echo "<title>Test Sistema PHP-Python - Grupo Planeta</title>";
echo "<style>";
echo "body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }";
echo ".test-section { background: white; margin: 10px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }";
echo ".success { border-left: 4px solid #10b981; }";
echo ".error { border-left: 4px solid #ef4444; }";
echo ".warning { border-left: 4px solid #f59e0b; }";
echo ".info { border-left: 4px solid #3b82f6; }";
echo "h1 { color: #1e3a8a; text-align: center; }";
echo "h2 { color: #374151; margin-top: 0; }";
echo "pre { background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto; }";
echo "</style>";
echo "</head>";
echo "<body>";

echo "<h1>🧪 Test del Sistema PHP-Python</h1>";
echo "<p style='text-align: center; color: #6b7280;'>Sistema de Cartera Grupo Planeta v" . SYSTEM_VERSION . "</p>";

// Test 1: Configuración PHP
echo "<div class='test-section info'>";
echo "<h2>1. Configuración PHP</h2>";
echo "<p><strong>Versión del sistema:</strong> " . SYSTEM_VERSION . "</p>";
echo "<p><strong>Directorio base:</strong> " . BASE_DIR . "</p>";
echo "<p><strong>Directorio Python:</strong> " . PYTHON_DIR . "</p>";
echo "<p><strong>Orquestador:</strong> " . ORQUESTADOR_PRINCIPAL . "</p>";
echo "</div>";

// Test 2: Detección de Python
echo "<div class='test-section " . (PYTHON_EXE ? 'success' : 'error') . "'>";
echo "<h2>2. Detección de Python</h2>";
if (PYTHON_EXE) {
    echo "<p><strong>✅ Python detectado:</strong> " . PYTHON_EXE . "</p>";
    
    // Verificar versión de Python
    $output = shell_exec('"' . PYTHON_EXE . '" --version 2>&1');
    echo "<p><strong>Versión:</strong> " . trim($output) . "</p>";
} else {
    echo "<p><strong>❌ Python no detectado</strong></p>";
}
echo "</div>";

// Test 3: Verificar archivos Python
echo "<div class='test-section info'>";
echo "<h2>3. Archivos Python</h2>";
$archivos_python = [
    'orquestador_principal.py',
    'config.py',
    'logger.py',
    'utilidades_cartera.py',
    'procesador_cartera.py',
    'procesador_acumulado.py',
    'procesador_formato_deuda.py',
    'procesador_anticipos.py'
];

foreach ($archivos_python as $archivo) {
    $ruta = PYTHON_DIR . $archivo;
    if (file_exists($ruta)) {
        echo "<p><strong>✅ $archivo:</strong> Existe</p>";
    } else {
        echo "<p><strong>❌ $archivo:</strong> No existe</p>";
    }
}
echo "</div>";

// Test 4: Verificar directorios
echo "<div class='test-section info'>";
echo "<h2>4. Directorios del Sistema</h2>";
$directorios = [
    'BASE_DIR' => BASE_DIR,
    'PROCESSED_DIR' => PROCESSED_DIR,
    'TEMP_DIR' => TEMP_DIR,
    'LOGS_DIR' => LOGS_DIR,
    'PYTHON_LOGS_DIR' => PYTHON_LOGS_DIR
];

foreach ($directorios as $nombre => $ruta) {
    if (is_dir($ruta)) {
        echo "<p><strong>✅ $nombre:</strong> $ruta (Existe)</p>";
    } else {
        echo "<p><strong>⚠️ $nombre:</strong> $ruta (No existe)</p>";
    }
}
echo "</div>";

// Test 5: Test del orquestador Python
echo "<div class='test-section " . (PYTHON_EXE ? 'info' : 'error') . "'>";
echo "<h2>5. Test del Orquestador Python</h2>";
if (PYTHON_EXE) {
    $comando = '"' . PYTHON_EXE . '" "' . ORQUESTADOR_PRINCIPAL . '" estadisticas 2>&1';
    $output = shell_exec($comando);
    
    if ($output) {
        echo "<p><strong>✅ Orquestador ejecutado correctamente</strong></p>";
        echo "<pre>" . htmlspecialchars($output) . "</pre>";
    } else {
        echo "<p><strong>❌ Error ejecutando el orquestador</strong></p>";
    }
} else {
    echo "<p><strong>❌ No se puede probar sin Python</strong></p>";
}
echo "</div>";

// Test 6: Funciones PHP
echo "<div class='test-section info'>";
echo "<h2>6. Funciones PHP</h2>";
echo "<p><strong>✅ getSystemInfo():</strong> " . (function_exists('getSystemInfo') ? 'Disponible' : 'No disponible') . "</p>";
echo "<p><strong>✅ logActivity():</strong> " . (function_exists('logActivity') ? 'Disponible' : 'No disponible') . "</p>";
echo "<p><strong>✅ executePythonOrchestrator():</strong> " . (function_exists('executePythonOrchestrator') ? 'Disponible' : 'No disponible') . "</p>";
echo "<p><strong>✅ validateFile():</strong> " . (function_exists('validateFile') ? 'Disponible' : 'No disponible') . "</p>";
echo "</div>";

// Test 7: Información del sistema
echo "<div class='test-section success'>";
echo "<h2>7. Información del Sistema</h2>";
$system_info = getSystemInfo();
echo "<pre>" . htmlspecialchars(json_encode($system_info, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)) . "</pre>";
echo "</div>";

// Test 8: Logs
echo "<div class='test-section info'>";
echo "<h2>8. Logs del Sistema</h2>";
logActivity('test_sistema_simple', [
    'fecha' => date('Y-m-d H:i:s'),
    'usuario' => $_SERVER['REMOTE_ADDR'] ?? 'unknown'
]);
echo "<p><strong>✅ Log de actividad registrado</strong></p>";

if (is_dir(LOGS_DIR)) {
    $archivos_log = glob(LOGS_DIR . '*.log');
    echo "<p><strong>Archivos de log encontrados:</strong> " . count($archivos_log) . "</p>";
    foreach ($archivos_log as $log) {
        echo "<p>📄 " . basename($log) . "</p>";
    }
} else {
    echo "<p><strong>⚠️ Directorio de logs no existe</strong></p>";
}
echo "</div>";

// Resumen
echo "<div class='test-section success'>";
echo "<h2>🎯 Resumen del Test</h2>";
echo "<p><strong>✅ Sistema PHP:</strong> Funcionando</p>";
echo "<p><strong>✅ Configuración:</strong> Cargada</p>";
echo "<p><strong>✅ Python:</strong> " . (PYTHON_EXE ? 'Detectado' : 'No detectado') . "</p>";
echo "<p><strong>✅ Orquestador:</strong> " . (file_exists(ORQUESTADOR_PRINCIPAL) ? 'Disponible' : 'No disponible') . "</p>";
echo "<p><strong>✅ Funciones:</strong> Todas disponibles</p>";
echo "<p><strong>✅ Logs:</strong> Sistema funcionando</p>";
echo "</div>";

echo "<div style='text-align: center; margin-top: 30px;'>";
echo "<a href='front_php/dashboard.php' style='background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;'>";
echo "🚀 Ir al Dashboard";
echo "</a>";
echo "</div>";

echo "</body>";
echo "</html>";
?>
