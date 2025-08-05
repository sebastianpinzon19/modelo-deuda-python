#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import sys
import os
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_archivo_excel(file_path: str, max_rows: int = 5) -> dict:
    """Analiza un archivo Excel y devuelve información de debug"""
    try:
        # Obtener información del archivo
        file_size = os.path.getsize(file_path)
        file_extension = Path(file_path).suffix.lower()
        
        # Leer el archivo Excel
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Información básica
        total_rows = len(df)
        total_columns = len(df.columns)
        
        # Obtener nombres de columnas
        columnas = df.columns.tolist()
        
        # Obtener primeras filas como muestra
        muestra_filas = df.head(max_rows).to_dict('records')
        
        # Convertir a formato JSON serializable
        for fila in muestra_filas:
            for key, value in fila.items():
                if pd.isna(value):
                    fila[key] = None
                elif isinstance(value, (int, float)):
                    fila[key] = float(value) if isinstance(value, float) else int(value)
                else:
                    fila[key] = str(value)
        
        return {
            'archivo': os.path.basename(file_path),
            'tamaño_bytes': file_size,
            'extension': file_extension,
            'total_filas': total_rows,
            'total_columnas': total_columns,
            'nombres_columnas': columnas,
            'muestra_filas': muestra_filas,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Error procesando {file_path}: {str(e)}")
        return {
            'archivo': os.path.basename(file_path),
            'error': str(e),
            'tamaño_bytes': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            'extension': Path(file_path).suffix.lower() if os.path.exists(file_path) else '',
            'total_filas': 0,
            'total_columnas': 0,
            'nombres_columnas': [],
            'muestra_filas': []
        }

def main():
    """Función principal para debug"""
    if len(sys.argv) != 4:
        print("Uso: python debug_balance_python.py <archivo_balance> <archivo_situacion> <archivo_focus>")
        sys.exit(1)
    
    balance_file = sys.argv[1]
    situacion_file = sys.argv[2]
    focus_file = sys.argv[3]
    
    # Verificar que los archivos existan
    for file_path in [balance_file, situacion_file, focus_file]:
        if not os.path.exists(file_path):
            print(f"Error: El archivo {file_path} no existe")
            sys.exit(1)
    
    try:
        # Debug de cada archivo
        debug_balance = debug_archivo_excel(balance_file)
        debug_situacion = debug_archivo_excel(situacion_file)
        debug_focus = debug_archivo_excel(focus_file)
        
        # Crear resultado final
        resultado = {
            'balance': debug_balance,
            'situacion': debug_situacion,
            'focus': debug_focus,
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        # Guardar en archivo JSON
        with open('debug_balance.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        
        print("Debug completado. Resultados guardados en debug_balance.json")
        
    except Exception as e:
        logger.error(f"Error en el debug: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 