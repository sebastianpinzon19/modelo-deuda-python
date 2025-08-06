<?php
/**
 * Test de Integración PHP-Python - Sistema de Cartera Grupo Planeta
 * Versión: 2.0.1
 * 
 * Script para verificar que la integración entre PHP y Python funciona correctamente
 */

// Incluir configuración
require_once '../front_php/configuracion.php';

echo "=== TEST DE INTEGRACIÓN PHP-PYTHON ===\n";
echo "Sistema de Cartera Grupo Planeta v" . SYSTEM_VERSION . "\n";
echo "Fecha: " . date('Y-m-d H:i:s') . "\n\n";

$tests_passed = 0;
$tests_total = 0;

/**
 * Función para ejecutar tests
 */
function runTest($name, $test_function) {
    global $tests_passed, $tests_total;
    
    echo "🧪 Test: $name\n";
    echo "   ";
    
    try {
        $result = $test_function();
        if ($result) {
            echo "✅ PASÓ\n";
            $tests_passed++;
        } else {
            echo "❌ FALLÓ\n";
        }
    } catch (Exception $e) {
        echo "❌ ERROR: " . $e->getMessage() . "\n";
    }
    
    $tests_total++;
    echo "\n";
}

/**
 * Test 1: Verificar configuración PHP
 */
runTest("Configuración PHP", function() {
    echo "Verificando constantes de configuración...";
    
    $required_constants = [
        'PYTHON_EXE', 'PYTHON_DIR', 'ORQUESTADOR_PRINCIPAL',
        'BASE_DIR', 'PROCESSED_DIR', 'TEMP_DIR', 'LOGS_DIR',
        'MAX_FILE_SIZE', 'ALLOWED_EXTENSIONS', 'SYSTEM_VERSION'
    ];
    
    foreach ($required_constants as $constant) {
        if (!defined($constant)) {
            throw new Exception("Constante $constant no definida");
        }
    }
    
    echo "Constantes definidas correctamente";
    return true;
});

/**
 * Test 2: Verificar detección de Python
 */
runTest("Detección de Python", function() {
    echo "Verificando detección automática de Python...";
    
    $python_path = PYTHON_EXE;
    echo "Ruta detectada: $python_path";
    
    if (empty($python_path)) {
        throw new Exception("No se detectó Python");
    }
    
    $version_output = shell_exec("$python_path --version 2>&1");
    if (strpos($version_output, 'Python') === false) {
        throw new Exception("Python no funciona correctamente: $version_output");
    }
    
    echo "Versión: " . trim($version_output);
    return true;
});

/**
 * Test 3: Verificar directorios del sistema
 */
runTest("Directorios del Sistema", function() {
    echo "Verificando directorios del sistema...";
    
    $directories = [
        'Base' => BASE_DIR,
        'Python' => PYTHON_DIR,
        'Resultados' => PROCESSED_DIR,
        'Temporal' => TEMP_DIR,
        'Logs' => LOGS_DIR
    ];
    
    foreach ($directories as $name => $path) {
        if (!is_dir($path)) {
            if (!mkdir($path, 0755, true)) {
                throw new Exception("No se pudo crear directorio $name: $path");
            }
            echo "Creado directorio $name: $path\n   ";
        }
        
        if (!is_writable($path)) {
            throw new Exception("Directorio $name no tiene permisos de escritura: $path");
        }
    }
    
    echo "Todos los directorios están disponibles y escribibles";
    return true;
});

/**
 * Test 4: Verificar archivos Python importantes
 */
runTest("Archivos Python Importantes", function() {
    echo "Verificando archivos Python importantes...";
    
    $important_files = [
        'Orquestador Principal' => ORQUESTADOR_PRINCIPAL,
        'Configuración' => PYTHON_DIR . 'config.py',
        'Logger' => PYTHON_DIR . 'logger.py',
        'Utilidades' => PYTHON_DIR . 'utilidades_cartera.py',
        'Requirements' => PYTHON_DIR . 'requirements.txt'
    ];
    
    foreach ($important_files as $name => $path) {
        if (!file_exists($path)) {
            throw new Exception("Archivo $name no existe: $path");
        }
        echo "✓ $name existe\n   ";
    }
    
    echo "Todos los archivos Python importantes están presentes";
    return true;
});

/**
 * Test 5: Verificar dependencias Python
 */
runTest("Dependencias Python", function() {
    echo "Verificando dependencias Python...";
    
    $dependencies = ['pandas', 'numpy', 'openpyxl'];
    
    foreach ($dependencies as $dep) {
        $output = shell_exec(PYTHON_EXE . " -c \"import $dep\" 2>&1");
        if (strpos($output, 'ImportError') !== false || strpos($output, 'ModuleNotFoundError') !== false) {
            throw new Exception("Dependencia $dep no está instalada: $output");
        }
        echo "✓ $dep instalada\n   ";
    }
    
    echo "Todas las dependencias Python están instaladas";
    return true;
});

/**
 * Test 6: Verificar orquestador Python
 */
