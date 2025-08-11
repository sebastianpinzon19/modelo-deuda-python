import pandas as pd
from utilidades_cartera import UtilidadesCartera

def procesar_datos_anticipos(df):
    """
    Procesa los datos de anticipos (versión global para scripts)
    """
    utilidades = UtilidadesCartera()
    # Copiar dataframe original
    df_procesado = df.copy()
    # Normalizar nombres de columnas
    df_procesado.columns = df_procesado.columns.str.strip().str.upper()
    # Procesar columnas de texto
    columnas_texto = df_procesado.select_dtypes(include=['object']).columns
    for columna in columnas_texto:
        df_procesado[columna] = df_procesado[columna].apply(utilidades.limpiar_texto)
    # Procesar columnas numéricas
    columnas_numericas = df_procesado.select_dtypes(include=['numpy.number']).columns
    for columna in columnas_numericas:
        df_procesado[columna] = pd.to_numeric(df_procesado[columna], errors='coerce')
    # Procesar fechas
    columnas_fecha = []
    for columna in df_procesado.columns:
        if any(palabra in columna.upper() for palabra in ['FECHA', 'DATE', 'FECHA_', 'DATE_']):
            columnas_fecha.append(columna)
    for columna in columnas_fecha:
        df_procesado[columna] = df_procesado[columna].apply(utilidades.convertir_fecha)
    # Agregar columnas calculadas específicas de anticipos
    # Reutiliza la lógica del método de clase, pero aquí directamente
    if 'MONTO_ANTICIPO' in df_procesado.columns:
        df_procesado['MONTO_ANTICIPO_NUM'] = pd.to_numeric(df_procesado['MONTO_ANTICIPO'], errors='coerce')
        df_procesado['ANTICIPO_VALIDO'] = df_procesado['MONTO_ANTICIPO_NUM'].apply(lambda x: x > 0 if pd.notna(x) else False)
    if 'FECHA_ANTICIPO' in df_procesado.columns:
        df_procesado['DIAS_DESDE_ANTICIPO'] = df_procesado['FECHA_ANTICIPO'].apply(
            lambda x: (pd.Timestamp.now() - pd.to_datetime(x)).days if pd.notna(x) else 0
        )
        df_procesado['ESTADO_ANTICIPO'] = df_procesado['DIAS_DESDE_ANTICIPO'].apply(
            lambda x: 'RECIENTE' if x <= 30 else 'MEDIO_PLAZO' if x <= 90 else 'LARGO_PLAZO'
        )
    if 'MONTO_ANTICIPO_NUM' in df_procesado.columns:
        df_procesado['CLASIFICACION_ANTICIPO'] = df_procesado['MONTO_ANTICIPO_NUM'].apply(
            lambda x: 'ALTO' if x > 50000 else 'MEDIO' if x > 10000 else 'BAJO'
        )
    # Ordenar por columnas relevantes
    columnas_orden = []
    for columna in ['CLIENTE', 'FECHA_ANTICIPO', 'MONTO_ANTICIPO']:
        if columna in df_procesado.columns:
            columnas_orden.append(columna)
    if columnas_orden:
        df_procesado = df_procesado.sort_values(columnas_orden)
    return df_procesado
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Anticipos
Sistema de Procesamiento de Cartera - Grupo Planeta
Versión: 2.0.1
"""

import time
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List, Optional, Union
from config import (
    TIPOS_PROCESAMIENTO, CONFIG_PROCESAMIENTO, DIRECTORIOS,
    obtener_timestamp, obtener_fecha_actual
)
from logger import crear_logger, log_funcion
from utilidades_cartera import UtilidadesCartera

def procesar_anticipos(ruta_archivo):
    """
    Procesa archivo de anticipos según reglas de negocio:
    - Renombra columnas
    - Multiplica valor anticipo por -1
    """
    util = UtilidadesCartera()
    try:
        util.validar_archivo(ruta_archivo)
        df = util.leer_archivo(ruta_archivo)
        df = util.limpiar_dataframe(df)
        df.columns = df.columns.str.strip().str.upper()
        # Renombrar columnas según reglas
        renombres = {
            'NCCDEM': 'EMPRESA', 'NCCDAC': 'ACTIVIDAD', 'NCCDCL': 'CODIGO CLIENTE',
            'WWNIT': 'NIT/CEDULA', 'WWNMCL': 'NOMBRE COMERCIAL', 'WWNMDO': 'DIRECCION',
            'WWTLF1': 'TELEFONO', 'WWNMPO': 'POBLACION', 'CCCDFB': 'CODIGO AGENTE',
            'BDNMNM': 'NOMBRE AGENTE', 'BDNMPA': 'APELLIDO AGENTE', 'NCMOMO': 'TIPO ANTICIPO',
            'NCCDR3': 'NRO ANTICIPO', 'NCIMAN': 'VALOR ANTICIPO', 'NCFEGR': 'FECHA ANTICIPO'
        }
        df = df.rename(columns=renombres)
        # Multiplicar valor anticipo por -1
        if 'VALOR ANTICIPO' in df.columns:
            df['VALOR ANTICIPO'] = pd.to_numeric(df['VALOR ANTICIPO'], errors='coerce') * -1
        # Guardar resultado
        nombre_salida = util.generar_nombre_archivo_salida("anticipos_procesados")
        ruta_salida = util.obtener_ruta_resultado(nombre_salida)
        util.escribir_resultado(df, ruta_salida)
        resumen = {'registros': len(df), 'archivo': ruta_salida}
        return ruta_salida, resumen
    except Exception as e:
        print(f"Error en procesamiento de anticipos: {e}")
        raise

    @log_funcion
    def procesar_datos_anticipos(self, df) -> Any:
        """
        Procesa los datos de anticipos
        """
        # Copiar dataframe original
        df_procesado = df.copy()
        
        # Normalizar nombres de columnas
        df_procesado.columns = df_procesado.columns.str.strip().str.upper()
        
        # Procesar columnas de texto
        columnas_texto = df_procesado.select_dtypes(include=['object']).columns
        for columna in columnas_texto:
            df_procesado[columna] = df_procesado[columna].apply(self.utilidades.limpiar_texto)
        
        # Procesar columnas numéricas
        columnas_numericas = df_procesado.select_dtypes(include=['numpy.number']).columns
        for columna in columnas_numericas:
            df_procesado[columna] = pd.to_numeric(df_procesado[columna], errors='coerce')
        
        # Procesar fechas
        columnas_fecha = []
        for columna in df_procesado.columns:
            if any(palabra in columna.upper() for palabra in ['FECHA', 'DATE', 'FECHA_', 'DATE_']):
                columnas_fecha.append(columna)
        
        for columna in columnas_fecha:
            df_procesado[columna] = df_procesado[columna].apply(self.utilidades.convertir_fecha)
        
        # Agregar columnas calculadas específicas de anticipos
        df_procesado = self.agregar_columnas_anticipos(df_procesado)
        
        # Ordenar por columnas relevantes
        columnas_orden = []
        for columna in ['CLIENTE', 'FECHA_ANTICIPO', 'MONTO_ANTICIPO']:
            if columna in df_procesado.columns:
                columnas_orden.append(columna)
        
        if columnas_orden:
            df_procesado = df_procesado.sort_values(columnas_orden)
        
        return df_procesado

    @log_funcion
    def agregar_columnas_anticipos(self, df) -> Any:
        """
        Agrega columnas calculadas específicas para anticipos
        """
        # Agregar columnas de análisis
        if 'MONTO_ANTICIPO' in df.columns:
            df['MONTO_ANTICIPO_NUM'] = pd.to_numeric(df['MONTO_ANTICIPO'], errors='coerce')
            df['ANTICIPO_VALIDO'] = df['MONTO_ANTICIPO_NUM'].apply(lambda x: x > 0 if pd.notna(x) else False)
        
        if 'FECHA_ANTICIPO' in df.columns:
            df['DIAS_DESDE_ANTICIPO'] = df['FECHA_ANTICIPO'].apply(
                lambda x: (pd.Timestamp.now() - pd.to_datetime(x)).days if pd.notna(x) else 0
            )
            df['ESTADO_ANTICIPO'] = df['DIAS_DESDE_ANTICIPO'].apply(
                lambda x: 'RECIENTE' if x <= 30 else 'MEDIO_PLAZO' if x <= 90 else 'LARGO_PLAZO'
            )
        
        # Agregar columnas de clasificación
        if 'MONTO_ANTICIPO_NUM' in df.columns:
            df['CLASIFICACION_ANTICIPO'] = df['MONTO_ANTICIPO_NUM'].apply(
                lambda x: 'ALTO' if x > 50000 else 'MEDIO' if x > 10000 else 'BAJO'
            )
        
        return df

    @log_funcion
    def crear_analisis_anticipos(self, df) -> Dict[str, Any]:
        """
        Crea análisis detallado de anticipos
        """
        analisis = {
            'total_registros': len(df),
            'total_anticipos': 0,
            'anticipos_validos': 0,
            'clientes_unicos': 0,
            'promedio_anticipo': 0
        }
        
        if 'MONTO_ANTICIPO_NUM' in df.columns:
            analisis['total_anticipos'] = df['MONTO_ANTICIPO_NUM'].sum()
            analisis['anticipos_validos'] = df[df['ANTICIPO_VALIDO']]['MONTO_ANTICIPO_NUM'].sum()
            analisis['promedio_anticipo'] = df['MONTO_ANTICIPO_NUM'].mean()
        
        if 'CLIENTE' in df.columns:
            analisis['clientes_unicos'] = df['CLIENTE'].nunique()
        
        return analisis

def menu():
    print("\n=== Procesador de Anticipos ===")
    print("1. Procesar archivo de anticipos")
    print("0. Salir")
    while True:
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo de anticipos: ")
            try:
                ruta_salida, resumen = procesar_anticipos(ruta)
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