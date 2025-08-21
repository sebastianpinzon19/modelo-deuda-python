#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración del Sistema de Gestión de Cartera
"""

import os
from pathlib import Path

# Configuración de la aplicación
class Config:
    # Configuración básica
    SECRET_KEY = 'grupo-planeta-cartera-2024'
    DEBUG = True
    
    # Carpetas del sistema
    BASE_DIR = Path(__file__).parent
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    OUTPUT_FOLDER = BASE_DIR / 'outputs'
    
    # Configuración de archivos
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max
    ALLOWED_EXTENSIONS = {
        'csv': ['.csv'],
        'excel': ['.xlsx', '.xls']
    }
    
    # Configuración del servidor
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Configuración de logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @staticmethod
    def init_app(app):
        """Inicializar configuración de la aplicación"""
        # Crear carpetas si no existen
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
        
        # Configurar logging
        import logging
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format=Config.LOG_FORMAT
        )

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
