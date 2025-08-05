# -*- coding: utf-8 -*-
"""
PRUEBAS SIMPLES - SISTEMA FORMATO DEUDA
GRUPO PLANETA

Script de pruebas básicas para verificar el funcionamiento del sistema
"""

import os
import sys
import pandas as pd
from datetime import datetime

def imprimir_seccion(titulo):
    """Imprime una sección de prueba"""
    print(f"\n{'='*60}")
    print(f"PRUEBA: {titulo}")
    print(f"{'='*60}")

def imprimir_resultado(prueba, resultado, detalles=""):
    """Imprime el resultado de una prueba"""
    estado = "✅ PASÓ" if resultado else "❌ FALLÓ"
    print(f"{estado} - {prueba}")
    if detalles:
        print(f"   Detalles: {detalles}")

def prueba_estructura_archivos():
    """Prueba que todos los archivos necesarios existan"""
    imprimir_seccion("ESTRUCTURA DE ARCHIVOS")
    
    archivos_requeridos = [
        "utilidades_cartera.py",
        "procesador_cartera.py", 
        "procesador_anticipos.py",
        "procesador_formato_deuda.py",
        "procesador_balance_completo.py",
        "requirements.txt"
    ]
    
    todos_existen = True
    for archivo in archivos_requeridos:
        existe = os.path.exists(archivo)
        imprimir_resultado(f"archivo {archivo}", existe)
        if not existe:
            todos_existen = False
    
    return todos_existen

def prueba_importaciones():
    """Prueba que se puedan importar los módulos principales"""
    imprimir_seccion("IMPORTACIONES DE MÓDULOS")
    
    try:
        import utilidades_cartera
        imprimir_resultado("import utilidades_cartera", True)
    except Exception as e:
        imprimir_resultado("import utilidades_cartera", False, str(e))
        return False
    
    try:
        import procesador_cartera
        imprimir_resultado("import procesador_cartera", True)
    except Exception as e:
        imprimir_resultado("import procesador_cartera", False, str(e))
        return False
    
    try:
        import procesador_anticipos
        imprimir_resultado("import procesador_anticipos", True)
    except Exception as e:
        imprimir_resultado("import procesador_anticipos", False, str(e))
        return False
    
    try:
        import procesador_formato_deuda
        imprimir_resultado("import procesador_formato_deuda", True)
    except Exception as e:
        imprimir_resultado("import procesador_formato_deuda", False, str(e))
        return False
    
    return True

def prueba_funciones_utilidades():
    """Prueba las funciones básicas de utilidades"""
    imprimir_seccion("FUNCIONES DE UTILIDADES")
    
    try:
        from utilidades_cartera import convertir_valor, formatear_numero_colombiano
        
        # Prueba convertir_valor
        valor1 = convertir_valor("1000000")
        valor2 = convertir_valor("1.000.000,50")
        imprimir_resultado("convertir_valor", isinstance(valor1, (int, float)) and isinstance(valor2, (int, float)))
        
        # Prueba formatear_numero_colombiano
        formato1 = formatear_numero_colombiano(1000000.50)
        formato2 = formatear_numero_colombiano(0.15, es_porcentaje=True)
        imprimir_resultado("formatear_numero_colombiano", isinstance(formato1, str) and isinstance(formato2, str))
        
        return True
        
    except Exception as e:
        imprimir_resultado("funciones_utilidades", False, str(e))
        return False

def prueba_creacion_dataframe():
    """Prueba la creación y manipulación de DataFrames"""
    imprimir_seccion("MANIPULACIÓN DE DATAFRAMES")
    
    try:
        # Crear DataFrame de prueba
        df = pd.DataFrame({
            'EMPRESA': ['CT80', 'PL41', 'CT80'],
            'CLIENTE': ['001', '002', '003'],
            'SALDO': [1000000, 2500000, 500000],
            'FECHA': ['2025-01-15', '2025-01-20', '2025-01-25']
        })
        
        imprimir_resultado("crear_dataframe", len(df) == 3)
        
        # Prueba filtrado
        df_filtrado = df[df['EMPRESA'] == 'CT80']
        imprimir_resultado("filtrar_dataframe", len(df_filtrado) == 2)
        
        # Prueba agrupación
        df_agrupado = df.groupby('EMPRESA')['SALDO'].sum()
        imprimir_resultado("agrupar_dataframe", len(df_agrupado) == 2)
        
        return True
        
    except Exception as e:
        imprimir_resultado("manipulacion_dataframe", False, str(e))
        return False

