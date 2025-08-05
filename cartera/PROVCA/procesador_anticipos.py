# -*- coding: utf-8 -*-
"""
PROCESADOR DE ANTICIPOS - GRUPO PLANETA

Este script procesa archivos de anticipos generados por el sistema Pisa, aplicando
las transformaciones y cálculos requeridos por el área de cartera.

OBJETIVO:
Procesar archivos de anticipos para generar reportes estructurados con información
de vencimientos, saldos y cálculos financieros.

PROCESO:
1. Leer archivo de anticipos (Excel/CSV)
2. Limpiar y validar datos
3. Renombrar columnas según mapeo oficial
4. Procesar fechas y crear columnas separadas
5. Calcular días vencidos y por vencer
6. Calcular saldos y dotaciones
7. Aplicar formato colombiano
8. Generar archivo Excel de salida
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Importar utilidades
try:
    from utilidades_cartera import convertir_fecha, convertir_valor, aplicar_formato_colombiano_dataframe
except ImportError:
    # Si no encuentra el módulo, definir funciones básicas
    def convertir_fecha(fecha_str):
        try:
            fecha = datetime.strptime(str(int(fecha_str)), "%Y%m%d")
            return fecha.strftime("%d-%m-%Y"), fecha.day, fecha.month, fecha.year, fecha
        except Exception:
            return "", "", "", "", None

    def convertir_valor(valor_str):
        try:
            if valor_str is None:
                return 0.0
            if isinstance(valor_str, (int, float)):
                return float(valor_str)
            s = str(valor_str).strip().replace('\u200b', '').replace(' ', '')
            if s == '' or s.lower() == 'nan':
                return 0.0
            return float(s)
        except Exception:
            return 0.0

    def aplicar_formato_colombiano_dataframe(df, columnas_numericas=None):
        return df

# Mapeo oficial de columnas para anticipos
MAPEO_ANTICIPOS = {
    'PCCDEM': 'EMPRESA',
    'PCCDAC': 'ACTIVIDAD',
    'PCDEAC': 'EMPRESA',
    'PCCDAG': 'CODIGO AGENTE',
    'PCNMAG': 'AGENTE',
    'PCCDCO': 'CODIGO COBRADOR',
    'PCNMCO': 'COBRADOR',
    'PCCDCL': 'CODIGO CLIENTE',
    'PCCDDN': 'IDENTIFICACION',
    'PCNMCL': 'NOMBRE',
    'PCNMCM': 'DENOMINACION COMERCIAL',
    'PCNMDO': 'DIRECCION',
    'PCTLF1': 'TELEFONO',
    'PCNMPO': 'CIUDAD',
    'PCNUFC': 'NUMERO FACTURA',
    'PCORPD': 'TIPO',
    'PCFEFA': 'FECHA',
    'PCFEVE': 'FECHA VTO',
    'PCVAFA': 'VALOR',
    'PCSALD': 'SALDO'
}

def obtener_fecha_cierre(fecha_cierre_str=None):
    """Obtiene la fecha de cierre. Si se proporciona fecha_cierre_str, la usa; si no, usa el último día del mes actual"""
    if fecha_cierre_str:
        try:
            return datetime.strptime(fecha_cierre_str, '%Y-%m-%d')
        except ValueError:
            print(f"ADVERTENCIA: Formato de fecha incorrecto '{fecha_cierre_str}'. Usando fecha por defecto.")
    
    # Fecha por defecto: último día del mes actual
    hoy = datetime.now()
    if hoy.month == 12:
        cierre = datetime(hoy.year + 1, 1, 1) - pd.Timedelta(days=1)
    else:
        cierre = datetime(hoy.year, hoy.month + 1, 1) - pd.Timedelta(days=1)
    return cierre

def limpiar_y_validar_datos(df):
    """Limpia y valida los datos del DataFrame de anticipos"""
    print("Iniciando limpieza y validación de datos de anticipos...")
    
    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()
    
    # Renombrar columnas según mapeo oficial
    columnas_renombradas = {}
    for col_original, col_nueva in MAPEO_ANTICIPOS.items():
        if col_original in df.columns:
            columnas_renombradas[col_original] = col_nueva
    
    df = df.rename(columns=columnas_renombradas)
    print(f"Columnas renombradas: {len(columnas_renombradas)}")
    
    # Eliminar filas con valores nulos en campos críticos
    registros_antes = len(df)
    df = df.dropna(subset=['SALDO', 'FECHA VTO'], how='all')
    registros_eliminados = registros_antes - len(df)
    if registros_eliminados > 0:
        print(f"Eliminados {registros_eliminados} registros con datos críticos nulos")
    
    return df

def procesar_fechas(df, fecha_cierre_str=None):
    """Procesa las fechas y crea columnas separadas"""
    print("Procesando fechas de anticipos...")
    
    fecha_cierre = obtener_fecha_cierre(fecha_cierre_str)
    
    for col_fecha in ['FECHA', 'FECHA VTO']:
        if col_fecha in df.columns:
            # Convertir fechas
            fechas_convertidas = df[col_fecha].apply(convertir_fecha)
            
            # Formatear fechas en formato dd/mm/yyyy
            fechas_formateadas = []
            dias = []
            meses = []
            años = []
            fechas_datetime = []
            
            for fecha_conv in fechas_convertidas:
                if fecha_conv[0]:  # Si la conversión fue exitosa
                    _, dia, mes, anio, fecha_dt = fecha_conv
                    fechas_formateadas.append(f"{dia:02d}/{mes:02d}/{anio}")
                    dias.append(dia)
                    meses.append(mes)
                    años.append(anio)
                    fechas_datetime.append(fecha_dt)
                else:
                    fechas_formateadas.append("")
                    dias.append("")
                    meses.append("")
                    años.append("")
                    fechas_datetime.append(None)
            
            # Actualizar columna original
            df[col_fecha] = fechas_formateadas
            
            # Crear columnas separadas
            df[f'DIA {col_fecha}'] = dias
            df[f'MES {col_fecha}'] = meses
            df[f'AÑO {col_fecha}'] = años
            
            # Guardar fechas como datetime para cálculos
            df[f'{col_fecha}_DT'] = fechas_datetime
    
    print("Fechas procesadas correctamente")
    return df

def calcular_dias_vencidos(df, fecha_cierre_str=None):
    """Calcula días vencidos y días por vencer para anticipos"""
    print("Calculando días vencidos de anticipos...")
    
    fecha_cierre = obtener_fecha_cierre(fecha_cierre_str)
    
    if 'FECHA VTO_DT' in df.columns and 'SALDO' in df.columns:
        dias_vencidos = []
        dias_por_vencer = []
        
        for fecha_vto in df['FECHA VTO_DT']:
            if fecha_vto and pd.notna(fecha_vto):
                dias_diff = (fecha_vto - fecha_cierre).days
                if dias_diff < 0:
                    # Vencido
                    dias_vencidos.append(abs(dias_diff))
                    dias_por_vencer.append(0)
                else:
                    # Por vencer
                    dias_vencidos.append(0)
                    dias_por_vencer.append(dias_diff)
            else:
                dias_vencidos.append(0)
                dias_por_vencer.append(0)
        
        df['DIAS VENCIDO'] = dias_vencidos
        df['DIAS POR VENCER'] = dias_por_vencer
        
        print("Días vencidos y por vencer calculados correctamente")
    
    return df

def calcular_saldos_anticipos(df):
    """Calcula saldos específicos para anticipos"""
    print("Calculando saldos de anticipos...")
    
    if 'SALDO' in df.columns and 'DIAS VENCIDO' in df.columns:
        # Saldo vencido
        df['SALDO VENCIDO'] = df.apply(
            lambda row: convertir_valor(str(row['SALDO'])) if row['DIAS VENCIDO'] > 0 else 0, axis=1
        )
        
        # Saldo por vencer
        df['SALDO POR VENCER'] = df.apply(
            lambda row: convertir_valor(str(row['SALDO'])) if row['DIAS VENCIDO'] <= 0 else 0, axis=1
        )
        
        # % Dotación (específico para anticipos)
        df['% Dotación'] = df['DIAS VENCIDO'].apply(lambda x: '100%' if x >= 90 else '0%')
        
        # Valor Dotación
        df['Valor Dotación'] = df.apply(
            lambda row: convertir_valor(str(row['SALDO'])) if row['DIAS VENCIDO'] >= 90 else 0, axis=1
        )
        
        print("Saldos de anticipos calculados correctamente")
    
    return df

def aplicar_formato_final(df):
    """Aplica el formato final al DataFrame de anticipos"""
    print("Aplicando formato final a anticipos...")
    
    # Eliminar columnas de datetime
    columnas_a_eliminar = [col for col in df.columns if col.endswith('_DT')]
    if columnas_a_eliminar:
        df = df.drop(columns=columnas_a_eliminar)
    
    # Columnas numéricas que requieren formato colombiano
    columnas_numericas = [
        'SALDO', 'SALDO VENCIDO', 'SALDO POR VENCER', 'Valor Dotación'
    ]
    
    # Filtrar solo las columnas que existen en el DataFrame
    columnas_existentes = [col for col in columnas_numericas if col in df.columns]
    
    # Aplicar formato colombiano
    df = aplicar_formato_colombiano_dataframe(df, columnas_existentes)
    
    # Reemplazar ceros por '-' en columnas numéricas
    for col in columnas_existentes:
        if '%' not in col:
            df[col] = df[col].replace(['0', '0,00', '0.00', '0,0', '0.0'], '-')
    
    print("Formato final aplicado correctamente")
    return df

def procesar_anticipos(input_path, output_path=None, fecha_cierre_str=None):
    """
    Procesa el archivo de anticipos según las especificaciones
    """
    print("=" * 80)
    print("PROCESADOR DE ANTICIPOS - GRUPO PLANETA")
    print("=" * 80)
    
    if fecha_cierre_str:
        print(f"Fecha de cierre especificada: {fecha_cierre_str}")
    else:
        print("Usando fecha de cierre por defecto (último día del mes actual)")
    
    try:
        # Leer archivo
        print(f"Leyendo archivo: {input_path}")
        
        # Intentar leer como Excel primero
        try:
            df = pd.read_excel(input_path, dtype=str)
        except:
            # Si falla, intentar como CSV
            df = pd.read_csv(input_path, sep=';', encoding='latin1', dtype=str)
        
        print(f"Archivo leído correctamente. Registros: {len(df)}")
        
        # Procesar datos
        df = limpiar_y_validar_datos(df)
        df = procesar_fechas(df, fecha_cierre_str)
        df = calcular_dias_vencidos(df, fecha_cierre_str)
        df = calcular_saldos_anticipos(df)
        df = aplicar_formato_final(df)
        
        # Definir carpeta de salida
        output_dir = r'C:\wamp64\www\modelo-deuda-python\cartera\resultados'
        os.makedirs(output_dir, exist_ok=True)
        
        if not output_path:
            ahora = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            output_path = os.path.join(output_dir, f'ANTICIPOS_PROCESADOS_{ahora}.xlsx')
        
        # Verificar que el DataFrame no esté vacío
        if df.empty:
            print("ERROR: El DataFrame está vacío. No se puede generar archivo.")
            return None
        
        # Guardar archivo Excel
        print(f"Guardando archivo: {output_path}")
        df.to_excel(output_path, index=False)
        
        # Verificar que el archivo se creó correctamente
        if not os.path.exists(output_path):
            print("ERROR: No se pudo crear el archivo Excel.")
            return None
        
        if os.path.getsize(output_path) == 0:
            print("ERROR: El archivo Excel está vacío.")
            os.remove(output_path)
            return None
        
        # Resumen final
        print("\n" + "=" * 80)
        print("PROCESAMIENTO DE ANTICIPOS COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        print(f"Archivo procesado: {input_path}")
        print(f"Archivo generado: {output_path}")
        print(f"Registros procesados: {len(df)}")
        print(f"Columnas generadas: {len(df.columns)}")
        
        # Mostrar columnas principales
        columnas_principales = [
            'EMPRESA', 'CODIGO CLIENTE', 'NOMBRE', 'DENOMINACION COMERCIAL',
            'NUMERO FACTURA', 'FECHA VTO', 'SALDO', 'DIAS VENCIDO',
            'SALDO VENCIDO', 'SALDO POR VENCER', '% Dotación', 'Valor Dotación'
        ]
        print(f"\nColumnas principales: {[col for col in columnas_principales if col in df.columns]}")
        
        return output_path
        
    except Exception as e:
        print(f"ERROR durante el procesamiento: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        fecha_cierre = sys.argv[2] if len(sys.argv) > 2 else None
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        procesar_anticipos(input_file, output_file, fecha_cierre)
    else:
        print("Uso: python procesador_anticipos.py <ruta_entrada> [<fecha_cierre_YYYY-MM-DD>] [<ruta_salida_excel>]") 