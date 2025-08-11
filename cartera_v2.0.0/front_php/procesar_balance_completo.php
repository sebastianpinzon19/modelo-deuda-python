<?php
session_start();
header('Content-Type: text/html; charset=utf-8');

// Configuración
$python_path = 'C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe';
$python_script = 'PROVCA/procesador_balance_completo.py';
$upload_dir = 'temp/';
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
        if (file_exists('resultados_balance_completo.json')) {
            $json_resultados = file_get_contents('resultados_balance_completo.json');
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
            padding: 15px 40px;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: block;
            margin: 0 auto;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
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
            display: none;
        }

        .results-section.show {
            display: block;
        }

        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .result-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }

        .result-card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.3em;
            display: flex;
            align-items: center;
        }

        .result-card h3 i {
            margin-right: 10px;
            color: #667eea;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        .data-table th,
        .data-table td {
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid #eee;
        }

        .data-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }

        .data-table td {
            font-family: 'Courier New', monospace;
            font-weight: 500;
        }

        .positive {
            color: #28a745;
        }

        .negative {
            color: #dc3545;
        }

        .summary-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
        }

        .summary-section h2 {
            margin-bottom: 20px;
            font-size: 1.8em;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .summary-item {
            text-align: center;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }

        .summary-item h4 {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 10px;
        }

        .summary-item .value {
            font-size: 1.5em;
            font-weight: 600;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
            .content {
                padding: 20px;
            }
            
            .file-inputs {
                grid-template-columns: 1fr;
            }
            
            .results-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
     <!-- Botón Volver -->
    <a href="index.php" style="position: fixed; top: 20px; left: 20px; z-index: 1000; text-decoration: none;">
        <button style="background: #2c3e50; color: white; border: none; padding: 10px 20px; border-radius: 5px;">
            <i class="fas fa-arrow-left"></i> Volver
        </button>
    </a>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-chart-line"></i> Procesador Completo de Balance</h1>
            <p>Grupo Planeta - Análisis Financiero Integrado</p>
        </div>

        <div class="content">
            <div class="upload-section">
                <h2><i class="fas fa-upload"></i> Subir Archivos</h2>
                
                <?php if ($mensaje): ?>
                    <div class="message <?= strpos($mensaje, 'Error') !== false ? 'error' : 'success' ?>">
                        <?= htmlspecialchars($mensaje) ?>
                    </div>
                <?php endif; ?>

                <form method="POST" enctype="multipart/form-data" id="uploadForm">
                    <div class="file-inputs">
                        <div class="file-input-group">
                            <label for="balance">
                                <i class="fas fa-file-excel"></i> Archivo BALANCE
                            </label>
                            <input type="file" name="balance" id="balance" accept=".xlsx,.xls" required>
                            <small>Archivo Excel con datos de balance</small>
                        </div>

                        <div class="file-input-group">
                            <label for="situacion">
                                <i class="fas fa-file-excel"></i> Archivo SITUACIÓN
                            </label>
                            <input type="file" name="situacion" id="situacion" accept=".xlsx,.xls" required>
                            <small>Archivo Excel con datos de situación</small>
                        </div>

                        <div class="file-input-group">
                            <label for="focus">
                                <i class="fas fa-file-excel"></i> Archivo FOCUS
                            </label>
                            <input type="file" name="focus" id="focus" accept=".xlsx,.xls" required>
                            <small>Archivo Excel con datos de focus</small>
                        </div>
                    </div>

                    <button type="submit" class="submit-btn" id="submitBtn">
                        <i class="fas fa-cogs"></i> Procesar Archivos
                    </button>
                </form>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Procesando archivos... Por favor espere.</p>
            </div>

            <?php if ($resultados): ?>
            <div class="results-section show" id="resultsSection">
                <h2><i class="fas fa-chart-bar"></i> Resultados del Procesamiento</h2>
                
                <div class="results-grid">
                    <div class="result-card">
                        <h3><i class="fas fa-calculator"></i> Resumen de Cálculos</h3>
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Concepto</th>
                                    <th>Vencida</th>
                                    <th>No Vencida</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($resultados['reporte_final']['resumen_calculos'] as $concepto => $valores): ?>
                                <tr>
                                    <td><?= htmlspecialchars($concepto) ?></td>
                                    <td class="<?= $valores['vencida'] >= 0 ? 'positive' : 'negative' ?>">
                                        <?= formatear_numero($valores['vencida']) ?>
                                    </td>
                                    <td class="<?= $valores['no_vencida'] >= 0 ? 'positive' : 'negative' ?>">
                                        <?= formatear_numero($valores['no_vencida']) ?>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>

                    <div class="result-card">
                        <h3><i class="fas fa-coins"></i> Provisión y Dotación</h3>
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Concepto</th>
                                    <th>Valor</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($resultados['reporte_final']['provision_dotacion'] as $concepto => $valor): ?>
                                <tr>
                                    <td><?= htmlspecialchars($concepto) ?></td>
                                    <td class="<?= $valor >= 0 ? 'positive' : 'negative' ?>">
                                        <?= $valor !== '' ? formatear_numero($valor) : '-' ?>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>

                    <div class="result-card">
                        <h3><i class="fas fa-chart-area"></i> Acumulado</h3>
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Concepto</th>
                                    <th>Vencida</th>
                                    <th>No Vencida</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($resultados['reporte_final']['acumulado'] as $concepto => $valores): ?>
                                <tr>
                                    <td><?= htmlspecialchars($concepto) ?></td>
                                    <td class="<?= $valores['vencida'] >= 0 ? 'positive' : 'negative' ?>">
                                        <?= formatear_numero($valores['vencida']) ?>
                                    </td>
                                    <td class="<?= $valores['no_vencida'] >= 0 ? 'positive' : 'negative' ?>">
                                        <?= formatear_numero($valores['no_vencida']) ?>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>

                    <div class="result-card">
                        <h3><i class="fas fa-balance-scale"></i> Deuda Final</h3>
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Concepto</th>
                                    <th>Valor</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($resultados['reporte_final']['deuda_final'] as $concepto => $valor): ?>
                                <tr>
                                    <td><?= htmlspecialchars($concepto) ?></td>
                                    <td class="<?= $valor >= 0 ? 'positive' : 'negative' ?>">
                                        <?= formatear_numero($valor) ?>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="summary-section">
                    <h2><i class="fas fa-chart-pie"></i> Resumen Ejecutivo</h2>
                    <div class="summary-grid">
                        <div class="summary-item">
                            <h4>Total Cobros</h4>
                            <div class="value">
                                <?= formatear_numero($resultados['reporte_final']['resumen_calculos']['- Cobros']['vencida'] + 
                                                   $resultados['reporte_final']['resumen_calculos']['- Cobros']['no_vencida']) ?>
                            </div>
                        </div>
                        <div class="summary-item">
                            <h4>Total Facturación</h4>
                            <div class="value">
                                <?= formatear_numero($resultados['reporte_final']['resumen_calculos']['+ Facturación']['vencida'] + 
                                                   $resultados['reporte_final']['resumen_calculos']['+ Facturación']['no_vencida']) ?>
                            </div>
                        </div>
                        <div class="summary-item">
                            <h4>Total Vencidos</h4>
                            <div class="value">
                                <?= formatear_numero($resultados['reporte_final']['resumen_calculos']['+/- Vencidos']['vencida'] + 
                                                   $resultados['reporte_final']['resumen_calculos']['+/- Vencidos']['no_vencida']) ?>
                            </div>
                        </div>
                        <div class="summary-item">
                            <h4>Deuda Final</h4>
                            <div class="value">
                                <?= formatear_numero($resultados['reporte_final']['deuda_final']['deuda_bruta_no_grupo_final']) ?>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <?php endif; ?>
        </div>
    </div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', function() {
            document.getElementById('loading').classList.add('show');
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('submitBtn').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
        });

        // Mostrar/ocultar resultados
        <?php if ($resultados): ?>
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
        <?php endif; ?>
    </script>
</body>
</html> 