<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Habilitar reporte de errores
error_reporting(E_ALL);
ini_set('display_errors', 1);

try {
    // Verificar archivos
    if (!isset($_FILES['balanceFile']) || !isset($_FILES['situacionFile']) || !isset($_FILES['focusFile'])) {
        throw new Exception('Todos los archivos son requeridos');
    }

    $balanceFile = $_FILES['balanceFile'];
    $situacionFile = $_FILES['situacionFile'];
    $focusFile = $_FILES['focusFile'];

    // Verificar errores de upload
    if ($balanceFile['error'] !== UPLOAD_ERR_OK || 
        $situacionFile['error'] !== UPLOAD_ERR_OK || 
        $focusFile['error'] !== UPLOAD_ERR_OK) {
        throw new Exception('Error al subir archivos');
    }

    // Crear directorio temporal
    $tempDir = 'temp_' . uniqid();
    if (!mkdir($tempDir, 0777, true)) {
        throw new Exception('No se pudo crear directorio temporal');
    }

    // Mover archivos
    $balancePath = $tempDir . '/balance.xlsx';
    $situacionPath = $tempDir . '/situacion.xlsx';
    $focusPath = $tempDir . '/focus.xlsx';

    if (!move_uploaded_file($balanceFile['tmp_name'], $balancePath) ||
        !move_uploaded_file($situacionFile['tmp_name'], $situacionPath) ||
        !move_uploaded_file($focusFile['tmp_name'], $focusPath)) {
        throw new Exception('Error al mover archivos');
    }

    // Verificar que los archivos existen
    if (!file_exists($balancePath) || !file_exists($situacionPath) || !file_exists($focusPath)) {
        throw new Exception('Archivos temporales no encontrados');
    }

    // Ejecutar Python
    $pythonScript = 'PROVCA/procesador_balance.py';
    $command = "C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe \"$pythonScript\" \"$balancePath\" \"$situacionPath\" \"$focusPath\" 2>&1";
    
    $output = [];
    $returnCode = 0;
    
    exec($command, $output, $returnCode);

    // Limpiar archivos temporales
    if (file_exists($balancePath)) unlink($balancePath);
    if (file_exists($situacionPath)) unlink($situacionPath);
    if (file_exists($focusPath)) unlink($focusPath);
    if (is_dir($tempDir)) rmdir($tempDir);

    if ($returnCode !== 0) {
        $errorMessage = implode("\n", $output);
        throw new Exception("Error Python (código $returnCode): $errorMessage");
    }

    // Leer resultados
    $resultsFile = 'resultados_balance.json';
    if (!file_exists($resultsFile)) {
        throw new Exception('Archivo de resultados no encontrado');
    }

    $resultsJson = file_get_contents($resultsFile);
    if ($resultsJson === false) {
        throw new Exception('No se pudo leer archivo de resultados');
    }

    $results = json_decode($resultsJson, true);
    if ($results === null) {
        throw new Exception('Error al parsear JSON: ' . json_last_error_msg());
    }

    // Limpiar archivo de resultados
    unlink($resultsFile);

    echo json_encode([
        'success' => true,
        'results' => $results,
        'python_output' => $output
    ]);

} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ]);
}
?> 