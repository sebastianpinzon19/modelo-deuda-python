<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procesar Anticipos - Grupo Planeta</title>
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
                <i class="fas fa-hand-holding-usd"></i>
                <span>Procesar Anticipos</span>
            </h1>
            <p>Procesa archivos de anticipos para generar reportes</p>
        </div>

        <!-- Procesador de Anticipos -->
        <div class="procesador-card" style="max-width: 800px; margin: 0 auto;">
            <div class="card-header">
                <div class="card-icon anticipo">
                    <i class="fas fa-hand-holding-usd"></i>
                </div>
                <div>
                    <h3 class="card-title">Anticipos</h3>
                    <p class="card-subtitle">Procesa archivos de anticipos</p>
                </div>
            </div>

            <form id="form-anticipo" action="procesar.php" method="post" enctype="multipart/form-data">
                <input type="hidden" name="tipo" value="anticipo">
                
                <div class="drop-zone" id="drop-zone-anticipo">
                    <div class="drop-zone-icon">
                        <i class="fas fa-cloud-upload-alt"></i>
                    </div>
                    <div class="drop-zone-text">Arrastra tu archivo aquí o haz clic</div>
                    <div class="drop-zone-hint">Archivos .XLSX, .XLS o .CSV</div>
                    <input type="file" name="archivo" accept=".xlsx,.xls,.csv" style="display: none;" required>
                </div>

                <div class="file-preview" id="preview-anticipo" style="display: none;">
                    <div class="preview-header">
                        <i class="fas fa-eye"></i> Vista Previa del Archivo
                    </div>
                    <div class="preview-content" id="preview-content-anticipo"></div>
                </div>

                <div class="file-info" id="file-info-anticipo">
                    <div class="file-name" id="file-name-anticipo"></div>
                    <div class="file-size" id="file-size-anticipo"></div>
                </div>

                <div class="validation-message" id="validation-anticipo" style="display: none;"></div>

                <button type="submit" class="btn btn-primary" id="btn-anticipo">
                    <i class="fas fa-cog"></i>
                    <span>Procesar Anticipos</span>
                    <div class="btn-loading" style="display: none;">
                        <i class="fas fa-spinner fa-spin"></i>
                    </div>
                </button>
            </form>

            <div class="progress-container" id="progress-anticipo">
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill-anticipo"></div>
                </div>
                <div class="progress-text" id="progress-text-anticipo">Iniciando procesamiento...</div>
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
            const fileInfo = document.getElementById(`file-info-${dropZoneId.split('-').pop()}`);
            const fileName = document.getElementById(`file-name-${dropZoneId.split('-').pop()}`);
            const fileSize = document.getElementById(`file-size-${dropZoneId.split('-').pop()}`);
            const validation = document.getElementById(`validation-${dropZoneId.split('-').pop()}`);

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
                        validation.innerHTML = errors.join('<br>');
                        validation.className = 'validation-message error';
                        validation.style.display = 'block';
                        dropZone.classList.remove('has-file');
                        fileInfo.classList.remove('show');
                        showToast(errors[0], 'error');
                        return;
                    }

                    fileName.textContent = file.name;
                    fileSize.textContent = formatFileSize(file.size);
                    fileInfo.classList.add('show');
                    dropZone.classList.add('has-file');
                    validation.style.display = 'none';
                    
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
                
                for (let [key, value] of formData.entries()) {
                    if (key.includes('file') && !value.name) {
                        showToast('Por favor selecciona un archivo', 'error');
                        isValid = false;
                        break;
                    }
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
                        btn.innerHTML = '<i class="fas fa-cog"></i> <span>Procesar Anticipos</span>';
                        
                        // Parse response and show modal
                        let type = 'success';
                        let title = 'Procesamiento Exitoso';
                        let message = 'El archivo se ha procesado correctamente.';
                        let actions = [];
                        
                        if (data.includes('Error') || data.includes('No se pudo')) {
                            type = 'error';
                            title = 'Error en el Procesamiento';
                            message = 'Ocurrió un error durante el procesamiento.';
                        } else if (data.includes('ADVERTENCIA')) {
                            type = 'warning';
                            title = 'Procesamiento con Advertencias';
                            message = 'El archivo se procesó pero hay algunas advertencias.';
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
                    btn.innerHTML = '<i class="fas fa-cog"></i> <span>Procesar Anticipos</span>';
                    
                    showModal('Error de Conexión', 'No se pudo conectar con el servidor. Por favor intenta nuevamente.', 'error');
                    console.error('Error:', error);
                });
            });
        }

        // Initialize
        setupDropZone('drop-zone-anticipo', 'archivo', ['.xlsx', '.xls', '.csv'], 10 * 1024 * 1024);
        submitForm('form-anticipo', 'progress-anticipo', 'btn-anticipo', 'procesar.php');

        // Close modal when clicking outside
        document.getElementById('modal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });

        // Welcome message
        setTimeout(() => {
            showToast('¡Bienvenido al procesador de Anticipos! Arrastra tu archivo para comenzar.', 'success', 3000);
        }, 1000);
    </script>
</body>
</html> 