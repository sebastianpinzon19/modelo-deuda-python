#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Anticipos
Versión simplificada usando solo pandas
"""

import pandas as pd
import os
import sys
from datetime import datetime

# -------------------------
# Configuración
# -------------------------

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

# Carpeta de salida FIJA
OUTPUT_DIR = r"C:\wamp64\www\modelo-deuda-python\cartera_v2.0.0\PROVCA_PROCESADOS"

# -------------------------
# Funciones auxiliares
# -------------------------

def formato_colombiano(valor):
    """Aplica formato colombiano a números"""
    try:
        return "{:,.0f}".format(valor).replace(",", ".")
    except:
        return valor

def procesar_anticipos(input_path):
    """Procesa archivo de anticipos"""

    # Leer archivo CSV
    df = pd.read_csv(input_path, sep=';', encoding='latin1', dtype=str)

    # Renombrar columnas según mapeo
    df = df.rename(columns={k: v for k, v in MAPEO_ANTICIPO.items() if k in df.columns})

    # Multiplicar por -1 el valor de anticipo
    if 'VALOR ANTICIPO' in df.columns:
        df['VALOR ANTICIPO'] = (
            df['VALOR ANTICIPO']
            .astype(str)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
        df['VALOR ANTICIPO'] = pd.to_numeric(df['VALOR ANTICIPO'], errors='coerce').fillna(0)
        df['VALOR ANTICIPO'] *= -1

    # Formatear fecha
    if 'FECHA ANTICIPO' in df.columns:
        df['FECHA ANTICIPO'] = pd.to_datetime(df['FECHA ANTICIPO'], errors='coerce').dt.strftime('%d-%m-%Y')

    # Aplicar formato colombiano
    if 'VALOR ANTICIPO' in df.columns:
        df['VALOR ANTICIPO'] = df['VALOR ANTICIPO'].apply(formato_colombiano)

    # Validaciones
    if df.empty or len(df.columns) == 0:
        print("❌ ERROR: No hay datos para procesar.")
        return

    # Crear carpeta de salida si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generar nombre de archivo con fecha/hora
    ahora = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_path = os.path.join(OUTPUT_DIR, f'ANTICIPO_PROCESADO_{ahora}.xlsx')

    # Guardar archivo
    df.to_excel(output_path, index=False)

    print(f"\n✅ Archivo de anticipos procesado y guardado en: {output_path}")
    print(f"📊 Registros procesados: {len(df)}")
    print(f"🗂 Columnas generadas: {len(df.columns)}")

# -------------------------
# Menú interactivo
# -------------------------

def menu():
    while True:
        print("\n=== Menú de Procesamiento de Anticipos ===")
        print("1. Procesar archivo de anticipos")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            input_file = input("Ingrese la ruta del archivo de anticipos: ").strip('"')
            try:
                procesar_anticipos(input_file)
            except Exception as e:
                print(f"\n❌ Error: {e}")
        elif opcion == "2":
            print("👋 Saliendo del programa...")
            sys.exit(0)
        else:
            print("⚠ Opción no válida, intente de nuevo.")

# -------------------------
# Ejecución
# -------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        procesar_anticipos(input_file)
    else:
        menu()
