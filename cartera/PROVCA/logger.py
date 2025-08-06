#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Logging para el Procesamiento de Cartera
Grupo Planeta - Sistema de Análisis Financiero
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from config import LOGGING_CONFIG, DIRECTORIOS

class SistemaLogger:
    """
    Clase para manejar el sistema de logging del procesamiento de cartera
    """
    
    def __init__(self, nombre_modulo="SistemaCartera"):
        """
        Inicializa el sistema de logging
        
        Args:
            nombre_modulo (str): Nombre del módulo que está usando el logger
        """
        self.nombre_modulo = nombre_modulo
        self.logger = self._configurar_logger()
    
    def _configurar_logger(self):
        """
        Configura el logger con handlers y formatters apropiados
        """
        # Crear logger
        logger = logging.getLogger(self.nombre_modulo)
        logger.setLevel(getattr(logging, LOGGING_CONFIG['nivel']))
        
        # Evitar duplicación de handlers
        if logger.handlers:
            return logger
        
        # Crear directorio de logs si no existe
        os.makedirs(DIRECTORIOS['logs'], exist_ok=True)
        
        # Handler para archivo con rotación
        archivo_handler = logging.handlers.RotatingFileHandler(
            LOGGING_CONFIG['archivo_log'],
            maxBytes=LOGGING_CONFIG['max_tamano'],
            backupCount=LOGGING_CONFIG['backup_count'],
            encoding='utf-8'
        )
        
        # Handler para consola
        consola_handler = logging.StreamHandler(sys.stdout)
        
        # Crear formatter
        formatter = logging.Formatter(LOGGING_CONFIG['formato'])
        
        # Aplicar formatter a los handlers
        archivo_handler.setFormatter(formatter)
        consola_handler.setFormatter(formatter)
        
        # Agregar handlers al logger
        logger.addHandler(archivo_handler)
        logger.addHandler(consola_handler)
        
        return logger
    
    def info(self, mensaje):
        """Registra mensaje de información"""
        self.logger.info(f"[{self.nombre_modulo}] {mensaje}")
    
    def warning(self, mensaje):
        """Registra mensaje de advertencia"""
        self.logger.warning(f"[{self.nombre_modulo}] {mensaje}")
    
    def error(self, mensaje):
        """Registra mensaje de error"""
        self.logger.error(f"[{self.nombre_modulo}] {mensaje}")
    
    def debug(self, mensaje):
        """Registra mensaje de debug"""
        self.logger.debug(f"[{self.nombre_modulo}] {mensaje}")
    
    def critical(self, mensaje):
        """Registra mensaje crítico"""
        self.logger.critical(f"[{self.nombre_modulo}] {mensaje}")
    
    def inicio_procesamiento(self, tipo_procesamiento, archivo=None):
        """Registra el inicio de un procesamiento"""
        mensaje = f"Iniciando procesamiento: {tipo_procesamiento}"
        if archivo:
            mensaje += f" - Archivo: {archivo}"
        self.info(mensaje)
    
    def fin_procesamiento(self, tipo_procesamiento, resultado=None):
        """Registra el fin de un procesamiento"""
        mensaje = f"Procesamiento completado: {tipo_procesamiento}"
        if resultado:
            mensaje += f" - Resultado: {resultado}"
        self.info(mensaje)
    
    def error_procesamiento(self, tipo_procesamiento, error):
        """Registra un error en el procesamiento"""
        self.error(f"Error en procesamiento {tipo_procesamiento}: {str(error)}")
    
    def estadisticas_procesamiento(self, registros_originales, registros_procesados, tiempo_procesamiento=None):
        """Registra estadísticas del procesamiento"""
        mensaje = f"Estadísticas: {registros_originales} → {registros_procesados} registros"
        if tiempo_procesamiento:
            mensaje += f" (Tiempo: {tiempo_procesamiento:.2f}s)"
        self.info(mensaje)

def crear_logger(nombre_modulo):
    """
    Función factory para crear loggers
    
    Args:
        nombre_modulo (str): Nombre del módulo
    
    Returns:
        SistemaLogger: Instancia del logger configurado
    """
    return SistemaLogger(nombre_modulo)

def log_funcion(func):
    """
    Decorador para logging automático de funciones
    
    Args:
        func: Función a decorar
    
    Returns:
        function: Función decorada
    """
    def wrapper(*args, **kwargs):
        logger = crear_logger(func.__module__)
        logger.info(f"Ejecutando función: {func.__name__}")
        
        try:
            resultado = func(*args, **kwargs)
            logger.info(f"Función {func.__name__} completada exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error en función {func.__name__}: {str(e)}")
            raise
    
    return wrapper

def log_clase(cls):
    """
    Decorador para logging automático de clases
    
    Args:
        cls: Clase a decorar
    
    Returns:
        class: Clase decorada
    """
    class Wrapper(cls):
        def __init__(self, *args, **kwargs):
            self.logger = crear_logger(cls.__name__)
            self.logger.info(f"Inicializando clase: {cls.__name__}")
            super().__init__(*args, **kwargs)
            self.logger.info(f"Clase {cls.__name__} inicializada correctamente")
    
    return Wrapper

# Logger global para el sistema
logger_global = crear_logger("SistemaGlobal")

def obtener_logger(nombre_modulo=None):
    """
    Obtiene un logger configurado
    
    Args:
        nombre_modulo (str, optional): Nombre del módulo. Defaults to None.
    
    Returns:
        SistemaLogger: Logger configurado
    """
    if nombre_modulo is None:
        return logger_global
    return crear_logger(nombre_modulo)

if __name__ == "__main__":
    # Prueba del sistema de logging
    logger = crear_logger("Prueba")
    logger.info("Sistema de logging funcionando correctamente")
    logger.warning("Este es un mensaje de advertencia")
    logger.error("Este es un mensaje de error")
    logger.debug("Este es un mensaje de debug")
