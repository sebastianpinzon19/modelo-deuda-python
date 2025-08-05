<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Crear archivos de prueba simples
$testDir = 'test_files_' . uniqid();
mkdir($testDir, 0777, true);

// Crear archivo de prueba simple
$testData = [
    ['Cuenta', 'Saldo AAF variación'],
    ['43001', 1000],
    ['43008', 2000],
    ['43042', 3000]
];

$testFile = $testDir . '/test_balance.xlsx';
// Por ahora usaremos CSV para simplificar
$csvContent = "Cuenta,Saldo AAF variación\n43001,1000\n43008,2000\n43042,3000\n";
file_put_contents($testDir . '/test_balance.csv', $csvContent);
file_put_contents($testDir . '/test_situacion.csv', "TOTAL 01010,SALDOS MES\n01010,5000\n");
file_put_contents($testDir . '/test_focus.csv', "Concepto,Inicial,Final\nDeuda bruta NO Grupo,10000,12000\n");

// Probar el comando Python
$pythonScript = 'PROVCA/procesador_balance.py';
$command = "C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe \"$pythonScript\" \"$testDir/test_balance.csv\" \"$testDir/test_situacion.csv\" \"$testDir/test_focus.csv\" 2>&1";

$output = [];
$returnCode = 0;

exec($command, $output, $returnCode);

// Limpiar archivos de prueba
array_map('unlink', glob("$testDir/*"));
rmdir($testDir);

echo json_encode([
    'success' => true,
    'message' => 'Test con archivos de ejemplo',
    'command' => $command,
    'return_code' => $returnCode,
    'output' => $output,
    'results_file_exists' => file_exists('resultados_balance.json'),
    'results_content' => file_exists('resultados_balance.json') ? file_get_contents('resultados_balance.json') : 'No existe',
    'timestamp' => date('Y-m-d H:i:s')
]);

// Limpiar archivo de resultados si existe
if (file_exists('resultados_balance.json')) {
    unlink('resultados_balance.json');
}
?> 