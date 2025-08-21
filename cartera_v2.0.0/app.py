#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación web Flask para el Sistema de Gestión de Cartera
Reemplaza toda la funcionalidad PHP con una interfaz web moderna
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from pathlib import Path

# Importar módulos del sistema
from PROVCA.procesador_cartera import procesar_cartera
from PROVCA.procesador_anticipos import procesar_anticipos
from PROVCA.modelo_deuda import procesar_modelo_deuda
from PROVCA.procesador_unificado import procesar_balance
from PROVCA.trm_config import TRMConfig

# Importar configuración
from config import config

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configurar aplicación
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])
config[config_name].init_app(app)

# Configuración TRM
trm_config = TRMConfig()

@app.route('/')
def index():
    """Página principal con interfaz moderna"""
    return render_template('index.html')

@app.route('/api/trm', methods=['GET'])
def get_trm():
    """Obtener configuración TRM actual"""
    try:
        config = trm_config.cargar_configuracion()
        return jsonify({
            'ok': True,
            'trm_usd': config.get('trm_usd', ''),
            'trm_eur': config.get('trm_eur', '')
        })
    except Exception as e:
        logger.error(f"Error obteniendo TRM: {e}")
        return jsonify({'ok': False, 'error': str(e)})

@app.route('/api/trm', methods=['POST'])
def save_trm():
    """Guardar configuración TRM"""
    try:
        data = request.get_json()
        trm_usd = data.get('trm_usd', '').strip()
        trm_eur = data.get('trm_eur', '').strip()
        
        # Validaciones
        if not trm_usd and not trm_eur:
            return jsonify({'ok': False, 'error': 'Debe ingresar al menos una tasa de cambio'})
        
        if trm_usd and (not trm_usd.replace('.', '').isdigit() or float(trm_usd) <= 0):
            return jsonify({'ok': False, 'error': 'TRM USD debe ser un número válido mayor a 0'})
        
        if trm_eur and (not trm_eur.replace('.', '').isdigit() or float(trm_eur) <= 0):
            return jsonify({'ok': False, 'error': 'TRM EUR debe ser un número válido mayor a 0'})
        
        # Guardar configuración
        config = {}
        if trm_usd:
            config['trm_usd'] = float(trm_usd)
        if trm_eur:
            config['trm_eur'] = float(trm_eur)
        
        trm_config.guardar_configuracion(config)
        
        return jsonify({
            'ok': True,
            'trm_usd': config.get('trm_usd', ''),
            'trm_eur': config.get('trm_eur', ''),
            'message': 'Tasas de cambio guardadas correctamente'
        })
    except Exception as e:
        logger.error(f"Error guardando TRM: {e}")
        return jsonify({'ok': False, 'error': str(e)})

