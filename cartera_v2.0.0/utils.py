#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades para el Sistema de Gestión de Cartera
"""

import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename, file_type):
    """Verificar si el archivo tiene una extensión permitida"""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS'].get(file_type, [])
    
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def validate_csv_file(filename):
    """Validar archivo CSV"""
    return allowed_file(filename, 'csv')

def validate_excel_file(filename):
    """Validar archivo Excel"""
    return allowed_file(filename, 'excel')

def save_upload_file(file, prefix='file'):
    """Guardar archivo subido de forma segura"""
    if file and file.filename:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{prefix}_{timestamp}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
        file.save(file_path)
        return file_path
    return None

def get_output_filename(original_filename, process_type):
    """Generar nombre de archivo de salida"""
    base_name = os.path.splitext(os.path.basename(original_filename))[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{process_type}_{base_name}_{timestamp}.xlsx"

def cleanup_temp_files(file_paths):
    """Limpiar archivos temporales"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            current_app.logger.warning(f"No se pudo eliminar archivo temporal {file_path}: {e}")

def format_file_size(size_bytes):
    """Formatear tamaño de archivo en formato legible"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def validate_date_format(date_str):
    """Validar formato de fecha YYYY-MM-DD"""
    if not date_str:
        return False
    
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_trm_value(value_str):
    """Validar valor de TRM"""
    if not value_str:
        return False
    
    try:
        value = float(value_str.replace(',', '.'))
        return value > 0
    except (ValueError, TypeError):
        return False

# Importar datetime aquí para evitar importación circular
from datetime import datetime
