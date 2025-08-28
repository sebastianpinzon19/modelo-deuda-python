# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
import re

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
            if pd.isna(valor_str):
                return 0.0
            return float(valor_str)
        
        # Limpiar el valor: eliminar espacios, caracteres invisibles y espacios al final
        s = str(valor_str).strip().replace('\u200b', '').replace(' ', '')
        if s == '' or s.lower() == 'nan':
            return 0.0
        
        # Handle accounting format like (123.45) -> -123.45
        s = s.replace('$', '')
        if s.startswith('(') and s.endswith(')'):
            s = '-' + s[1:-1]

        has_dot = '.' in s
        has_comma = ',' in s

        # Case 1: Both dot and comma are present. Determine decimal separator by position.
        if has_dot and has_comma:
            if s.rfind(',') > s.rfind('.'):
                # Format is "1.234,56" (Colombian/Latin)
                s = s.replace('.', '').replace(',', '.')
            else:
                # Format is "1,234.56" (International)
                s = s.replace(',', '')
        
        # Case 2: Only commas are present.
        elif has_comma:
            # If more than one comma, they are thousand separators.
            if s.count(',') > 1:
                s = s.replace(',', '')
            else: # A single comma is a decimal separator.
                s = s.replace(',', '.')
        
        # Case 3: Only dots are present. This is ambiguous.
        elif has_dot and s.count('.') > 1:
            parts = s.split('.')
            # Heuristic: if the last part has 2 digits, it's likely a decimal part.
            if len(parts[-1]) == 2:
                 # e.g., "1.234.56" -> 1234.56
                 s = ''.join(parts[:-1]) + '.' + parts[-1]
            else:
                 # e.g., "1.234.567" -> 1234567
                 s = ''.join(parts)
        
        # Validación final: asegurar que sea un número válido
        resultado = float(s)
        
        # Si el resultado es NaN o infinito, retornar 0
        if pd.isna(resultado) or resultado == float('inf') or resultado == float('-inf'):
            return 0.0
            
        return resultado
    except (ValueError, TypeError) as e:
        print(f"Error convirtiendo valor: {valor_str}, Error: {e}")
        return 0.0

def validar_formato_colombiano(valor_original, valor_formateado):
    """
    Valida que el formato colombiano se aplique correctamente
    """
    try:
        # Ejemplos de formato correcto
        ejemplos = {
            1234567.89: "1.234.567,89",
            1000.00: "1.000,00",
            0.00: "0,00",
            123.45: "123,45"
        }
        
        # Verificar que el valor formateado tenga el formato correcto
        if valor_formateado.count('.') > 0 and valor_formateado.count(',') == 1:
            return True
        else:
            print(f"Formato incorrecto: {valor_original} -> {valor_formateado}")
            return False
    except Exception:
        return False

def formatear_numero_colombiano(valor, es_porcentaje=False):
    """
    Formatea un número en formato colombiano (puntos para miles, comas para decimales)
    Ejemplo: 1234567.89 -> 1.234.567,89
    Si es_porcentaje=True: 0.15 -> 15,00%
    """
    try:
        if valor is None or pd.isna(valor):
            return "-"
        
        # Convertir a float si es string
        if isinstance(valor, str):
            # Limpiar el string de caracteres extraños
            valor_str = str(valor).strip().replace(' ', '').replace('\u200b', '')
            if valor_str == '' or valor_str.lower() == 'nan':
                return "-"
            # Convertir usando la función existente
            valor = convertir_valor(valor_str)
        
        # Si el valor es 0, retornar "-"
        if valor == 0:
            return "-"
        
        # Manejar porcentajes
        if es_porcentaje:
            # Convertir a porcentaje (multiplicar por 100)
            valor_porcentaje = valor * 100
            if valor_porcentaje == int(valor_porcentaje):
                return f"{int(valor_porcentaje)}%"
            else:
                return f"{valor_porcentaje:.2f}%"
        
        # Verificar si es un número entero
        if valor == int(valor):
            # Es entero, no agregar decimales
            valor_str = f"{int(valor)}"
        else:
            # Tiene decimales, usar 2 decimales
            valor_str = f"{valor:.2f}"
        
        # Formato colombiano: agregar puntos para miles y coma para decimales
        # Para números grandes, agregar puntos cada 3 dígitos desde la derecha
        if valor >= 1000:
            # Convertir a string con formato de miles
            valor_str = f"{valor:,.0f}" if valor == int(valor) else f"{valor:,.2f}"
            # Reemplazar comas por puntos para miles
            valor_str = valor_str.replace(',', '.')
            # Reemplazar el punto decimal por coma
            if '.' in valor_str:
                partes = valor_str.split('.')
                if len(partes) > 1:
                    # El último punto es el decimal
                    valor_str = '.'.join(partes[:-1]) + ',' + partes[-1]
        else:
            # Para números pequeños, solo cambiar punto por coma
            valor_str = valor_str.replace('.', ',')
        
        return valor_str
    except Exception as e:
        print(f"Error formateando número: {valor}, Error: {e}")
        return "-"

def aplicar_formato_colombiano_dataframe(df, columnas_numericas=None):
    """
    Aplica formato colombiano a las columnas numéricas de un DataFrame
    """
    if columnas_numericas is None:
        # Detectar columnas numéricas automáticamente
        columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    
    df_formateado = df.copy()
    
    for columna in columnas_numericas:
        if columna in df.columns:
            # Solo aplicar formato si la columna contiene datos numéricos
            if df_formateado[columna].dtype in ['int64', 'float64'] or df_formateado[columna].dtype == 'object':
                try:
                    # Solo convertir si es string, no si ya es numérico
                    if df_formateado[columna].dtype == 'object':
                        df_formateado[columna] = df_formateado[columna].apply(convertir_valor)
                    
                    # Determinar si es columna de porcentaje
                    # NOTA: "Valor Dotación" es un valor, no un porcentaje
                    es_porcentaje = any(palabra in columna.lower() for palabra in [
                        '%', 'porcentaje', 'porcentual'
                    ]) and 'valor dotación' not in columna.lower()
                    
                    # Aplicar formato colombiano
                    df_formateado[columna] = df_formateado[columna].apply(
                        lambda x: formatear_numero_colombiano(x, es_porcentaje)
                    )
                except Exception as e:
                    print(f"Error aplicando formato a columna {columna}: {e}")
                    # Si hay error, mantener la columna original
                    continue
    
    return df_formateado 