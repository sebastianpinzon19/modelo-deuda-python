"""
AREA DE CARTERA - PROCESO FORMATO DEUDA

Este script procesa el archivo de anticipos generado por el sistema Pisa, siguiendo las reglas y transformaciones requeridas por el área de cartera:
- Renombra los campos según el mapeo oficial.
- Multiplica el valor de anticipo por -1 (deben ser negativos).
- Formatea la fecha de anticipo.
- Aplica formato colombiano a los números (puntos para miles, comas para decimales).

Este script NO realiza unificación ni combinación con archivos de provisión ni otros modelos. Solo genera el archivo de anticipos modificado de forma independiente.
"""
# procesador_anticipos.py
import pandas as pd
import os
import sys
from datetime import datetime
from utilidades import aplicar_formato_colombiano_dataframe

MAPEO_ANTICIPO = {
    'NCCDEM': 'EMPRESA',
    'NCCDAC': 'ACTIVIDAD',
    'NCCDCL': 'CODIGO CLIENTE',
    'WWNIT': 'NIT/CEDULA',
    'WWNMCL': 'NOMBRE COMERCIAL',
    'WWNMDO': 'DIRECCION',
    'WWTLF1': 'TELEFONO',
    'WWNMPO': 'POBLACION',
    'CCCDFB': 'CODIGO AGENTE',
    'BDNMNM': 'NOMBRE AGENTE',
    'BDNMPA': 'APELLIDO AGENTE',
    'NCMOMO': 'TIPO ANTICIPO',
    'NCCDR3': 'NRO ANTICIPO',
    'NCIMAN': 'VALOR ANTICIPO',
    'NCFEGR': 'FECHA ANTICIPO'
}

def procesar_anticipos(input_path, output_path=None):
        
    df = pd.read_csv(input_path, sep=';', encoding='latin1', dtype=str)
    # Renombrar columnas si existen en el mapeo
    df = df.rename(columns={k: v for k, v in MAPEO_ANTICIPO.items() if k in df.columns})
    # Multiplicar por -1 el valor de anticipo si existe la columna
    if 'VALOR ANTICIPO' in df.columns:
        # Limpiar y convertir a número
        df['VALOR ANTICIPO'] = (
            df['VALOR ANTICIPO']
            .astype(str)
            .str.replace('.', '', regex=False)   # Quita puntos de miles
            .str.replace(',', '.', regex=False)  # Cambia coma decimal por punto
        )
        df['VALOR ANTICIPO'] = pd.to_numeric(df['VALOR ANTICIPO'], errors='coerce').fillna(0)
        df['VALOR ANTICIPO'] = df['VALOR ANTICIPO'] * -1
    # Formatear fecha de anticipo si existe
    if 'FECHA ANTICIPO' in df.columns:
        df['FECHA ANTICIPO'] = pd.to_datetime(df['FECHA ANTICIPO'], errors='coerce').dt.strftime('%d-%m-%Y')
    
    # Aplicar formato colombiano a los números
    if 'VALOR ANTICIPO' in df.columns:
        df = aplicar_formato_colombiano_dataframe(df, ['VALOR ANTICIPO'])
    
    # Verificar que el DataFrame no esté vacío
    if df.empty:
        print("ERROR: El DataFrame está vacío. No se puede generar archivo.")
        return
    
    # Verificar que hay al menos una fila de datos
    if len(df) == 0:
        print("ERROR: No hay datos para procesar. No se puede generar archivo.")
        return
    
    # Verificar que hay columnas
    if len(df.columns) == 0:
        print("ERROR: No hay columnas en el DataFrame. No se puede generar archivo.")
        return
    
    # Definir carpeta de salida FIJA
    output_dir = r'C:\wamp64\www\cartera\PROVCA_PROCESADOS'
    os.makedirs(output_dir, exist_ok=True)
    if not output_path:
        ahora = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = os.path.join(output_dir, f'ANTICIPO_PROCESADO_{ahora}.xlsx')
    
    df.to_excel(output_path, index=False)
    
    # Verificar que el archivo se creó correctamente
    if not os.path.exists(output_path):
        print("ERROR: No se pudo crear el archivo Excel.")
        return
    
    if os.path.getsize(output_path) == 0:
        print("ERROR: El archivo Excel está vacío.")
        os.remove(output_path)  # Eliminar archivo vacío
        return
    
    print(f"Archivo de anticipos procesado y guardado en: {output_path}")
    print(f"Registros procesados: {len(df)}")
    print(f"Columnas generadas: {len(df.columns)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        procesar_anticipos(input_file, output_file)
    else:
        print("Uso: python procesador_anticipos.py <ruta_entrada_excel> [<ruta_salida_excel>]") 