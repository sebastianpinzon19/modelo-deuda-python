# -*- coding: utf-8 -*-
import os
import re
import pandas as pd
from datetime import datetime

OUTPUT_DIR = r"C:\wamp64\www\modelo-deuda-python\cartera_v2.0.0\PROVCA_PROCESADOS"

def asegurar_directorio(path_dir):
    os.makedirs(path_dir, exist_ok=True)

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def convertir_valor(valor_str):
    try:
        if valor_str is None:
            return 0.0
        if isinstance(valor_str, (int, float)):
            return float(valor_str)
        s = str(valor_str).strip().replace('\u200b', '').replace(' ', '')
        if s == '' or s.lower() == 'nan':
            return 0.0
        if s.count('.') > 1 and s.count(',') > 1:
            numeros = re.findall(r'\d+', s)
            if len(numeros) >= 2:
                s = f"{numeros[0]}.{numeros[1][:2]}"
            else:
                s = numeros[0]
        elif s.count('.') > 1:
            partes = s.split('.')
            s = ''.join(partes[:-1]) + '.' + partes[-1]
        elif s.count(',') > 1:
            partes = s.split(',')
            s = ''.join(partes[:-1]) + '.' + partes[-1]
        if '.' in s and ',' in s:
            s = s.replace('.', '').replace(',', '.')
        elif ',' in s:
            s = s.replace(',', '.')
        return float(s)
    except:
        return 0.0

def formatear_numero_colombiano(valor):
    if valor is None or pd.isna(valor):
        return "-"
    if isinstance(valor, str):
        valor = convertir_valor(valor)
    if valor == 0:
        return "-"
    if valor == int(valor):
        s = f"{int(valor)}"
    else:
        s = f"{valor:.2f}"
    if valor >= 1000:
        s = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        s = s.replace(".", ",")
    return s

def obtener_saldo_total_01010(ruta_excel):
    xls = pd.ExcelFile(ruta_excel)
    for hoja in xls.sheet_names:
        df = pd.read_excel(ruta_excel, sheet_name=hoja, dtype=str)
        df.columns = [str(c).strip().upper() for c in df.columns]
        col_saldo = next((c for c in df.columns if "SALDO" in c and "MES" in c), None)
        if not col_saldo:
            continue
        df_norm = df.astype(str).apply(lambda col: col.str.strip().str.upper())
        mask = df_norm.apply(lambda fila: "TOTAL" in " ".join(fila.values) and "01010" in " ".join(fila.values), axis=1)
        if mask.any():
            return convertir_valor(df.loc[mask, col_saldo].iloc[0])
    raise ValueError("No se encontró columna SALDOS MES y fila TOTAL 01010.")

def guardar_resultado(valor, archivo):
    asegurar_directorio(OUTPUT_DIR)
    ruta_out = os.path.join(OUTPUT_DIR, f"situacion_total01010_{timestamp()}.xlsx")
    pd.DataFrame({
        "ArchivoOrigen": [os.path.basename(archivo)],
        "Concepto": ["TOTAL_01010_SALDO_MES"],
        "Valor_Num": [valor],
        "Valor_Formateado": [formatear_numero_colombiano(valor)]
    }).to_excel(ruta_out, index=False)
    return ruta_out

if __name__ == "__main__":
    print("=== Procesador Específico de Situación ===")
    archivo = input("Ruta del archivo Excel de Situación: ").strip('"')
    try:
        valor = obtener_saldo_total_01010(archivo)
        print(f"✅ Valor encontrado: {formatear_numero_colombiano(valor)}")
        ruta = guardar_resultado(valor, archivo)
        print(f"📁 Archivo generado en: {ruta}")
    except Exception as e:
        print(f"❌ Error: {e}")
