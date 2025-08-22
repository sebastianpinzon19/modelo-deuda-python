#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI para Modelo de Deuda - Versión Corregida
Interfaz gráfica para procesar modelo de deuda con formato correcto
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from datetime import datetime
from pathlib import Path

# Importar el modelo corregido
from modelo_deuda import procesar_modelo_deuda
from trm_config import load_trm, save_trm, parse_trm_value, format_trm_display

class ModeloDeudaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modelo de Deuda - Procesador v2.0")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variables
        self.cartera_file = tk.StringVar()
        self.anticipos_file = tk.StringVar()
        self.trm_usd = tk.StringVar()
        self.trm_eur = tk.StringVar()
        self.output_path = tk.StringVar()
        
        # Cargar TRM guardadas
        self.cargar_trm_guardadas()
        
        # Crear interfaz
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crea la interfaz gráfica"""
        
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="PROCESADOR MODELO DE DEUDA", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sección Archivos
        ttk.Label(main_frame, text="ARCHIVOS DE ENTRADA", 
                 font=('Arial', 12, 'bold')).grid(row=1, column=0, columnspan=3, 
                                                 sticky=tk.W, pady=(0, 10))
        
        # Archivo Cartera
        ttk.Label(main_frame, text="Archivo Cartera:").grid(row=2, column=0, sticky=tk.W, pady=5)
        cartera_entry = ttk.Entry(main_frame, textvariable=self.cartera_file, width=50)
        cartera_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5))
        ttk.Button(main_frame, text="Buscar", 
                  command=lambda: self.seleccionar_archivo(self.cartera_file, "Cartera")
                  ).grid(row=2, column=2, padx=(5, 0))
        
        # Archivo Anticipos
        ttk.Label(main_frame, text="Archivo Anticipos:").grid(row=3, column=0, sticky=tk.W, pady=5)
        anticipos_entry = ttk.Entry(main_frame, textvariable=self.anticipos_file, width=50)
        anticipos_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 5))
        ttk.Button(main_frame, text="Buscar", 
                  command=lambda: self.seleccionar_archivo(self.anticipos_file, "Anticipos")
                  ).grid(row=3, column=2, padx=(5, 0))
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=4, column=0, columnspan=3, 
                                                          sticky=(tk.W, tk.E), pady=20)
        
        # Sección TRM
        ttk.Label(main_frame, text="TASAS DE CAMBIO (TRM)", 
                 font=('Arial', 12, 'bold')).grid(row=5, column=0, columnspan=3, 
                                                 sticky=tk.W, pady=(0, 10))
        
        # Información TRM guardadas
        self.info_trm_label = ttk.Label(main_frame, text=self.obtener_info_trm(), 
                                       foreground='blue', font=('Arial', 9))
        self.info_trm_label.grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # TRM Dólar
        ttk.Label(main_frame, text="TRM Dólar (USD):").grid(row=7, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.trm_usd, width=20).grid(row=7, column=1, 
                                                                       sticky=tk.W, padx=(10, 0))
        
        # TRM Euro
        ttk.Label(main_frame, text="TRM Euro (EUR):").grid(row=8, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.trm_eur, width=20).grid(row=8, column=1, 
                                                                       sticky=tk.W, padx=(10, 0))
        
        # Botón actualizar TRM
        ttk.Button(main_frame, text="🔄 Actualizar TRM", 
                  command=self.actualizar_trm_desde_web).grid(row=9, column=0, columnspan=2, 
                                                             pady=10, sticky=tk.W)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=10, column=0, columnspan=3, 
                                                          sticky=(tk.W, tk.E), pady=20)
        
        # Sección Salida
        ttk.Label(main_frame, text="ARCHIVO DE SALIDA", 
                 font=('Arial', 12, 'bold')).grid(row=11, column=0, columnspan=3, 
                                                 sticky=tk.W, pady=(0, 10))
        
        ttk.Label(main_frame, text="Ruta de salida (opcional):").grid(row=12, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=12, column=1, 
                                                                           sticky=(tk.W, tk.E), padx=(10, 5))
        ttk.Button(main_frame, text="Buscar", 
                  command=self.seleccionar_salida).grid(row=12, column=2, padx=(5, 0))
        
        # Nota sobre archivo de salida
        nota_salida = ttk.Label(main_frame, 
                               text="Si no especifica ruta, se creará automáticamente en PROVCA_PROCESADOS", 
                               foreground='gray', font=('Arial', 9))
        nota_salida.grid(row=13, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=14, column=0, columnspan=3, 
                                                          sticky=(tk.W, tk.E), pady=20)
        
        # Botón procesar
        self.btn_procesar = ttk.Button(main_frame, text="🚀 PROCESAR MODELO DE DEUDA", 
                                      command=self.iniciar_procesamiento)
        self.btn_procesar.grid(row=15, column=0, columnspan=3, pady=20)
        
        # Configurar estilo del botón principal
        style = ttk.Style()
        style.configure('Proceso.TButton', font=('Arial', 11, 'bold'))
        self.btn_procesar.configure(style='Proceso.TButton')
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=16, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        self.progress_bar.grid_remove()  # Ocultar inicialmente
        
        # Label de estado
        self.status_label = ttk.Label(main_frame, text="Listo para procesar", 
                                     foreground='green', font=('Arial', 10))
        self.status_label.grid(row=17, column=0, columnspan=3, pady=10)
        
        # Información del proceso
        info_frame = ttk.LabelFrame(main_frame, text="Información del Proceso", padding="10")
        info_frame.grid(row=18, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        info_frame.columnconfigure(0, weight=1)
        
        info_text = """
