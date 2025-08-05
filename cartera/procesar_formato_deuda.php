<?php
session_start();
header('Content-Type: application/json');

// Incluir configuración centralizada
require_once 'config.php';

try {
    // Limpiar archivos antiguos
    limpiarArchivosAntiguos(DIR_TEMP);
    limpiarArchivosAntiguos(DIR_RESULTADOS);
    
    // Verificar si se recibió un archivo
    if (!isset($_FILES['archivo'])) {
        throw new Exception('No se recibió ningún archivo');
    }

    $archivo = $_FILES['archivo'];
    
    // Validar archivo usando la función mejorada
    $errores = validarArchivo($archivo);
    if (!empty($errores)) {
        throw new Exception(implode('; ', $errores));
    }

    $nombreOriginal = $archivo['name'];
    $tamanoArchivo = $archivo['size'];
    $archivoTemporal = $archivo['tmp_name'];
    $extension = strtolower(pathinfo($nombreOriginal, PATHINFO_EXTENSION));

    // Generar nombre único para el archivo
    $nombreUnico = generarNombreUnico('formato_deuda', $extension);
    $rutaDestino = DIR_TEMP . $nombreUnico;

    // Mover archivo subido al directorio temporal
    if (!move_uploaded_file($archivoTemporal, $rutaDestino)) {
        escribirErrorLog("Error al mover archivo: $archivoTemporal a $rutaDestino");
        throw new Exception('Error al guardar el archivo en el servidor');
    }

    escribirLog("Archivo formato deuda subido: $nombreOriginal -> $rutaDestino");

    // Ejecutar script de Python para procesar formato deuda
    try {
        $output = ejecutarScriptPython(SCRIPT_FORMATO_DEUDA, $rutaDestino);
        escribirLog("Procesamiento de formato deuda completado para: $nombreOriginal");
    } catch (Exception $e) {
        // Limpiar archivo temporal en caso de error
        if (file_exists($rutaDestino)) {
            unlink($rutaDestino);
        }
        throw $e;
    }

    // Buscar archivo de resultado generado
    $timestamp = date('Y-m-d_H-i-s');
    $archivosResultado = glob(DIR_RESULTADOS . '*formato_deuda*' . $timestamp . '*');
    $archivoResultado = null;
    
    if (!empty($archivosResultado)) {
        $archivoResultado = $archivosResultado[0];
        escribirLog("Archivo de resultado encontrado: " . basename($archivoResultado));
    } else {
        escribirLog("No se encontró archivo de resultado para: $nombreOriginal");
    }

    // Preparar respuesta de éxito
    $respuesta = [
        'success' => true,
        'message' => 'Archivo de formato deuda procesado exitosamente',
        'data' => [
            'archivo_original' => $nombreOriginal,
            'archivo_procesado' => $archivoResultado ? basename($archivoResultado) : null,
            'tamano_archivo' => formatBytes($tamanoArchivo),
            'timestamp' => $timestamp,
            'tipo_procesamiento' => 'Formato Deuda',
            'ruta_resultado' => $archivoResultado ? $archivoResultado : null
        ]
    ];

    // Limpiar archivo temporal después de procesar
    if (file_exists($rutaDestino)) {
        if (unlink($rutaDestino)) {
            escribirLog("Archivo temporal eliminado: $rutaDestino");
        } else {
            escribirErrorLog("No se pudo eliminar archivo temporal: $rutaDestino");
        }
    }

    echo json_encode($respuesta);

} catch (Exception $e) {
    escribirErrorLog("Error en procesamiento de formato deuda: " . $e->getMessage(), $e);
    
    $respuesta = [
        'success' => false,
        'message' => $e->getMessage(),
        'error' => true,
        'error_type' => 'processing_error'
    ];
    
    echo json_encode($respuesta);
}
?>
            $comando .= " \"\"";
        }
        
        if (isset($archivos_subidos['focus'])) {
            $comando .= " \"{$archivos_subidos['focus']}\"";
        } else {
            $comando .= " \"\"";
        }
        
        // Agregar fecha de cierre si se especificó
        if ($fecha_cierre) {
            $comando .= " \"$fecha_cierre\"";
        }

        $comando .= " 2>&1";

        $output = [];
        $return_code = 0;

        exec($comando, $output, $return_code);

        if ($return_code !== 0) {
            throw new Exception("Error en el procesamiento Python: " . implode("\n", $output));
        }

        // Buscar archivo de resultados generado
        $archivos_resultado = glob('resultados/FORMATO_DEUDA_*.xlsx');
        if (empty($archivos_resultado)) {
            throw new Exception("No se encontró el archivo de resultados generado");
        }

        $archivo_resultado = end($archivos_resultado); // Tomar el más reciente
        
        // Buscar archivo de resumen JSON
        $archivo_resumen = str_replace('.xlsx', '_resumen.json', $archivo_resultado);
        if (file_exists($archivo_resumen)) {
            $json_resultados = file_get_contents($archivo_resumen);
            $resultados = json_decode($json_resultados, true);
        } else {
            // Crear resumen básico si no existe el JSON
            $resultados = [
                'archivo_generado' => $archivo_resultado,
                'registros_procesados' => count($archivos_procesados),
                'fecha_procesamiento' => date('Y-m-d H:i:s'),
                'archivos_entrada' => $archivos_procesados
            ];
        }

        $mensaje = "Procesamiento de formato deuda completado exitosamente";

        // Limpiar archivos temporales
        foreach ($archivos_subidos as $archivo) {
            if (file_exists($archivo)) {
                unlink($archivo);
            }
        }

    } catch (Exception $e) {
        $mensaje = "Error: " . $e->getMessage();

        // Limpiar archivos en caso de error
        if (isset($archivos_subidos)) {
            foreach ($archivos_subidos as $archivo) {
                if (file_exists($archivo)) {
                    unlink($archivo);
                }
            }
        }
    }
}

