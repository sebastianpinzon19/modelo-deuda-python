#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplificado para ejecutar el Modelo de Deuda
"""

import os
import sys
import subprocess
from pathlib import Path

def mostrar_banner():
    """Muestra el banner del sistema"""
    print("=" * 60)
    print("           MODELO DE DEUDA - SISTEMA PYTHON")
    print("=" * 60)
    print()

def verificar_archivos():
    """Verifica que existan los archivos necesarios"""
    archivos_requeridos = [
        "modelo_deuda.py",
        "trm_config.py",
        "utilidades.py"
    ]
    
    faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
    
    if faltantes:
        print("❌ ERROR: Faltan los siguientes archivos:")
        for archivo in faltantes:
            print(f"   - {archivo}")
        return False
    
    print("✅ Archivos del sistema verificados")
    return True

def verificar_dependencias():
    """Verifica que estén instaladas las dependencias de Python"""
    try:
        import pandas
        import xlsxwriter
        import openpyxl
        print("✅ Dependencias de Python verificadas")
        return True
    except ImportError as e:
        print(f"❌ ERROR: Falta dependencia: {e}")
        print("Ejecute: pip install pandas xlsxwriter openpyxl")
        return False

def solicitar_archivo_cartera():
    """Solicita la ruta del archivo de cartera"""
    while True:
        print("\n📁 ARCHIVO DE CARTERA (PROVISIÓN)")
        print("Debe ser un archivo Excel (.xlsx) ya procesado")
        print("Ejemplo: PROVCA_PROCESADO.xlsx")
        
        ruta = input("Ruta del archivo: ").strip().strip('"')
        
        if not ruta:
            print("❌ La ruta no puede estar vacía")
            continue
            
        if not os.path.exists(ruta):
            print(f"❌ El archivo '{ruta}' no existe")
            continue
            
        if not ruta.lower().endswith('.xlsx'):
            print("❌ El archivo debe ser Excel (.xlsx)")
            continue
            
        print(f"✅ Archivo encontrado: {os.path.basename(ruta)}")
        return ruta

def solicitar_archivo_anticipos():
    """Solicita la ruta del archivo de anticipos"""
    while True:
        print("\n💰 ARCHIVO DE ANTICIPOS")
        print("Debe ser un archivo Excel (.xlsx) ya procesado")
        print("Ejemplo: ANTICIPO_PROCESADO.xlsx")
        
        ruta = input("Ruta del archivo: ").strip().strip('"')
        
        if not ruta:
            print("❌ La ruta no puede estar vacía")
            continue
            
        if not os.path.exists(ruta):
            print(f"❌ El archivo '{ruta}' no existe")
            continue
            
        if not ruta.lower().endswith('.xlsx'):
            print("❌ El archivo debe ser Excel (.xlsx)")
            continue
            
        print(f"✅ Archivo encontrado: {os.path.basename(ruta)}")
        return ruta

def solicitar_trm():
    """Solicita las tasas de cambio TRM"""
    print("\n💱 TASAS DE CAMBIO (TRM)")
    print("Ingrese las tasas del último día del mes anterior")
    print("Use punto como separador decimal (ejemplo: 4000.50)")
    
    while True:
        try:
            trm_dolar = input("TRM Dólar (USD/COP): ").strip().replace(',', '.')
            if not trm_dolar:
                print("❌ La TRM Dólar es obligatoria")
                continue
            trm_dolar = float(trm_dolar)
            if trm_dolar <= 0:
                print("❌ La TRM debe ser mayor a 0")
                continue
            break
        except ValueError:
            print("❌ Ingrese un número válido")
    
    while True:
        try:
            trm_euro = input("TRM Euro (EUR/COP): ").strip().replace(',', '.')
            if not trm_euro:
                print("❌ La TRM Euro es obligatoria")
                continue
            trm_euro = float(trm_euro)
            if trm_euro <= 0:
                print("❌ La TRM debe ser mayor a 0")
                continue
            break
        except ValueError:
            print("❌ Ingrese un número válido")
    
    print(f"✅ TRM configuradas - Dólar: {trm_dolar:,.2f}, Euro: {trm_euro:,.2f}")
    return trm_dolar, trm_euro

def ejecutar_modelo_deuda(cartera_file, anticipos_file, trm_dolar, trm_euro):
    """Ejecuta el modelo de deuda"""
    print("\n🚀 EJECUTANDO MODELO DE DEUDA...")
    print("=" * 50)
    
    try:
        # Construir comando
        comando = [
            sys.executable, "modelo_deuda.py",
            cartera_file,
            anticipos_file,
            str(trm_dolar),
            str(trm_euro)
        ]
        
        print(f"Comando: {' '.join(comando)}")
        print()
        
        # Ejecutar
        resultado = subprocess.run(comando, capture_output=True, text=True, encoding='utf-8')
        
        if resultado.returncode == 0:
            print("✅ MODELO DE DEUDA EJECUTADO EXITOSAMENTE")
            print()
            print("📊 RESULTADO:")
            print(resultado.stdout)
            
            # Buscar archivo generado
            output_dir = "PROVCA_PROCESADOS"
            if os.path.exists(output_dir):
                archivos = [f for f in os.listdir(output_dir) if f.startswith("1_Modelo_Deuda_")]
                if archivos:
                    archivo_generado = os.path.join(output_dir, archivos[-1])
                    print(f"\n📁 Archivo generado: {archivo_generado}")
                else:
                    print("\n⚠️ No se encontró archivo de salida")
            else:
                print(f"\n⚠️ Carpeta de salida no encontrada: {output_dir}")
                
        else:
            print("❌ ERROR EN LA EJECUCIÓN")
            print("STDOUT:")
            print(resultado.stdout)
            print("STDERR:")
            print(resultado.stderr)
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    """Función principal"""
    mostrar_banner()
    
    # Verificar sistema
    if not verificar_archivos():
        input("\nPresione Enter para salir...")
        return
    
    if not verificar_dependencias():
        input("\nPresione Enter para salir...")
        return
    
    print("\n🎯 SISTEMA LISTO PARA PROCESAR")
    print("=" * 50)
    
    try:
        # Solicitar archivos y TRM
        cartera_file = solicitar_archivo_cartera()
        anticipos_file = solicitar_archivo_anticipos()
        trm_dolar, trm_euro = solicitar_trm()
        
        # Confirmar ejecución
        print("\n" + "=" * 50)
        print("📋 RESUMEN DE CONFIGURACIÓN:")
        print(f"   Cartera: {os.path.basename(cartera_file)}")
        print(f"   Anticipos: {os.path.basename(anticipos_file)}")
        print(f"   TRM Dólar: {trm_dolar:,.2f}")
        print(f"   TRM Euro: {trm_euro:,.2f}")
        print("=" * 50)
        
        confirmar = input("\n¿Ejecutar el modelo de deuda? (S/N): ").strip().upper()
        if confirmar == 'S':
            ejecutar_modelo_deuda(cartera_file, anticipos_file, trm_dolar, trm_euro)
        else:
            print("\n❌ Ejecución cancelada por el usuario")
            
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
    
    input("\nPresione Enter para salir...")

if __name__ == "__main__":
    main()
