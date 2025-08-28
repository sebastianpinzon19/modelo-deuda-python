#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador Unificado de Cartera - Grupo Planeta
Versión Optimizada con GUI integrado
Procesa Balance, Situación, Focus, Dotación y Acumulado
"""

import os
import sys
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
from typing import Dict, Optional, Tuple, Any

# ========================================
# CONFIGURACIÓN
# ========================================

OUTPUT_DIR = r"C:\wamp64\www\modelo-deuda-python\cartera_v2.0.0\PROVCA_PROCESADOS"

CONFIG = {
    "files_patterns": {
        "balance": ["balance"],
        "situacion": ["situacion"],
        "focus": ["focus"],
        "dotacion": ["provca", "provision", "dotacion", "prov"],
        "acumulado": ["acumulado"]
    },
    "balance": {
        "cuentas_objetivo": [
            "43001", "43002.20", "43002.21", "43002.15", 
            "43002.28", "43002.31", "43002.63", "43008", "43042"
        ],
        "saldo_columna_preferida": ["saldo", "aaf", "variacion"]
    },
    "situacion": {
        "fila_objetivo": ["total", "01010"],
        "columna_objetivo": ["saldo", "mes"]
    },
    "focus": {
        "hoja_preferida": ["españa", "espana"],
        "vencimientos": {
            "no_vencido": ["por_vencer", "no vencido", "no_vencida"],
            "vencido_30": ["vencido 30", "30 dias", "30 días", "1-30"],
            "vencido_60": ["60 dias", "60 días", "31-60", "vencido 60"],
            "vencido_90": ["90 dias", "90 días", "61-90", "vencido 90"],
            "vencido_mas_90": ["+90", "mas de 90", "más de 90", ">=90"]
        }
    },
    "acumulado": {
        "fila_objetivo": 54,
        "columnas_rango": (1, 6)  # B a F (índices 1-5)
    },
    "calculos": {
        "cobro_vencida_divisor": 1000.0,
        "cobro_total_divisor": -1000.0
    }
}

# ========================================
# UTILIDADES
# ========================================

def asegurar_directorio():
    """Crea el directorio de salida si no existe"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def timestamp():
    """Genera timestamp para nombres de archivo"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def convertir_valor(valor) -> float:
    """Convierte strings con formato colombiano/latino a float"""
    try:
        if valor is None or (isinstance(valor, float) and pd.isna(valor)):
            return 0.0
        if isinstance(valor, (int, float)):
            return float(valor)
        
        s = str(valor).strip().replace('\u200b', '').replace(' ', '')
        if s == '' or s.lower() == 'nan':
            return 0.0
            
        # Remover símbolos
        s = s.replace('$', '').replace('(', '-').replace(')', '')
        
        # Manejar formato latino (punto como separador de miles, coma como decimal)
        if '.' in s and ',' in s:
            s = s.replace('.', '').replace(',', '.')
        elif ',' in s and '.' not in s:
            s = s.replace(',', '.')
            
        # Limpiar caracteres no numéricos excepto punto y signo negativo
        s = re.sub(r'[^0-9\.\-]', '', s)
        
        if s in ('', '-', '.', '-.'):
            return 0.0
            
        return float(s)
    except:
        return 0.0

def buscar_archivo_patron(carpeta: str, patrones: list) -> Optional[str]:
    """Busca archivo que contenga alguno de los patrones"""
    if not os.path.exists(carpeta):
        return None
        
    archivos = os.listdir(carpeta)
    for archivo in archivos:
        nombre_lower = archivo.lower()
        if any(patron in nombre_lower for patron in patrones):
            if nombre_lower.endswith(('.xlsx', '.xls', '.csv')):
                return os.path.join(carpeta, archivo)
    return None

def leer_excel_multihoja(ruta: str) -> pd.DataFrame:
    """Lee todas las hojas de un Excel y las concatena"""
    xls = pd.ExcelFile(ruta)
    frames = []
    
    for hoja in xls.sheet_names:
        try:
            df = pd.read_excel(ruta, sheet_name=hoja, dtype=str)
            if not df.empty:
                df.columns = [str(c).strip().upper() for c in df.columns]
                df["__HOJA__"] = hoja
                frames.append(df)
        except Exception:
            continue
            
    if not frames:
        raise ValueError(f"No se pudieron leer hojas válidas de: {os.path.basename(ruta)}")
    
    return pd.concat(frames, ignore_index=True)

def encontrar_columna(columnas: list, palabras_clave: list) -> Optional[str]:
    """Encuentra columna que contenga todas las palabras clave"""
    for col in columnas:
        col_lower = str(col).lower()
        if all(palabra.lower() in col_lower for palabra in palabras_clave):
            return col
    return None

def encontrar_columnas_any(columnas: list, palabras_clave: list) -> list:
    """Encuentra columnas que contengan alguna de las palabras clave"""
    encontradas = []
    for col in columnas:
        col_lower = str(col).lower()
        if any(palabra.lower() in col_lower for palabra in palabras_clave):
            encontradas.append(col)
    return encontradas

# ========================================
# PROCESADORES ESPECÍFICOS
# ========================================

class ProcesadorBalance:
    def __init__(self, config: dict):
        self.config = config
    
    def procesar(self, ruta: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Procesa archivo de balance y retorna balance normalizado y sumas"""
        df = leer_excel_multihoja(ruta)
        
        # Encontrar columnas
        col_division = encontrar_columna(df.columns, ["div"]) or df.columns[0]
        col_cuenta = encontrar_columna(df.columns, ["cuenta"]) or df.columns[1]
        
        # Preferir columna con "saldo aaf variación"
        col_saldo = encontrar_columna(df.columns, self.config["saldo_columna_preferida"])
        if not col_saldo:
            col_saldo = encontrar_columna(df.columns, ["saldo"]) or df.columns[-1]
        
        # Normalizar balance
        balance = df[[col_division, col_cuenta, col_saldo]].copy()
        balance.columns = ["DIVISION", "CUENTA", "SALDO"]
        balance["SALDO"] = balance["SALDO"].apply(convertir_valor)
        balance = balance.groupby(["DIVISION", "CUENTA"], as_index=False)["SALDO"].sum()
        
        # Calcular sumas por cuentas específicas
        sumas = self._calcular_sumas_cuentas(balance)
        
        return balance, sumas
    
    def _calcular_sumas_cuentas(self, df_balance: pd.DataFrame) -> pd.DataFrame:
        """Calcula sumas de cuentas específicas según documento"""
        resultados = []
        
        # Mapeo de cuentas según documento
        grupos_cuentas = {
            "Total_43001": ["43001"],
            "Total_43002_detalle": ["43002.20", "43002.21", "43002.15", "43002.28", "43002.31", "43002.63"],
            "Total_43008": ["43008"],
            "Total_43042": ["43042"]
        }
        
        for grupo, cuentas in grupos_cuentas.items():
            total = 0.0
            for cuenta in cuentas:
                # Buscar cuenta exacta o con prefijo 0080
                mask1 = df_balance["CUENTA"].astype(str).str.contains(rf"\b{re.escape(cuenta)}\b", na=False, case=False)
                mask2 = df_balance["CUENTA"].astype(str).str.contains(rf"0080\.{re.escape(cuenta)}", na=False, case=False)
                mask = mask1 | mask2
                total += df_balance.loc[mask, "SALDO"].sum()
            
            resultados.append({"Concepto": grupo, "Valor": total})
        
        return pd.DataFrame(resultados)

