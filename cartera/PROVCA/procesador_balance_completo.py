#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador Completo de Balance - Grupo Planeta
Maneja archivos Excel (BALANCE, SITUACIÓN, FOCUS) y realiza cálculos financieros completos
"""

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import json
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProcesadorBalanceCompleto:
    def __init__(self):
        self.results = {}
        self.mes_cierre = None
        
    def procesar_archivo_balance(self, file_path: str) -> Dict[str, Any]:
        """Procesa el archivo BALANCE según las especificaciones"""
        logger.info(f"Procesando archivo BALANCE: {file_path}")
        
        try:
            # Leer archivo Excel
            df = pd.read_excel(file_path, engine='openpyxl')
            logger.info(f"Archivo BALANCE leído correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
            
            # Buscar columna "Saldo AAF variación"
            columna_saldo = None
            for col in df.columns:
                if 'Saldo AAF variación' in str(col):
                    columna_saldo = col
                    break
            
            if columna_saldo is None:
                raise ValueError('No se encontró la columna "Saldo AAF variación"')
            
            # Buscar columna de cuenta objeto
            columna_cuenta = None
            for col in df.columns:
                if 'cuenta objeto' in str(col).lower() or 'cuenta' in str(col).lower():
                    columna_cuenta = col
                    break
            
            if columna_cuenta is None:
                raise ValueError('No se encontró la columna de cuenta objeto')
            
            results = {}
            
            # Procesar cuentas objeto: 43001, 43008, 43042
            cuentas_objeto = ['43001', '43008', '43042']
            for cuenta in cuentas_objeto:
                mask = df[columna_cuenta].astype(str).str.contains(cuenta, na=False)
                total = df.loc[mask, columna_saldo].sum()
                results[f"total_{cuenta}"] = float(total)
                logger.info(f"Total cuenta {cuenta}: {total}")
            
            # Procesar subcuentas específicas
            subcuentas = ['0080.43002.20', '0080.43002.21', '0080.43002.15', 
                         '0080.43002.28', '0080.43002.31', '0080.43002.63']
            
            results['subcuentas'] = {}
            for subcuenta in subcuentas:
                mask = df[columna_cuenta].astype(str).str.contains(subcuenta, na=False)
                total = df.loc[mask, columna_saldo].sum()
                results['subcuentas'][subcuenta] = float(total)
                logger.info(f"Total subcuenta {subcuenta}: {total}")
            
            # Calcular totales
            total_43001 = results.get('total_43001', 0)
            total_43008 = results.get('total_43008', 0)
            total_43042 = results.get('total_43042', 0)
            total_subcuentas = sum(results['subcuentas'].values())
            
            results['total_general'] = total_43001 + total_43008 + total_43042 + total_subcuentas
            
            return results
            
        except Exception as e:
            logger.error(f"Error procesando archivo BALANCE: {str(e)}")
            raise
    
    def procesar_archivo_situacion(self, file_path: str) -> Dict[str, Any]:
        """Procesa el archivo SITUACIÓN según las especificaciones"""
        logger.info(f"Procesando archivo SITUACIÓN: {file_path}")
        
        try:
            # Leer archivo Excel
            df = pd.read_excel(file_path, engine='openpyxl')
            logger.info(f"Archivo SITUACIÓN leído correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
            
            # Buscar columna "SALDOS MES"
            columna_saldos_mes = None
            for col in df.columns:
                if 'SALDOS MES' in str(col):
                    columna_saldos_mes = col
                    break
            
            if columna_saldos_mes is None:
                raise ValueError('No se encontró la columna "SALDOS MES"')
            
            # Buscar TOTAL 01010
            columna_total = None
            for col in df.columns:
                if 'TOTAL 01010' in str(col) or '01010' in str(col):
                    columna_total = col
                    break
            
            if columna_total is None:
                raise ValueError('No se encontró la columna TOTAL 01010')
            
            # Buscar el valor de TOTAL 01010
            mask = df[columna_total].astype(str).str.contains('01010', na=False)
            if mask.any():
                valor_total = df.loc[mask, columna_saldos_mes].iloc[0]
                logger.info(f"TOTAL 01010 SALDOS MES: {valor_total}")
                return {'total_01010_saldos_mes': float(valor_total)}
            else:
                raise ValueError('No se encontró el valor TOTAL 01010')
                
        except Exception as e:
            logger.error(f"Error procesando archivo SITUACIÓN: {str(e)}")
            raise
    
    def procesar_archivo_focus(self, file_path: str) -> Dict[str, Any]:
        """Procesa el archivo FOCUS según las especificaciones"""
        logger.info(f"Procesando archivo FOCUS: {file_path}")
        
        try:
            # Leer archivo Excel
            df = pd.read_excel(file_path, engine='openpyxl')
            logger.info(f"Archivo FOCUS leído correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
            
            results = {}
            
            # Buscar datos de vencimientos (formato España)
            # Buscar Deuda bruta NO Grupo (Inicial y Final)
            deuda_inicial = self._buscar_valor_en_focus(df, 'Deuda bruta NO Grupo', 'Inicial')
            deuda_final = self._buscar_valor_en_focus(df, 'Deuda bruta NO Grupo', 'Final')
            
            results['deuda_bruta_no_grupo_inicial'] = deuda_inicial
            results['deuda_bruta_no_grupo_final'] = deuda_final
            
            # Buscar Dotaciones Acumuladas
            dotaciones_inicial = self._buscar_valor_en_focus(df, 'Dotaciones Acumuladas', 'Inicial')
            dotaciones_final = self._buscar_valor_en_focus(df, 'Dotaciones Acumuladas', 'Final')
            
            results['dotaciones_acumuladas_inicial'] = dotaciones_inicial
            results['dotaciones_acumuladas_final'] = dotaciones_final
            
            # Buscar Provisión acumulada
            provision_final = self._buscar_valor_en_focus(df, 'Provisión acumulada', 'Final')
            results['provision_acumulada_final'] = provision_final
            
            # Buscar datos de vencimientos (30 días, 60 días, etc.)
            vencido_30_dias = self._buscar_valor_en_focus(df, 'Vencido 30 días', 'Mes')
            vencido_60_dias = self._buscar_valor_en_focus(df, 'Vencido 60 días', 'Mes')
            
            results['vencido_30_dias'] = vencido_30_dias
            results['vencido_60_dias'] = vencido_60_dias
            
            return results
            
        except Exception as e:
            logger.error(f"Error procesando archivo FOCUS: {str(e)}")
            raise
    
    def _buscar_valor_en_focus(self, df: pd.DataFrame, concepto: str, periodo: str) -> float:
        """Busca un valor específico en el archivo FOCUS"""
        try:
            # Buscar en todas las columnas
            for col in df.columns:
                if concepto.lower() in str(col).lower():
                    # Buscar en la fila correspondiente
                    for idx, row in df.iterrows():
                        if periodo.lower() in str(row[col]).lower():
                            # Buscar el valor numérico en las columnas adyacentes
                            for col_valor in df.columns:
                                if pd.api.types.is_numeric_dtype(df[col_valor]):
                                    valor = row[col_valor]
                                    if pd.notna(valor) and valor != 0:
                                        return float(valor)
            return 0.0
        except:
            return 0.0
    
    def realizar_calculos_completos(self, balance_data: Dict, situacion_data: Dict, focus_data: Dict) -> Dict[str, Any]:
        """Realiza todos los cálculos financieros según las especificaciones"""
        logger.info("Realizando cálculos completos...")
        
        results = {}
        
        # 1. Tipos de cambio - Cambiar el mes de cierre y actualizar tasas de cambio
        # (Esto se manejaría con datos externos de tipos de cambio)
        results['mes_cierre'] = self.mes_cierre or datetime.now().strftime('%Y-%m')
        
        # 2. Deuda bruta NO Grupo (Inicial) = Deuda bruta NO Grupo (Final)
        deuda_final = focus_data.get('deuda_bruta_no_grupo_final', 0)
        results['deuda_bruta_no_grupo_inicial'] = deuda_final
        
        # 3. - Dotaciones Acumuladas (Inicial) = '+/- Provisión acumulada (Final)
        provision_final = focus_data.get('provision_acumulada_final', 0)
        results['dotaciones_acumuladas_inicial'] = provision_final
        
        # 4. Cobro de mes - Vencida = Deuda bruta NO Grupo (Inicial) Vencidas - Total vencido de 60 días en adelante / 1000
        deuda_inicial = focus_data.get('deuda_bruta_no_grupo_inicial', 0)
        vencido_60_dias = focus_data.get('vencido_60_dias', 0)
        results['cobro_mes_vencida'] = (deuda_inicial - vencido_60_dias) / 1000
        
        # 5. Cobro mes - Total Deuda = COBROS SITUACION (SALDO MES) / -1000
        cobros_situacion = situacion_data.get('total_01010_saldos_mes', 0)
        results['cobro_mes_total_deuda'] = cobros_situacion / -1000
        
        # 6. Cobros del mes - No Vencida = =H15-D15 (cobro total - cobro vencida)
        results['cobro_mes_no_vencida'] = results['cobro_mes_total_deuda'] - results['cobro_mes_vencida']
        
        # 7. +/- Vencidos en el mes – vencido = VENCIDO MES 30 días signo positivo
        vencido_30_dias = focus_data.get('vencido_30_dias', 0)
        results['vencidos_mes_vencido'] = vencido_30_dias
        
        # 8. +/- Vencidos en el mes – No vencido = D17 (mismo valor que vencido)
        results['vencidos_mes_no_vencido'] = results['vencidos_mes_vencido']
        
        # 9. '+/- Vencidos en el mes – Total deuda = D17 - F17
        results['vencidos_mes_total_deuda'] = results['vencidos_mes_vencido'] - results['vencidos_mes_no_vencido']
        
        # 10. + Facturación del mes – vencida = 0
        results['facturacion_mes_vencida'] = 0
        
        # 11. + Facturación del mes – no vencida = Deuda bruta NO Grupo (Final) - total deuda
        deuda_final = focus_data.get('deuda_bruta_no_grupo_final', 0)
        results['facturacion_mes_no_vencida'] = deuda_final - results['cobro_mes_total_deuda']
        
        # Dotación del mes
        # Del archivo de datos de la provisión del mes Interco RESTO
        # - Dotaciones Acumuladas (Inicial) - Provisión del mes
        dotaciones_inicial = focus_data.get('dotaciones_acumuladas_inicial', 0)
        provision_mes = focus_data.get('provision_acumulada_final', 0) - dotaciones_inicial
        results['dotacion_mes'] = dotaciones_inicial - provision_mes
        
        # Calcular totales para el cuadro final
        results['subtotal_1'] = results['cobro_mes_vencida'] + results['facturacion_mes_vencida'] + results['vencidos_mes_vencido']
        results['subtotal_2'] = results['cobro_mes_no_vencida'] + results['facturacion_mes_no_vencida'] + results['vencidos_mes_no_vencido']
        
        # ACUMULADO - Copiar fórmulas de B54 a F54
        results['acumulado_vencida'] = deuda_inicial + results['cobro_mes_vencida'] + results['facturacion_mes_vencida'] + results['vencidos_mes_vencido']
        results['acumulado_no_vencida'] = deuda_inicial + results['cobro_mes_no_vencida'] + results['facturacion_mes_no_vencida'] + results['vencidos_mes_no_vencido']
        
        return results
    
    def generar_reporte_final(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Genera el reporte final con el formato especificado"""
        
        reporte = {
            'resumen_calculos': {
                '- Cobros': {
                    'vencida': round(results.get('cobro_mes_vencida', 0), 3),
                    'no_vencida': round(results.get('cobro_mes_no_vencida', 0), 3)
                },
                '+ Facturación': {
                    'vencida': round(results.get('facturacion_mes_vencida', 0), 3),
                    'no_vencida': round(results.get('facturacion_mes_no_vencida', 0), 3)
                },
                '+/- Vencidos': {
                    'vencida': round(results.get('vencidos_mes_vencido', 0), 3),
                    'no_vencida': round(results.get('vencidos_mes_no_vencido', 0), 3)
                },
                'Subtotal': {
                    'vencida': round(results.get('subtotal_1', 0), 3),
                    'no_vencida': round(results.get('subtotal_2', 0), 3)
                }
            },
            'provision_dotacion': {
                'PROVISION': '',
                'DOTACION': round(results.get('dotacion_mes', 0), 3),
                '- Dotaciones': round(results.get('dotaciones_acumuladas_inicial', 0), 3),
                '+ Desdotaciones': round(results.get('provision_acumulada_final', 0), 3)
            },
            'acumulado': {
                'deuda_bruta_no_grupo_inicial': {
                    'vencida': round(results.get('deuda_bruta_no_grupo_inicial', 0), 2),
                    'no_vencida': round(results.get('deuda_bruta_no_grupo_inicial', 0), 2)
                },
                'cobros': {
                    'vencida': round(results.get('cobro_mes_vencida', 0), 3),
                    'no_vencida': round(results.get('cobro_mes_no_vencida', 0), 3)
                },
                'facturacion': {
                    'vencida': round(results.get('facturacion_mes_vencida', 0), 3),
                    'no_vencida': round(results.get('facturacion_mes_no_vencida', 0), 3)
                },
                'vencidos': {
                    'vencida': round(results.get('vencidos_mes_vencido', 0), 3),
                    'no_vencida': round(results.get('vencidos_mes_no_vencido', 0), 3)
                }
            },
            'deuda_final': {
                'deuda_bruta_no_grupo_final': round(results.get('deuda_bruta_no_grupo_final', 0), 2),
                'dotaciones_acumuladas_inicial': round(results.get('dotaciones_acumuladas_inicial', 0), 2),
                'dotaciones': round(results.get('dotacion_mes', 0), 2),
                'desdotaciones': round(results.get('provision_acumulada_final', 0), 2)
            }
        }
        
        return reporte
    
    def procesar_archivos(self, balance_file: str, situacion_file: str, focus_file: str) -> Dict[str, Any]:
        """Procesa todos los archivos y realiza los cálculos completos"""
        logger.info("Iniciando procesamiento completo de archivos...")
        
        try:
            # Procesar cada archivo
            balance_data = self.procesar_archivo_balance(balance_file)
            situacion_data = self.procesar_archivo_situacion(situacion_file)
            focus_data = self.procesar_archivo_focus(focus_file)
            
            # Realizar cálculos completos
            calculos = self.realizar_calculos_completos(balance_data, situacion_data, focus_data)
            
            # Generar reporte final
            reporte_final = self.generar_reporte_final(calculos)
            
            # Combinar todos los resultados
            resultados_completos = {
                'balance_data': balance_data,
                'situacion_data': situacion_data,
                'focus_data': focus_data,
                'calculos': calculos,
                'reporte_final': reporte_final,
                'timestamp': datetime.now().isoformat(),
                'mes_cierre': self.mes_cierre
            }
            
            # Guardar resultados en archivo JSON
            with open('resultados_balance_completo.json', 'w', encoding='utf-8') as f:
                json.dump(resultados_completos, f, ensure_ascii=False, indent=2)
            
            logger.info("Procesamiento completo finalizado exitosamente")
            return resultados_completos
            
        except Exception as e:
            logger.error(f"Error en el procesamiento completo: {str(e)}")
            raise

def main():
    """Función principal"""
    if len(sys.argv) != 4:
        print("Uso: python procesador_balance_completo.py <archivo_balance> <archivo_situacion> <archivo_focus>")
        sys.exit(1)
    
    balance_file = sys.argv[1]
    situacion_file = sys.argv[2]
    focus_file = sys.argv[3]
    
    # Verificar que los archivos existan
    for file_path in [balance_file, situacion_file, focus_file]:
        if not os.path.exists(file_path):
            print(f"Error: El archivo {file_path} no existe")
            sys.exit(1)
    
    try:
        procesador = ProcesadorBalanceCompleto()
        resultados = procesador.procesar_archivos(balance_file, situacion_file, focus_file)
        
        print("Procesamiento completado exitosamente")
        print(f"Resultados guardados en: resultados_balance_completo.json")
        
    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 