<?php
/**
 * Test del Sistema de Procesamiento de Cartera
 * Verifica el correcto funcionamiento de todos los componentes
 */

require_once 'config.php';

// Función para mostrar resultados de pruebas
function mostrarPrueba($nombre, $exito, $mensaje = '', $detalles = '') {
    $icono = $exito ? '✅' : '❌';
    $color = $exito ? 'green' : 'red';
    echo "<div style='margin: 10px 0; padding: 10px; border-left: 4px solid $color; background: #f8f9fa;'>";
    echo "<strong>$icono $nombre</strong><br>";
    if ($mensaje) echo "<span style='color: #666;'>$mensaje</span><br>";
    if ($detalles) echo "<small style='color: #888;'>$detalles</small>";
    echo "</div>";
}

// Función para verificar archivo
function verificarArchivo($ruta, $descripcion) {
    $existe = file_exists($ruta);
    $permisos = $existe ? substr(sprintf('%o', fileperms($ruta)), -4) : 'N/A';
    $tamanio = $existe ? formatBytes(filesize($ruta)) : 'N/A';
    return [
        'existe' => $existe,
        'permisos' => $permisos,
        'tamanio' => $tamanio,
        'descripcion' => $descripcion
    ];
}

// Función para verificar directorio
function verificarDirectorio($ruta, $descripcion) {
    $existe = is_dir($ruta);
    $escribible = $existe ? is_writable($ruta) : false;
    $archivos = $existe ? count(glob($ruta . '/*')) : 0;
    return [
        'existe' => $existe,
        'escribible' => $escribible,
        'archivos' => $archivos,
        'descripcion' => $descripcion
    ];
}

// Función para verificar comando
function verificarComando($comando, $descripcion) {
    exec("$comando --version 2>&1", $output, $returnCode);
    $disponible = $returnCode === 0;
    $version = $disponible ? implode(' ', $output) : 'No disponible';
    return [
        'disponible' => $disponible,
        'version' => $version,
        'descripcion' => $descripcion
    ];
}