class ProcesadorSituacion:
    def __init__(self, config: dict):
        self.config = config
    
    def procesar(self, ruta: str) -> pd.DataFrame:
        """Procesa archivo de situación"""
        df = leer_excel_multihoja(ruta)
        
        # Encontrar columna SALDOS MES
        col_saldos = encontrar_columna(df.columns, self.config["columna_objetivo"])
        if not col_saldos:
            raise ValueError(f"No se encontró columna con las palabras clave {self.config['columna_objetivo']} en Situación")
        
        # Encontrar fila TOTAL 01010
        df_texto = df.astype(str).apply(lambda col: col.str.strip().str.upper())
        mask = df_texto.apply(
            lambda fila: all(palabra in " ".join(fila.values) for palabra in ["TOTAL", "01010"]),
            axis=1
        )
        
        if not mask.any():
            raise ValueError("No se encontró fila 'TOTAL 01010' en Situación")
        
        valor = convertir_valor(df.loc[mask, col_saldos].iloc[0])
        
        return pd.DataFrame({
            "Concepto": ["TOTAL_01010_SALDOS_MES"],
            "Valor": [valor]
        })

class ProcesadorFocus:
    def __init__(self, config: dict):
        self.config = config
    
    def procesar(self, ruta: str) -> pd.DataFrame:
        """Procesa archivo Focus de vencimientos"""
        # Intentar leer hoja España específicamente
        xls = pd.ExcelFile(ruta)
        hoja_objetivo = None
        
        for hoja in xls.sheet_names:
            if any(pref.lower() in hoja.lower() for pref in self.config["hoja_preferida"]):
                hoja_objetivo = hoja
                break
        
        if hoja_objetivo:
            df = pd.read_excel(ruta, sheet_name=hoja_objetivo, dtype=str)
            df.columns = [str(c).strip().upper() for c in df.columns]
        else:
            df = leer_excel_multihoja(ruta)
        
        # Convertir a numérico
        for col in df.columns:
            if col != "__HOJA__":
                df[col] = df[col].apply(convertir_valor)
        
        # Extraer vencimientos por categorías
        vencimientos = {}
        for categoria, patrones in self.config["vencimientos"].items():
            cols = encontrar_columnas_any(df.columns, patrones)
            total = df[cols].sum().sum() if cols else 0.0
            vencimientos[categoria] = float(total)
        
        # Calcular totales
        total_vencido = sum(v for k, v in vencimientos.items() if k != "no_vencido")
        total_no_vencido = vencimientos.get("no_vencido", 0.0)
        total_deuda = total_vencido + total_no_vencido
        
        # Preparar resultados
        resultados = []
        for categoria, valor in vencimientos.items():
            resultados.append({"Concepto": categoria.title(), "Valor": valor})
        
        resultados.extend([
            {"Concepto": "Total_Vencido", "Valor": total_vencido},
            {"Concepto": "Total_No_Vencido", "Valor": total_no_vencido},
            {"Concepto": "Total_Deuda", "Valor": total_deuda}
        ])
        
        return pd.DataFrame(resultados)
    
    def extraer_facturacion_q22_h22(self, ruta: str) -> float:
        """Extrae Q22-H22 de hoja España para facturación no vencida"""
        try:
            xls = pd.ExcelFile(ruta)
            hoja_esp = None
            
            for hoja in xls.sheet_names:
                if any(pref.lower() in hoja.lower() for pref in self.config["hoja_preferida"]):
                    hoja_esp = hoja
                    break
            
            if not hoja_esp:
                return 0.0
            
            # Leer sin encabezados para preservar coordenadas
            df = pd.read_excel(ruta, sheet_name=hoja_esp, header=None, dtype=str)
            
            # Fila 22 (índice 21), columnas Q (16) y H (7)
            fila = 21
            col_q = 16  # Q
            col_h = 7   # H
            
            if fila < len(df) and col_q < df.shape[1] and col_h < df.shape[1]:
                val_q = convertir_valor(df.iat[fila, col_q])
                val_h = convertir_valor(df.iat[fila, col_h])
                return val_q - val_h
            
        except Exception:
            pass
        
        return 0.0

