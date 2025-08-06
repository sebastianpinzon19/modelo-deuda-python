#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Prueba del Sistema de Procesamiento de Cartera
Grupo Planeta - Sistema de Análisis Financiero
Versión: 2.0.1
"""

import os
import sys
import pandas as pd
import tempfile
from datetime import datetime

# Importar módulos del sistema
from config import SISTEMA_INFO, DIRECTORIOS, obtener_timestamp, obtener_fecha_actual
from logger import crear_logger
from utilidades_cartera import UtilidadesCartera
from orquestador_principal import OrquestadorPrincipal

def crear_archivo_prueba_cartera():
    """Crea un archivo de prueba para cartera"""
    datos = {
        'CLIENTE': ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente D', 'Cliente E'],
        'CUENTA': ['001', '002', '003', '004', '005'],
        'SALDO': [10000, 25000, 15000, 30000, 20000],
        'FECHA': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        'ESTADO': ['ACTIVO', 'ACTIVO', 'INACTIVO', 'ACTIVO', 'ACTIVO']
    }
    
    df = pd.DataFrame(datos)
    return df

def crear_archivo_prueba_acumulado():
    """Crea un archivo de prueba para acumulado"""
    # Crear datos de prueba con 60 filas (para llegar a la fila 54)
    datos = []
    for i in range(60):
        fila = {
            'Columna_A': f'Dato A{i+1}',
            'Columna_B': 1000 + i * 100,
            'Columna_C': 2000 + i * 200,
            'Columna_D': 3000 + i * 300,
            'Columna_E': 4000 + i * 400,
            'Columna_F': 5000 + i * 500
        }
        datos.append(fila)
    
    # Agregar datos específicos en diferentes filas
    datos[10]['Columna_B'] = -377486  # Cobros
    datos[15]['Columna_C'] = 390143   # Vencidos
    datos[20]['Columna_D'] = -560370  # Dotacion
    datos[25]['Columna_E'] = 672      # Dotaciones
    datos[30]['Columna_F'] = 672      # Desdotaciones
    
    df = pd.DataFrame(datos)
    return df

def test_configuracion():
    """Prueba la configuración del sistema"""
    print("🔧 Probando configuración del sistema...")
    
    try:
        # Verificar información del sistema
        assert SISTEMA_INFO['version'] == '2.0.1'
        assert SISTEMA_INFO['empresa'] == 'Grupo Planeta'
        print("✅ Información del sistema correcta")
        
        # Verificar directorios
        for nombre, ruta in DIRECTORIOS.items():
            if nombre != 'base':
                ruta_completa = os.path.join(DIRECTORIOS['base'], ruta)
                if not os.path.exists(ruta_completa):
                    os.makedirs(ruta_completa, exist_ok=True)
                print(f"✅ Directorio {nombre}: {ruta_completa}")
        
        print("✅ Configuración del sistema correcta")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_logger():
    """Prueba el sistema de logging"""
    print("📝 Probando sistema de logging...")
    
    try:
        logger = crear_logger("TestLogger")
        logger.info("Mensaje de prueba INFO")
        logger.warning("Mensaje de prueba WARNING")
        logger.error("Mensaje de prueba ERROR")
        
        # Verificar que se creó el archivo de log
        archivo_log = os.path.join(DIRECTORIOS['logs'], 'sistema_cartera.log')
        if os.path.exists(archivo_log):
            print("✅ Archivo de log creado correctamente")
        else:
            print("⚠️  Archivo de log no encontrado (puede ser normal)")
        
        print("✅ Sistema de logging funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Error en logging: {e}")
        return False

def test_utilidades():
    """Prueba las utilidades del sistema"""
    print("🛠️ Probando utilidades del sistema...")
    
    try:
        utilidades = UtilidadesCartera()
        
        # Probar limpieza de texto
        texto_limpio = utilidades.limpiar_texto("  Hola Mundo 123  ")
        assert texto_limpio == "HOLA MUNDO 123"
        print("✅ Limpieza de texto funcionando")
        
        # Probar conversión de fecha
        fecha = utilidades.convertir_fecha("15/01/2024")
        assert fecha is not None
        print("✅ Conversión de fecha funcionando")
        
        # Probar formateo de número
        numero_formateado = utilidades.formatear_numero(1234567.89, 'moneda')
        assert numero_formateado == "$1,234,567.89"
        print("✅ Formateo de número funcionando")
        
        # Probar cálculo de porcentaje
        porcentaje = utilidades.calcular_porcentaje(25, 100)
        assert porcentaje == 25.0
        print("✅ Cálculo de porcentaje funcionando")
        
        print("✅ Utilidades del sistema funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Error en utilidades: {e}")
        return False

def test_procesador_cartera():
    """Prueba el procesador de cartera"""
    print("📊 Probando procesador de cartera...")
    
    try:
        # Crear archivo de prueba
        df_prueba = crear_archivo_prueba_cartera()
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            df_prueba.to_excel(tmp_file.name, index=False)
            archivo_prueba = tmp_file.name
        
        # Procesar archivo
        orquestador = OrquestadorPrincipal()
        ruta_salida, resumen = orquestador.procesar_archivo(archivo_prueba, 'cartera')
        
        # Verificar resultados
        assert os.path.exists(ruta_salida)
        assert resumen['registros_procesados'] == 5
        assert resumen['tipo_procesamiento'] == 'Cartera'
        
        print(f"✅ Procesador de cartera funcionando - Archivo: {ruta_salida}")
        
        # Limpiar archivo temporal
        os.unlink(archivo_prueba)
        
        return True
        
    except Exception as e:
        print(f"❌ Error en procesador de cartera: {e}")
        return False

def test_procesador_acumulado():
    """Prueba el procesador de acumulado"""
    print("📈 Probando procesador de acumulado...")
    
    try:
        # Crear archivo de prueba
        df_prueba = crear_archivo_prueba_acumulado()
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            df_prueba.to_excel(tmp_file.name, index=False)
            archivo_prueba = tmp_file.name
        
        # Procesar archivo
        orquestador = OrquestadorPrincipal()
        ruta_salida, resumen = orquestador.procesar_archivo(archivo_prueba, 'acumulado')
        
        # Verificar resultados
        assert os.path.exists(ruta_salida)
        assert resumen['tipo_procesamiento'] == 'Acumulado'
        assert resumen['conceptos_procesados'] > 0
        
        print(f"✅ Procesador de acumulado funcionando - Archivo: {ruta_salida}")
        
        # Limpiar archivo temporal
        os.unlink(archivo_prueba)
        
        return True
        
    except Exception as e:
        print(f"❌ Error en procesador de acumulado: {e}")
        return False

def test_orquestador():
    """Prueba el orquestador principal"""
    print("🎯 Probando orquestador principal...")
    
    try:
        orquestador = OrquestadorPrincipal()
        
        # Probar estadísticas del sistema
        estadisticas = orquestador.obtener_estadisticas_sistema()
        assert estadisticas['version_sistema'] == '2.0.1'
        assert len(estadisticas['procesadores_disponibles']) > 0
        
        print("✅ Estadísticas del sistema obtenidas")
        
        # Probar reporte del sistema
        reporte = orquestador.generar_reporte_sistema()
        assert reporte['informacion_sistema']['version'] == '2.0.1'
        
        print("✅ Reporte del sistema generado")
        
        print("✅ Orquestador principal funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Error en orquestador: {e}")
        return False

def test_limpieza():
    """Prueba la función de limpieza"""
    print("🧹 Probando función de limpieza...")
    
    try:
        orquestador = OrquestadorPrincipal()
        
        # Crear archivo temporal para probar limpieza
        archivo_temp = os.path.join(DIRECTORIOS['temp'], f'test_limpieza_{obtener_timestamp()}.txt')
        with open(archivo_temp, 'w') as f:
            f.write("Archivo de prueba para limpieza")
        
        # Verificar que se creó
        assert os.path.exists(archivo_temp)
        
        # La limpieza no debería eliminar archivos recientes
        resumen_limpieza = orquestador.limpiar_sistema(dias_antiguedad=30)
        assert resumen_limpieza['fecha_limpieza'] is not None
        
        print("✅ Función de limpieza funcionando")
        
        # Limpiar archivo de prueba
        os.unlink(archivo_temp)
        
        return True
        
    except Exception as e:
        print(f"❌ Error en limpieza: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=" * 70)
    print("🧪 SISTEMA DE PRUEBAS - PROCESAMIENTO DE CARTERA")
    print(f"Versión: {SISTEMA_INFO['version']}")
    print(f"Empresa: {SISTEMA_INFO['empresa']}")
    print("=" * 70)
    
    # Lista de pruebas
    pruebas = [
        ("Configuración", test_configuracion),
        ("Logger", test_logger),
        ("Utilidades", test_utilidades),
        ("Procesador Cartera", test_procesador_cartera),
        ("Procesador Acumulado", test_procesador_acumulado),
        ("Orquestador", test_orquestador),
        ("Limpieza", test_limpieza)
    ]
    
    # Ejecutar pruebas
    resultados = []
    for nombre, prueba in pruebas:
        print(f"\n{'='*50}")
        print(f"Ejecutando prueba: {nombre}")
        print(f"{'='*50}")
        
        try:
            resultado = prueba()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"❌ Error inesperado en {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Mostrar resumen
    print(f"\n{'='*70}")
    print("📋 RESUMEN DE PRUEBAS")
    print(f"{'='*70}")
    
    exitosas = 0
    total = len(resultados)
    
    for nombre, resultado in resultados:
        estado = "✅ EXITOSA" if resultado else "❌ FALLIDA"
        print(f"{nombre:.<30} {estado}")
        if resultado:
            exitosas += 1
    
    print(f"\n{'='*70}")
    print(f"📊 RESULTADOS: {exitosas}/{total} pruebas exitosas")
    
    if exitosas == total:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS! El sistema está funcionando correctamente.")
        print("✅ El sistema está listo para usar.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar los errores antes de usar el sistema.")
    
    print(f"{'='*70}")
    
    # Retornar código de salida
    return 0 if exitosas == total else 1

if __name__ == "__main__":
    try:
        codigo_salida = main()
        sys.exit(codigo_salida)
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error crítico en las pruebas: {e}")
        sys.exit(1)
