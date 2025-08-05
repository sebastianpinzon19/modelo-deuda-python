<?php
header('Content-Type: text/html; charset=utf-8');

// Configuración de errores
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Función para limpiar y validar entrada
function limpiar_entrada($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

// Función para generar respuesta JSON
function responder_json($success, $message, $data = null) {
    $response = [
        'success' => $success,
        'message' => $message
    ];
    
    if ($data !== null) {
        $response['data'] = $data;
    }
    
    echo json_encode($response, JSON_UNESCAPED_UNICODE);
    exit;
}

// Verificar método de petición
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    responder_json(false, 'Método no permitido');
}

// Verificar si se subió un archivo
if (!isset($_FILES['archivo']) || $_FILES['archivo']['error'] !== UPLOAD_ERR_OK) {
    $error_msg = 'No se pudo subir el archivo';
    if (isset($_FILES['archivo']['error'])) {
        switch ($_FILES['archivo']['error']) {
            case UPLOAD_ERR_INI_SIZE:
                $error_msg = 'El archivo excede el tamaño máximo permitido por el servidor';
                break;
            case UPLOAD_ERR_FORM_SIZE:
                $error_msg = 'El archivo excede el tamaño máximo permitido por el formulario';
                break;
            case UPLOAD_ERR_PARTIAL:
                $error_msg = 'El archivo se subió parcialmente';
                break;
            case UPLOAD_ERR_NO_FILE:
                $error_msg = 'No se seleccionó ningún archivo';
                break;
        }
    }
    responder_json(false, $error_msg);
}

// Obtener tipo de procesamiento
$tipo = isset($_POST['tipo']) ? limpiar_entrada($_POST['tipo']) : '';
if (!in_array($tipo, ['cartera', 'anticipo'])) {
    responder_json(false, 'Tipo de procesamiento no válido');
}

// Obtener fecha de cierre si es cartera
$fecha_cierre = null;
if ($tipo === 'cartera' && isset($_POST['fecha_cierre'])) {
    $fecha_cierre = limpiar_entrada($_POST['fecha_cierre']);
    if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $fecha_cierre)) {
        responder_json(false, 'Formato de fecha de cierre no válido. Use YYYY-MM-DD');
    }
}

// Configurar directorios
$upload_dir = __DIR__ . '/PROVCA/';
$output_dir = __DIR__ . '/PROVCA_PROCESADOS/';

// Crear directorios si no existen
if (!is_dir($upload_dir)) {
    mkdir($upload_dir, 0755, true);
}
if (!is_dir($output_dir)) {
    mkdir($output_dir, 0755, true);
}

// Procesar archivo subido
$archivo = $_FILES['archivo'];
$nombre_original = $archivo['name'];
$tipo_archivo = $archivo['type'];
$tamanio = $archivo['size'];
$tmp_name = $archivo['tmp_name'];

// Validar extensión según tipo
$extension = strtolower(pathinfo($nombre_original, PATHINFO_EXTENSION));
if ($tipo === 'cartera' && $extension !== 'csv') {
    responder_json(false, 'Para cartera solo se permiten archivos CSV');
}
if ($tipo === 'anticipo' && !in_array($extension, ['xlsx', 'xls', 'csv'])) {
    responder_json(false, 'Para anticipos se permiten archivos XLSX, XLS o CSV');
}

// Validar tamaño (máximo 10MB)
if ($tamanio > 10 * 1024 * 1024) {
    responder_json(false, 'El archivo es demasiado grande. Máximo 10MB');
}

// Generar nombre único para el archivo
$timestamp = date('Y-m-d_H-i-s');
$nombre_archivo = $tipo . '_' . $timestamp . '.' . $extension;
$ruta_archivo = $upload_dir . $nombre_archivo;

// Mover archivo subido
if (!move_uploaded_file($tmp_name, $ruta_archivo)) {
    responder_json(false, 'No se pudo guardar el archivo en el servidor');
}