runTest("Orquestador Python", function() {
    echo "Verificando orquestador principal...";
    
    if (!file_exists(ORQUESTADOR_PRINCIPAL)) {
        throw new Exception("Orquestador principal no existe");
    }
    
    $help_output = shell_exec(PYTHON_EXE . ' ' . escapeshellarg(ORQUESTADOR_PRINCIPAL) . ' --help 2>&1');
    
    if (strpos($help_output, 'usage:') === false && strpos($help_output, 'help') === false) {
        throw new Exception("Orquestador no responde correctamente: $help_output");
    }
    
    echo "Orquestador responde correctamente";
    return true;
});

/**
 * Test 7: Verificar funciones PHP
 */
runTest("Funciones PHP", function() {
    echo "Verificando funciones PHP...";
    
    $required_functions = [
        'detectarPython', 'checkPermissions', 'validateFile',
        'executePythonOrchestrator', 'jsonResponse', 'handleError',
        'getSystemInfo', 'logActivity'
    ];
    
    foreach ($required_functions as $function) {
        if (!function_exists($function)) {
            throw new Exception("Función $function no existe");
        }
    }
    
    echo "Todas las funciones PHP están disponibles";
    return true;
});

/**
 * Test 8: Verificar permisos del sistema
 */
runTest("Permisos del Sistema", function() {
    echo "Verificando permisos del sistema...";
    
    $errors = checkPermissions();
    
    if (!empty($errors)) {
        throw new Exception("Errores de permisos: " . implode(', ', $errors));
    }
    
    echo "Todos los permisos están correctos";
    return true;
});

/**
 * Test 9: Verificar logging
 */
runTest("Sistema de Logging", function() {
    echo "Verificando sistema de logging...";
    
    $test_action = 'test_integracion_' . time();
    logActivity($test_action, ['test' => true]);
    
    $log_file = LOGS_DIR . 'php_activity.log';
    if (!file_exists($log_file)) {
        throw new Exception("Archivo de log no se creó");
    }
    
    $log_content = file_get_contents($log_file);
    if (strpos($log_content, $test_action) === false) {
        throw new Exception("Log no contiene la acción de prueba");
    }
    
    echo "Sistema de logging funciona correctamente";
    return true;
});

/**
 * Test 10: Verificar comunicación PHP-Python
 */
runTest("Comunicación PHP-Python", function() {
    echo "Verificando comunicación PHP-Python...";
    
    // Crear archivo de prueba temporal
    $test_file = TEMP_DIR . 'test_integracion_' . time() . '.txt';
    file_put_contents($test_file, 'Test de integración');
    
    try {
        // Probar comunicación con orquestador
        $result = executePythonOrchestrator('test', [$test_file], ['test_mode' => 'true']);
        
        if ($result === null) {
            throw new Exception("No se recibió respuesta del orquestador");
        }
        
        echo "Comunicación exitosa con orquestador";
        
    } finally {
        // Limpiar archivo de prueba
        if (file_exists($test_file)) {
            unlink($test_file);
        }
    }
    
    return true;
});

/**
 * Test 11: Verificar información del sistema
 */
runTest("Información del Sistema", function() {
    echo "Verificando información del sistema...";
    
    $system_info = getSystemInfo();
    
    $required_keys = ['version', 'python_path', 'python_version', 'orquestador_exists', 'directories'];
    
    foreach ($required_keys as $key) {
        if (!isset($system_info[$key])) {
            throw new Exception("Clave $key no está en la información del sistema");
        }
    }
    
    echo "Información del sistema disponible: " . $system_info['version'];
    return true;
});

/**
 * Test 12: Verificar validación de archivos
 */
runTest("Validación de Archivos", function() {
    echo "Verificando validación de archivos...";
    
    // Crear archivo de prueba
    $test_file = TEMP_DIR . 'test_validation.xlsx';
    file_put_contents($test_file, 'Test content');
    
    // Simular archivo subido
    $uploaded_file = [
        'tmp_name' => $test_file,
        'name' => 'test_validation.xlsx',
        'size' => filesize($test_file),
        'error' => UPLOAD_ERR_OK
    ];
    
    $errors = validateFile($uploaded_file);
    
    if (!empty($errors)) {
        throw new Exception("Validación falló: " . implode(', ', $errors));
    }
    
    // Limpiar
    unlink($test_file);
    
    echo "Validación de archivos funciona correctamente";
    return true;
});

// Ejecutar todos los tests
echo "=== EJECUTANDO TESTS ===\n\n";

// Los tests se ejecutan automáticamente arriba

// Mostrar resumen
echo "=== RESUMEN DE TESTS ===\n";
echo "Tests pasados: $tests_passed/$tests_total\n";
echo "Porcentaje de éxito: " . round(($tests_passed / $tests_total) * 100, 2) . "%\n\n";

if ($tests_passed === $tests_total) {
    echo "🎉 ¡TODOS LOS TESTS PASARON! La integración PHP-Python está funcionando correctamente.\n";
    exit(0);
} else {
    echo "⚠️  ALGUNOS TESTS FALLARON. Revisa los errores arriba y corrige los problemas.\n";
    exit(1);
}
?>
