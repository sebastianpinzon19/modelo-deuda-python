<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once 'python_config.php';

echo json_encode([
    'success' => true,
    'message' => 'Test de Configuración de Python',
    'python_path' => $python_path,
    'python_version' => $python_path ? trim(shell_exec("\"$python_path\" --version 2>&1")) : 'No encontrado',
    'pandas_test' => $python_path ? trim(shell_exec("\"$python_path\" -c \"import pandas; print('OK')\" 2>&1")) : 'No encontrado',
    'script_test' => $python_path ? trim(shell_exec("\"$python_path\" PROVCA/debug_balance_python.py --help 2>&1")) : 'No encontrado',
    'timestamp' => date('Y-m-d H:i:s')
]);
?> 