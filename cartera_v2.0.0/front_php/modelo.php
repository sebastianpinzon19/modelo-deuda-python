<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modelo de Deuda - Grupo Planeta</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Botón Volver -->
    <a href="index.php" class="back-button">
        <i class="fas fa-arrow-left"></i>
        Volver
    </a>

    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>
                <i class="fas fa-calculator"></i>
                <span>Modelo de Deuda</span>
            </h1>
            <p>Genera modelo de deuda combinando archivos de cartera y anticipos</p>
        </div>

        <!-- Generador de Modelo Deuda -->
        <div class="procesador-card" style="max-width: 800px; margin: 0 auto;">
            <div class="card-header">
                <div class="card-icon modelo">
                    <i class="fas fa-calculator"></i>
                </div>
                <div>
                    <h3 class="card-title">Modelo Deuda</h3>
                    <p class="card-subtitle">Genera modelo de deuda</p>
                </div>
            </div>

            <form id="form-modelo" method="post" enctype="multipart/form-data">
                <div class="form-group">
                    <label class="form-label">
                        <i class="fas fa-file-excel"></i> Archivo de Cartera Procesada
                    </label>
                    <div class="drop-zone" id="drop-zone-cartera-modelo">
                        <div class="drop-zone-icon">
                            <i class="fas fa-cloud-upload-alt"></i>
                        </div>
                        <div class="drop-zone-text">Arrastra el archivo de cartera</div>
                        <div class="drop-zone-hint">Solo archivos .XLSX</div>
                        <input type="file" name="cartera_file" accept=".xlsx,.xls" style="display: none;">
                    </div>

                    <div class="file-preview" id="preview-cartera-modelo" style="display: none;">
                        <div class="preview-header">
                            <i class="fas fa-eye"></i> Vista Previa del Archivo
                        </div>
                        <div class="preview-content" id="preview-content-cartera-modelo"></div>
                    </div>
                    <div class="file-info" id="file-info-cartera-modelo">
                        <div class="file-name" id="file-name-cartera-modelo"></div>
                        <div class="file-size" id="file-size-cartera-modelo"></div>
                    </div>

                    <div class="validation-message" id="validation-cartera-modelo" style="display: none;"></div>
                </div>

                <div class="form-group">
                    <label class="form-label">
                        <i class="fas fa-file-excel"></i> Archivo de Anticipos Procesados
                    </label>
                    <div class="drop-zone" id="drop-zone-anticipo-modelo">
                        <div class="drop-zone-icon">
                            <i class="fas fa-cloud-upload-alt"></i>
                        </div>
                        <div class="drop-zone-text">Arrastra el archivo de anticipos</div>
                        <div class="drop-zone-hint">Solo archivos .XLSX</div>
                        <input type="file" name="anticipos_file" accept=".xlsx,.xls" style="display: none;">
                    </div>

                    <div class="file-preview" id="preview-anticipo-modelo" style="display: none;">
                        <div class="preview-header">
                            <i class="fas fa-eye"></i> Vista Previa del Archivo
                        </div>
                        <div class="preview-content" id="preview-content-anticipo-modelo"></div>
                    </div>
                    <div class="file-info" id="file-info-anticipo-modelo">
                        <div class="file-name" id="file-name-anticipo-modelo"></div>
                        <div class="file-size" id="file-size-anticipo-modelo"></div>
                    </div>

                    <div class="validation-message" id="validation-anticipo-modelo" style="display: none;"></div>
                </div>

                <div class="form-group">
                    <label class="form-label">
                        <i class="fas fa-exchange-alt"></i> Tasas de Cambio (TRM)
                    </label>
                    <div class="trm-fields">
                        <div class="trm-field">
                            <label class="trm-label">
                                <i class="fas fa-dollar-sign"></i> Dólar (USD/COP)
                            </label>
                            <input type="number" name="trm_dolar" class="trm-input" step="0.01" min="0" placeholder="Ej: 4000" required>
                        </div>
                        <div class="trm-field">
                            <label class="trm-label">
                                <i class="fas fa-euro-sign"></i> Euro (EUR/COP)
                            </label>
                            <input type="number" name="trm_euro" class="trm-input" step="0.01" min="0" placeholder="Ej: 4700" required>
                        </div>
                    </div>
                    <small style="color:#6b7280;font-size:12px;margin-top:4px;display:block;">
                        Ingresa las tasas de cambio para las conversiones de moneda en el modelo de deuda
                    </small>
                </div>

                <button type="submit" class="btn btn-primary" id="btn-modelo">
                    <i class="fas fa-cog"></i>
                    <span>Generar Modelo Deuda</span>
                    <div class="btn-loading" style="display: none;">
                        <i class="fas fa-spinner fa-spin"></i>
                    </div>
                </button>
            </form>

            <div class="progress-container" id="progress-modelo">
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill-modelo"></div>
                </div>
                <div class="progress-text" id="progress-text-modelo">Iniciando procesamiento...</div>
            </div>
        </div>
    </div>

    <!-- Toast Container -->
    <div class="toast-container" id="toast-container"></div>

    <!-- Modal -->
    <div class="modal" id="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-icon" id="modal-icon">
                    <i class="fas fa-check"></i>
                </div>
                <h3 class="modal-title" id="modal-title">Procesamiento Completado</h3>
            </div>
            <div class="modal-body">
                <div class="modal-message" id="modal-message"></div>
                <div class="modal-actions" id="modal-actions">
                    <button class="btn-modal secondary" onclick="closeModal()">Cerrar</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Utility functions
        function showToast(message, type = 'success', duration = 5000) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            
            const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'exclamation-triangle';
            
            toast.innerHTML = `
                <div class="toast-icon">
                    <i class="fas fa-${icon}"></i>
                </div>
                <div class="toast-content">
                    <div class="toast-title">${type === 'success' ? 'Éxito' : type === 'error' ? 'Error' : 'Advertencia'}</div>
                    <div class="toast-message">${message}</div>
                </div>
            `;
            
            container.appendChild(toast);
            
            setTimeout(() => toast.classList.add('show'), 100);
            
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => container.removeChild(toast), 300);
            }, duration);
        }

        function showModal(title, message, type = 'success', actions = []) {
            const modal = document.getElementById('modal');
            const modalIcon = document.getElementById('modal-icon');
            const modalTitle = document.getElementById('modal-title');
            const modalMessage = document.getElementById('modal-message');
            const modalActions = document.getElementById('modal-actions');
            
            modalTitle.textContent = title;
            modalMessage.textContent = message;
            
            // Set icon and color based on type
            const icon = type === 'success' ? 'check' : type === 'error' ? 'times' : 'exclamation-triangle';
            modalIcon.className = `modal-icon ${type}`;
            modalIcon.innerHTML = `<i class="fas fa-${icon}"></i>`;
            
            // Set actions
            modalActions.innerHTML = actions.length > 0 ? actions.join('') : 
                '<button class="btn-modal secondary" onclick="closeModal()">Cerrar</button>';
            
            modal.classList.add('show');
        }

        function closeModal() {
            document.getElementById('modal').classList.remove('show');
        }

        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        function validateFile(file, allowedTypes, maxSize = 50 * 1024 * 1024) {
            const errors = [];
            
            if (!allowedTypes.some(type => file.name.toLowerCase().endsWith(type))) {
                errors.push(`Tipo de archivo no válido. Permitidos: ${allowedTypes.join(', ')}`);
            }
            
            if (file.size > maxSize) {
                errors.push(`Archivo demasiado grande. Máximo: ${formatFileSize(maxSize)}`);
            }
            
            return errors;
        }

        // Drag & Drop functionality
        function setupDropZone(dropZoneId, fileInputName, allowedTypes, maxSize) {
            const dropZone = document.getElementById(dropZoneId);
            const fileInput = dropZone.querySelector('input[type="file"]');
            
            // Obtener elementos de información del archivo
            let fileInfo, fileName, fileSize, validation, previewId, contentId;
            
            if (dropZoneId.includes('modelo')) {
                // Para archivos del modelo de deuda
                const suffix = dropZoneId.split('-').slice(-2).join('-'); // 'cartera-modelo' o 'anticipo-modelo'
                fileInfo = document.getElementById(`file-info-${suffix}`);
                fileName = document.getElementById(`file-name-${suffix}`);
                fileSize = document.getElementById(`file-size-${suffix}`);
                validation = document.getElementById(`validation-${suffix}`);
                previewId = `preview-${suffix}`;
                contentId = `preview-content-${suffix}`;
            } else {
                // Para archivos normales
                const suffix = dropZoneId.split('-').pop();
                fileInfo = document.getElementById(`file-info-${suffix}`);
                fileName = document.getElementById(`file-name-${suffix}`);
                fileSize = document.getElementById(`file-size-${suffix}`);
                validation = document.getElementById(`validation-${suffix}`);
                previewId = `preview-${suffix}`;
                contentId = `preview-content-${suffix}`;
            }

            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, preventDefaults, false);
            });

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, highlight, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, unhighlight, false);
            });

            function highlight(e) {
                dropZone.classList.add('dragover');
            }

            function unhighlight(e) {
                dropZone.classList.remove('dragover');
            }

            dropZone.addEventListener('drop', handleDrop, false);
            dropZone.addEventListener('click', () => fileInput.click());
            fileInput.addEventListener('change', handleFileSelect);

            function handleDrop(e) {
                const dt = e.dataTransfer;
                const files = dt.files;
                handleFiles(files);
            }

            function handleFileSelect(e) {
                const files = e.target.files;
                handleFiles(files);
            }

            function handleFiles(files) {
                if (files.length > 0) {
                    const file = files[0];
                    const errors = validateFile(file, allowedTypes, maxSize);
                    
                    if (errors.length > 0) {
                        if (validation) {
                            validation.innerHTML = errors.join('<br>');
                            validation.className = 'validation-message error';
                            validation.style.display = 'block';
                        }
                        dropZone.classList.remove('has-file');
                        if (fileInfo) fileInfo.classList.remove('show');
                        if (previewId && document.getElementById(previewId)) {
                            document.getElementById(previewId).style.display = 'none';
                        }
                        showToast(errors[0], 'error');
                        return;
                    }

                    if (fileName) fileName.textContent = file.name;
                    if (fileSize) fileSize.textContent = formatFileSize(file.size);
                    if (fileInfo) fileInfo.classList.add('show');
                    dropZone.classList.add('has-file');
                    if (validation) validation.style.display = 'none';
                    
                    showToast(`Archivo "${file.name}" seleccionado correctamente`, 'success');
                }
            }
        }

        // Form submission with progress
        function submitForm(formId, progressId, btnId, url) {
            const form = document.getElementById(formId);
            const progress = document.getElementById(progressId);
            const btn = document.getElementById(btnId);
            const progressFill = document.getElementById(`progress-fill-${progressId.split('-').pop()}`);
            const progressText = document.getElementById(`progress-text-${progressId.split('-').pop()}`);

            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Validate form
                const formData = new FormData(form);
                let isValid = true;
                
                // Validación específica para el modelo de deuda
                const carteraFile = formData.get('cartera_file');
                const anticiposFile = formData.get('anticipos_file');
                const trmDolar = formData.get('trm_dolar');
                const trmEuro = formData.get('trm_euro');
                
                if (!carteraFile || !carteraFile.name) {
                    showToast('Por favor selecciona el archivo de cartera procesada', 'error');
                    isValid = false;
                } else if (!anticiposFile || !anticiposFile.name) {
                    showToast('Por favor selecciona el archivo de anticipos procesados', 'error');
                    isValid = false;
                } else if (!trmDolar || trmDolar.trim() === '') {
                    showToast('Por favor ingresa el TRM del Dólar', 'error');
                    isValid = false;
                } else if (isNaN(parseFloat(trmDolar)) || parseFloat(trmDolar) <= 0) {
                    showToast('El TRM del Dólar debe ser un número válido mayor a 0', 'error');
                    isValid = false;
                } else if (!trmEuro || trmEuro.trim() === '') {
                    showToast('Por favor ingresa el TRM del Euro', 'error');
                    isValid = false;
                } else if (isNaN(parseFloat(trmEuro)) || parseFloat(trmEuro) <= 0) {
                    showToast('El TRM del Euro debe ser un número válido mayor a 0', 'error');
                    isValid = false;
                }
                
                if (!isValid) return;

                // Show progress
                progress.classList.add('show');
                btn.disabled = true;
                btn.innerHTML = '<span class="loading-spinner"></span>Procesando...';
                
                // Simulate progress
                let progressValue = 0;
                const progressInterval = setInterval(() => {
                    progressValue += Math.random() * 15;
                    if (progressValue > 90) progressValue = 90;
                    progressFill.style.width = progressValue + '%';
                    progressText.textContent = `Procesando... ${Math.round(progressValue)}%`;
                }, 500);

                // Submit form
                fetch(url, {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.text())
                .then(data => {
                    clearInterval(progressInterval);
                    progressFill.style.width = '100%';
                    progressText.textContent = 'Completado';
                    
                    setTimeout(() => {
                        progress.classList.remove('show');
                        btn.disabled = false;
                        btn.innerHTML = '<i class="fas fa-cog"></i> <span>Generar Modelo Deuda</span>';
                        
                        // Parse response and show modal
                        let type = 'success';
                        let title = 'Procesamiento Exitoso';
                        let message = 'El modelo de deuda se ha generado correctamente.';
                        let actions = [];
                        
                        if (data.includes('Error') || data.includes('No se pudo')) {
                            type = 'error';
                            title = 'Error en el Procesamiento';
                            message = 'Ocurrió un error durante el procesamiento.';
                        } else if (data.includes('ADVERTENCIA')) {
                            type = 'warning';
                            title = 'Procesamiento con Advertencias';
                            message = 'El modelo se generó pero hay algunas advertencias.';
                        }
                        
                        // Extract download link if available
                        const downloadMatch = data.match(/<a[^>]*href="([^"]*)"[^>]*class="btn-descarga"[^>]*>([^<]+)<\/a>/);
                        if (downloadMatch) {
                            actions.push(`<a href="${downloadMatch[1]}" class="btn-modal primary" target="_blank">${downloadMatch[2]}</a>`);
                        }
                        
                        actions.push('<button class="btn-modal secondary" onclick="closeModal()">Cerrar</button>');
                        
                        showModal(title, message, type, actions);
                        
                    }, 1000);
                })
                .catch(error => {
                    clearInterval(progressInterval);
                    progress.classList.remove('show');
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fas fa-cog"></i> <span>Generar Modelo Deuda</span>';
                    
                    showModal('Error de Conexión', 'No se pudo conectar con el servidor. Por favor intenta nuevamente.', 'error');
                    console.error('Error:', error);
                });
            });
        }

        // Initialize
        setupDropZone('drop-zone-cartera-modelo', 'cartera_file', ['.xlsx', '.xls'], 10 * 1024 * 1024);
        setupDropZone('drop-zone-anticipo-modelo', 'anticipos_file', ['.xlsx', '.xls'], 10 * 1024 * 1024);
        submitForm('form-modelo', 'progress-modelo', 'btn-modelo', 'modelo_deuda.php');

        // Close modal when clicking outside
        document.getElementById('modal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });

        // Welcome message
        setTimeout(() => {
            showToast('¡Bienvenido al generador de Modelo de Deuda! Completa todos los campos para comenzar.', 'success', 3000);
        }, 1000);
    </script>
</body>
</html> 