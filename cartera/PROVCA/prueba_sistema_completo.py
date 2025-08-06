#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba del Sistema Completo
Sistema de Procesamiento de Cartera - Grupo Planeta
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def crear_archivos_prueba():
    """
    Crea archivos de prueba para todos los procesadores
    """
    archivos_creados = {}
    
    # Crear directorio de pruebas si no existe
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    # 1. Archivo de prueba para Balance Específico
    datos_balance = {
        'Cuenta': ['43001', '0080.43002.20', '0080.43002.21', '0080.43002.15', '0080.43002.28', '0080.43002.31', '0080.43002.63', '43008', '43042'],
        'Saldo AAF variación': [1000000, 500000, 750000, 300000, 450000, 600000, 250000, 800000, 900000],
        'Descripción': ['Cuenta 1', 'Cuenta 2', 'Cuenta 3', 'Cuenta 4', 'Cuenta 5', 'Cuenta 6', 'Cuenta 7', 'Cuenta 8', 'Cuenta 9']
    }
    df_balance = pd.DataFrame(datos_balance)
    archivo_balance = "temp/prueba_balance.xlsx"
    df_balance.to_excel(archivo_balance, index=False)
    archivos_creados['BALANCE'] = archivo_balance
    
    # 2. Archivo de prueba para Situación Específico
    datos_situacion = {
        'Concepto': ['TOTAL 01010', 'Otro concepto'],
        'SALDOS MES': [2500000, 1000000],
        'Otros datos': ['A', 'B']
    }
    df_situacion = pd.DataFrame(datos_situacion)
    archivo_situacion = "temp/prueba_situacion.xlsx"
    df_situacion.to_excel(archivo_situacion, index=False)
    archivos_creados['SITUACION'] = archivo_situacion
    
    # 3. Archivo de prueba para Focus Específico
    datos_focus = {
        'Vencimiento 30 días': [100000, 200000, 150000],
        'Vencimiento 60 días': [50000, 75000, 25000],
        'Vencimiento 90 días': [25000, 30000, 15000],
        'Total Deuda': [500000, 750000, 400000],
        'Cliente': ['Cliente A', 'Cliente B', 'Cliente C']
    }
    df_focus = pd.DataFrame(datos_focus)
    archivo_focus = "temp/prueba_focus.xlsx"
    df_focus.to_excel(archivo_focus, index=False)
    archivos_creados['FOCUS'] = archivo_focus
    
    # 4. Archivo de prueba para Dotación Mes
    datos_dotacion = {
        'Interco RESTO': [1000000],
        'Dotaciones Acumuladas (Inicial)': [500000],
        'Provisión del mes': [200000],
        'Otros datos': ['A']
    }
    df_dotacion = pd.DataFrame(datos_dotacion)
    archivo_dotacion = "temp/prueba_dotacion.xlsx"
    df_dotacion.to_excel(archivo_dotacion, index=False)
    archivos_creados['DOTACION_MES'] = archivo_dotacion
    
    # 5. Archivo de prueba para Acumulado
    datos_acumulado = {
        'Columna A': ['Cobros', 'Facturación', 'Vencidos'],
        'Columna B': [-377486, 0, 390143],
        'Columna C': [-7717668, 9308786, -390143],
        'Columna D': [1258658, 1200974, 0],
        'Columna E': ['Provision', 'Dotacion', 'Dotaciones'],
        'Columna F': [0, -560370, 672]
    }
    df_acumulado = pd.DataFrame(datos_acumulado)
    archivo_acumulado = "temp/prueba_acumulado.xlsx"
    df_acumulado.to_excel(archivo_acumulado, index=False)
    archivos_creados['ACUMULADO'] = archivo_acumulado
    
    # 6. Archivo de prueba para Tipos de Cambio
    datos_tipos_cambio = {
        'USD_COP': [4000.0, 4100.0, 4200.0],
        'EUR_COP': [4300.0, 4400.0, 4500.0],
        'USD_EUR': [0.85, 0.86, 0.87],
        'Fecha': ['2025-01-01', '2025-02-01', '2025-03-01']
    }
    df_tipos_cambio = pd.DataFrame(datos_tipos_cambio)
    archivo_tipos_cambio = "temp/prueba_tipos_cambio.xlsx"
    df_tipos_cambio.to_excel(archivo_tipos_cambio, index=False)
    archivos_creados['TIPOS_CAMBIO'] = archivo_tipos_cambio
    
    return archivos_creados

