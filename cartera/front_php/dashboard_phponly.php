<?php
// Procesamiento de archivos desde el dashboard principal (solo PHP, sin JS)
$resultado = '';
$log = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $tipo = $_POST['tipo_procesamiento'] ?? '';
    $archivo = $_FILES['archivo'] ?? null;
    $args = [];
    if ($tipo === 'formato_deuda') {
        $args['trm_dolar'] = $_POST['trm_dolar'] ?? '';
        $args['trm_euro'] = $_POST['trm_euro'] ?? '';
    } elseif ($tipo === 'balance_especifico' || $tipo === 'focus_especifico') {
        $args['mes'] = $_POST['mes'] ?? '';
        $args['division'] = $_POST['division'] ?? '';
    } elseif ($tipo === 'cartera') {
        $args['fecha_corte'] = $_POST['fecha_corte'] ?? '';
    } elseif ($tipo === 'balance_completo') {
        $args['mes'] = $_POST['mes'] ?? '';
    }
    if ($archivo && $archivo['error'] === UPLOAD_ERR_OK) {
        // Llama al backend PHP de procesamiento y muestra el resultado
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'front_php/procesar.php');
        curl_setopt($ch, CURLOPT_POST, 1);
        $postfields = [
            'archivo' => new CURLFile($archivo['tmp_name'], $archivo['type'], $archivo['name']),
            'tipo_procesamiento' => $tipo
        ];
        foreach ($args as $k => $v) {
            $postfields[$k] = $v;
        }
        curl_setopt($ch, CURLOPT_POSTFIELDS, $postfields);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        $response = curl_exec($ch);
        $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($response === false) {
            $resultado = 'Error al conectar con el backend: ' . curl_error($ch);
        } else {
            $json = json_decode($response, true);
            if ($json && isset($json['success'])) {
                $resultado = $json['message'];
                if (!$json['success'] && isset($json['data']['error'])) {
                    $log = $json['data']['error'];
                }
                if (isset($json['data']['url_descarga'])) {
                    $resultado .= '<br><a href="' . $json['data']['url_descarga'] . '" target="_blank">Descargar resultado</a>';
                }
            } else {
                $resultado = 'Respuesta inesperada del backend: ' . htmlspecialchars($response);
            }
        }
        curl_close($ch);
    } else {
        $resultado = 'Debe seleccionar un archivo válido.';
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Procesador Cartera (PHP Only)</title>
    <link rel="stylesheet" href="front_php/styles.css">
</head>
<body>
<div class="dashboard-container">
    <h2>Procesar Archivo (PHP Only)</h2>
    <form method="post" enctype="multipart/form-data">
        <label>Archivo a procesar:</label>
        <input type="file" name="archivo" required><br><br>
        <label>Tipo de procesamiento:</label>
        <select name="tipo_procesamiento" id="tipo_procesamiento" required onchange="this.form.submit()">
            <option value="cartera">Cartera</option>
            <option value="acumulado">Acumulado</option>
            <option value="formato_deuda">Formato Deuda</option>
            <option value="anticipos">Anticipos</option>
            <option value="balance_completo">Balance Completo</option>
            <option value="balance_especifico">Balance Específico</option>
            <option value="focus_especifico">Focus Específico</option>
        </select><br><br>
        <div id="opciones-adicionales"></div>
        <button type="submit">Procesar</button>
    </form>
    <?php if ($resultado): ?>
        <div class="logs mt-2"><strong>Resultado:</strong> <?= $resultado ?></div>
    <?php endif; ?>
    <?php if ($log): ?>
        <div class="logs mt-2" style="color:red;"><strong>Log/Salida:</strong><br><pre><?= htmlspecialchars($log) ?></pre></div>
    <?php endif; ?>
</div>
</body>
</html>
