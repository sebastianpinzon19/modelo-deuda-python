#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de Deuda - Versión Corregida Final (completo)

Cambios aplicados según lo solicitado por el cliente:
- En VENCIMIENTO el cliente aparece por NOMBRE (DENOMINACION_COMERCIAL) y no por código.
- En cada línea de venta (LINEA_VENTA / CANAL) un cliente aparece sólo 1 vez (se agrupan y suman los saldos y vencimientos).
- En DIVISAS se conserva una columna con el saldo en moneda original (SALDO_ORIGINAL) y el tipo de moneda (MONEDA_ORIGINAL).
  El SALDO_ORIGINAL queda en la columna E del Excel (ordenando las columnas para lograrlo).
- CANAL en VENCIMIENTO es la LINEA_VENTA (ej. PL20, PL15) y está ubicada en la columna C (por orden de columnas en el DataFrame).
- Se mantienen y suman los vencimientos (Vencido 30, 60, 90, etc.).

Salida: archivo XLSX con hojas PESOS, DIVISAS y VENCIMIENTO.
"""

import pandas as pd
import os
from datetime import datetime
from pathlib import Path


def procesar_modelo_deuda(cartera_path, anticipos_path, trm_dolar, trm_euro, output_path):
    """Proceso completo: lectura, normalización, creación de hojas y exportación a Excel."""
    print("🔄 Iniciando procesamiento del modelo de deuda...")

    df_cartera = leer_archivo(cartera_path, "Cartera")
    df_anticipos = leer_archivo(anticipos_path, "Anticipos")

    df_cartera = normalizar_columnas_cartera(df_cartera)
    df_anticipos = normalizar_columnas_anticipos(df_anticipos)

    df_cartera = crear_linea_venta(df_cartera)

    # Definir líneas y monedas
    lineas_pesos = [
        'CT80','ED41','ED44','ED47','PL10','PL15','PL20','PL21','PL23','PL25',
        'PL28','PL29','PL31','PL32','PL53','PL56','PL60','PL62','PL63','PL64',
        'PL65','PL66','PL69'
    ]
    lineas_divisas = ['PL11','PL18','PL57','PL41']
    monedas_divisas = ['USD', 'DOLAR', 'EURO', 'EUR'] # Aceptar varios nombres

    # Separar cartera por tipo (la lógica de línea de venta es la principal para cartera)
    df_cartera_pesos = df_cartera[df_cartera['LINEA_VENTA'].isin(lineas_pesos)].copy()
    df_cartera_divisas = df_cartera[df_cartera['LINEA_VENTA'].isin(lineas_divisas)].copy()

    # --- CORRECCIÓN ---
    # Separar anticipos por MONEDA, que es más robusto que LINEA_VENTA
    df_anticipos['MONEDA_NORM'] = df_anticipos['MONEDA'].str.upper().str.strip()
    df_anticipos_pesos = df_anticipos[~df_anticipos['MONEDA_NORM'].isin(monedas_divisas)].copy()
    df_anticipos_divisas = df_anticipos[df_anticipos['MONEDA_NORM'].isin(monedas_divisas)].copy()

    # Crear hojas
    df_pesos = crear_hoja_pesos(df_cartera_pesos, df_anticipos_pesos)
    df_divisas = crear_hoja_divisas(df_cartera_divisas, df_anticipos_divisas, trm_dolar, trm_euro)
    df_vencimiento = crear_hoja_vencimiento(df_cartera_pesos, df_cartera_divisas, df_anticipos, trm_dolar, trm_euro)

    crear_excel_final(df_pesos, df_divisas, df_vencimiento, output_path)

    print(f"✅ Archivo generado: {output_path}")
    return os.path.abspath(output_path)


def leer_archivo(file_path, tipo_archivo):
    """Lee CSV o Excel intentando varias codificaciones/separadores para CSV."""
    file_path = str(file_path)
    if file_path.lower().endswith('.csv'):
        for sep in [';', ',', '	']:
            for enc in ['latin1', 'utf-8', 'cp1252']:
                try:
                    df = pd.read_csv(file_path, sep=sep, encoding=enc, dtype=str)
                    if len(df.columns) > 1:
                        print(f"✅ {tipo_archivo} CSV leído: sep='{sep}', enc='{enc}'")
                        return df
                except Exception:
                    continue
        raise ValueError(f"No se pudo leer el archivo CSV {file_path}")
    else:
        df = pd.read_excel(file_path, engine='openpyxl', dtype=str)
        print(f"✅ {tipo_archivo} Excel leído correctamente")
        return df


def _find_and_rename_column(df, new_name, candidates):
    """
    Busca en las columnas de un DataFrame una lista de nombres candidatos (case-insensitive).
    Renombra la primera coincidencia encontrada al nuevo nombre (new_name).
    Devuelve True si se encontró y renombró, False en caso contrario.
    """
    df_cols_upper = {col.upper().strip(): col for col in df.columns}
    for cand in candidates:
        cand_upper = cand.upper().strip()
        if cand_upper in df_cols_upper:
            original_col_name = df_cols_upper[cand_upper]
            df.rename(columns={original_col_name: new_name}, inplace=True)
            print(f"    ✓ Columna encontrada: '{original_col_name}' -> '{new_name}'")
            return True
    return False


def normalizar_columnas_cartera(df):
    """Normaliza nombres de columnas y asegura columnas de vencimiento y nombre del cliente."""
    print("🔧 Normalizando columnas de cartera...")

    # Listas de candidatos para las columnas clave (en orden de prioridad)
    CANDIDATOS_SALDO = ['SALDO TOTAL', 'SALDO', 'PCSALD', 'BALANCE', 'VALOR']
    CANDIDATOS_CLIENTE_COD = ['CODIGO_CLIENTE', 'CODIGO CLIENTE', 'PCCDCL']
    CANDIDATOS_CLIENTE_NOMBRE = ['DENOMINACION_COMERCIAL', 'DENOMINACION COMERCIAL', 'PCNMCM', 'CLIENTE', 'NOMBRE']
    CANDIDATOS_EMPRESA = ['EMPRESA', 'PCCDEM']
    CANDIDATOS_ACTIVIDAD = ['ACTIVIDAD', 'PCCDAC']
    CANDIDATOS_MONEDA = ['MONEDA']

    # Búsqueda y renombrado flexible
    _find_and_rename_column(df, 'SALDO_TOTAL', CANDIDATOS_SALDO)
    _find_and_rename_column(df, 'CODIGO_CLIENTE', CANDIDATOS_CLIENTE_COD)
    _find_and_rename_column(df, 'DENOMINACION_COMERCIAL', CANDIDATOS_CLIENTE_NOMBRE)
    _find_and_rename_column(df, 'EMPRESA', CANDIDATOS_EMPRESA)
    _find_and_rename_column(df, 'ACTIVIDAD', CANDIDATOS_ACTIVIDAD)
    _find_and_rename_column(df, 'MONEDA', CANDIDATOS_MONEDA)

    # columnas base
    if 'EMPRESA' not in df.columns: df['EMPRESA'] = 'PL'
    if 'ACTIVIDAD' not in df.columns: df['ACTIVIDAD'] = '99'
    if 'CODIGO_CLIENTE' not in df.columns: df['CODIGO_CLIENTE'] = 'SIN_CODIGO'
    if 'DENOMINACION_COMERCIAL' not in df.columns:
        df['DENOMINACION_COMERCIAL'] = df['CODIGO_CLIENTE']

    if 'MONEDA' not in df.columns:
        df['MONEDA'] = 'PESOS COL'
    else:
        df['MONEDA'] = df['MONEDA'].fillna('PESOS COL')

    # convertir SALDO_TOTAL
    df['SALDO_TOTAL'] = convertir_a_numerico(df.get('SALDO_TOTAL', 0))

    # crear/normalizar columnas de vencimiento
    venc_cols = ['SALDO_NO_VENCIDO', 'VENCIDO_30', 'VENCIDO_60', 'VENCIDO_90', 'VENCIDO_180', 'VENCIDO_360', 'VENCIDO_360_PLUS', 'DEUDA_INCOBRABLE']
    venc_candidates = {
        'SALDO_NO_VENCIDO': ['SALDO NO VENCIDO', 'Saldo No vencido', 'SALDO_NO_VENCIDO'],
        'VENCIDO_30': ['VENCIDO 30', 'Vencido 30', 'VENCIDO_30'],
        'VENCIDO_60': ['VENCIDO 60', 'Vencido 60', 'VENCIDO_60'],
        'VENCIDO_90': ['VENCIDO 90', 'Vencido 90', 'VENCIDO_90'],
        'VENCIDO_180': ['VENCIDO 180', 'Vencido 180', 'VENCIDO_180'],
        'VENCIDO_360': ['VENCIDO 360', 'Vencido 360', 'VENCIDO_360'],
        'VENCIDO_360_PLUS': ['VENCIDO + 360', 'VENCIDO_360_PLUS'],
        'DEUDA_INCOBRABLE': ['DEUDA INCOBRABLE', 'DEUDA_INCOBRABLE']
    }
    for new_name, candidates in venc_candidates.items():
        _find_and_rename_column(df, new_name, candidates)

    for col in venc_cols:
        if col in df.columns:
            df[col] = convertir_a_numerico(df[col])
        else:
            df[col] = 0.0

    # si no hay SALDO_NO_VENCIDO, calcularlo
    if df['SALDO_NO_VENCIDO'].sum() == 0 and 'SALDO_TOTAL' in df.columns:
        vencidos_total = df[['VENCIDO_30', 'VENCIDO_60', 'VENCIDO_90', 'VENCIDO_180', 'VENCIDO_360', 'VENCIDO_360_PLUS']].sum(axis=1)
        df['SALDO_NO_VENCIDO'] = (df['SALDO_TOTAL'] - vencidos_total).clip(lower=0)

    # mantener solo columnas relevantes
    cols_keep = ['EMPRESA', 'ACTIVIDAD', 'LINEA_VENTA'] if 'LINEA_VENTA' in df.columns else ['EMPRESA', 'ACTIVIDAD']
    cols_keep += ['CODIGO_CLIENTE', 'DENOMINACION_COMERCIAL', 'MONEDA', 'SALDO_TOTAL'] + venc_cols
    # filtrar intersección
    cols_keep = [c for c in cols_keep if c in df.columns]

    df = df[cols_keep].copy()

    print(f"✅ Cartera normalizada: {len(df)} registros")
    return df


def normalizar_columnas_anticipos(df):
    """Normaliza anticipos y los convierte a formato compatible con cartera (saldos negativos)."""
    print("🔧 Normalizando columnas de anticipos...")

    mapping = {
        'NCCDEM': 'EMPRESA', 'NCCDAC': 'ACTIVIDAD', 'NCCDCL': 'CODIGO_CLIENTE', 'NCIMAN': 'VALOR_ANTICIPO',
        'VALOR ANTICIPO': 'VALOR_ANTICIPO', 'CODIGO CLIENTE': 'CODIGO_CLIENTE'
    }
    df = df.rename(columns=mapping)

    if 'EMPRESA' not in df.columns: df['EMPRESA'] = 'AN'
    if 'ACTIVIDAD' not in df.columns: df['ACTIVIDAD'] = '00'
    if 'CODIGO_CLIENTE' not in df.columns: df['CODIGO_CLIENTE'] = 'ANTICIPO_SIN_CODIGO'
    if 'DENOMINACION_COMERCIAL' not in df.columns: df['DENOMINACION_COMERCIAL'] = 'ANTICIPO'
    if 'MONEDA' not in df.columns:
        df['MONEDA'] = 'PESOS COL' # Asumir pesos si no se especifica
    else:
        df['MONEDA'] = df['MONEDA'].fillna('PESOS COL')

    df['VALOR_ANTICIPO'] = convertir_a_numerico(df.get('VALOR_ANTICIPO', 0))
    # convertir a saldo (negativo)
    df['SALDO_TOTAL'] = (df['VALOR_ANTICIPO'].abs() * -1)

    # El valor del anticipo es un saldo a favor, se refleja en SALDO_TOTAL y SALDO_NO_VENCIDO
    df['SALDO_NO_VENCIDO'] = df['SALDO_TOTAL']

    # El resto de vencimientos son cero para anticipos
    venc_cols = ['VENCIDO_30', 'VENCIDO_60', 'VENCIDO_90', 'VENCIDO_180', 'VENCIDO_360', 'VENCIDO_360_PLUS', 'DEUDA_INCOBRABLE']
    for col in venc_cols:
        df[col] = 0.0

    cols_keep = ['EMPRESA', 'ACTIVIDAD', 'CODIGO_CLIENTE', 'DENOMINACION_COMERCIAL', 'MONEDA', 'SALDO_TOTAL', 'SALDO_NO_VENCIDO'] + venc_cols
    df = df[[c for c in cols_keep if c in df.columns]].copy()

    print(f"✅ Anticipos normalizados: {len(df)} registros")
    return df


def crear_linea_venta(df):
    """Crea la columna LINEA_VENTA combinando EMPRESA + ACTIVIDAD (rellenando con ceros si es necesario)."""
    if 'EMPRESA' not in df.columns or 'ACTIVIDAD' not in df.columns:
        df['LINEA_VENTA'] = 'ND' # No disponible
        return df
    df['EMPRESA'] = df['EMPRESA'].astype(str).str.strip()
    df['ACTIVIDAD'] = df['ACTIVIDAD'].astype(str).str.strip().str.zfill(2)
    df['LINEA_VENTA'] = df['EMPRESA'] + df['ACTIVIDAD']
    return df


def convertir_a_numerico(serie):
    """Convierte series a float manejando formatos con separadores de miles y decimales colombianos."""
    def _convert(x):
        if pd.isna(x) or x == '' or x is None:
            return 0.0
        s = str(x).replace('$', '').replace(' ', '').replace('​', '').strip()
        if s == '' or s == '-':
            return 0.0
        # formato 1.234.567,89 -> 1234567.89
        try:
            if '.' in s and ',' in s:
                s = s.replace('.', '').replace(',', '.')
            elif ',' in s and '.' not in s:
                s = s.replace(',', '.')
            return float(s)
        except Exception:
            try:
                return float(s)
            except:
                return 0.0
    return serie.apply(_convert)


def crear_hoja_pesos(df_cartera_pesos, df_anticipos_pesos):
    """Consolida cartera y anticipos en PESOS agrupando por LINEA_VENTA y NOMBRE cliente (DENOMINACION_COMERCIAL)."""
    print("📄 Creando hoja PESOS...")
    df = pd.concat([df_cartera_pesos, df_anticipos_pesos], ignore_index=True)
    if df.empty:
        print("⚠️ No hay registros PESOS")
        return pd.DataFrame()

    # eliminar saldos muy pequeños
    df = df[df['SALDO_TOTAL'].abs() > 0.01]

    # columnas numéricas a sumar
    num_cols = [c for c in df.columns if c not in ['EMPRESA', 'ACTIVIDAD', 'LINEA_VENTA', 'CODIGO_CLIENTE', 'DENOMINACION_COMERCIAL']]

    agg_dict = {c: 'sum' for c in num_cols}
    df_agr = df.groupby(['LINEA_VENTA', 'DENOMINACION_COMERCIAL'], as_index=False).agg(agg_dict)

    # renombrar columnas para salida legible
    # Mantener orden: LINEA_VENTA, DENOMINACION_COMERCIAL, SALDO_TOTAL, SALDO_NO_VENCIDO, VENCIDO_30...
    cols_order = ['LINEA_VENTA', 'DENOMINACION_COMERCIAL'] + [c for c in ['SALDO_TOTAL', 'SALDO_NO_VENCIDO', 'VENCIDO_30', 'VENCIDO_60', 'VENCIDO_90', 'VENCIDO_180', 'VENCIDO_360', 'VENCIDO_360_PLUS', 'DEUDA_INCOBRABLE'] if c in df_agr.columns]
    df_agr = df_agr[cols_order]
    df_agr = df_agr.rename(columns={'DENOMINACION_COMERCIAL': 'CLIENTE'})

    print(f"✅ Hoja PESOS creada: {len(df_agr)} registros")
    return df_agr


def crear_hoja_divisas(df_cartera_divisas, df_anticipos_divisas, trm_dolar, trm_euro):
    """Crea la hoja DIVISAS, guarda SALDO_ORIGINAL y MONEDA_ORIGINAL y convierte a pesos para SALDO_TOTAL."""
    print("📄 Creando hoja DIVISAS...")
    df = pd.concat([df_cartera_divisas, df_anticipos_divisas], ignore_index=True)
    if df.empty:
        print("⚠️ No hay registros DIVISAS")
        return pd.DataFrame()

    # identificar moneda original
    def moneda_orig(row):
        linea = str(row.get('LINEA_VENTA', '')).strip()
        # Para cartera, la línea de venta define la moneda
        if linea == 'PL41':
            return 'EUR'
        elif linea in ['PL11', 'PL18', 'PL57']:
            return 'USD'
        # Para anticipos (o si no coincide), usar la columna MONEDA que ya traen
        moneda_col = str(row.get('MONEDA', 'USD')).upper()
        if 'EUR' in moneda_col:
            return 'EUR'
        return 'USD'

    df['MONEDA_ORIGINAL'] = df.apply(moneda_orig, axis=1)
    # conservar saldo antes de convertir
    df['SALDO_ORIGINAL'] = df['SALDO_TOTAL']

    # también conservar vencimientos originales si existen (opcional)
    venc_cols = [c for c in ['SALDO_NO_VENCIDO', 'VENCIDO_30', 'VENCIDO_60', 'VENCIDO_90', 'VENCIDO_180', 'VENCIDO_360', 'VENCIDO_360_PLUS', 'DEUDA_INCOBRABLE'] if c in df.columns]
    for col in venc_cols:
        df[col] = df[col].astype(float)

    # convertir a pesos según la moneda original detectada
    mask_eur = df['MONEDA_ORIGINAL'] == 'EUR'
    mask_usd = df['MONEDA_ORIGINAL'] == 'USD'

    # columnas a convertir
    cols_convert = ['SALDO_TOTAL'] + venc_cols
    for col in cols_convert:
        df.loc[mask_eur, col] = df.loc[mask_eur, col].astype(float) * float(trm_euro)
        df.loc[mask_usd, col] = df.loc[mask_usd, col].astype(float) * float(trm_dolar)

    # eliminar saldos cero
    df = df[df['SALDO_TOTAL'].abs() > 0.01]

    # Eliminar cualquier mención de 'ANTICIPO' en los nombres de clientes
    if 'DENOMINACION_COMERCIAL' in df.columns:
        # Convertir a string, limpiar espacios y eliminar 'ANTICIPO' en cualquier parte del nombre
        df['DENOMINACION_COMERCIAL'] = (
            df['DENOMINACION_COMERCIAL']
            .astype(str)
            .str.upper()
            .str.replace('ANTICIPO', '', regex=False)
            .str.strip()
        )

    # agrupar por linea + nombre + moneda original (para mantener SALDO_ORIGINAL consolidado)
    cols_to_sum = list(dict.fromkeys(['SALDO_ORIGINAL'] + cols_convert))
    agg_cols = {c: 'sum' for c in cols_to_sum}
    df_agr = df.groupby(['LINEA_VENTA', 'DENOMINACION_COMERCIAL', 'MONEDA_ORIGINAL'], as_index=False).agg(agg_cols)

    # Agregar filas de totales por moneda, como se solicita
    totales = []

    # Total Dólares
    df_usd = df_agr[df_agr['MONEDA_ORIGINAL'] == 'USD']
    if not df_usd.empty:
        suma_usd = {col: df_usd[col].sum() for col in cols_to_sum}
        fila_usd = {'LINEA_VENTA': 'TOTAL USD', 'DENOMINACION_COMERCIAL': ''}
        fila_usd.update(suma_usd)
        totales.append(fila_usd)

    # Total Euros
    df_eur = df_agr[df_agr['MONEDA_ORIGINAL'] == 'EUR']
    if not df_eur.empty:
        suma_eur = {col: df_eur[col].sum() for col in cols_to_sum}
        fila_eur = {'LINEA_VENTA': 'TOTAL EUR', 'DENOMINACION_COMERCIAL': ''}
        fila_eur.update(suma_eur)
        totales.append(fila_eur)

    if totales:
        df_totales = pd.DataFrame(totales)
        df_agr = pd.concat([df_agr, df_totales], ignore_index=True)

    # ordenar columnas de salida para garantizar SALDO_ORIGINAL en columna D (índice 3)
    out_cols = ['LINEA_VENTA', 'DENOMINACION_COMERCIAL', 'SALDO_ORIGINAL', 'MONEDA_ORIGINAL', 'SALDO_TOTAL'] + venc_cols

    # filtrar solo las columnas existentes
    out_cols = [c for c in out_cols if c in df_agr.columns]
    df_agr = df_agr[out_cols]

    # renombrar cliente
    df_agr = df_agr.rename(columns={'DENOMINACION_COMERCIAL': 'CLIENTE'})

    print(f"✅ Hoja DIVISAS creada: {len(df_agr)} registros")
    return df_agr


def crear_hoja_vencimiento(df_cartera_pesos, df_cartera_divisas, df_anticipos, trm_dolar, trm_euro):
    """Crea hoja VENCIMIENTO consolidando todo, usando NOMBRE del cliente y CANAL = LINEA_VENTA en columna C."""
    print("📄 Creando hoja VENCIMIENTO...")

    df = pd.concat([df_cartera_pesos, df_cartera_divisas, df_anticipos], ignore_index=True)
    if df.empty:
        print("⚠️ No hay registros para VENCIMIENTO")
        return pd.DataFrame()

    # Asegurar que todos los DFs tengan LINEA_VENTA para el mapeo
    df = crear_linea_venta(df)

    # negocio / canal mapping (puedes ajustar según necesidades)
    negocio_canal_mapping = {
        'PL15': 'E-COMMERCE', 'PL20': 'LIBRERIAS 1', 'PL25': 'LIBRERIAS 1', 'PL10': 'LIBRERIAS 2',
        'PL21': 'LIBRERIAS 2', 'PL53': 'LIBRERIAS 3', 'PL63': 'LIBRERIAS 3', 'PL66': 'OTOS DIGITAL',
        'PL60': 'OTROS', 'PL64': 'OTROS', 'PL65': 'OTROS', 'PL28': 'SALDOS', 'PL29': 'SALDOS',
        'PL31': 'SALDOS', 'PL18': 'EXPORTACION', 'PL11': 'EXPORTACION', 'PL57': 'AULA', 'PL41': 'OTR',
        'CT80': 'TINTA CLUB DEL LIBRO', 'AN00': 'ANTICIPOS'
    }

    df['NEGOCIO'] = df['LINEA_VENTA'].map(negocio_canal_mapping).fillna('OTROS')
    df['CANAL'] = df['LINEA_VENTA']  # este será la columna C en la salida (por orden)
    df['Pais'] = 'Colombia'
    df['COBRO/PAGO'] = 'CLIENTE'

    def determinar_moneda(linea):
        if linea in ['PL11', 'PL18', 'PL57']:
            return 'DOLAR'
        elif linea == 'PL41':
            return 'EURO'
        else:
            return 'PESOS COL'

    df['MONEDA'] = df['LINEA_VENTA'].apply(determinar_moneda)

    # Convertir divisas a pesos para consolidación
    cols_convert = [c for c in ['SALDO_TOTAL', 'SALDO_NO_VENCIDO', 'VENCIDO_30', 'VENCIDO_60', 'VENCIDO_90', 'VENCIDO_180', 'VENCIDO_360', 'VENCIDO_360_PLUS', 'DEUDA_INCOBRABLE'] if c in df.columns]

    df_conv = df.copy()
    mask_dolar = df_conv['MONEDA'] == 'DOLAR'
    mask_euro = df_conv['MONEDA'] == 'EURO'
    for col in cols_convert:
        df_conv.loc[mask_dolar, col] = df_conv.loc[mask_dolar, col].astype(float) * float(trm_dolar)
        df_conv.loc[mask_euro, col] = df_conv.loc[mask_euro, col].astype(float) * float(trm_euro)

    # Agrupar por dimensiones: Pais, NEGOCIO, CANAL (linea), COBRO/PAGO, MONEDA, CLIENTE (nombre)
    # Eliminar cualquier mención de 'ANTICIPO' en los nombres de clientes
    if 'DENOMINACION_COMERCIAL' in df.columns:
        # Convertir a string, limpiar espacios y eliminar 'ANTICIPO' en cualquier parte del nombre
        df['DENOMINACION_COMERCIAL'] = (
            df['DENOMINACION_COMERCIAL']
            .astype(str)
            .str.upper()
            .str.replace('ANTICIPO', '', regex=False)
            .str.strip()
        )
    group_cols = ['Pais', 'NEGOCIO', 'CANAL', 'COBRO/PAGO', 'MONEDA', 'DENOMINACION_COMERCIAL']
    agg_dict = {c: 'sum' for c in cols_convert}

    df_agr = df_conv.groupby(group_cols).agg(agg_dict).reset_index()

    # renombrar columnas para la salida
    df_agr = df_agr.rename(columns={'DENOMINACION_COMERCIAL': 'CLIENTE', 'SALDO_TOTAL': 'SALDO TOTAL', 'SALDO_NO_VENCIDO': 'Saldo No vencido',
                                    'VENCIDO_30': 'Vencido 30', 'VENCIDO_60': 'Vencido 60', 'VENCIDO_90': 'Vencido 90',
                                    'VENCIDO_180': 'Vencido 180', 'VENCIDO_360': 'Vencido 360', 'VENCIDO_360_PLUS': 'Vencido + 360',
                                    'DEUDA_INCOBRABLE': 'DEUDA INCOBRABLE'})

    # Crear totales por moneda y concatenar
    df_totales = crear_totales_por_moneda(df_agr, trm_dolar, trm_euro)
    df_final = pd.concat([df_agr, df_totales], ignore_index=True, sort=False)

    # Reordenar columnas para salida (asegurar CANAL en 3ra columna, CLIENTE visible)
    # Orden preferido: Pais, NEGOCIO, CANAL, COBRO/PAGO, MONEDA, CLIENTE, SALDO TOTAL, Saldo No vencido, Vencido 30...
    prefer_order = ['Pais', 'NEGOCIO', 'CANAL', 'COBRO/PAGO', 'MONEDA', 'CLIENTE', 'SALDO TOTAL', 'Saldo No vencido', 'Vencido 30', 'Vencido 60', 'Vencido 90', 'Vencido 180', 'Vencido 360', 'Vencido + 360', 'DEUDA INCOBRABLE']
    final_cols = [c for c in prefer_order if c in df_final.columns]
    df_final = df_final[final_cols]

    print(f"✅ Hoja VENCIMIENTO creada: {len(df_final)} registros")
    return df_final


def crear_totales_por_moneda(df_agrupado, trm_dolar, trm_euro):
    """Genera filas de totales separadas por moneda y un total general."""
    print("📊 Creando totales por moneda...")
    cols_sum = [c for c in ['SALDO TOTAL', 'Saldo No vencido', 'Vencido 30', 'Vencido 60', 'Vencido 90', 'Vencido 180', 'Vencido 360', 'Vencido + 360', 'DEUDA INCOBRABLE'] if c in df_agrupado.columns]

    totales = []

    # Moneda Local (PESOS)
    df_pesos = df_agrupado[df_agrupado['MONEDA'] == 'PESOS COL'] if 'MONEDA' in df_agrupado.columns else pd.DataFrame()
    if not df_pesos.empty:
        suma = {col: df_pesos[col].sum() for col in cols_sum}
        fila = {'Pais': '', 'NEGOCIO': '', 'CANAL': '', 'COBRO/PAGO': '', 'MONEDA': 'Moneda Local', 'CLIENTE': ''}
        fila.update(suma)
        totales.append(fila)

    # Dólar
    df_dolar = df_agrupado[df_agrupado['MONEDA'] == 'DOLAR'] if 'MONEDA' in df_agrupado.columns else pd.DataFrame()
    if not df_dolar.empty:
        suma = {col: df_dolar[col].sum() for col in cols_sum}
        # mostrar valor original en USD (sumando SALDO TOTAL y dividiendo por TRM)
        valor_original_usd = suma.get('SALDO TOTAL', 0) / float(trm_dolar) if trm_dolar else 0
        fila = {'Pais': '', 'NEGOCIO': '', 'CANAL': '', 'COBRO/PAGO': '', 'MONEDA': 'Dólar', 'CLIENTE': f"{valor_original_usd:,.2f}"}
        fila.update(suma)
        totales.append(fila)

    # Euro
    df_euro = df_agrupado[df_agrupado['MONEDA'] == 'EURO'] if 'MONEDA' in df_agrupado.columns else pd.DataFrame()
    if not df_euro.empty:
        suma = {col: df_euro[col].sum() for col in cols_sum}
        valor_original_eur = suma.get('SALDO TOTAL', 0) / float(trm_euro) if trm_euro else 0
        fila = {'Pais': '', 'NEGOCIO': '', 'CANAL': '', 'COBRO/PAGO': '', 'MONEDA': 'Euro', 'CLIENTE': f"{valor_original_eur:,.2f}"}
        fila.update(suma)
        totales.append(fila)

    # Total general
    if totales:
        suma_general = {}
        for col in cols_sum:
            suma_general[col] = sum(t.get(col, 0) for t in totales if isinstance(t.get(col, 0), (int, float)))
        fila = {'Pais': '', 'NEGOCIO': '', 'CANAL': '', 'COBRO/PAGO': '', 'MONEDA': '', 'CLIENTE': 'Totales'}
        fila.update(suma_general)
        totales.append(fila)

    return pd.DataFrame(totales)


def crear_excel_final(df_pesos, df_divisas, df_vencimiento, output_path):
    """Escribe las 3 hojas en un archivo Excel y aplica formatos básicos."""
    print("📝 Creando archivo Excel...")
    import xlsxwriter

    # Asegurar carpeta
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        # Escribir hojas (si están vacías se escribirá un dataframe vacío)
        df_pesos.to_excel(writer, sheet_name='PESOS', index=False)
        df_divisas.to_excel(writer, sheet_name='DIVISAS', index=False)
        df_vencimiento.to_excel(writer, sheet_name='VENCIMIENTO', index=False)

        workbook = writer.book

        # Formatos
        header_fmt = workbook.add_format({'bold': True, 'bg_color': '#366092', 'font_color': 'white', 'align': 'center'})
        num_fmt = workbook.add_format({'num_format': '#,##0.00', 'align': 'right'})
        total_fmt = workbook.add_format({'bold': True, 'bg_color': '#E6F3FF', 'num_format': '#,##0.00', 'align': 'right'})
        grand_total_fmt = workbook.add_format({'bold': True, 'bg_color': '#D4E6B7', 'num_format': '#,##0.00', 'align': 'right'})

        # Aplicar formato por hoja
        for sheet_name, df in [('PESOS', df_pesos), ('DIVISAS', df_divisas), ('VENCIMIENTO', df_vencimiento)]:
            worksheet = writer.sheets[sheet_name]
            if df is None or df.empty:
                continue

            # headers
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_fmt)

            # ajustar anchos y aplicar formato numérico a columnas detectadas
            numeric_cols = [c for c in df.columns if any(x in c.upper() for x in ['SALDO', 'VENCIDO', 'VENCIDO +', 'DEUDA'])]
            for idx, col in enumerate(df.columns):
                # ancho basado en contenido
                try:
                    max_len = max(df[col].astype(str).map(len).max(), len(str(col))) + 2
                except Exception:
                    max_len = len(str(col)) + 2
                worksheet.set_column(idx, idx, min(max_len, 50))

                # aplicar formato numerico
                if col in numeric_cols:
                    worksheet.set_column(idx, idx, min(max_len, 50), num_fmt)

            # resaltar totales en VENCIMIENTO
            if sheet_name == 'VENCIMIENTO':
                try:
                    for row_idx in range(1, len(df) + 1):
                        row = df.iloc[row_idx - 1]
                        moneda_val = str(row.get('MONEDA', '')).strip()
                        cliente_val = str(row.get('CLIENTE', '')).strip()

                        if moneda_val in ['Moneda Local', 'Dólar', 'Euro']:
                            # total por moneda
                            for col_idx, col_name in enumerate(df.columns):
                                if col_name in numeric_cols:
                                    worksheet.write(row_idx, col_idx, row[col_name], total_fmt)
                                else:
                                    worksheet.write(row_idx, col_idx, row[col_name], workbook.add_format({'bold': True, 'bg_color': '#E6F3FF'}))
                        elif cliente_val == 'Totales':
                            for col_idx, col_name in enumerate(df.columns):
                                if col_name in numeric_cols:
                                    worksheet.write(row_idx, col_idx, row[col_name], grand_total_fmt)
                                else:
                                    worksheet.write(row_idx, col_idx, row[col_name], workbook.add_format({'bold': True, 'bg_color': '#D4E6B7'}))
                except Exception:
                    pass

    print("✅ Excel creado con las hojas PESOS, DIVISAS y VENCIMIENTO.")


def main():
    import sys
    if len(sys.argv) < 5:
        print("Uso: python modelo_deuda.py <cartera> <anticipos> <TRM_USD> <TRM_EUR> [salida]")
        sys.exit(1)

    cartera_path = sys.argv[1]
    anticipos_path = sys.argv[2]
    try:
        trm_usd = float(str(sys.argv[3]).replace(',', '.'))
        trm_eur = float(str(sys.argv[4]).replace(',', '.'))
    except Exception:
        print("TRM inválida. Use formato 4250.50 o 4250,50")
        sys.exit(2)

    if len(sys.argv) >= 6:
        output_path = sys.argv[5]
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(os.getcwd(), f'1_Modelo_Deuda_{timestamp}.xlsx')

    procesar_modelo_deuda(cartera_path, anticipos_path, trm_usd, trm_eur, output_path)


if __name__ == '__main__':
    main()
