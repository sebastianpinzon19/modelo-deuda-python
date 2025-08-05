<?php
session_start();
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: no-cache, no-store, must-revalidate');
header('Pragma: no-cache');
header('Expires: 0');

// Incluir configuración centralizada
require_once 'config.php';

// Limpiar archivos antiguos
limpiarArchivosAntiguos(DIR_TEMP);
limpiarArchivosAntiguos(DIR_RESULTADOS);

// Obtener estadísticas usando la función mejorada
$estadisticas = obtenerEstadisticasSistema();
$totalArchivos = $estadisticas['total_archivos'];
$archivosRecientes = $estadisticas['archivos_recientes'];

// Verificar salud del sistema
$problemasSistema = verificarSaludSistema();
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>Sistema de Procesamiento de Cartera - Grupo Planeta</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="front_php/styles.css">
    <style>
        /* Estilos adicionales para la nueva interfaz */
        .hero-section {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
            color: white;
            padding: 4rem 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
        }

        .hero-content {
            position: relative;
            z-index: 2;
        }

        .hero-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }

        .hero-subtitle {
            font-size: 1.25rem;
            opacity: 0.9;
            margin-bottom: 2rem;
        }

        .upload-section {
            background: white;
            border-radius: 20px;
            padding: 3rem;
            margin: -2rem 2rem 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            position: relative;
            z-index: 10;
        }

        .upload-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .upload-card {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
        }

        .upload-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 1;
        }

        .upload-card:hover::before {
            opacity: 0.1;
        }

        .upload-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
            border-color: var(--primary-color);
        }

        .upload-icon {
            font-size: 3rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
            position: relative;
            z-index: 2;
        }

        .upload-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
            position: relative;
            z-index: 2;
        }

        .upload-description {
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
            line-height: 1.6;
            position: relative;
            z-index: 2;
        }

        .upload-form {
            position: relative;
            z-index: 2;
        }

        .file-input-wrapper {
            position: relative;
            margin-bottom: 1rem;
        }

        .file-input {
            position: absolute;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }

        .file-input-label {
            display: block;
            padding: 1rem 2rem;
            background: var(--primary-color);
            color: white;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .file-input-label:hover {
            background: var(--primary-dark);
            transform: translateY(-2px);
        }

        .file-info {
            display: none;
            margin-top: 1rem;
            padding: 1rem;
            background: var(--success-light);
            border-radius: 8px;
            border-left: 4px solid var(--success-color);
        }

        .file-info.show {
            display: block;
            animation: slideUp 0.3s ease;
        }

        .file-name {
            font-weight: 600;
            color: var(--text-primary);
        }

        .file-size {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .upload-btn {
            background: var(--success-color);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 1rem;
        }

        .upload-btn:hover:not(:disabled) {
            background: #059669;
            transform: translateY(-2px);
        }

        .upload-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .stats-section {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
        }

        .stat-card {
            text-align: center;
            padding: 1.5rem;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 15px;
            border-left: 4px solid var(--primary-color);
        }

        .stat-icon {
            font-size: 2rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-radius: 10px;
            padding: 1rem 1.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            z-index: 1000;
            transform: translateX(400px);
            transition: transform 0.3s ease;
            border-left: 4px solid var(--success-color);
        }

        .notification.show {
            transform: translateX(0);
        }

        .notification.success {
            border-left-color: var(--success-color);
        }

        .notification.error {
            border-left-color: var(--error-color);
        }

        .notification-icon {
            margin-right: 0.5rem;
            color: var(--success-color);
        }

        .notification.error .notification-icon {
            color: var(--error-color);
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .loading {
            display: none;
            text-align: center;
            padding: 2rem;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid var(--primary-color);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin: 1rem 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
            width: 0%;
            transition: width 0.3s ease;
        }

        @media (max-width: 768px) {
            .hero-title {
                font-size: 2rem;
            }
            
            .upload-section {
                margin: -1rem 1rem 1rem;
                padding: 2rem 1rem;
            }
            
            .upload-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <!-- Notificación flotante -->
    <div id="notification" class="notification">
        <i class="fas fa-check-circle notification-icon"></i>
        <span id="notification-text">Archivo procesado exitosamente</span>
    </div>

    <!-- Sección Hero -->
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">
                <i class="fas fa-chart-line"></i>
                Sistema de Procesamiento de Cartera
            </h1>
            <p class="hero-subtitle">
                Plataforma integral para el procesamiento de datos financieros del Grupo Planeta
            </p>
            <div class="hero-badges">
                <span class="badge badge-primary">
                    <i class="fas fa-shield-alt"></i>
                    Seguro
                </span>
                <span class="badge badge-secondary">
                    <i class="fas fa-bolt"></i>
                    Rápido
                </span>
                <span class="badge badge-accent">
                    <i class="fas fa-check-circle"></i>
                    Confiable
                </span>
                <a href="limpiar_cache.php" class="badge badge-accent" style="text-decoration: none; color: inherit;">
                    <i class="fas fa-sync-alt"></i>
                    Actualizar
                </a>
            </div>
        </div>
    </div>

    <!-- Sección de Subida de Archivos -->
    <div class="upload-section">
        <h2 class="text-center mb-4">
            <i class="fas fa-upload"></i>
            Subir Archivos Individuales
        </h2>
        <p class="text-center mb-4" style="color: var(--text-secondary);">
            Selecciona el tipo de archivo que deseas procesar y súbelo individualmente
        </p>

        <div class="upload-grid">
            <!-- Formato Deuda -->
            <div class="upload-card">
                <div class="upload-icon">
                    <i class="fas fa-file-invoice-dollar"></i>
                </div>
                <h3 class="upload-title">Formato Deuda</h3>
                <p class="upload-description">
                    Procesamiento completo de formato deuda con provisión, anticipos, balance y focus
                </p>
                <form class="upload-form" action="procesar_formato_deuda.php" method="post" enctype="multipart/form-data">
                    <div class="file-input-wrapper">
                        <input type="file" name="archivo" class="file-input" accept=".xlsx,.xls,.csv" required>
                        <label for="file-input-1" class="file-input-label">
                            <i class="fas fa-cloud-upload-alt"></i>
                            Seleccionar Archivo
                        </label>
                    </div>
                    <div class="file-info" id="file-info-1">
                        <div class="file-name" id="file-name-1"></div>
                        <div class="file-size" id="file-size-1"></div>
                    </div>
                    <button type="submit" class="upload-btn" id="upload-btn-1">
                        <i class="fas fa-cogs"></i>
                        Procesar Formato Deuda
                    </button>
                </form>
            </div>

            <!-- Balance -->
            <div class="upload-card">
                <div class="upload-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <h3 class="upload-title">Balance Completo</h3>
                <p class="upload-description">
                    Procesamiento de archivos de balance, situación y focus para análisis financiero
                </p>
                <form class="upload-form" action="procesar_balance.php" method="post" enctype="multipart/form-data">
                    <div class="file-input-wrapper">
                        <input type="file" name="archivo" class="file-input" accept=".xlsx,.xls,.csv" required>
                        <label for="file-input-2" class="file-input-label">
                            <i class="fas fa-cloud-upload-alt"></i>
                            Seleccionar Archivo
                        </label>
                    </div>
                    <div class="file-info" id="file-info-2">
                        <div class="file-name" id="file-name-2"></div>
                        <div class="file-size" id="file-size-2"></div>
                    </div>
                    <button type="submit" class="upload-btn" id="upload-btn-2">
                        <i class="fas fa-cogs"></i>
                        Procesar Balance
                    </button>
                </form>
            </div>

            <!-- Cartera -->
            <div class="upload-card">
                <div class="upload-icon">
                    <i class="fas fa-file-csv"></i>
                </div>
                <h3 class="upload-title">Cartera</h3>
                <p class="upload-description">
                    Procesamiento de archivos de cartera con validaciones y formatos flexibles
                </p>
                <form class="upload-form" action="procesar_cartera.php" method="post" enctype="multipart/form-data">
                    <div class="file-input-wrapper">
                        <input type="file" name="archivo" class="file-input" accept=".xlsx,.xls,.csv" required>
                        <label for="file-input-3" class="file-input-label">
                            <i class="fas fa-cloud-upload-alt"></i>
                            Seleccionar Archivo
                        </label>
                    </div>
                    <div class="file-info" id="file-info-3">
                        <div class="file-name" id="file-name-3"></div>
                        <div class="file-size" id="file-size-3"></div>
                    </div>
                    <button type="submit" class="upload-btn" id="upload-btn-3">
                        <i class="fas fa-cogs"></i>
                        Procesar Cartera
                    </button>
                </form>
            </div>

            <!-- Anticipos -->
            <div class="upload-card">
                <div class="upload-icon">
                    <i class="fas fa-money-bill-wave"></i>
                </div>
                <h3 class="upload-title">Anticipos</h3>
                <p class="upload-description">
                    Procesamiento de archivos de anticipos con análisis detallado
                </p>
                <form class="upload-form" action="procesar_anticipos.php" method="post" enctype="multipart/form-data">
                    <div class="file-input-wrapper">
                        <input type="file" name="archivo" class="file-input" accept=".xlsx,.xls,.csv" required>
                        <label for="file-input-4" class="file-input-label">
                            <i class="fas fa-cloud-upload-alt"></i>
                            Seleccionar Archivo
                        </label>
                    </div>
                    <div class="file-info" id="file-info-4">
                        <div class="file-name" id="file-name-4"></div>
                        <div class="file-size" id="file-size-4"></div>
                    </div>
                    <button type="submit" class="upload-btn" id="upload-btn-4">
                        <i class="fas fa-cogs"></i>
                        Procesar Anticipos
                    </button>
                </form>
            </div>
        </div>

        <!-- Loading -->
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Procesando archivo...</p>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill"></div>
            </div>
        </div>
    </div>

    <!-- Sección de Estadísticas -->
    <div class="stats-section">
        <h2 class="text-center mb-4">
            <i class="fas fa-chart-bar"></i>
            Estadísticas del Sistema
        </h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-file-alt"></i>
                </div>
                <div class="stat-value" data-stat="total"><?php echo $totalArchivos; ?></div>
                <div class="stat-label">Archivos Totales</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-clock"></i>
                </div>
                <div class="stat-value" data-stat="recientes"><?php echo $archivosRecientes; ?></div>
                <div class="stat-label">Archivos Recientes (24h)</div>
            </div>
            <?php if (!empty($problemasSistema)): ?>
            <div class="stat-card warning">
                <div class="stat-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <div class="stat-value"><?php echo count($problemasSistema); ?></div>
                <div class="stat-label">Problemas Detectados</div>
            </div>
            <?php else: ?>
            <div class="stat-card success">
                <div class="stat-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-value">OK</div>
                <div class="stat-label">Sistema Saludable</div>
            </div>
            <?php endif; ?>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <div class="stat-value">100%</div>
                <div class="stat-label">Seguridad</div>
            </div>
        </div>
    </div>

    <!-- Enlaces Rápidos -->
    <div class="stats-section">
        <h2 class="text-center mb-4">
            <i class="fas fa-link"></i>
            Accesos Rápidos
        </h2>
        <div class="stats-grid">
            <a href="descargar_archivos.php" class="stat-card" style="text-decoration: none; color: inherit;">
                <div class="stat-icon">
                    <i class="fas fa-download"></i>
                </div>
                <div class="stat-value">Descargar</div>
                <div class="stat-label">Archivos</div>
            </a>
            <a href="test_sistema.php" class="stat-card" style="text-decoration: none; color: inherit;" target="_blank">
                <div class="stat-icon">
                    <i class="fas fa-tools"></i>
                </div>
                <div class="stat-value">Test</div>
                <div class="stat-label">Sistema</div>
            </a>
            <a href="ESTADO_FINAL_SISTEMA.md" class="stat-card" style="text-decoration: none; color: inherit;" target="_blank">
                <div class="stat-icon">
                    <i class="fas fa-book"></i>
                </div>
                <div class="stat-value">Ver</div>
                <div class="stat-label">Documentación</div>
            </a>
            <a href="logs/" class="stat-card" style="text-decoration: none; color: inherit;" target="_blank">
                <div class="stat-icon">
                    <i class="fas fa-clipboard-list"></i>
                </div>
                <div class="stat-value">Ver</div>
                <div class="stat-label">Logs</div>
            </a>
        </div>
    </div>

    <script>
        // Funcionalidad para manejo de archivos
        document.querySelectorAll('.file-input').forEach((input, index) => {
            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    // Validar archivo en el cliente
                    if (!validarArchivoCliente(file)) {
                        input.value = ''; // Limpiar input
                        return;
                    }
                    
                    const fileInfo = document.getElementById(`file-info-${index + 1}`);
                    const fileName = document.getElementById(`file-name-${index + 1}`);
                    const fileSize = document.getElementById(`file-size-${index + 1}`);
                    
                    fileName.textContent = file.name;
                    fileSize.textContent = formatFileSize(file.size);
                    fileInfo.classList.add('show');
                }
            });
        });

        // Funcionalidad para formularios
        document.querySelectorAll('.upload-form').forEach((form, index) => {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData(form);
                const loading = document.getElementById('loading');
                const progressFill = document.getElementById('progress-fill');
                
                // Mostrar loading
                loading.classList.add('show');
                
                // Simular progreso
                let progress = 0;
                const progressInterval = setInterval(() => {
                    progress += Math.random() * 15;
                    if (progress > 90) progress = 90;
                    progressFill.style.width = progress + '%';
                }, 200);
                
                fetch(form.action, {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    return response.text();
                })
                .then(data => {
                    clearInterval(progressInterval);
                    progressFill.style.width = '100%';
                    
                    // Intentar parsear como JSON
                    let responseData;
                    try {
                        responseData = JSON.parse(data);
                    } catch (e) {
                        // Si no es JSON, tratar como texto plano
                        responseData = { success: true, message: data };
                    }
                    
                    setTimeout(() => {
                        loading.classList.remove('show');
                        
                        if (responseData.success) {
                            showNotification(responseData.message || 'Archivo procesado exitosamente', 'success');
                            
                            // Limpiar formulario
                            form.reset();
                            document.getElementById(`file-info-${index + 1}`).classList.remove('show');
                            
                            // Actualizar estadísticas si están disponibles
                            if (responseData.data) {
                                actualizarEstadisticas();
                            }
                            
                            // Mostrar botón para descargar archivos
                            setTimeout(() => {
                                if (confirm('¿Deseas descargar los archivos generados?')) {
                                    window.location.href = 'descargar_archivos.php';
                                }
                            }, 2000);
                        } else {
                            showNotification(responseData.message || 'Error al procesar el archivo', 'error');
                        }
                    }, 1000);
                })
                .catch(error => {
                    clearInterval(progressInterval);
                    loading.classList.remove('show');
                    console.error('Error en la petición:', error);
                    showNotification('Error de conexión: ' + error.message, 'error');
                });
            });
        });

        // Función para formatear tamaño de archivo
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        // Función para mostrar notificaciones mejorada
        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            const notificationText = document.getElementById('notification-text');
            const notificationIcon = notification.querySelector('.notification-icon');
            
            notificationText.textContent = message;
            notification.className = `notification ${type}`;
            notificationIcon.className = `fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} notification-icon`;
            
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 5000);
        }

        // Función para actualizar estadísticas
        function actualizarEstadisticas() {
            // Actualizar contadores en tiempo real
            const totalElement = document.querySelector('.stat-value[data-stat="total"]');
            const recientesElement = document.querySelector('.stat-value[data-stat="recientes"]');
            
            if (totalElement && recientesElement) {
                // Incrementar contadores
                const totalActual = parseInt(totalElement.textContent) || 0;
                const recientesActual = parseInt(recientesElement.textContent) || 0;
                
                totalElement.textContent = totalActual + 1;
                recientesElement.textContent = recientesActual + 1;
                
                // Agregar animación
                totalElement.style.transform = 'scale(1.1)';
                recientesElement.style.transform = 'scale(1.1)';
                
                setTimeout(() => {
                    totalElement.style.transform = 'scale(1)';
                    recientesElement.style.transform = 'scale(1)';
                }, 300);
            }
        }

        // Función para validar archivo antes de enviar
        function validarArchivoCliente(file) {
            const maxSize = 50 * 1024 * 1024; // 50MB
            const allowedTypes = ['xlsx', 'xls', 'csv'];
            
            if (file.size > maxSize) {
                showNotification('El archivo es demasiado grande. Máximo 50MB.', 'error');
                return false;
            }
            
            const extension = file.name.split('.').pop().toLowerCase();
            if (!allowedTypes.includes(extension)) {
                showNotification('Tipo de archivo no permitido. Solo Excel (.xlsx, .xls) y CSV (.csv)', 'error');
                return false;
            }
            
            if (file.size === 0) {
                showNotification('El archivo está vacío.', 'error');
                return false;
            }
            
            return true;
        }

        // Animaciones al cargar la página
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.upload-card');
            cards.forEach((card, index) => {
                setTimeout(() => {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    card.style.transition = 'all 0.5s ease';
                    
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 100);
                }, index * 100);
            });
        });
    </script>
</body>
</html> 