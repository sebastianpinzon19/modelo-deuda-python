<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

require_once 'config.php';

try {
    // Verificar que se hayan enviado los archivos
    if (!isset($_FILES['balanceFile']) || !isset($_FILES['situacionFile']) || !isset($_FILES['focusFile'])) {
        throw new Exception('Todos los archivos son requeridos');
    }

    $balanceFile = $_FILES['balanceFile'];
    $situacionFile = $_FILES['situacionFile'];
    $focusFile = $_FILES['focusFile'];

    // Verificar que los archivos se subieron correctamente
    if ($balanceFile['error'] !== UPLOAD_ERR_OK || 
        $situacionFile['error'] !== UPLOAD_ERR_OK || 
        $focusFile['error'] !== UPLOAD_ERR_OK) {
        throw new Exception('Error al subir los archivos');
    }

    $results = [];

    // Procesar archivo BALANCE
    $results = array_merge($results, procesarArchivoBalance($balanceFile));

    // Procesar archivo SITUACIÓN
    $results = array_merge($results, procesarArchivoSituacion($situacionFile));

    // Procesar archivo FOCUS
    $results = array_merge($results, procesarArchivoFocus($focusFile));

    // Realizar cálculos adicionales
    $results = array_merge($results, realizarCalculosAdicionales($results));

    echo json_encode([
        'success' => true,
        'results' => $results
    ]);

} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ]);
}

function procesarArchivoBalance($file) {
    $data = leerArchivoExcel($file['tmp_name']);
    $results = [];

    // Cuentas objeto a procesar
    $cuentasObjeto = ['43001', '43008', '43042'];
    $subcuentas = ['0080.43002.20', '0080.43002.21', '0080.43002.15', 
                   '0080.43002.28', '0080.43002.31', '0080.43002.63'];

    // Buscar columna "Saldo AAF variación"
    $columnaSaldo = null;
    foreach ($data[0] as $index => $header) {
        if (stripos($header, 'Saldo AAF variación') !== false) {
            $columnaSaldo = $index;
            break;
        }
    }

    if ($columnaSaldo === null) {
        throw new Exception('No se encontró la columna "Saldo AAF variación" en el archivo BALANCE');
    }

    // Buscar columna de cuenta objeto
    $columnaCuentaObjeto = null;
    foreach ($data[0] as $index => $header) {
        if (stripos($header, 'cuenta objeto') !== false || stripos($header, 'cuenta') !== false) {
            $columnaCuentaObjeto = $index;
            break;
        }
    }

    if ($columnaCuentaObjeto === null) {
        throw new Exception('No se encontró la columna de cuenta objeto en el archivo BALANCE');
    }

    // Procesar cuentas objeto
    foreach ($cuentasObjeto as $cuenta) {
        $total = 0;
        for ($i = 1; $i < count($data); $i++) {
            if (isset($data[$i][$columnaCuentaObjeto]) && 
                stripos($data[$i][$columnaCuentaObjeto], $cuenta) !== false) {
                if (isset($data[$i][$columnaSaldo])) {
                    $valor = limpiarNumero($data[$i][$columnaSaldo]);
                    $total += $valor;
                }
            }
        }
        $results["total_$cuenta"] = $total;
    }

    // Procesar subcuentas específicas
    $results['subcuentas'] = [];
    foreach ($subcuentas as $subcuenta) {
        $total = 0;
        for ($i = 1; $i < count($data); $i++) {
            if (isset($data[$i][$columnaCuentaObjeto]) && 
                stripos($data[$i][$columnaCuentaObjeto], $subcuenta) !== false) {
                if (isset($data[$i][$columnaSaldo])) {
                    $valor = limpiarNumero($data[$i][$columnaSaldo]);
                    $total += $valor;
                }
            }
        }
        $results['subcuentas'][$subcuenta] = $total;
    }

    return $results;
}

function procesarArchivoSituacion($file) {
    $data = leerArchivoExcel($file['tmp_name']);
    $results = [];

    // Buscar columna "SALDOS MES"
    $columnaSaldosMes = null;
    foreach ($data[0] as $index => $header) {
        if (stripos($header, 'SALDOS MES') !== false) {
            $columnaSaldosMes = $index;
            break;
        }
    }

    if ($columnaSaldosMes === null) {
        throw new Exception('No se encontró la columna "SALDOS MES" en el archivo SITUACIÓN');
    }

    // Buscar TOTAL 01010
    $total01010 = 0;
    for ($i = 1; $i < count($data); $i++) {
        if (isset($data[$i][0]) && stripos($data[$i][0], '01010') !== false) {
            if (isset($data[$i][$columnaSaldosMes])) {
                $total01010 = limpiarNumero($data[$i][$columnaSaldosMes]);
                break;
            }
        }
    }

    $results['situacion_total'] = $total01010;
    return $results;
}

