#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Pruebas Simples
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

def crear_archivo_prueba(tipo_procesamiento, ruta_archivo):
    """
    Crea un archivo de prueba para cada tipo de procesamiento
    """
    if tipo_procesamiento == "cartera":
        # Datos de prueba para cartera
        datos = {
            'CLIENTE': ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente A', 'Cliente B'],
            'CUENTA': ['CU001', 'CU002', 'CU003', 'CU004', 'CU005'],
            'SALDO': [10000, 25000, 15000, 30000, 5000],
            'FECHA': ['2025-01-15', '2025-01-20', '2025-02-01', '2025-02-15', '2025-03-01'],
            'ESTADO': ['ACTIVO', 'ACTIVO', 'INACTIVO', 'ACTIVO', 'ACTIVO']
        }
    elif tipo_procesamiento == "anticipos":
        # Datos de prueba para anticipos
        datos = {
            'CLIENTE': ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente A', 'Cliente B'],
            'MONTO_ANTICIPO': [5000, 10000, 7500, 12000, 3000],
            'FECHA_ANTICIPO': ['2025-01-15', '2025-01-20', '2025-02-01', '2025-02-15', '2025-03-01'],
            'TIPO_ANTICIPO': ['EFECTIVO', 'TRANSFERENCIA', 'CHEQUE', 'EFECTIVO', 'TRANSFERENCIA']
        }
    elif tipo_procesamiento == "balance":
        # Datos de prueba para balance
        datos = {
            'CUENTA': ['ACTIVO_CORRIENTE', 'PASIVO_CORRIENTE', 'ACTIVO_FIJO', 'PATRIMONIO'],
            'SALDO': [50000, 30000, 100000, 120000],
            'FECHA_BALANCE': ['2025-01-31', '2025-01-31', '2025-01-31', '2025-01-31'],
            'TIPO_CUENTA': ['ACTIVO', 'PASIVO', 'ACTIVO', 'PATRIMONIO']
        }
    elif tipo_procesamiento == "formato_deuda":
        # Datos de prueba para formato deuda
        datos = {
            'CLIENTE': ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente A', 'Cliente B'],
            'SALDO_DEUDA': [15000, 25000, 10000, 35000, 8000],
            'FECHA_VENCIMIENTO': ['2025-06-15', '2025-07-20', '2025-08-01', '2025-09-15', '2025-10-01'],
            'TIPO_DEUDA': ['COMERCIAL', 'COMERCIAL', 'PERSONAL', 'COMERCIAL', 'PERSONAL']
        }
    else:
        raise ValueError(f"Tipo de procesamiento no válido: {tipo_procesamiento}")
    
    # Crear DataFrame
    df = pd.DataFrame(datos)
    
    # Guardar archivo
    df.to_excel(ruta_archivo, index=False, engine='openpyxl')
    logging.info(f"Archivo de prueba creado: {ruta_archivo}")
    
    return ruta_archivo

def probar_procesador(procesador, archivo_prueba):
    """
    Prueba un procesador específico
    """
    try:
        # Importar el procesador
        if procesador == "cartera":
            from procesador_cartera import procesar_cartera
            resultado = procesar_cartera(archivo_prueba)
        elif procesador == "anticipos":
            from procesador_anticipos import procesar_anticipos
            resultado = procesar_anticipos(archivo_prueba)
        elif procesador == "balance":
            from procesador_balance_completo import procesar_balance_completo
            resultado = procesar_balance_completo(archivo_prueba)
        elif procesador == "formato_deuda":
            from procesador_formato_deuda import procesar_formato_deuda
            resultado = procesar_formato_deuda(archivo_prueba)
        else:
            raise ValueError(f"Procesador no válido: {procesador}")
        
        logging.info(f"✅ Procesador {procesador} funcionando correctamente")
        return True
        
    except Exception as e:
        logging.error(f"❌ Error en procesador {procesador}: {e}")
        return False

def main():
    """
    Función principal de pruebas
    """
    print("🧪 Iniciando pruebas del sistema de procesamiento...")
    
    # Crear directorio de pruebas si no existe
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    # Lista de procesadores a probar
    procesadores = [
        ("cartera", "procesador_cartera.py"),
        ("anticipos", "procesador_anticipos.py"),
        ("balance", "procesador_balance_completo.py"),
        ("formato_deuda", "procesador_formato_deuda.py")
    ]
    
    resultados = {}
    
    for tipo_procesamiento, nombre_procesador in procesadores:
        print(f"\n🔍 Probando {nombre_procesador}...")
        
        # Crear archivo de prueba
        archivo_prueba = f"temp/prueba_{tipo_procesamiento}.xlsx"
        crear_archivo_prueba(tipo_procesamiento, archivo_prueba)
        
        # Probar procesador
        resultado = probar_procesador(tipo_procesamiento, archivo_prueba)
        resultados[tipo_procesamiento] = resultado
        
        # Limpiar archivo de prueba
        if os.path.exists(archivo_prueba):
            os.remove(archivo_prueba)
    
    # Mostrar resumen
    print("\n📊 RESUMEN DE PRUEBAS:")
    print("=" * 50)
    
    exitos = sum(resultados.values())
    total = len(resultados)
    
    for tipo_procesamiento, resultado in resultados.items():
        estado = "✅ PASÓ" if resultado else "❌ FALLÓ"
        print(f"{estado} - {tipo_procesamiento}")
    
    print(f"\n🎯 Resultado: {exitos}/{total} procesadores funcionando correctamente")
    
    if exitos == total:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        return 0
    else:
        print("⚠️ Algunas pruebas fallaron. Revisar los errores.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 