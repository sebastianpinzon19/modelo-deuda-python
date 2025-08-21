import pandas as pd
import numpy as np

def generar_formato_deuda(cartera_path, anticipos_path, negocio_canal_path=None):
    """
    Genera el formato de deuda consolidando los archivos de cartera y anticipos.

    Args:
        cartera_path (str): Ruta al archivo CSV de cartera.
        anticipos_path (str): Ruta al archivo CSV de anticipos.
        negocio_canal_path (str): (Opcional) Ruta al archivo CSV o Excel con la tabla de Negocio y Canal.
    
    Returns:
        pd.DataFrame: DataFrame consolidado con el formato de deuda.
    """
    # Cargar los archivos de cartera y anticipos
    df_cartera = pd.read_csv(cartera_path, encoding='latin1', delimiter=',')
    df_anticipos = pd.read_csv(anticipos_path, encoding='latin1', delimiter=',')

    # Renombrar columnas para la unificación
    df_cartera = df_cartera.rename(columns={
        'CODIGO CLIENTE': 'CLIENTE',
        'SALDO': 'SALDO TOTAL',
        'SALDO NO VENCIDO': 'Saldo No vencido',
        'VENCIDO 30': 'Vencido 30',
        'VENCIDO 60': 'Vencido 60',
        'VENCIDO 90': 'Vencido 90',
        'VENCIDO 180': 'Vencido 180',
        'VENCIDO 360': 'Vencido 360',
        'VENCIDO + 360': 'Vencido + 360',
        'DEUDA INCOBRABLE': 'DEUDA INCOBRABLE'
    })
    
    df_anticipos = df_anticipos.rename(columns={
        'CODIGO CLIENTE': 'CLIENTE',
        'SALDO': 'SALDO TOTAL',
        'SALDO NO VENCIDO': 'Saldo No vencido',
        'VENCIDO 30': 'Vencido 30',
        'VENCIDO 60': 'Vencido 60',
        'VENCIDO 90': 'Vencido 90',
        'VENCIDO 180': 'Vencido 180',
        'VENCIDO 360': 'Vencido 360',
        'VENCIDO + 360': 'Vencido + 360',
        'DEUDA INCOBRABLE': 'DEUDA INCOBRABLE'
    })

    # Asegurarse de que las columnas numéricas estén en el tipo correcto
    cols_numericas = ['SALDO TOTAL', 'Saldo No vencido', 'Vencido 30', 'Vencido 60', 
                       'Vencido 90', 'Vencido 180', 'Vencido 360', 'Vencido + 360', 
                       'DEUDA INCOBRABLE']
    
    for col in cols_numericas:
        if col in df_cartera.columns:
            df_cartera[col] = pd.to_numeric(df_cartera[col].astype(str).str.replace(',', '', regex=False).str.strip(), errors='coerce').fillna(0)
        if col in df_anticipos.columns:
            df_anticipos[col] = pd.to_numeric(df_anticipos[col].astype(str).str.replace(',', '', regex=False).str.strip(), errors='coerce').fillna(0)

    # Combinar los dataframes de cartera y anticipos
    df_consolidado = pd.concat([df_cartera, df_anticipos], ignore_index=True)

    # Llenar valores faltantes en 'CLIENTE' con la columna 'CODIGO CLIENTE'
    if 'CLIENTE' not in df_consolidado.columns and 'CODIGO CLIENTE' in df_consolidado.columns:
        df_consolidado['CLIENTE'] = df_consolidado['CODIGO CLIENTE']

    # Unificar valores nulos en columnas importantes
    df_consolidado['NOMBRE'] = df_consolidado['NOMBRE'].fillna('')
    df_consolidado['DENOMINACION COMERCIAL'] = df_consolidado['DENOMINACION COMERCIAL'].fillna('')
    df_consolidado['MONEDA'] = df_consolidado['MONEDA'].fillna('PESOS COL')
    df_consolidado['NEGOCIO'] = df_consolidado['ACTIVIDAD'].fillna('')
    df_consolidado['CANAL'] = df_consolidado['EMPRESA'].fillna('')

    # Mapear los nombres de negocio y canal a partir del documento
    # Si se tiene una tabla de mapeo, se usa, de lo contrario se mantienen los valores.
    # El código no tiene acceso a los valores de la tabla en el documento, por lo que se asume el mapeo por defecto.
    
    # Agregar las columnas requeridas por el formato de deuda
    df_consolidado['País'] = 'Colombia'
    df_consolidado['COBRO/PAGO'] = 'CLIENTE'
    df_consolidado['CLIENTE'] = df_consolidado['NOMBRE'] + ' (' + df_consolidado['DENOMINACION COMERCIAL'] + ')'
    df_consolidado['CLIENTE'] = df_consolidado['CLIENTE'].str.replace('()', '', regex=False).str.strip()

    # Agrupar por las columnas clave y sumar los saldos
    df_agrupado = df_consolidado.groupby(['País', 'NEGOCIO', 'CANAL', 'COBRO/PAGO', 'MONEDA', 'CLIENTE']).agg(
        **{col: ('SALDO TOTAL' if col == 'SALDO TOTAL' else col, 'sum') for col in cols_numericas}
    ).reset_index()

    # Redondear los valores numéricos
    for col in cols_numericas:
        df_agrupado[col] = np.round(df_agrupado[col], 2)
        
    return df_agrupado

# --- Ejecución del script ---
if __name__ == "__main__":
    cartera_file = "PROVCA_PROCESADO_20250821_090656.xlsx - Cartera.csv"
    anticipos_file = "ANTICIPO_PROCESADO_2025-08-21_08-46-18.xlsx - Anticipos.csv"
    
    try:
        df_final = generar_formato_deuda(cartera_file, anticipos_file)
        
        # Guardar el DataFrame final en un archivo Excel
        output_file = 'FormatoDeuda_Consolidado.xlsx'
        df_final.to_excel(output_file, index=False, engine='openpyxl')
        
        print(f"✅ Archivo '{output_file}' generado con éxito.")
        print("El archivo contiene la siguiente información consolidada:")
        print(df_final.head())
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}. Asegúrate de que los archivos estén en la misma carpeta que el script.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")