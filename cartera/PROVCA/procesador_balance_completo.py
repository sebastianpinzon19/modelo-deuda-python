#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Balance Completo
Sistema de Procesamiento de Cartera - Grupo Planeta
"""

import pandas as pd
import numpy as np
import sys
from datetime import datetime
from utilidades_cartera import UtilidadesCartera

def procesar_balance_completo(ruta_archivo):
    """
    Procesa archivo de balance completo según reglas de negocio (solo cuentas y sumas requeridas).
    """
    util = UtilidadesCartera()
    try:
        util.validar_archivo(ruta_archivo)
        df = util.leer_archivo(ruta_archivo)
        df = util.limpiar_dataframe(df)
        df.columns = df.columns.str.strip().str.upper()
        # Filtrar cuentas requeridas y sumar columna 'SALDO AAF VARIACION'
        cuentas_objeto = [
            '43001', '0080.43002.20', '0080.43002.21', '0080.43002.15', '0080.43002.28',
            '0080.43002.31', '0080.43002.63', '43008', '43042'
        ]
        col_cuenta = next((c for c in df.columns if 'CUENTA' in c), None)
        col_saldo = next((c for c in df.columns if 'SALDO AAF VARIACION' in c), None)
        if not col_cuenta or not col_saldo:
            raise Exception('No se encontraron columnas de cuenta o saldo requeridas')
        resumen = {}
        for cuenta in cuentas_objeto:
            mask = df[col_cuenta].astype(str).str.strip() == cuenta
            total = df.loc[mask, col_saldo].sum()
            resumen[cuenta] = total
        df_resumen = pd.DataFrame(list(resumen.items()), columns=['CUENTA_OBJETO','TOTAL_SALDO_AAF_VARIACION'])
        # Guardar resultado
        nombre_salida = util.generar_nombre_archivo_salida("balance_completo_procesado")
        ruta_salida = util.obtener_ruta_resultado(nombre_salida)
        util.escribir_resultado(df_resumen, ruta_salida)
        return ruta_salida, resumen
    except Exception as e:
        print(f"Error en procesamiento de balance completo: {e}")
        raise

def procesar_datos_balance(df):
    """
    Procesa los datos de balance
    """
    # Copiar dataframe original
    df_procesado = df.copy()
    df_procesado.columns = df_procesado.columns.str.strip().str.upper()
    # Limpiar texto
    columnas_texto = df_procesado.select_dtypes(include=['object']).columns
    for columna in columnas_texto:
        df_procesado[columna] = df_procesado[columna].apply(limpiar_texto)
    
    def limpiar_texto(valor):
        """
        Limpia y normaliza texto eliminando espacios y convirtiendo a mayúsculas.
        """
        if pd.isna(valor):
            return valor
        return str(valor).strip().upper()
    # Convertir numéricos
    for columna in df_procesado.columns:
        df_procesado[columna] = pd.to_numeric(df_procesado[columna], errors='ignore')
    # Filtrar cuentas requeridas
    cuentas_objeto = [
        '43001', '0080.43002.20', '0080.43002.21', '0080.43002.15', '0080.43002.28',
        '0080.43002.31', '0080.43002.63', '43008', '43042'
    ]
    # Buscar columna de cuenta y saldo
    col_cuenta = next((c for c in df_procesado.columns if 'CUENTA' in c), None)
    col_saldo = next((c for c in df_procesado.columns if 'SALDO AAF VARIACION' in c), None)
    if not col_cuenta or not col_saldo:
        raise Exception('No se encontraron columnas de cuenta o saldo requeridas')
    # Filtrar y sumar
    resumen = {}
    for cuenta in cuentas_objeto:
        mask = df_procesado[col_cuenta].astype(str).str.strip() == cuenta
        total = df_procesado.loc[mask, col_saldo].sum()
        resumen[cuenta] = total
    # Crear dataframe resumen
    df_resumen = pd.DataFrame(list(resumen.items()), columns=['CUENTA_OBJETO','TOTAL_SALDO_AAF_VARIACION'])
    # Estructura de salida
    return df_resumen

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

def menu():
    print("\n=== Procesador de Balance Completo ===")
    print("1. Procesar archivo de balance completo")
    print("0. Salir")
    while True:
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo de balance: ")
            try:
                ruta_salida, resumen = procesar_balance_completo(ruta)
                print(f"Procesamiento completado exitosamente\nArchivo de salida: {ruta_salida}\nResumen: {resumen}")
            except Exception as e:
                print(f"Error: {e}")
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()