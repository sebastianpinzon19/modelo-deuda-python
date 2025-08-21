#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interfaz gráfica (Tkinter) para Procesador Unificado de Cartera
- Usa el motor procesador_unificado (con pandas)
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import procesador_unificado as proc   # importa tu script con la lógica

class ProcesadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesador Unificado de Cartera")
        self.root.geometry("600x400")

        self.files = {
            "Balance": tk.StringVar(),
            "Situacion": tk.StringVar(),
            "Focus": tk.StringVar(),
            "Dotacion": tk.StringVar(),
            "Acumulado": tk.StringVar()
        }

        # Etiquetas y botones
        row = 0
        for key in self.files.keys():
            tk.Label(root, text=key, width=15, anchor="w").grid(row=row, column=0, padx=5, pady=5)
            tk.Entry(root, textvariable=self.files[key], width=50).grid(row=row, column=1, padx=5, pady=5)
            tk.Button(root, text="Seleccionar", command=lambda k=key: self.select_file(k)).grid(row=row, column=2, padx=5, pady=5)
            row += 1

        # Botón para seleccionar carpeta
        tk.Button(root, text="Seleccionar carpeta (auto detectar)", command=self.select_folder).grid(row=row, column=0, columnspan=3, pady=10)
        row += 1

        # Botón de procesar
        tk.Button(root, text="Procesar", bg="green", fg="white", command=self.procesar).grid(row=row, column=0, columnspan=3, pady=20)

    def select_file(self, key):
        filetypes = [("Excel/CSV", "*.xlsx *.xls *.csv")]
        filename = filedialog.askopenfilename(title=f"Seleccionar archivo {key}", filetypes=filetypes)
        if filename:
            self.files[key].set(filename)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta con archivos")
        if not folder:
            return
        balance, situacion, focus, dotacion, acumulado = proc.descubrir_archivos(folder)
        self.files["Balance"].set(balance or "")
        self.files["Situacion"].set(situacion or "")
        self.files["Focus"].set(focus or "")
        self.files["Dotacion"].set(dotacion or "")
        self.files["Acumulado"].set(acumulado or "")

    def procesar(self):
        try:
            # Si todos los archivos están seleccionados manualmente
            if all(self.files[k].get() for k in self.files):
                carpeta = os.path.dirname(self.files["Balance"].get())
                # Guardamos archivos en carpeta temporal y procesamos
                # Calcular facturación no vencida (Q22-H22) desde Focus hoja España
                fact_no_vencida_es = proc.extraer_facturacion_no_vencida_focus_es(self.files["Focus"].get(), fila=22, col_q="Q", col_h="H")
                out = proc.guardar_excel_salida(
                    carpeta,
                    Balance_Normalizado=proc.procesar_balance(self.files["Balance"].get()),
                    Balance_Sumas_Cuentas=proc.sumar_cuentas_balance(proc.procesar_balance(self.files["Balance"].get())),
                    Situacion_Total_01010=proc.procesar_situacion(self.files["Situacion"].get()),
                    Focus_Vencimientos=proc.procesar_focus(self.files["Focus"].get()),
                    Dotacion_Mes=proc.procesar_dotacion(self.files["Dotacion"].get()),
                    Acumulado=proc.procesar_acumulado(self.files["Acumulado"].get()),
                    Resumen_Final=proc.construir_resumen(
                        proc.procesar_situacion(self.files["Situacion"].get()),
                        proc.procesar_focus(self.files["Focus"].get()),
                        proc.procesar_dotacion(self.files["Dotacion"].get()),
                        fact_no_vencida_override=fact_no_vencida_es
                    ),
                    Resumen_Matriz=proc.construir_resumen_matriz(
                        proc.procesar_situacion(self.files["Situacion"].get()),
                        proc.procesar_focus(self.files["Focus"].get()),
                        proc.procesar_dotacion(self.files["Dotacion"].get()),
                        fact_no_vencida_override=fact_no_vencida_es
                    )
                )
            else:
                # Si faltan archivos, pedimos carpeta y procesamos automático
                carpeta = filedialog.askdirectory(title="Seleccionar carpeta con archivos")
                if not carpeta:
                    return
                out = proc.ejecutar_proceso(carpeta)

            messagebox.showinfo("Éxito", f"Procesamiento completado.\nArchivo generado en:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcesadorGUI(root)
    root.mainloop()
