import os
import json
from datetime import datetime


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'trm_config.json')


def _ensure_dir_exists(path):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def load_trm():
    """Devuelve un dict {'usd': float|None, 'eur': float|None, 'updated_at': str|None}.
    Si no existe, retorna valores en None.
    """
    try:
        if not os.path.exists(CONFIG_PATH):
            return {'usd': None, 'eur': None, 'updated_at': None}
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
        return {'usd': None, 'eur': None, 'updated_at': None}


def save_trm(usd, eur):
    """Guarda TRM en archivo JSON y devuelve la ruta."""
    _ensure_dir_exists(CONFIG_PATH)
    payload = {
        'usd': float(usd) if usd is not None else None,
        'eur': float(eur) if eur is not None else None,
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return CONFIG_PATH


def parse_trm_value(text, fallback=None):
    """Parsea valores de TRM ingresados por el usuario con formato LATAM.
    Reglas:
    - Si tiene '.' y ',' → quitar puntos (miles) y usar coma como decimal
    - Si solo tiene ',' → usar como decimal
    - Si solo tiene '.' → si los grupos después de los puntos son de 3 en 3, tratar como miles
      (ej: "4.780" -> 4780), de lo contrario tratar como decimal
    - Si no tiene separadores → convertir directo
    """
    try:
        if text is None:
            return fallback
        s = str(text).strip().replace('\u200b', '').replace(' ', '')
        if s == '':
            return fallback
        if '.' in s and ',' in s:
            s = s.replace('.', '').replace(',', '.')
            return float(s)
        if ',' in s:
            return float(s.replace(',', '.'))
        if '.' in s:
            parts = s.split('.')
            if len(parts) > 1 and all(p.isdigit() and len(p) == 3 for p in parts[1:]) and parts[0].isdigit():
                # puntos como miles
                return float(''.join(parts))
            return float(s)
        return float(s)
    except Exception:
        return fallback


def format_trm_display(value):
    """Formatea TRM para mostrar con separador de miles y sin decimales: 4780 -> '4.780'."""
    try:
        if value is None:
            return '-'
        return f"{float(value):,.0f}".replace(',', '.')
    except Exception:
        return str(value)

