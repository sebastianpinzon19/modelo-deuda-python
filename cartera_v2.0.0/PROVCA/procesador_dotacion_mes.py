#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Dotación del Mes
Sistema de Procesamiento de Cartera - Grupo Planeta
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import logging
from utilidades_cartera import *

def procesar_dotacion_mes(ruta_archivo):
    """
    Procesa archivo de dotación del mes según reglas específicas
    """
    try:
        logging.info(f"Iniciando procesamiento de dotación del mes: {ruta_archivo}")
        
        # Validar archivo
        validar_archivo(ruta_archivo)
        
        # Leer archivo
        df = leer_archivo(ruta_archivo)
        logging.info(f"Archivo leído: {len(df)} registros")
        
        # Procesar datos según reglas específicas
        resultados = procesar_datos_dotacion_mes(df)
        
        # Generar archivo de salida
        nombre_salida = generar_nombre_archivo_salida("dotacion_mes_procesado")
        ruta_salida = os.path.join("resultados", nombre_salida)
        
        # Crear directorio si no existe
        crear_directorio_si_no_existe("resultados")
        
        # Guardar resultado
        escribir_resultado(resultados, ruta_salida)
        
        logging.info("Procesamiento de dotación del mes completado exitosamente")
        return ruta_salida, resultados
        
    except Exception as e:
        logging.error(f"Error en procesamiento de dotación del mes: {e}")
        raise

def procesar_datos_dotacion_mes(df):
    """
    Procesa los datos de dotación del mes según las reglas específicas
    """
    # Normalizar nombres de columnas
    df.columns = df.columns.str.strip().str.upper()
    
    # Buscar columnas relacionadas con dotaciones
    columnas_dotacion = []
    for col in df.columns:
        if any(palabra in col.upper() for palabra in ['DOTACION', 'PROVISION', 'ACUMULADA', 'INTERCO']):
            columnas_dotacion.append(col)
    
    logging.info(f"Columnas de dotación encontradas: {columnas_dotacion}")
    
    # Buscar columna "Interco RESTO"
    columna_interco_resto = None
    for col in df.columns:
        if 'INTERCO RESTO' in col.upper() or 'INTERCO' in col.upper():
            columna_interco_resto = col
            break
    
    # Buscar columna "Provisión del mes"
    columna_provision_mes = None
    for col in df.columns:
        if 'PROVISION DEL MES' in col.upper() or 'PROVISION MES' in col.upper():
            columna_provision_mes = col
            break
    
    # Buscar columna "Dotaciones Acumuladas (Inicial)"
    columna_dotaciones_acumuladas = None
    for col in df.columns:
        if 'DOTACIONES ACUMULADAS' in col.upper() and 'INICIAL' in col.upper():
            columna_dotaciones_acumuladas = col
            break
    
    # Calcular dotación del mes según fórmula:
    # Dotación del mes = Interco RESTO - Dotaciones Acumuladas (Inicial) - Provisión del mes
    
    resultados_dotacion = {}
    
    # Obtener valores
    valor_interco_resto = 0
    valor_dotaciones_acumuladas = 0
    valor_provision_mes = 0
    
    if columna_interco_resto and columna_interco_resto in df.columns:
        valor_interco_resto = df[columna_interco_resto].sum()
        resultados_dotacion['Interco_RESTO'] = valor_interco_resto
        logging.info(f"Interco RESTO: {valor_interco_resto:,.2f}")
    
    if columna_dotaciones_acumuladas and columna_dotaciones_acumuladas in df.columns:
        valor_dotaciones_acumuladas = df[columna_dotaciones_acumuladas].sum()
        resultados_dotacion['Dotaciones_Acumuladas_Inicial'] = valor_dotaciones_acumuladas
        logging.info(f"Dotaciones Acumuladas (Inicial): {valor_dotaciones_acumuladas:,.2f}")
    
    if columna_provision_mes and columna_provision_mes in df.columns:
        valor_provision_mes = df[columna_provision_mes].sum()
        resultados_dotacion['Provision_Mes'] = valor_provision_mes
        logging.info(f"Provisión del mes: {valor_provision_mes:,.2f}")
    
    # Calcular dotación del mes
    dotacion_mes = valor_interco_resto - valor_dotaciones_acumuladas - valor_provision_mes
    resultados_dotacion['Dotacion_Mes'] = dotacion_mes
    logging.info(f"Dotación del mes calculada: {dotacion_mes:,.2f}")
    
    # Crear DataFrame de resultados
    df_resultados = pd.DataFrame({
        'Concepto': list(resultados_dotacion.keys()),
        'Valor': list(resultados_dotacion.values()),
        'Fecha_Procesamiento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Tipo_Procesamiento': 'DOTACION_MES'
    })
    
    # Agregar información adicional
    info_adicional = {
        'Registros_Originales': len(df),
        'Columnas_Dotacion': columnas_dotacion,
        'Columna_Interco_Resto': columna_interco_resto,
        'Columna_Dotaciones_Acumuladas': columna_dotaciones_acumuladas,
        'Columna_Provision_Mes': columna_provision_mes,
        'Dotacion_Mes_Calculada': dotacion_mes
    }
    
    return df_resultados, info_adicional

def main():
    """
    Función principal
    """
    if len(sys.argv) != 2:
        print("Uso: python procesador_dotacion_mes.py <ruta_archivo>")
        sys.exit(1)
    
    ruta_archivo = sys.argv[1]
    
    try:
        ruta_salida, resultados = procesar_dotacion_mes(ruta_archivo)
        print(f"Procesamiento completado exitosamente")
        print(f"Archivo de salida: {ruta_salida}")
        print(f"Resultados: {resultados}")
        
    except Exception as e:
        print(f"Error en procesamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 