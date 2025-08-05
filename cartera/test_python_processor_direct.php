<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Crear archivos de prueba simples
$testDir = 'test_files_' . uniqid();
mkdir($testDir, 0777, true);

// Crear archivos CSV de prueba
$balanceCsv = "Cuenta,Saldo AAF variación\n43001,1000\n43008,2000\n43042,3000\n0080.43002.20,500\n0080.43002.21,600\n";
$situacionCsv = "TOTAL 01010,SALDOS MES\n01010,5000\n";
$focusCsv = "Concepto,Inicial,Final\nDeuda bruta NO Grupo,10000,12000\nDotaciones Acumuladas,2000,2500\nProvisión acumulada,1500,1800\n";

file_put_contents($testDir . '/balance.csv', $balanceCsv);
file_put_contents($testDir . '/situacion.csv', $situacionCsv);
file_put_contents($testDir . '/focus.csv', $focusCsv);

// Probar el comando Python
$pythonScript = 'PROVCA/procesador_balance.py';
$command = "C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe \"$pythonScript\" \"$testDir/balance.csv\" \"$testDir/situacion.csv\" \"$testDir/focus.csv\" 2>&1";

$output = [];
$returnCode = 0;

exec($command, $output, $returnCode);

// Limpiar archivos de prueba
array_map('unlink', glob("$testDir/*"));
rmdir($testDir);

$results = [];
if (file_exists('resultados_balance.json')) {
    $resultsJson = file_get_contents('resultados_balance.json');
    $results = json_decode($resultsJson, true);
    unlink('resultados_balance.json');
}

echo json_encode([
    'success' => true,
    'message' => 'Test directo del procesador Python',
    'command' => $command,
    'return_code' => $returnCode,
    'output' => $output,
    'results_file_exists' => file_exists('resultados_balance.json'),
    'results' => $results,
    'timestamp' => date('Y-m-d H:i:s')
]);
?> 