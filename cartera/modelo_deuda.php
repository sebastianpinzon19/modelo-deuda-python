<?php
// Habilitar reporte de errores
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Console log inicial
echo '<script>console.log("=== INICIANDO PROCESO MODELO DEUDA ===");</script>';

try {
    // Verificar que se recibieron los archivos
    if (!isset($_FILES['cartera_file']) || !isset($_FILES['anticipos_file']) || !isset($_POST['trm_dolar']) || !isset($_POST['trm_euro'])) {
        echo '<script>console.error("ERROR: Faltan datos para procesar el modelo de deuda");</script>';
        echo '<script>console.log("Datos POST recibidos: ' . json_encode($_POST) . '");</script>';
        echo '<script>console.log("Archivos recibidos: ' . json_encode($_FILES) . '");</script>';
        echo "Faltan datos para procesar el modelo de deuda.";
        exit;
    }
    
    echo '<script>console.log("✅ Datos recibidos correctamente");</script>';

    $cartera_file = $_FILES['cartera_file'];
    $anticipos_file = $_FILES['anticipos_file'];
    $trm_dolar = $_POST['trm_dolar'];
    $trm_euro = $_POST['trm_euro'];

    echo '<script>console.log("📁 Archivos recibidos:");</script>';
    echo '<script>console.log("- Cartera: ' . $cartera_file['name'] . ' (' . $cartera_file['size'] . ' bytes)");</script>';
    echo '<script>console.log("- Anticipos: ' . $anticipos_file['name'] . ' (' . $anticipos_file['size'] . ' bytes)");</script>';
    echo '<script>console.log("💰 TRM Dólar: ' . $trm_dolar . '");</script>';
    echo '<script>console.log("💰 TRM Euro: ' . $trm_euro . '");</script>';

    // Verificar que los archivos se subieron correctamente
    if ($cartera_file['error'] !== UPLOAD_ERR_OK || $anticipos_file['error'] !== UPLOAD_ERR_OK) {
        echo '<script>console.error("ERROR: Error al subir los archivos");</script>';
        echo '<script>console.error("- Error cartera: ' . $cartera_file['error'] . '");</script>';
        echo '<script>console.error("- Error anticipos: ' . $anticipos_file['error'] . '");</script>';
        echo "Error al subir los archivos.";
        exit;
    }

    echo '<script>console.log("✅ Archivos subidos correctamente");</script>';

    // Crear carpeta temporal para los archivos subidos
    $temp_dir = __DIR__ . "/temp/";
    if (!is_dir($temp_dir)) {
        mkdir($temp_dir, 0777, true);
        echo '<script>console.log("📁 Carpeta temporal creada: ' . $temp_dir . '");</script>';
    } else {
        echo '<script>console.log("📁 Carpeta temporal ya existe: ' . $temp_dir . '");</script>';
    }

    // Mover archivos subidos a carpeta temporal
    $cartera_temp = $temp_dir . basename($cartera_file['name']);
    $anticipos_temp = $temp_dir . basename($anticipos_file['name']);

    echo '<script>console.log("📂 Moviendo archivos a carpeta temporal:");</script>';
    echo '<script>console.log("- Cartera temporal: ' . $cartera_temp . '");</script>';
    echo '<script>console.log("- Anticipos temporal: ' . $anticipos_temp . '");</script>';

    if (!move_uploaded_file($cartera_file['tmp_name'], $cartera_temp) || 
        !move_uploaded_file($anticipos_file['tmp_name'], $anticipos_temp)) {
        echo '<script>console.error("ERROR: Error al guardar los archivos temporalmente");</script>';
        echo "Error al guardar los archivos temporalmente.";
        exit;
    }

    echo '<script>console.log("✅ Archivos movidos a carpeta temporal correctamente");</script>';

    // Sanitiza TRMs
    $trm_dolar = str_replace(',', '.', $trm_dolar);
    $trm_euro = str_replace(',', '.', $trm_euro);

    echo '<script>console.log("💰 TRMs sanitizados:");</script>';
    echo '<script>console.log("- TRM Dólar: ' . $trm_dolar . '");</script>';
    echo '<script>console.log("- TRM Euro: ' . $trm_euro . '");</script>';

    // Guardar timestamp antes de procesar
    $timestamp_inicio = time();
    echo '<script>console.log("⏰ Timestamp inicio: ' . $timestamp_inicio . ' (' . date('Y-m-d H:i:s', $timestamp_inicio) . ')");</script>';

    // Usar la ruta completa de Python
    $python = "C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe";
    
    echo '<script>console.log("🐍 Usando Python desde ruta completa");</script>';
    
    // Verificar que Python funciona
    if (!file_exists($python)) {
        echo '<script>console.error("ERROR: Python no encontrado en la ruta especificada");</script>';
        echo '<div style="background: #f8d7da; padding: 15px; border: 1px solid #f5c6cb; border-radius: 5px; margin: 10px 0;">';
        echo '<h3>❌ Error: Python no encontrado</h3>';
        echo '<p>Python no se encontró en la ruta: ' . $python . '</p>';
        echo '<p>Por favor, verifica que Python esté instalado correctamente.</p>';
        echo '</div>';
        exit;
    }
    
    $test_cmd = "\"$python\" --version 2>&1";
    $output = shell_exec($test_cmd);
    
    if (!$output || strpos($output, 'no se reconoce') !== false || strpos($output, 'not recognized') !== false) {
        echo '<script>console.error("ERROR: Python no se puede ejecutar");</script>';
        echo '<div style="background: #f8d7da; padding: 15px; border: 1px solid #f5c6cb; border-radius: 5px; margin: 10px 0;">';
        echo '<h3>❌ Error: Python no se puede ejecutar</h3>';
        echo '<p>Python se encontró pero no se puede ejecutar.</p>';
        echo '<p><strong>Comando probado:</strong> ' . $test_cmd . '</p>';
        echo '<p><strong>Salida:</strong> ' . htmlspecialchars($output) . '</p>';
        echo '</div>';
        exit;
    }
    
    echo '<script>console.log("✅ Python encontrado: ' . htmlspecialchars($output) . '");</script>';

    $script = __DIR__ . "/PROVCA/modelo_deuda.py";

    echo '<script>console.log("🐍 Configuración Python:");</script>';
    echo '<script>console.log("- Python: ' . $python . '");</script>';
    echo '<script>console.log("- Script: ' . $script . '");</script>';

    if (!file_exists($script)) {
        echo '<script>console.error("ERROR: Script Python no encontrado en ' . $script . '");</script>';
        echo "Error: Script Python no encontrado.";
        exit;
    }

    echo '<script>console.log("✅ Python y script verificados correctamente");</script>';

    // Ejecuta directamente el script Python del modelo de deuda con los archivos originales
    $cmd = "\"$python\" \"$script\" \"$cartera_temp\" \"$anticipos_temp\" \"$trm_dolar\" \"$trm_euro\" 2>&1";

    echo '<script>console.log("🚀 Ejecutando modelo de deuda...");</script>';
    echo '<script>console.log("Comando: ' . $cmd . '");</script>';

    $output = shell_exec($cmd);

    echo '<script>console.log("📤 Salida modelo de deuda:");</script>';
    echo '<script>console.log("' . addslashes($output) . '");</script>';

    // Filtra solo las líneas importantes del output
    $lines = explode("\n", $output);
    $important_lines = [];
    foreach ($lines as $line) {
        if (strpos($line, '=== INICIANDO PROCESO MODELO DEUDA ===') !== false || 
            strpos($line, 'ADVERTENCIA:') !== false || 
            strpos($line, 'Columnas disponibles') !== false ||
            strpos($line, 'Archivo generado:') !== false ||
            strpos($line, '=== PROCESO COMPLETADO EXITOSAMENTE ===') !== false ||
            strpos($line, 'Traceback') !== false ||
            strpos($line, 'Error') !== false ||
            strpos($line, 'TypeError') !== false ||
            strpos($line, 'Convirtiendo tipos') !== false ||
            strpos($line, 'Aplicando TRM') !== false ||
            strpos($line, 'Agregados') !== false ||
            strpos($line, 'Registros en hoja') !== false ||
            strpos($line, 'Procesando hoja') !== false ||
            strpos($line, 'DataFrames validados') !== false) {
            $important_lines[] = $line;
        }
    }

    echo '<script>console.log("📋 Líneas importantes encontradas: ' . count($important_lines) . '");</script>';

    // Muestra solo las líneas importantes
    if (!empty($important_lines)) {
        echo "<pre>" . implode("\n", $important_lines) . "</pre>";
        echo '<script>console.log("📄 Líneas importantes mostradas en pantalla");</script>';
    } else {
        echo '<script>console.warn("⚠️ No se encontraron líneas importantes para mostrar");</script>';
    }

    // Buscar el archivo generado DESPUÉS del timestamp de inicio
    $archivo_generado = null;
    $output_dir = __DIR__ . "/PROVCA_PROCESADOS/";

    echo '<script>console.log("🔍 Buscando archivo generado...");</script>';

    if (is_dir($output_dir)) {
        // Buscar archivos con el patrón "1_Modelo_Deuda_*"
        $archivos = glob($output_dir . "1_Modelo_Deuda_*.xlsx");
        echo '<script>console.log("Archivos modelo deuda encontrados: ' . count($archivos) . '");</script>';
        
        if ($archivos) {
            // Buscar archivos creados después del timestamp de inicio
            foreach ($archivos as $archivo) {
                $tiempo_archivo = filemtime($archivo);
                echo '<script>console.log("Archivo: ' . basename($archivo) . ' - Modificado: ' . date('Y-m-d H:i:s', $tiempo_archivo) . '");</script>';
                
                if ($tiempo_archivo >= $timestamp_inicio) {
                    if (!$archivo_generado || $tiempo_archivo > filemtime($archivo_generado)) {
                        $archivo_generado = $archivo;
                        echo '<script>console.log("✅ Archivo modelo seleccionado: ' . basename($archivo) . '");</script>';
                    }
                }
            }
        }
        
        // Si no se encontró con el patrón específico, buscar cualquier archivo Excel
        if (!$archivo_generado) {
            echo '<script>console.log("🔍 Buscando cualquier archivo Excel...");</script>';
            $archivos = glob($output_dir . "*.xlsx");
            echo '<script>console.log("Archivos Excel encontrados: ' . count($archivos) . '");</script>';
            
            if ($archivos) {
                foreach ($archivos as $archivo) {
                    $tiempo_archivo = filemtime($archivo);
                    echo '<script>console.log("Archivo: ' . basename($archivo) . ' - Modificado: ' . date('Y-m-d H:i:s', $tiempo_archivo) . '");</script>';
                    
                    if ($tiempo_archivo >= $timestamp_inicio) {
                        if (!$archivo_generado || $tiempo_archivo > filemtime($archivo_generado)) {
                            $archivo_generado = $archivo;
                            echo '<script>console.log("✅ Archivo Excel seleccionado: ' . basename($archivo) . '");</script>';
                        }
                    }
                }
            }
        }
    } else {
        echo '<script>console.error("ERROR: Directorio de salida no existe: ' . $output_dir . '");</script>';
    }

    // Limpieza silenciosa de archivos temporales
    if (file_exists($cartera_temp)) {
        unlink($cartera_temp);
    }
    if (file_exists($anticipos_temp)) {
        unlink($anticipos_temp);
    }

    // Limpiar otros archivos temporales antiguos silenciosamente
    $temp_dir = __DIR__ . "/temp/";
    if (is_dir($temp_dir)) {
        $archivos_temp = glob($temp_dir . "*");
        foreach ($archivos_temp as $archivo_temp) {
            if (is_file($archivo_temp)) {
                $edad_minutos = (time() - filemtime($archivo_temp)) / 60;
                if ($edad_minutos > 30) {
                    unlink($archivo_temp);
                }
            }
        }
    }

    // Enlace para descargar el archivo generado
    if ($archivo_generado && file_exists($archivo_generado)) {
        echo '<script>console.log("✅ Archivo generado encontrado: ' . basename($archivo_generado) . '");</script>';
        
        // Verificar que el archivo no esté vacío
        $tamaño_archivo = filesize($archivo_generado);
        echo '<script>console.log("📏 Tamaño del archivo: ' . number_format($tamaño_archivo) . ' bytes");</script>';
        
        if ($tamaño_archivo > 0) {
            $nombre_archivo = basename($archivo_generado);
            echo '<div class="alert-success">¡Modelo de Deuda generado correctamente!</div>';
            echo '<p><strong>Archivo:</strong> ' . htmlspecialchars($nombre_archivo) . '</p>';
            echo '<p><strong>Tamaño del archivo:</strong> ' . number_format($tamaño_archivo) . ' bytes</p>';
            echo '<a href="descargar.php?file=' . urlencode($archivo_generado) . '" class="btn-descarga">Descargar Modelo Deuda</a>';
            echo '<script>console.log("🎉 ÉXITO: Modelo de deuda generado correctamente");</script>';
            echo '<script>console.log("📁 Archivo: ' . $archivo_generado . '");</script>';
            echo '<script>console.log("📏 Tamaño: ' . $tamaño_archivo . ' bytes");</script>';
        } else {
            echo '<script>console.error("❌ ERROR: El archivo del modelo de deuda está vacío");</script>';
            echo '<div class="alert-danger">Error: El archivo del modelo de deuda está vacío.</div>';
            echo '<script>console.log("📁 Archivo vacío: ' . $archivo_generado . '");</script>';
        }
    } else {
        echo '<script>console.error("❌ ERROR: No se generó el archivo del modelo de deuda");</script>';
        echo '<div class="alert-danger">No se generó el archivo del modelo de deuda.</div>';
        echo '<p>Verificando archivos en: ' . htmlspecialchars($output_dir) . '</p>';
        echo '<script>console.log("🔍 No se encontró modelo de deuda generado después de ' . date('Y-m-d H:i:s', $timestamp_inicio) . '");</script>';
    }

    echo '<script>console.log("=== FIN PROCESO MODELO DEUDA ===");</script>';

} catch (Exception $e) {
    echo '<script>console.error("❌ ERROR CRÍTICO: ' . addslashes($e->getMessage()) . '");</script>';
    echo '<script>console.error("Archivo: ' . $e->getFile() . '");</script>';
    echo '<script>console.error("Línea: ' . $e->getLine() . '");</script>';
    echo '<script>console.error("Trace: ' . addslashes($e->getTraceAsString()) . '");</script>';
    
    echo '<div class="alert-danger">Error crítico: ' . htmlspecialchars($e->getMessage()) . '</div>';
    echo '<p><strong>Archivo:</strong> ' . htmlspecialchars($e->getFile()) . '</p>';
    echo '<p><strong>Línea:</strong> ' . $e->getLine() . '</p>';
}

?>

