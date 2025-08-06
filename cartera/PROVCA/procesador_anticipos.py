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

class ProcesadorAnticipos:
    def __init__(self):
        self.logger = crear_logger("ProcesadorAnticipos")
        self.utilidades = UtilidadesCartera()
    
    @log_funcion
    def procesar_anticipos(self, ruta_archivo: str) -> Tuple[str, Dict[str, Any]]:
        """
        Procesa archivo de anticipos
        """
        try:
            self.logger.info(f"Iniciando procesamiento de anticipos: {ruta_archivo}")
            
            # Validar archivo
            self.utilidades.validar_archivo(ruta_archivo)
            
            # Leer archivo
            df = self.utilidades.leer_archivo(ruta_archivo)
            self.logger.info(f"Archivo leído: {len(df)} registros")
            
            # Limpiar dataframe
            df = self.utilidades.limpiar_dataframe(df)
            self.logger.info(f"Dataframe limpiado: {len(df)} registros")
            
            # Procesar datos
            df_procesado = self.procesar_datos_anticipos(df)
            
            # Generar archivo de salida
            nombre_salida = self.utilidades.generar_nombre_archivo_salida("anticipos_procesados")
            ruta_salida = self.utilidades.obtener_ruta_resultado(nombre_salida)
            
            # Guardar resultado
            self.utilidades.escribir_resultado(df_procesado, ruta_salida)
            
            # Crear resumen
            resumen = self.utilidades.crear_resumen_procesamiento(df, df_procesado, "Anticipos")
            
            self.logger.info("Procesamiento de anticipos completado exitosamente")
            return ruta_salida, resumen
            
        except Exception as e:
            self.logger.error(f"Error en procesamiento de anticipos: {e}")
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

def main():
    """
    Función principal para ejecución directa
    """
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='Procesador de Anticipos')
    parser.add_argument('archivo', help='Ruta del archivo a procesar')
    parser.add_argument('--output', '-o', help='Archivo de salida (opcional)')
    
    args = parser.parse_args()
    
    try:
        procesador = ProcesadorAnticipos()
        ruta_salida, resumen = procesador.procesar_anticipos(args.archivo)
        
        print(f"✅ Procesamiento completado exitosamente")
        print(f"📁 Archivo de salida: {ruta_salida}")
        print(f"📊 Resumen: {resumen}")
        
    except Exception as e:
        print(f"❌ Error en el procesamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 