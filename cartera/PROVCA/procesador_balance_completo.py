#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Balance Completo
Sistema de Procesamiento de Cartera - Grupo Planeta
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import logging
from utilidades_cartera import *

def procesar_balance_completo(ruta_archivo):
    """
    Procesa archivo de balance completo
    """
    try:
        logging.info(f"Iniciando procesamiento de balance completo: {ruta_archivo}")
        
        # Validar archivo
        validar_archivo(ruta_archivo)
        
        # Leer archivo
        df = leer_archivo(ruta_archivo)
        logging.info(f"Archivo leído: {len(df)} registros")
        
        # Limpiar dataframe
        df = limpiar_dataframe(df)
        logging.info(f"Dataframe limpiado: {len(df)} registros")
        
        # Procesar datos
        df_procesado = procesar_datos_balance(df)
        
        # Generar archivo de salida
        nombre_salida = generar_nombre_archivo_salida("balance_completo_procesado")
        ruta_salida = os.path.join("resultados", nombre_salida)
        
        # Crear directorio si no existe
        crear_directorio_si_no_existe("resultados")
        
        # Guardar resultado
        escribir_resultado(df_procesado, ruta_salida)
        
        # Crear resumen
        resumen = crear_resumen_procesamiento(df, df_procesado, "Balance Completo")
        
        logging.info("Procesamiento de balance completo completado exitosamente")
        return ruta_salida, resumen
        
    except Exception as e:
        logging.error(f"Error en procesamiento de balance completo: {e}")
        raise

def procesar_datos_balance(df):
    """
    Procesa los datos de balance
    """
    # Copiar dataframe original
    df_procesado = df.copy()
    
    # Normalizar nombres de columnas
    df_procesado.columns = df_procesado.columns.str.strip().str.upper()
    
    # Procesar columnas de texto
    columnas_texto = df_procesado.select_dtypes(include=['object']).columns
    for columna in columnas_texto:
        df_procesado[columna] = df_procesado[columna].apply(limpiar_texto)
    
    # Procesar columnas numéricas
    columnas_numericas = df_procesado.select_dtypes(include=[np.number]).columns
    for columna in columnas_numericas:
        df_procesado[columna] = pd.to_numeric(df_procesado[columna], errors='coerce')
    
    # Procesar fechas
    columnas_fecha = []
    for columna in df_procesado.columns:
        if any(palabra in columna.upper() for palabra in ['FECHA', 'DATE', 'FECHA_', 'DATE_']):
            columnas_fecha.append(columna)
    
    for columna in columnas_fecha:
        df_procesado[columna] = df_procesado[columna].apply(convertir_fecha)
    
    # Agregar columnas calculadas específicas de balance
    df_procesado = agregar_columnas_balance(df_procesado)
    
    # Ordenar por columnas relevantes
    columnas_orden = []
    for columna in ['CUENTA', 'FECHA', 'SALDO', 'ACTIVO', 'PASIVO']:
        if columna in df_procesado.columns:
            columnas_orden.append(columna)
    
    if columnas_orden:
        df_procesado = df_procesado.sort_values(columnas_orden)
    
    return df_procesado