@app.route('/api/procesar/cartera', methods=['POST'])
def procesar_cartera():
    """Procesar archivo de cartera"""
    try:
        if 'archivo' not in request.files:
            return jsonify({'ok': False, 'error': 'No se seleccionó ningún archivo'})
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            return jsonify({'ok': False, 'error': 'No se seleccionó ningún archivo'})
        
        if not archivo.filename.lower().endswith('.csv'):
            return jsonify({'ok': False, 'error': 'El archivo debe ser un CSV'})
        
        # Guardar archivo temporal
        filename = secure_filename(archivo.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_filename = f"cartera_{timestamp}_{filename}"
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        archivo.save(temp_path)
        
        # Obtener parámetros
        moneda = request.form.get('moneda', '')
        fecha_cierre = request.form.get('fecha_cierre', datetime.now().strftime('%Y-%m-%d'))
        
        # Procesar cartera
        output_path = procesar_cartera(temp_path, None, fecha_cierre, False, moneda)
        
        # Obtener TRM actual
        config = trm_config.cargar_configuracion()
        
        return jsonify({
            'ok': True,
            'url': f'/descargar/{os.path.basename(output_path)}',
            'file': os.path.basename(output_path),
            'trm_usd': config.get('trm_usd', ''),
            'trm_eur': config.get('trm_eur', '')
        })
        
    except Exception as e:
        logger.error(f"Error procesando cartera: {e}")
        return jsonify({'ok': False, 'error': str(e)})

@app.route('/api/procesar/anticipos', methods=['POST'])
def procesar_anticipos():
    """Procesar archivo de anticipos"""
    try:
        if 'archivo' not in request.files:
            return jsonify({'ok': False, 'error': 'No se seleccionó ningún archivo'})
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            return jsonify({'ok': False, 'error': 'No se seleccionó ningún archivo'})
        
        if not archivo.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'ok': False, 'error': 'El archivo debe ser un Excel'})
        
        # Guardar archivo temporal
        filename = secure_filename(archivo.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_filename = f"anticipos_{timestamp}_{filename}"
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        archivo.save(temp_path)
        
        # Procesar anticipos
        output_path = procesar_anticipos(temp_path)
        
        # Obtener TRM actual
        config = trm_config.cargar_configuracion()
        
        return jsonify({
            'ok': True,
            'url': f'/descargar/{os.path.basename(output_path)}',
            'file': os.path.basename(output_path),
            'trm_usd': config.get('trm_usd', ''),
            'trm_eur': config.get('trm_eur', '')
        })
        
    except Exception as e:
        logger.error(f"Error procesando anticipos: {e}")
        return jsonify({'ok': False, 'error': str(e)})

@app.route('/api/procesar/modelo', methods=['POST'])
def procesar_modelo():
    """Procesar modelo de deuda"""
    try:
        if 'cartera' not in request.files or 'anticipos' not in request.files:
            return jsonify({'ok': False, 'error': 'Debe seleccionar archivos de cartera y anticipos'})
        
        archivo_cartera = request.files['cartera']
        archivo_anticipos = request.files['anticipos']
        
        if archivo_cartera.filename == '' or archivo_anticipos.filename == '':
            return jsonify({'ok': False, 'error': 'Debe seleccionar ambos archivos'})
        
        # Guardar archivos temporales
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        cartera_filename = secure_filename(archivo_cartera.filename)
        cartera_temp = f"modelo_cartera_{timestamp}_{cartera_filename}"
        cartera_path = os.path.join(app.config['UPLOAD_FOLDER'], cartera_temp)
        archivo_cartera.save(cartera_path)
        
        anticipos_filename = secure_filename(archivo_anticipos.filename)
        anticipos_temp = f"modelo_anticipos_{timestamp}_{anticipos_filename}"
        anticipos_path = os.path.join(app.config['UPLOAD_FOLDER'], anticipos_temp)
        archivo_anticipos.save(anticipos_path)
        
        # Procesar modelo
        config = trm_config.cargar_configuracion()
        trm_usd = config.get('trm_usd', 0.0)
        trm_eur = config.get('trm_eur', 0.0)
        output_path = procesar_modelo_deuda(cartera_path, anticipos_path, trm_usd, trm_eur)
        
        # Obtener TRM actual
        config = trm_config.cargar_configuracion()
        
        return jsonify({
            'ok': True,
            'url': f'/descargar/{os.path.basename(output_path)}',
            'file': os.path.basename(output_path),
            'trm_usd': config.get('trm_usd', ''),
            'trm_eur': config.get('trm_eur', '')
        })
        
    except Exception as e:
        logger.error(f"Error procesando modelo: {e}")
        return jsonify({'ok': False, 'error': str(e)})

@app.route('/api/procesar/balance', methods=['POST'])
def procesar_balance():
    """Procesar archivo de balance"""
    try:
        if 'archivo' not in request.files:
            return jsonify({'ok': False, 'error': 'No se seleccionó ningún archivo'})
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            return jsonify({'ok': False, 'error': 'No se seleccionó ningún archivo'})
        
        if not archivo.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'ok': False, 'error': 'El archivo debe ser un Excel'})
        
        # Guardar archivo temporal
        filename = secure_filename(archivo.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_filename = f"balance_{timestamp}_{filename}"
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        archivo.save(temp_path)
        
        # Procesar balance
        output_path = procesar_balance(temp_path)
        
        # Obtener TRM actual
        config = trm_config.cargar_configuracion()
        
        return jsonify({
            'ok': True,
            'url': f'/descargar/{os.path.basename(output_path)}',
            'file': os.path.basename(output_path),
            'trm_usd': config.get('trm_usd', ''),
            'trm_eur': config.get('trm_eur', '')
        })
        
    except Exception as e:
        logger.error(f"Error procesando balance: {e}")
        return jsonify({'ok': False, 'error': str(e)})

@app.route('/descargar/<filename>')
def descargar_archivo(filename):
    """Descargar archivo procesado"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
    except Exception as e:
        logger.error(f"Error descargando archivo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Endpoint de estado del sistema"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    })

if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Gestión de Cartera - Grupo Planeta")
    print("📊 Versión 2.0.0 - Aplicación Web Python")
    print(f"🌐 Servidor disponible en: http://localhost:{app.config['PORT']}")
    app.run(
        debug=app.config['DEBUG'], 
        host=app.config['HOST'], 
        port=app.config['PORT']
    )
