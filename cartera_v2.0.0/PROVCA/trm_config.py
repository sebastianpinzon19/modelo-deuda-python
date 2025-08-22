import os
import json
from datetime import datetime

# Se establece la ruta del archivo de configuración para que esté en la misma carpeta del script
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'trm_config.json')

def _ensure_config_file_exists():
    """Asegura que el archivo de configuración exista con valores iniciales."""
    if not os.path.exists(CONFIG_PATH):
        payload = {
            'usd': 0.0,
            'eur': 0.0,
            'updated_at': None
        }
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

def load_trm():
    """Devuelve un dict {'usd': float|None, 'eur': float|None, 'updated_at': str|None}.
    Si el archivo no existe o hay un error, retorna un diccionario con valores nulos.
    """
    _ensure_config_file_exists()
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        usd = data.get('usd')
        eur = data.get('eur')
        return {
            'usd': float(usd) if usd is not None else None,
            'eur': float(eur) if eur is not None else None,
            'updated_at': data.get('updated_at')
        }
    except Exception:
        # En caso de error de lectura, se vuelve a crear el archivo
        _ensure_config_file_exists()
        return {'usd': None, 'eur': None, 'updated_at': None}


def save_trm(usd, eur):
    """Guarda los valores de TRM en un archivo JSON."""
    payload = {
        'usd': float(usd) if usd is not None else None,
        'eur': float(eur) if eur is not None else None,
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return CONFIG_PATH


def parse_trm_value(text, fallback=None):
    """Parsea valores de TRM ingresados por el usuario con formato LATAM,
    convirtiéndolos a float.
    """
    try:
        if text is None:
            return fallback
        s = str(text).strip().replace('\u200b', '').replace(' ', '')
        if s == '':
            return fallback

        # Si tiene punto y coma, trata la coma como decimal y el punto como miles.
        if '.' in s and ',' in s:
            s = s.replace('.', '').replace(',', '.')
        # Si solo tiene coma, trata la coma como decimal.
        elif ',' in s:
            s = s.replace(',', '.')
        # Si solo tiene punto, se evalúa si es un separador de miles o un decimal.
        elif '.' in s:
            parts = s.split('.')
            if len(parts) > 1 and all(p.isdigit() and len(p) == 3 for p in parts[1:]) and parts[0].isdigit():
                # Puntos como miles (ej. "4.780" -> 4780)
                s = ''.join(parts)
            # Si no, se asume que el punto es un decimal (ej. "4.5" -> 4.5)

        return float(s)
    except Exception:
        return fallback


def format_trm_display(value):
    """Formatea la TRM para mostrarla con separador de miles.
    Ejemplo: 4780 -> '4.780'
    """
    try:
        if value is None:
            return '-'
        # Convertir a float y luego a string con formato de miles
        formatted_value = f"{float(value):,.0f}"
        # Reemplazar la coma por punto para el formato LATAM
        return formatted_value.replace(',', '.')
    except Exception:
        return str(value)