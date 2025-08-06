#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades para el Procesamiento de Cartera
Sistema de Procesamiento de Cartera - Grupo Planeta
"""

import pandas as pd
import numpy as np
import os
import sys
import re
from datetime import datetime
from typing import Union, List, Dict, Any, Optional
from config import (
    EXTENSIONES_SOPORTADAS, EXCEL_CONFIG, CSV_CONFIG, 
    FORMATOS_FECHA, FORMATOS_NUMERO, VALIDACION_CONFIG,
    DIRECTORIOS, obtener_timestamp, obtener_fecha_actual
)
from logger import crear_logger, log_funcion

# =============================================================================
# CLASE PRINCIPAL DE UTILIDADES
# =============================================================================

class UtilidadesCartera:
    """
    Clase principal que contiene todas las utilidades para el procesamiento de cartera
    """
    
    def __init__(self):
        """Inicializa la clase de utilidades"""
        self.logger = crear_logger("UtilidadesCartera")
        self.logger.info("Inicializando sistema de utilidades")
    
    # =============================================================================
    # FUNCIONES DE LIMPIEZA Y NORMALIZACIÓN
    # =============================================================================
    
    @log_funcion
    def limpiar_texto(self, texto: Union[str, Any]) -> str:
        """
        Limpia y normaliza texto
        
        Args:
            texto: Texto a limpiar
            
        Returns:
            str: Texto limpio y normalizado
        """
        if pd.isna(texto) or texto is None:
            return ""
        
        texto_str = str(texto).strip()
        
        # Convertir a mayúsculas
        texto_str = texto_str.upper()
        
        # Eliminar caracteres especiales problemáticos
        texto_str = re.sub(r'[^\w\s\-\.]', '', texto_str)
        
        # Normalizar espacios
        texto_str = re.sub(r'\s+', ' ', texto_str)
        
        return texto_str
    
    @log_funcion
    def convertir_fecha(self, fecha_str: Union[str, Any]) -> Optional[pd.Timestamp]:
        """
        Convierte string de fecha a datetime
        
        Args:
            fecha_str: String de fecha a convertir
            
        Returns:
            pd.Timestamp: Fecha convertida o None si no se puede convertir
        """
        if pd.isna(fecha_str) or fecha_str is None:
        return None
    
    try:
            # Si ya es un timestamp, retornarlo
            if isinstance(fecha_str, pd.Timestamp):
                return fecha_str
            
            # Convertir a string
            fecha_str = str(fecha_str).strip()
            
            if not fecha_str:
                return None
            
        # Intentar diferentes formatos de fecha
            for formato in FORMATOS_FECHA:
            try:
                return pd.to_datetime(fecha_str, format=formato)
                except (ValueError, TypeError):
                continue
        
            # Si no funciona con formatos específicos, usar pandas
            return pd.to_datetime(fecha_str, errors='coerce')
            
        except Exception as e:
            self.logger.warning(f"No se pudo convertir fecha '{fecha_str}': {e}")
        return None

    @log_funcion
    def formatear_numero(self, valor: Union[float, int, str], 
                        formato: str = 'moneda') -> str:
        """
        Formatea número con separadores de miles
        
        Args:
            valor: Valor numérico a formatear
            formato: Tipo de formato ('moneda', 'porcentaje', 'numero')
            
        Returns:
            str: Número formateado
        """
        if pd.isna(valor) or valor is None:
            return "0.00"
    
    try:
        numero = float(valor)
            
            if formato == 'moneda':
                return f"${numero:,.2f}"
            elif formato == 'porcentaje':
                return f"{numero:.2f}%"
            elif formato == 'numero':
                return f"{numero:,.2f}"
            else:
        return f"{numero:,.2f}"
                
        except (ValueError, TypeError):
        return "0.00"

    @log_funcion
    def calcular_porcentaje(self, valor: float, total: float) -> float:
        """
        Calcula porcentaje
        
        Args:
            valor: Valor para calcular porcentaje
            total: Valor total
            
        Returns:
            float: Porcentaje calculado
        """
        if total == 0 or pd.isna(total) or pd.isna(valor):
            return 0.0
    return (valor / total) * 100

    # =============================================================================
    # FUNCIONES DE VALIDACIÓN
    # =============================================================================
    
    @log_funcion
    def validar_archivo(self, ruta_archivo: str) -> bool:
        """
        Valida que el archivo existe y es legible
        
        Args:
            ruta_archivo: Ruta del archivo a validar
            
        Returns:
            bool: True si el archivo es válido
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            PermissionError: Si no se puede leer el archivo
            ValueError: Si el archivo no es válido
        """
        if not ruta_archivo:
            raise ValueError("Ruta de archivo no puede estar vacía")
        
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
    
    if not os.access(ruta_archivo, os.R_OK):
        raise PermissionError(f"No se puede leer el archivo: {ruta_archivo}")
    
        # Validar tamaño del archivo
        tamano_archivo = os.path.getsize(ruta_archivo)
        if tamano_archivo > VALIDACION_CONFIG['tamano_maximo_archivo']:
            raise ValueError(f"Archivo demasiado grande: {tamano_archivo} bytes")
        
        # Validar extensión
        extension = self.obtener_extension(ruta_archivo)
        extensiones_validas = []
        for ext_list in EXTENSIONES_SOPORTADAS.values():
            extensiones_validas.extend(ext_list)
        
        if extension not in extensiones_validas:
            raise ValueError(f"Extensión no soportada: {extension}")
        
        self.logger.info(f"Archivo validado correctamente: {ruta_archivo}")
    return True

    @log_funcion
    def obtener_extension(self, ruta_archivo: str) -> str:
        """
        Obtiene la extensión del archivo
        
        Args:
            ruta_archivo: Ruta del archivo
            
        Returns:
            str: Extensión del archivo en minúsculas
        """
    return os.path.splitext(ruta_archivo)[1].lower()

    @log_funcion
    def validar_columnas_requeridas(self, df: pd.DataFrame, 
                                  columnas_requeridas: List[str]) -> bool:
        """
        Valida que el dataframe tenga las columnas requeridas
        
        Args:
            df: DataFrame a validar
            columnas_requeridas: Lista de columnas requeridas
            
        Returns:
            bool: True si todas las columnas están presentes
            
        Raises:
            ValueError: Si faltan columnas requeridas
        """
    columnas_faltantes = []
    for columna in columnas_requeridas:
        if columna not in df.columns:
            columnas_faltantes.append(columna)
    
    if columnas_faltantes:
        raise ValueError(f"Columnas faltantes: {', '.join(columnas_faltantes)}")
    
        self.logger.info(f"Columnas requeridas validadas: {len(columnas_requeridas)} columnas")
    return True

    # =============================================================================
    # FUNCIONES DE ARCHIVOS Y DIRECTORIOS
    # =============================================================================
    
    @log_funcion
    def crear_directorio_si_no_existe(self, directorio: str) -> str:
        """
        Crea directorio si no existe
        
        Args:
            directorio: Ruta del directorio a crear
            
        Returns:
            str: Ruta del directorio creado
        """
        if not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)
            self.logger.info(f"Directorio creado: {directorio}")
        return directorio
    
    @log_funcion
    def generar_nombre_archivo_salida(self, tipo_procesamiento: str, 
                                    extension: str = ".xlsx") -> str:
        """
        Genera nombre único para archivo de salida
        
        Args:
            tipo_procesamiento: Tipo de procesamiento
            extension: Extensión del archivo
            
        Returns:
            str: Nombre único del archivo
        """
        timestamp = obtener_timestamp()
        nombre_base = f"{tipo_procesamiento}_{timestamp}"
        
        # Sanitizar nombre
        nombre_base = re.sub(r'[^\w\-_]', '_', nombre_base)
        
        return f"{nombre_base}{extension}"
    
    @log_funcion
    def limpiar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia y prepara dataframe
        
        Args:
            df: DataFrame a limpiar
            
        Returns:
            pd.DataFrame: DataFrame limpio
        """
        if df.empty:
            self.logger.warning("DataFrame vacío recibido")
            return df
        
        # Eliminar filas completamente vacías
        df_limpio = df.dropna(how='all')
        
        # Eliminar columnas completamente vacías
        df_limpio = df_limpio.dropna(axis=1, how='all')
        
        # Limpiar nombres de columnas
        df_limpio.columns = df_limpio.columns.str.strip().str.upper()
        
        # Eliminar espacios en blanco al inicio y final de los datos
        for columna in df_limpio.select_dtypes(include=['object']).columns:
            df_limpio[columna] = df_limpio[columna].astype(str).str.strip()
        
        self.logger.info(f"DataFrame limpiado: {len(df)} → {len(df_limpio)} registros")
        return df_limpio
    
    # =============================================================================
    # FUNCIONES DE LECTURA DE ARCHIVOS
    # =============================================================================
    
    @log_funcion
    def leer_archivo_excel(self, ruta_archivo: str, hoja: Union[int, str] = 0) -> pd.DataFrame:
        """
        Lee archivo Excel con manejo de errores
        
        Args:
            ruta_archivo: Ruta del archivo Excel
            hoja: Nombre o índice de la hoja a leer
            
        Returns:
            pd.DataFrame: Datos leídos del archivo
            
        Raises:
            Exception: Si hay error al leer el archivo
        """
        try:
            df = pd.read_excel(
                ruta_archivo, 
                sheet_name=hoja, 
                engine=EXCEL_CONFIG['engine'],
                encoding=EXCEL_CONFIG['encoding']
            )
            self.logger.info(f"Archivo Excel leído: {ruta_archivo} - {len(df)} registros")
        return df
            
    except Exception as e:
            self.logger.error(f"Error al leer Excel {ruta_archivo}: {e}")
        raise

    @log_funcion
    def leer_archivo_csv(self, ruta_archivo: str, separador: str = None) -> pd.DataFrame:
        """
        Lee archivo CSV con manejo de errores
        
        Args:
            ruta_archivo: Ruta del archivo CSV
            separador: Separador de campos
            
        Returns:
            pd.DataFrame: Datos leídos del archivo
            
        Raises:
            Exception: Si hay error al leer el archivo
        """
        try:
            if separador is None:
                separador = CSV_CONFIG['separador']
            
            df = pd.read_csv(
                ruta_archivo, 
                sep=separador, 
                encoding=CSV_CONFIG['encoding']
            )
            self.logger.info(f"Archivo CSV leído: {ruta_archivo} - {len(df)} registros")
        return df
            
    except Exception as e:
            self.logger.error(f"Error al leer CSV {ruta_archivo}: {e}")
        raise

    @log_funcion
    def leer_archivo(self, ruta_archivo: str) -> pd.DataFrame:
        """
        Lee archivo automáticamente según su extensión
        
        Args:
            ruta_archivo: Ruta del archivo a leer
            
        Returns:
            pd.DataFrame: Datos leídos del archivo
            
        Raises:
            ValueError: Si el tipo de archivo no es soportado
        """
        extension = self.obtener_extension(ruta_archivo)
        
        if extension in EXTENSIONES_SOPORTADAS['excel']:
            return self.leer_archivo_excel(ruta_archivo)
        elif extension in EXTENSIONES_SOPORTADAS['csv']:
            return self.leer_archivo_csv(ruta_archivo)
    else:
        raise ValueError(f"Tipo de archivo no soportado: {extension}")

    # =============================================================================
    # FUNCIONES DE ESCRITURA DE ARCHIVOS
    # =============================================================================
    
    @log_funcion
    def escribir_resultado(self, df: pd.DataFrame, ruta_salida: str, 
                          tipo_archivo: str = "excel") -> bool:
        """
        Escribe resultado a archivo
        
        Args:
            df: DataFrame a guardar
            ruta_salida: Ruta donde guardar el archivo
            tipo_archivo: Tipo de archivo ('excel' o 'csv')
            
        Returns:
            bool: True si se guardó correctamente
            
        Raises:
            ValueError: Si el tipo de archivo no es soportado
            Exception: Si hay error al guardar
        """
        try:
            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_salida)
            if directorio:
                self.crear_directorio_si_no_existe(directorio)
            
            if tipo_archivo == "excel":
                df.to_excel(ruta_salida, index=False, engine=EXCEL_CONFIG['engine'])
            elif tipo_archivo == "csv":
                df.to_csv(ruta_salida, index=False, encoding=CSV_CONFIG['encoding'])
            else:
                raise ValueError(f"Tipo de archivo no soportado: {tipo_archivo}")
            
            self.logger.info(f"Archivo guardado: {ruta_salida} - {len(df)} registros")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al guardar archivo {ruta_salida}: {e}")
            raise
    
    # =============================================================================
    # FUNCIONES DE RESUMEN Y ESTADÍSTICAS
    # =============================================================================
    
    @log_funcion
    def crear_resumen_procesamiento(self, datos_originales: pd.DataFrame, 
                                  datos_procesados: pd.DataFrame, 
                                  tipo_procesamiento: str) -> Dict[str, Any]:
        """
        Crea resumen del procesamiento
        
        Args:
            datos_originales: DataFrame original
            datos_procesados: DataFrame procesado
            tipo_procesamiento: Tipo de procesamiento realizado
            
        Returns:
            Dict: Resumen del procesamiento
        """
    resumen = {
        'tipo_procesamiento': tipo_procesamiento,
            'fecha_procesamiento': obtener_fecha_actual(),
        'registros_originales': len(datos_originales),
        'registros_procesados': len(datos_procesados),
        'columnas_originales': list(datos_originales.columns),
            'columnas_procesadas': list(datos_procesados.columns),
            'reduccion_registros': len(datos_originales) - len(datos_procesados),
            'porcentaje_reduccion': self.calcular_porcentaje(
                len(datos_originales) - len(datos_procesados), 
                len(datos_originales)
            )
        }
        
        self.logger.info(f"Resumen creado: {resumen['registros_originales']} → {resumen['registros_procesados']} registros")
    return resumen
    
    @log_funcion
    def generar_estadisticas_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Genera estadísticas detalladas de un DataFrame
        
        Args:
            df: DataFrame a analizar
            
        Returns:
            Dict: Estadísticas del DataFrame
        """
        if df.empty:
            return {'error': 'DataFrame vacío'}
        
        estadisticas = {
            'total_registros': len(df),
            'total_columnas': len(df.columns),
            'columnas_numericas': len(df.select_dtypes(include=[np.number]).columns),
            'columnas_texto': len(df.select_dtypes(include=['object']).columns),
            'columnas_fecha': len(df.select_dtypes(include=['datetime']).columns),
            'valores_nulos': df.isnull().sum().sum(),
            'porcentaje_nulos': self.calcular_porcentaje(df.isnull().sum().sum(), len(df) * len(df.columns))
        }
        
        # Estadísticas por columnas numéricas
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
        if len(columnas_numericas) > 0:
            estadisticas['estadisticas_numericas'] = df[columnas_numericas].describe().to_dict()
        
        return estadisticas

# =============================================================================
# INSTANCIA GLOBAL Y FUNCIONES DE CONVENIENCIA
# =============================================================================

# Instancia global de utilidades
utilidades = UtilidadesCartera()

# Funciones de conveniencia para compatibilidad con código existente
def limpiar_texto(texto):
    return utilidades.limpiar_texto(texto)

def convertir_fecha(fecha_str):
    return utilidades.convertir_fecha(fecha_str)

def formatear_numero(valor, formato='moneda'):
    return utilidades.formatear_numero(valor, formato)

def calcular_porcentaje(valor, total):
    return utilidades.calcular_porcentaje(valor, total)

def validar_archivo(ruta_archivo):
    return utilidades.validar_archivo(ruta_archivo)

def obtener_extension(ruta_archivo):
    return utilidades.obtener_extension(ruta_archivo)

def crear_directorio_si_no_existe(directorio):
    return utilidades.crear_directorio_si_no_existe(directorio)

def generar_nombre_archivo_salida(tipo_procesamiento, extension=".xlsx"):
    return utilidades.generar_nombre_archivo_salida(tipo_procesamiento, extension)

def limpiar_dataframe(df):
    return utilidades.limpiar_dataframe(df)

def validar_columnas_requeridas(df, columnas_requeridas):
    return utilidades.validar_columnas_requeridas(df, columnas_requeridas)

def escribir_resultado(df, ruta_salida, tipo_archivo="excel"):
    return utilidades.escribir_resultado(df, ruta_salida, tipo_archivo)

def leer_archivo_excel(ruta_archivo, hoja=0):
    return utilidades.leer_archivo_excel(ruta_archivo, hoja)

def leer_archivo_csv(ruta_archivo, separador=","):
    return utilidades.leer_archivo_csv(ruta_archivo, separador)

def leer_archivo(ruta_archivo):
    return utilidades.leer_archivo(ruta_archivo)

def crear_resumen_procesamiento(datos_originales, datos_procesados, tipo_procesamiento):
    return utilidades.crear_resumen_procesamiento(datos_originales, datos_procesados, tipo_procesamiento)

def generar_estadisticas_dataframe(df):
    return utilidades.generar_estadisticas_dataframe(df)

if __name__ == "__main__":
    print("Módulo de utilidades para procesamiento de cartera")
    print("Este módulo contiene funciones auxiliares para el procesamiento de archivos.") 
    
    # Prueba básica del sistema
    utilidades.logger.info("Sistema de utilidades funcionando correctamente") 