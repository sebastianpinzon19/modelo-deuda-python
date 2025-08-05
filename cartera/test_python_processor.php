<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

echo json_encode([
    'success' => true,
    'message' => 'Test del Procesador de Python',
    'python_script_exists' => file_exists('PROVCA/procesador_balance.py'),
    'python_version' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version 2>&1')),
    'pandas_test' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -c "import pandas; print(\"OK\")" 2>&1')),
    'openpyxl_test' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -c "import openpyxl; print(\"OK\")" 2>&1')),
    'numpy_test' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -c "import numpy; print(\"OK\")" 2>&1')),
    'script_help' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" PROVCA/procesador_balance.py --help 2>&1')),
    'current_dir' => getcwd(),
    'timestamp' => date('Y-m-d H:i:s')
]);
?> 