// Función para formatear números
function formatear_numero($numero, $decimales = 2) {
    return number_format($numero, $decimales, ',', '.');
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procesador de Formato Deuda - Grupo Planeta</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <img src="Logo grupo planeta color transparente.jpg" alt="Grupo Planeta">
            </div>
            <h1>Procesador de Formato Deuda</h1>
            <p>Sistema de procesamiento completo de formato deuda según especificaciones del área de cartera</p>
        </div>

        <div class="content">
            <?php if ($mensaje): ?>
                <div class="alert <?php echo strpos($mensaje, 'Error') !== false ? 'error' : 'success'; ?>">
                    <i class="fas <?php echo strpos($mensaje, 'Error') !== false ? 'fa-exclamation-triangle' : 'fa-check-circle'; ?>"></i>
                    <?php echo htmlspecialchars($mensaje); ?>
                </div>
            <?php endif; ?>

            <form method="POST" enctype="multipart/form-data" class="upload-form">
                <div class="form-section">
                    <h3><i class="fas fa-file-csv"></i> Archivos Requeridos</h3>
                    
                    <div class="form-group">
                        <label for="provision">
                            <i class="fas fa-file-csv"></i>
                            Archivo de PROVISIÓN (PROVCA.csv)
                        </label>
                        <input type="file" id="provision" name="provision" accept=".csv,.xlsx,.xls" required>
                        <small>Archivo CSV de provisión generado por el sistema Pisa (GESLOC → CARTERA → PROVCAE)</small>
                    </div>

                    <div class="form-group">
                        <label for="anticipos">
                            <i class="fas fa-file-csv"></i>
                            Archivo de ANTICIPOS (ANTICI.csv)
                        </label>
                        <input type="file" id="anticipos" name="anticipos" accept=".csv,.xlsx,.xls" required>
                        <small>Archivo CSV de anticipos generado por el sistema Pisa (GESLOC → CARTERA → CLANTI)</small>
                    </div>
                </div>

                <div class="form-section">
                    <h3><i class="fas fa-file-excel"></i> Archivos Opcionales</h3>
                    
                    <div class="form-group">
                        <label for="balance">
                            <i class="fas fa-file-excel"></i>
                            Archivo BALANCE (JDE)
                        </label>
                        <input type="file" id="balance" name="balance" accept=".xlsx,.xls">
                        <small>Archivo Excel de balance contable con cuentas específicas (43002.20, 43002.21, etc.)</small>
                    </div>

                    <div class="form-group">
                        <label for="situacion">
                            <i class="fas fa-file-excel"></i>
                            Archivo SITUACIÓN (Tesorería)
                        </label>
                        <input type="file" id="situacion" name="situacion" accept=".xlsx,.xls">
                        <small>Archivo Excel de situación con datos de cobros y saldos mensuales</small>
                    </div>

                    <div class="form-group">
                        <label for="focus">
                            <i class="fas fa-file-excel"></i>
                            Archivo FOCUS (Citrix)
                        </label>
                        <input type="file" id="focus" name="focus" accept=".xlsx,.xls">
                        <small>Archivo Excel de focus con datos de vencimientos y dotaciones</small>
                    </div>
                </div>

                <div class="form-section">
                    <h3><i class="fas fa-calendar"></i> Configuración</h3>
                    
                    <div class="form-group">
                        <label for="fecha_cierre">
                            <i class="fas fa-calendar-alt"></i>
                            Fecha de Cierre (Opcional)
                        </label>
                        <input type="date" id="fecha_cierre" name="fecha_cierre">
                        <small>Fecha de cierre del mes para cálculos. Si no se especifica, se usa el último día del mes anterior.</small>
                    </div>
                </div>

                <button type="submit" class="btn-primary">
                    <i class="fas fa-cogs"></i>
                    Procesar Formato Deuda Completo
                </button>
            </form>

            <?php if ($resultados): ?>
                <div class="results">
                    <h2><i class="fas fa-chart-line"></i> Resultados del Procesamiento</h2>

                    <div class="result-section">
                        <h3>Resumen de Procesamiento</h3>
                        <div class="result-grid">
                            <div class="result-item">
                                <span class="label">Archivo Generado:</span>
                                <span class="value"><?php echo basename($resultados['archivo_generado']); ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Registros Provisión:</span>
                                <span class="value"><?php echo isset($resultados['registros_provision']) ? number_format($resultados['registros_provision']) : 'N/A'; ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Registros Anticipos:</span>
                                <span class="value"><?php echo isset($resultados['registros_anticipos']) ? number_format($resultados['registros_anticipos']) : 'N/A'; ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Registros Pesos:</span>
                                <span class="value"><?php echo isset($resultados['registros_pesos']) ? number_format($resultados['registros_pesos']) : 'N/A'; ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Registros Divisas:</span>
                                <span class="value"><?php echo isset($resultados['registros_divisas']) ? number_format($resultados['registros_divisas']) : 'N/A'; ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Registros Vencimientos:</span>
                                <span class="value"><?php echo isset($resultados['registros_vencimientos']) ? number_format($resultados['registros_vencimientos']) : 'N/A'; ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Fecha de Cierre:</span>
                                <span class="value"><?php echo isset($resultados['fecha_cierre']) ? $resultados['fecha_cierre'] : 'N/A'; ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Fecha de Procesamiento:</span>
                                <span class="value"><?php echo isset($resultados['fecha_procesamiento']) ? date('d/m/Y H:i:s', strtotime($resultados['fecha_procesamiento'])) : 'N/A'; ?></span>
                            </div>
                        </div>
                    </div>

                    <div class="result-section">
                        <h3>Archivos Procesados</h3>
                        <ul class="file-list">
                            <?php foreach ($archivos_procesados as $archivo): ?>
                                <li><i class="fas fa-file"></i> <?php echo htmlspecialchars($archivo); ?></li>
                            <?php endforeach; ?>
                        </ul>
                    </div>

                    <div class="download-section">
                        <a href="<?php echo $resultados['archivo_generado']; ?>" class="btn-download" download>
                            <i class="fas fa-download"></i>
                            Descargar Formato Deuda Excel
                        </a>
                    </div>
                </div>
            <?php endif; ?>
        </div>

        <div class="footer">
            <p>&copy; 2025 Grupo Planeta. Todos los derechos reservados.</p>
        </div>
    </div>

    <script>
        // Mostrar loading durante el procesamiento
        document.querySelector('form').addEventListener('submit', function() {
            const btn = this.querySelector('button[type="submit"]');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando Formato Deuda...';
            btn.disabled = true;
        });
    </script>
</body>
</html> 