#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador Específico de Situación
Sistema de Procesamiento de Cartera - Grupo Planeta
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import logging
from utilidades_cartera import *

def procesar_situacion_especifico(ruta_archivo):
    """
    Procesa archivo de situación según reglas específicas
    """
    try:
        logging.info(f"Iniciando procesamiento específico de situación: {ruta_archivo}")
        
        # Validar archivo
        validar_archivo(ruta_archivo)
        
        # Leer archivo
        df = leer_archivo(ruta_archivo)
        logging.info(f"Archivo leído: {len(df)} registros")
        
        # Procesar datos según reglas específicas
        resultados, info_adicional = procesar_datos_situacion_especifico(df)
        
        # Generar archivo de salida
        nombre_salida = generar_nombre_archivo_salida("situacion_especifico_procesado")
        ruta_salida = os.path.join("resultados", nombre_salida)
        
        # Crear directorio si no existe
        crear_directorio_si_no_existe("resultados")
        
        # Guardar resultado
        escribir_resultado(resultados, ruta_salida)
        
        logging.info("Procesamiento específico de situación completado exitosamente")
        return ruta_salida, resultados
        
    except Exception as e:
        logging.error(f"Error en procesamiento específico de situación: {e}")
        raise

def procesar_datos_situacion_especifico(df):
    """
    Procesa los datos de situación según las reglas específicas
    """
    # Normalizar nombres de columnas
    df.columns = df.columns.str.strip().str.upper()
    
    # Buscar columna "SALDOS MES"
    columna_saldos_mes = None
    for col in df.columns:
        if 'SALDOS MES' in col.upper():
            columna_saldos_mes = col
            break
    
    if columna_saldos_mes is None:
        raise ValueError("No se encontró la columna 'SALDOS MES'")
    
    # Buscar columna que contenga "TOTAL 01010"
    columna_total = None
    for col in df.columns:
        if 'TOTAL' in col.upper() and '01010' in str(df[col].iloc[0]).upper():
            columna_total = col
            break
    
    if columna_total is None:
        # Buscar en los valores de la primera columna
        for idx, valor in enumerate(df.iloc[:, 0]):
            if 'TOTAL 01010' in str(valor).upper():
                columna_total = df.columns[0]
                break
    
    if columna_total is None:
        raise ValueError("No se encontró 'TOTAL 01010' en el archivo")
    
    # Buscar la fila que contenga "TOTAL 01010"
    fila_total = None
    for idx, valor in enumerate(df[columna_total]):
        if 'TOTAL 01010' in str(valor).upper():
            fila_total = idx
            break
    
    if fila_total is None:
        raise ValueError("No se encontró la fila con 'TOTAL 01010'")
    
    # Obtener el valor de SALDOS MES para TOTAL 01010
    valor_saldos_mes = df.loc[fila_total, columna_saldos_mes]
    
    # Convertir a numérico si es posible
    try:
        valor_saldos_mes = pd.to_numeric(valor_saldos_mes, errors='coerce')
        if pd.isna(valor_saldos_mes):
            valor_saldos_mes = 0
    except:
        valor_saldos_mes = 0
    
    logging.info(f"Valor encontrado para TOTAL 01010 - SALDOS MES: {valor_saldos_mes}")
    
    # Crear DataFrame de resultados
    df_resultados = pd.DataFrame({
        'Concepto': ['TOTAL_01010_SALDOS_MES'],
        'Valor': [valor_saldos_mes],
        'Fecha_Procesamiento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Tipo_Procesamiento': 'SITUACION_ESPECIFICO'
    })
    
    # Agregar información adicional
    info_adicional = {
        'Registros_Originales': len(df),
        'Fila_Encontrada': fila_total,
        'Columna_Saldos_Mes': columna_saldos_mes,
        'Columna_Total': columna_total,
        'Valor_Extraido': valor_saldos_mes
    }
    
    return df_resultados, info_adicional

def main():
    """
    Función principal
    """
    if len(sys.argv) != 2:
        print("Uso: python procesador_situacion_especifico.py <ruta_archivo>")
        sys.exit(1)
    
    ruta_archivo = sys.argv[1]
    
    try:
        ruta_salida, resultados = procesar_situacion_especifico(ruta_archivo)
        print(f"Procesamiento completado exitosamente")
        print(f"Archivo de salida: {ruta_salida}")
        print(f"Resultados: {resultados}")
        
    except Exception as e:
        print(f"Error en procesamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 