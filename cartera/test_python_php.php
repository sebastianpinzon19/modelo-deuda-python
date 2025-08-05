<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

echo json_encode([
    'success' => true,
    'message' => 'Test de Python desde PHP',
    'python_version_1' => trim(shell_exec('py -3 --version 2>&1')),
    'python_version_2' => trim(shell_exec('python --version 2>&1')),
    'python_version_3' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version 2>&1')),
    'pandas_test_1' => trim(shell_exec('py -3 -c "import pandas; print(\"OK\")" 2>&1')),
    'pandas_test_2' => trim(shell_exec('python -c "import pandas; print(\"OK\")" 2>&1')),
    'pandas_test_3' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -c "import pandas; print(\"OK\")" 2>&1')),
    'script_test' => trim(shell_exec('"C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" PROVCA/debug_balance_python.py --help 2>&1')),
    'timestamp' => date('Y-m-d H:i:s')
]);
?> 