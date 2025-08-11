<?php
// index.php - Dashboard principal del sistema de cartera
require_once __DIR__ . '/front_php/configuracion.php';
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Sistema Cartera - Grupo Planeta</title>
    <link rel="stylesheet" href="front_php/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            background: var(--primary-gradient);
            min-height: 100vh;
            font-family: 'Montserrat', Arial, sans-serif;
        }
        .dashboard-container {
            max-width: 1100px;
            margin: 40px auto;
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 8px 32px #0003;
            padding: 40px 36px 32px 36px;
            border: 1.5px solid var(--primary-light);
        }
        .dashboard-header {
            display: flex;
            align-items: center;
            gap: 24px;
            margin-bottom: 36px;
        }
        .dashboard-header img {
            height: 60px;
            border-radius: 12px;
            box-shadow: 0 2px 8px #0001;
        }
        .dashboard-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary-color);
            letter-spacing: 1px;
            text-shadow: 0 2px 8px #3b82f633;
        }
        .section {
            margin-bottom: 38px;
            background: #f8fafc;
            border-radius: 12px;
            box-shadow: 0 2px 8px #0001;
            padding: 28px 24px 18px 24px;
        }
        .section-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--primary-dark);
            margin-bottom: 18px;
            letter-spacing: 0.5px;
        }
        .logs, .resultados, .estadisticas {
            background: var(--info-light);
            border-radius: 8px;
            padding: 18px 14px;
            min-height: 60px;
            font-size: 1.05rem;
            color: var(--text-primary);
            margin-top: 10px;
        }
        .btn {
            background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 12px 28px;
            font-size: 1.08rem;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
            box-shadow: 0 2px 8px #1e3a8a22;
        }
        .btn:hover {
            background: var(--primary-dark);
            color: #fff;
            transform: translateY(-2px) scale(1.03);
            box-shadow: 0 4px 16px #1e3a8a33;
        }
        .flex {
            display: flex;
            gap: 32px;
        }
        .w-50 {
            width: 50%;
        }
        .mt-2 {
            margin-top: 16px;
        }
        label {
            font-weight: 600;
            color: var(--primary-dark);
            margin-bottom: 6px;
            display: block;
        }
        input[type="file"], select {
            width: 100%;
            padding: 8px 10px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            background: #f1f5f9;
            font-size: 1rem;
            margin-top: 4px;
        }
        @media (max-width: 900px) {
            .dashboard-container { padding: 18px 4vw; }
            .flex { flex-direction: column; gap: 12px; }
            .w-50 { width: 100%; }
        }
    </style>
</head>
<body>
<div class="dashboard-container">
    <div class="dashboard-header">
        <img src="front_php/Logo grupo planeta color transparente.jpg" alt="Logo Grupo Planeta">
        <span class="dashboard-title">Dashboard Sistema Cartera</span>
    </div>

    <!-- Sección: Procesamiento de Archivos -->
    <div class="section">
        <div class="section-title">Procesar Archivo</div>
        <form id="form-procesar" enctype="multipart/form-data">
            <div class="flex">
                <div class="w-50">
                    <label>Archivo a procesar:</label>
                    <input type="file" name="archivo" required class="mt-2">
                </div>
                <div class="w-50">
                    <label>Tipo de procesamiento:</label>
                    <select name="tipo_procesamiento" id="tipo_procesamiento" required class="mt-2" onchange="mostrarOpcionesTipo()">
                        <option value="cartera">Cartera</option>
                        <option value="acumulado">Acumulado</option>
                        <option value="formato_deuda">Formato Deuda</option>
                        <option value="anticipos">Anticipos</option>
                        <option value="balance_completo">Balance Completo</option>
                        <option value="balance_especifico">Balance Específico</option>
                        <option value="focus_especifico">Focus Específico</option>
                    </select>
                </div>
            </div>
            <!-- Opciones adicionales dinámicas -->
            <div id="opciones-adicionales" class="mt-2"></div>
            <button type="submit" class="btn mt-2">Procesar</button>
        </form>
        <div id="procesar-resultado" class="logs mt-2"></div>
    </div>
</div>
<script>
function mostrarOpcionesTipo() {
    const tipo = document.getElementById('tipo_procesamiento').value;
    const cont = document.getElementById('opciones-adicionales');
    let html = '';
    if (tipo === 'formato_deuda') {
        html += `<div class='campo-adicional'><label>TRM Dólar:</label><input type="number" name="trm_dolar" step="0.01" class="mt-2" required></div>`;
        html += `<div class='campo-adicional'><label>TRM Euro:</label><input type="number" name="trm_euro" step="0.01" class="mt-2" required></div>`;
    } else if (tipo === 'balance_especifico' || tipo === 'focus_especifico') {
        html += `<div class='campo-adicional'><label>Mes:</label><input type="month" name="mes" class="mt-2" required></div>`;
        html += `<div class='campo-adicional'><label>División:</label><input type="text" name="division" class="mt-2" required></div>`;
    } else if (tipo === 'cartera') {
        html += `<div class='campo-adicional'><label>Fecha de corte:</label><input type="date" name="fecha_corte" class="mt-2" required></div>`;
    } else if (tipo === 'balance_completo') {
        html += `<div class='campo-adicional'><label>Mes:</label><input type="month" name="mes" class="mt-2" required></div>`;
    }
    cont.innerHTML = html;
}
window.onload = mostrarOpcionesTipo;
</script>
</body>
</html>


