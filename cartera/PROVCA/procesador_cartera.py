#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Cartera
Sistema de Procesamiento de Cartera - Grupo Planeta
Versión: 2.0.1
"""

import pandas as pd
import numpy as np
import os
import sys
import time
from datetime import datetime
from typing import Tuple, Dict, Any, List, Optional
from config import (
    TIPOS_PROCESAMIENTO, CONFIG_PROCESAMIENTO, DIRECTORIOS,
    obtener_timestamp, obtener_fecha_actual
)
from logger import crear_logger, log_funcion
from utilidades_cartera import UtilidadesCartera

# =============================================================================
# CLASE PRINCIPAL DEL PROCESADOR DE CARTERA
# =============================================================================

class ProcesadorCartera:
    """
    Clase principal para el procesamiento de archivos de cartera
    """
    
    def __init__(self):
        """Inicializa el procesador de cartera"""
        self.logger = crear_logger("ProcesadorCartera")
        self.utilidades = UtilidadesCartera()
        self.config_procesamiento = CONFIG_PROCESAMIENTO.get('cartera', {})
        self.logger.info("Procesador de cartera inicializado")
    
    @log_funcion
    def procesar_cartera(self, ruta_archivo: str) -> Tuple[str, Dict[str, Any]]:
        """
        Procesa archivo de cartera completo
        
        Args:
            ruta_archivo: Ruta del archivo a procesar
            
        Returns:
            Tuple[str, Dict]: (ruta_salida, resumen_procesamiento)
            
        Raises:
            Exception: Si hay error en el procesamiento
        """
        tiempo_inicio = time.time()
        
        try:
            self.logger.inicio_procesamiento("Cartera", ruta_archivo)
            
            # Validar archivo
            self.utilidades.validar_archivo(ruta_archivo)
            
            # Leer archivo
            df_original = self.utilidades.leer_archivo(ruta_archivo)
            self.logger.info(f"Archivo leído: {len(df_original)} registros")
            
            # Limpiar dataframe
            df_limpio = self.utilidades.limpiar_dataframe(df_original)
            self.logger.info(f"Dataframe limpiado: {len(df_limpio)} registros")
            
            # Procesar datos
            df_procesado = self._procesar_datos_cartera(df_limpio)
            
            # Generar archivo de salida
            nombre_salida = self.utilidades.generar_nombre_archivo_salida("cartera_procesada")
            ruta_salida = os.path.join(DIRECTORIOS['resultados'], nombre_salida)
            
            # Crear directorio si no existe
            self.utilidades.crear_directorio_si_no_existe(DIRECTORIOS['resultados'])
            
            # Guardar resultado
            self.utilidades.escribir_resultado(df_procesado, ruta_salida)
            
            # Crear resumen
            tiempo_procesamiento = time.time() - tiempo_inicio
            resumen = self._crear_resumen_completo(
                df_original, df_procesado, tiempo_procesamiento
            )
            
            self.logger.fin_procesamiento("Cartera", f"Archivo guardado: {ruta_salida}")
            self.logger.estadisticas_procesamiento(
                len(df_original), len(df_procesado), tiempo_procesamiento
            )
            
            return ruta_salida, resumen
            
        except Exception as e:
            self.logger.error_procesamiento("Cartera", e)
            raise
    
    def _procesar_datos_cartera(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Procesa los datos de cartera específicamente
        
        Args:
            df: DataFrame a procesar
            
        Returns:
            pd.DataFrame: DataFrame procesado
        """
        self.logger.info("Iniciando procesamiento específico de datos de cartera")
        
        # Copiar dataframe original
        df_procesado = df.copy()
        
        # Normalizar nombres de columnas
        df_procesado.columns = df_procesado.columns.str.strip().str.upper()
        
        # Procesar columnas de texto
        self._procesar_columnas_texto(df_procesado)
        
        # Procesar columnas numéricas
        self._procesar_columnas_numericas(df_procesado)
        
        # Procesar fechas
        self._procesar_columnas_fecha(df_procesado)
        
        # Agregar columnas calculadas
        df_procesado = self._agregar_columnas_calculadas(df_procesado)
        
        # Ordenar por columnas relevantes
        df_procesado = self._ordenar_dataframe(df_procesado)
        
        # Validar datos procesados
        self._validar_datos_procesados(df_procesado)
        
        self.logger.info(f"Procesamiento de datos completado: {len(df_procesado)} registros")
        return df_procesado
    
    def _procesar_columnas_texto(self, df: pd.DataFrame) -> None:
        """Procesa columnas de texto"""
        columnas_texto = df.select_dtypes(include=['object']).columns
        for columna in columnas_texto:
            df[columna] = df[columna].apply(self.utilidades.limpiar_texto)
        
        self.logger.info(f"Procesadas {len(columnas_texto)} columnas de texto")
    
    def _procesar_columnas_numericas(self, df: pd.DataFrame) -> None:
        """Procesa columnas numéricas"""
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
        for columna in columnas_numericas:
            df[columna] = pd.to_numeric(df[columna], errors='coerce')
        
        self.logger.info(f"Procesadas {len(columnas_numericas)} columnas numéricas")
    
    def _procesar_columnas_fecha(self, df: pd.DataFrame) -> None:
        """Procesa columnas de fecha"""
        columnas_fecha = []
        for columna in df.columns:
            if any(palabra in columna.upper() for palabra in ['FECHA', 'DATE', 'FECHA_', 'DATE_']):
                columnas_fecha.append(columna)
        
        for columna in columnas_fecha:
            df[columna] = df[columna].apply(self.utilidades.convertir_fecha)
        
        self.logger.info(f"Procesadas {len(columnas_fecha)} columnas de fecha")
    
    def _agregar_columnas_calculadas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agrega columnas calculadas al dataframe
        
        Args:
            df: DataFrame al que agregar columnas
            
        Returns:
            pd.DataFrame: DataFrame con columnas calculadas
        """
        # Buscar columnas de monto
        columnas_monto = []
        for columna in df.columns:
            if any(palabra in columna.upper() for palabra in ['MONTO', 'SALDO', 'VALOR', 'AMOUNT', 'BALANCE']):
                columnas_monto.append(columna)
        
        # Calcular totales si hay columnas de monto
        if columnas_monto:
            for columna in columnas_monto:
                if columna in df.columns and df[columna].dtype in ['float64', 'int64']:
                    total = df[columna].sum()
                    if total != 0:
                        df[f'TOTAL_{columna}'] = total
                        df[f'PORCENTAJE_{columna}'] = df[columna] / total * 100
        
        # Agregar columnas de estado
        df['ESTADO_PROCESAMIENTO'] = 'PROCESADO'
        df['FECHA_PROCESAMIENTO'] = obtener_fecha_actual()
        df['TIPO_PROCESAMIENTO'] = 'CARTERA'
        
        # Agregar columnas de auditoría
        df['USUARIO_PROCESAMIENTO'] = 'SISTEMA'
        df['VERSION_PROCESAMIENTO'] = '2.0.1'
        
        self.logger.info(f"Agregadas columnas calculadas: {len(columnas_monto)} columnas de monto")
        return df
    
    def _ordenar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ordena el dataframe por columnas relevantes
        
        Args:
            df: DataFrame a ordenar
            
        Returns:
            pd.DataFrame: DataFrame ordenado
        """
        columnas_orden = self.config_procesamiento.get('orden_por_defecto', [])
        columnas_disponibles = [col for col in columnas_orden if col in df.columns]
        
        if columnas_disponibles:
            df = df.sort_values(columnas_disponibles)
            self.logger.info(f"DataFrame ordenado por: {', '.join(columnas_disponibles)}")
        
        return df
    
    def _validar_datos_procesados(self, df: pd.DataFrame) -> None:
        """
        Valida que los datos procesados sean correctos
        
        Args:
            df: DataFrame a validar
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        # Validar que no esté vacío
        if df.empty:
            raise ValueError("DataFrame procesado está vacío")
        
        # Validar columnas requeridas si están definidas
        columnas_requeridas = self.config_procesamiento.get('columnas_requeridas', [])
        if columnas_requeridas:
            self.utilidades.validar_columnas_requeridas(df, columnas_requeridas)
        
        # Validar que haya al menos una columna de monto
        columnas_monto = [col for col in df.columns if any(palabra in col.upper() 
                          for palabra in ['MONTO', 'SALDO', 'VALOR', 'AMOUNT', 'BALANCE'])]
        
        if not columnas_monto:
            self.logger.warning("No se encontraron columnas de monto en el DataFrame")
        
        self.logger.info("Validación de datos procesados completada")
    
    def _crear_resumen_completo(self, df_original: pd.DataFrame, 
                               df_procesado: pd.DataFrame, 
                               tiempo_procesamiento: float) -> Dict[str, Any]:
        """
        Crea un resumen completo del procesamiento
        
        Args:
            df_original: DataFrame original
            df_procesado: DataFrame procesado
            tiempo_procesamiento: Tiempo de procesamiento en segundos
            
        Returns:
            Dict: Resumen completo del procesamiento
        """
        resumen_base = self.utilidades.crear_resumen_procesamiento(
            df_original, df_procesado, "Cartera"
        )
        
        # Agregar estadísticas adicionales
        estadisticas = self.utilidades.generar_estadisticas_dataframe(df_procesado)
        
        resumen_completo = {
            **resumen_base,
            'tiempo_procesamiento_segundos': tiempo_procesamiento,
            'tiempo_procesamiento_formateado': f"{tiempo_procesamiento:.2f}s",
            'estadisticas_detalladas': estadisticas,
            'configuracion_usada': self.config_procesamiento,
            'version_procesador': '2.0.1',
            'fecha_procesamiento_timestamp': obtener_timestamp()
        }
        
        return resumen_completo
    
    def generar_reporte_estadisticas(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Genera un reporte detallado de estadísticas
        
        Args:
            df: DataFrame a analizar
            
        Returns:
            Dict: Reporte de estadísticas
        """
        reporte = {
            'fecha_generacion': obtener_fecha_actual(),
            'total_registros': len(df),
            'total_columnas': len(df.columns),
            'columnas_por_tipo': {
                'numericas': len(df.select_dtypes(include=[np.number]).columns),
                'texto': len(df.select_dtypes(include=['object']).columns),
                'fecha': len(df.select_dtypes(include=['datetime']).columns)
            },
            'valores_nulos': df.isnull().sum().to_dict(),
            'porcentaje_nulos': (df.isnull().sum() / len(df) * 100).to_dict()
        }
        
        # Estadísticas de columnas numéricas
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
        if len(columnas_numericas) > 0:
            reporte['estadisticas_numericas'] = df[columnas_numericas].describe().to_dict()
        
        return reporte

