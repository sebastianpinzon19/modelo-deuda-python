<?php
header('Content-Type: text/html; charset=utf-8');
error_reporting(E_ALL);
ini_set('display_errors', 1);

function limpiar_entrada($data) {
    return htmlspecialchars(stripslashes(trim($data)));
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    exit('Método no permitido');
}

if (!isset($_FILES['archivo']) || $_FILES['archivo']['error'] !== UPLOAD_ERR_OK) {
    exit('No se pudo subir el archivo');
}

$tipo = limpiar_entrada($_POST['tipo'] ?? '');
if ($tipo !== 'cartera') {
    exit('Tipo no válido');
}

$fecha_cierre = limpiar_entrada($_POST['fecha_cierre'] ?? '');
if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $fecha_cierre)) {
    exit('Formato de fecha no válido');
}

// Configuración de rutas
$base_dir       = "C:\\wamp64\\www\\modelo-deuda-python\\cartera_v2.0.0";
$upload_dir     = $base_dir . "\\PROVCA";
$output_dir     = $base_dir . "\\PROVCA_PROCESADOS";
$python_path    = "C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe";
$python_script  = $base_dir . "\\PROVCA\\procesador_cartera.py";

if (!is_dir($upload_dir)) mkdir($upload_dir, 0755, true);
if (!is_dir($output_dir)) mkdir($output_dir, 0755, true);

$extension = strtolower(pathinfo($_FILES['archivo']['name'], PATHINFO_EXTENSION));
if ($extension !== 'csv') {
    exit('Solo se permiten archivos CSV');
}

$timestamp = date('Y-m-d_H-i-s');
$nombre_archivo = $tipo . '_' . $timestamp . '.' . $extension;
$ruta_csv = $upload_dir . "\\" . $nombre_archivo;

if (!move_uploaded_file($_FILES['archivo']['tmp_name'], $ruta_csv)) {
    exit('Error al guardar el archivo subido');
}

if (!file_exists($python_script)) {
    exit("No se encontró el script de Python: $python_script");
}

// Ejecutar Python
$comando = "\"$python_path\" \"$python_script\" \"$ruta_csv\" \"$fecha_cierre\"";
exec($comando . " 2>&1", $output, $return_var);

if ($return_var !== 0) {
    echo "<pre>Error al procesar:\n" . implode("\n", $output) . "</pre>";
    exit;
}

// El nombre exacto del archivo generado lo devuelve Python en la última línea
$archivo_generado = trim(end($output));
$ruta_salida = $output_dir . "\\" . $archivo_generado;

if (!file_exists($ruta_salida)) {
    exit("No se encontró el archivo generado: $archivo_generado");
}

$url_descarga = "PROVCA_PROCESADOS/" . $archivo_generado;
echo "<a href='$url_descarga' class='btn-descarga' target='_blank'>
        <i class='fas fa-download'></i> Descargar Archivo
      </a>";
?>