HOJAS GENERADAS:
• PESOS: Deuda en moneda nacional (líneas CT80, ED41-47, PL10-69)
• DIVISAS: Deuda en divisas convertida a pesos (líneas PL11, PL18, PL57, PL41)
• VENCIMIENTO: Consolidado por rangos de vencimiento con totales por moneda
• INFORMACIÓN: Detalles del proceso y TRM utilizadas

FORMATO:
• Números con formato colombiano (punto miles, coma decimal)
• Totales por moneda resaltados
• Conversión automática de divisas a pesos
        """
        
        ttk.Label(info_frame, text=info_text.strip(), font=('Arial', 9), 
                 justify=tk.LEFT).grid(row=0, column=0, sticky=(tk.W, tk.N))
    
    def cargar_trm_guardadas(self):
        """Carga las TRM guardadas en los campos"""
        try:
            cfg = load_trm()
            if cfg.get('usd'):
                self.trm_usd.set(format_trm_display(cfg.get('usd')))
            if cfg.get('eur'):
                self.trm_eur.set(format_trm_display(cfg.get('eur')))
        except:
            pass
    
    def obtener_info_trm(self):
        """Obtiene información de las TRM guardadas"""
        try:
            cfg = load_trm()
            usd_val = format_trm_display(cfg.get("usd")) if cfg.get("usd") else "No definida"
            eur_val = format_trm_display(cfg.get("eur")) if cfg.get("eur") else "No definida"
            updated_at = cfg.get("updated_at", "Nunca")
            
            return f"TRM guardadas: USD {usd_val} | EUR {eur_val} | Actualizada: {updated_at}"
        except:
            return "No hay TRM guardadas"
    
    def actualizar_trm_desde_web(self):
        """Actualiza TRM desde web (placeholder para futuro)"""
        messagebox.showinfo("Información", 
                           "Funcionalidad de actualización automática desde web\n" +
                           "será implementada en próxima versión.\n\n" +
                           "Por ahora, ingrese manualmente las TRM actuales.")
    
    def seleccionar_archivo(self, variable, tipo):
        """Selecciona archivo de entrada"""
        archivo = filedialog.askopenfilename(
            title=f"Seleccionar archivo de {tipo}",
            filetypes=[
                ("Todos los archivos soportados", "*.xlsx;*.xls;*.csv"),
                ("Archivos Excel", "*.xlsx;*.xls"), 
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ]
        )
        if archivo:
            variable.set(archivo)
    
    def seleccionar_salida(self):
        """Selecciona archivo de salida"""
        archivo = filedialog.asksaveasfilename(
            title="Guardar modelo de deuda como...",
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.output_path.set(archivo)
    
    def validar_datos(self):
        """Valida que todos los datos necesarios estén completos"""
        errores = []
        
        # Validar archivos
        if not self.cartera_file.get() or not os.path.exists(self.cartera_file.get()):
            errores.append("Debe seleccionar un archivo de cartera válido")
        
        if not self.anticipos_file.get() or not os.path.exists(self.anticipos_file.get()):
            errores.append("Debe seleccionar un archivo de anticipos válido")
        
        # Validar TRM
        try:
            trm_usd = parse_trm_value(self.trm_usd.get())
            if not trm_usd or trm_usd <= 0:
                errores.append("TRM Dólar debe ser un valor positivo")
        except:
            errores.append("TRM Dólar no es un valor válido")
        
        try:
            trm_eur = parse_trm_value(self.trm_eur.get())
            if not trm_eur or trm_eur <= 0:
                errores.append("TRM Euro debe ser un valor positivo")
        except:
            errores.append("TRM Euro no es un valor válido")
        
        return errores
    
    def iniciar_procesamiento(self):
        """Inicia el procesamiento en un hilo separado"""
        errores = self.validar_datos()
        if errores:
            messagebox.showerror("Errores de Validación", "\n".join(errores))
            return
        
        # Desactivar botón y mostrar progreso
        self.btn_procesar.configure(state='disabled')
        self.progress_bar.grid()
        self.status_label.configure(text="Procesando...", foreground='blue')
        
        # Iniciar procesamiento en hilo separado
        thread = threading.Thread(target=self.procesar_modelo)
        thread.daemon = True
        thread.start()
    
    def procesar_modelo(self):
        """Ejecuta el procesamiento del modelo de deuda"""
        try:
            # Actualizar progreso
            self.root.after(0, lambda: self.progress_var.set(10))
            self.root.after(0, lambda: self.status_label.configure(text="Leyendo archivos..."))
            
            # Obtener valores
            cartera_file = self.cartera_file.get()
            anticipos_file = self.anticipos_file.get()
            trm_usd = parse_trm_value(self.trm_usd.get())
            trm_eur = parse_trm_value(self.trm_eur.get())
            
            # Determinar archivo de salida
            output_path = self.output_path.get()
            if not output_path:
                base_dir = Path(__file__).resolve().parent
                output_dir = base_dir / 'PROVCA_PROCESADOS'
                output_dir.mkdir(parents=True, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = str(output_dir / f'1_Modelo_Deuda_{timestamp}.xlsx')
            
            self.root.after(0, lambda: self.progress_var.set(30))
            self.root.after(0, lambda: self.status_label.configure(text="Procesando cartera..."))
            
            # Procesar modelo
            resultado = procesar_modelo_deuda(
                cartera_file, 
                anticipos_file, 
                trm_usd, 
                trm_eur, 
                output_path
            )
            
            # Guardar TRM utilizadas
            save_trm(trm_usd, trm_eur)
            
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.status_label.configure(text="¡Completado!", foreground='green'))
            
            # Mostrar resultado exitoso
            mensaje = f"""
