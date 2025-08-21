# -*- coding: utf-8 -*-
"""
Procesador de Cartera PROVCA - Versión Final
- Fecha de cierre exacta ingresada por el usuario
- Llena DENOMINACION COMERCIAL con NOMBRE si está vacía
- Calcula día, mes y año de las fechas
- Formatea montos con separador de miles en Excel
- Orden de columnas según plantilla final
- Validaciones internas realizadas pero no mostradas
"""

import pandas as pd
from datetime import datetime
import os
import sys

# -------------------
# Configuración
# -------------------
RENOMBRES = {
    "PCCDEM": "EMPRESA",
    "PCCDAC": "ACTIVIDAD",
    "PCDEAC": "EMPRESA_2",
    "PCCDAG": "CODIGO AGENTE",
    "PCNMAG": "AGENTE",
    "PCCDCO": "CODIGO COBRADOR",
    "PCNMCO": "COBRADOR",
    "PCCDCL": "CODIGO CLIENTE",
    "PCCDDN": "IDENTIFICACION",
    "PCNMCL": "NOMBRE",
    "PCNMCM": "DENOMINACION COMERCIAL",
    "PCNMDO": "DIRECCION",
    "PCTLF1": "TELEFONO",
    "PCNMPO": "CIUDAD",
    "PCNUFC": "NUMERO FACTURA",
    "PCORPD": "TIPO",
    "PCFEFA": "FECHA",
    "PCFEVE": "FECHA VTO",
    "PCVAFA": "VALOR",
    "PCSALD": "SALDO"
}

VENCIMIENTOS_RANGOS = [
    ("SALDO NO VENCIDO", 0, 29),
    ("VENCIDO 30", 30, 59),
    ("VENCIDO 60", 60, 89),
    ("VENCIDO 90", 90, 179),
    ("VENCIDO 180", 180, 359),
    ("VENCIDO 360", 360, 369),
    ("VENCIDO + 360", 370, 999999),
]

OUT_DIR = r"C:\wamp64\www\modelo-deuda-python\cartera_v2.0.0\PROVCA_PROCESADOS"
os.makedirs(OUT_DIR, exist_ok=True)

# -------------------
# Helpers
# -------------------
def obtener_fecha_cierre(fecha_cierre_str=None):
    if fecha_cierre_str:
        dt = pd.to_datetime(fecha_cierre_str, errors="coerce", dayfirst=True)
        if pd.isna(dt):
            raise ValueError("Fecha de cierre inválida. Use YYYY-MM-DD")
        return pd.to_datetime(dt).normalize()
    return pd.to_datetime(datetime.today()).normalize()

def convertir_valor_to_float(x):
    if pd.isna(x):
        return 0.0
    s = str(x).strip().replace("$", "").replace(" ", "").replace("\u200b", "")
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except Exception:
        digits = "".join(ch for ch in s if ch.isdigit() or ch == ".")
        return float(digits) if digits else 0.0

def formato_fecha_str(dt):
    if pd.isna(dt):
        return ""
    return pd.to_datetime(dt).strftime("%d/%m/%Y")

def parse_fecha_segura(serie):
    def try_parse(val):
        if pd.isna(val) or str(val).strip() == "":
            return pd.NaT
        return pd.to_datetime(val, errors="coerce", dayfirst=True)
    return serie.apply(try_parse)

def guardar_excel_con_miles(df, output_path, columnas_montos):
    try:
        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Cartera")
            ws = writer.sheets["Cartera"]
            book = writer.book
            fmt = book.add_format({"num_format": "#,##0"})
            for col in columnas_montos:
                if col in df.columns:
                    idx = df.columns.get_loc(col)
                    ws.set_column(idx, idx, None, fmt)
    except Exception:
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Cartera")

