# -*- coding: utf-8 -*-
"""
PROCESADOR FORMATO DEUDA - GRUPO PLANETA

Este script implementa el proceso completo de formato deuda según las especificaciones
de los documentos Word del área de cartera.

OBJETIVO:
Generar el formato de deuda completo con información de provisión, anticipos, balance,
situación y focus, aplicando todas las transformaciones y cálculos especificados.

PROCESO:
1. Procesar archivo de provisión (PROVCA)
2. Procesar archivo de anticipos (ANTICI)
3. Crear modelo de deuda con hojas de pesos y divisas
4. Procesar archivos de balance, situación y focus
5. Generar formato de deuda final
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import os
import sys
import json
import warnings
warnings.filterwarnings('ignore')

# Importar utilidades
try:
    from utilidades_cartera import convertir_fecha, convertir_valor, aplicar_formato_colombiano_dataframe
except ImportError:
    # Fallback si no encuentra las utilidades
    def convertir_fecha(fecha_str):
        try:
            if pd.isna(fecha_str) or fecha_str == '':
                return None, None, None, None, None
            fecha_str = str(fecha_str).strip()
            if len(fecha_str) == 8:  # YYYYMMDD
                fecha = datetime.strptime(fecha_str, '%Y%m%d')
            else:
                fecha = pd.to_datetime(fecha_str)
            return fecha.strftime('%d-%m-%Y'), fecha.day, fecha.month, fecha.year, fecha
        except:
            return None, None, None, None, None
    
    def convertir_valor(valor_str):
        try:
            if pd.isna(valor_str) or valor_str == '':
                return 0.0
            valor_str = str(valor_str).strip()
            # Limpiar caracteres problemáticos
            valor_str = valor_str.replace(' ', '').replace(',', '.').replace('nan', '0')
            return float(valor_str)
        except:
            return 0.0
    
    def aplicar_formato_colombiano_dataframe(df, columnas_numericas=None):
        return df

# Mapeo oficial de columnas para provisión
MAPEO_PROVISION = {
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

# Mapeo oficial de columnas para anticipos
MAPEO_ANTICIPOS = {
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

# Tabla de códigos de negocio-canal
TABLA_NEGOCIO_CANAL = {
    'CT80': {'NEGOCIO': 'TINTA CLUB DEL LIBRO', 'CANAL': 'CT80', 'MONEDA': 'PESOS COL'},
    'ED41': {'NEGOCIO': 'PLANETA CREDI. ELITE 2000', 'CANAL': 'ED41', 'MONEDA': 'PESOS COL'},
    'ED44': {'NEGOCIO': 'PLANETA VENTA DIGITAL', 'CANAL': 'ED44', 'MONEDA': 'PESOS COL'},
    'ED47': {'NEGOCIO': 'EVENTOS FERIA CREDITO', 'CANAL': 'ED47', 'MONEDA': 'PESOS COL'},
    'PL10': {'NEGOCIO': 'MERMA GRANDES SUPERFICIES', 'CANAL': 'PL10', 'MONEDA': 'PESOS COL'},
    'PL15': {'NEGOCIO': 'MARKETING DIRECTO - WEB', 'CANAL': 'PL15', 'MONEDA': 'PESOS COL'},
    'PL20': {'NEGOCIO': 'LIBRERIAS (PLANETA)', 'CANAL': 'PL20', 'MONEDA': 'PESOS COL'},
    'PL21': {'NEGOCIO': 'LIBRERIA GDES SUPERFICIES', 'CANAL': 'PL21', 'MONEDA': 'PESOS COL'},
    'PL23': {'NEGOCIO': 'EVENTOS FERIAS LIBRERIA 1', 'CANAL': 'PL23', 'MONEDA': 'PESOS COL'},
    'PL25': {'NEGOCIO': 'DISTRIBUIDORA - PLANETA', 'CANAL': 'PL25', 'MONEDA': 'PESOS COL'},
    'PL28': {'NEGOCIO': 'VENTA SALDOS LIBRERIAS', 'CANAL': 'PL28', 'MONEDA': 'PESOS COL'},
    'PL29': {'NEGOCIO': 'VENTA SALDOS DISTR/BDORA', 'CANAL': 'PL29', 'MONEDA': 'PESOS COL'},
    'PL31': {'NEGOCIO': 'PLACISMO - COLOMBIANA', 'CANAL': 'PL31', 'MONEDA': 'PESOS COL'},
    'PL32': {'NEGOCIO': 'DISTRIBUCION DE TERCEROS', 'CANAL': 'PL32', 'MONEDA': 'PESOS COL'},
    'PL53': {'NEGOCIO': 'FERIA PLANETA LECTOR', 'CANAL': 'PL53', 'MONEDA': 'PESOS COL'},
    'PL56': {'NEGOCIO': 'VENTA DIGITAL LIBRERIAS', 'CANAL': 'PL56', 'MONEDA': 'PESOS COL'},
    'PL60': {'NEGOCIO': 'VENTA INSTITUCIONAL', 'CANAL': 'PL60', 'MONEDA': 'PESOS COL'},
    'PL62': {'NEGOCIO': 'NEGOCIO PERIODICOS', 'CANAL': 'PL62', 'MONEDA': 'PESOS COL'},
    'PL63': {'NEGOCIO': 'CANAL PROMOCION ESCOLAR', 'CANAL': 'PL63', 'MONEDA': 'PESOS COL'},
    'PL64': {'NEGOCIO': 'NEGOCIO LICITACIONES', 'CANAL': 'PL64', 'MONEDA': 'PESOS COL'},
    'PL65': {'NEGOCIO': 'VENTA CLIENTES ESPECIALES', 'CANAL': 'PL65', 'MONEDA': 'PESOS COL'},
    'PL66': {'NEGOCIO': 'AULA PLANETA', 'CANAL': 'PL66', 'MONEDA': 'PESOS COL'},
    'PL69': {'NEGOCIO': 'VENTA AUTORES SIN DERECHO', 'CANAL': 'PL69', 'MONEDA': 'PESOS COL'},
    # Divisas
    'PL11': {'NEGOCIO': 'TERCEROS DOLARES N.E.', 'CANAL': 'PL11', 'MONEDA': 'DOLAR'},
    'PL18': {'NEGOCIO': 'COLOMBIANA TERCEROS DOLARES', 'CANAL': 'PL18', 'MONEDA': 'DOLAR'},
    'PL57': {'NEGOCIO': 'COLOMBIANA AULA PLANETA DOLARES', 'CANAL': 'PL57', 'MONEDA': 'DOLAR'},
    'PL41': {'NEGOCIO': 'COLOMBIANA TERCEROS EURO N.E.', 'CANAL': 'PL41', 'MONEDA': 'EURO'}
}

def obtener_fecha_cierre(fecha_cierre_str=None):
    """Obtiene la fecha de cierre del mes"""
    if fecha_cierre_str:
        try:
            return datetime.strptime(fecha_cierre_str, '%Y-%m-%d')
        except:
            pass
    
    # Por defecto, último día del mes anterior
    hoy = date.today()
    primer_dia_mes = date(hoy.year, hoy.month, 1)
    ultimo_dia_mes_anterior = primer_dia_mes - pd.Timedelta(days=1)
    return datetime.combine(ultimo_dia_mes_anterior, datetime.min.time())

def procesar_archivo_provision(ruta_archivo, fecha_cierre_str=None):
    """Procesa el archivo de provisión según las especificaciones"""
    print("Procesando archivo de provisión...")
    
    # Leer archivo
    df = pd.read_csv(ruta_archivo, encoding='latin1')
    
    # Renombrar columnas
    df = df.rename(columns=MAPEO_PROVISION)
    
    # Eliminar columna PCIMCO si existe
    if 'PCIMCO' in df.columns:
        df = df.drop('PCIMCO', axis=1)
    
    # Eliminar fila PL30
    df = df[df['ACTIVIDAD'] != 30]
    
    # Unificar nombres de clientes
    df['DENOMINACION COMERCIAL'] = df['DENOMINACION COMERCIAL'].fillna('')
    df['NOMBRE'] = df['NOMBRE'].fillna('')
    df['DENOMINACION COMERCIAL'] = df.apply(
        lambda row: row['NOMBRE'] if row['DENOMINACION COMERCIAL'] == '' else row['DENOMINACION COMERCIAL'], 
        axis=1
    )
    
    # Procesar fechas
    fecha_cierre = obtener_fecha_cierre(fecha_cierre_str)
    
    # Convertir fechas de factura y vencimiento
    df['FECHA_FORMATO'] = df['FECHA'].apply(lambda x: convertir_fecha(x)[0])
    df['FECHA_VTO_FORMATO'] = df['FECHA VTO'].apply(lambda x: convertir_fecha(x)[0])
    
    # Crear columnas de fecha separadas
    df['DIA_VTO'] = df['FECHA VTO'].apply(lambda x: convertir_fecha(x)[1])
    df['MES_VTO'] = df['FECHA VTO'].apply(lambda x: convertir_fecha(x)[2])
    df['AÑO_VTO'] = df['FECHA VTO'].apply(lambda x: convertir_fecha(x)[3])
    
    # Calcular días vencidos
    df['DIAS_VENCIDO'] = df['FECHA VTO'].apply(
        lambda x: (fecha_cierre - convertir_fecha(x)[4]).days if convertir_fecha(x)[4] else 0
    )
    
    # Calcular días por vencer
    df['DIAS_POR_VENCER'] = df['FECHA VTO'].apply(
        lambda x: (convertir_fecha(x)[4] - fecha_cierre).days if convertir_fecha(x)[4] else 0
    )
    
    # Calcular saldo vencido
    df['SALDO_VENCIDO'] = df.apply(
        lambda row: row['SALDO'] if row['DIAS_VENCIDO'] > 0 else 0, axis=1
    )
    
    # Calcular % dotación (100% si >= 180 días)
    df['%_DOTACION'] = df['DIAS_VENCIDO'].apply(
        lambda x: 100 if x >= 180 else 0
    )
    
    # Calcular valor dotación
    df['VALOR_DOTACION'] = df.apply(
        lambda row: row['SALDO'] if row['DIAS_VENCIDO'] >= 180 else 0, axis=1
    )
    
    # Calcular vencimientos históricos (últimos 6 meses)
    for i in range(1, 7):
        mes_anterior = fecha_cierre - pd.DateOffset(months=i)
        df[f'VENCIDO_MES_{i}'] = df['FECHA VTO'].apply(
            lambda x: convertir_valor(x) if convertir_fecha(x)[4] and convertir_fecha(x)[4].month == mes_anterior.month else 0
        )
    
    # Calcular mora total
    df['MORA_TOTAL'] = df['SALDO_VENCIDO']
    
    # Calcular valores por vencer (próximos 3 meses)
    for i in range(1, 4):
        mes_futuro = fecha_cierre + pd.DateOffset(months=i)
        df[f'POR_VENCER_MES_{i}'] = df['FECHA VTO'].apply(
            lambda x: convertir_valor(x) if convertir_fecha(x)[4] and convertir_fecha(x)[4].month == mes_futuro.month else 0
        )
    
    # Calcular valor por vencer +90 días
    df['POR_VENCER_+90_DIAS'] = df.apply(
        lambda row: row['SALDO'] if row['DIAS_POR_VENCER'] > 90 else 0, axis=1
    )
    
    # Calcular valor total por vencer
    df['VALOR_TOTAL_POR_VENCER'] = df.apply(
        lambda row: row['SALDO'] if row['DIAS_VENCIDO'] <= 0 else 0, axis=1
    )
    
    # Validar que mora total + valor total por vencer = saldo
    df['VALIDACION_SALDO'] = df['MORA_TOTAL'] + df['VALOR_TOTAL_POR_VENCER'] - df['SALDO']
    
    # Crear columnas de vencimientos por rango
    df['SALDO_NO_VENCIDO'] = df.apply(
        lambda row: row['SALDO'] if 0 <= row['DIAS_VENCIDO'] <= 29 else 0, axis=1
    )
    df['VENCIDO_30'] = df.apply(
        lambda row: row['SALDO'] if 30 <= row['DIAS_VENCIDO'] <= 59 else 0, axis=1
    )
    df['VENCIDO_60'] = df.apply(
        lambda row: row['SALDO'] if 60 <= row['DIAS_VENCIDO'] <= 89 else 0, axis=1
    )
    df['VENCIDO_90'] = df.apply(
        lambda row: row['SALDO'] if 90 <= row['DIAS_VENCIDO'] <= 179 else 0, axis=1
    )
    df['VENCIDO_180'] = df.apply(
        lambda row: row['SALDO'] if 180 <= row['DIAS_VENCIDO'] <= 359 else 0, axis=1
    )
    df['VENCIDO_360'] = df.apply(
        lambda row: row['SALDO'] if 360 <= row['DIAS_VENCIDO'] <= 369 else 0, axis=1
    )
    df['VENCIDO_+360'] = df.apply(
        lambda row: row['SALDO'] if row['DIAS_VENCIDO'] >= 370 else 0, axis=1
    )
    
    # Validar suma de vencimientos
    df['VALIDACION_VENCIMIENTOS'] = (
        df['SALDO_NO_VENCIDO'] + df['VENCIDO_30'] + df['VENCIDO_60'] + 
        df['VENCIDO_90'] + df['VENCIDO_180'] + df['VENCIDO_360'] + df['VENCIDO_+360'] - df['SALDO']
    )
    
    # Crear columna de deuda incobrable
    df['DEUDA_INCOBRABLE'] = df['VALOR_DOTACION']
    
    # Aplicar formato colombiano
    df = aplicar_formato_colombiano_dataframe(df)
    
    return df

def procesar_archivo_anticipos(ruta_archivo, fecha_cierre_str=None):
    """Procesa el archivo de anticipos según las especificaciones"""
    print("Procesando archivo de anticipos...")
    
    # Leer archivo
    df = pd.read_csv(ruta_archivo, encoding='latin1')
    
    # Renombrar columnas
    df = df.rename(columns=MAPEO_ANTICIPOS)
    
    # Multiplicar valor de anticipo por -1 (deben ser negativos)
    df['VALOR ANTICIPO'] = df['VALOR ANTICIPO'] * -1
    
    # Procesar fechas
    df['FECHA_ANTICIPO_FORMATO'] = df['FECHA ANTICIPO'].apply(lambda x: convertir_fecha(x)[0])
    
    # Crear columnas compatibles con provisión
    df['EMPRESA'] = df['EMPRESA'].fillna('')
    df['ACTIVIDAD'] = df['ACTIVIDAD'].fillna('')
    df['CODIGO_CLIENTE'] = df['CODIGO CLIENTE'].fillna('')
    df['IDENTIFICACION'] = df['NIT/CEDULA'].fillna('')
    df['NOMBRE'] = df['NOMBRE COMERCIAL'].fillna('')
    df['DENOMINACION_COMERCIAL'] = df['NOMBRE COMERCIAL'].fillna('')
    df['DIRECCION'] = df['DIRECCION'].fillna('')
    df['TELEFONO'] = df['TELEFONO'].fillna('')
    df['CIUDAD'] = df['POBLACION'].fillna('')
    df['NUMERO_FACTURA'] = df['NRO ANTICIPO'].fillna('')
    df['TIPO'] = df['TIPO ANTICIPO'].fillna('')
    df['FECHA'] = df['FECHA ANTICIPO']
    df['FECHA_VTO'] = df['FECHA ANTICIPO']  # Para anticipos, fecha de vencimiento = fecha de anticipo
    df['VALOR'] = df['VALOR ANTICIPO']
    df['SALDO'] = df['VALOR ANTICIPO']
    
    # Aplicar formato colombiano
    df = aplicar_formato_colombiano_dataframe(df)
    
    return df

def crear_modelo_deuda(df_provision, df_anticipos, fecha_cierre_str=None):
    """Crea el modelo de deuda con hojas de pesos y divisas"""
    print("Creando modelo de deuda...")
    
    # Filtrar líneas en pesos (ACTIVIDAD != 11, 18, 41, 57)
    df_pesos = df_provision[~df_provision['ACTIVIDAD'].isin([11, 18, 41, 57])].copy()
    
    # Filtrar líneas en divisas (ACTIVIDAD = 11, 18, 41, 57)
    df_divisas = df_provision[df_provision['ACTIVIDAD'].isin([11, 18, 41, 57])].copy()
    
    # Agregar anticipos a cada hoja
    df_pesos = pd.concat([df_pesos, df_anticipos], ignore_index=True)
    df_divisas = pd.concat([df_divisas, df_anticipos], ignore_index=True)
    
    # Crear hoja de vencimientos
    df_vencimientos = crear_hoja_vencimientos(df_pesos, df_divisas)
    
    return {
        'pesos': df_pesos,
        'divisas': df_divisas,
        'vencimientos': df_vencimientos
    }

def crear_hoja_vencimientos(df_pesos, df_divisas):
    """Crea la hoja de vencimientos con totales por línea"""
    print("Creando hoja de vencimientos...")
    
    # Combinar datos de pesos y divisas
    df_combinado = pd.concat([df_pesos, df_divisas], ignore_index=True)
    
    # Agrupar por cliente y calcular totales
    df_vencimientos = df_combinado.groupby(['DENOMINACION COMERCIAL', 'ACTIVIDAD']).agg({
        'SALDO': 'sum',
        'SALDO_NO_VENCIDO': 'sum',
        'VENCIDO_30': 'sum',
        'VENCIDO_60': 'sum',
        'VENCIDO_90': 'sum',
        'VENCIDO_180': 'sum',
        'VENCIDO_360': 'sum',
        'VENCIDO_+360': 'sum',
        'DEUDA_INCOBRABLE': 'sum'
    }).reset_index()
    
    # Agregar información de negocio-canal
    df_vencimientos['CODIGO_NEGOCIO'] = df_vencimientos['ACTIVIDAD'].apply(
        lambda x: f"PL{x}" if x in [11, 18, 41, 57] else f"PL{x}"
    )
    
    return df_vencimientos

def procesar_archivos_adicionales(ruta_balance, ruta_situacion, ruta_focus):
    """Procesa los archivos adicionales (balance, situación, focus)"""
    print("Procesando archivos adicionales...")
    
    resultados = {}
    
    # Procesar archivo balance
    if ruta_balance and os.path.exists(ruta_balance):
        df_balance = pd.read_excel(ruta_balance)
        # Extraer cuentas específicas según especificaciones
        cuentas_balance = ['0080.43002.20', '0080.43002.21', '0080.43002.15', 
                          '0080.43002.28', '0080.43002.31', '0080.43002.63']
        df_balance_filtrado = df_balance[df_balance['Número cuenta'].isin(cuentas_balance)]
        resultados['balance'] = df_balance_filtrado
    
    # Procesar archivo situación
    if ruta_situacion and os.path.exists(ruta_situacion):
        df_situacion = pd.read_excel(ruta_situacion)
        # Extraer valor TOTAL 01010 Columna SALDOS MES
        resultados['situacion'] = df_situacion
    
    # Procesar archivo focus
    if ruta_focus and os.path.exists(ruta_focus):
        df_focus = pd.read_excel(ruta_focus)
        resultados['focus'] = df_focus
    
    return resultados

def generar_formato_deuda_final(modelo_deuda, archivos_adicionales, output_path=None):
    """Genera el formato de deuda final en Excel"""
    print("Generando formato de deuda final...")
    
    if output_path is None:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = f'../resultados/FORMATO_DEUDA_{timestamp}.xlsx'
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Crear archivo Excel con múltiples hojas
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Hoja de pesos
        modelo_deuda['pesos'].to_excel(writer, sheet_name='PESOS', index=False)
        
        # Hoja de divisas
        modelo_deuda['divisas'].to_excel(writer, sheet_name='DIVISAS', index=False)
        
        # Hoja de vencimientos
        modelo_deuda['vencimientos'].to_excel(writer, sheet_name='VENCIMIENTOS', index=False)
        
        # Hojas de archivos adicionales
        if 'balance' in archivos_adicionales:
            archivos_adicionales['balance'].to_excel(writer, sheet_name='BALANCE', index=False)
        
        if 'situacion' in archivos_adicionales:
            archivos_adicionales['situacion'].to_excel(writer, sheet_name='SITUACION', index=False)
        
        if 'focus' in archivos_adicionales:
            archivos_adicionales['focus'].to_excel(writer, sheet_name='FOCUS', index=False)
    
    print(f"Formato de deuda generado: {output_path}")
    return output_path

def procesar_formato_deuda_completo(
    archivo_provision, 
    archivo_anticipos, 
    archivo_balance=None, 
    archivo_situacion=None, 
    archivo_focus=None,
    fecha_cierre_str=None,
    output_path=None
):
    """Procesa el formato de deuda completo"""
    print("INICIANDO PROCESAMIENTO DE FORMATO DEUDA COMPLETO")
    print("="*80)
    
    try:
        # 1. Procesar archivo de provisión
        df_provision = procesar_archivo_provision(archivo_provision, fecha_cierre_str)
        
        # 2. Procesar archivo de anticipos
        df_anticipos = procesar_archivo_anticipos(archivo_anticipos, fecha_cierre_str)
        
        # 3. Crear modelo de deuda
        modelo_deuda = crear_modelo_deuda(df_provision, df_anticipos, fecha_cierre_str)
        
        # 4. Procesar archivos adicionales
        archivos_adicionales = procesar_archivos_adicionales(
            archivo_balance, archivo_situacion, archivo_focus
        )
        
        # 5. Generar formato de deuda final
        output_file = generar_formato_deuda_final(
            modelo_deuda, archivos_adicionales, output_path
        )
        
        # 6. Generar resumen de resultados
        resumen = {
            'archivo_generado': output_file,
            'registros_provision': len(df_provision),
            'registros_anticipos': len(df_anticipos),
            'registros_pesos': len(modelo_deuda['pesos']),
            'registros_divisas': len(modelo_deuda['divisas']),
            'registros_vencimientos': len(modelo_deuda['vencimientos']),
            'fecha_procesamiento': datetime.now().isoformat(),
            'fecha_cierre': fecha_cierre_str or obtener_fecha_cierre().strftime('%Y-%m-%d')
        }
        
        # Guardar resumen en JSON
        resumen_path = output_file.replace('.xlsx', '_resumen.json')
        with open(resumen_path, 'w', encoding='utf-8') as f:
            json.dump(resumen, f, indent=2, ensure_ascii=False)
        
        print("PROCESAMIENTO COMPLETADO EXITOSAMENTE")
        print("="*80)
        return resumen
        
    except Exception as e:
        print(f"Error en el procesamiento: {str(e)}")
        raise

if __name__ == "__main__":
    # Procesamiento desde línea de comandos
    if len(sys.argv) < 3:
        print("Uso: python procesador_formato_deuda.py <archivo_provision> <archivo_anticipos> [archivo_balance] [archivo_situacion] [archivo_focus] [fecha_cierre]")
        sys.exit(1)
    
    archivo_provision = sys.argv[1]
    archivo_anticipos = sys.argv[2]
    archivo_balance = sys.argv[3] if len(sys.argv) > 3 else None
    archivo_situacion = sys.argv[4] if len(sys.argv) > 4 else None
    archivo_focus = sys.argv[5] if len(sys.argv) > 5 else None
    fecha_cierre = sys.argv[6] if len(sys.argv) > 6 else None
    
    try:
        resumen = procesar_formato_deuda_completo(
            archivo_provision, archivo_anticipos, archivo_balance, 
            archivo_situacion, archivo_focus, fecha_cierre
        )
        print("Procesamiento completado exitosamente")
        print(f"Archivo generado: {resumen['archivo_generado']}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1) 