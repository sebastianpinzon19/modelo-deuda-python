<?php
/**
 * Script de diagnóstico para Python
 * Verifica la instalación y configuración de Python en el sistema
 */

header('Content-Type: text/html; charset=utf-8');
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagnóstico Python - Sistema de Procesamiento</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .section {
            margin-bottom: 25px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #fafafa;
        }
        .section h2 {
            color: #34495e;
            margin-top: 0;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .status {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        .info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .code {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
        }
        .step {
            margin: 15px 0;
            padding: 15px;
            background-color: #e8f4fd;
            border-left: 4px solid #3498db;
            border-radius: 5px;
        }
        .step h3 {
            margin-top: 0;
            color: #2980b9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Diagnóstico de Python</h1>
        
        <?php
        // Función para detectar Python
        function detectarPython() {
            $comandos = ['python', 'python3', 'py'];
            $resultados = [];
            
            foreach ($comandos as $comando) {
                $output = [];
                $returnCode = 0;
                exec("$comando --version 2>&1", $output, $returnCode);
                
                if ($returnCode === 0) {
                    $resultados[$comando] = [
                        'encontrado' => true,
                        'version' => implode("\n", $output),
                        'comando' => $comando
                    ];
                } else {
                    $resultados[$comando] = [
                        'encontrado' => false,
                        'error' => implode("\n", $output)
                    ];
                }
            }
            
            return $resultados;
        }
        
        // Función para verificar rutas comunes de Python en Windows
        function verificarRutasWindows() {
            $rutas = [
                'C:\\Python39\\python.exe',
                'C:\\Python38\\python.exe',
                'C:\\Python37\\python.exe',
                'C:\\Python36\\python.exe',
                'C:\\Users\\' . get_current_user() . '\\AppData\\Local\\Programs\\Python\\Python39\\python.exe',
                'C:\\Users\\' . get_current_user() . '\\AppData\\Local\\Programs\\Python\\Python38\\python.exe',
                'C:\\Users\\' . get_current_user() . '\\AppData\\Local\\Programs\\Python\\Python37\\python.exe',
                'C:\\Users\\' . get_current_user() . '\\AppData\\Local\\Programs\\Python\\Python36\\python.exe'
            ];
            
            $encontradas = [];
            foreach ($rutas as $ruta) {
                if (file_exists($ruta)) {
                    $encontradas[] = $ruta;
                }
            }
            
            return $encontradas;
        }
        
        // Función para verificar variables de entorno
        function verificarVariablesEntorno() {
            $path = getenv('PATH');
            $python_home = getenv('PYTHON_HOME');
            $python_path = getenv('PYTHONPATH');
            
            return [
                'PATH' => $path,
                'PYTHON_HOME' => $python_home,
                'PYTHONPATH' => $python_path
            ];
        }
        
        // Ejecutar diagnósticos
        $pythonResultados = detectarPython();
        $rutasWindows = verificarRutasWindows();
        $variablesEntorno = verificarVariablesEntorno();
        ?>
        
        <div class="section">
            <h2>🐍 Detección de Python</h2>
            
            <?php
            $pythonEncontrado = false;
            foreach ($pythonResultados as $comando => $resultado) {
                if ($resultado['encontrado']) {
                    echo "<div class='status success'>";
                    echo "<strong>✅ $comando encontrado</strong><br>";
                    echo "Versión: " . htmlspecialchars($resultado['version']);
                    echo "</div>";
                    $pythonEncontrado = true;
                } else {
                    echo "<div class='status error'>";
                    echo "<strong>❌ $comando no encontrado</strong><br>";
                    echo "Error: " . htmlspecialchars($resultado['error']);
                    echo "</div>";
                }
            }
            
            if (!$pythonEncontrado) {
                echo "<div class='status warning'>";
                echo "<strong>⚠️ Python no encontrado en el PATH</strong>";
                echo "</div>";
            }
            ?>
        </div>
        
        <div class="section">
            <h2>📁 Rutas de Python en Windows</h2>
            
            <?php if (!empty($rutasWindows)): ?>
                <div class="status success">
                    <strong>✅ Python encontrado en las siguientes rutas:</strong>
                </div>
                <?php foreach ($rutasWindows as $ruta): ?>
                    <div class="code"><?php echo htmlspecialchars($ruta); ?></div>
                <?php endforeach; ?>
            <?php else: ?>
                <div class="status error">
                    <strong>❌ No se encontró Python en las rutas comunes de Windows</strong>
                </div>
            <?php endif; ?>
        </div>
        
        <div class="section">
            <h2>🔧 Variables de Entorno</h2>
            
            <div class="status info">
                <strong>PATH:</strong><br>
                <div class="code"><?php echo htmlspecialchars($variablesEntorno['PATH']); ?></div>
            </div>
            
            <?php if ($variablesEntorno['PYTHON_HOME']): ?>
                <div class="status info">
                    <strong>PYTHON_HOME:</strong> <?php echo htmlspecialchars($variablesEntorno['PYTHON_HOME']); ?>
                </div>
            <?php endif; ?>
            
            <?php if ($variablesEntorno['PYTHONPATH']): ?>
                <div class="status info">
                    <strong>PYTHONPATH:</strong> <?php echo htmlspecialchars($variablesEntorno['PYTHONPATH']); ?>
                </div>
            <?php endif; ?>
        </div>
        
        <div class="section">
            <h2>🛠️ Soluciones Recomendadas</h2>
            
            <?php if (!$pythonEncontrado && empty($rutasWindows)): ?>
                <div class="step">
                    <h3>1. Instalar Python</h3>
                    <p>Descarga e instala Python desde <a href="https://www.python.org/downloads/" target="_blank">python.org</a></p>
                    <p><strong>Importante:</strong> Durante la instalación, marca la opción "Add Python to PATH"</p>
                </div>
                
                <div class="step">
                    <h3>2. Verificar la instalación</h3>
                    <p>Abre una nueva ventana de Command Prompt y ejecuta:</p>
                    <div class="code">python --version</div>
                </div>
                
                <div class="step">
                    <h3>3. Si Python está instalado pero no en PATH</h3>
                    <p>Busca la ruta de instalación de Python y agrega manualmente al PATH:</p>
                    <ol>
                        <li>Abre "Variables de entorno del sistema"</li>
                        <li>Edita la variable PATH</li>
                        <li>Agrega la ruta donde está instalado Python (ej: C:\Python39\)</li>
                        <li>Agrega también la ruta Scripts (ej: C:\Python39\Scripts\)</li>
                    </ol>
                </div>
            <?php elseif (!empty($rutasWindows) && !$pythonEncontrado): ?>
                <div class="step">
                    <h3>Python está instalado pero no en PATH</h3>
                    <p>Python se encontró en las siguientes rutas pero no está en el PATH del sistema:</p>
                    <?php foreach ($rutasWindows as $ruta): ?>
                        <div class="code"><?php echo htmlspecialchars($ruta); ?></div>
                    <?php endforeach; ?>
                    
                    <p><strong>Solución:</strong> Agrega la carpeta de Python al PATH del sistema o modifica la configuración del sistema para usar la ruta completa.</p>
                </div>
            <?php else: ?>
                <div class="step">
                    <h3>✅ Python está correctamente configurado</h3>
                    <p>El sistema debería funcionar correctamente con Python.</p>
                </div>
            <?php endif; ?>
        </div>
        
        <div class="section">
            <h2>📋 Información del Sistema</h2>
            
            <div class="status info">
                <strong>Sistema Operativo:</strong> <?php echo php_uname('s'); ?><br>
                <strong>Arquitectura:</strong> <?php echo php_uname('m'); ?><br>
                <strong>Versión de PHP:</strong> <?php echo phpversion(); ?><br>
                <strong>Usuario actual:</strong> <?php echo get_current_user(); ?>
            </div>
        </div>
        
        <div class="section">
            <h2>🔄 Probar Comando Python</h2>
            
            <form method="post" action="">
                <button type="submit" name="test_python" style="padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Probar Comando Python
                </button>
            </form>
            
            <?php
            if (isset($_POST['test_python'])) {
                echo "<div class='status info'>";
                echo "<strong>Resultado del comando 'python --version':</strong><br>";
                $output = [];
                $returnCode = 0;
                exec("python --version 2>&1", $output, $returnCode);
                
                if ($returnCode === 0) {
                    echo "<div class='status success'>";
                    echo "✅ Comando ejecutado exitosamente:<br>";
                    echo "<div class='code'>" . htmlspecialchars(implode("\n", $output)) . "</div>";
                    echo "</div>";
                } else {
                    echo "<div class='status error'>";
                    echo "❌ Error al ejecutar comando:<br>";
                    echo "<div class='code'>" . htmlspecialchars(implode("\n", $output)) . "</div>";
                    echo "</div>";
                }
                echo "</div>";
            }
            ?>
        </div>
    </div>
</body>
</html> 