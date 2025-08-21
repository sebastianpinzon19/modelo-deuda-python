# -*- coding: utf-8 -*-
"""
Modelo de Deuda - Versión limpia y final
Cumple con FORMATO DEUDA.docx:
1. Hoja PESOS con anticipos.
2. Hoja DIVISAS con TRM aplicado y columnas en COP.
3. Hoja VENCIMIENTO consolidada en COP.
4. Totales por moneda y TOTAL GENERAL.
5. Solo columnas requeridas en cada hoja.
6. Formato colombiano para montos (miles y decimales).
"""

import pandas as pd
import os
from datetime import datetime

# --------------------------
# Configuración
# --------------------------
OUT_DIR = r"C:\wamp64\www\modelo-deuda-python\cartera_v2.0.0\PROVCA_PROCESADOS"
os.makedirs(OUT_DIR, exist_ok=True)

LINEAS_PESOS = [
    ("CT", 80), ("ED", 41), ("ED", 44), ("ED", 47),
    ("PL", 10), ("PL", 15), ("PL", 20), ("PL", 21),
    ("PL", 23), ("PL", 25), ("PL", 28), ("PL", 29),
    ("PL", 31), ("PL", 32), ("PL", 53), ("PL", 56),
    ("PL", 60), ("PL", 62), ("PL", 63), ("PL", 64),
    ("PL", 65), ("PL", 66), ("PL", 69)
]
LINEAS_DIVISAS = [("PL", 11), ("PL", 18), ("PL", 57), ("PL", 41)]
LINEA_A_MONEDA = {"PL11": "USD", "PL18": "USD", "PL57": "USD", "PL41": "EUR"}

# Columnas necesarias según FORMATO
NUM_COLS = ["SALDO", "SALDO NO VENCIDO", "VENCIDO 30", "VENCIDO 60", "VENCIDO 90",
            "VENCIDO 180", "VENCIDO 360", "VENCIDO + 360", "DEUDA INCOBRABLE"]
BASE_COLS = ["EMPRESA", "LINEA", "DENOMINACION COMERCIAL", "MONEDA"]

# --------------------------
# Funciones auxiliares
# --------------------------
def convertir_valor(valor):
    """Convierte texto a float (formato colombiano)."""
    try:
        if pd.isna(valor):
            return 0.0
        if isinstance(valor, (int, float)):
            return float(valor)
        s = str(valor).strip().replace(" ", "")
        if s in ["", "-", "nan", "None"]:
            return 0.0
        if "." in s and "," in s:
            s = s.replace(".", "").replace(",", ".")
        elif "," in s and "." not in s:
            s = s.replace(",", ".")
        return float(s)
    except Exception:
        return 0.0


def normalizar_linea(act, empresa):
    """Construye clave de línea tipo PL10, CT80, ED41..."""
    act = str(act).strip()
    empresa = str(empresa).strip().upper() if empresa else ""
    if act.upper().startswith(("PL", "CT", "ED")):
        return act.upper()
    if act.isdigit():
        pref = empresa if empresa in ["PL", "CT", "ED"] else "PL"
        return f"{pref}{int(act)}"
    return f"{empresa}{act}".upper() if empresa in ["PL", "CT", "ED"] else act.upper()


def totales_por_moneda(df, num_cols):
    """Agrega filas de totales por moneda y un TOTAL GENERAL."""
    if df.empty or "MONEDA" not in df.columns:
        return df
    bloques = []

    # Totales por cada moneda
    for moneda, datos in df.groupby(df["MONEDA"].str.upper()):
        fila = {c: "" for c in df.columns}
        for c in num_cols:
            fila[c] = float(datos[c].sum())
        fila["MONEDA"] = moneda
        fila[df.columns[0]] = f"TOTAL {moneda}"
        bloques.append(fila)

    # Total general
    fila = {c: "" for c in df.columns}
    for c in num_cols:
        fila[c] = float(df[c].sum())
    fila[df.columns[0]] = "TOTAL GENERAL"
    bloques.append(fila)

    return pd.concat([df, pd.DataFrame(bloques)], ignore_index=True)