class ProcesadorDotacion:
    def procesar(self, ruta: str) -> pd.DataFrame:
        """Procesa archivo de dotación/provisión"""
        df = leer_excel_multihoja(ruta)
        
        # Convertir a numérico
        for col in df.columns:
            if col != "__HOJA__":
                df[col] = df[col].apply(convertir_valor)
        
        # Buscar componentes
        interco_cols = encontrar_columnas_any(df.columns, ["interco", "resto"])
        acumuladas_cols = encontrar_columnas_any(df.columns, ["dotaciones", "acumuladas", "inicial"])
        provision_cols = encontrar_columnas_any(df.columns, ["provision", "mes"])
        
        interco_valor = df[interco_cols].sum().sum() if interco_cols else 0.0
        acumuladas_valor = df[acumuladas_cols].sum().sum() if acumuladas_cols else 0.0
        provision_valor = df[provision_cols].sum().sum() if provision_cols else 0.0
        
        # Cálculo según documento: Interco RESTO - Dotaciones Acumuladas (Inicial) - Provisión del mes
        dotacion_mes = interco_valor - acumuladas_valor - provision_valor
        
        return pd.DataFrame({
            "Concepto": ["Interco_RESTO", "Dotaciones_Acumuladas", "Provision_Mes", "Dotacion_Mes"],
            "Valor": [interco_valor, acumuladas_valor, provision_valor, dotacion_mes]
        })

