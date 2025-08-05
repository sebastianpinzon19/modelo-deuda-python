<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

echo json_encode([
    'success' => true,
    'message' => 'Test Final del Sistema de Balance',
    'archivos_php' => [
        'procesar_balance_python.php' => file_exists('procesar_balance_python.php'),
        'debug_balance_python.php' => file_exists('debug_balance_python.php'),
        'balance.php' => file_exists('balance.php')
    ],
    'archivos_python' => [
        'procesador_balance.py' => file_exists('PROVCA/procesador_balance.py'),
        'debug_balance_python.py' => file_exists('PROVCA/debug_balance_python.py')
    ],
    'python_path' => 'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe',
    'python_version' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version 2>&1')),
    'pandas_test' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -c "import pandas; print(\"OK\")" 2>&1')),
    'openpyxl_test' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -c "import openpyxl; print(\"OK\")" 2>&1')),
    'numpy_test' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -c "import numpy; print(\"OK\")" 2>&1')),
    'script_test' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" PROVCA/debug_balance_python.py --help 2>&1')),
    'timestamp' => date('Y-m-d H:i:s')
]);
?> 