# =============================================================================
# FUNCIÓN PRINCIPAL Y FUNCIONES DE CONVENIENCIA
# =============================================================================

def procesar_cartera(ruta_archivo: str) -> Tuple[str, Dict[str, Any]]:
    """
    Función de conveniencia para procesar cartera
    
    Args:
        ruta_archivo: Ruta del archivo a procesar
        
    Returns:
        Tuple[str, Dict]: (ruta_salida, resumen_procesamiento)
    """
    procesador = ProcesadorCartera()
    return procesador.procesar_cartera(ruta_archivo)

def procesar_datos_cartera(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función de conveniencia para procesar datos de cartera
    
    Args:
        df: DataFrame a procesar
        
    Returns:
        pd.DataFrame: DataFrame procesado
    """
    procesador = ProcesadorCartera()
    return procesador._procesar_datos_cartera(df)

def agregar_columnas_calculadas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función de conveniencia para agregar columnas calculadas
    
    Args:
        df: DataFrame al que agregar columnas
        
    Returns:
        pd.DataFrame: DataFrame con columnas calculadas
    """
    procesador = ProcesadorCartera()
    return procesador._agregar_columnas_calculadas(df)

# =============================================================================
# FUNCIÓN MAIN
# =============================================================================

def main():
    """
    Función principal para ejecución desde línea de comandos
    """
    if len(sys.argv) != 2:
        print("Uso: python procesador_cartera.py <ruta_archivo>")
        print("Ejemplo: python procesador_cartera.py datos_cartera.xlsx")
        sys.exit(1)
    
    ruta_archivo = sys.argv[1]
    
    try:
        print("=" * 60)
        print("PROCESADOR DE CARTERA - GRUPO PLANETA")
        print("Versión: 2.0.1")
        print("=" * 60)
        
        ruta_salida, resumen = procesar_cartera(ruta_archivo)
        
        print("\n✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
        print(f"📁 Archivo de salida: {ruta_salida}")
        print(f"📊 Registros procesados: {resumen['registros_procesados']}")
        print(f"⏱️  Tiempo de procesamiento: {resumen['tiempo_procesamiento_formateado']}")
        print(f"📈 Reducción de registros: {resumen['reduccion_registros']}")
        print(f"📉 Porcentaje de reducción: {resumen['porcentaje_reduccion']:.2f}%")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR EN PROCESAMIENTO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 