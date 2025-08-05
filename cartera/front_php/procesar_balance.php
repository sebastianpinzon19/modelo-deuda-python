<?php
session_start();
header('Content-Type: text/html; charset=utf-8');

// Configuración
$python_path = 'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe';
$python_script = '../PROVCA/procesador_balance_completo.py';
$upload_dir = '../temp/';
$max_file_size = 50 * 1024 * 1024; // 50MB

// Crear directorio temporal si no existe
if (!file_exists($upload_dir)) {
    mkdir($upload_dir, 0777, true);
}

$mensaje = '';
$resultados = null;
$archivos_procesados = [];

// Procesar formulario
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    try {
        $archivos_requeridos = ['balance', 'situacion', 'focus'];
        $archivos_subidos = [];
        
        // Verificar archivos subidos
        foreach ($archivos_requeridos as $tipo) {
            if (!isset($_FILES[$tipo]) || $_FILES[$tipo]['error'] !== UPLOAD_ERR_OK) {
                throw new Exception("Error al subir el archivo de $tipo");
            }
            
            $archivo = $_FILES[$tipo];
            
            // Validaciones
            if ($archivo['size'] > $max_file_size) {
                throw new Exception("El archivo de $tipo es demasiado grande (máximo 50MB)");
            }
            
            $extension = strtolower(pathinfo($archivo['name'], PATHINFO_EXTENSION));
            if (!in_array($extension, ['xlsx', 'xls'])) {
                throw new Exception("El archivo de $tipo debe ser un archivo Excel (.xlsx o .xls)");
            }
            
            // Guardar archivo
            $nombre_archivo = $tipo . '_' . date('Y-m-d_H-i-s') . '.' . $extension;
            $ruta_archivo = $upload_dir . $nombre_archivo;
            
            if (!move_uploaded_file($archivo['tmp_name'], $ruta_archivo)) {
                throw new Exception("Error al guardar el archivo de $tipo");
            }
            
            $archivos_subidos[$tipo] = $ruta_archivo;
            $archivos_procesados[] = $archivo['name'];
        }
        
        // Ejecutar procesador Python
        $comando = "\"$python_path\" \"$python_script\" \"{$archivos_subidos['balance']}\" \"{$archivos_subidos['situacion']}\" \"{$archivos_subidos['focus']}\" 2>&1";
        
        $output = [];
        $return_code = 0;
        
        exec($comando, $output, $return_code);
        
        if ($return_code !== 0) {
            throw new Exception("Error en el procesamiento Python: " . implode("\n", $output));
        }
        
        // Leer resultados
        if (file_exists('../resultados/resultados_balance_completo.json')) {
            $json_resultados = file_get_contents('../resultados/resultados_balance_completo.json');
            $resultados = json_decode($json_resultados, true);
            
            if ($resultados === null) {
                throw new Exception("Error al leer los resultados JSON");
            }
            
            $mensaje = "Procesamiento completado exitosamente";
        } else {
            throw new Exception("No se encontró el archivo de resultados");
        }
        
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
    <title>Procesador de Balance - Grupo Planeta</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <img src="Logo grupo planeta color transparente.jpg" alt="Grupo Planeta">
            </div>
            <h1>Procesador de Balance Completo</h1>
            <p>Sistema de procesamiento financiero integrado</p>
        </div>

        <div class="content">
            <?php if ($mensaje): ?>
                <div class="alert <?php echo strpos($mensaje, 'Error') !== false ? 'error' : 'success'; ?>">
                    <i class="fas <?php echo strpos($mensaje, 'Error') !== false ? 'fa-exclamation-triangle' : 'fa-check-circle'; ?>"></i>
                    <?php echo htmlspecialchars($mensaje); ?>
                </div>
            <?php endif; ?>

            <form method="POST" enctype="multipart/form-data" class="upload-form">
                <div class="form-group">
                    <label for="balance">
                        <i class="fas fa-file-excel"></i>
                        Archivo BALANCE
                    </label>
                    <input type="file" id="balance" name="balance" accept=".xlsx,.xls" required>
                    <small>Archivo Excel con datos de cuentas objeto y saldos</small>
                </div>

                <div class="form-group">
                    <label for="situacion">
                        <i class="fas fa-file-excel"></i>
                        Archivo SITUACIÓN
                    </label>
                    <input type="file" id="situacion" name="situacion" accept=".xlsx,.xls" required>
                    <small>Archivo Excel con datos de cobros y saldos mensuales</small>
                </div>

                <div class="form-group">
                    <label for="focus">
                        <i class="fas fa-file-excel"></i>
                        Archivo FOCUS
                    </label>
                    <input type="file" id="focus" name="focus" accept=".xlsx,.xls" required>
                    <small>Archivo Excel con datos de vencimientos y dotaciones</small>
                </div>

                <button type="submit" class="btn-primary">
                    <i class="fas fa-cogs"></i>
                    Procesar Balance Completo
                </button>
            </form>

            <?php if ($resultados): ?>
                <div class="results">
                    <h2><i class="fas fa-chart-line"></i> Resultados del Procesamiento</h2>
                    
                    <div class="result-section">
                        <h3>Resumen de Cálculos</h3>
                        <div class="result-grid">
                            <div class="result-item">
                                <span class="label">Cobros Vencida:</span>
                                <span class="value"><?php echo formatear_numero($resultados['resumen_calculos']['cobros']['vencida']); ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Cobros No Vencida:</span>
                                <span class="value"><?php echo formatear_numero($resultados['resumen_calculos']['cobros']['no_vencida']); ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Facturación Vencida:</span>
                                <span class="value"><?php echo formatear_numero($resultados['resumen_calculos']['facturacion']['vencida']); ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Facturación No Vencida:</span>
                                <span class="value"><?php echo formatear_numero($resultados['resumen_calculos']['facturacion']['no_vencida']); ?></span>
                            </div>
                        </div>
                    </div>

                    <div class="result-section">
                        <h3>Provisión y Dotación</h3>
                        <div class="result-grid">
                            <div class="result-item">
                                <span class="label">Provisión:</span>
                                <span class="value"><?php echo formatear_numero($resultados['provision_dotacion']['provision']); ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Dotación:</span>
                                <span class="value"><?php echo formatear_numero($resultados['provision_dotacion']['dotacion']); ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Dotaciones:</span>
                                <span class="value"><?php echo formatear_numero($resultados['provision_dotacion']['dotaciones']); ?></span>
                            </div>
                            <div class="result-item">
                                <span class="label">Desdotaciones:</span>
                                <span class="value"><?php echo formatear_numero($resultados['provision_dotacion']['desdotaciones']); ?></span>
                            </div>
                        </div>
                    </div>

                    <div class="result-section">
                        <h3>Archivos Procesados</h3>
                        <ul class="file-list">
                            <?php foreach ($archivos_procesados as $archivo): ?>
                                <li><i class="fas fa-file-excel"></i> <?php echo htmlspecialchars($archivo); ?></li>
                            <?php endforeach; ?>
                        </ul>
                    </div>

                    <div class="download-section">
                        <a href="../resultados/BALANCE_COMPLETO_<?php echo date('Y-m-d_H-i-s'); ?>.xlsx" class="btn-download" download>
                            <i class="fas fa-download"></i>
                            Descargar Reporte Excel
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
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
            btn.disabled = true;
        });
    </script>
</body>
</html>