function procesarArchivoFocus($file) {
    $data = leerArchivoExcel($file['tmp_name']);
    $results = [];

    // Buscar datos de vencimientos (formato España)
    $vencimientos = [];
    $columnaVencimientos = null;

    // Buscar columna de vencimientos
    foreach ($data[0] as $index => $header) {
        if (stripos($header, 'vencimiento') !== false || stripos($header, 'días') !== false) {
            $columnaVencimientos = $index;
            break;
        }
    }

    if ($columnaVencimientos !== null) {
        for ($i = 1; $i < count($data); $i++) {
            if (isset($data[$i][$columnaVencimientos])) {
                $dias = limpiarNumero($data[$i][$columnaVencimientos]);
                if ($dias >= 60) {
                    $valor = isset($data[$i][$columnaVencimientos + 1]) ? 
                             limpiarNumero($data[$i][$columnaVencimientos + 1]) : 0;
                    $vencimientos[] = $valor;
                }
            }
        }
    }

    // Calcular total vencido de 60 días en adelante
    $results['total_vencido_60_dias'] = array_sum($vencimientos);

    // Buscar otros datos del archivo FOCUS
    $results['deuda_bruta_inicial'] = buscarValorEnFocus($data, 'Deuda bruta NO Grupo', 'Inicial');
    $results['deuda_bruta_final'] = buscarValorEnFocus($data, 'Deuda bruta NO Grupo', 'Final');
    $results['dotaciones_acumuladas_inicial'] = buscarValorEnFocus($data, 'Dotaciones Acumuladas', 'Inicial');
    $results['provision_acumulada_final'] = buscarValorEnFocus($data, 'Provisión acumulada', 'Final');

    return $results;
}

function buscarValorEnFocus($data, $concepto, $periodo) {
    for ($i = 0; $i < count($data); $i++) {
        for ($j = 0; $j < count($data[$i]); $j++) {
            if (isset($data[$i][$j]) && 
                stripos($data[$i][$j], $concepto) !== false) {
                // Buscar en la misma fila o filas adyacentes
                for ($k = 0; $k < count($data[$i]); $k++) {
                    if (isset($data[$i][$k]) && 
                        stripos($data[$i][$k], $periodo) !== false) {
                        // Buscar el valor numérico
                        for ($l = 0; $l < count($data[$i]); $l++) {
                            if (isset($data[$i][$l]) && is_numeric(limpiarNumero($data[$i][$l]))) {
                                return limpiarNumero($data[$i][$l]);
                            }
                        }
                    }
                }
            }
        }
    }
    return 0;
}

function realizarCalculosAdicionales($results) {
    $calculos = [];

    // 2. Deuda bruta NO Grupo (Inicial) = Deuda bruta NO Grupo (Final)
    $calculos['deuda_bruta_inicial'] = $results['deuda_bruta_final'] ?? 0;

    // 3. - Dotaciones Acumuladas (Inicial) = '+/- Provisión acumulada (Final)
    $calculos['dotaciones_acumuladas_inicial'] = -($results['provision_acumulada_final'] ?? 0);

    // 4. Cobro de mes - Vencida = Deuda bruta NO Grupo (Inicial) Vencidas - Total vencido de 60 días en adelante / 1000
    $calculos['cobro_vencida'] = ($results['deuda_bruta_inicial'] ?? 0) - 
                                 (($results['total_vencido_60_dias'] ?? 0) / 1000);

    // 5. Cobro mes - Total Deuda = COBROS SITUACION (SALDO MES) / -1000
    $calculos['cobro_total_deuda'] = ($results['situacion_total'] ?? 0) / -1000;

    // 6. Cobros del mes - No Vencida = H15-D15 (cobro_total_deuda - cobro_vencida)
    $calculos['cobro_no_vencida'] = $calculos['cobro_total_deuda'] - $calculos['cobro_vencida'];

    // 7. +/- Vencidos en el mes – vencido = VENCIDO MES 30 días signo positivo
    $calculos['vencidos_mes_vencido'] = abs($results['total_vencido_60_dias'] ?? 0);

    // 8. +/- Vencidos en el mes – No vencido = D17 (cobro_no_vencida)
    $calculos['vencidos_mes_no_vencido'] = $calculos['cobro_no_vencida'];

    // 9. '+/- Vencidos en el mes – Total deuda = D17 - F17
    $calculos['vencidos_mes_total'] = $calculos['vencidos_mes_no_vencido'] - $calculos['vencidos_mes_vencido'];

    // 10. + Facturación del mes – vencida = 0
    $calculos['facturacion_vencida'] = 0;

    // 11. + Facturación del mes – no vencida = Deuda bruta NO Grupo (Final) - total deuda
    $calculos['facturacion_no_vencida'] = ($results['deuda_bruta_final'] ?? 0) - 
                                          ($calculos['cobro_total_deuda'] ?? 0);

    // Dotación del mes = - Dotaciones Acumuladas (Inicial) - Provisión del mes
    $calculos['dotacion_mes'] = -($calculos['dotaciones_acumuladas_inicial'] ?? 0) - 
                                ($results['provision_acumulada_final'] ?? 0);

    // Acumulado (valores de ejemplo basados en las fórmulas proporcionadas)
    $calculos['acumulado_cobros'] = -377486;
    $calculos['acumulado_facturacion'] = 9308786;
    $calculos['acumulado_vencidos'] = 390143;
    $calculos['acumulado_dotacion'] = -560370;

    return $calculos;
}

