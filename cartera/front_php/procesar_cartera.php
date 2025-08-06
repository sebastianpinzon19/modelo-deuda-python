<?php
session_start();
header('Content-Type: text/html; charset=utf-8');

// Incluir configuración mejorada
require_once 'configuracion.php';

// Log de actividad
logActivity('procesar_cartera_init');

$mensaje = '';
$resultados = null;
$archivos_procesados = [];
$errores_sistema = [];

// Verificar permisos del sistema
$errores_sistema = checkPermissions();
if (!empty($errores_sistema)) {
    $mensaje = "Errores de configuración del sistema:<br>" . implode("<br>", $errores_sistema);
}

// Procesar formulario
if ($_SERVER['REQUEST_METHOD'] === 'POST' && empty($errores_sistema)) {
    try {
        logActivity('procesar_cartera_start');
        
        $archivos_requeridos = ['balance', 'situacion', 'focus'];
        $archivos_subidos = [];
        
        // Verificar archivos subidos
        foreach ($archivos_requeridos as $tipo) {
            if (!isset($_FILES[$tipo]) || $_FILES[$tipo]['error'] !== UPLOAD_ERR_OK) {
                throw new Exception("Error al subir el archivo de $tipo");
            }
            
            $archivo = $_FILES[$tipo];
            
            // Validaciones usando la nueva función
            $errores_validacion = validateFile($archivo);
            if (!empty($errores_validacion)) {
                throw new Exception("Error en archivo de $tipo: " . implode(", ", $errores_validacion));
            }
            
            // Guardar archivo
            $nombre_archivo = $tipo . '_' . date('Y-m-d_H-i-s') . '.' . pathinfo($archivo['name'], PATHINFO_EXTENSION);
            $ruta_archivo = TEMP_DIR . $nombre_archivo;
            
            if (!move_uploaded_file($archivo['tmp_name'], $ruta_archivo)) {
                throw new Exception("Error al guardar el archivo de $tipo");
            }
            
            $archivos_subidos[$tipo] = $ruta_archivo;
            $archivos_procesados[] = $archivo['name'];
        }
        
        // Ejecutar procesamiento usando el orquestador principal
        $opciones = [
            'balance_file' => $archivos_subidos['balance'],
            'situacion_file' => $archivos_subidos['situacion'],
            'focus_file' => $archivos_subidos['focus']
        ];
        
        $resultado = executePythonOrchestrator('cartera', [], $opciones);
        
        if (isset($resultado['success']) && $resultado['success']) {
            $resultados = $resultado;
            $mensaje = "Procesamiento completado exitosamente";
            logActivity('procesar_cartera_success', [
                'archivos' => $archivos_procesados,
                'resultado' => $resultado
            ]);
        } else {
            throw new Exception("Error en el procesamiento: " . ($resultado['error'] ?? 'Error desconocido'));
        }
        
        // Limpiar archivos temporales
        foreach ($archivos_subidos as $archivo) {
            if (file_exists($archivo)) {
                unlink($archivo);
            }
        }
        
    } catch (Exception $e) {
        $mensaje = "Error: " . $e->getMessage();
        logActivity('procesar_cartera_error', [
            'error' => $e->getMessage(),
            'archivos' => $archivos_procesados ?? []
        ]);
        
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

// Obtener información del sistema para mostrar
$system_info = getSystemInfo();
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procesador Completo de Balance - Grupo Planeta</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .system-info {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 0.9em;
        }

        .content {
            padding: 40px;
        }

        .upload-section {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
        }

        .upload-section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .file-inputs {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .file-input-group {
            background: white;
            border-radius: 10px;
            padding: 20px;
            border: 2px dashed #ddd;
            transition: all 0.3s ease;
        }

        .file-input-group:hover {
            border-color: #667eea;
            transform: translateY(-2px);
        }

        .file-input-group label {
            display: block;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
        }

        .file-input-group input[type="file"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background: #f8f9fa;
        }

        .submit-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        .submit-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .message {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-weight: 500;
        }

        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .results-section {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
        }

        .results-section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .result-item {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }

        .result-item h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }

        .result-value {
            font-size: 1.2em;
            font-weight: 600;
            color: #667eea;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .loading img {
            width: 100px;
            height: 100px;
        }

        .loading p {
            margin-top: 20px;
            color: #666;
            font-size: 1.1em;
        }

        .back-btn {
            background: #6c757d;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }

        .back-btn:hover {
            background: #5a6268;
            transform: translateY(-1px);
        }

        @media (max-width: 768px) {
            .file-inputs {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-chart-line"></i> Procesador Completo de Balance</h1>
            <p>Sistema de Análisis Financiero - Grupo Planeta</p>
            <div class="system-info">
                <strong>Versión:</strong> <?php echo SYSTEM_VERSION; ?> | 
                <strong>Python:</strong> <?php echo $system_info['python_version']; ?> |
                <strong>Estado:</strong> <?php echo empty($errores_sistema) ? '<span style="color: #28a745;">✓ Operativo</span>' : '<span style="color: #dc3545;">✗ Con errores</span>'; ?>
            </div>
        </div>

        <div class="content">
            <a href="dashboard.php" class="back-btn">
                <i class="fas fa-arrow-left"></i> Volver al Dashboard
            </a>

            <?php if (!empty($errores_sistema)): ?>
                <div class="message error">
                    <strong>Errores de configuración:</strong><br>
                    <?php echo implode('<br>', $errores_sistema); ?>
                </div>
            <?php endif; ?>

            <?php if (!empty($mensaje)): ?>
                <div class="message <?php echo strpos($mensaje, 'Error') === 0 ? 'error' : 'success'; ?>">
                    <?php echo $mensaje; ?>
                    </div>
                <?php endif; ?>

            <div class="upload-section">
                <h2><i class="fas fa-upload"></i> Subir Archivos</h2>
                <form method="POST" enctype="multipart/form-data" id="uploadForm">
                    <div class="file-inputs">
                        <div class="file-input-group">
                            <label for="balance">
                                <i class="fas fa-file-excel"></i> Archivo de Balance
                            </label>
                            <input type="file" id="balance" name="balance" accept=".xlsx,.xls" required>
                        </div>

                        <div class="file-input-group">
                            <label for="situacion">
                                <i class="fas fa-file-excel"></i> Archivo de Situación
                            </label>
                            <input type="file" id="situacion" name="situacion" accept=".xlsx,.xls" required>
                        </div>

                        <div class="file-input-group">
                            <label for="focus">
                                <i class="fas fa-file-excel"></i> Archivo de Focus
                            </label>
                            <input type="file" id="focus" name="focus" accept=".xlsx,.xls" required>
                        </div>
                    </div>

                    <button type="submit" class="submit-btn" id="submitBtn">
                        <i class="fas fa-play"></i> Procesar Archivos
                    </button>
                </form>
            </div>

            <div class="loading" id="loading">
                <img src="planetacargando.gif" alt="Procesando...">
                <p>Procesando archivos, por favor espere...</p>
            </div>

            <?php if ($resultados): ?>
                <div class="results-section">
                <h2><i class="fas fa-chart-bar"></i> Resultados del Procesamiento</h2>
                
                    <?php if (isset($resultados['archivos_procesados'])): ?>
                        <div class="result-item">
                            <h3>Archivos Procesados</h3>
                            <p><?php echo implode(', ', $resultados['archivos_procesados']); ?></p>
                    </div>
                    <?php endif; ?>
                    
                    <?php if (isset($resultados['estadisticas'])): ?>
                        <div class="result-item">
                            <h3>Estadísticas</h3>
                            <p><strong>Registros procesados:</strong> <?php echo $resultados['estadisticas']['total_registros'] ?? 'N/A'; ?></p>
                            <p><strong>Tiempo de procesamiento:</strong> <?php echo $resultados['estadisticas']['tiempo_procesamiento'] ?? 'N/A'; ?> segundos</p>
                    </div>
                    <?php endif; ?>
                    
                    <?php if (isset($resultados['archivo_resultado'])): ?>
                        <div class="result-item">
                            <h3>Archivo de Resultado</h3>
                            <p><strong>Ruta:</strong> <?php echo $resultados['archivo_resultado']; ?></p>
                            <a href="descargar_resultado.php?archivo=<?php echo urlencode($resultados['archivo_resultado']); ?>" 
                               class="submit-btn" style="text-decoration: none; display: inline-block; margin-top: 10px;">
                                <i class="fas fa-download"></i> Descargar Resultado
                            </a>
                    </div>
                    <?php endif; ?>
            </div>
            <?php endif; ?>
        </div>
    </div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', function() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('submitBtn').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
        });
    </script>
</body>
</html> 