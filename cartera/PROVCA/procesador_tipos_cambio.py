#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Tipos de Cambio
Sistema de Procesamiento de Cartera - Grupo Planeta
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import logging
from utilidades_cartera import *

def procesar_tipos_cambio(ruta_archivo):
    """
    Procesa archivo de tipos de cambio según reglas específicas
    """
    try:
        logging.info(f"Iniciando procesamiento de tipos de cambio: {ruta_archivo}")
        
        # Validar archivo
        validar_archivo(ruta_archivo)
        
        # Leer archivo
        df = leer_archivo(ruta_archivo)
        logging.info(f"Archivo leído: {len(df)} registros")
        
        # Procesar datos según reglas específicas
        resultados = procesar_datos_tipos_cambio(df)
        
        # Generar archivo de salida
        nombre_salida = generar_nombre_archivo_salida("tipos_cambio_procesado")
        ruta_salida = os.path.join("resultados", nombre_salida)
        
        # Crear directorio si no existe
        crear_directorio_si_no_existe("resultados")
        
        # Guardar resultado
        escribir_resultado(resultados, ruta_salida)
        
        logging.info("Procesamiento de tipos de cambio completado exitosamente")
        return ruta_salida, resultados
        
    except Exception as e:
        logging.error(f"Error en procesamiento de tipos de cambio: {e}")
        raise

def procesar_datos_tipos_cambio(df):
    """
    Procesa los datos de tipos de cambio según las reglas específicas
    """
    # Normalizar nombres de columnas
    df.columns = df.columns.str.strip().str.upper()
    
    # Buscar columnas relacionadas con tipos de cambio
    columnas_tipo_cambio = []
    for col in df.columns:
        if any(palabra in col.upper() for palabra in ['TIPO', 'CAMBIO', 'TASA', 'MONEDA', 'USD', 'EUR']):
            columnas_tipo_cambio.append(col)
    
    logging.info(f"Columnas de tipos de cambio encontradas: {columnas_tipo_cambio}")
    
    # Buscar columna de fecha/mes
    columna_fecha = None
    for col in df.columns:
        if any(palabra in col.upper() for palabra in ['FECHA', 'MES', 'PERIODO', 'CIERRE']):
            columna_fecha = col
            break
    
    # Obtener mes de cierre actual
    mes_cierre_actual = datetime.now().strftime('%Y-%m')
    logging.info(f"Mes de cierre actual: {mes_cierre_actual}")
    
    # Actualizar tipos de cambio según el mes de cierre
    resultados_tipos_cambio = {}
    
    # Tipos de cambio por defecto (pueden ser actualizados según necesidades)
    tipos_cambio_default = {
        'USD_COP': 4000.0,  # Dólar a Peso Colombiano
        'EUR_COP': 4300.0,  # Euro a Peso Colombiano
        'USD_EUR': 0.85,     # Dólar a Euro
        'COP_USD': 0.00025,  # Peso Colombiano a Dólar
        'COP_EUR': 0.00023   # Peso Colombiano a Euro
    }
    
    # Buscar tipos de cambio existentes en el archivo
    for tipo_cambio, valor_default in tipos_cambio_default.items():
        # Buscar en las columnas
        for col in df.columns:
            if tipo_cambio.replace('_', '') in col.upper() or tipo_cambio.split('_')[0] in col.upper():
                # Buscar el valor más reciente
                valores = df[col].dropna()
                if not valores.empty:
                    valor_actual = valores.iloc[-1]
                    resultados_tipos_cambio[f'{tipo_cambio}_Actual'] = valor_actual
                    logging.info(f"{tipo_cambio} actual: {valor_actual}")
                else:
                    resultados_tipos_cambio[f'{tipo_cambio}_Actual'] = valor_default
                    logging.info(f"{tipo_cambio} no encontrado, usando valor por defecto: {valor_default}")
                break
        else:
            resultados_tipos_cambio[f'{tipo_cambio}_Actual'] = valor_default
            logging.info(f"Columna para {tipo_cambio} no encontrada, usando valor por defecto: {valor_default}")
    
    # Agregar información del mes de cierre
    resultados_tipos_cambio['Mes_Cierre'] = mes_cierre_actual
    resultados_tipos_cambio['Fecha_Actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Crear DataFrame de resultados
    df_resultados = pd.DataFrame({
        'Concepto': list(resultados_tipos_cambio.keys()),
        'Valor': list(resultados_tipos_cambio.values()),
        'Fecha_Procesamiento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Tipo_Procesamiento': 'TIPOS_CAMBIO'
    })
    
    # Agregar información adicional
    info_adicional = {
        'Registros_Originales': len(df),
        'Columnas_Tipo_Cambio': columnas_tipo_cambio,
        'Columna_Fecha': columna_fecha,
        'Mes_Cierre_Actual': mes_cierre_actual,
        'Tipos_Cambio_Procesados': len(tipos_cambio_default)
    }
    
    return df_resultados, info_adicional

def main():
    """
    Función principal
    """
    if len(sys.argv) != 2:
        print("Uso: python procesador_tipos_cambio.py <ruta_archivo>")
        sys.exit(1)
    
    ruta_archivo = sys.argv[1]
    
    try:
        ruta_salida, resultados = procesar_tipos_cambio(ruta_archivo)
        print(f"Procesamiento completado exitosamente")
        print(f"Archivo de salida: {ruta_salida}")
        print(f"Resultados: {resultados}")
        
    except Exception as e:
        print(f"Error en procesamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 