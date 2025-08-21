#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración para el Procesador de Acumulado
"""

import os
from datetime import datetime

# Configuración de directorios
DIRECTORIOS = {
    'resultados': r"C:\wamp64\www\modelo-deuda-python\cartera_v2.0.0\PROVCA_PROCESADOS",
    'logs': r"C:\wamp64\www\modelo-deuda-python\cartera_v2.0.0\PROVCA_PROCESADOS\logs"
}

# Configuración de procesamiento
CONFIG_PROCESAMIENTO = {
    'acumulado': {
        'fila_objetivo': 54,
        'columnas_objetivo': ['B', 'C', 'D', 'E', 'F']
    }
}

def obtener_timestamp():
    """Obtiene timestamp actual"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def obtener_fecha_actual():
    """Obtiene fecha actual formateada"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Crear directorios si no existen
for directorio in DIRECTORIOS.values():
    os.makedirs(directorio, exist_ok=True)

