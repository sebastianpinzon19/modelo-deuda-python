<?php
/**
 * Estado del Sistema - Sistema de Cartera Grupo Planeta
 * Versión: 2.0.1
 * 
 * Página de monitoreo del estado del sistema y configuración
 */

require_once 'configuracion.php';

// Log de actividad
logActivity('estado_sistema_consultado');

// Obtener información del sistema
$system_info = getSystemInfo();
$errores_sistema = checkPermissions();

// Verificar dependencias Python
$dependencias_python = [];
$dependencias_requeridas = ['pandas', 'numpy', 'openpyxl', 'xlrd'];

foreach ($dependencias_requeridas as $dep) {
    $output = shell_exec(PYTHON_EXE . " -c \"import $dep\" 2>&1");
    $dependencias_python[$dep] = strpos($output, 'ImportError') === false && strpos($output, 'ModuleNotFoundError') === false;
}

// Verificar archivos importantes
$archivos_importantes = [
    'Orquestador Principal' => ORQUESTADOR_PRINCIPAL,
    'Configuración Python' => PYTHON_DIR . 'config.py',
    'Logger Python' => PYTHON_DIR . 'logger.py',
    'Utilidades Python' => PYTHON_DIR . 'utilidades_cartera.py',
    'Requirements Python' => PYTHON_DIR . 'requirements.txt',
    'README Python' => PYTHON_DIR . 'README.md'
];

$estado_archivos = [];
foreach ($archivos_importantes as $nombre => $ruta) {
    $estado_archivos[$nombre] = [
        'existe' => file_exists($ruta),
        'ruta' => $ruta,
        'tamano' => file_exists($ruta) ? filesize($ruta) : 0,
        'modificado' => file_exists($ruta) ? date('Y-m-d H:i:s', filemtime($ruta)) : 'N/A'
    ];
}

// Verificar directorios
$directorios_importantes = [
    'Directorio Base' => BASE_DIR,
    'Directorio Python' => PYTHON_DIR,
    'Directorio Resultados' => PROCESSED_DIR,
    'Directorio Temporal' => TEMP_DIR,
    'Directorio Logs' => LOGS_DIR,
    'Directorio Logs Python' => PYTHON_LOGS_DIR
];

$estado_directorios = [];
foreach ($directorios_importantes as $nombre => $ruta) {
    $estado_directorios[$nombre] = [
        'existe' => is_dir($ruta),
        'escribible' => is_writable($ruta),
        'ruta' => $ruta
    ];
}

// Probar comunicación con Python
$test_python = shell_exec(PYTHON_EXE . ' --version 2>&1');
$python_funcionando = strpos($test_python, 'Python') !== false;

