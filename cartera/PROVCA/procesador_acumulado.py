#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Acumulado
Sistema de Procesamiento de Cartera - Grupo Planeta
Versión: 2.0.1
"""

import pandas as pd
import numpy as np
import os
import sys
import time
from datetime import datetime
from typing import Tuple, Dict, Any, List, Optional, Union
from config import (
    TIPOS_PROCESAMIENTO, CONFIG_PROCESAMIENTO, DIRECTORIOS,
    obtener_timestamp, obtener_fecha_actual
)
from logger import crear_logger, log_funcion
from utilidades_cartera import UtilidadesCartera

# =============================================================================
# CLASE PRINCIPAL DEL PROCESADOR DE ACUMULADO
# =============================================================================

class ProcesadorAcumulado:
    """
    Clase principal para el procesamiento de archivos de acumulado
    """
    
    def __init__(self):
        """Inicializa el procesador de acumulado"""
        self.logger = crear_logger("ProcesadorAcumulado")
        self.utilidades = UtilidadesCartera()
        self.config_procesamiento = CONFIG_PROCESAMIENTO.get('acumulado', {})
        self.logger.info("Procesador de acumulado inicializado")
        
        # Configuración específica para acumulado
        self.config_acumulado = {
            'fila_objetivo': 54,  # Fila 54 (índice 53)
            'columnas_objetivo': ['B', 'C', 'D', 'E', 'F'],  # Columnas B a F
            'datos_especificos': {
                'Cobros': -377486,
                'Facturacion': 0,
                'Vencidos': 390143,
                'Provision': 0,
                'Dotacion': -560370,
                'Dotaciones': 672,
                'Desdotaciones': 672
            }
        }
    
    @log_funcion
    def procesar_acumulado(self, ruta_archivo: str) -> Tuple[str, Dict[str, Any]]:
    """
    Procesa archivo de acumulado según reglas específicas
        
        Args:
            ruta_archivo: Ruta del archivo a procesar
            
        Returns:
            Tuple[str, Dict]: (ruta_salida, resultados_procesamiento)
            
        Raises:
            Exception: Si hay error en el procesamiento
        """
        tiempo_inicio = time.time()
        
        try:
            self.logger.inicio_procesamiento("Acumulado", ruta_archivo)
        
        # Validar archivo
            self.utilidades.validar_archivo(ruta_archivo)
        
        # Leer archivo
            df_original = self.utilidades.leer_archivo(ruta_archivo)
            self.logger.info(f"Archivo leído: {len(df_original)} registros")
        
        # Procesar datos según reglas específicas
            df_resultados, info_adicional = self._procesar_datos_acumulado(df_original)
        
        # Generar archivo de salida
            nombre_salida = self.utilidades.generar_nombre_archivo_salida("acumulado_procesado")
            ruta_salida = os.path.join(DIRECTORIOS['resultados'], nombre_salida)
        
        # Crear directorio si no existe
            self.utilidades.crear_directorio_si_no_existe(DIRECTORIOS['resultados'])
        
        # Guardar resultado
            self.utilidades.escribir_resultado(df_resultados, ruta_salida)
            
            # Crear resumen completo
            tiempo_procesamiento = time.time() - tiempo_inicio
            resumen = self._crear_resumen_completo(
                df_original, df_resultados, info_adicional, tiempo_procesamiento
            )
            
            self.logger.fin_procesamiento("Acumulado", f"Archivo guardado: {ruta_salida}")
            self.logger.estadisticas_procesamiento(
                len(df_original), len(df_resultados), tiempo_procesamiento
            )
            
            return ruta_salida, resumen
        
    except Exception as e:
            self.logger.error_procesamiento("Acumulado", e)
        raise

    def _procesar_datos_acumulado(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Procesa los datos de acumulado según las reglas específicas
        
        Args:
            df: DataFrame a procesar
            
        Returns:
            Tuple[pd.DataFrame, Dict]: (DataFrame de resultados, información adicional)
        """
        self.logger.info("Iniciando procesamiento específico de datos de acumulado")
        
    # Normalizar nombres de columnas
    df.columns = df.columns.str.strip().str.upper()
        
        # Extraer datos de la fila objetivo
        datos_fila_objetivo = self._extraer_datos_fila_objetivo(df)
        
        # Buscar datos específicos
        datos_especificos = self._buscar_datos_especificos(df)
        
        # Combinar todos los datos
        datos_acumulado = {**datos_fila_objetivo, **datos_especificos}
        
        # Crear DataFrame de resultados
        df_resultados = self._crear_dataframe_resultados(datos_acumulado)
        
        # Crear información adicional
        info_adicional = self._crear_info_adicional(df, datos_acumulado)
        
        self.logger.info(f"Procesamiento de datos completado: {len(df_resultados)} conceptos")
        return df_resultados, info_adicional
    
    def _extraer_datos_fila_objetivo(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extrae datos de la fila objetivo (fila 54)
        
        Args:
            df: DataFrame a procesar
            
        Returns:
            Dict: Datos extraídos de la fila objetivo
        """
        fila_objetivo = self.config_acumulado['fila_objetivo']
        columnas_objetivo = self.config_acumulado['columnas_objetivo']
        
        datos_extraidos = {}
    
    # Buscar fila 54 (índice 53 en Python)
        if len(df) >= fila_objetivo:
            fila_54 = df.iloc[fila_objetivo - 1]  # Fila 54 (índice 53)
            self.logger.info(f"Fila {fila_objetivo} encontrada: {fila_54.to_dict()}")
    else:
            self.logger.warning(f"El archivo no tiene {fila_objetivo} filas, usando la última fila")
        fila_54 = df.iloc[-1]
            self.logger.info(f"Última fila encontrada: {fila_54.to_dict()}")
    
    # Extraer datos de las columnas B a F (índices 1 a 5)
        for i, columna in enumerate(columnas_objetivo):
        if i < len(df.columns):
            valor = fila_54.iloc[i] if i < len(fila_54) else 0
                datos_extraidos[f'Columna_{columna}'] = valor
                self.logger.info(f"Columna {columna}: {valor}")
        
        return datos_extraidos
    
    def _buscar_datos_especificos(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Busca datos específicos de acumulado según las reglas
        
        Args:
            df: DataFrame a procesar
            
        Returns:
            Dict: Datos específicos encontrados
        """
        datos_especificos = self.config_acumulado['datos_especificos']
        datos_encontrados = {}
        
    for concepto, valor_default in datos_especificos.items():
            valor_encontrado = self._buscar_concepto_en_dataframe(df, concepto, valor_default)
            datos_encontrados[f'{concepto}_Encontrado'] = valor_encontrado
        
        return datos_encontrados
    
    def _buscar_concepto_en_dataframe(self, df: pd.DataFrame, concepto: str, valor_default: float) -> float:
        """
        Busca un concepto específico en el DataFrame
        
        Args:
            df: DataFrame a buscar
            concepto: Concepto a buscar
            valor_default: Valor por defecto si no se encuentra
            
        Returns:
            float: Valor encontrado o valor por defecto
        """
        # Buscar en las columnas
        for col in df.columns:
            if concepto.upper() in col.upper():
                # Buscar en todas las filas
                for idx, valor in enumerate(df[col]):
                    if pd.notna(valor) and valor != 0:
                        self.logger.info(f"{concepto} encontrado en fila {idx+1}: {valor}")
                        return valor
                else:
                    self.logger.info(f"{concepto} no encontrado en columna {col}, usando valor por defecto: {valor_default}")
                    return valor_default
        
        self.logger.info(f"Columna para {concepto} no encontrada, usando valor por defecto: {valor_default}")
        return valor_default
    
    def _crear_dataframe_resultados(self, datos_acumulado: Dict[str, Any]) -> pd.DataFrame:
        """
        Crea DataFrame de resultados
        
        Args:
            datos_acumulado: Datos procesados
            
        Returns:
            pd.DataFrame: DataFrame de resultados
        """
    df_resultados = pd.DataFrame({
        'Concepto': list(datos_acumulado.keys()),
        'Valor': list(datos_acumulado.values()),
            'Fecha_Procesamiento': obtener_fecha_actual(),
            'Tipo_Procesamiento': 'ACUMULADO',
            'Version_Procesador': '2.0.1',
            'Usuario_Procesamiento': 'SISTEMA'
        })
        
        # Agregar columnas adicionales
        df_resultados['Valor_Formateado'] = df_resultados['Valor'].apply(
            lambda x: self.utilidades.formatear_numero(x, 'moneda') if isinstance(x, (int, float)) else str(x)
        )
        
        df_resultados['Tipo_Dato'] = df_resultados['Valor'].apply(
            lambda x: type(x).__name__
        )
        
        return df_resultados
    
    def _crear_info_adicional(self, df_original: pd.DataFrame, datos_acumulado: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea información adicional del procesamiento
        
        Args:
            df_original: DataFrame original
            datos_acumulado: Datos procesados
            
        Returns:
            Dict: Información adicional
        """
    info_adicional = {
            'Registros_Originales': len(df_original),
            'Columnas_Originales': list(df_original.columns),
            'Fila_Objetivo_Procesada': True,
            'Datos_Especificos_Encontrados': len([k for k in datos_acumulado.keys() if 'Encontrado' in k]),
            'Total_Conceptos_Procesados': len(datos_acumulado),
            'Configuracion_Usada': self.config_acumulado,
            'Fecha_Procesamiento': obtener_fecha_actual(),
            'Timestamp_Procesamiento': obtener_timestamp()
        }
        
        # Agregar estadísticas del DataFrame original
        estadisticas = self.utilidades.generar_estadisticas_dataframe(df_original)
        info_adicional['Estadisticas_DataFrame_Original'] = estadisticas
        
        return info_adicional
    
    def _crear_resumen_completo(self, df_original: pd.DataFrame, 
                               df_resultados: pd.DataFrame, 
                               info_adicional: Dict[str, Any],
                               tiempo_procesamiento: float) -> Dict[str, Any]:
        """
        Crea un resumen completo del procesamiento
        
        Args:
            df_original: DataFrame original
            df_resultados: DataFrame de resultados
            info_adicional: Información adicional
            tiempo_procesamiento: Tiempo de procesamiento en segundos
            
        Returns:
            Dict: Resumen completo del procesamiento
        """
        resumen = {
            'tipo_procesamiento': 'Acumulado',
            'fecha_procesamiento': obtener_fecha_actual(),
            'registros_originales': len(df_original),
            'conceptos_procesados': len(df_resultados),
            'columnas_originales': list(df_original.columns),
            'conceptos_resultado': list(df_resultados['Concepto']),
            'tiempo_procesamiento_segundos': tiempo_procesamiento,
            'tiempo_procesamiento_formateado': f"{tiempo_procesamiento:.2f}s",
            'configuracion_usada': self.config_acumulado,
            'version_procesador': '2.0.1',
            'fecha_procesamiento_timestamp': obtener_timestamp(),
            'info_adicional': info_adicional
        }
        
        return resumen
    
    def generar_reporte_detallado(self, df_resultados: pd.DataFrame) -> Dict[str, Any]:
        """
        Genera un reporte detallado de los resultados
        
        Args:
            df_resultados: DataFrame de resultados
            
        Returns:
            Dict: Reporte detallado
        """
        reporte = {
            'fecha_generacion': obtener_fecha_actual(),
            'total_conceptos': len(df_resultados),
            'conceptos_por_tipo': df_resultados['Tipo_Dato'].value_counts().to_dict(),
            'valores_por_concepto': df_resultados.set_index('Concepto')['Valor'].to_dict(),
            'conceptos_encontrados': len(df_resultados[df_resultados['Concepto'].str.contains('Encontrado')]),
            'conceptos_por_defecto': len(df_resultados[~df_resultados['Concepto'].str.contains('Encontrado')])
        }
        
        # Análisis de valores
        valores_numericos = df_resultados[df_resultados['Tipo_Dato'] == 'float64']['Valor']
        if len(valores_numericos) > 0:
            reporte['estadisticas_valores'] = {
                'suma_total': valores_numericos.sum(),
                'promedio': valores_numericos.mean(),
                'maximo': valores_numericos.max(),
                'minimo': valores_numericos.min()
            }
        
        return reporte

# =============================================================================
# FUNCIÓN PRINCIPAL Y FUNCIONES DE CONVENIENCIA
# =============================================================================

def procesar_acumulado(ruta_archivo: str) -> Tuple[str, Dict[str, Any]]:
    """
    Función de conveniencia para procesar acumulado
    
    Args:
        ruta_archivo: Ruta del archivo a procesar
        
    Returns:
        Tuple[str, Dict]: (ruta_salida, resultados_procesamiento)
    """
    procesador = ProcesadorAcumulado()
    return procesador.procesar_acumulado(ruta_archivo)

def procesar_datos_acumulado(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Función de conveniencia para procesar datos de acumulado
    
    Args:
        df: DataFrame a procesar
        
    Returns:
        Tuple[pd.DataFrame, Dict]: (DataFrame de resultados, información adicional)
    """
    procesador = ProcesadorAcumulado()
    return procesador._procesar_datos_acumulado(df)

# =============================================================================
# FUNCIÓN MAIN
# =============================================================================

def main():
    """
    Función principal para ejecución desde línea de comandos
    """
    if len(sys.argv) != 2:
        print("Uso: python procesador_acumulado.py <ruta_archivo>")
        print("Ejemplo: python procesador_acumulado.py datos_acumulado.xlsx")
        sys.exit(1)
    
    ruta_archivo = sys.argv[1]
    
    try:
        print("=" * 60)
        print("PROCESADOR DE ACUMULADO - GRUPO PLANETA")
        print("Versión: 2.0.1")
        print("=" * 60)
        
        ruta_salida, resumen = procesar_acumulado(ruta_archivo)
        
        print("\n✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
        print(f"📁 Archivo de salida: {ruta_salida}")
        print(f"📊 Conceptos procesados: {resumen['conceptos_procesados']}")
        print(f"⏱️  Tiempo de procesamiento: {resumen['tiempo_procesamiento_formateado']}")
        print(f"🔍 Datos específicos encontrados: {resumen['info_adicional']['Datos_Especificos_Encontrados']}")
        
        # Mostrar algunos conceptos procesados
        print(f"\n📋 Conceptos procesados:")
        for concepto in resumen['conceptos_resultado'][:5]:  # Mostrar primeros 5
            print(f"   • {concepto}")
        if len(resumen['conceptos_resultado']) > 5:
            print(f"   • ... y {len(resumen['conceptos_resultado']) - 5} más")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR EN PROCESAMIENTO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 