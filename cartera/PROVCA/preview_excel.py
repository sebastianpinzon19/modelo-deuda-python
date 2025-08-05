#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para previsualizar archivos Excel y CSV
Muestra información básica del archivo antes del procesamiento
"""

import pandas as pd
import sys
import json
import os
from datetime import datetime
import traceback

def previsualizar_archivo(ruta_archivo):
    """
    Previsualiza un archivo Excel o CSV y retorna información básica
    """
    try:
        # Verificar que el archivo existe
        if not os.path.exists(ruta_archivo):
            return {
                'error': f'El archivo no existe: {ruta_archivo}'
            }

        # Obtener información del archivo
        stat_info = os.stat(ruta_archivo)
        tamaño = stat_info.st_size
        fecha_modificacion = datetime.fromtimestamp(stat_info.st_mtime)

        # Determinar el tipo de archivo
        extension = os.path.splitext(ruta_archivo)[1].lower()
        
        # Leer el archivo según su tipo
        if extension == '.csv':
            # Intentar detectar el encoding y separador
            encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
            separators = [';', ',', '\t']  # Punto y coma primero para archivos europeos
            df = None
            
            for encoding in encodings:
                for sep in separators:
                    try:
                        df = pd.read_csv(ruta_archivo, encoding=encoding, sep=sep, nrows=1000, on_bad_lines='skip', quotechar='"')
                        # Verificar que se leyó correctamente (más de una columna)
                        if len(df.columns) > 1:
                            break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        continue
                if df is not None and len(df.columns) > 1:
                    break
            
            # Si no se pudo leer correctamente, intentar con engine='python'
            if df is None or len(df.columns) <= 1:
                for encoding in encodings:
                    for sep in separators:
                        try:
                            df = pd.read_csv(ruta_archivo, encoding=encoding, sep=sep, nrows=1000, 
                                           on_bad_lines='skip', quotechar='"', engine='python')
                            if len(df.columns) > 1:
                                break
                        except UnicodeDecodeError:
                            continue
                        except Exception as e:
                            continue
                    if df is not None and len(df.columns) > 1:
                        break
            
            if df is None or len(df.columns) <= 1:
                return {
                    'error': 'No se pudo leer el archivo CSV correctamente. Verificar el separador y formato.'
                }
        else:
            # Archivo Excel
            try:
                df = pd.read_excel(ruta_archivo, nrows=1000)
            except Exception as e:
                return {
                    'error': f'Error al leer archivo Excel: {str(e)}'
                }

        # Información básica del archivo
        info_archivo = {
            'nombre': os.path.basename(ruta_archivo),
            'tamaño': tamaño,
            'tamaño_formateado': formatear_tamaño(tamaño),
            'fecha_modificacion': fecha_modificacion.strftime('%d/%m/%Y %H:%M:%S'),
            'tipo': 'Excel' if extension != '.csv' else 'CSV',
            'extension': extension
        }

        # Información del DataFrame
        info_dataframe = {
            'filas_totales': len(df),
            'columnas': len(df.columns),
            'nombres_columnas': df.columns.tolist(),
            'tipos_datos': df.dtypes.astype(str).to_dict(),
            'filas_con_datos': df.count().to_dict(),
            'valores_unicos': {col: df[col].nunique() for col in df.columns},
            'valores_nulos': df.isnull().sum().to_dict()
        }

        # Muestra de datos (primeras 5 filas)
        muestra_datos = df.head(5).fillna('').astype(str).to_dict('records')

        # Análisis de columnas numéricas
        columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
        info_numericas = {}
        
        for col in columnas_numericas:
            try:
                valores = pd.to_numeric(df[col], errors='coerce').dropna()
                if len(valores) > 0:
                    info_numericas[col] = {
                        'min': float(valores.min()),
                        'max': float(valores.max()),
                        'promedio': float(valores.mean()),
                        'total': float(valores.sum()),
                        'valores_validos': len(valores)
                    }
            except:
                continue

        # Detectar posibles problemas
        problemas = []
        
        # Verificar columnas vacías
        columnas_vacias = [col for col in df.columns if df[col].isnull().all()]
        if columnas_vacias:
            problemas.append(f"Columnas completamente vacías: {', '.join(columnas_vacias)}")

        # Verificar filas duplicadas
        filas_duplicadas = df.duplicated().sum()
        if filas_duplicadas > 0:
            problemas.append(f"Filas duplicadas encontradas: {filas_duplicadas}")

        # Verificar valores extremos en columnas numéricas
        for col in columnas_numericas:
            if col in info_numericas:
                valores = pd.to_numeric(df[col], errors='coerce').dropna()
                if len(valores) > 0:
                    q1 = valores.quantile(0.25)
                    q3 = valores.quantile(0.75)
                    iqr = q3 - q1
                    outliers = valores[(valores < (q1 - 1.5 * iqr)) | (valores > (q3 + 1.5 * iqr))]
                    if len(outliers) > 0:
                        problemas.append(f"Valores atípicos en '{col}': {len(outliers)} valores")

        # Verificar formato de fechas
        columnas_fecha = []
        for col in df.columns:
            if df[col].dtype == 'object':
                # Intentar convertir a fecha
                try:
                    pd.to_datetime(df[col].head(10), errors='raise')
                    columnas_fecha.append(col)
                except:
                    continue

        return {
            'success': True,
            'archivo': info_archivo,
            'estructura': info_dataframe,
            'muestra': muestra_datos,
            'analisis_numerico': info_numericas,
            'columnas_fecha': columnas_fecha,
            'problemas': problemas,
            'recomendaciones': generar_recomendaciones(info_dataframe, problemas)
        }

    except Exception as e:
        return {
            'error': f'Error al previsualizar archivo: {str(e)}',
            'traceback': traceback.format_exc()
        }

def formatear_tamaño(bytes):
    """Formatea el tamaño en bytes a formato legible"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} TB"

def generar_recomendaciones(info_dataframe, problemas):
    """Genera recomendaciones basadas en el análisis del archivo"""
    recomendaciones = []
    
    # Recomendaciones basadas en el número de filas
    if info_dataframe['filas_totales'] > 10000:
        recomendaciones.append("Archivo grande detectado. El procesamiento puede tomar varios minutos.")
    
    # Recomendaciones basadas en columnas vacías
    columnas_vacias = [col for col in info_dataframe['nombres_columnas'] 
                      if info_dataframe['valores_nulos'][col] == info_dataframe['filas_totales']]
    if columnas_vacias:
        recomendaciones.append(f"Considerar eliminar columnas vacías: {', '.join(columnas_vacias)}")
    
    # Recomendaciones basadas en problemas detectados
    if problemas:
        recomendaciones.append("Se detectaron posibles problemas. Revisar antes del procesamiento.")
    
    # Recomendaciones generales
    if info_dataframe['columnas'] > 20:
        recomendaciones.append("Archivo con muchas columnas. Verificar que todas sean necesarias.")
    
    if not recomendaciones:
        recomendaciones.append("Archivo parece estar en buen formato para el procesamiento.")
    
    return recomendaciones

def main():
    """Función principal"""
    if len(sys.argv) != 2:
        print(json.dumps({
            'error': 'Uso: python preview_excel.py <ruta_archivo>'
        }))
        sys.exit(1)
    
    ruta_archivo = sys.argv[1]
    resultado = previsualizar_archivo(ruta_archivo)
    
    # Imprimir resultado como JSON
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 