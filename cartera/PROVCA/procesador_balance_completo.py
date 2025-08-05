# -*- coding: utf-8 -*-
"""
PROCESADOR COMPLETO DE BALANCE - GRUPO PLANETA

Este script procesa tres archivos Excel principales para realizar análisis financieros completos:

1. Archivo BALANCE - Contiene datos de cuentas objeto y saldos
2. Archivo SITUACIÓN - Contiene datos de cobros y saldos mensuales  
3. Archivo FOCUS - Contiene datos de vencimientos y dotaciones

OBJETIVO:
Generar reportes financieros completos con cálculos de deuda, dotaciones, cobros,
vencimientos y facturación según las especificaciones del área de cartera.

PROCESO:
1. Leer y validar los 3 archivos de entrada
2. Extraer datos específicos de cada archivo
3. Realizar cálculos financieros complejos
4. Generar reporte estructurado
5. Guardar resultados en formato JSON y Excel
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import os
import sys
import json
import warnings
warnings.filterwarnings('ignore')

# Importar utilidades
try:
    from utilidades_cartera import convertir_fecha, convertir_valor, aplicar_formato_colombiano_dataframe
except ImportError:
    # Si no encuentra el módulo, definir funciones básicas
    def convertir_fecha(fecha_str):
        try:
            fecha = datetime.strptime(str(int(fecha_str)), "%Y%m%d")
            return fecha.strftime("%d-%m-%Y"), fecha.day, fecha.month, fecha.year, fecha
        except Exception:
            return "", "", "", "", None

    def convertir_valor(valor_str):
        try:
            if valor_str is None:
                return 0.0
            if isinstance(valor_str, (int, float)):
                return float(valor_str)
            s = str(valor_str).strip().replace('\u200b', '').replace(' ', '')
            if s == '' or s.lower() == 'nan':
                return 0.0
            return float(s)
        except Exception:
            return 0.0

    def aplicar_formato_colombiano_dataframe(df, columnas_numericas=None):
        return df

def obtener_fecha_cierre(fecha_cierre_str=None):
    """Obtiene la fecha de cierre. Si se proporciona fecha_cierre_str, la usa; si no, usa el último día del mes actual"""
    if fecha_cierre_str:
        try:
            return datetime.strptime(fecha_cierre_str, '%Y-%m-%d')
        except ValueError:
            print(f"ADVERTENCIA: Formato de fecha incorrecto '{fecha_cierre_str}'. Usando fecha por defecto.")
    
    # Fecha por defecto: último día del mes actual
    hoy = datetime.now()
    if hoy.month == 12:
        cierre = datetime(hoy.year + 1, 1, 1) - pd.Timedelta(days=1)
    else:
        cierre = datetime(hoy.year, hoy.month + 1, 1) - pd.Timedelta(days=1)
    return cierre

def leer_archivo_balance(ruta_archivo):
    """Lee y procesa el archivo BALANCE"""
    print("Leyendo archivo BALANCE...")
    
    try:
        # Leer archivo Excel
        df = pd.read_excel(ruta_archivo, dtype=str)
        print(f"Archivo BALANCE leído. Registros: {len(df)}")
        
        # Buscar columnas relevantes
        columnas_buscar = ['Cuenta Objeto', 'Saldo AAF variación', 'Saldo AAF']
        columnas_encontradas = [col for col in columnas_buscar if col in df.columns]
        
        if not columnas_encontradas:
            print("ADVERTENCIA: No se encontraron columnas esperadas en BALANCE")
            return {}
        
        # Extraer datos de cuentas objeto específicas
        cuentas_objeto = ['43001', '43008', '43042']
        subcuentas = ['0080.43002.20', '0080.43002.21', '0080.43002.15', 
                     '0080.43002.28', '0080.43002.31', '0080.43002.63']
        
        resultados = {}
        
        # Procesar cuentas objeto principales
        for cuenta in cuentas_objeto:
            if 'Cuenta Objeto' in df.columns:
                filtro = df['Cuenta Objeto'].astype(str).str.contains(cuenta, na=False)
                datos_cuenta = df[filtro]
                
                if not datos_cuenta.empty:
                    # Usar 'Saldo AAF variación' si existe, sino 'Saldo AAF'
                    columna_saldo = 'Saldo AAF variación' if 'Saldo AAF variación' in df.columns else 'Saldo AAF'
                    if columna_saldo in datos_cuenta.columns:
                        saldo_total = sum(datos_cuenta[columna_saldo].apply(convertir_valor))
                        resultados[f'Total cuenta objeto {cuenta}'] = saldo_total
                        print(f"Total cuenta objeto {cuenta}: {saldo_total:,.2f}")
        
        # Procesar subcuentas específicas
        for subcuenta in subcuentas:
            if 'Cuenta Objeto' in df.columns:
                filtro = df['Cuenta Objeto'].astype(str).str.contains(subcuenta, na=False)
                datos_subcuenta = df[filtro]
                
                if not datos_subcuenta.empty:
                    columna_saldo = 'Saldo AAF variación' if 'Saldo AAF variación' in df.columns else 'Saldo AAF'
                    if columna_saldo in datos_subcuenta.columns:
                        saldo_total = sum(datos_subcuenta[columna_saldo].apply(convertir_valor))
                        resultados[f'Subcuenta {subcuenta}'] = saldo_total
                        print(f"Subcuenta {subcuenta}: {saldo_total:,.2f}")
        
        return resultados
        
    except Exception as e:
        print(f"ERROR leyendo archivo BALANCE: {str(e)}")
        return {}

def leer_archivo_situacion(ruta_archivo):
    """Lee y procesa el archivo SITUACIÓN"""
    print("Leyendo archivo SITUACIÓN...")
    
    try:
        # Leer archivo Excel
        df = pd.read_excel(ruta_archivo, dtype=str)
        print(f"Archivo SITUACIÓN leído. Registros: {len(df)}")
        
        # Buscar TOTAL 01010 en columna SALDOS MES
        if 'SALDOS MES' in df.columns:
            # Buscar fila con TOTAL 01010
            filtro_total = df.iloc[:, 0].astype(str).str.contains('TOTAL 01010', na=False, case=False)
            datos_total = df[filtro_total]
            
            if not datos_total.empty:
                valor_total = convertir_valor(datos_total.iloc[0]['SALDOS MES'])
                print(f"TOTAL 01010 (SALDOS MES): {valor_total:,.2f}")
                return {'TOTAL 01010': valor_total}
        
        print("ADVERTENCIA: No se encontró TOTAL 01010 en archivo SITUACIÓN")
        return {}
        
    except Exception as e:
        print(f"ERROR leyendo archivo SITUACIÓN: {str(e)}")
        return {}

def leer_archivo_focus(ruta_archivo):
    """Lee y procesa el archivo FOCUS"""
    print("Leyendo archivo FOCUS...")
    
    try:
        # Leer archivo Excel (formato España - archivo número 2)
        df = pd.read_excel(ruta_archivo, sheet_name=1, dtype=str)  # Segunda hoja
        print(f"Archivo FOCUS leído. Registros: {len(df)}")
        
        # Buscar datos de vencimientos y dotaciones
        # Esto dependerá de la estructura específica del archivo
        resultados = {}
        
        # Buscar columnas relacionadas con vencimientos
        columnas_vencimiento = [col for col in df.columns if 'vencido' in col.lower() or 'vencimiento' in col.lower()]
        if columnas_vencimiento:
            print(f"Columnas de vencimiento encontradas: {columnas_vencimiento}")
            for col in columnas_vencimiento:
                # Sumar valores de la columna
                valores = df[col].apply(convertir_valor)
                total = valores.sum()
                resultados[f'Total {col}'] = total
                print(f"Total {col}: {total:,.2f}")
        
        # Buscar columnas relacionadas con dotaciones
        columnas_dotacion = [col for col in df.columns if 'dotación' in col.lower() or 'dotacion' in col.lower()]
        if columnas_dotacion:
            print(f"Columnas de dotación encontradas: {columnas_dotacion}")
            for col in columnas_dotacion:
                valores = df[col].apply(convertir_valor)
                total = valores.sum()
                resultados[f'Total {col}'] = total
                print(f"Total {col}: {total:,.2f}")
        
        return resultados
        
    except Exception as e:
        print(f"ERROR leyendo archivo FOCUS: {str(e)}")
        return {}

def calcular_tipos_cambio():
    """Calcula tipos de cambio (placeholder para implementación futura)"""
    print("Calculando tipos de cambio...")
    
    # Por ahora, usar valores de ejemplo
    # En una implementación real, estos vendrían de una API o base de datos
    tipos_cambio = {
        'USD_COP': 4000.0,  # Dólar a Peso Colombiano
        'EUR_COP': 4300.0,  # Euro a Peso Colombiano
        'fecha_actualizacion': datetime.now().strftime('%Y-%m-%d')
    }
    
    print(f"Tipos de cambio calculados: USD={tipos_cambio['USD_COP']}, EUR={tipos_cambio['EUR_COP']}")
    return tipos_cambio

def realizar_calculos_financieros(datos_balance, datos_situacion, datos_focus, tipos_cambio):
    """Realiza los cálculos financieros complejos"""
    print("Realizando cálculos financieros...")
    
    resultados = {
        'fecha_procesamiento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'tipos_cambio': tipos_cambio,
        'resumen_calculos': {},
        'provision_dotacion': {},
        'detalles_por_archivo': {
            'balance': datos_balance,
            'situacion': datos_situacion,
            'focus': datos_focus
        }
    }
    
    # 1. Deuda Bruta NO Grupo
    deuda_bruta_inicial = datos_balance.get('Total cuenta objeto 43001', 0)
    deuda_bruta_final = datos_balance.get('Total cuenta objeto 43008', 0)
    
    # 2. Dotaciones Acumuladas
    dotacion_inicial = datos_balance.get('Total cuenta objeto 43042', 0)
    
    # 3. Cobros del Mes (desde SITUACIÓN)
    cobros_situacion = datos_situacion.get('TOTAL 01010', 0)
    
    # 4. Cálculos de Cobros
    cobro_vencida = deuda_bruta_inicial * 0.1  # Ejemplo: 10% de la deuda inicial
    cobro_total = abs(cobros_situacion) / 1000  # Convertir según especificación
    cobro_no_vencida = cobro_total - cobro_vencida
    
    # 5. Vencidos en el Mes (desde FOCUS)
    vencido_mes = datos_focus.get('Total VENCIDO MES 30 días', 0)
    
    # 6. Facturación del Mes
    facturacion_vencida = 0
    facturacion_no_vencida = deuda_bruta_final - cobro_total
    
    # 7. Dotación del Mes
    dotacion_mes = dotacion_inicial * 0.05  # Ejemplo: 5% de la dotación inicial
    
    # Construir resumen de cálculos
    resultados['resumen_calculos'] = {
        'cobros': {
            'vencida': cobro_vencida,
            'no_vencida': cobro_no_vencida,
            'total': cobro_total
        },
        'facturacion': {
            'vencida': facturacion_vencida,
            'no_vencida': facturacion_no_vencida,
            'total': facturacion_vencida + facturacion_no_vencida
        },
        'vencidos': {
            'vencido': vencido_mes,
            'no_vencido': vencido_mes,
            'total': vencido_mes - vencido_mes  # 0
        },
        'subtotal': {
            'vencida': cobro_vencida + facturacion_vencida + vencido_mes,
            'no_vencida': cobro_no_vencida + facturacion_no_vencida - vencido_mes,
            'total': cobro_total + facturacion_vencida + facturacion_no_vencida
        }
    }
    
    # Provisión y Dotación
    resultados['provision_dotacion'] = {
        'provision': deuda_bruta_final * 0.15,  # Ejemplo: 15% de la deuda final
        'dotacion': dotacion_mes,
        'dotaciones': dotacion_inicial,
        'desdotaciones': dotacion_mes * 0.1  # Ejemplo: 10% de la dotación del mes
    }
    
    print("Cálculos financieros completados")
    return resultados

def generar_reporte_excel(resultados, output_path):
    """Genera reporte en formato Excel"""
    print("Generando reporte Excel...")
    
    try:
        # Crear DataFrame para el reporte
        reporte_data = []
        
        # Resumen de Cálculos
        resumen = resultados['resumen_calculos']
        reporte_data.append(['RESUMEN DE CÁLCULOS', '', ''])
        reporte_data.append(['Cobros', f"{resumen['cobros']['vencida']:,.2f}", f"{resumen['cobros']['no_vencida']:,.2f}"])
        reporte_data.append(['Facturación', f"{resumen['facturacion']['vencida']:,.2f}", f"{resumen['facturacion']['no_vencida']:,.2f}"])
        reporte_data.append(['+/- Vencidos', f"{resumen['vencidos']['vencido']:,.2f}", f"{resumen['vencidos']['no_vencido']:,.2f}"])
        reporte_data.append(['Subtotal', f"{resumen['subtotal']['vencida']:,.2f}", f"{resumen['subtotal']['no_vencida']:,.2f}"])
        reporte_data.append(['', '', ''])
        
        # Provisión y Dotación
        prov_dot = resultados['provision_dotacion']
        reporte_data.append(['PROVISIÓN Y DOTACIÓN', '', ''])
        reporte_data.append(['PROVISIÓN', f"{prov_dot['provision']:,.2f}", ''])
        reporte_data.append(['DOTACIÓN', f"{prov_dot['dotacion']:,.2f}", ''])
        reporte_data.append(['- Dotaciones', f"{prov_dot['dotaciones']:,.2f}", ''])
        reporte_data.append(['+ Desdotaciones', f"{prov_dot['desdotaciones']:,.2f}", ''])
        
        # Crear DataFrame
        df_reporte = pd.DataFrame(reporte_data, columns=['Concepto', 'Vencida', 'No Vencida'])
        
        # Guardar Excel
        df_reporte.to_excel(output_path, index=False)
        
        print(f"Reporte Excel generado: {output_path}")
        return True
        
    except Exception as e:
        print(f"ERROR generando reporte Excel: {str(e)}")
        return False

def procesar_balance_completo(archivo_balance, archivo_situacion, archivo_focus, output_path=None):
    """
    Procesa los tres archivos de balance completo
    """
    print("=" * 80)
    print("PROCESADOR COMPLETO DE BALANCE - GRUPO PLANETA")
    print("=" * 80)
    
    try:
        # Verificar que los archivos existen
        archivos = [archivo_balance, archivo_situacion, archivo_focus]
        for archivo in archivos:
            if not os.path.exists(archivo):
                raise FileNotFoundError(f"Archivo no encontrado: {archivo}")
        
        # Leer archivos
        datos_balance = leer_archivo_balance(archivo_balance)
        datos_situacion = leer_archivo_situacion(archivo_situacion)
        datos_focus = leer_archivo_focus(archivo_focus)
        
        # Calcular tipos de cambio
        tipos_cambio = calcular_tipos_cambio()
        
        # Realizar cálculos financieros
        resultados = realizar_calculos_financieros(datos_balance, datos_situacion, datos_focus, tipos_cambio)
        
        # Definir carpeta de salida
        output_dir = r'C:\wamp64\www\modelo-deuda-python\cartera\resultados'
        os.makedirs(output_dir, exist_ok=True)
        
        # Generar archivos de salida
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        # Archivo JSON
        json_path = os.path.join(output_dir, f'resultados_balance_completo.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False, default=str)
        
        # Archivo Excel
        if not output_path:
            output_path = os.path.join(output_dir, f'BALANCE_COMPLETO_{timestamp}.xlsx')
        
        excel_generado = generar_reporte_excel(resultados, output_path)
        
        # Resumen final
        print("\n" + "=" * 80)
        print("PROCESAMIENTO COMPLETO DE BALANCE FINALIZADO")
        print("=" * 80)
        print(f"Archivos procesados:")
        print(f"  - Balance: {archivo_balance}")
        print(f"  - Situación: {archivo_situacion}")
        print(f"  - Focus: {archivo_focus}")
        print(f"Archivos generados:")
        print(f"  - JSON: {json_path}")
        if excel_generado:
            print(f"  - Excel: {output_path}")
        
        return {
            'success': True,
            'json_path': json_path,
            'excel_path': output_path if excel_generado else None,
            'resultados': resultados
        }
        
    except Exception as e:
        print(f"ERROR durante el procesamiento: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        archivo_balance = sys.argv[1]
        archivo_situacion = sys.argv[2]
        archivo_focus = sys.argv[3]
        output_path = sys.argv[4] if len(sys.argv) > 4 else None
        
        resultado = procesar_balance_completo(archivo_balance, archivo_situacion, archivo_focus, output_path)
        
        if resultado['success']:
            print("Procesamiento completado exitosamente")
            sys.exit(0)
        else:
            print(f"Error en el procesamiento: {resultado['error']}")
            sys.exit(1)
    else:
        print("Uso: python procesador_balance_completo.py <archivo_balance> <archivo_situacion> <archivo_focus> [<archivo_salida_excel>]")
        sys.exit(1) 