?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test del Sistema - Grupo Planeta</title>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            margin: 20px;
            background: #f8f9fa;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
        }
        .header h1 {
            color: #1e3a8a;
            margin-bottom: 10px;
        }
        .header p {
            color: #6c757d;
            font-size: 1.1em;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            background: #f8f9fa;
        }
        .section h2 {
            color: #495057;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #dee2e6;
        }
        .summary {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .summary h3 {
            color: #1976d2;
            margin-bottom: 10px;
        }
        .status-ok { color: #28a745; }
        .status-error { color: #dc3545; }
        .status-warning { color: #ffc107; }
        .details {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            margin-top: 5px;
            font-family: monospace;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Test del Sistema de Procesamiento</h1>
            <p>Verificación completa de todos los componentes del sistema</p>
        </div>

        <?php
        $totalPruebas = 0;
        $pruebasExitosas = 0;
        
        // 1. Verificar configuración
        echo "<div class='section'>";
        echo "<h2>📋 Configuración del Sistema</h2>";
        
        $totalPruebas++;
        $configExiste = file_exists('config.php');
        if ($configExiste) {
            $pruebasExitosas++;
            mostrarPrueba('Archivo de configuración', true, 'config.php encontrado');
        } else {
            mostrarPrueba('Archivo de configuración', false, 'config.php no encontrado');
        }
        
        $totalPruebas++;
        if (defined('SISTEMA_NOMBRE')) {
            $pruebasExitosas++;
            mostrarPrueba('Constantes del sistema', true, 'Constantes definidas correctamente');
        } else {
            mostrarPrueba('Constantes del sistema', false, 'Constantes no definidas');
        }
        
        echo "</div>";
        
        // 2. Verificar directorios
        echo "<div class='section'>";
        echo "<h2>📁 Directorios del Sistema</h2>";
        
        $directorios = [
            DIR_TEMP => 'Directorio temporal',
            DIR_RESULTADOS => 'Directorio de resultados',
            DIR_LOGS => 'Directorio de logs',
            DIR_PYTHON => 'Directorio de scripts Python'
        ];
        
        foreach ($directorios as $ruta => $descripcion) {
            $totalPruebas++;
            $info = verificarDirectorio($ruta, $descripcion);
            if ($info['existe'] && $info['escribible']) {
                $pruebasExitosas++;
                mostrarPrueba($descripcion, true, "Existe y es escribible", "Archivos: {$info['archivos']}");
            } else {
                mostrarPrueba($descripcion, false, "No existe o no es escribible", "Ruta: $ruta");
            }
        }
        
        echo "</div>";
        
        // 3. Verificar scripts de Python
        echo "<div class='section'>";
        echo "<h2>🐍 Scripts de Python</h2>";
        
        $scripts = [
            SCRIPT_FORMATO_DEUDA => 'Procesador Formato Deuda',
            SCRIPT_BALANCE => 'Procesador Balance',
            SCRIPT_CARTERA => 'Procesador Cartera',
            SCRIPT_ANTICIPOS => 'Procesador Anticipos'
        ];
        
        foreach ($scripts as $ruta => $descripcion) {
            $totalPruebas++;
            $info = verificarArchivo($ruta, $descripcion);
            if ($info['existe']) {
                $pruebasExitosas++;
                mostrarPrueba($descripcion, true, "Archivo encontrado", "Tamaño: {$info['tamanio']}, Permisos: {$info['permisos']}");
            } else {
                mostrarPrueba($descripcion, false, "Archivo no encontrado", "Ruta: $ruta");
            }
        }
        
        echo "</div>";
        
        // 4. Verificar comandos de Python
        echo "<div class='section'>";
        echo "<h2>🐍 Comandos de Python</h2>";
        
        $comandos = [
            PYTHON_PATH => 'Python (python)',
            PYTHON_PATH_ALT => 'Python3 (python3)'
        ];
        
        $pythonDisponible = false;
        foreach ($comandos as $comando => $descripcion) {
            $totalPruebas++;
            $info = verificarComando($comando, $descripcion);
            if ($info['disponible']) {
                $pruebasExitosas++;
                $pythonDisponible = true;
                mostrarPrueba($descripcion, true, "Comando disponible", "Versión: {$info['version']}");
            } else {
                mostrarPrueba($descripcion, false, "Comando no disponible", "Comando: $comando");
            }
        }
        
        echo "</div>";
        
        // 5. Verificar archivos PHP
        echo "<div class='section'>";
        echo "<h2>🔧 Archivos PHP</h2>";
        
        $archivosPHP = [
            'index.php' => 'Página principal',
            'procesar_balance.php' => 'Procesador de balance',
            'procesar_cartera.php' => 'Procesador de cartera',
            'procesar_anticipos.php' => 'Procesador de anticipos',
            'procesar_formato_deuda.php' => 'Procesador de formato deuda'
        ];
        
        foreach ($archivosPHP as $archivo => $descripcion) {
            $totalPruebas++;
            $info = verificarArchivo($archivo, $descripcion);
            if ($info['existe']) {
                $pruebasExitosas++;
                mostrarPrueba($descripcion, true, "Archivo encontrado", "Tamaño: {$info['tamanio']}");
            } else {
                mostrarPrueba($descripcion, false, "Archivo no encontrado", "Archivo: $archivo");
            }
        }
        
        echo "</div>";
        
        // 6. Verificar archivos CSS
        echo "<div class='section'>";
        echo "<h2>🎨 Archivos CSS</h2>";
        
        $archivosCSS = [
            'front_php/styles.css' => 'Estilos principales'
        ];
        
        foreach ($archivosCSS as $archivo => $descripcion) {
            $totalPruebas++;
            $info = verificarArchivo($archivo, $descripcion);
            if ($info['existe']) {
                $pruebasExitosas++;
                mostrarPrueba($descripcion, true, "Archivo encontrado", "Tamaño: {$info['tamanio']}");
            } else {
                mostrarPrueba($descripcion, false, "Archivo no encontrado", "Archivo: $archivo");
            }
        }
        
        echo "</div>";
        
        // 7. Verificar funciones del sistema
        echo "<div class='section'>";
        echo "<h2>⚙️ Funciones del Sistema</h2>";
        
        $funciones = [
            'validarArchivo' => 'Validación de archivos',
            'ejecutarScriptPython' => 'Ejecución de scripts Python',
            'limpiarArchivosAntiguos' => 'Limpieza automática',
            'obtenerEstadisticasSistema' => 'Estadísticas del sistema',
            'verificarSaludSistema' => 'Verificación de salud'
        ];
        
        foreach ($funciones as $funcion => $descripcion) {
            $totalPruebas++;
            if (function_exists($funcion)) {
                $pruebasExitosas++;
                mostrarPrueba($descripcion, true, "Función disponible");
            } else {
                mostrarPrueba($descripcion, false, "Función no disponible", "Función: $funcion");
            }
        }
        
        echo "</div>";
        
        // 8. Verificar estadísticas del sistema
        echo "<div class='section'>";
        echo "<h2>📊 Estadísticas del Sistema</h2>";
        
        $totalPruebas++;
        try {
            $estadisticas = obtenerEstadisticasSistema();
            $pruebasExitosas++;
            mostrarPrueba('Estadísticas disponibles', true, 'Total archivos: ' . $estadisticas['total_archivos']);
            
            echo "<div class='details'>";
            echo "Archivos temporales: {$estadisticas['archivos_temp']}<br>";
            echo "Archivos de resultados: {$estadisticas['archivos_resultados']}<br>";
            echo "Archivos recientes: {$estadisticas['archivos_recientes']}<br>";
            echo "Espacio temp: {$estadisticas['espacio_temp']}<br>";
            echo "Espacio resultados: {$estadisticas['espacio_resultados']}";
            echo "</div>";
        } catch (Exception $e) {
            mostrarPrueba('Estadísticas disponibles', false, 'Error al obtener estadísticas', $e->getMessage());
        }
        
        echo "</div>";
        
        // 9. Verificar salud del sistema
        echo "<div class='section'>";
        echo "<h2>🏥 Salud del Sistema</h2>";
        
        $totalPruebas++;
        try {
            $problemas = verificarSaludSistema();
            if (empty($problemas)) {
                $pruebasExitosas++;
                mostrarPrueba('Salud del sistema', true, 'Sistema funcionando correctamente');
            } else {
                mostrarPrueba('Salud del sistema', false, count($problemas) . ' problemas detectados');
                echo "<div class='details'>";
                foreach ($problemas as $problema) {
                    echo "• $problema<br>";
                }
                echo "</div>";
            }
        } catch (Exception $e) {
            mostrarPrueba('Salud del sistema', false, 'Error al verificar salud', $e->getMessage());
        }
        
        echo "</div>";
        
        // 10. Verificar permisos y configuración del servidor
        echo "<div class='section'>";
        echo "<h2>🔐 Configuración del Servidor</h2>";
        
        $totalPruebas++;
        $uploadMaxFilesize = ini_get('upload_max_filesize');
        $postMaxSize = ini_get('post_max_size');
        $maxExecutionTime = ini_get('max_execution_time');
        
        $pruebasExitosas++;
        mostrarPrueba('Configuración de PHP', true, "Upload max: $uploadMaxFilesize, Post max: $postMaxSize, Max execution: {$maxExecutionTime}s");
        
        $totalPruebas++;
        if (function_exists('exec')) {
            $pruebasExitosas++;
            mostrarPrueba('Función exec', true, 'Función exec disponible');
        } else {
            mostrarPrueba('Función exec', false, 'Función exec no disponible');
        }
        
        echo "</div>";
        
        // Resumen final
        $porcentajeExito = $totalPruebas > 0 ? round(($pruebasExitosas / $totalPruebas) * 100, 1) : 0;
        $colorEstado = $porcentajeExito >= 90 ? 'status-ok' : ($porcentajeExito >= 70 ? 'status-warning' : 'status-error');
        
        echo "<div class='summary'>";
        echo "<h3>📈 Resumen del Test</h3>";
        echo "<p><strong>Pruebas totales:</strong> $totalPruebas</p>";
        echo "<p><strong>Pruebas exitosas:</strong> $pruebasExitosas</p>";
        echo "<p><strong>Porcentaje de éxito:</strong> <span class='$colorEstado'>$porcentajeExito%</span></p>";
        
        if ($porcentajeExito >= 90) {
            echo "<p><strong>Estado:</strong> <span class='status-ok'>✅ Sistema funcionando correctamente</span></p>";
        } elseif ($porcentajeExito >= 70) {
            echo "<p><strong>Estado:</strong> <span class='status-warning'>⚠️ Sistema con advertencias</span></p>";
        } else {
            echo "<p><strong>Estado:</strong> <span class='status-error'>❌ Sistema con problemas críticos</span></p>";
        }
        
        if (!$pythonDisponible) {
            echo "<p><strong>⚠️ Advertencia:</strong> Python no está disponible. El procesamiento de archivos no funcionará.</p>";
        }
        
        echo "</div>";
        ?>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="index.php" style="background: #1e3a8a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                🏠 Volver al Sistema
            </a>
        </div>
    </div>
</body>
</html> 