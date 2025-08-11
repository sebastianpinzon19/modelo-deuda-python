import os
import sys
import subprocess
from datetime import datetime

def validar_fecha(fecha_str):
    """Valida que la fecha tenga el formato correcto (YYYY-MM-DD)"""
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        return fecha
    except ValueError:
        return None

def solicitar_fecha_cierre():
    """Solicita al usuario la fecha de cierre"""
    while True:
        print("\n=== FECHA DE CIERRE ===")
        print("La fecha de cierre es la fecha hasta la cual se procesarán los datos.")
        print("Formato requerido: YYYY-MM-DD (ejemplo: 2024-12-31)")
        
        fecha_str = input("Ingrese la fecha de cierre: ").strip()
        
        if fecha_str.lower() == 'salir':
            return None
            
        fecha = validar_fecha(fecha_str)
        if fecha:
            print(f"Fecha de cierre confirmada: {fecha.strftime('%d/%m/%Y')}")
            return fecha_str
        else:
            print("❌ Formato de fecha incorrecto. Use YYYY-MM-DD (ejemplo: 2024-12-31)")
            print("O escriba 'salir' para cancelar.")

def menu():
    print("\n=== Procesador de Archivos ===")
    print("1. Procesar Cartera (CSV)")
    print("2. Procesar Anticipos (Excel)")
    print("0. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion.strip()

def procesar_cartera():
    # Solicitar fecha de cierre
    fecha_cierre = solicitar_fecha_cierre()
    if fecha_cierre is None:
        print("Operación cancelada.")
        return
        
    archivo = input("Ingrese la ruta del archivo CSV de cartera: ").strip()
    if not os.path.isfile(archivo):
        print(f"El archivo '{archivo}' no existe.")
        return
    comando = [sys.executable, "procesador_cartera.py", archivo, fecha_cierre]
    print(f"Ejecutando: {' '.join(comando)}")
    subprocess.run(comando)

def procesar_anticipos():
    archivo = input("Ingrese la ruta del archivo Excel de anticipos: ").strip()
    if not os.path.isfile(archivo):
        print(f"El archivo '{archivo}' no existe.")
        return
    comando = [sys.executable, "procesador_anticipos.py", archivo]
    print(f"Ejecutando: {' '.join(comando)}")
    subprocess.run(comando)

if __name__ == "__main__":
    while True:
        op = menu()
        if op == "1":
            procesar_cartera()
        elif op == "2":
            procesar_anticipos()
        elif op == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.") 