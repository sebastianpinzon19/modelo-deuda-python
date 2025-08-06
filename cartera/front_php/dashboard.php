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

        .sistema .button-icon {
            background: linear-gradient(135deg, #6b7280, #4b5563);
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

        <!-- Botones principales -->
        <div class="main-buttons">
            <a href="procesar_cartera.php" class="main-button balance">
                <div class="button-icon">
                    <i class="fas fa-balance-scale"></i>
                </div>
                <div class="button-content">
                    <h3>Procesador de Cartera</h3>
                    <p>Análisis completo de balance, situación y focus</p>
                </div>
            </a>

            <a href="procesar_balance.php" class="main-button cartera">
                <div class="button-icon">
                    <i class="fas fa-chart-bar"></i>
                </div>
                <div class="button-content">
                    <h3>Procesador de Balance</h3>
                    <p>Procesamiento específico de archivos de balance</p>
                </div>
            </a>

            <a href="modelo_deuda.php" class="main-button modelo">
                <div class="button-icon">
                    <i class="fas fa-calculator"></i>
                </div>
                <div class="button-content">
                    <h3>Modelo de Deuda</h3>
                    <p>Genera modelo de deuda y análisis financiero</p>
                </div>
            </a>

            <a href="estado_sistema.php" class="main-button sistema">
                <div class="button-icon">
                    <i class="fas fa-server"></i>
                </div>
                <div class="button-content">
                    <h3>Estado del Sistema</h3>
                    <p>Monitoreo y configuración del sistema</p>
                </div>
            </a>
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
    </script>
</body>
</html> 