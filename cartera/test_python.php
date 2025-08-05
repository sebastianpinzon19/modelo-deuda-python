<?php
require_once 'config.php';

echo "<h1>Test de Configuración Python</h1>";

// Verificar que Python esté disponible
echo "<h2>1. Verificación de Python</h2>";
$python_path = PYTHON_PATH;
echo "Ruta Python configurada: $python_path<br>";

// Probar ejecución de Python
echo "<h2>2. Prueba de Ejecución</h2>";
$output = [];
$returnCode = 0;
$comando = "$python_path --version 2>&1";
echo "Comando a ejecutar: $comando<br>";

exec($comando, $output, $returnCode);

if ($returnCode === 0) {
    echo "<p style='color: green;'>✅ Python funciona correctamente</p>";
    echo "Salida: " . implode("<br>", $output) . "<br>";
} else {
    echo "<p style='color: red;'>❌ Error al ejecutar Python</p>";
    echo "Código de retorno: $returnCode<br>";
    echo "Salida: " . implode("<br>", $output) . "<br>";
}

// Probar script de Python
echo "<h2>3. Prueba de Script Python</h2>";
$script_path = 'PROVCA/procesador_anticipos.py';
if (file_exists($script_path)) {
    echo "✅ Script encontrado: $script_path<br>";
    
    // Crear un archivo de prueba
    $test_file = 'temp/test_anticipos.csv';
    if (!is_dir('temp')) {
        mkdir('temp', 0755, true);
    }
    
    // Crear contenido de prueba
    $test_content = "EMPRESA,ACTIVIDAD,CODIGO_CLIENTE,NIT_CEDULA,NOMBRE_COMERCIAL,DIRECCION,TELEFONO,POBLACION,CODIGO_AGENTE,NOMBRE_AGENTE,APELLIDO_AGENTE,TIPO_ANTICIPO,NRO_ANTICIPO,VALOR_ANTICIPO,FECHA_ANTICIPO\n";
    $test_content .= "PL10,001,12345,12345678,Cliente Test,Dirección Test,1234567,Bogotá,001,Agente,Test,ANT,001,1000000,20250101\n";
    
    file_put_contents($test_file, $test_content);
    echo "✅ Archivo de prueba creado: $test_file<br>";
    
    // Probar ejecución del script
    $comando_script = "$python_path \"$script_path\" \"$test_file\" 2>&1";
    echo "Comando del script: $comando_script<br>";
    
    $output_script = [];
    $returnCode_script = 0;
    exec($comando_script, $output_script, $returnCode_script);
    
    if ($returnCode_script === 0) {
        echo "<p style='color: green;'>✅ Script Python ejecutado correctamente</p>";
    } else {
        echo "<p style='color: orange;'>⚠️ Script ejecutado con advertencias</p>";
    }
    
    echo "Salida del script:<br>";
    echo "<pre>" . implode("\n", $output_script) . "</pre>";
    
    // Limpiar archivo de prueba
    if (file_exists($test_file)) {
        unlink($test_file);
        echo "✅ Archivo de prueba eliminado<br>";
    }
    
} else {
    echo "❌ Script no encontrado: $script_path<br>";
}

echo "<h2>4. Verificación de Directorios</h2>";
$directorios = ['temp', 'resultados', 'logs'];
foreach ($directorios as $dir) {
    if (is_dir($dir)) {
        echo "✅ Directorio existe: $dir<br>";
    } else {
        echo "❌ Directorio no existe: $dir<br>";
    }
}

echo "<h2>5. Verificación de Permisos</h2>";
foreach ($directorios as $dir) {
    if (is_writable($dir)) {
        echo "✅ Directorio escribible: $dir<br>";
    } else {
        echo "❌ Directorio no escribible: $dir<br>";
    }
}

echo "<h2>6. Resumen</h2>";
if ($returnCode === 0) {
    echo "<p style='color: green; font-weight: bold;'>🎉 Python está configurado correctamente y listo para usar</p>";
} else {
    echo "<p style='color: red; font-weight: bold;'>❌ Hay problemas con la configuración de Python</p>";
}
?> 