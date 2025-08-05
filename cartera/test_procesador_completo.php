<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Configuración
$python_path = 'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe';
$python_script = 'PROVCA/procesador_balance_completo.py';

// Crear directorio de prueba
$testDir = 'test_files_' . uniqid();
mkdir($testDir, 0777, true);

try {
    // Crear archivos Excel de prueba usando Python
    $create_test_files_script = "
import pandas as pd
import numpy as np
import os

# Crear directorio de prueba
test_dir = '$testDir'
os.makedirs(test_dir, exist_ok=True)

# Archivo BALANCE
balance_data = {
    'Cuenta objeto': ['43001', '43008', '43042', '0080.43002.20', '0080.43002.21', '0080.43002.15', '0080.43002.28', '0080.43002.31', '0080.43002.63'],
    'Saldo AAF variación': [1000000, 2000000, 3000000, 500000, 600000, 400000, 700000, 800000, 900000]
}
df_balance = pd.DataFrame(balance_data)
df_balance.to_excel(f'{test_dir}/balance.xlsx', index=False)

# Archivo SITUACIÓN
situacion_data = {
    'TOTAL 01010': ['01010'],
    'SALDOS MES': [5000000]
}
df_situacion = pd.DataFrame(situacion_data)
df_situacion.to_excel(f'{test_dir}/situacion.xlsx', index=False)

# Archivo FOCUS
focus_data = {
    'Concepto': ['Deuda bruta NO Grupo', 'Deuda bruta NO Grupo', 'Dotaciones Acumuladas', 'Dotaciones Acumuladas', 'Provisión acumulada', 'Vencido 30 días', 'Vencido 60 días'],
    'Periodo': ['Inicial', 'Final', 'Inicial', 'Final', 'Final', 'Mes', 'Mes'],
    'Valor': [10000000, 12000000, 2000000, 2500000, 1800000, 300000, 500000]
}
df_focus = pd.DataFrame(focus_data)
df_focus.to_excel(f'{test_dir}/focus.xlsx', index=False)

print('Archivos de prueba creados exitosamente')
";

    // Guardar y ejecutar script de creación de archivos
    file_put_contents($testDir . '/create_test_files.py', $create_test_files_script);
    
    $create_command = "\"$python_path\" \"$testDir/create_test_files.py\" 2>&1";
    $create_output = [];
    $create_return = 0;
    
    exec($create_command, $create_output, $create_return);
    
    if ($create_return !== 0) {
        throw new Exception("Error creando archivos de prueba: " . implode("\n", $create_output));
    }
    
    // Ejecutar procesador completo
    $balance_file = $testDir . '/balance.xlsx';
    $situacion_file = $testDir . '/situacion.xlsx';
    $focus_file = $testDir . '/focus.xlsx';
    
    $command = "\"$python_path\" \"$python_script\" \"$balance_file\" \"$situacion_file\" \"$focus_file\" 2>&1";
    
    $output = [];
    $return_code = 0;
    
    exec($command, $output, $return_code);
    
    // Leer resultados
    $results = null;
    if (file_exists('resultados_balance_completo.json')) {
        $resultsJson = file_get_contents('resultados_balance_completo.json');
        $results = json_decode($resultsJson, true);
        unlink('resultados_balance_completo.json');
    }
    
    // Limpiar archivos de prueba
    array_map('unlink', glob("$testDir/*"));
    rmdir($testDir);
    
    echo json_encode([
        'success' => true,
        'message' => 'Test del procesador completo ejecutado exitosamente',
        'command' => $command,
        'return_code' => $return_code,
        'output' => $output,
        'results_file_exists' => file_exists('resultados_balance_completo.json'),
        'results' => $results,
        'timestamp' => date('Y-m-d H:i:s')
    ], JSON_PRETTY_PRINT);
    
} catch (Exception $e) {
    // Limpiar en caso de error
    if (isset($testDir) && file_exists($testDir)) {
        array_map('unlink', glob("$testDir/*"));
        rmdir($testDir);
    }
    
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s')
    ], JSON_PRETTY_PRINT);
}
?> 