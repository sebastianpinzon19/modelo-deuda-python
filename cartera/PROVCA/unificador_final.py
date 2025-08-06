#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unificador Final
Sistema de Procesamiento de Cartera - Grupo Planeta
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import logging
from utilidades_cartera import *

def unificar_resultados():
    """
    Une todos los resultados de los procesadores en un archivo Excel final
    """
    try:
        logging.info("Iniciando unificación de resultados")
        
        # Crear directorio de resultados si no existe
        crear_directorio_si_no_existe("resultados")
        
        # Buscar todos los archivos procesados
        archivos_procesados = buscar_archivos_procesados()
        
        if not archivos_procesados:
            raise ValueError("No se encontraron archivos procesados para unificar")
        
        # Leer y organizar resultados
        resultados_organizados = leer_y_organizar_resultados(archivos_procesados)
        
        # Generar archivo Excel final
        nombre_salida = generar_nombre_archivo_salida("reporte_final_unificado")
        ruta_salida = os.path.join("resultados", nombre_salida)
        
        # Crear Excel con hojas separadas
        crear_excel_final(resultados_organizados, ruta_salida)
        
        logging.info("Unificación completada exitosamente")
        return ruta_salida, resultados_organizados
        
    except Exception as e:
        logging.error(f"Error en unificación: {e}")
        raise

def buscar_archivos_procesados():
    """
    Busca todos los archivos procesados en el directorio resultados
    """
    archivos = {}
    
    if not os.path.exists("resultados"):
        return archivos
    
    for archivo in os.listdir("resultados"):
        if archivo.endswith(('.xlsx', '.csv')) and 'procesado' in archivo.lower():
            tipo_procesamiento = extraer_tipo_procesamiento(archivo)
            if tipo_procesamiento:
                archivos[tipo_procesamiento] = os.path.join("resultados", archivo)
    
    logging.info(f"Archivos procesados encontrados: {list(archivos.keys())}")
    return archivos

def extraer_tipo_procesamiento(nombre_archivo):
    """
    Extrae el tipo de procesamiento del nombre del archivo
    """
    nombre_lower = nombre_archivo.lower()
    
    if 'balance' in nombre_lower:
        return 'BALANCE'
    elif 'situacion' in nombre_lower:
        return 'SITUACION'
    elif 'focus' in nombre_lower:
        return 'FOCUS'
    elif 'dotacion' in nombre_lower:
        return 'DOTACION_MES'
    elif 'acumulado' in nombre_lower:
        return 'ACUMULADO'
    elif 'tipos_cambio' in nombre_lower or 'cambio' in nombre_lower:
        return 'TIPOS_CAMBIO'
    elif 'anticipos' in nombre_lower:
        return 'ANTICIPOS'
    elif 'cartera' in nombre_lower:
        return 'CARTERA'
    else:
        return None

def leer_y_organizar_resultados(archivos_procesados):
    """
    Lee y organiza todos los resultados
    """
    resultados_organizados = {}
    
    for tipo_procesamiento, ruta_archivo in archivos_procesados.items():
        try:
            df = leer_archivo(ruta_archivo)
            resultados_organizados[tipo_procesamiento] = df
            logging.info(f"Resultado {tipo_procesamiento} cargado: {len(df)} registros")
        except Exception as e:
            logging.error(f"Error al cargar {tipo_procesamiento}: {e}")
            # Crear DataFrame vacío como fallback
            resultados_organizados[tipo_procesamiento] = pd.DataFrame({
                'Concepto': ['Error_Carga'],
                'Valor': [0],
                'Fecha_Procesamiento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Tipo_Procesamiento': tipo_procesamiento
            })
    
    return resultados_organizados

def crear_excel_final(resultados_organizados, ruta_salida):
    """
    Crea el archivo Excel final con hojas separadas
    """
    with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
        
        # Crear hoja de resumen
        crear_hoja_resumen(resultados_organizados, writer)
        
        # Crear hojas individuales para cada procesamiento
        for tipo_procesamiento, df in resultados_organizados.items():
            nombre_hoja = tipo_procesamiento.replace('_', ' ').title()
            # Limitar nombre de hoja a 31 caracteres (límite de Excel)
            if len(nombre_hoja) > 31:
                nombre_hoja = nombre_hoja[:31]
            
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)
            logging.info(f"Hoja '{nombre_hoja}' creada con {len(df)} registros")
        
        # Crear hoja de fórmulas y cálculos
        crear_hoja_formulas(resultados_organizados, writer)
    
    logging.info(f"Archivo Excel final creado: {ruta_salida}")

