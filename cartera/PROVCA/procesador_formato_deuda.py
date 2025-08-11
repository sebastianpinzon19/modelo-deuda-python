#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Formato Deuda
Sistema de Procesamiento de Cartera - Grupo Planeta
Versión: 2.0.1
"""

import time
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List, Optional, Union
from config import (
    TIPOS_PROCESAMIENTO, CONFIG_PROCESAMIENTO, DIRECTORIOS,
    obtener_timestamp, obtener_fecha_actual
)
from logger import crear_logger, log_funcion
from utilidades_cartera import UtilidadesCartera

class ProcesadorFormatoDeuda:
    def __init__(self):
        self.logger = crear_logger("ProcesadorFormatoDeuda")
        self.utilidades = UtilidadesCartera()
    
    @log_funcion
    def procesar_formato_deuda(self, ruta_archivo: str, anticipos_path: str = None, trm: float = 1.0) -> Tuple[str, Dict[str, Any]]:
        """
        Procesa archivo de formato deuda (procesador principal) según reglas de negocio.
        """
        try:
            self.logger.info(f"Iniciando procesamiento de formato deuda: {ruta_archivo}")
            self.utilidades.validar_archivo(ruta_archivo)
            df = self.utilidades.leer_archivo(ruta_archivo)
            df = self.utilidades.limpiar_dataframe(df)
            df.columns = df.columns.str.strip().str.upper()

            # Filtrar líneas en pesos y divisas
            lineas_pesos = [
                ("CT", 80), ("ED", 41), ("ED", 44), ("ED", 47), ("PL", 10), ("PL", 15), ("PL", 20), ("PL", 21),
                ("PL", 23), ("PL", 25), ("PL", 28), ("PL", 29), ("PL", 31), ("PL", 32), ("PL", 53), ("PL", 56),
                ("PL", 60), ("PL", 62), ("PL", 63), ("PL", 64), ("PL", 65), ("PL", 66), ("PL", 69)
            ]
            lineas_divisas = [
                ("PL", 11), ("PL", 18), ("PL", 57), ("PL", 41)
            ]
            df_pesos = df[df.apply(lambda x: (x.get("CODIGO","").strip(), int(x.get("EMPRESA",0))) in lineas_pesos, axis=1)].copy()
            df_divisas = df[df.apply(lambda x: (x.get("CODIGO","").strip(), int(x.get("EMPRESA",0))) in lineas_divisas, axis=1)].copy()

            # Integrar anticipos si se provee
            if anticipos_path:
                self.utilidades.validar_archivo(anticipos_path)
                anticipos = self.utilidades.leer_archivo(anticipos_path)
                anticipos.columns = anticipos.columns.str.strip().str.upper()
                # Ajustar anticipos a estructura de provisión
                anticipos["SALDO"] = anticipos["VALOR ANTICIPO"] * -1
                anticipos["SALDO POR VENCER"] = anticipos["SALDO"]
                anticipos["SALDO NO VENCIDO"] = anticipos["SALDO"]
                anticipos = anticipos.reindex(columns=df_pesos.columns, fill_value=None)
                df_pesos = pd.concat([df_pesos, anticipos], ignore_index=True)

            # Calcular vencimientos por rangos
            def calcular_vencimientos(row, fecha_cierre):
                dias_vencido = (fecha_cierre - pd.to_datetime(row["FECHA VTO"]).normalize()).days if pd.notna(row["FECHA VTO"]) else 0
                buckets = {
                    "NO_VENCIDO": 0, "VENCIDO_30": 0, "VENCIDO_60": 0, "VENCIDO_90": 0,
                    "VENCIDO_180": 0, "VENCIDO_360": 0, "VENCIDO_MAS_360": 0
                }
                saldo = row.get("SALDO", 0)
                if dias_vencido < 0:
                    buckets["NO_VENCIDO"] = saldo
                elif dias_vencido < 30:
                    buckets["NO_VENCIDO"] = saldo
                elif dias_vencido < 60:
                    buckets["VENCIDO_30"] = saldo
                elif dias_vencido < 90:
                    buckets["VENCIDO_60"] = saldo
                elif dias_vencido < 180:
                    buckets["VENCIDO_90"] = saldo
                elif dias_vencido < 360:
                    buckets["VENCIDO_180"] = saldo
                elif dias_vencido < 370:
                    buckets["VENCIDO_360"] = saldo
                else:
                    buckets["VENCIDO_MAS_360"] = saldo
                return pd.Series(buckets)

            fecha_cierre = pd.Timestamp.now().normalize()
            for df_ in [df_pesos, df_divisas]:
                vencimientos = df_.apply(lambda row: calcular_vencimientos(row, fecha_cierre), axis=1)
                for col in vencimientos.columns:
                    df_[col] = vencimientos[col]
                # Validar suma de vencimientos = saldo
                df_["VALIDA_VENCIMIENTOS"] = np.isclose(df_[["NO_VENCIDO","VENCIDO_30","VENCIDO_60","VENCIDO_90","VENCIDO_180","VENCIDO_360","VENCIDO_MAS_360"]].sum(axis=1), df_["SALDO"], atol=1)

            # Totales y TRM para divisas
            if not df_divisas.empty:
                df_divisas["SALDO_TRM"] = df_divisas["SALDO"] * trm

            # Crear hoja vencimiento (totales por cliente y bucket)
            def hoja_vencimiento(df_, moneda):
                cols = ["CLIENTE","SALDO","NO_VENCIDO","VENCIDO_30","VENCIDO_60","VENCIDO_90","VENCIDO_180","VENCIDO_360","VENCIDO_MAS_360"]
                if not all(c in df_.columns for c in cols):
                    return pd.DataFrame()
                resumen = df_.groupby("CLIENTE")[cols[1:]].sum().reset_index()
                resumen["MONEDA"] = moneda
                return resumen
            hoja_venc_pesos = hoja_vencimiento(df_pesos, "PESOS")
            hoja_venc_divisas = hoja_vencimiento(df_divisas, "DIVISAS")

            # Guardar en Excel con varias hojas
            nombre_salida = self.utilidades.generar_nombre_archivo_salida("formato_deuda_procesado")
            ruta_salida = self.utilidades.obtener_ruta_resultado(nombre_salida)
            with pd.ExcelWriter(ruta_salida, engine="xlsxwriter") as writer:
                df_pesos.to_excel(writer, sheet_name="pesos", index=False)
                df_divisas.to_excel(writer, sheet_name="divisas", index=False)
                hoja_venc_pesos.to_excel(writer, sheet_name="vencimiento_pesos", index=False)
                hoja_venc_divisas.to_excel(writer, sheet_name="vencimiento_divisas", index=False)

            resumen = {
                "registros_pesos": len(df_pesos),
                "registros_divisas": len(df_divisas),
                "archivo": ruta_salida
            }
            self.logger.info("Procesamiento de formato deuda completado exitosamente")
            return ruta_salida, resumen
        except Exception as e:
            self.logger.error(f"Error en procesamiento de formato deuda: {e}")
            raise

    @log_funcion
    def procesar_datos_formato_deuda(self, df) -> Any:
        """
        Procesa los datos de formato deuda
        """
        # Copiar dataframe original
        df_procesado = df.copy()
        
        # Normalizar nombres de columnas
        df_procesado.columns = df_procesado.columns.str.strip().str.upper()
        
        # Procesar columnas de texto
        columnas_texto = df_procesado.select_dtypes(include=['object']).columns
        for columna in columnas_texto:
            df_procesado[columna] = df_procesado[columna].apply(self.utilidades.limpiar_texto)
        
        # Procesar columnas numéricas
        columnas_numericas = df_procesado.select_dtypes(include=['numpy.number']).columns
        for columna in columnas_numericas:
            df_procesado[columna] = pd.to_numeric(df_procesado[columna], errors='coerce')
        
        # Procesar fechas
        columnas_fecha = []
        for columna in df_procesado.columns:
            if any(palabra in columna.upper() for palabra in ['FECHA', 'DATE', 'FECHA_', 'DATE_']):
                columnas_fecha.append(columna)
        
        for columna in columnas_fecha:
            df_procesado[columna] = df_procesado[columna].apply(self.utilidades.convertir_fecha)
        
        # Agregar columnas calculadas específicas de formato deuda
        df_procesado = self.agregar_columnas_formato_deuda(df_procesado)
        
        # Ordenar por columnas relevantes
        columnas_orden = []
        for columna in ['CLIENTE', 'CUENTA', 'FECHA_VENCIMIENTO', 'SALDO_DEUDA']:
            if columna in df_procesado.columns:
                columnas_orden.append(columna)
        
        if columnas_orden:
            df_procesado = df_procesado.sort_values(columnas_orden)
        
        return df_procesado

    @log_funcion
    def agregar_columnas_formato_deuda(self, df) -> Any:
        """
        Agrega columnas calculadas específicas para formato deuda
        """
        import pandas as pd
        import numpy as np
        
        # Agregar columnas de análisis
        if 'SALDO_DEUDA' in df.columns:
            df['SALDO_DEUDA_NUM'] = pd.to_numeric(df['SALDO_DEUDA'], errors='coerce')
            df['DEUDA_VENCIDA'] = df['SALDO_DEUDA_NUM'].apply(lambda x: x if x > 0 else 0)
        
        if 'FECHA_VENCIMIENTO' in df.columns:
            df['DIAS_VENCIDO'] = df['FECHA_VENCIMIENTO'].apply(
                lambda x: (pd.Timestamp.now() - pd.to_datetime(x)).days if pd.notna(x) else 0
            )
            df['ESTADO_VENCIMIENTO'] = df['DIAS_VENCIDO'].apply(
                lambda x: 'VENCIDO' if x > 0 else 'AL_DIA'
            )
        
        # Agregar columnas de clasificación
        if 'SALDO_DEUDA_NUM' in df.columns:
            df['CLASIFICACION_DEUDA'] = df['SALDO_DEUDA_NUM'].apply(
                lambda x: 'ALTA' if x > 100000 else 'MEDIA' if x > 10000 else 'BAJA'
            )
        
        return df

    @log_funcion
    def crear_analisis_formato_deuda(self, df) -> Dict[str, Any]:
        """
        Crea análisis detallado del formato deuda
        """
        analisis = {
            'total_registros': len(df),
            'total_deuda': 0,
            'deuda_vencida': 0,
            'clientes_unicos': 0,
            'cuentas_unicas': 0
        }
        
        if 'SALDO_DEUDA_NUM' in df.columns:
            analisis['total_deuda'] = df['SALDO_DEUDA_NUM'].sum()
            analisis['deuda_vencida'] = df[df['DIAS_VENCIDO'] > 0]['SALDO_DEUDA_NUM'].sum()
        
        if 'CLIENTE' in df.columns:
            analisis['clientes_unicos'] = df['CLIENTE'].nunique()
        
        if 'CUENTA' in df.columns:
            analisis['cuentas_unicas'] = df['CUENTA'].nunique()
        
        return analisis

def main():
    """
    Función principal para ejecución directa
    """
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='Procesador de Formato Deuda')
    parser.add_argument('archivo', help='Ruta del archivo a procesar')
    parser.add_argument('--output', '-o', help='Archivo de salida (opcional)')
    
    args = parser.parse_args()
    
    try:
        procesador = ProcesadorFormatoDeuda()
        ruta_salida, resumen = procesador.procesar_formato_deuda(args.archivo)
        
        print(f"✅ Procesamiento completado exitosamente")
        print(f"📁 Archivo de salida: {ruta_salida}")
        print(f"📊 Resumen: {resumen}")
        
    except Exception as e:
        print(f"❌ Error en el procesamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 