class ProcesadorAcumulado:
    def __init__(self, config: dict):
        self.config = config
    
    def procesar(self, ruta: str) -> pd.DataFrame:
        """Procesa archivo de acumulado - extrae fila 54, columnas B-F"""
        # Leer sin encabezados para preservar estructura
        df = pd.read_excel(ruta, sheet_name=0, header=None, dtype=str)
        
        fila_objetivo = self.config["fila_objetivo"] - 1  # Convertir a índice 0
        inicio_col, fin_col = self.config["columnas_rango"]
        
        if fila_objetivo >= len(df):
            fila_objetivo = len(df) - 1
        
        resultados = []
        for i in range(inicio_col, min(fin_col, df.shape[1])):
            letra_col = chr(ord('A') + i)  # A=0, B=1, etc.
            concepto = f"Fila{self.config['fila_objetivo']}_Col_{letra_col}"
            valor = convertir_valor(df.iat[fila_objetivo, i])
            resultados.append({"Concepto": concepto, "Valor": valor})
        
        return pd.DataFrame(resultados)

# ========================================
# CALCULADOR DE RESUMEN
# ========================================

class CalculadorResumen:
    def __init__(self, config: dict):
        self.config = config
    
    def calcular(self, df_situacion: pd.DataFrame, df_focus: pd.DataFrame, 
                 df_dotacion: pd.DataFrame, facturacion_no_vencida: float = 0.0) -> pd.DataFrame:
        """Calcula resumen final según especificaciones del documento"""
        
        # Obtener valores base
        situacion_map = df_situacion.set_index("Concepto")["Valor"].to_dict()
        focus_map = df_focus.set_index("Concepto")["Valor"].to_dict()
        dotacion_map = df_dotacion.set_index("Concepto")["Valor"].to_dict()
        
        cobros_situacion = situacion_map.get("TOTAL_01010_SALDOS_MES", 0.0)
        total_vencido = focus_map.get("Total_Vencido", 0.0)
        total_no_vencido = focus_map.get("Total_No_Vencido", 0.0)
        vencido_30 = focus_map.get("Vencido_30", 0.0)
        vencido_60_mas = (focus_map.get("Vencido_60", 0.0) + 
                         focus_map.get("Vencido_90", 0.0) + 
                         focus_map.get("Vencido_Mas_90", 0.0))
        
        # Cálculos según documento Word
        # 4. Cobro mes - Vencida = (Deuda bruta vencidas - total vencido >=60) / 1000
        cobro_mes_vencida = (total_vencido - vencido_60_mas) / self.config["calculos"]["cobro_vencida_divisor"]
        
        # 5. Cobro mes - Total = COBROS SITUACION / -1000
        cobro_mes_total = cobros_situacion / self.config["calculos"]["cobro_total_divisor"]
        
        # 6. Cobros mes - No Vencida = Total - Vencida
        cobro_mes_no_vencida = cobro_mes_total - cobro_mes_vencida
        
        # 7. +/- Vencidos mes - vencido = VENCIDO MES 30 días (positivo)
        ajuste_vencidos_vencido = vencido_30
        
        # 8. +/- Vencidos mes - No vencido = valor opuesto
        ajuste_vencidos_no_vencido = -ajuste_vencidos_vencido
        
        # 9. +/- Vencidos mes - Total = vencido - no vencido
        ajuste_vencidos_total = ajuste_vencidos_vencido - ajuste_vencidos_no_vencido
        
        # 10. Facturación mes - vencida = 0
        fact_mes_vencida = 0.0
        
        # 11. Facturación mes - no vencida = Q22-H22
        fact_mes_no_vencida = facturacion_no_vencida
        
        # Dotación del mes
        dotacion_mes = dotacion_map.get("Dotacion_Mes", 0.0)
        
        return pd.DataFrame({
            "Concepto": [
                "Cobros_Mes_Total", "Cobros_Mes_Vencida", "Cobros_Mes_No_Vencida",
                "Ajuste_Vencidos_Vencido", "Ajuste_Vencidos_No_Vencido", "Ajuste_Vencidos_Total",
                "Facturacion_Mes_Vencida", "Facturacion_Mes_No_Vencida",
                "Total_Vencido", "Total_No_Vencido", "Total_Deuda",
                "Dotacion_Mes"
            ],
            "Valor": [
                cobro_mes_total, cobro_mes_vencida, cobro_mes_no_vencida,
                ajuste_vencidos_vencido, ajuste_vencidos_no_vencido, ajuste_vencidos_total,
                fact_mes_vencida, fact_mes_no_vencida,
                total_vencido, total_no_vencido, total_vencido + total_no_vencido,
                dotacion_mes
            ]
        })

