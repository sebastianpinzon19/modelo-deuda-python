<?php
// cartera.php
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procesar Cartera - Grupo Planeta</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <a href="index.php" class="back-button">
        <i class="fas fa-arrow-left"></i>
        Volver
    </a>

    <div class="container">
        <div class="header">
            <h1>
                <i class="fas fa-file-invoice-dollar"></i>
                <span>Procesar Cartera</span>
            </h1>
            <p>Procesa archivos PROVCA.CSV para generar reportes de cartera</p>
        </div>

        <div class="procesador-card" style="max-width: 800px; margin: 0 auto;">
            <div class="card-header">
                <div class="card-icon cartera">
                    <i class="fas fa-file-invoice-dollar"></i>
                </div>
                <div>
                    <h3 class="card-title">Cartera (Provisión)</h3>
                    <p class="card-subtitle">Procesa archivos PROVCA.CSV</p>
                </div>
            </div>

            <form id="form-cartera" action="procesar.php" method="post" enctype="multipart/form-data">
                <input type="hidden" name="tipo" value="cartera">
                
                <div class="drop-zone" id="drop-zone-cartera">
                    <div class="drop-zone-icon">
                        <i class="fas fa-cloud-upload-alt"></i>
                    </div>
                    <div class="drop-zone-text">Arrastra tu archivo aquí o haz clic</div>
                    <div class="drop-zone-hint">Solo archivos .CSV</div>
                    <input type="file" name="archivo" accept=".csv" style="display: none;" required>
                </div>

                <div class="file-info" id="file-info-cartera">
                    <div class="file-name" id="file-name-cartera"></div>
                    <div class="file-size" id="file-size-cartera"></div>
                </div>

                <div class="validation-message" id="validation-cartera" style="display: none;"></div>

                <div class="form-group">
                    <label for="fecha_cierre" class="form-label">
                        <i class="fas fa-calendar-alt"></i>
                        Fecha de Cierre
                    </label>
                    <input type="date" 
                           id="fecha_cierre" 
                           name="fecha_cierre" 
                           class="form-input"
                           value="<?php echo date('Y-m-d'); ?>"
                           required>
                </div>

                <button type="submit" class="btn btn-primary" id="btn-cartera">
                    <i class="fas fa-cog"></i>
                    <span>Procesar Cartera</span>
                </button>
            </form>

            <div class="progress-container" id="progress-cartera">
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill-cartera"></div>
                </div>
                <div class="progress-text" id="progress-text-cartera">Iniciando procesamiento...</div>
            </div>
        </div>
    </div>

    <div class="toast-container" id="toast-container"></div>

    <script>
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

        function validateFile(file, allowedTypes, maxSize = 50 * 1024 * 1024) {
            const errors = [];
            if (!allowedTypes.some(type => file.name.toLowerCase().endsWith(type))) {
                errors.push(`Tipo de archivo no válido. Permitidos: ${allowedTypes.join(', ')}`);
            }
            if (file.size > maxSize) {
                errors.push(`Archivo demasiado grande. Máximo: ${(maxSize / 1024 / 1024)}MB`);
            }
            return errors;
        }

        function setupDropZone(dropZoneId, allowedTypes, maxSize) {
            const dropZone = document.getElementById(dropZoneId);
            const fileInput = dropZone.querySelector('input[type="file"]');
            const fileName = document.getElementById(`file-name-${dropZoneId.split('-').pop()}`);
            const fileSize = document.getElementById(`file-size-${dropZoneId.split('-').pop()}`);
            const validation = document.getElementById(`validation-${dropZoneId.split('-').pop()}`);
            const fileInfo = document.getElementById(`file-info-${dropZoneId.split('-').pop()}`);

            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(e => 
                dropZone.addEventListener(e, ev => { ev.preventDefault(); ev.stopPropagation(); }, false)
            );

            ['dragenter', 'dragover'].forEach(e => dropZone.addEventListener(e, () => dropZone.classList.add('dragover'), false));
            ['dragleave', 'drop'].forEach(e => dropZone.addEventListener(e, () => dropZone.classList.remove('dragover'), false));

            dropZone.addEventListener('drop', e => handleFiles(e.dataTransfer.files));
            dropZone.addEventListener('click', () => fileInput.click());
            fileInput.addEventListener('change', e => handleFiles(e.target.files));

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
                    fileSize.textContent = (file.size / 1024).toFixed(2) + ' KB';
                    fileInfo.classList.add('show');
                    dropZone.classList.add('has-file');
                    validation.style.display = 'none';
                    showToast(`Archivo "${file.name}" seleccionado correctamente`, 'success');
                }
            }
        }

        setupDropZone('drop-zone-cartera', ['.csv'], 10 * 1024 * 1024);
    </script>
</body>
</html>
