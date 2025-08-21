<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procesador de Archivos - Grupo Planeta</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            width: 100%;
        }

        .header {
            text-align: center;
            margin-bottom: 60px;
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 800;
            color: #1e3a8a;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }

        .header h1 i {
            color: #3b82f6;
            font-size: 2.5rem;
        }

        .header p {
            font-size: 1.2rem;
            color: #64748b;
            font-weight: 500;
        }

        .main-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            padding: 20px;
        }

        .main-button {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px 30px;
            text-decoration: none;
            color: #1f2937;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
            min-height: 280px;
            justify-content: center;
        }

        .main-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #10b981);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .main-button:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
            border-color: #3b82f6;
        }

        .main-button:hover::before {
            transform: scaleX(1);
        }

        .button-icon {
            width: 100px;
            height: 100px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            color: white;
            margin-bottom: 25px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }

        .main-button:hover .button-icon {
            transform: scale(1.1) rotate(5deg);
        }

        .cartera .button-icon {
            background: linear-gradient(135deg, #10b981, #059669);
        }

        .anticipo .button-icon {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        }

        .modelo .button-icon {
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
        }

        .balance .button-icon {
            background: linear-gradient(135deg, #f59e0b, #d97706);
        }

        .button-content h3 {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 10px;
            transition: color 0.3s ease;
        }

        .button-content p {
            color: #6b7280;
            font-size: 1rem;
            font-weight: 500;
            line-height: 1.5;
            transition: color 0.3s ease;
        }

        .main-button:hover .button-content h3 {
            color: #3b82f6;
        }

        .main-button:hover .button-content p {
            color: #64748b;
        }

        /* Efectos de partículas */
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
                flex-direction: column;
                gap: 10px;
            }

            .header h1 i {
                font-size: 2rem;
            }

            .main-buttons {
                grid-template-columns: 1fr;
                gap: 20px;
            }

            .main-button {
                padding: 30px 20px;
                min-height: 250px;
            }

            .button-icon {
                width: 80px;
                height: 80px;
                font-size: 2rem;
            }
        }

        /* Animación de entrada */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .main-button {
            animation: fadeInUp 0.6s ease forwards;
        }

        .main-button:nth-child(1) { animation-delay: 0.1s; }
        .main-button:nth-child(2) { animation-delay: 0.2s; }
        .main-button:nth-child(3) { animation-delay: 0.3s; }
        .main-button:nth-child(4) { animation-delay: 0.4s; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>
                <i class="fas fa-chart-line"></i>
                <span>Procesador de Archivos</span>
            </h1>
            <p>Sistema de procesamiento de cartera y anticipos - Grupo Planeta</p>
        </div>

        <!-- Panel único con selector y acciones -->
        <div class="main-buttons" style="display:block;">
            <div class="main-button" style="max-width:900px;margin:0 auto;gap:20px;">
                <div class="button-icon" style="background:linear-gradient(135deg,#3b82f6,#8b5cf6);">
                    <i class="fas fa-sliders-h"></i>
                </div>
                <div class="button-content" style="width:100%;">
                    <h3 style="margin-bottom:12px;">Selecciona el proceso</h3>
                    <p style="margin-bottom:16px;">Según la opción, aparecen las acciones disponibles.</p>
                    <div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;">
                        <label for="procesoSelect" style="font-weight:600;color:#1f2937;">Proceso:</label>
                        <select id="procesoSelect" style="flex:1;min-width:220px;padding:10px 12px;border-radius:10px;border:1px solid #d1d5db;background:#fff;font-weight:600;">
                            <option value="cartera">Cartera (Provisión)</option>
                            <option value="anticipos">Anticipos</option>
                            <option value="modelo">Modelo Deuda</option>
                            <option value="balance">Balance</option>
                        </select>
                </div>

                    <!-- Acciones dinámicas -->
                    <div id="acciones" style="margin-top:18px;display:flex;flex-wrap:wrap;gap:12px;"></div>
                    <!-- TRM para Modelo Deuda -->
                    <div id="trmBox" class="trm-container" style="display:none;">
                        <div class="trm-header">
                            <h4 class="trm-title">
                                <i class="fas fa-exchange-alt"></i> Tasas de Cambio (TRM)
                            </h4>
                            <div class="trm-subtitle">Ingresa las tasas de cambio para las conversiones de moneda</div>
                        </div>
                        <div class="trm-fields">
                            <div class="trm-field">
                                <label class="trm-label">
                                    <i class="fas fa-dollar-sign"></i> Dólar (USD/COP)
                                </label>
                                <input id="trmUsd" type="number" step="0.01" min="0" placeholder="Ej: 4000" class="trm-input">
                            </div>
                            <div class="trm-field">
                                <label class="trm-label">
                                    <i class="fas fa-euro-sign"></i> Euro (EUR/COP)
                                </label>
                                <input id="trmEur" type="number" step="0.01" min="0" placeholder="Ej: 4700" class="trm-input">
                            </div>
                            <div class="trm-field">
                                <button id="btnGuardarTRM" type="button" class="trm-save-btn">
                                    <i class="fas fa-save"></i> Guardar TRM
                                </button>
                            </div>
                        </div>
                        <div id="trmStatus" class="trm-status info"></div>
                    </div>
                    <div id="resultado" style="margin-top:10px;width:100%;"></div>
                </div>
                </div>
        </div>
    </div>

    <script>
        // Efectos interactivos mejorados
        document.querySelectorAll('.main-button').forEach(button => {
            // Efecto de partículas al hacer hover
            button.addEventListener('mouseenter', function() {
                createParticles(this);
            });

            // Efecto de click
            button.addEventListener('click', function(e) {
                // Crear efecto de onda
                const ripple = document.createElement('div');
                ripple.style.position = 'absolute';
                ripple.style.borderRadius = '50%';
                ripple.style.background = 'rgba(59, 130, 246, 0.3)';
                ripple.style.transform = 'scale(0)';
                ripple.style.animation = 'ripple 0.6s linear';
                ripple.style.left = (e.clientX - this.offsetLeft) + 'px';
                ripple.style.top = (e.clientY - this.offsetTop) + 'px';
                ripple.style.width = ripple.style.height = '20px';
                ripple.style.pointerEvents = 'none';
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });

        // Función para crear partículas
        function createParticles(element) {
            const rect = element.getBoundingClientRect();
            const colors = ['#3b82f6', '#8b5cf6', '#10b981'];
            
            for (let i = 0; i < 8; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                
                const startX = rect.left + rect.width / 2;
                const startY = rect.top + rect.height / 2;
                
                particle.style.left = startX + 'px';
                particle.style.top = startY + 'px';
                
                document.body.appendChild(particle);
                
                const angle = (Math.PI * 2 * i) / 8;
                const velocity = 80 + Math.random() * 40;
                const endX = startX + Math.cos(angle) * velocity;
                const endY = startY + Math.sin(angle) * velocity;
                
                particle.animate([
                    { 
                        transform: 'translate(0, 0) scale(1)',
                        opacity: 1 
                    },
                    { 
                        transform: `translate(${endX - startX}px, ${endY - startY}px) scale(0)`,
                        opacity: 0 
                    }
                ], {
                    duration: 800,
                    easing: 'ease-out'
                }).onfinish = () => {
                    document.body.removeChild(particle);
                };
            }
        }

        // Agregar estilos para la animación de ripple
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);

        // Efecto de escritura para el título
        const title = document.querySelector('.header h1 span');
        if (title) {
            const text = title.textContent;
            title.textContent = '';
            title.style.borderRight = '3px solid #3b82f6';
            
            let i = 0;
            const typeWriter = () => {
                if (i < text.length) {
                    title.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, 80);
                } else {
                    setTimeout(() => {
                        title.style.borderRight = 'none';
                    }, 1000);
                }
            };
            
            setTimeout(typeWriter, 500);
        }

        // Acciones dinámicas por proceso
        const acciones = document.getElementById('acciones');
        const select = document.getElementById('procesoSelect');
        const trmBox = document.getElementById('trmBox');
        const trmUsd = document.getElementById('trmUsd');
        const trmEur = document.getElementById('trmEur');
        const resultado = document.getElementById('resultado');

        function btn(label, icon, action){
            return `
                <button data-action="${action}" class="main-button" style="min-height:auto;padding:14px 16px;gap:10px;cursor:pointer;">
                    <div class="button-icon" style="width:56px;height:56px;font-size:1.2rem;background:#3b82f6;">
                        <i class="${icon}"></i>
                    </div>
                    <div class="button-content"><h3 style="margin:0;">${label}</h3></div>
                </button>
            `;
        }

        const templates = {
            cartera: `
                <form id="formCartera" class="main-button" style="min-height:auto;padding:18px 20px;gap:12px;">
                    <div class="button-icon"><i class="fas fa-file-invoice-dollar"></i></div>
                    <div class="button-content" style="width:100%">
                        <h3 style="margin-bottom:8px;">Generar Cartera</h3>
                        <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;">
                            <input type="file" name="archivo" accept=".csv" required style="padding:8px 10px;border:1px solid #d1d5db;border-radius:8px;">
                            <select name="moneda" style="padding:8px 10px;border:1px solid #d1d5db;border-radius:8px;">
                                <option value="">Moneda (por defecto)</option>
                                <option value="PESOS COL">PESOS COL</option>
                                <option value="USD">USD</option>
                                <option value="EURO">EURO</option>
                            </select>
                            <button type="submit" class="main-button" style="min-height:auto;padding:10px 14px;background:#3b82f6;color:#fff;cursor:pointer;">
                                <div class="button-content"><h3 style="margin:0;">Generar</h3></div>
                            </button>
                        </div>
                    </div>
                </form>
            `,
            anticipos: btn('Generar Anticipos','fas fa-hand-holding-usd','anticipos'),
            modelo: `
                <form id="formModelo" class="main-button" style="min-height:auto;padding:18px 20px;gap:12px;">
                    <div class="button-icon"><i class="fas fa-calculator"></i></div>
                    <div class="button-content" style="width:100%">
                        <h3 style="margin-bottom:8px;">Generar Modelo Deuda</h3>
                        <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;">
                            <label style="font-weight:600;color:#1f2937;">Cartera:</label>
                            <input type="file" name="cartera" accept=".xlsx" style="padding:8px 10px;border:1px solid #d1d5db;border-radius:8px;">
                            <label style="font-weight:600;color:#1f2937;">Anticipos:</label>
                            <input type="file" name="anticipos" accept=".xlsx" style="padding:8px 10px;border:1px solid #d1d5db;border-radius:8px;">
                            <button type="submit" class="main-button" style="min-height:auto;padding:10px 14px;background:#3b82f6;color:#fff;cursor:pointer;">
                                <div class="button-content"><h3 style="margin:0;">Generar</h3></div>
                            </button>
                        </div>
                    </div>
                </form>
            `,
            balance: `<a href="balance.php" class="main-button balance" style="min-height:auto;padding:18px 20px;">
                        <div class=\"button-icon\"><i class=\"fas fa-balance-scale\"></i></div>
                        <div class=\"button-content\"><h3>Procesar Balance</h3><p>Análisis de cuentas</p></div>
                      </a>`
        };

        async function fetchTRM(){
            try{
                const res = await fetch('runner.php',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'accion=trm'});
                const json = await res.json();
                if(json.ok){
                    trmUsd.value = json.trm_usd ?? '';
                    trmEur.value = json.trm_eur ?? '';
                    updateTRMStatus();
                }
            }catch(err){
                console.error('Error cargando TRM:', err);
            }
        }

        async function guardarTRM(){
            const usd = trmUsd.value.trim();
            const eur = trmEur.value.trim();
            
            // Validación
            if (!usd && !eur) {
                showTRMStatus('Por favor ingresa al menos una tasa de cambio', 'error');
                return;
            }
            
            if (usd && (isNaN(parseFloat(usd)) || parseFloat(usd) <= 0)) {
                showTRMStatus('El TRM del Dólar debe ser un número válido mayor a 0', 'error');
                trmUsd.focus();
                return;
            }
            
            if (eur && (isNaN(parseFloat(eur)) || parseFloat(eur) <= 0)) {
                showTRMStatus('El TRM del Euro debe ser un número válido mayor a 0', 'error');
                trmEur.focus();
                return;
            }
            
            try {
                const params = new URLSearchParams();
                params.set('accion', 'guardar_trm');
                if (usd) params.set('trm_usd', usd);
                if (eur) params.set('trm_eur', eur);
                
                const res = await fetch('runner.php', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: params.toString()
                });
                
                const json = await res.json();
                if (json.ok) {
                    showTRMStatus('Tasas de cambio guardadas correctamente', 'success');
                    // Actualizar valores en los campos
                    trmUsd.value = json.trm_usd ?? usd;
                    trmEur.value = json.trm_eur ?? eur;
                } else {
                    showTRMStatus('Error al guardar: ' + (json.error || 'Error desconocido'), 'error');
                }
            } catch (err) {
                showTRMStatus('Error de conexión al guardar', 'error');
                console.error('Error guardando TRM:', err);
            }
        }

        function showTRMStatus(message, type = 'info') {
            const status = document.getElementById('trmStatus');
            status.className = `trm-status ${type}`;
            status.textContent = message;
            
            // Auto-limpiar mensajes de éxito después de 3 segundos
            if (type === 'success') {
                setTimeout(() => {
                    status.textContent = '';
                    status.className = 'trm-status info';
                }, 3000);
            }
        }

        function updateTRMStatus() {
            const usd = trmUsd.value.trim();
            const eur = trmEur.value.trim();
            
            if (usd && eur) {
                showTRMStatus(`TRM configurada: USD=${usd} | EUR=${eur}`, 'info');
            } else if (usd) {
                showTRMStatus(`TRM configurada: USD=${usd}`, 'info');
            } else if (eur) {
                showTRMStatus(`TRM configurada: EUR=${eur}`, 'info');
            } else {
                showTRMStatus('Ingresa las tasas de cambio para continuar', 'info');
            }
        }

        function renderAcciones() {
            const v = select.value;
            acciones.innerHTML = templates[v] || '';
            
            // Mostrar TRM para todos los procesos, no solo modelo
            trmBox.style.display = 'flex';
            
            // Cargar TRM y configurar event listeners para todos los procesos
            fetchTRM();
            setTimeout(() => {
                const btnGuardarTRM = document.getElementById('btnGuardarTRM');
                if (btnGuardarTRM) {
                    // Remover event listeners previos para evitar duplicados
                    btnGuardarTRM.removeEventListener('click', guardarTRM);
                    btnGuardarTRM.addEventListener('click', guardarTRM);
                }
                
                // Event listeners para validación en tiempo real
                trmUsd.removeEventListener('input', updateTRMStatus);
                trmEur.removeEventListener('input', updateTRMStatus);
                trmUsd.addEventListener('input', updateTRMStatus);
                trmEur.addEventListener('input', updateTRMStatus);
                
                // Efectos visuales en los campos
                [trmUsd, trmEur].forEach(input => {
                    input.removeEventListener('focus', function() {
                        this.style.borderColor = '#3b82f6';
                    });
                    input.removeEventListener('blur', function() {
                        this.style.borderColor = '#d1d5db';
                    });
                    input.addEventListener('focus', function() {
                        this.style.borderColor = '#3b82f6';
                    });
                    input.addEventListener('blur', function() {
                        this.style.borderColor = '#d1d5db';
                    });
                });
            }, 100);
        }
        if (acciones && select) {
            renderAcciones();
            select.addEventListener('change', renderAcciones);
            acciones.addEventListener('click', async (e)=>{
                const b = e.target.closest('button[data-action]');
                if(!b) return;
                const accion = b.getAttribute('data-action');
                resultado.innerHTML = '<span style="color:#1f2937;">Procesando...</span>';
                try{
                    const params = new URLSearchParams();
                    params.set('accion', accion);
                    // Enviar TRM para todos los procesos, no solo modelo
                    if (trmUsd.value) params.set('trm_usd', trmUsd.value);
                    if (trmEur.value) params.set('trm_eur', trmEur.value);
                    const res = await fetch('runner.php',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:params.toString()});
                    const json = await res.json();
                    if(json.ok){
                        const trm = (json.trm_usd||json.trm_eur) ? ` <span style='color:#111827;font-weight:600;'>TRM USD=${json.trm_usd ?? '-'} | EUR=${json.trm_eur ?? '-'}</span>` : '';
                        resultado.innerHTML = `<div style="display:flex;flex-direction:column;gap:8px;"><a class="main-button" style="min-height:auto;padding:12px 16px;background:#10b981;color:#fff;" href="${json.url}" target="_blank"><div class=\"button-content\"><h3 style=\"margin:0;\"><i class=\"fas fa-download\"></i> Descargar ${json.file}</h3></div></a><div>${trm}</div></div>`;
                    }else{
                        resultado.innerHTML = `<div style="color:#b91c1c;font-weight:700;">${json.error}</div>`;
                    }
                }catch(err){
                    resultado.innerHTML = `<div style="color:#b91c1c;font-weight:700;">Error de conexión</div>`;
                }
            });
            // submit cartera (con archivo y moneda)
            acciones.addEventListener('submit', async (e)=>{
                const form = e.target.closest('#formCartera');
                if(!form) return;
                e.preventDefault();
                const fd = new FormData(form);
                fd.set('accion','cartera');
                resultado.innerHTML = '<span style="color:#1f2937;">Procesando...</span>';
                try{
                    const res = await fetch('runner.php',{method:'POST',body:fd});
                    const json = await res.json();
                    if(json.ok){
                        const trm = (json.trm_usd||json.trm_eur) ? ` <span style='color:#111827;font-weight:600;'>TRM USD=${json.trm_usd ?? '-'} | EUR=${json.trm_eur ?? '-'}</span>` : '';
                        resultado.innerHTML = `<div style="display:flex;flex-direction:column;gap:8px;"><a class="main-button" style="min-height:auto;padding:12px 16px;background:#10b981;color:#fff;" href="${json.url}" target="_blank"><div class=\"button-content\"><h3 style=\"margin:0;\"><i class=\"fas fa-download\"></i> Descargar ${json.file}</h3></div></a><div>${trm}</div></div>`;
                    }else{
                        resultado.innerHTML = `<div style="color:#b91c1c;font-weight:700;">${json.error}</div>`;
                    }
                }catch(err){
                    resultado.innerHTML = `<div style="color:#b91c1c;font-weight:700;">Error de conexión</div>`;
                }
            });
        }
    </script>
</body>
</html> 