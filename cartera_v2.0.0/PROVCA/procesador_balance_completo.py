#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Balance 
- Limpia y normaliza el balance por División/Cuenta
- (Reglas genéricas y tolerantes; ajusta encabezados flexibles)
- Guarda salidas en PROVCA_PROCESADOS
"""

import os
import re
import pandas as pd
from datetime import datetime

OUTPUT_DIR = r"C:\wamp64\www\modelo-deuda-python\cartera_v2.0.0\PROVCA_PROCESADOS"

def asegurar_directorio(path_dir: str):
    os.makedirs(path_dir, exist_ok=True)

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def convertir_valor(valor):
    try:
        if valor is None or (isinstance(valor, float) and pd.isna(valor)):
            return 0.0
        if isinstance(valor, (int, float)):
            return float(valor)
        s = str(valor).strip().replace('\u200b','').replace(' ','')
        if s == '' or s.lower() == 'nan':
            return 0.0
        if '.' in s and ',' in s:
            s = s.replace('.', '').replace(',', '.')
        elif ',' in s and '.' not in s:
            s = s.replace(',', '.')
        return float(s)
    except Exception:
        return 0.0

def leer_balance(ruta_excel: str) -> pd.DataFrame:
    xls = pd.ExcelFile(ruta_excel)
    frames = []
    for hoja in xls.sheet_names:
        try:
            df = pd.read_excel(ruta_excel, sheet_name=hoja, dtype=str)
            if df.empty:
                continue
            df.columns = [str(c).strip().upper() for c in df.columns]
            df["__HOJA__"] = hoja
            frames.append(df)
        except Exception:
            continue
    if not frames:
        raise ValueError("No se pudieron leer hojas válidas del Balance.")
    return pd.concat(frames, ignore_index=True)

def normalizar_balance(df: pd.DataFrame) -> pd.DataFrame:
    # Intentar detectar columnas típicas
    posibles_div = [c for c in df.columns if "DIV" in c or "DIVISION" in c]
    posibles_cuenta = [c for c in df.columns if "CUENTA" in c or "COD" in c]
    posibles_saldo = [c for c in df.columns if ("SALDO" in c and "MES" not in c) or "VALOR" in c or "DEBITO" in c or "CRÉDITO" in c or "CREDITO" in c]

    col_div = posibles_div[0] if posibles_div else df.columns[0]
    col_cuenta = posibles_cuenta[0] if posibles_cuenta else df.columns[1]
    col_saldo = posibles_saldo[0] if posibles_saldo else df.columns[-1]

    out = df[[col_div, col_cuenta, col_saldo]].copy()
    out.columns = ["DIVISION", "CUENTA", "SALDO"]
    out["SALDO"] = out["SALDO"].apply(convertir_valor)
    out = out.groupby(["DIVISION", "CUENTA"], as_index=False)["SALDO"].sum()
    return out

def guardar_balance(df: pd.DataFrame, origen: str) -> str:
    asegurar_directorio(OUTPUT_DIR)
    ruta = os.path.join(OUTPUT_DIR, f"balance_normalizado_{timestamp()}.xlsx")
    with pd.ExcelWriter(ruta, engine="xlsxwriter") as w:
        df.to_excel(w, sheet_name="balance", index=False)
        meta = pd.DataFrame({"ArchivoOrigen":[os.path.basename(origen)], "Filas":[len(df)]})
        meta.to_excel(w, sheet_name="meta", index=False)
    return ruta

def main():
    import argparse
    p = argparse.ArgumentParser(description="Procesador Balance Completo")
    p.add_argument("archivo", help="Ruta al Balance (xlsx)")
    args = p.parse_args()

    df_raw = leer_balance(args.archivo)
    df_out = normalizar_balance(df_raw)
    ruta = guardar_balance(df_out, args.archivo)
    print(f"✅ Balance normalizado guardado en: {ruta}")

if __name__ == "__main__":
    main()
