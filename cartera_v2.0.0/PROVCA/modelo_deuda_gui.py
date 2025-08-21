import tkinter as tk
from tkinter import filedialog, messagebox
import os
from modelo_deuda import procesar_modelo_deuda
from trm_config import load_trm, save_trm, parse_trm_value, format_trm_display

# -------------------------------
# Funciones auxiliares
# -------------------------------
def seleccionar_archivo(entrada):
    archivo = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
    if archivo:
        entrada.delete(0, tk.END)
        entrada.insert(0, archivo)

def procesar():
    cartera_file = entrada_cartera.get().strip()
    anticipos_file = entrada_anticipos.get().strip()

    if not os.path.exists(cartera_file):
        messagebox.showerror("Error", "Debe seleccionar el archivo de cartera.")
        return
    if not os.path.exists(anticipos_file):
        messagebox.showerror("Error", "Debe seleccionar el archivo de anticipos.")
        return

    # Leer TRM guardadas
    cfg = load_trm()
    try:
        usd_text = entrada_trm_dolar.get().strip().replace(",", ".")
        eur_text = entrada_trm_euro.get().strip().replace(",", ".")

        trm_dolar = float(usd_text) if usd_text else float(cfg.get("usd", 0.0))
        trm_euro = float(eur_text) if eur_text else float(cfg.get("eur", 0.0))

    except ValueError:
        messagebox.showerror("Error", "TRM debe ser un número válido.")
        return

    try:
        ruta_salida = procesar_modelo_deuda(cartera_file, anticipos_file, trm_dolar, trm_euro)
        save_trm(trm_dolar, trm_euro)
        messagebox.showinfo(
            "Éxito",
            f"Se usó TRM USD={trm_dolar:,.2f} y EUR={trm_euro:,.2f}\n\nArchivo generado:\n{ruta_salida}"
        )
    except Exception as e:
        messagebox.showerror("Error en procesamiento", str(e))

# -------------------------------
# Interfaz gráfica
# -------------------------------
ventana = tk.Tk()
ventana.title("Modelo de Deuda - Interfaz Gráfica")
ventana.geometry("600x350")

# Archivo Cartera
tk.Label(ventana, text="Archivo Cartera:").pack()
entrada_cartera = tk.Entry(ventana, width=60)
entrada_cartera.pack()
tk.Button(ventana, text="Seleccionar", command=lambda: seleccionar_archivo(entrada_cartera)).pack()

# Archivo Anticipos
tk.Label(ventana, text="Archivo Anticipos:").pack(pady=5)
entrada_anticipos = tk.Entry(ventana, width=60)
entrada_anticipos.pack()
tk.Button(ventana, text="Seleccionar", command=lambda: seleccionar_archivo(entrada_anticipos)).pack()

# Info TRM guardada
try:
    cfg = load_trm()
    info_trm = f"TRM guardadas → USD: {format_trm_display(cfg.get('usd'))} | EUR: {format_trm_display(cfg.get('eur'))}"
except FileNotFoundError:
    info_trm = "No se encontraron TRM guardadas. Se usarán 0.0."
    cfg = {}
except Exception:
    info_trm = "No se pudieron cargar las TRM guardadas."
    cfg = {}
tk.Label(ventana, text=info_trm).pack(pady=6)

# TRM Dólar
tk.Label(ventana, text="TRM Dólar (deje vacío para usar guardada):").pack()
entrada_trm_dolar = tk.Entry(ventana)
entrada_trm_dolar.pack()
if cfg.get("usd") is not None:
    entrada_trm_dolar.insert(0, str(cfg.get("usd")))

# TRM Euro
tk.Label(ventana, text="TRM Euro (deje vacío para usar guardada):").pack()
entrada_trm_euro = tk.Entry(ventana)
entrada_trm_euro.pack()
if cfg.get("eur") is not None:
    entrada_trm_euro.insert(0, str(cfg.get("eur")))

# Botón procesar
tk.Button(ventana, text="Procesar", command=procesar, bg="green", fg="white", width=15).pack(pady=15)

ventana.mainloop()