MODELO DE DEUDA GENERADO EXITOSAMENTE

📁 Archivo: {os.path.basename(resultado)}
📂 Ubicación: {os.path.dirname(resultado)}

💱 TRM utilizadas:
   • Dólar: {trm_usd:,.2f}
   • Euro: {trm_eur:,.2f}

📊 Hojas generadas:
   • PESOS (moneda nacional)
   • DIVISAS (convertidas a pesos)
   • VENCIMIENTO (consolidado)
   • INFORMACIÓN (detalles del proceso)

¿Desea abrir la carpeta donde se guardó el archivo?
            """.strip()
            
            respuesta = messagebox.askyesno("¡Proceso Completado!", mensaje)
            if respuesta:
                self.abrir_carpeta_resultado(resultado)
                
        except Exception as e:
            self.root.after(0, lambda: self.progress_var.set(0))
            self.root.after(0, lambda: self.status_label.configure(text="Error en procesamiento", foreground='red'))
            messagebox.showerror("Error de Procesamiento", f"Ocurrió un error:\n\n{str(e)}")
        
        finally:
            # Reactivar interfaz
            self.root.after(0, lambda: self.btn_procesar.configure(state='normal'))
            self.root.after(0, lambda: self.progress_bar.grid_remove())
            self.root.after(0, lambda: self.actualizar_info_trm())
    
    def abrir_carpeta_resultado(self, archivo_resultado):
        """Abre la carpeta donde se guardó el resultado"""
        try:
            import subprocess
            import platform
            
            carpeta = os.path.dirname(archivo_resultado)
            
            if platform.system() == "Windows":
                subprocess.run(["explorer", carpeta])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", carpeta])
            else:  # Linux
                subprocess.run(["xdg-open", carpeta])
        except:
            messagebox.showinfo("Ubicación del archivo", 
                              f"El archivo se guardó en:\n{archivo_resultado}")
    
    def actualizar_info_trm(self):
        """Actualiza la información de TRM mostrada"""
        self.info_trm_label.configure(text=self.obtener_info_trm())


class SplashScreen:
    """Pantalla de bienvenida"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # Crear ventana splash
        self.splash = tk.Toplevel()
        self.splash.title("Modelo de Deuda")
        self.splash.geometry("500x300")
        self.splash.resizable(False, False)
        self.splash.configure(bg='white')
        
        # Centrar en pantalla
        self.splash.transient(parent)
        self.splash.grab_set()
        
        # Contenido
        title_frame = tk.Frame(self.splash, bg='#366092', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="MODELO DE DEUDA", 
                font=('Arial', 18, 'bold'), fg='white', bg='#366092').pack(expand=True)
        
        content_frame = tk.Frame(self.splash, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(content_frame, text="Procesador de Cartera y Anticipos", 
                font=('Arial', 12), bg='white').pack(pady=10)
        
        tk.Label(content_frame, 
                text="Genera modelo de deuda consolidado con:\n" +
                     "• Deuda en pesos\n" + 
                     "• Deuda en divisas convertida\n" +
                     "• Análisis por vencimiento\n" +
                     "• Formato profesional Excel",
                font=('Arial', 10), bg='white', justify=tk.LEFT).pack(pady=10)
        
        tk.Label(content_frame, text="Versión 2.0 - 2025", 
                font=('Arial', 9), fg='gray', bg='white').pack(pady=10)
        
        # Cerrar automáticamente después de 2 segundos
        self.splash.after(2000, self.cerrar_splash)
        
        # Centrar la ventana splash
        self.centrar_ventana()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.splash.update_idletasks()
        x = (self.splash.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.splash.winfo_screenheight() // 2) - (300 // 2)
        self.splash.geometry(f"500x300+{x}+{y}")
    
    def cerrar_splash(self):
        """Cierra la pantalla splash"""
        self.splash.grab_release()
        self.splash.destroy()


def main():
    """Función principal de la aplicación"""
    
    # Crear ventana principal (oculta inicialmente)
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    # Mostrar splash screen
    splash = SplashScreen(root)
    root.wait_window(splash.splash)  # Esperar que se cierre el splash
    
    # Mostrar ventana principal
    root.deiconify()
    
    # Crear aplicación
    app = ModeloDeudaGUI(root)
    
    # Centrar ventana principal
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (700 // 2)
    y = (root.winfo_screenheight() // 2) - (600 // 2)
    root.geometry(f"700x600+{x}+{y}")
    
    # Configurar cierre
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Está seguro que desea cerrar la aplicación?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Iniciar aplicación
    root.mainloop()


if __name__ == "__main__":
    main()