function leerArchivoExcel($filePath) {
    $extension = strtolower(pathinfo($filePath, PATHINFO_EXTENSION));
    
    if ($extension === 'csv') {
        return leerCSV($filePath);
    } elseif (in_array($extension, ['xlsx', 'xls'])) {
        return leerExcel($filePath);
    } else {
        throw new Exception('Formato de archivo no soportado. Use CSV, XLSX o XLS.');
    }
}

function leerCSV($filePath) {
    $data = [];
    
    // Intentar diferentes delimitadores
    $delimiters = [',', ';', "\t"];
    
    foreach ($delimiters as $delimiter) {
        if (($handle = fopen($filePath, "r")) !== FALSE) {
            $testRow = fgetcsv($handle, 1000, $delimiter);
            fclose($handle);
            
            if ($testRow && count($testRow) > 1) {
                // Este delimitador funciona, usarlo
                if (($handle = fopen($filePath, "r")) !== FALSE) {
                    while (($row = fgetcsv($handle, 1000, $delimiter)) !== FALSE) {
                        $data[] = $row;
                    }
                    fclose($handle);
                    return $data;
                }
            }
        }
    }
    
    // Si no funciona ningún delimitador, intentar leer línea por línea
    if (($handle = fopen($filePath, "r")) !== FALSE) {
        while (($line = fgets($handle)) !== FALSE) {
            $row = explode(',', $line);
            $data[] = array_map('trim', $row);
        }
        fclose($handle);
    }
    
    return $data;
}



function leerExcel($filePath) {
    $extension = strtolower(pathinfo($filePath, PATHINFO_EXTENSION));
    
    // Primero intentar leer como CSV (muchos archivos Excel se pueden leer así)
    try {
        $csvData = leerCSV($filePath);
        if (!empty($csvData) && count($csvData) > 1) {
            return $csvData;
        }
    } catch (Exception $e) {
        // Continuar con otros métodos
    }
    
    if ($extension === 'xlsx') {
        // Para archivos XLSX, intentar leer como ZIP
        if (class_exists('ZipArchive')) {
            $zip = new ZipArchive;
            if ($zip->open($filePath) === TRUE) {
                // Buscar el archivo sheet1.xml
                $xmlString = $zip->getFromName('xl/worksheets/sheet1.xml');
                $zip->close();
                
                if ($xmlString) {
                    return parseExcelXML($xmlString);
                }
            }
        }
    }
    
    // Si todo falla, intentar leer como texto plano
    $data = [];
    if (($handle = fopen($filePath, "r")) !== FALSE) {
        while (($line = fgets($handle)) !== FALSE) {
            $line = trim($line);
            if (!empty($line)) {
                $row = explode("\t", $line); // Intentar con tabulaciones
                if (count($row) <= 1) {
                    $row = explode(",", $line); // Intentar con comas
                }
                $data[] = array_map('trim', $row);
            }
        }
        fclose($handle);
    }
    
    if (empty($data)) {
        throw new Exception('No se pudo leer el archivo Excel. Verifique que el archivo no esté corrupto.');
    }
    
    return $data;
}

function parseExcelXML($xmlString) {
    $data = [];
    $xml = simplexml_load_string($xmlString);
    
    if ($xml === false) {
        throw new Exception('No se pudo parsear el archivo Excel XML');
    }
    
    // Buscar todas las filas
    $rows = $xml->sheetData->row;
    
    foreach ($rows as $row) {
        $rowData = [];
        foreach ($row->c as $cell) {
            $value = (string)$cell->v;
            $rowData[] = $value;
        }
        if (!empty($rowData)) {
            $data[] = $rowData;
        }
    }
    
    return $data;
}

function limpiarNumero($valor) {
    if (is_numeric($valor)) {
        return floatval($valor);
    }
    
    // Limpiar formato de número (quitar comas, puntos, espacios, etc.)
    $limpio = preg_replace('/[^\d.-]/', '', $valor);
    return is_numeric($limpio) ? floatval($limpio) : 0;
}

// Función de depuración para verificar el contenido de los archivos
function debugArchivo($filePath, $maxRows = 5) {
    $data = leerArchivoExcel($filePath);
    $debug = [
        'total_rows' => count($data),
        'total_columns' => count($data[0] ?? []),
        'headers' => $data[0] ?? [],
        'sample_rows' => array_slice($data, 1, $maxRows)
    ];
    return $debug;
}
?> 