<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Habilitar reporte de errores para debug
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once 'config.php';

try {
    // Log de inicio
    error_log("Iniciando procesamiento de balance");
    
    // Verificar que se hayan enviado los archivos
    if (!isset($_FILES['balanceFile']) || !isset($_FILES['situacionFile']) || !isset($_FILES['focusFile'])) {
        throw new Exception('Todos los archivos son requeridos');
    }

    $balanceFile = $_FILES['balanceFile'];
    $situacionFile = $_FILES['situacionFile'];
    $focusFile = $_FILES['focusFile'];

    // Log de archivos recibidos
    error_log("Archivos recibidos: " . json_encode([
        'balance' => $balanceFile['name'],
        'situacion' => $situacionFile['name'],
        'focus' => $focusFile['name']
    ]));

    // Verificar que los archivos se subieron correctamente
    if ($balanceFile['error'] !== UPLOAD_ERR_OK || 
        $situacionFile['error'] !== UPLOAD_ERR_OK || 
        $focusFile['error'] !== UPLOAD_ERR_OK) {
        throw new Exception('Error al subir los archivos: ' . json_encode([
            'balance_error' => $balanceFile['error'],
            'situacion_error' => $situacionFile['error'],
            'focus_error' => $focusFile['error']
        ]));
    }

    // Crear directorio temporal para los archivos
    $tempDir = 'temp_' . uniqid();
    if (!mkdir($tempDir, 0777, true)) {
        throw new Exception('No se pudo crear el directorio temporal: ' . $tempDir);
    }

    error_log("Directorio temporal creado: " . $tempDir);

    // Mover archivos al directorio temporal
    $balancePath = $tempDir . '/balance.xlsx';
    $situacionPath = $tempDir . '/situacion.xlsx';
    $focusPath = $tempDir . '/focus.xlsx';

    if (!move_uploaded_file($balanceFile['tmp_name'], $balancePath)) {
        throw new Exception('Error al mover archivo balance');
    }
    if (!move_uploaded_file($situacionFile['tmp_name'], $situacionPath)) {
        throw new Exception('Error al mover archivo situacion');
    }
    if (!move_uploaded_file($focusFile['tmp_name'], $focusPath)) {
        throw new Exception('Error al mover archivo focus');
    }

    error_log("Archivos movidos correctamente");

    // Verificar que el script de Python existe
    $pythonScript = 'PROVCA/procesador_balance.py';
    if (!file_exists($pythonScript)) {
        throw new Exception('Script de Python no encontrado: ' . $pythonScript);
    }

    // Ejecutar el procesador Python
    $command = "C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe \"$pythonScript\" \"$balancePath\" \"$situacionPath\" \"$focusPath\" 2>&1";
    
    error_log("Ejecutando comando: " . $command);
    
    $output = [];
    $returnCode = 0;
    
    exec($command, $output, $returnCode);

    error_log("Comando ejecutado. Código de retorno: " . $returnCode);
    error_log("Salida del comando: " . json_encode($output));

    // Limpiar archivos temporales
    if (file_exists($balancePath)) unlink($balancePath);
    if (file_exists($situacionPath)) unlink($situacionPath);
    if (file_exists($focusPath)) unlink($focusPath);
    if (is_dir($tempDir)) rmdir($tempDir);

    if ($returnCode !== 0) {
        $errorMessage = implode("\n", $output);
        throw new Exception("Error ejecutando Python (código $returnCode): $errorMessage");
    }

    // Leer resultados del archivo JSON generado por Python
    $resultsFile = 'resultados_balance.json';
    if (!file_exists($resultsFile)) {
        throw new Exception('No se generó el archivo de resultados: ' . $resultsFile);
    }

    error_log("Archivo de resultados encontrado: " . $resultsFile);

    $resultsJson = file_get_contents($resultsFile);
    if ($resultsJson === false) {
        throw new Exception('No se pudo leer el archivo de resultados');
    }

    error_log("Contenido del archivo JSON: " . substr($resultsJson, 0, 200) . "...");

    $results = json_decode($resultsJson, true);

    if ($results === null) {
        $jsonError = json_last_error_msg();
        throw new Exception('Error al parsear los resultados JSON: ' . $jsonError . '. Contenido: ' . substr($resultsJson, 0, 500));
    }

    // Eliminar archivo de resultados temporal
    unlink($resultsFile);

    error_log("Procesamiento completado exitosamente");

    echo json_encode([
        'success' => true,
        'results' => $results,
        'python_output' => $output,
        'debug_info' => [
            'temp_dir' => $tempDir,
            'python_script' => $pythonScript,
            'command' => $command,
            'return_code' => $returnCode
        ]
    ]);

} catch (Exception $e) {
    error_log("Error en procesamiento: " . $e->getMessage());
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage(),
        'debug_info' => [
            'error_type' => get_class($e),
            'file' => $e->getFile(),
            'line' => $e->getLine()
        ]
    ]);
}
?> 