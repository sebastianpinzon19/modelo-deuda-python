<?php
// Configuración de Python
$python_paths = [
    'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe',
    'python.exe',
    'py.exe',
    'python3.exe',
    'py -3'
];

// Función para encontrar Python disponible
function find_python_path() {
    global $python_paths;
    
    foreach ($python_paths as $path) {
        $output = [];
        $returnCode = 0;
        
        if (strpos($path, ' ') !== false) {
            // Comando con espacios, usar exec
            exec("$path --version 2>&1", $output, $returnCode);
        } else {
            // Comando simple, usar shell_exec
            $result = shell_exec("$path --version 2>&1");
            $returnCode = $result !== null ? 0 : 1;
        }
        
        if ($returnCode === 0) {
            return $path;
        }
    }
    
    return null;
}

// Obtener la ruta de Python
$python_path = find_python_path();

if ($python_path === null) {
    error_log("No se encontró Python instalado en el sistema");
}
?> 