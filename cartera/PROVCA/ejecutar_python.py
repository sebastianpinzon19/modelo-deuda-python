#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Anticipos
Sistema de Procesamiento de Cartera - Grupo Planeta
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import logging
from tkinter import Tk, filedialog, messagebox
from utilidades_cartera import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def procesar_anticipos(ruta_archivo):
    try:
        logging.info(f"Iniciando procesamiento de anticipos: {ruta_archivo}")
        validar_archivo(ruta_archivo)
        df = leer_archivo(ruta_archivo)
        logging.info(f"Archivo leído: {len(df)} registros")
        df = limpiar_dataframe(df)
        logging.info(f"Dataframe limpiado: {len(df)} registros")
        df_procesado = procesar_datos_anticipos(df)
        nombre_salida = generar_nombre_archivo_salida("anticipos_procesados")
        ruta_salida = os.path.join("resultados", nombre_salida)
        crear_directorio_si_no_existe("resultados")
        escribir_resultado(df_procesado, ruta_salida)
        resumen = crear_resumen_procesamiento(df, df_procesado, "Anticipos")
        logging.info("Procesamiento de anticipos completado exitosamente")
        return ruta_salida, resumen
    except Exception as e:
        logging.error(f"Error en procesamiento de anticipos: {e}")
        raise

# Las demás funciones se mantienen igual: procesar_datos_anticipos, agregar_columnas_anticipos, crear_analisis_anticipos...

def mostrar_menu_y_procesar():
    """
    Menú gráfico para seleccionar archivo y procesarlo
    """
    root = Tk()
    root.withdraw()  # Ocultar ventana principal

    messagebox.showinfo("Procesador de Anticipos", "Seleccione el archivo de anticipos a procesar.")
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de anticipos",
        filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")]
    )

    if not ruta_archivo:
        messagebox.showwarning("Procesador cancelado", "No se seleccionó ningún archivo.")
        return

    try:
        ruta_salida, resumen = procesar_anticipos(ruta_archivo)
        messagebox.showinfo("Éxito", f"Archivo procesado correctamente:\n{ruta_salida}")
        print("Resumen del procesamiento:")
        print(resumen)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo:\n{e}")

def main():
    mostrar_menu_y_procesar()

if __name__ == "__main__":
    main()