# ========================================
# PROCESADOR PRINCIPAL
# ========================================

class ProcesadorCarteraUnificado:
    def __init__(self):
        self.config = CONFIG
        asegurar_directorio()
        
        # Inicializar procesadores
        self.proc_balance = ProcesadorBalance(self.config["balance"])
        self.proc_situacion = ProcesadorSituacion(self.config["situacion"])
        self.proc_focus = ProcesadorFocus(self.config["focus"])
        self.proc_dotacion = ProcesadorDotacion()
        self.proc_acumulado = ProcesadorAcumulado(self.config["acumulado"])
        self.calculador = CalculadorResumen(self.config)
    
    def descubrir_archivos(self, carpeta: str) -> Dict[str, Optional[str]]:
        """Descubre archivos automáticamente en la carpeta"""
        archivos = {}
        for tipo, patrones in self.config["files_patterns"].items():
            archivos[tipo] = buscar_archivo_patron(carpeta, patrones)
        return archivos
    
    def procesar_carpeta(self, carpeta: str) -> str:
        """Procesa todos los archivos de una carpeta"""
        archivos = self.descubrir_archivos(carpeta)
        return self.procesar_archivos(**archivos)
    
    def procesar_archivos(self, balance: str = None, situacion: str = None, 
                         focus: str = None, dotacion: str = None, acumulado: str = None) -> str:
        """Procesa archivos individuales y genera Excel consolidado"""
        
        resultados = {}
        
        # Validar archivos requeridos
        archivos_requeridos = {"balance": balance, "situacion": situacion, "focus": focus}
        faltantes = [k for k, v in archivos_requeridos.items() if not v or not os.path.exists(v)]
        
        if faltantes:
            raise FileNotFoundError(f"Archivos faltantes o no encontrados: {', '.join(faltantes)}")
        
        # Procesar Balance
        print("Procesando Balance...")
        df_balance, df_balance_sumas = self.proc_balance.procesar(balance)
        resultados["Balance_Normalizado"] = df_balance
        resultados["Balance_Sumas_Cuentas"] = df_balance_sumas
        
        # Procesar Situación
        print("Procesando Situación...")
        df_situacion = self.proc_situacion.procesar(situacion)
        resultados["Situacion_Total_01010"] = df_situacion
        
        # Procesar Focus
        print("Procesando Focus...")
        df_focus = self.proc_focus.procesar(focus)
        resultados["Focus_Vencimientos"] = df_focus
        
        # Extraer facturación no vencida (Q22-H22)
        facturacion_no_vencida = self.proc_focus.extraer_facturacion_q22_h22(focus)
        
        # Procesar Dotación (opcional)
        if dotacion and os.path.exists(dotacion):
            print("Procesando Dotación...")
            df_dotacion = self.proc_dotacion.procesar(dotacion)
            resultados["Dotacion_Mes"] = df_dotacion
        else:
            print("Dotación no encontrada, usando valores por defecto...")
            df_dotacion = pd.DataFrame({
                "Concepto": ["Dotacion_Mes"], 
                "Valor": [0.0]
            })
        
        # Procesar Acumulado (opcional)
        if acumulado and os.path.exists(acumulado):
            print("Procesando Acumulado...")
            df_acumulado = self.proc_acumulado.procesar(acumulado)
            resultados["Acumulado"] = df_acumulado
        
        # Calcular Resumen Final
        print("Calculando resumen final...")
        df_resumen = self.calculador.calcular(df_situacion, df_focus, df_dotacion, facturacion_no_vencida)
        resultados["Resumen_Final"] = df_resumen
        
        # Guardar archivo Excel consolidado
        return self._guardar_excel_consolidado(resultados)
    
    def _guardar_excel_consolidado(self, resultados: Dict[str, pd.DataFrame]) -> str:
        """Guarda todas las hojas en un Excel consolidado"""
        nombre_archivo = f"procesamiento_cartera_unificado_{timestamp()}.xlsx"
        ruta_salida = os.path.join(OUTPUT_DIR, nombre_archivo)
        
        with pd.ExcelWriter(ruta_salida, engine="xlsxwriter") as writer:
            workbook = writer.book
            
            # Formato para números con separador de miles
            formato_numero = workbook.add_format({
                'num_format': '#,##0.00',
                'align': 'right'
            })
            
            for nombre_hoja, df in resultados.items():
                # Limitar nombre de hoja a 31 caracteres
                nombre_corto = nombre_hoja[:31]
                df.to_excel(writer, sheet_name=nombre_corto, index=False)
                
                worksheet = writer.sheets[nombre_corto]
                
                # Aplicar formato a columnas numéricas
                if 'Valor' in df.columns:
                    col_idx = df.columns.get_loc('Valor')
                    worksheet.set_column(col_idx, col_idx, 15, formato_numero)
                
                # Auto-ajustar ancho de columnas
                for i, col in enumerate(df.columns):
                    max_len = max(len(str(col)), df[col].astype(str).str.len().max())
                    worksheet.set_column(i, i, min(max_len + 2, 50))
        
        print(f"Archivo consolidado generado: {ruta_salida}")
        return ruta_salida