# -------------------
# Procesador principal
# -------------------
def procesar_cartera(input_path, output_path=None, fecha_cierre_str=None):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No se encontró el archivo CSV: {input_path}")

    df = pd.read_csv(input_path, sep=";", encoding="latin1", dtype=str)
    df.rename(columns=RENOMBRES, inplace=True)

    # MONEDA por defecto
    if "MONEDA" not in df.columns:
        df["MONEDA"] = "PESOS COL"

    # Llenar denominación comercial si está vacía
    if "DENOMINACION COMERCIAL" in df.columns and "NOMBRE" in df.columns:
        df["DENOMINACION COMERCIAL"] = df["DENOMINACION COMERCIAL"].replace("", pd.NA)
        df["DENOMINACION COMERCIAL"] = df["DENOMINACION COMERCIAL"].fillna(df["NOMBRE"])

    # Convertir montos
    for col in ["SALDO", "VALOR"]:
        if col in df.columns:
            df[col] = df[col].apply(convertir_valor_to_float)

    # Fechas
    for col in ["FECHA", "FECHA VTO"]:
        if col in df.columns:
            df[col] = parse_fecha_segura(df[col])

    # Fecha de cierre
    fecha_cierre = obtener_fecha_cierre(fecha_cierre_str)

    # Días vencidos y por vencer
    if "FECHA VTO" in df.columns:
        df["DIAS VENCIDO"] = df["FECHA VTO"].apply(
            lambda fv: max((fecha_cierre - fv).days, 0) if pd.notna(fv) else 0
        )
        df["DIAS POR VENCER"] = df["FECHA VTO"].apply(
            lambda fv: max((fv - fecha_cierre).days, 0) if pd.notna(fv) else 0
        )
    else:
        df["DIAS VENCIDO"] = 0
        df["DIAS POR VENCER"] = 0

    # Mora y vencimientos
    df["SALDO VENCIDO"] = df.apply(lambda r: r["SALDO"] if r["DIAS VENCIDO"] > 0 else 0, axis=1)
    df["% Dotación"] = df["DIAS VENCIDO"].apply(lambda x: "100%" if x >= 180 else "0%")
    df["Valor Dotación"] = df.apply(lambda r: r["SALDO"] if r["DIAS VENCIDO"] >= 180 else 0, axis=1)
    df[">=180 días"] = df.apply(lambda r: r["SALDO"] if r["DIAS VENCIDO"] >= 180 else 0, axis=1)

    # Meses históricos desde fecha de cierre
    mes_cierre_inicio = datetime(fecha_cierre.year, fecha_cierre.month, 1)
    meses_hist = []
    for i in range(6):
        a = mes_cierre_inicio - pd.DateOffset(months=i)
        b = mes_cierre_inicio - pd.DateOffset(months=i - 1)
        col = a.strftime("%b-%y").lower()
        meses_hist.append(col)
        df[col] = df.apply(
            lambda r, a=a, b=b: r["SALDO"] if pd.notna(r["FECHA VTO"]) and a <= r["FECHA VTO"] < b else 0,
            axis=1
        )

    # Por vencer
    por_vencer_cols = []
    for i in range(1, 4):
        a = mes_cierre_inicio + pd.DateOffset(months=i)
        b = mes_cierre_inicio + pd.DateOffset(months=i + 1)
        col = f"Por_Vencer_{i}_meses"
        por_vencer_cols.append(col)
        df[col] = df.apply(
            lambda r, a=a, b=b: r["SALDO"] if pd.notna(r["FECHA VTO"]) and a <= r["FECHA VTO"] < b else 0,
            axis=1
        )

    fecha_90 = fecha_cierre + pd.DateOffset(days=90)
    df["Por_Vencer_+90_dias"] = df.apply(
        lambda r: r["SALDO"] if pd.notna(r["FECHA VTO"]) and r["FECHA VTO"] >= fecha_90 else 0, axis=1
    )

    # Rango vencimientos
    for name, mind, maxd in VENCIMIENTOS_RANGOS:
        df[name] = df.apply(
            lambda r, mind=mind, maxd=maxd: r["SALDO"] if mind <= r["DIAS VENCIDO"] <= maxd else 0,
            axis=1
        )

    # Deuda incobrable
    df["DEUDA INCOBRABLE"] = df["Valor Dotación"]

    # Desglose fecha
    if "FECHA" in df.columns:
        df["DIA FECHA"] = df["FECHA"].dt.day.fillna(0).astype(int)
        df["MES FECHA"] = df["FECHA"].dt.month.fillna(0).astype(int)
        df["AÑO FECHA"] = df["FECHA"].dt.year.fillna(0).astype(int)
        df["FECHA"] = df["FECHA"].apply(formato_fecha_str)
    if "FECHA VTO" in df.columns:
        df["DIA FECHA VTO"] = df["FECHA VTO"].dt.day.fillna(0).astype(int)
        df["MES FECHA VTO"] = df["FECHA VTO"].dt.month.fillna(0).astype(int)
        df["AÑO FECHA VTO"] = df["FECHA VTO"].dt.year.fillna(0).astype(int)
        df["FECHA VTO"] = df["FECHA VTO"].apply(formato_fecha_str)

    # Orden de columnas
    final_cols = [
        "EMPRESA", "ACTIVIDAD", "EMPRESA_2", "CODIGO AGENTE", "AGENTE",
        "CODIGO COBRADOR", "COBRADOR", "CODIGO CLIENTE", "IDENTIFICACION",
        "NOMBRE", "DENOMINACION COMERCIAL", "DIRECCION", "TELEFONO", "CIUDAD",
        "NUMERO FACTURA", "TIPO", "MONEDA", "FECHA", "DIA FECHA", "MES FECHA", "AÑO FECHA",
        "FECHA VTO", "DIA FECHA VTO", "MES FECHA VTO", "AÑO FECHA VTO",
        "VALOR", "SALDO", "SALDO VENCIDO", "% Dotación", "Valor Dotación", ">=180 días"
    ] + meses_hist + por_vencer_cols + ["Mora Total", "Por_Vencer_+90_dias"] + \
      [v[0] for v in VENCIMIENTOS_RANGOS] + ["Valor Total Por Vencer", "DEUDA INCOBRABLE"]

    df["Mora Total"] = df["SALDO VENCIDO"]
    df["Valor Total Por Vencer"] = df.apply(lambda r: r["SALDO"] if r["DIAS VENCIDO"] == 0 else 0, axis=1)

    df = df[[c for c in final_cols if c in df.columns]]

    # Guardar
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not output_path:
        output_path = os.path.join(OUT_DIR, f"PROVCA_PROCESADO_{timestamp}.xlsx")

    columnas_montos = ["VALOR", "SALDO", "SALDO VENCIDO", "Valor Dotación", ">=180 días"] + \
                       meses_hist + por_vencer_cols + ["Mora Total", "Por_Vencer_+90_dias"] + \
                       [v[0] for v in VENCIMIENTOS_RANGOS] + ["Valor Total Por Vencer", "DEUDA INCOBRABLE"]

    guardar_excel_con_miles(df, output_path, columnas_montos)
    print(f"✅ Archivo generado: {output_path}")
    return output_path

# -------------------
# CLI
# -------------------
def menu():
    print("=== Menú de Procesamiento de Cartera PROVCA ===")
    input_path = input("Ruta del archivo CSV: ").strip()
    output_path = input("Ruta de salida (opcional): ").strip() or None
    fecha_cierre_str = input("Fecha de cierre EXACTA (YYYY-MM-DD, vacío = hoy): ").strip() or None
    try:
        ruta_salida = procesar_cartera(input_path, output_path, fecha_cierre_str)
        print(f"Archivo generado en: {ruta_salida}")
    except Exception as e:
        print("❌ ERROR:", e)

if __name__ == "__main__":
    menu()
