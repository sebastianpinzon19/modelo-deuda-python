<?php
// index.php - Frontend Grupo Planeta conectado a backend Python
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Grupo Planeta - Procesador Cartera</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header -->
    <header>
        <div class="logo-container">
            <img src="assets/img/logo.jpg" alt="Grupo Planeta Logo" class="logo">
            <h1>Procesador de Cartera</h1>
        </div>
        <div class="trm-container">
            <span id="trm-display">TRM: Cargando...</span>
            <button class="btn" onclick="abrirTrmModal()">Actualizar TRM</button>
        </div>
    </header>

    <!-- Modal TRM -->
    <div id="trm-modal" class="modal">
        <div class="modal-content">
            <h2>Actualizar TRM</h2>
            <label>Dólar (USD):</label>
            <input type="number" step="0.01" id="trm-usd">
            <label>Euro (EUR):</label>
            <input type="number" step="0.01" id="trm-eur">
            <div class="modal-actions">
                <button class="btn" onclick="guardarTrm()">Guardar</button>
                <button class="btn btn-sec" onclick="cerrarTrmModal()">Cancelar</button>
            </div>
        </div>
    </div>

    <!-- Main -->
    <main>
        <h2>Seleccione un proceso</h2>
        <select id="proceso-select" onchange="mostrarFormulario()">
            <option value="">-- Seleccione --</option>
            <option value="modelo_deuda">Modelo de Deuda</option>
            <option value="anticipos">Procesar Anticipos</option>
            <option value="cartera">Procesar Cartera</option>
            <option value="unificado">Procesador Unificado</option>
        </select>

        <!-- Formularios dinámicos -->
        <div id="formularios"></div>
    </main>

    <!-- Footer -->
    <footer>
        <p>© <?php echo date("Y"); ?> Grupo Planeta</p>
    </footer>

    <script src="assets/js/app.js"></script>
</body>
</html>
<?php
// index.php - Frontend Grupo Planeta conectado a backend Python
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Grupo Planeta - Procesador de Cartera</title>
    <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
    <!-- Header -->
    <header>
        <div class="logo-container">
            <img src="assets/img/logo.jpg" alt="Logo Grupo Planeta" class="logo">
            <h1>Procesador de Cartera</h1>
        </div>
        <div class="trm-container">
            <span id="trm-display">TRM: Cargando...</span>
            <button class="btn" type="button" onclick="abrirTrmModal()">Actualizar TRM</button>
        </div>
    </header>

    <!-- Modal TRM -->
    <div id="trm-modal" class="modal">
        <div class="modal-content">
            <h2>Actualizar TRM</h2>
            <label for="trm-usd">Dólar (USD):</label>
            <input type="number" step="0.01" id="trm-usd" required>
            
            <label for="trm-eur">Euro (EUR):</label>
            <input type="number" step="0.01" id="trm-eur" required>

            <div class="modal-actions">
                <button class="btn" type="button" onclick="guardarTrm()">Guardar</button>
                <button class="btn btn-sec" type="button" onclick="cerrarTrmModal()">Cancelar</button>
            </div>
        </div>
    </div>

    <!-- Main -->
    <main>
        <h2>Seleccione un proceso</h2>
        <select id="proceso-select" onchange="mostrarFormulario()" required>
            <option value="">-- Seleccione --</option>
            <option value="modelo_deuda">Modelo de Deuda</option>
            <option value="anticipos">Procesar Anticipos</option>
            <option value="cartera">Procesar Cartera</option>
            <option value="unificado">Procesador Unificado</option>
        </select>

        <!-- Formularios dinámicos (inyectados desde JS) -->
        <div id="formularios"></div>
        
        <!-- Aquí se mostrará el link de descarga -->
        <div id="resultado" class="resultado"></div>
    </main>

    <!-- Footer -->
    <footer>
        <p>© <?= date("Y"); ?> Grupo Planeta</p>
    </footer>

    <script src="assets/js/app.js"></script>
</body>
</html>
