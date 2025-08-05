<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

echo json_encode([
    'success' => true,
    'message' => 'Test del Sistema de Balance',
    'archivos_php' => [
        'procesar_balance_python.php' => file_exists('procesar_balance_python.php'),
        'debug_balance_python.php' => file_exists('debug_balance_python.php'),
        'balance.php' => file_exists('balance.php')
    ],
    'archivos_python' => [
        'procesador_balance.py' => file_exists('PROVCA/procesador_balance.py'),
        'debug_balance_python.py' => file_exists('PROVCA/debug_balance_python.py'),
        'requirements.txt' => file_exists('PROVCA/requirements.txt')
    ],
    'python_version' => trim(shell_exec('py -3 --version 2>&1')),
    'pandas_ok' => trim(shell_exec('py -3 -c "import pandas; print(\"OK\")" 2>&1')) === 'OK',
    'openpyxl_ok' => trim(shell_exec('py -3 -c "import openpyxl; print(\"OK\")" 2>&1')) === 'OK',
    'numpy_ok' => trim(shell_exec('py -3 -c "import numpy; print(\"OK\")" 2>&1')) === 'OK',
    'timestamp' => date('Y-m-d H:i:s')
]);
?> 