def probar_procesador(procesador, archivo_prueba):
    """
    Prueba un procesador específico
    """
    try:
        logging.info(f"Probando procesador: {procesador}")
        
        # Importar y ejecutar el procesador correspondiente
        if procesador == 'BALANCE':
            from procesador_balance_especifico import procesar_balance_especifico
            ruta_salida, resultados = procesar_balance_especifico(archivo_prueba)
        elif procesador == 'SITUACION':
            from procesador_situacion_especifico import procesar_situacion_especifico
            ruta_salida, resultados = procesar_situacion_especifico(archivo_prueba)
        elif procesador == 'FOCUS':
            from procesador_focus_especifico import procesar_focus_especifico
            ruta_salida, resultados = procesar_focus_especifico(archivo_prueba)
        elif procesador == 'DOTACION_MES':
            from procesador_dotacion_mes import procesar_dotacion_mes
            ruta_salida, resultados = procesar_dotacion_mes(archivo_prueba)
        elif procesador == 'ACUMULADO':
            from procesador_acumulado import procesar_acumulado
            ruta_salida, resultados = procesar_acumulado(archivo_prueba)
        elif procesador == 'TIPOS_CAMBIO':
            from procesador_tipos_cambio import procesar_tipos_cambio
            ruta_salida, resultados = procesar_tipos_cambio(archivo_prueba)
        else:
            raise ValueError(f"Procesador no válido: {procesador}")
        
        logging.info(f"✅ {procesador} procesado exitosamente")
        return True, ruta_salida
        
    except Exception as e:
        logging.error(f"❌ Error en {procesador}: {e}")
        return False, str(e)

def probar_unificador():
    """
    Prueba el unificador final
    """
    try:
        logging.info("Probando unificador final...")
        
        from unificador_final import unificar_resultados
        ruta_salida, resultados = unificar_resultados()
        
        logging.info(f"✅ Unificador final ejecutado exitosamente")
        return True, ruta_salida
        
    except Exception as e:
        logging.error(f"❌ Error en unificador final: {e}")
        return False, str(e)

def main():
    """
    Función principal de prueba del sistema completo
    """
    print("🧪 Iniciando prueba del sistema completo...")
    
    # Crear archivos de prueba
    archivos_prueba = crear_archivos_prueba()
    print(f"Archivos de prueba creados: {list(archivos_prueba.keys())}")
    
    # Lista de procesadores a probar
    procesadores = [
        'BALANCE',
        'SITUACION', 
        'FOCUS',
        'DOTACION_MES',
        'ACUMULADO',
        'TIPOS_CAMBIO'
    ]
    
    resultados = {}
    archivos_generados = []
    
    # Probar cada procesador
    for procesador in procesadores:
        if procesador in archivos_prueba:
            print(f"\n🔍 Probando {procesador}...")
            
            exito, resultado = probar_procesador(procesador, archivos_prueba[procesador])
            resultados[procesador] = exito
            
            if exito:
                archivos_generados.append(resultado)
                print(f"✅ {procesador} - EXITOSO")
            else:
                print(f"❌ {procesador} - FALLÓ: {resultado}")
    
    # Probar unificador final
    print(f"\n🔍 Probando unificador final...")
    exito_unificador, resultado_unificador = probar_unificador()
    resultados['UNIFICADOR'] = exito_unificador
    
    if exito_unificador:
        print(f"✅ UNIFICADOR - EXITOSO")
        archivos_generados.append(resultado_unificador)
    else:
        print(f"❌ UNIFICADOR - FALLÓ: {resultado_unificador}")
    
    # Mostrar resumen
    print("\n📊 RESUMEN DE PRUEBAS:")
    print("=" * 50)
    
    exitos = sum(resultados.values())
    total = len(resultados)
    
    for procesador, resultado in resultados.items():
        estado = "✅ PASÓ" if resultado else "❌ FALLÓ"
        print(f"{estado} - {procesador}")
    
    print(f"\n🎯 Resultado: {exitos}/{total} procesadores funcionando correctamente")
    
    if archivos_generados:
        print(f"\n📁 Archivos generados:")
        for archivo in archivos_generados:
            print(f"   - {archivo}")
    
    # Limpiar archivos de prueba
    print(f"\n🧹 Limpiando archivos de prueba...")
    for archivo in archivos_prueba.values():
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"   - Eliminado: {archivo}")
    
    if exitos == total:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("✅ El sistema está funcionando correctamente")
        return 0
    else:
        print("\n⚠️ Algunas pruebas fallaron. Revisar los errores.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 