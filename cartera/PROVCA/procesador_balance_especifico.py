#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador Específico de Balance
Sistema de Procesamiento de Cartera - Grupo Planeta
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import logging
from utilidades_cartera import *

def procesar_balance_especifico(ruta_archivo):
    """
    Procesa archivo de balance según reglas específicas
    """
    try:
        logging.info(f"Iniciando procesamiento específico de balance: {ruta_archivo}")
        
        # Validar archivo
        validar_archivo(ruta_archivo)
        
        # Leer archivo
        df = leer_archivo(ruta_archivo)
        logging.info(f"Archivo leído: {len(df)} registros")
        
        # Procesar datos según reglas específicas
        resultados = procesar_datos_balance_especifico(df)
        
        # Generar archivo de salida
        nombre_salida = generar_nombre_archivo_salida("balance_especifico_procesado")
        ruta_salida = os.path.join("resultados", nombre_salida)
        
        # Crear directorio si no existe
        crear_directorio_si_no_existe("resultados")
        
        # Guardar resultado
        escribir_resultado(resultados, ruta_salida)
        
        logging.info("Procesamiento específico de balance completado exitosamente")
        return ruta_salida, resultados
        
    except Exception as e:
        logging.error(f"Error en procesamiento específico de balance: {e}")
        raise

def procesar_datos_balance_especifico(df):
    """
    Procesa los datos de balance según las reglas específicas
    """
    # Normalizar nombres de columnas
    df.columns = df.columns.str.strip().str.upper()
    
    # Cuentas específicas a procesar según reglas
    cuentas_especificas = [
        '43001',  # Total cuenta objeto 43001
        '0080.43002.20',
        '0080.43002.21', 
        '0080.43002.15',
        '0080.43002.28',
        '0080.43002.31',
        '0080.43002.63',
        '43008',  # Total cuenta objeto 43008
        '43042'   # Total cuenta objeto 43042
    ]
    
    # Buscar columna "Saldo AAF variación"
    columna_saldo = None
    for col in df.columns:
        if 'SALDO AAF VARIACIÓN' in col.upper() or 'SALDO AAF VARIACION' in col.upper():
            columna_saldo = col
            break
    
    if columna_saldo is None:
        raise ValueError("No se encontró la columna 'Saldo AAF variación'")
    
    # Buscar columna de cuenta
    columna_cuenta = None
    for col in df.columns:
        if 'CUENTA' in col.upper() or 'OBJETO' in col.upper():
            columna_cuenta = col
            break
    
    if columna_cuenta is None:
        raise ValueError("No se encontró la columna de cuenta/objeto")
    
    # Filtrar por cuentas específicas
    df_filtrado = df[df[columna_cuenta].astype(str).str.contains('|'.join(cuentas_especificas), na=False)]
    
    # Calcular totales por cuenta
    resultados = {}
    for cuenta in cuentas_especificas:
        # Filtrar registros que contengan la cuenta
        df_cuenta = df_filtrado[df_filtrado[columna_cuenta].astype(str).str.contains(cuenta, na=False)]
        
        if not df_cuenta.empty:
            total_saldo = df_cuenta[columna_saldo].sum()
            resultados[f'Total_Cuenta_{cuenta}'] = total_saldo
            logging.info(f"Cuenta {cuenta}: {total_saldo:,.2f}")
        else:
            resultados[f'Total_Cuenta_{cuenta}'] = 0
            logging.warning(f"No se encontraron registros para la cuenta {cuenta}")
    
    # Calcular total general
    total_general = sum(resultados.values())
    resultados['Total_General'] = total_general
    
    # Crear DataFrame de resultados
    df_resultados = pd.DataFrame({
        'Cuenta': list(resultados.keys()),
        'Saldo_AAF_Variacion': list(resultados.values()),
        'Fecha_Procesamiento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Tipo_Procesamiento': 'BALANCE_ESPECIFICO'
    })
    
    # Agregar información adicional
    info_adicional = {
        'Registros_Originales': len(df),
        'Registros_Filtrados': len(df_filtrado),
        'Cuentas_Procesadas': len(cuentas_especificas),
        'Total_General': total_general
    }
    
    return df_resultados, info_adicional

def main():
    """
    Función principal
    """
    if len(sys.argv) != 2:
        print("Uso: python procesador_balance_especifico.py <ruta_archivo>")
        sys.exit(1)
    
    ruta_archivo = sys.argv[1]
    
    try:
        ruta_salida, resultados = procesar_balance_especifico(ruta_archivo)
        print(f"Procesamiento completado exitosamente")
        print(f"Archivo de salida: {ruta_salida}")
        print(f"Resultados: {resultados}")
        
    except Exception as e:
        print(f"Error en procesamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 