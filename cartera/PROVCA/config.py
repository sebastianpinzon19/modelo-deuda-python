#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración del Sistema de Procesamiento de Cartera
Grupo Planeta - Sistema de Análisis Financiero
"""

import os
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN GENERAL DEL SISTEMA
# =============================================================================

# Información del sistema
SISTEMA_INFO = {
    'nombre': 'Sistema de Procesamiento de Cartera',
    'version': '2.0.1',
    'empresa': 'Grupo Planeta',
    'desarrollador': 'Equipo de Desarrollo',
    'fecha_creacion': '2024-01-01'
}

# =============================================================================
# CONFIGURACIÓN DE DIRECTORIOS
# =============================================================================

# Directorios base
DIRECTORIOS = {
    'base': os.path.dirname(os.path.abspath(__file__)),
    'resultados': 'resultados',
    'logs': 'logs',
    'temp': 'temp',
    'backup': 'backup'
}

# Crear directorios si no existen
for directorio in DIRECTORIOS.values():
    if directorio != DIRECTORIOS['base']:
        ruta_completa = os.path.join(DIRECTORIOS['base'], directorio)
        if not os.path.exists(ruta_completa):
            os.makedirs(ruta_completa)

# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================

LOGGING_CONFIG = {
    'nivel': 'INFO',
    'formato': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'archivo_log': os.path.join(DIRECTORIOS['logs'], 'sistema_cartera.log'),
    'max_tamano': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# =============================================================================
# CONFIGURACIÓN DE ARCHIVOS
# =============================================================================

# Extensiones soportadas
EXTENSIONES_SOPORTADAS = {
    'excel': ['.xlsx', '.xls'],
    'csv': ['.csv'],
    'texto': ['.txt']
}

# Configuración de archivos Excel
EXCEL_CONFIG = {
    'engine': 'openpyxl',
    'encoding': 'utf-8',
    'decimal': '.',
    'thousands': ','
}

# Configuración de archivos CSV
CSV_CONFIG = {
    'encoding': 'utf-8-sig',
    'separador': ',',
    'decimal': '.',
    'thousands': ','
}

# =============================================================================
# CONFIGURACIÓN DE PROCESAMIENTO
# =============================================================================

# Tipos de procesamiento
TIPOS_PROCESAMIENTO = {
    'CARTERA': 'cartera',
    'FORMATO_DEUDA': 'formato_deuda',
    'BALANCE_COMPLETO': 'balance_completo',
    'BALANCE_ESPECIFICO': 'balance_especifico',
    'SITUACION_ESPECIFICO': 'situacion_especifico',
    'FOCUS_ESPECIFICO': 'focus_especifico',
    'ANTICIPOS': 'anticipos',
    'ACUMULADO': 'acumulado'
}

# Configuración específica por tipo de procesamiento
CONFIG_PROCESAMIENTO = {
    'cartera': {
        'columnas_requeridas': ['CLIENTE', 'CUENTA', 'SALDO'],
        'columnas_opcionales': ['FECHA', 'ESTADO', 'TIPO'],
        'orden_por_defecto': ['CLIENTE', 'CUENTA', 'FECHA']
    },
    'formato_deuda': {
        'columnas_requeridas': ['CLIENTE', 'SALDO_DEUDA', 'FECHA_VENCIMIENTO'],
        'columnas_opcionales': ['PROVISION', 'ANTICIPOS', 'FOCUS'],
        'orden_por_defecto': ['CLIENTE', 'FECHA_VENCIMIENTO', 'SALDO_DEUDA']
    },
    'balance_completo': {
        'columnas_requeridas': ['CUENTA', 'SALDO'],
        'columnas_opcionales': ['FECHA', 'TIPO_CUENTA'],
        'orden_por_defecto': ['CUENTA', 'FECHA']
    }
}

# =============================================================================
# CONFIGURACIÓN DE VALIDACIÓN
# =============================================================================

# Reglas de validación
VALIDACION_CONFIG = {
    'tamano_maximo_archivo': 100 * 1024 * 1024,  # 100MB
    'registros_maximos': 1000000,  # 1 millón de registros
    'columnas_maximas': 100,
    'timeout_procesamiento': 300  # 5 minutos
}

# =============================================================================
# CONFIGURACIÓN DE FORMATOS
# =============================================================================

# Formatos de fecha soportados
FORMATOS_FECHA = [
    '%d/%m/%Y',
    '%Y-%m-%d',
    '%d-%m-%Y',
    '%m/%d/%Y',
    '%d/%m/%y',
    '%Y%m%d'
]

# Formatos de número
FORMATOS_NUMERO = {
    'decimal': '.',
    'miles': ',',
    'porcentaje': '%',
    'moneda': '$'
}

# =============================================================================
# CONFIGURACIÓN DE REPORTES
# =============================================================================

# Configuración de reportes
REPORTE_CONFIG = {
    'formato_salida': 'excel',
    'incluir_resumen': True,
    'incluir_estadisticas': True,
    'incluir_graficos': False,
    'comprimir_resultado': False
}

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================

# Configuración de seguridad
SEGURIDAD_CONFIG = {
    'validar_extensiones': True,
    'sanitizar_nombres_archivo': True,
    'limpiar_archivos_temporales': True,
    'max_intentos_procesamiento': 3
}

# =============================================================================
# FUNCIONES DE CONFIGURACIÓN
# =============================================================================

def obtener_ruta_completa(directorio, archivo=None):
    """Obtiene la ruta completa de un directorio o archivo"""
    ruta_base = DIRECTORIOS.get(directorio, directorio)
    if archivo:
        return os.path.join(ruta_base, archivo)
    return ruta_base

def obtener_config_procesamiento(tipo):
    """Obtiene la configuración específica para un tipo de procesamiento"""
    return CONFIG_PROCESAMIENTO.get(tipo, {})

def validar_tipo_procesamiento(tipo):
    """Valida que el tipo de procesamiento sea válido"""
    return tipo in TIPOS_PROCESAMIENTO.values()

def obtener_timestamp():
    """Obtiene timestamp actual formateado"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def obtener_fecha_actual():
    """Obtiene fecha actual formateada"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =============================================================================
# CONFIGURACIÓN DE DESARROLLO
# =============================================================================

# Configuración para desarrollo
DESARROLLO_CONFIG = {
    'modo_debug': True,
    'mostrar_progreso': True,
    'guardar_logs_detallados': True,
    'validar_datos_estrictamente': False
}

if __name__ == "__main__":
    print("Configuración del Sistema de Procesamiento de Cartera")
    print(f"Versión: {SISTEMA_INFO['version']}")
    print(f"Empresa: {SISTEMA_INFO['empresa']}")
    print(f"Directorio base: {DIRECTORIOS['base']}")