def agregar_columnas_balance(df):
    """
    Agrega columnas calculadas específicas para balance
    """
    # Buscar columnas de saldo y balance
    columnas_saldo = []
    for columna in df.columns:
        if any(palabra in columna.upper() for palabra in ['SALDO', 'BALANCE', 'ACTIVO', 'PASIVO', 'PATRIMONIO']):
            columnas_saldo.append(columna)
    
    # Calcular totales y ratios financieros
    if columnas_saldo:
        for columna in columnas_saldo:
            if columna in df.columns:
                # Total del balance
                total_balance = df[columna].sum()
                df[f'TOTAL_{columna}'] = total_balance
                
                # Porcentaje del total
                df[f'PORCENTAJE_{columna}'] = df[columna] / total_balance * 100
                
                # Promedio del balance
                promedio_balance = df[columna].mean()
                df[f'PROMEDIO_{columna}'] = promedio_balance
    
    # Calcular ratios financieros si hay columnas de activo y pasivo
    if 'ACTIVO' in df.columns and 'PASIVO' in df.columns:
        df['RATIO_ACTIVO_PASIVO'] = df['ACTIVO'] / df['PASIVO'].replace(0, np.nan)
        df['RATIO_ACTIVO_PASIVO'] = df['RATIO_ACTIVO_PASIVO'].fillna(0)
    
    if 'ACTIVO' in df.columns and 'PATRIMONIO' in df.columns:
        df['RATIO_ACTIVO_PATRIMONIO'] = df['ACTIVO'] / df['PATRIMONIO'].replace(0, np.nan)
        df['RATIO_ACTIVO_PATRIMONIO'] = df['RATIO_ACTIVO_PATRIMONIO'].fillna(0)
    
    # Clasificación de cuentas
    if 'CUENTA' in df.columns:
        df['TIPO_CUENTA'] = df['CUENTA'].apply(clasificar_cuenta)
    
    # Agregar columnas de estado
    df['ESTADO_PROCESAMIENTO'] = 'PROCESADO'
    df['FECHA_PROCESAMIENTO'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['TIPO_PROCESAMIENTO'] = 'BALANCE_COMPLETO'
    
    # Agregar análisis temporal si hay fechas
    columnas_fecha = [col for col in df.columns if 'FECHA' in col.upper()]
    if columnas_fecha:
        for columna_fecha in columnas_fecha:
            if columna_fecha in df.columns:
                # Extraer año y mes
                df[f'ANIO_{columna_fecha}'] = pd.to_datetime(df[columna_fecha]).dt.year
                df[f'MES_{columna_fecha}'] = pd.to_datetime(df[columna_fecha]).dt.month
                df[f'TRIMESTRE_{columna_fecha}'] = pd.to_datetime(df[columna_fecha]).dt.quarter
    
    return df

def clasificar_cuenta(cuenta):
    """
    Clasifica las cuentas según su naturaleza
    """
    if pd.isna(cuenta):
        return "NO_CLASIFICADA"
    
    cuenta_str = str(cuenta).upper()
    
    # Clasificación de activos
    if any(palabra in cuenta_str for palabra in ['EFECTIVO', 'CASH', 'BANCO', 'BANK']):
        return "ACTIVO_CORRIENTE"
    elif any(palabra in cuenta_str for palabra in ['CUENTA', 'ACCOUNT', 'CLIENTE', 'CUSTOMER']):
        return "ACTIVO_CORRIENTE"
    elif any(palabra in cuenta_str for palabra in ['INVENTARIO', 'INVENTORY', 'MERCADERIA']):
        return "ACTIVO_CORRIENTE"
    elif any(palabra in cuenta_str for palabra in ['MAQUINARIA', 'EQUIPO', 'MACHINERY', 'EQUIPMENT']):
        return "ACTIVO_FIJO"
    elif any(palabra in cuenta_str for palabra in ['EDIFICIO', 'CONSTRUCCION', 'BUILDING']):
        return "ACTIVO_FIJO"
    
    # Clasificación de pasivos
    elif any(palabra in cuenta_str for palabra in ['PROVEEDOR', 'SUPPLIER', 'CUENTA_PAGAR']):
        return "PASIVO_CORRIENTE"
    elif any(palabra in cuenta_str for palabra in ['PRESTAMO', 'LOAN', 'DEUDA', 'DEBT']):
        return "PASIVO_LARGO_PLAZO"
    
    # Clasificación de patrimonio
    elif any(palabra in cuenta_str for palabra in ['CAPITAL', 'CAPITAL', 'UTILIDAD', 'PROFIT']):
        return "PATRIMONIO"
    
    else:
        return "NO_CLASIFICADA"

def crear_analisis_balance(df):
    """
    Crea análisis detallado del balance
    """
    analisis = {}
    
    # Estadísticas básicas
    columnas_balance = [col for col in df.columns if any(palabra in col.upper() for palabra in ['SALDO', 'BALANCE', 'ACTIVO', 'PASIVO', 'PATRIMONIO'])]
    
    if columnas_balance:
        for columna in columnas_balance:
            if columna in df.columns:
                analisis[f'estadisticas_{columna}'] = {
                    'total': df[columna].sum(),
                    'promedio': df[columna].mean(),
                    'mediana': df[columna].median(),
                    'maximo': df[columna].max(),
                    'minimo': df[columna].min(),
                    'desviacion_estandar': df[columna].std()
                }
    
    # Análisis por tipo de cuenta
    if 'TIPO_CUENTA' in df.columns:
        analisis['por_tipo_cuenta'] = df.groupby('TIPO_CUENTA').agg({
            col: ['sum', 'mean', 'count'] for col in columnas_balance if col in df.columns
        }).round(2)
    
    # Análisis temporal
    columnas_fecha = [col for col in df.columns if 'FECHA' in col.upper()]
    if columnas_fecha:
        for columna_fecha in columnas_fecha:
            if columna_fecha in df.columns:
                df_temp = df.copy()
                df_temp[columna_fecha] = pd.to_datetime(df_temp[columna_fecha])
                analisis[f'por_fecha_{columna_fecha}'] = df_temp.groupby(df_temp[columna_fecha].dt.to_period('M')).agg({
                    col: 'sum' for col in columnas_balance if col in df.columns
                }).round(2)
    
    return analisis

def main():
    """
    Función principal
    """
    if len(sys.argv) != 2:
        print("Uso: python procesador_balance_completo.py <ruta_archivo>")
        sys.exit(1)
    
    ruta_archivo = sys.argv[1]
    
    try:
        ruta_salida, resumen = procesar_balance_completo(ruta_archivo)
        print(f"Procesamiento completado exitosamente")
        print(f"Archivo de salida: {ruta_salida}")
        print(f"Resumen: {resumen}")
        
    except Exception as e:
        print(f"Error en procesamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 