def crear_hoja_resumen(resultados_organizados, writer):
    """
    Crea hoja de resumen con estadísticas generales
    """
    resumen_data = []
    
    for tipo_procesamiento, df in resultados_organizados.items():
        if not df.empty:
            # Calcular estadísticas básicas
            total_registros = len(df)
            total_valor = df['Valor'].sum() if 'Valor' in df.columns else 0
            
            resumen_data.append({
                'Tipo_Procesamiento': tipo_procesamiento,
                'Total_Registros': total_registros,
                'Total_Valor': total_valor,
                'Fecha_Procesamiento': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    
    df_resumen = pd.DataFrame(resumen_data)
    df_resumen.to_excel(writer, sheet_name='RESUMEN', index=False)

def crear_hoja_formulas(resultados_organizados, writer):
    """
    Crea hoja con fórmulas y cálculos según las reglas de negocio
    """
    formulas_data = []
    
    # Aplicar fórmulas según las reglas específicas
    formulas_aplicadas = aplicar_formulas_negocio(resultados_organizados)
    
    for formula, resultado in formulas_aplicadas.items():
        formulas_data.append({
            'Formula': formula,
            'Resultado': resultado,
            'Fecha_Calculo': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    df_formulas = pd.DataFrame(formulas_data)
    df_formulas.to_excel(writer, sheet_name='FORMULAS', index=False)

def aplicar_formulas_negocio(resultados_organizados):
    """
    Aplica las fórmulas de negocio según las reglas específicas
    """
    formulas = {}
    
    # Obtener valores de los diferentes procesamientos
    balance_data = resultados_organizados.get('BALANCE', pd.DataFrame())
    situacion_data = resultados_organizados.get('SITUACION', pd.DataFrame())
    focus_data = resultados_organizados.get('FOCUS', pd.DataFrame())
    dotacion_data = resultados_organizados.get('DOTACION_MES', pd.DataFrame())
    acumulado_data = resultados_organizados.get('ACUMULADO', pd.DataFrame())
    
    # Fórmula 1: Deuda bruta NO Grupo (Inicial) = Deuda bruta NO Grupo (Final)
    if not balance_data.empty:
        total_balance = balance_data['Valor'].sum() if 'Valor' in balance_data.columns else 0
        formulas['Deuda_Bruta_NO_Grupo_Inicial'] = total_balance
        formulas['Deuda_Bruta_NO_Grupo_Final'] = total_balance
    
    # Fórmula 2: - Dotaciones Acumuladas (Inicial) = '+/- Provisión acumulada (Final)
    if not dotacion_data.empty:
        dotaciones_acumuladas = dotacion_data[dotacion_data['Concepto'].str.contains('Dotaciones_Acumuladas', na=False)]['Valor'].sum()
        formulas['Dotaciones_Acumuladas_Inicial'] = -dotaciones_acumuladas
        formulas['Provision_Acumulada_Final'] = dotaciones_acumuladas
    
    # Fórmula 3: Cobro de mes - Vencida
    if not focus_data.empty and not balance_data.empty:
        vencido_60_dias = focus_data[focus_data['Concepto'].str.contains('Vencido_60', na=False)]['Valor'].sum()
        deuda_bruta_vencidas = balance_data['Valor'].sum() * 0.1  # Estimación del 10%
        cobro_vencida = (deuda_bruta_vencidas - vencido_60_dias) / 1000
        formulas['Cobro_Mes_Vencida'] = cobro_vencida
    
    # Fórmula 4: Cobro mes - Total Deuda
    if not situacion_data.empty:
        cobros_situacion = situacion_data['Valor'].sum()
        cobro_total_deuda = cobros_situacion / -1000
        formulas['Cobro_Mes_Total_Deuda'] = cobro_total_deuda
    
    # Fórmula 5: Dotación del mes
    if not dotacion_data.empty:
        dotacion_mes = dotacion_data[dotacion_data['Concepto'].str.contains('Dotacion_Mes', na=False)]['Valor'].sum()
        formulas['Dotacion_Mes'] = dotacion_mes
    
    return formulas

def main():
    """
    Función principal
    """
    try:
        ruta_salida, resultados = unificar_resultados()
        print(f"Unificación completada exitosamente")
        print(f"Archivo de salida: {ruta_salida}")
        print(f"Procesamientos unificados: {list(resultados.keys())}")
        
    except Exception as e:
        print(f"Error en unificación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 