// Configurar ruta de Python
$python_path = "C:\\Users\\USPRBA\\AppData\\Local\\Programs\\Python\\Python313\\python.exe";

// Verificar que Python existe
if (!file_exists($python_path)) {
    unlink($ruta_archivo); // Eliminar archivo subido
    responder_json(false, "No se encontró Python en la ruta: $python_path");
}

// Ejecutar script de Python correspondiente
$python_script = '';
$comando = '';

if ($tipo === 'cartera') {
    $python_script = 'PROVCA/procesador_cartera.py';
    $comando = "\"$python_path\" \"$python_script\" \"$ruta_archivo\"";
    if ($fecha_cierre) {
        $comando .= " \"$fecha_cierre\"";
    }
} else { // anticipo
    $python_script = 'PROVCA/procesador_anticipos.py';
    $comando = "\"$python_path\" \"$python_script\" \"$ruta_archivo\"";
}

// Verificar que existe el script de Python
if (!file_exists($python_script)) {
    unlink($ruta_archivo); // Eliminar archivo subido
    responder_json(false, "No se encontró el script de procesamiento: $python_script");
}

// Ejecutar comando
$output = [];
$return_var = 0;

// Cambiar al directorio del proyecto
chdir(__DIR__);

// Ejecutar comando y capturar salida
$comando_completo = $comando . " 2>&1";
exec($comando_completo, $output, $return_var);

// Log para debugging
error_log("Comando ejecutado: $comando_completo");
error_log("Código de retorno: $return_var");
error_log("Salida: " . implode("\n", $output));

// Verificar si el procesamiento fue exitoso
if ($return_var !== 0) {
    $error_output = implode("\n", $output);
    unlink($ruta_archivo); // Eliminar archivo subido
    responder_json(false, "Error durante el procesamiento. Código: $return_var. Salida: $error_output");
}

// Buscar archivo de salida generado
$archivos_salida = glob($output_dir . $tipo . '*_PROCESAD*' . $timestamp . '*.xlsx');
if (empty($archivos_salida)) {
    // Buscar archivos más recientes si no encuentra por timestamp exacto
    $archivos_salida = glob($output_dir . $tipo . '*_PROCESAD*.xlsx');
    // Ordenar por fecha de modificación (más reciente primero)
    usort($archivos_salida, function($a, $b) {
        return filemtime($b) - filemtime($a);
    });
}

if (empty($archivos_salida)) {
    unlink($ruta_archivo); // Eliminar archivo subido
    responder_json(false, 'No se pudo encontrar el archivo de salida generado');
}

$archivo_salida = $archivos_salida[0];
$nombre_archivo_salida = basename($archivo_salida);

// Verificar que el archivo de salida existe y no está vacío
if (!file_exists($archivo_salida) || filesize($archivo_salida) === 0) {
    unlink($ruta_archivo); // Eliminar archivo subido
    responder_json(false, 'El archivo de salida está vacío o no se pudo crear');
}

// Limpiar archivo de entrada
unlink($ruta_archivo);

// Preparar respuesta exitosa
$tipo_titulo = $tipo === 'cartera' ? 'Cartera' : 'Anticipos';
$mensaje_exito = "El archivo de $tipo_titulo se ha procesado correctamente.";

// Crear enlace de descarga
$url_descarga = "descargar.php?file=" . urlencode($archivo_salida);

// Respuesta HTML para el frontend
$html_response = "
<div class='resultado-procesamiento'>
    <div class='resultado-header'>
        <i class='fas fa-check-circle'></i>
        <h3>Procesamiento Completado</h3>
    </div>
    <div class='resultado-body'>
        <p>$mensaje_exito</p>
        <div class='archivo-info'>
            <strong>Archivo generado:</strong> $nombre_archivo_salida
        </div>
    </div>
    <div class='resultado-actions'>
        <a href='$url_descarga' class='btn-descarga' target='_blank'>
            <i class='fas fa-download'></i>
            Descargar Archivo
        </a>
    </div>
</div>";

echo $html_response;
?> 