# --------------------------
# Procesamiento principal
# --------------------------
def procesar_modelo(cartera_file, anticipos_file, trm_usd, trm_eur):
    print(f"🚀 Procesando cartera con TRM USD={trm_usd}, EUR={trm_eur}")

    df_cartera = pd.read_excel(cartera_file, dtype=str)
    df_anticipos = pd.read_excel(anticipos_file, dtype=str)

    # Normalizar numéricos
    for c in NUM_COLS:
        if c in df_cartera.columns:
            df_cartera[c] = df_cartera[c].apply(convertir_valor)
        else:
            df_cartera[c] = 0.0

    # Línea clave
    df_cartera["LINEA"] = df_cartera.apply(lambda r: normalizar_linea(r.get("ACTIVIDAD", ""), r.get("EMPRESA", "")), axis=1)

    # ---------------- PESOS ----------------
    allowed_pesos = set(f"{c}{n}" for c, n in LINEAS_PESOS)
    df_pesos = df_cartera[(df_cartera["LINEA"].isin(allowed_pesos)) &
                          (df_cartera["MONEDA"].str.upper().isin(["COP", "PESO", "PESOS", "PESOS COL"]))].copy()

    # Anticipos
    anticipos_pesos = df_anticipos.copy()
    anticipos_pesos["EMPRESA"] = anticipos_pesos.get("EMPRESA", "ANTICIPO")
    anticipos_pesos["LINEA"] = "ANT"
    anticipos_pesos["DENOMINACION COMERCIAL"] = anticipos_pesos.get("CLIENTE", "")
    anticipos_pesos["MONEDA"] = "PESOS COL"
    anticipos_pesos["SALDO"] = anticipos_pesos["VALOR ANTICIPO"].apply(convertir_valor)
    anticipos_pesos["SALDO NO VENCIDO"] = anticipos_pesos["SALDO"]
    for c in NUM_COLS:
        if c not in anticipos_pesos:
            anticipos_pesos[c] = 0.0

    df_pesos = pd.concat([df_pesos, anticipos_pesos[df_pesos.columns.intersection(anticipos_pesos.columns)]], ignore_index=True)

    df_pesos = totales_por_moneda(df_pesos[BASE_COLS + NUM_COLS], NUM_COLS)

    # ---------------- DIVISAS ----------------
    allowed_div = set(f"{c}{n}" for c, n in LINEAS_DIVISAS)
    df_div = df_cartera[df_cartera["LINEA"].isin(allowed_div) |
                        df_cartera["MONEDA"].str.upper().isin(["USD", "DOLAR", "DÓLAR", "EUR", "EURO"])].copy()

    df_div["MONEDA"] = df_div["LINEA"].map(LINEA_A_MONEDA).fillna(df_div["MONEDA"])
    mapa_trm = {"USD": trm_usd, "DOLAR": trm_usd, "DÓLAR": trm_usd, "EUR": trm_eur, "EURO": trm_eur}

    for base in ["SALDO", "SALDO NO VENCIDO"]:
        if base in df_div.columns:
            df_div[f"{base}_COP"] = df_div.apply(
                lambda r: convertir_valor(r[base]) * mapa_trm.get(str(r["MONEDA"]).upper(), 1),
                axis=1
            )

    df_div = totales_por_moneda(df_div[BASE_COLS + NUM_COLS + [c for c in df_div.columns if c.endswith("_COP")]], NUM_COLS)

    # ---------------- VENCIMIENTO ----------------
    df_venc = df_cartera.copy()
    for moneda, trm in [("USD", trm_usd), ("EUR", trm_eur)]:
        mask = df_venc["MONEDA"].str.upper().isin([moneda, "DOLAR", "DÓLAR", "EURO"])
        for c in NUM_COLS:
            df_venc.loc[mask, c] = df_venc.loc[mask, c].apply(convertir_valor) * trm

    venc = df_venc.groupby(["DENOMINACION COMERCIAL", "MONEDA"])[NUM_COLS].sum().reset_index()
    venc = totales_por_moneda(venc, NUM_COLS)

    # ---------------- Exportar ----------------
    ruta_salida = os.path.join(OUT_DIR, f"Modelo_Deuda_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    with pd.ExcelWriter(ruta_salida, engine="xlsxwriter") as writer:
        df_pesos.to_excel(writer, sheet_name="PESOS", index=False)
        df_div.to_excel(writer, sheet_name="DIVISAS", index=False)
        venc.to_excel(writer, sheet_name="VENCIMIENTO", index=False)

        # Formato colombiano por miles
        book = writer.book
        fmt = book.add_format({"num_format": '#,##0;-#,##0;"-"'})
        for sheet_name, df_out in [("PESOS", df_pesos), ("DIVISAS", df_div), ("VENCIMIENTO", venc)]:
            ws = writer.sheets[sheet_name]
            for idx, col in enumerate(df_out.columns):
                if df_out[col].dtype in ["float64", "int64"]:
                    ws.set_column(idx, idx, 18, fmt)
                else:
                    ws.set_column(idx, idx, 20)

    print(f"✅ Archivo generado en: {ruta_salida}")
    return ruta_salida

# --------------------------
# Main
# --------------------------
if __name__ == "__main__":
    cartera_file = input("Ruta archivo cartera: ").strip('"')
    anticipos_file = input("Ruta archivo anticipos: ").strip('"')
    trm_usd = float(input("TRM Dólar: ").replace(",", "."))
    trm_eur = float(input("TRM Euro: ").replace(",", "."))
    procesar_modelo(cartera_file, anticipos_file, trm_usd, trm_eur)
