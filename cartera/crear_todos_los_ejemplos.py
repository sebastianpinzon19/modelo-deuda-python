#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Principal para Crear Todos los Ejemplos de Cartera
Este script ejecuta todos los ejemplos para generar múltiples archivos de prueba
con diferentes escenarios de cartera y anticipos.
"""

import os
import subprocess
import sys

def ejecutar_ejemplo(numero_ejemplo):
    """Ejecuta un ejemplo específico"""
    script = f"ejemplo_{numero_ejemplo}_cartera"
    
    if numero_ejemplo == 1:
        script = "ejemplo_1_cartera_completa"
    elif numero_ejemplo == 2:
        script = "ejemplo_2_cartera_vencida"
    elif numero_ejemplo == 3:
        script = "ejemplo_3_cartera_por_vencer"
    
    script_path = f"{script}.py"
    
    if os.path.exists(script_path):
        print(f"\n{'='*60}")
        print(f"EJECUTANDO EJEMPLO {numero_ejemplo}")
        print(f"{'='*60}")
        
        try:
            # Ejecutar el script
            result = subprocess.run([sys.executable, script_path], 
                                  capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print("✅ Ejemplo ejecutado exitosamente")
                print(result.stdout)
            else:
                print("❌ Error ejecutando el ejemplo:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando {script_path}: {e}")
    else:
        print(f"❌ No se encontró el archivo {script_path}")

def mostrar_resumen():
    """Muestra un resumen de todos los archivos creados"""
    carpeta = "PROVCA_PROCESADOS"
    
    if os.path.exists(carpeta):
        print(f"\n{'='*80}")
        print("📁 RESUMEN DE ARCHIVOS CREADOS")
        print(f"{'='*80}")
        
        archivos = os.listdir(carpeta)
        archivos_cartera = [f for f in archivos if f.startswith('CARTERA_EJEMPLO')]
        archivos_anticipos = [f for f in archivos if f.startswith('ANTICIPOS_EJEMPLO')]
        
        print(f"\n📊 Archivos de Cartera ({len(archivos_cartera)}):")
        for archivo in sorted(archivos_cartera):
            ruta_completa = os.path.join(carpeta, archivo)
            tamaño = os.path.getsize(ruta_completa) / 1024  # KB
            print(f"   • {archivo} ({tamaño:.1f} KB)")
        
        print(f"\n💰 Archivos de Anticipos ({len(archivos_anticipos)}):")
        for archivo in sorted(archivos_anticipos):
            ruta_completa = os.path.join(carpeta, archivo)
            tamaño = os.path.getsize(ruta_completa) / 1024  # KB
            print(f"   • {archivo} ({tamaño:.1f} KB)")
        
        print(f"\n🔧 Comandos para procesar con el modelo de deuda:")
        print(f"{'='*80}")
        
        for i in range(1, 4):
            archivo_cartera = f"CARTERA_EJEMPLO_{i}"
            if i == 1:
                archivo_cartera = "CARTERA_EJEMPLO_1"
            elif i == 2:
                archivo_cartera = "CARTERA_EJEMPLO_2_VENCIDA"
            elif i == 3:
                archivo_cartera = "CARTERA_EJEMPLO_3_POR_VENCER"
            
            archivo_anticipos = f"ANTICIPOS_EJEMPLO_{i}"
            
            ruta_cartera = os.path.join(carpeta, f"{archivo_cartera}.xlsx")
            ruta_anticipos = os.path.join(carpeta, f"{archivo_anticipos}.xlsx")
            
            if os.path.exists(ruta_cartera) and os.path.exists(ruta_anticipos):
                print(f"\n📋 Ejemplo {i}:")
                print(f"   python PROVCA/modelo_deuda.py \"{ruta_cartera}\" \"{ruta_anticipos}\" 4000 4500")
        
        print(f"\n{'='*80}")
        print("✅ TODOS LOS EJEMPLOS CREADOS EXITOSAMENTE")
        print("🎯 Ahora puedes probar el modelo de deuda con diferentes escenarios")
        print(f"{'='*80}")

def main():
    """Función principal"""
    print("🚀 INICIANDO CREACIÓN DE TODOS LOS EJEMPLOS")
    print("=" * 80)
    
    # Verificar que existan los scripts
    scripts_requeridos = [
        "ejemplo_1_cartera_completa.py",
        "ejemplo_2_cartera_vencida.py", 
        "ejemplo_3_cartera_por_vencer.py"
    ]
    
    scripts_faltantes = []
    for script in scripts_requeridos:
        if not os.path.exists(script):
            scripts_faltantes.append(script)
    
    if scripts_faltantes:
        print("❌ Faltan los siguientes scripts:")
        for script in scripts_faltantes:
            print(f"   • {script}")
        print("\nPor favor, asegúrate de que todos los scripts estén presentes.")
        return
    
    print("✅ Todos los scripts están presentes")
    
    # Crear carpeta de salida
    carpeta = "PROVCA_PROCESADOS"
    os.makedirs(carpeta, exist_ok=True)
    print(f"📁 Carpeta de salida creada: {carpeta}")
    
    # Ejecutar todos los ejemplos
    for i in range(1, 4):
        ejecutar_ejemplo(i)
    
    # Mostrar resumen
    mostrar_resumen()

if __name__ == "__main__":
    main() 