# ========================================
# GUI
# ========================================

class CarteraGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Procesador Unificado de Cartera - Grupo Planeta")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.procesador = ProcesadorCarteraUnificado()
        self.archivos = {
            "balance": tk.StringVar(),
            "situacion": tk.StringVar(), 
            "focus": tk.StringVar(),
            "dotacion": tk.StringVar(),
            "acumulado": tk.StringVar()
        }
        
        self._crear_interfaz()
        
    def _crear_interfaz(self):
        """Crea la interfaz gráfica"""
        # Título
        titulo = tk.Label(self.root, text="Procesador Unificado de Cartera", 
                         font=("Arial", 16, "bold"))
        titulo.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sección de selección de archivos
        archivos_frame = ttk.LabelFrame(main_frame, text="Selección de Archivos", padding=10)
        archivos_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Archivos individuales
        row = 0
        archivos_info = {
            "balance": ("Balance", "Archivo de balance contable", True),
            "situacion": ("Situación", "Archivo de situación financiera", True),
            "focus": ("Focus", "Archivo de vencimientos Focus", True),
            "dotacion": ("Dotación/Provisión", "Archivo de provisión del mes", False),
            "acumulado": ("Acumulado", "Archivo de datos acumulados", False)
        }
        
        for key, (nombre, descripcion, requerido) in archivos_info.items():
            # Etiqueta
            label_text = f"{nombre}{'*' if requerido else ''}:"
            label = ttk.Label(archivos_frame, text=label_text, width=20)
            label.grid(row=row, column=0, sticky=tk.W, padx=(0, 10), pady=5)
            
            # Entry
            entry = ttk.Entry(archivos_frame, textvariable=self.archivos[key], width=50)
            entry.grid(row=row, column=1, sticky=tk.EW, padx=(0, 10), pady=5)
            
            # Botón seleccionar
            btn = ttk.Button(archivos_frame, text="Seleccionar", 
                           command=lambda k=key: self._seleccionar_archivo(k))
            btn.grid(row=row, column=2, padx=(0, 10), pady=5)
            
            # Tooltip con descripción
            self._crear_tooltip(label, descripcion)
            
            row += 1
        
        # Configurar expansión de columnas
        archivos_frame.columnconfigure(1, weight=1)
        
        # Separador
        ttk.Separator(archivos_frame, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=3, sticky=tk.EW, pady=10)
        row += 1
        
        # Botón seleccionar carpeta
        ttk.Button(archivos_frame, text="🗂️ Seleccionar Carpeta (Auto-detectar)", 
                  command=self._seleccionar_carpeta).grid(
            row=row, column=0, columnspan=3, pady=10)
        
        # Frame de acciones
        acciones_frame = ttk.Frame(main_frame)
        acciones_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botón procesar
        self.btn_procesar = ttk.Button(acciones_frame, text="🚀 Procesar Archivos", 
                                      command=self._procesar, style="Accent.TButton")
        self.btn_procesar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón limpiar
        ttk.Button(acciones_frame, text="🗑️ Limpiar", 
                  command=self._limpiar_campos).pack(side=tk.LEFT)
        
        # Frame de progreso y log
        progress_frame = ttk.LabelFrame(main_frame, text="Progreso", padding=10)
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Área de log
        log_frame = ttk.Frame(progress_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD, 
                               font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Información en la parte inferior
        info_text = ("* Archivos requeridos: Balance, Situación, Focus\n"
                    "Los archivos Dotación y Acumulado son opcionales")
        ttk.Label(main_frame, text=info_text, foreground="gray").pack(pady=5)
    
    def _crear_tooltip(self, widget, text):
        """Crea tooltip para un widget"""
        def mostrar_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="lightyellow", 
                           relief="solid", borderwidth=1, wraplength=300)
            label.pack()
        
        def ocultar_tooltip(event):
            for child in widget.winfo_children():
                if isinstance(child, tk.Toplevel):
                    child.destroy()
        
        widget.bind("<Enter>", mostrar_tooltip)
        widget.bind("<Leave>", ocultar_tooltip)
    
    def _seleccionar_archivo(self, tipo):
        """Selecciona archivo individual"""
        filetypes = [
            ("Archivos Excel", "*.xlsx *.xls"),
            ("Archivos CSV", "*.csv"),
            ("Todos los archivos", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title=f"Seleccionar archivo {tipo.title()}",
            filetypes=filetypes
        )
        
        if filename:
            self.archivos[tipo].set(filename)
            self._log(f"Seleccionado {tipo}: {os.path.basename(filename)}")
    
    def _seleccionar_carpeta(self):
        """Selecciona carpeta y auto-detecta archivos"""
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta con archivos")
        
        if not carpeta:
            return
        
        self._log(f"Analizando carpeta: {carpeta}")
        
        # Auto-detectar archivos
        archivos_encontrados = self.procesador.descubrir_archivos(carpeta)
        
        for tipo, ruta in archivos_encontrados.items():
            if ruta:
                self.archivos[tipo].set(ruta)
                self._log(f"Auto-detectado {tipo}: {os.path.basename(ruta)}")
            else:
                self.archivos[tipo].set("")
                self._log(f"No se encontró archivo para {tipo}")
    
    def _limpiar_campos(self):
        """Limpia todos los campos"""
        for var in self.archivos.values():
            var.set("")
        self.log_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        self._log("Campos limpiados")
    
    def _log(self, mensaje):
        """Agrega mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def _actualizar_progreso(self, valor, mensaje=""):
        """Actualiza barra de progreso"""
        self.progress_var.set(valor)
        if mensaje:
            self._log(mensaje)
        self.root.update_idletasks()
    
    def _procesar(self):
        """Procesa los archivos seleccionados"""
        try:
            # Limpiar log anterior
            self.log_text.delete(1.0, tk.END)
            self._actualizar_progreso(0, "Iniciando procesamiento...")
            
            # Desactivar botón durante procesamiento
            self.btn_procesar.config(state="disabled")
            
            # Obtener rutas de archivos
            rutas_archivos = {k: v.get().strip() for k, v in self.archivos.items()}
            
            # Validar archivos requeridos
            requeridos = ["balance", "situacion", "focus"]
            faltantes = []
            
            for req in requeridos:
                if not rutas_archivos[req] or not os.path.exists(rutas_archivos[req]):
                    faltantes.append(req)
            
            if faltantes:
                raise ValueError(f"Archivos requeridos faltantes: {', '.join(faltantes)}")
            
            self._actualizar_progreso(10, "Archivos validados correctamente")
            
            # Si hay archivos individuales, procesarlos directamente
            if all(rutas_archivos[req] for req in requeridos):
                self._actualizar_progreso(20, "Procesando archivos individuales...")
                
                # Procesar cada archivo
                resultado = self.procesador.procesar_archivos(
                    balance=rutas_archivos["balance"],
                    situacion=rutas_archivos["situacion"],
                    focus=rutas_archivos["focus"],
                    dotacion=rutas_archivos["dotacion"] if rutas_archivos["dotacion"] else None,
                    acumulado=rutas_archivos["acumulado"] if rutas_archivos["acumulado"] else None
                )
                
            else:
                # Si no hay archivos individuales, intentar carpeta
                carpeta = os.path.dirname(rutas_archivos["balance"]) if rutas_archivos["balance"] else None
                if not carpeta:
                    raise ValueError("No se puede determinar carpeta de procesamiento")
                
                self._actualizar_progreso(20, f"Procesando carpeta: {carpeta}")
                resultado = self.procesador.procesar_carpeta(carpeta)
            
            self._actualizar_progreso(100, "Procesamiento completado exitosamente")
            
            # Mostrar resultado
            mensaje_exito = (
                f"✅ Procesamiento completado exitosamente\n\n"
                f"Archivo generado:\n{resultado}\n\n"
                f"¿Desea abrir la carpeta de destino?"
            )
            
            respuesta = messagebox.askyesno("Procesamiento Completado", mensaje_exito)
            
            if respuesta:
                # Abrir carpeta en explorador
                import subprocess
                subprocess.run(f'explorer "{OUTPUT_DIR}"', shell=True)
                
        except Exception as e:
            self._actualizar_progreso(0, f"❌ Error: {str(e)}")
            messagebox.showerror("Error de Procesamiento", f"Ocurrió un error:\n\n{str(e)}")
        
        finally:
            # Reactivar botón
            self.btn_procesar.config(state="normal")
    
    def ejecutar(self):
        """Inicia la aplicación GUI"""
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Centrar ventana en pantalla
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_width()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_height()) // 2
        self.root.geometry(f"+{x}+{y}")
        
        # Mensaje de bienvenida
        self._log("Bienvenido al Procesador Unificado de Cartera")
        self._log("Seleccione los archivos individuales o una carpeta para comenzar")
        
        # Iniciar loop principal
        self.root.mainloop()

# ========================================
# INTERFAZ DE LÍNEA DE COMANDOS
# ========================================

def main_cli():
    """Interfaz de línea de comandos"""
    if len(sys.argv) < 2:
        print("Uso: python procesador_cartera_unificado.py [carpeta] [--gui]")
        print("  carpeta: Ruta de la carpeta con los archivos")
        print("  --gui: Abrir interfaz gráfica")
        return
    
    if "--gui" in sys.argv:
        gui = CarteraGUI()
        gui.ejecutar()
        return
    
    carpeta = sys.argv[1]
    
    if not os.path.isdir(carpeta):
        print(f"Error: {carpeta} no es una carpeta válida")
        return
    
    try:
        print("="*60)
        print("PROCESADOR UNIFICADO DE CARTERA - GRUPO PLANETA")
        print("="*60)
        
        procesador = ProcesadorCarteraUnificado()
        resultado = procesador.procesar_carpeta(carpeta)
        
        print(f"\n✅ Procesamiento completado exitosamente")
        print(f"📁 Archivo generado: {resultado}")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error durante el procesamiento: {str(e)}")
        sys.exit(1)

# ========================================
# PUNTO DE ENTRADA
# ========================================

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Sin argumentos, abrir GUI
        gui = CarteraGUI()
        gui.ejecutar()
    else:
        # Con argumentos, usar CLI
        main_cli()