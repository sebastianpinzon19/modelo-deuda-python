<?php
header('Content-Type: application/json; charset=utf-8');
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/python_config.php';

function json_exit($arr) {
	echo json_encode($arr, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
	exit;
}

$accion = $_POST['accion'] ?? '';
$accion = strtolower(trim($accion));
if ($accion === '') {
	json_exit(['ok' => false, 'error' => 'Falta parámetro accion']);
}

$base_dir   = realpath(__DIR__ . '/../');
$out_dir    = $base_dir . DIRECTORY_SEPARATOR . 'PROVCA_PROCESADOS';
$provca_dir = $base_dir . DIRECTORY_SEPARATOR . 'PROVCA';

if (!is_dir($out_dir)) { @mkdir($out_dir, 0755, true); }

$python = isset($python_path) && $python_path ? $python_path : 'python';

// Cargar TRM guardada (para reportar al front y usar en modelo)
$cfg_file = $provca_dir . DIRECTORY_SEPARATOR . 'trm_config.json';
$usd_cfg = 4000; $eur_cfg = 4500;
if (file_exists($cfg_file)) {
	$data = json_decode(@file_get_contents($cfg_file), true);
	if (isset($data['usd']) && is_numeric($data['usd'])) { $usd_cfg = (float)$data['usd']; }
	if (isset($data['eur']) && is_numeric($data['eur'])) { $eur_cfg = (float)$data['eur']; }
}

function latest_file($dir, $pattern, $exclude = null) {
	$files = glob($dir . DIRECTORY_SEPARATOR . $pattern);
	if (!$files) { return null; }
	usort($files, function($a, $b) { return filemtime($b) <=> filemtime($a); });
	if ($exclude) {
		$files = array_values(array_filter($files, function($f) use ($exclude) {
			return stripos(basename($f), $exclude) === false;
		}));
	}
	return $files ? $files[0] : null;
}

			try {
	// Función para procesar TRM desde POST
	function procesar_trm_post() {
		global $usd_cfg, $eur_cfg, $cfg_file;
		$usd = $usd_cfg; $eur = $eur_cfg;
		// Permitir override desde el front y persistir
		if (isset($_POST['trm_usd']) && is_numeric($_POST['trm_usd'])) { $usd = (float)$_POST['trm_usd']; }
		if (isset($_POST['trm_eur']) && is_numeric($_POST['trm_eur'])) { $eur = (float)$_POST['trm_eur']; }
		// Guardar automáticamente si hay cambios
		if ($usd !== $usd_cfg || $eur !== $eur_cfg) {
			@file_put_contents($cfg_file, json_encode(['usd'=>$usd, 'eur'=>$eur, 'updated_at'=>date('Y-m-d H:i:s')], JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT));
		}
		return [$usd, $eur];
	}

	switch ($accion) {
		case 'trm': {
			json_exit(['ok' => true, 'trm_usd' => $usd_cfg, 'trm_eur' => $eur_cfg]);
		}
		case 'guardar_trm': {
			list($usd, $eur) = procesar_trm_post();
			json_exit(['ok' => true, 'trm_usd' => $usd, 'trm_eur' => $eur, 'message' => 'TRM guardada correctamente']);
		}
		case 'cartera': {
			// Procesar TRM si se envían
			list($usd, $eur) = procesar_trm_post();
			
			$csv = $provca_dir . DIRECTORY_SEPARATOR . 'PROVCA.CSV';
			$script = $provca_dir . DIRECTORY_SEPARATOR . 'procesador_cartera.py';
			// Permitir subir un CSV desde el front
			if (isset($_FILES['archivo']) && $_FILES['archivo']['error'] === UPLOAD_ERR_OK) {
				$dest = $provca_dir . DIRECTORY_SEPARATOR . basename($_FILES['archivo']['name']);
				@move_uploaded_file($_FILES['archivo']['tmp_name'], $dest);
				$csv = $dest;
			}
			if (!file_exists($csv)) json_exit(['ok' => false, 'error' => 'No existe PROVCA.CSV']);
			if (!file_exists($script)) json_exit(['ok' => false, 'error' => 'No existe procesador_cartera.py']);
			$moneda = isset($_POST['moneda']) ? trim($_POST['moneda']) : '';
			$cmd = '"' . $python . '" ' . '"' . $script . '" ' . '"' . $csv . '"';
			if ($moneda !== '') { $cmd .= ' None False 0 0 ' . escapeshellarg($moneda); }
			exec($cmd . ' 2>&1', $out, $code);
			if ($code !== 0) json_exit(['ok' => false, 'error' => 'Error ejecutando cartera', 'log' => $out]);
			$file = latest_file($out_dir, '*_PROCESADO_*.xlsx', 'ANTICIPO');
			if (!$file) json_exit(['ok' => false, 'error' => 'No se encontró salida de cartera']);
			json_exit(['ok' => true, 'file' => basename($file), 'url' => 'PROVCA_PROCESADOS/' . basename($file), 'trm_usd' => $usd, 'trm_eur' => $eur]);
		}
		case 'anticipos': {
			// Procesar TRM si se envían
			list($usd, $eur) = procesar_trm_post();
			
			$csv = $provca_dir . DIRECTORY_SEPARATOR . 'ANTICI.CSV';
			$script = $provca_dir . DIRECTORY_SEPARATOR . 'procesador_anticipos.py';
			if (!file_exists($csv)) json_exit(['ok' => false, 'error' => 'No existe ANTICI.CSV']);
			if (!file_exists($script)) json_exit(['ok' => false, 'error' => 'No existe procesador_anticipos.py']);
			$cmd = '"' . $python . '" ' . '"' . $script . '" ' . '"' . $csv . '"';
			exec($cmd . ' 2>&1', $out, $code);
			if ($code !== 0) json_exit(['ok' => false, 'error' => 'Error ejecutando anticipos', 'log' => $out]);
			$file = latest_file($out_dir, 'ANTICIPO_PROCESADO_*.xlsx');
			if (!$file) json_exit(['ok' => false, 'error' => 'No se encontró salida de anticipos']);
			json_exit(['ok' => true, 'file' => basename($file), 'url' => 'PROVCA_PROCESADOS/' . basename($file), 'trm_usd' => $usd, 'trm_eur' => $eur]);
		}
		case 'modelo': {
			// Procesar TRM si se envían
			list($usd, $eur) = procesar_trm_post();
			
			$cartera = latest_file($out_dir, '*_PROCESADO_*.xlsx', 'ANTICIPO');
			$anticipo = latest_file($out_dir, 'ANTICIPO_PROCESADO_*.xlsx');
			// Si llegan archivos subidos, usarlos en su lugar
			if (isset($_FILES['cartera']) && $_FILES['cartera']['error'] === UPLOAD_ERR_OK) {
				$dest = $out_dir . DIRECTORY_SEPARATOR . basename($_FILES['cartera']['name']);
				@move_uploaded_file($_FILES['cartera']['tmp_name'], $dest);
				$cartera = $dest;
			}
			if (isset($_FILES['anticipos']) && $_FILES['anticipos']['error'] === UPLOAD_ERR_OK) {
				$dest2 = $out_dir . DIRECTORY_SEPARATOR . basename($_FILES['anticipos']['name']);
				@move_uploaded_file($_FILES['anticipos']['tmp_name'], $dest2);
				$anticipo = $dest2;
			}
			if (!$cartera || !$anticipo) json_exit(['ok' => false, 'error' => 'Falta cartera o anticipos procesados']);
			$script = $provca_dir . DIRECTORY_SEPARATOR . 'modelo_deuda.py';
			if (!file_exists($script)) json_exit(['ok' => false, 'error' => 'No existe modelo_deuda.py']);
			$cmd = '"' . $python . '" ' . '"' . $script . '" ' . '"' . $cartera . '" ' . '"' . $anticipo . '" ' . $usd . ' ' . $eur;
			exec($cmd . ' 2>&1', $out, $code);
			if ($code !== 0) json_exit(['ok' => false, 'error' => 'Error ejecutando modelo', 'log' => $out]);
			$file = latest_file($out_dir, '1_Modelo_Deuda_*.xlsx');
			if (!$file) json_exit(['ok' => false, 'error' => 'No se encontró salida de modelo']);
			json_exit(['ok' => true, 'file' => basename($file), 'url' => 'PROVCA_PROCESADOS/' . basename($file), 'trm_usd' => $usd, 'trm_eur' => $eur]);
		}
		default:
			json_exit(['ok' => false, 'error' => 'Acción no soportada']);
	}
} catch (Throwable $e) {
	json_exit(['ok' => false, 'error' => $e->getMessage()]);
}

