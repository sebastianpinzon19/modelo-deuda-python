#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Formato Deuda
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

class ProcesadorFormatoDeuda:
    def __init__(self):
        self.logger = crear_logger("ProcesadorFormatoDeuda")
        self.utilidades = UtilidadesCartera()
    
    @log_funcion
    def procesar_formato_deuda(self, ruta_archivo: str) -> Tuple[str, Dict[str, Any]]:
        """
        Procesa archivo de formato deuda (procesador principal)
        """
        try:
            self.logger.info(f"Iniciando procesamiento de formato deuda: {ruta_archivo}")
            
            # Validar archivo
            self.utilidades.validar_archivo(ruta_archivo)
            
            # Leer archivo
            df = self.utilidades.leer_archivo(ruta_archivo)
            self.logger.info(f"Archivo leído: {len(df)} registros")
            
            # Limpiar dataframe
            df = self.utilidades.limpiar_dataframe(df)
            self.logger.info(f"Dataframe limpiado: {len(df)} registros")
            
            # Procesar datos
            df_procesado = self.procesar_datos_formato_deuda(df)
            
            # Generar archivo de salida
            nombre_salida = self.utilidades.generar_nombre_archivo_salida("formato_deuda_procesado")
            ruta_salida = self.utilidades.obtener_ruta_resultado(nombre_salida)
            
            # Guardar resultado
            self.utilidades.escribir_resultado(df_procesado, ruta_salida)
            
            # Crear resumen
            resumen = self.utilidades.crear_resumen_procesamiento(df, df_procesado, "Formato Deuda")
            
            self.logger.info("Procesamiento de formato deuda completado exitosamente")
            return ruta_salida, resumen
            
        except Exception as e:
            self.logger.error(f"Error en procesamiento de formato deuda: {e}")
            raise

    @log_funcion
    def procesar_datos_formato_deuda(self, df) -> Any:
        """
        Procesa los datos de formato deuda
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
        
        # Agregar columnas calculadas específicas de formato deuda
        df_procesado = self.agregar_columnas_formato_deuda(df_procesado)
        
        # Ordenar por columnas relevantes
        columnas_orden = []
        for columna in ['CLIENTE', 'CUENTA', 'FECHA_VENCIMIENTO', 'SALDO_DEUDA']:
            if columna in df_procesado.columns:
                columnas_orden.append(columna)
        
        if columnas_orden:
            df_procesado = df_procesado.sort_values(columnas_orden)
        
        return df_procesado

    @log_funcion
    def agregar_columnas_formato_deuda(self, df) -> Any:
        """
        Agrega columnas calculadas específicas para formato deuda
        """
        import pandas as pd
        import numpy as np
        
        # Agregar columnas de análisis
        if 'SALDO_DEUDA' in df.columns:
            df['SALDO_DEUDA_NUM'] = pd.to_numeric(df['SALDO_DEUDA'], errors='coerce')
            df['DEUDA_VENCIDA'] = df['SALDO_DEUDA_NUM'].apply(lambda x: x if x > 0 else 0)
        
        if 'FECHA_VENCIMIENTO' in df.columns:
            df['DIAS_VENCIDO'] = df['FECHA_VENCIMIENTO'].apply(
                lambda x: (pd.Timestamp.now() - pd.to_datetime(x)).days if pd.notna(x) else 0
            )
            df['ESTADO_VENCIMIENTO'] = df['DIAS_VENCIDO'].apply(
                lambda x: 'VENCIDO' if x > 0 else 'AL_DIA'
            )
        
        # Agregar columnas de clasificación
        if 'SALDO_DEUDA_NUM' in df.columns:
            df['CLASIFICACION_DEUDA'] = df['SALDO_DEUDA_NUM'].apply(
                lambda x: 'ALTA' if x > 100000 else 'MEDIA' if x > 10000 else 'BAJA'
            )
        
        return df

    @log_funcion
    def crear_analisis_formato_deuda(self, df) -> Dict[str, Any]:
        """
        Crea análisis detallado del formato deuda
        """
        analisis = {
            'total_registros': len(df),
            'total_deuda': 0,
            'deuda_vencida': 0,
            'clientes_unicos': 0,
            'cuentas_unicas': 0
        }
        
        if 'SALDO_DEUDA_NUM' in df.columns:
            analisis['total_deuda'] = df['SALDO_DEUDA_NUM'].sum()
            analisis['deuda_vencida'] = df[df['DIAS_VENCIDO'] > 0]['SALDO_DEUDA_NUM'].sum()
        
        if 'CLIENTE' in df.columns:
            analisis['clientes_unicos'] = df['CLIENTE'].nunique()
        
        if 'CUENTA' in df.columns:
            analisis['cuentas_unicas'] = df['CUENTA'].nunique()
        
        return analisis

def main():
    """
    Función principal para ejecución directa
    """
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='Procesador de Formato Deuda')
    parser.add_argument('archivo', help='Ruta del archivo a procesar')
    parser.add_argument('--output', '-o', help='Archivo de salida (opcional)')
    
    args = parser.parse_args()
    
    try:
        procesador = ProcesadorFormatoDeuda()
        ruta_salida, resumen = procesador.procesar_formato_deuda(args.archivo)
        
        print(f"✅ Procesamiento completado exitosamente")
        print(f"📁 Archivo de salida: {ruta_salida}")
        print(f"📊 Resumen: {resumen}")
        
    except Exception as e:
        print(f"❌ Error en el procesamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 