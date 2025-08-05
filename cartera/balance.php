<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procesador de Balance - Grupo Planeta</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="styles.css">
    <style>
        .balance-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            margin: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        .file-upload-section {
            margin-bottom: 30px;
            padding: 20px;
            border: 2px dashed #3b82f6;
            border-radius: 15px;
            text-align: center;
        }

        .file-input-group {
            margin: 15px 0;
        }

        .file-input-group label {
            display: block;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 8px;
        }

        .file-input-group input[type="file"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            font-size: 14px;
        }

        .calculate-btn {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
        }

        .calculate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
        }

        .results-section {
            margin-top: 30px;
            padding: 20px;
            background: #f8fafc;
            border-radius: 15px;
            border-left: 4px solid #3b82f6;
        }

        .result-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #e5e7eb;
        }

        .result-item:last-child {
            border-bottom: none;
        }

        .result-label {
            font-weight: 600;
            color: #1f2937;
        }

        .result-value {
            font-weight: 700;
            color: #3b82f6;
            font-size: 1.1em;
        }

        .error-message {
            background: #fef2f2;
            color: #dc2626;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #dc2626;
        }

        .success-message {
            background: #f0fdf4;
            color: #16a34a;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #16a34a;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }

        .loading img {
            width: 50px;
            height: 50px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>
                <i class="fas fa-balance-scale"></i>
                <span>Procesador de Balance</span>
            </h1>
            <p>Análisis de cuentas y cálculos financieros - Grupo Planeta</p>
        </div>

        <div class="balance-container">
            <form id="balanceForm" enctype="multipart/form-data">
                <div class="file-upload-section">
                    <h3><i class="fas fa-file-upload"></i> Cargar Archivos</h3>
                    
                    <div class="file-input-group">
                        <label for="balanceFile">Archivo BALANCE (CSV/Excel):</label>
                        <input type="file" id="balanceFile" name="balanceFile" accept=".csv,.xlsx,.xls" required>
                    </div>

                    <div class="file-input-group">
                        <label for="situacionFile">Archivo SITUACIÓN (CSV/Excel):</label>
                        <input type="file" id="situacionFile" name="situacionFile" accept=".csv,.xlsx,.xls" required>
                    </div>

                    <div class="file-input-group">
                        <label for="focusFile">Archivo FOCUS (CSV/Excel):</label>
                        <input type="file" id="focusFile" name="focusFile" accept=".csv,.xlsx,.xls" required>
                    </div>

                    <button type="submit" class="calculate-btn">
                        <i class="fas fa-calculator"></i> Calcular Balance
                    </button>
                    
                    <button type="button" id="debugBtn" class="calculate-btn" style="background: linear-gradient(135deg, #f59e0b, #d97706); margin-left: 10px;">
                        <i class="fas fa-bug"></i> Debug Archivos
                    </button>
                </div>
            </form>

            <div class="loading" id="loading">
                <img src="planetacargando.gif" alt="Procesando...">
                <p>Procesando archivos...</p>
            </div>

            <div id="results" class="results-section" style="display: none;">
                <h3><i class="fas fa-chart-bar"></i> Resultados del Análisis</h3>
                <div id="resultsContent"></div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('balanceForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');
            
            // Log de archivos seleccionados
            console.log('Archivos seleccionados:');
            console.log('Balance:', document.getElementById('balanceFile').files[0]);
            console.log('Situación:', document.getElementById('situacionFile').files[0]);
            console.log('Focus:', document.getElementById('focusFile').files[0]);
            
            loading.style.display = 'block';
            results.style.display = 'none';
            
            console.log('Enviando archivos para procesamiento...');
            fetch('procesar_balance_fixed.php', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                console.log('Respuesta recibida:', response);
                return response.json();
            })
            .then(data => {
                console.log('Datos procesados:', data);
                loading.style.display = 'none';
                results.style.display = 'block';
                
                if (data.success) {
                    displayResults(data.results);
                } else {
                    console.error('Error en el procesamiento:', data.message);
                    resultsContent.innerHTML = `<div class="error-message">${data.message}</div>`;
                }
            })
            .catch(error => {
                console.error('Error en la petición de procesamiento:', error);
                loading.style.display = 'none';
                results.style.display = 'block';
                resultsContent.innerHTML = `<div class="error-message">Error al procesar: ${error.message}</div>`;
            });
        });

        document.getElementById('debugBtn').addEventListener('click', function() {
            const formData = new FormData(document.getElementById('balanceForm'));
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');
            
            loading.style.display = 'block';
            results.style.display = 'none';
            
            console.log('Enviando archivos para debug...');
            fetch('debug_balance_python.php', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                console.log('Respuesta debug recibida:', response);
                return response.json();
            })
            .then(data => {
                console.log('Datos debug procesados:', data);
                loading.style.display = 'none';
                results.style.display = 'block';
                
                if (data.success) {
                    displayDebugResults(data.debug);
                } else {
                    console.error('Error en el debug:', data.message);
                    resultsContent.innerHTML = `<div class="error-message">${data.message}</div>`;
                }
            })
            .catch(error => {
                console.error('Error en la petición de debug:', error);
                loading.style.display = 'none';
                results.style.display = 'block';
                resultsContent.innerHTML = `<div class="error-message">Error al procesar: ${error.message}</div>`;
            });
        });

        function displayResults(results) {
            const resultsContent = document.getElementById('resultsContent');
            let html = '';

            // Sección de cuentas del archivo BALANCE
            html += '<h4>Archivo BALANCE - Totales por Cuenta Objeto</h4>';
            html += '<div class="result-item">';
            html += '<span class="result-label">Total cuenta objeto 43001:</span>';
            html += `<span class="result-value">${formatNumber(results.total_43001)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">Total cuenta objeto 43008:</span>';
            html += `<span class="result-value">${formatNumber(results.total_43008)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">Total cuenta objeto 43042:</span>';
            html += `<span class="result-value">${formatNumber(results.total_43042)}</span>`;
            html += '</div>';

            // Subcuentas específicas
            html += '<h4>Subcuentas Específicas</h4>';
            const subcuentas = ['0080.43002.20', '0080.43002.21', '0080.43002.15', 
                               '0080.43002.28', '0080.43002.31', '0080.43002.63'];
            
            subcuentas.forEach(subcuenta => {
                if (results.subcuentas && results.subcuentas[subcuenta]) {
                    html += '<div class="result-item">';
                    html += `<span class="result-label">${subcuenta}:</span>`;
                    html += `<span class="result-value">${formatNumber(results.subcuentas[subcuenta])}</span>`;
                    html += '</div>';
                }
            });

            // Archivo SITUACIÓN
            html += '<h4>Archivo SITUACIÓN</h4>';
            html += '<div class="result-item">';
            html += '<span class="result-label">TOTAL 01010 (SALDOS MES):</span>';
            html += `<span class="result-value">${formatNumber(results.situacion_total)}</span>`;
            html += '</div>';

            // Cálculos del archivo FOCUS
            html += '<h4>Cálculos FOCUS</h4>';
            html += '<div class="result-item">';
            html += '<span class="result-label">Deuda bruta NO Grupo (Inicial):</span>';
            html += `<span class="result-value">${formatNumber(results.deuda_bruta_inicial)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">Deuda bruta NO Grupo (Final):</span>';
            html += `<span class="result-value">${formatNumber(results.deuda_bruta_final)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">Dotaciones Acumuladas (Inicial):</span>';
            html += `<span class="result-value">${formatNumber(results.dotaciones_acumuladas_inicial)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">+/- Provisión acumulada (Final):</span>';
            html += `<span class="result-value">${formatNumber(results.provision_acumulada_final)}</span>`;
            html += '</div>';

            // Cálculos de cobros
            html += '<h4>Cálculos de Cobros</h4>';
            html += '<div class="result-item">';
            html += '<span class="result-label">Cobro de mes - Vencida:</span>';
            html += `<span class="result-value">${formatNumber(results.cobro_vencida)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">Cobro mes - Total Deuda:</span>';
            html += `<span class="result-value">${formatNumber(results.cobro_total_deuda)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">Cobros del mes - No Vencida:</span>';
            html += `<span class="result-value">${formatNumber(results.cobro_no_vencida)}</span>`;
            html += '</div>';

            // Vencidos en el mes
            html += '<h4>Vencidos en el Mes</h4>';
            html += '<div class="result-item">';
            html += '<span class="result-label">+/- Vencidos en el mes – vencido:</span>';
            html += `<span class="result-value">${formatNumber(results.vencidos_mes_vencido)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">+/- Vencidos en el mes – No vencido:</span>';
            html += `<span class="result-value">${formatNumber(results.vencidos_mes_no_vencido)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">+/- Vencidos en el mes – Total deuda:</span>';
            html += `<span class="result-value">${formatNumber(results.vencidos_mes_total)}</span>`;
            html += '</div>';

            // Facturación del mes
            html += '<h4>Facturación del Mes</h4>';
            html += '<div class="result-item">';
            html += '<span class="result-label">+ Facturación del mes – vencida:</span>';
            html += `<span class="result-value">${formatNumber(results.facturacion_vencida)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">+ Facturación del mes – no vencida:</span>';
            html += `<span class="result-value">${formatNumber(results.facturacion_no_vencida)}</span>`;
            html += '</div>';

            // Dotación del mes
            html += '<h4>Dotación del Mes</h4>';
            html += '<div class="result-item">';
            html += '<span class="result-label">Dotación del mes:</span>';
            html += `<span class="result-value">${formatNumber(results.dotacion_mes)}</span>`;
            html += '</div>';

            // Acumulado
            html += '<h4>Acumulado</h4>';
            html += '<div class="result-item">';
            html += '<span class="result-label">- Cobros:</span>';
            html += `<span class="result-value">${formatNumber(results.acumulado_cobros)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">+ Facturación:</span>';
            html += `<span class="result-value">${formatNumber(results.acumulado_facturacion)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">+/- Vencidos:</span>';
            html += `<span class="result-value">${formatNumber(results.acumulado_vencidos)}</span>`;
            html += '</div>';

            html += '<div class="result-item">';
            html += '<span class="result-label">DOTACIÓN:</span>';
            html += `<span class="result-value">${formatNumber(results.acumulado_dotacion)}</span>`;
            html += '</div>';

            resultsContent.innerHTML = html;
        }

        function formatNumber(num) {
            if (num === null || num === undefined) return 'N/A';
            return new Intl.NumberFormat('es-ES', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(num);
        }

        function displayDebugResults(debug) {
            const resultsContent = document.getElementById('resultsContent');
            let html = '<h3>Información de Debug de Archivos</h3>';
            
                         // Archivo BALANCE
             html += '<h4>Archivo BALANCE</h4>';
             html += `<div class="result-item"><span class="result-label">Archivo:</span><span class="result-value">${debug.balance.archivo}</span></div>`;
             html += `<div class="result-item"><span class="result-label">Total filas:</span><span class="result-value">${debug.balance.total_filas}</span></div>`;
             html += `<div class="result-item"><span class="result-label">Total columnas:</span><span class="result-value">${debug.balance.total_columnas}</span></div>`;
             html += `<div class="result-item"><span class="result-label">Tamaño archivo:</span><span class="result-value">${debug.balance.tamaño_bytes} bytes</span></div>`;
             html += `<div class="result-item"><span class="result-label">Extensión:</span><span class="result-value">${debug.balance.extension}</span></div>`;
             
             if (debug.balance.error) {
                 html += `<div class="result-item"><span class="result-label">Error:</span><span class="result-value" style="color: red;">${debug.balance.error}</span></div>`;
             } else {
                 html += '<h5>Nombres de columnas:</h5>';
                 html += '<div style="background: #f1f5f9; padding: 10px; border-radius: 5px; margin: 10px 0;">';
                 html += '<pre>' + JSON.stringify(debug.balance.nombres_columnas, null, 2) + '</pre>';
                 html += '</div>';
                 
                 html += '<h5>Muestra de filas:</h5>';
                 html += '<div style="background: #f1f5f9; padding: 10px; border-radius: 5px; margin: 10px 0;">';
                 html += '<pre>' + JSON.stringify(debug.balance.muestra_filas, null, 2) + '</pre>';
                 html += '</div>';
             }
            
                         // Archivo SITUACIÓN
             html += '<h4>Archivo SITUACIÓN</h4>';
             html += `<div class="result-item"><span class="result-label">Archivo:</span><span class="result-value">${debug.situacion.archivo}</span></div>`;
             html += `<div class="result-item"><span class="result-label">Total filas:</span><span class="result-value">${debug.situacion.total_filas}</span></div>`;
             html += `<div class="result-item"><span class="result-label">Total columnas:</span><span class="result-value">${debug.situacion.total_columnas}</span></div>`;
             html += `<div class="result-item"><span class="result-label">Tamaño archivo:</span><span class="result-value">${debug.situacion.tamaño_bytes} bytes</span></div>`;
             html += `<div class="result-item"><span class="result-label">Extensión:</span><span class="result-value">${debug.situacion.extension}</span></div>`;
             
             if (debug.situacion.error) {
                 html += `<div class="result-item"><span class="result-label">Error:</span><span class="result-value" style="color: red;">${debug.situacion.error}</span></div>`;
             } else {
                 html += '<h5>Nombres de columnas:</h5>';
                 html += '<div style="background: #f1f5f9; padding: 10px; border-radius: 5px; margin: 10px 0;">';
                 html += '<pre>' + JSON.stringify(debug.situacion.nombres_columnas, null, 2) + '</pre>';
                 html += '</div>';
             }
            
                         // Archivo FOCUS
             html += '<h4>Archivo FOCUS</h4>';
             html += `<div class="result-item"><span class="result-label">Archivo:</span><span class="result-value">${debug.focus.archivo}</span></div>`;
             html += `<div class="result-item"><span class="result-label">Total filas:</span><span class="result-value">${debug.focus.total_filas}</span></div>`;
             html += `<div class="result-item"><span class="result-label">Total columnas:</span><span class="result-value">${debug.focus.total_columnas}</span></div>`;
             html += `<div class="result-item"><span class="result-label">Tamaño archivo:</span><span class="result-value">${debug.focus.tamaño_bytes} bytes</span></div>`;
             html += `<div class="result-item"><span class="result-label">Extensión:</span><span class="result-value">${debug.focus.extension}</span></div>`;
             
             if (debug.focus.error) {
                 html += `<div class="result-item"><span class="result-label">Error:</span><span class="result-value" style="color: red;">${debug.focus.error}</span></div>`;
             } else {
                 html += '<h5>Nombres de columnas:</h5>';
                 html += '<div style="background: #f1f5f9; padding: 10px; border-radius: 5px; margin: 10px 0;">';
                 html += '<pre>' + JSON.stringify(debug.focus.nombres_columnas, null, 2) + '</pre>';
                 html += '</div>';
             }
            
            resultsContent.innerHTML = html;
        }
    </script>
</body>
</html> 