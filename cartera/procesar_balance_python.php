<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

require_once 'config.php';

try {
    // Verificar que se hayan enviado los archivos
    if (!isset($_FILES['balanceFile']) || !isset($_FILES['situacionFile']) || !isset($_FILES['focusFile'])) {
        throw new Exception('Todos los archivos son requeridos');
    }

    $balanceFile = $_FILES['balanceFile'];
    $situacionFile = $_FILES['situacionFile'];
    $focusFile = $_FILES['focusFile'];

    // Verificar que los archivos se subieron correctamente
    if ($balanceFile['error'] !== UPLOAD_ERR_OK || 
        $situacionFile['error'] !== UPLOAD_ERR_OK || 
        $focusFile['error'] !== UPLOAD_ERR_OK) {
        throw new Exception('Error al subir los archivos');
    }

    // Crear directorio temporal para los archivos
    $tempDir = 'temp_' . uniqid();
    if (!mkdir($tempDir, 0777, true)) {
        throw new Exception('No se pudo crear el directorio temporal');
    }

    // Mover archivos al directorio temporal
    $balancePath = $tempDir . '/balance.xlsx';
    $situacionPath = $tempDir . '/situacion.xlsx';
    $focusPath = $tempDir . '/focus.xlsx';

    if (!move_uploaded_file($balanceFile['tmp_name'], $balancePath) ||
        !move_uploaded_file($situacionFile['tmp_name'], $situacionPath) ||
        !move_uploaded_file($focusFile['tmp_name'], $focusPath)) {
        throw new Exception('Error al mover los archivos');
    }

    // Ejecutar el procesador Python
    $pythonScript = 'PROVCA/procesador_balance.py';
    $command = "C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe \"$pythonScript\" \"$balancePath\" \"$situacionPath\" \"$focusPath\" 2>&1";
    
    $output = [];
    $returnCode = 0;
    
    exec($command, $output, $returnCode);

    // Limpiar archivos temporales
    unlink($balancePath);
    unlink($situacionPath);
    unlink($focusPath);
    rmdir($tempDir);

    if ($returnCode !== 0) {
        $errorMessage = implode("\n", $output);
        throw new Exception("Error ejecutando Python: $errorMessage");
    }

    // Leer resultados del archivo JSON generado por Python
    $resultsFile = 'resultados_balance.json';
    if (!file_exists($resultsFile)) {
        throw new Exception('No se generó el archivo de resultados');
    }

    $resultsJson = file_get_contents($resultsFile);
    $results = json_decode($resultsJson, true);

    if ($results === null) {
        throw new Exception('Error al parsear los resultados JSON');
    }

    // Eliminar archivo de resultados temporal
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