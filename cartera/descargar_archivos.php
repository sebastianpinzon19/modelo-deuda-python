<?php
require_once 'config.php';

// Obtener archivos de resultados
$archivos_resultados = [];
if (is_dir(DIR_RESULTADOS)) {
    $archivos = glob(DIR_RESULTADOS . '*');
    foreach ($archivos as $archivo) {
        if (is_file($archivo)) {
            $archivos_resultados[] = [
                'nombre' => basename($archivo),
                'ruta' => $archivo,
                'tamaño' => formatBytes(filesize($archivo)),
                'fecha' => date('d/m/Y H:i:s', filemtime($archivo)),
                'tipo' => pathinfo($archivo, PATHINFO_EXTENSION)
            ];
        }
    }
}

// Ordenar por fecha más reciente
usort($archivos_resultados, function($a, $b) {
    return filemtime($b['ruta']) - filemtime($a['ruta']);
});
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Descargar Archivos - Sistema de Procesamiento de Cartera</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="front_php/styles.css">
    <style>
        .download-section {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .file-list {
            display: grid;
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .file-item {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 10px;
            padding: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .file-item:hover {
            border-color: var(--primary-color);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .file-info {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .file-icon {
            width: 50px;
            height: 50px;
            background: var(--primary-color);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
        }
        
        .file-details h3 {
            margin: 0;
            color: var(--text-primary);
            font-weight: 600;
        }
        
        .file-details p {
            margin: 0.25rem 0 0 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        .download-btn {
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .download-btn:hover {
            background: var(--primary-dark);
            transform: translateY(-1px);
        }
        
        .empty-state {
            text-align: center;
            padding: 3rem;
            color: var(--text-secondary);
        }
        
        .empty-state i {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        
        .back-btn {
            background: var(--secondary-color);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 2rem;
        }
        
        .back-btn:hover {
            background: var(--secondary-dark);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="download-section">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
                <a href="index.php" class="back-btn">
                    <i class="fas fa-arrow-left"></i>
                    Volver al Dashboard
                </a>
                <h1 style="margin: 0;">
                    <i class="fas fa-download"></i>
                    Descargar Archivos Generados
                </h1>
            </div>
            
            <?php if (empty($archivos_resultados)): ?>
                <div class="empty-state">
                    <i class="fas fa-folder-open"></i>
                    <h2>No hay archivos disponibles</h2>
                    <p>Los archivos generados aparecerán aquí después de procesar datos.</p>
                    <a href="index.php" class="download-btn">
                        <i class="fas fa-upload"></i>
                        Ir a Procesar Archivos
                    </a>
                </div>
            <?php else: ?>
                <div class="file-list">
                    <?php foreach ($archivos_resultados as $archivo): ?>
                        <div class="file-item">
                            <div class="file-info">
                                <div class="file-icon">
                                    <?php if ($archivo['tipo'] === 'xlsx'): ?>
                                        <i class="fas fa-file-excel"></i>
                                    <?php elseif ($archivo['tipo'] === 'csv'): ?>
                                        <i class="fas fa-file-csv"></i>
                                    <?php elseif ($archivo['tipo'] === 'json'): ?>
                                        <i class="fas fa-file-code"></i>
                                    <?php else: ?>
                                        <i class="fas fa-file"></i>
                                    <?php endif; ?>
                                </div>
                                <div class="file-details">
                                    <h3><?php echo htmlspecialchars($archivo['nombre']); ?></h3>
                                    <p>
                                        <i class="fas fa-calendar"></i> <?php echo $archivo['fecha']; ?> |
                                        <i class="fas fa-weight-hanging"></i> <?php echo $archivo['tamaño']; ?>
                                    </p>
                                </div>
                            </div>
                            <a href="<?php echo $archivo['ruta']; ?>" class="download-btn" download>
                                <i class="fas fa-download"></i>
                                Descargar
                            </a>
                        </div>
                    <?php endforeach; ?>
                </div>
                
                <div style="margin-top: 2rem; text-align: center;">
                    <p style="color: var(--text-secondary);">
                        <i class="fas fa-info-circle"></i>
                        Los archivos se eliminan automáticamente después de 7 días para mantener el sistema limpio.
                    </p>
                </div>
            <?php endif; ?>
        </div>
    </div>
</body>
</html> 