// Probar orquestador
$test_orquestador = '';
$orquestador_funcionando = false;
if (file_exists(ORQUESTADOR_PRINCIPAL)) {
    $test_orquestador = shell_exec(PYTHON_EXE . ' ' . escapeshellarg(ORQUESTADOR_PRINCIPAL) . ' --help 2>&1');
    $orquestador_funcionando = strpos($test_orquestador, 'usage:') !== false || strpos($test_orquestador, 'help') !== false;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estado del Sistema - Grupo Planeta</title>
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

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }

        .status-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            border-left: 4px solid #667eea;
        }

        .status-card h3 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.3em;
            display: flex;
            align-items: center;
        }

        .status-card h3 i {
            margin-right: 10px;
            color: #667eea;
        }

        .status-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }

        .status-item:last-child {
            border-bottom: none;
        }

        .status-label {
            font-weight: 500;
            color: #2c3e50;
        }

        .status-value {
            font-weight: 600;
        }

        .status-ok {
            color: #28a745;
        }

        .status-error {
            color: #dc3545;
        }

        .status-warning {
            color: #ffc107;
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

        .refresh-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            display: inline-block;
            margin-left: 10px;
            transition: all 0.3s ease;
        }

        .refresh-btn:hover {
            background: #218838;
            transform: translateY(-1px);
        }

        .system-overview {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
        }

        .system-overview h2 {
            font-size: 2em;
            margin-bottom: 15px;
        }

        .system-status {
            font-size: 1.2em;
            margin-bottom: 20px;
        }

        .error-list {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }

        .error-list h3 {
            margin-bottom: 15px;
        }

        .error-list ul {
            list-style: none;
        }

        .error-list li {
            padding: 5px 0;
            border-bottom: 1px solid #f5c6cb;
        }

        .error-list li:last-child {
            border-bottom: none;
        }

        @media (max-width: 768px) {
            .status-grid {
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
            <h1><i class="fas fa-server"></i> Estado del Sistema</h1>
            <p>Sistema de Análisis Financiero - Grupo Planeta v<?php echo SYSTEM_VERSION; ?></p>
        </div>

        <div class="content">
            <a href="dashboard.php" class="back-btn">
                <i class="fas fa-arrow-left"></i> Volver al Dashboard
            </a>
            <a href="estado_sistema.php" class="refresh-btn">
                <i class="fas fa-sync-alt"></i> Actualizar
            </a>

            <div class="system-overview">
                <h2>Resumen del Sistema</h2>
                <div class="system-status">
                    <?php if (empty($errores_sistema) && $python_funcionando && $orquestador_funcionando): ?>
                        <i class="fas fa-check-circle"></i> Sistema Operativo
                    <?php elseif (empty($errores_sistema) && $python_funcionando): ?>
                        <i class="fas fa-exclamation-triangle"></i> Sistema Parcialmente Operativo
                    <?php else: ?>
                        <i class="fas fa-times-circle"></i> Sistema con Problemas
                    <?php endif; ?>
                </div>
                <p>Versión: <?php echo SYSTEM_VERSION; ?> | Python: <?php echo trim($system_info['python_version']); ?></p>
            </div>

            <?php if (!empty($errores_sistema)): ?>
                <div class="error-list">
                    <h3><i class="fas fa-exclamation-triangle"></i> Errores de Configuración</h3>
                    <ul>
                        <?php foreach ($errores_sistema as $error): ?>
                            <li><?php echo htmlspecialchars($error); ?></li>
                        <?php endforeach; ?>
                    </ul>
                </div>
            <?php endif; ?>

            <div class="status-grid">
                <div class="status-card">
                    <h3><i class="fas fa-python"></i> Configuración Python</h3>
                    <div class="status-item">
                        <span class="status-label">Python Detectado:</span>
                        <span class="status-value <?php echo $python_funcionando ? 'status-ok' : 'status-error'; ?>">
                            <?php echo $python_funcionando ? '✓ Sí' : '✗ No'; ?>
                        </span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Ruta Python:</span>
                        <span class="status-value"><?php echo $system_info['python_path']; ?></span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Versión Python:</span>
                        <span class="status-value"><?php echo trim($system_info['python_version']); ?></span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Orquestador:</span>
                        <span class="status-value <?php echo $orquestador_funcionando ? 'status-ok' : 'status-error'; ?>">
                            <?php echo $orquestador_funcionando ? '✓ Funcionando' : '✗ No funciona'; ?>
                        </span>
                    </div>
                </div>

                <div class="status-card">
                    <h3><i class="fas fa-box"></i> Dependencias Python</h3>
                    <?php foreach ($dependencias_python as $dep => $instalada): ?>
                        <div class="status-item">
                            <span class="status-label"><?php echo ucfirst($dep); ?>:</span>
                            <span class="status-value <?php echo $instalada ? 'status-ok' : 'status-error'; ?>">
                                <?php echo $instalada ? '✓ Instalada' : '✗ No instalada'; ?>
                            </span>
                        </div>
                    <?php endforeach; ?>
                </div>

                <div class="status-card">
                    <h3><i class="fas fa-folder"></i> Directorios del Sistema</h3>
                    <?php foreach ($estado_directorios as $nombre => $info): ?>
                        <div class="status-item">
                            <span class="status-label"><?php echo $nombre; ?>:</span>
                            <span class="status-value <?php echo $info['existe'] && $info['escribible'] ? 'status-ok' : ($info['existe'] ? 'status-warning' : 'status-error'); ?>">
                                <?php echo $info['existe'] ? ($info['escribible'] ? '✓ OK' : '⚠ Solo lectura') : '✗ No existe'; ?>
                            </span>
                        </div>
                    <?php endforeach; ?>
                </div>

                <div class="status-card">
                    <h3><i class="fas fa-file-code"></i> Archivos Importantes</h3>
                    <?php foreach ($estado_archivos as $nombre => $info): ?>
                        <div class="status-item">
                            <span class="status-label"><?php echo $nombre; ?>:</span>
                            <span class="status-value <?php echo $info['existe'] ? 'status-ok' : 'status-error'; ?>">
                                <?php echo $info['existe'] ? '✓ Existe' : '✗ No existe'; ?>
                            </span>
                        </div>
                    <?php endforeach; ?>
                </div>

                <div class="status-card">
                    <h3><i class="fas fa-cogs"></i> Configuración PHP</h3>
                    <div class="status-item">
                        <span class="status-label">Versión PHP:</span>
                        <span class="status-value"><?php echo PHP_VERSION; ?></span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Tiempo máximo ejecución:</span>
                        <span class="status-value"><?php echo ini_get('max_execution_time'); ?>s</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Límite memoria:</span>
                        <span class="status-value"><?php echo ini_get('memory_limit'); ?></span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Tamaño máximo archivo:</span>
                        <span class="status-value"><?php echo ini_get('upload_max_filesize'); ?></span>
                    </div>
                </div>

                <div class="status-card">
                    <h3><i class="fas fa-chart-line"></i> Estadísticas</h3>
                    <div class="status-item">
                        <span class="status-label">Archivos en temp:</span>
                        <span class="status-value"><?php echo count(glob(TEMP_DIR . '/*.*')); ?></span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Archivos en resultados:</span>
                        <span class="status-value"><?php echo count(glob(PROCESSED_DIR . '/*.*')); ?></span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Logs PHP:</span>
                        <span class="status-value"><?php echo file_exists(LOGS_DIR . 'php_activity.log') ? filesize(LOGS_DIR . 'php_activity.log') . ' bytes' : 'No existe'; ?></span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Última actualización:</span>
                        <span class="status-value"><?php echo date('Y-m-d H:i:s'); ?></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