def prueba_lectura_csv():
    """Prueba la lectura de archivos CSV"""
    imprimir_seccion("LECTURA DE ARCHIVOS CSV")
    
    try:
        # Verificar que existan los archivos de prueba
        archivo_provision = "datos_prueba_provision.csv"
        archivo_anticipos = "datos_prueba_anticipos.csv"
        
        if not os.path.exists(archivo_provision):
            imprimir_resultado("archivo_provision_existe", False, "Archivo no encontrado")
            return False
        
        if not os.path.exists(archivo_anticipos):
            imprimir_resultado("archivo_anticipos_existe", False, "Archivo no encontrado")
            return False
        
        # Leer archivos
        df_provision = pd.read_csv(archivo_provision)
        df_anticipos = pd.read_csv(archivo_anticipos)
        
        imprimir_resultado("leer_provision", len(df_provision) > 0)
        imprimir_resultado("leer_anticipos", len(df_anticipos) > 0)
        
        print(f"   Provisión: {len(df_provision)} registros, {len(df_provision.columns)} columnas")
        print(f"   Anticipos: {len(df_anticipos)} registros, {len(df_anticipos.columns)} columnas")
        
        return True
        
    except Exception as e:
        imprimir_resultado("lectura_csv", False, str(e))
        return False

def prueba_dependencias():
    """Prueba que las dependencias estén instaladas"""
    imprimir_seccion("DEPENDENCIAS DE PYTHON")
    
    try:
        import pandas
        imprimir_resultado("pandas", True, f"Versión: {pandas.__version__}")
    except ImportError:
        imprimir_resultado("pandas", False, "No instalado")
        return False
    
    try:
        import numpy
        imprimir_resultado("numpy", True, f"Versión: {numpy.__version__}")
    except ImportError:
        imprimir_resultado("numpy", False, "No instalado")
        return False
    
    try:
        import openpyxl
        imprimir_resultado("openpyxl", True)
    except ImportError:
        imprimir_resultado("openpyxl", False, "No instalado")
        return False
    
    return True

def main():
    """Función principal de pruebas"""
    print("PRUEBAS SIMPLES - SISTEMA FORMATO DEUDA")
    print("GRUPO PLANETA")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ejecutar pruebas
    resultados = []
    
    resultados.append(("Estructura de archivos", prueba_estructura_archivos()))
    resultados.append(("Dependencias", prueba_dependencias()))
    resultados.append(("Importaciones", prueba_importaciones()))
    resultados.append(("Funciones utilidades", prueba_funciones_utilidades()))
    resultados.append(("DataFrames", prueba_creacion_dataframe()))
    resultados.append(("Lectura CSV", prueba_lectura_csv()))
    
    # Resumen
    imprimir_seccion("RESUMEN")
    
    total = len(resultados)
    exitosas = sum(1 for _, resultado in resultados if resultado)
    
    print(f"Total de pruebas: {total}")
    print(f"Pruebas exitosas: {exitosas}")
    print(f"Pruebas fallidas: {total - exitosas}")
    print(f"Porcentaje de éxito: {(exitosas/total)*100:.1f}%")
    
    if exitosas == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ El sistema está listo para funcionar")
    else:
        print("\n⚠️  ALGUNAS PRUEBAS FALLARON")
        print("❌ Revisar los errores indicados")
    
    return exitosas == total

if __name__ == "__main__":
    exit(0 if main() else 1) 