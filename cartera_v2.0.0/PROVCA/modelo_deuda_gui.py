import tkinter as tk
from tkinter import filedialog, messagebox
import os
from modelo_deuda import procesar_modelo
from trm_config import load_trm, save_trm

def seleccionar_cartera():
    archivo = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if archivo:
        entrada_cartera.delete(0, tk.END)
        entrada_cartera.insert(0, archivo)

def seleccionar_anticipos():
    archivo = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if archivo:
        entrada_anticipos.delete(0, tk.END)
        entrada_anticipos.insert(0, archivo)

def procesar():
    cartera_file = entrada_cartera.get()
    anticipos_file = entrada_anticipos.get()
    try:
        cfg = load_trm()
        usd_text = entrada_trm_dolar.get().strip()
        eur_text = entrada_trm_euro.get().strip()
        trm_dolar = float(usd_text.replace(',', '.')) if usd_text != '' else (cfg.get('usd') or 0.0)
        trm_euro = float(eur_text.replace(',', '.')) if eur_text != '' else (cfg.get('eur') or 0.0)
    except ValueError:
        messagebox.showerror("Error", "TRM debe ser un número.")
        return

    if not os.path.exists(cartera_file) or not os.path.exists(anticipos_file):
        messagebox.showerror("Error", "Debe seleccionar los archivos de cartera y anticipos.")
        return

    try:
        ruta_salida = procesar_modelo(cartera_file, anticipos_file, trm_dolar, trm_euro)    
        save_trm(trm_dolar, trm_euro)
        messagebox.showinfo("Éxito", f"Se usó TRM USD={trm_dolar} y EUR={trm_euro}\nArchivo generado:\n{ruta_salida}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --------------------------
# Main
# --------------------------
ventana = tk.Tk()
ventana.title("Modelo de Deuda - Interfaz Gráfica")
ventana.geometry("550x350")

# Campos de selección de archivos
tk.Label(ventana, text="Archivo Cartera:").pack()
entrada_cartera = tk.Entry(ventana, width=50)
entrada_cartera.pack()
tk.Button(ventana, text="Seleccionar", command=seleccionar_cartera).pack()

tk.Label(ventana, text="Archivo Anticipos:").pack()
entrada_anticipos = tk.Entry(ventana, width=50)
entrada_anticipos.pack()
tk.Button(ventana, text="Seleccionar", command=seleccionar_anticipos).pack()

# Campos TRM
cfg = load_trm()
info_trm = f"TRM guardadas → USD: {cfg.get('usd')}  |  EUR: {cfg.get('eur')}" if cfg else ""
tk.Label(ventana, text=info_trm).pack(pady=4)

tk.Label(ventana, text="TRM Dólar (deje vacío para usar guardada):").pack()
entrada_trm_dolar = tk.Entry(ventana)
entrada_trm_dolar.pack()
if cfg and cfg.get('usd') is not None:
    entrada_trm_dolar.insert(0, str(cfg.get('usd')))

tk.Label(ventana, text="TRM Euro (deje vacío para usar guardada):").pack()
entrada_trm_euro = tk.Entry(ventana)
entrada_trm_euro.pack()
if cfg and cfg.get('eur') is not None:
    entrada_trm_euro.insert(0, str(cfg.get('eur')))

# Botón procesar
tk.Button(ventana, text="Procesar", command=procesar, bg="green", fg="white").pack(pady=10)

ventana.mainloop()
