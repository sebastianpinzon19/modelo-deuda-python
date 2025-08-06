#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orquestador Principal del Sistema de Procesamiento de Cartera
Grupo Planeta - Sistema de Análisis Financiero
Versión: 2.0.1
"""

import argparse
import sys
import time
from typing import Tuple, Dict, Any, List, Optional
from config import (
    TIPOS_PROCESAMIENTO, CONFIG_PROCESAMIENTO, DIRECTORIOS,
    obtener_timestamp, obtener_fecha_actual
)
from logger import crear_logger, log_funcion
from utilidades_cartera import UtilidadesCartera

# Importar procesadores disponibles
from procesador_cartera import ProcesadorCartera
from procesador_acumulado import ProcesadorAcumulado
from procesador_formato_deuda import ProcesadorFormatoDeuda
from procesador_anticipos import ProcesadorAnticipos

# Procesadores pendientes de refactorización
# from procesador_balance_completo import ProcesadorBalanceCompleto
# from procesador_balance_especifico import ProcesadorBalanceEspecifico
# from procesador_situacion_especifico import ProcesadorSituacionEspecifico
# from procesador_focus_especifico import ProcesadorFocusEspecifico

# =============================================================================
# CLASE PRINCIPAL DEL ORQUESTADOR
# =============================================================================

class OrquestadorPrincipal:
    """
    Clase principal que orquesta todos los procesadores del sistema
    """
    
    def __init__(self):
        """Inicializa el orquestador principal"""
        self.logger = crear_logger("OrquestadorPrincipal")
        self.utilidades = UtilidadesCartera()
        
        # Mapeo de procesadores disponibles
        self.procesadores = {
            'cartera': ProcesadorCartera(),
            'acumulado': ProcesadorAcumulado(),
            'formato_deuda': ProcesadorFormatoDeuda(),
            'anticipos': ProcesadorAnticipos()
        }
        
        # Procesadores pendientes
        self.procesadores_pendientes = [
            'balance_completo',
            'balance_especifico', 
            'situacion_especifico',
            'focus_especifico'
        ]
        
        self.logger.info("Orquestador principal inicializado")
        self.logger.info(f"Procesadores disponibles: {list(self.procesadores.keys())}")
        self.logger.info(f"Procesadores pendientes: {self.procesadores_pendientes}")
    
    @log_funcion
    def procesar_archivo(self, ruta_archivo: str, tipo_procesamiento: str, 
                        opciones: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Procesa un archivo con el procesador especificado
        
        Args:
            ruta_archivo: Ruta del archivo a procesar
            tipo_procesamiento: Tipo de procesamiento a realizar
            opciones: Opciones adicionales para el procesamiento
            
        Returns:
            Tuple[str, Dict]: (ruta_salida, resumen_procesamiento)
            
        Raises:
            ValueError: Si el tipo de procesamiento no es válido
            Exception: Si hay error en el procesamiento
        """
        if opciones is None:
            opciones = {}
        
        # Validar tipo de procesamiento
        if tipo_procesamiento not in self.procesadores:
            tipos_disponibles = list(self.procesadores.keys())
            tipos_pendientes = self.procesadores_pendientes
            raise ValueError(f"Tipo de procesamiento '{tipo_procesamiento}' no válido. "
                           f"Tipos disponibles: {tipos_disponibles}. "
                           f"Tipos pendientes: {tipos_pendientes}")
        
        # Obtener procesador
        procesador = self.procesadores[tipo_procesamiento]
        
        # Validar archivo
        self.utilidades.validar_archivo(ruta_archivo)
        
        # Ejecutar procesamiento
        self.logger.info(f"Iniciando procesamiento: {tipo_procesamiento} - {ruta_archivo}")
        
        try:
            if tipo_procesamiento == 'cartera':
                ruta_salida, resumen = procesador.procesar_cartera(ruta_archivo)
            elif tipo_procesamiento == 'acumulado':
                ruta_salida, resumen = procesador.procesar_acumulado(ruta_archivo)
            elif tipo_procesamiento == 'formato_deuda':
                ruta_salida, resumen = procesador.procesar_formato_deuda(ruta_archivo)
            elif tipo_procesamiento == 'anticipos':
                ruta_salida, resumen = procesador.procesar_anticipos(ruta_archivo)
            else:
                raise ValueError(f"Procesador '{tipo_procesamiento}' no implementado")
            
            self.logger.info(f"Procesamiento completado: {ruta_salida}")
            return ruta_salida, resumen
            
        except Exception as e:
            self.logger.error(f"Error en procesamiento {tipo_procesamiento}: {e}")
            raise
    
    @log_funcion
    def procesar_lote(self, archivos: List[Tuple[str, str]], 
                     opciones: Optional[Dict[str, Any]] = None) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Procesa múltiples archivos en lote
        
        Args:
            archivos: Lista de tuplas (ruta_archivo, tipo_procesamiento)
            opciones: Opciones adicionales para el procesamiento
            
        Returns:
            List[Tuple[str, Dict]]: Lista de resultados (ruta_salida, resumen)
        """
        if opciones is None:
            opciones = {}
        
        resultados = []
        total_archivos = len(archivos)
        
        self.logger.info(f"Iniciando procesamiento de lote: {total_archivos} archivos")
        
        for i, (ruta_archivo, tipo_procesamiento) in enumerate(archivos, 1):
            try:
                self.logger.info(f"Procesando archivo {i}/{total_archivos}: {ruta_archivo}")
                ruta_salida, resumen = self.procesar_archivo(ruta_archivo, tipo_procesamiento, opciones)
                resultados.append((ruta_salida, resumen))
                
            except Exception as e:
                self.logger.error(f"Error procesando archivo {ruta_archivo}: {e}")
                resultados.append((None, {'error': str(e)}))
        
        self.logger.info(f"Procesamiento de lote completado: {len(resultados)} archivos")
        return resultados
    
    @log_funcion
    def obtener_estadisticas_sistema(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del sistema
        
        Returns:
            Dict: Estadísticas del sistema
        """
        import os
        estadisticas = {
            'fecha_consulta': obtener_fecha_actual(),
            'procesadores_disponibles': list(self.procesadores.keys()),
            'procesadores_pendientes': self.procesadores_pendientes,
            'total_procesadores': len(self.procesadores),
            'directorios_sistema': {}
        }
        
        # Verificar directorios del sistema
        for nombre, ruta in DIRECTORIOS.items():
            try:
                if os.path.exists(ruta):
                    tamano = self._obtener_tamano_directorio(ruta)
                    estadisticas['directorios_sistema'][nombre] = {
                        'ruta': ruta,
                        'existe': True,
                        'tamano_bytes': tamano,
                        'tamano_mb': round(tamano / (1024 * 1024), 2)
                    }
                else:
                    estadisticas['directorios_sistema'][nombre] = {
                        'ruta': ruta,
                        'existe': False,
                        'tamano_bytes': 0,
                        'tamano_mb': 0
                    }
            except Exception as e:
                estadisticas['directorios_sistema'][nombre] = {
                    'ruta': ruta,
                    'existe': False,
                    'error': str(e)
                }
        
        return estadisticas
    
    def _obtener_tamano_directorio(self, ruta: str) -> int:
        """Calcula el tamaño total de un directorio"""
        import os
        tamano_total = 0
        try:
            for dirpath, dirnames, filenames in os.walk(ruta):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        tamano_total += os.path.getsize(filepath)
        except Exception:
            pass
        return tamano_total
    
    @log_funcion
    def limpiar_sistema(self, dias_antiguedad: int = 30) -> Dict[str, Any]:
        """
        Limpia archivos antiguos del sistema
        
        Args:
            dias_antiguedad: Días de antigüedad para considerar archivos obsoletos
            
        Returns:
            Dict: Resumen de la limpieza
        """
        import os
        from datetime import datetime, timedelta
        
        fecha_limite = datetime.now() - timedelta(days=dias_antiguedad)
        resumen = {
            'fecha_limpieza': obtener_fecha_actual(),
            'dias_antiguedad': dias_antiguedad,
            'archivos_eliminados': 0,
            'espacio_liberado_mb': 0,
            'errores': []
        }
        
        # Directorios a limpiar
        directorios_limpiar = ['temp', 'logs']
        
        for nombre_dir in directorios_limpiar:
            if nombre_dir in DIRECTORIOS:
                ruta_dir = DIRECTORIOS[nombre_dir]
                try:
                    archivos_eliminados, espacio_liberado = self._limpiar_directorio(ruta_dir, dias_antiguedad)
                    resumen['archivos_eliminados'] += archivos_eliminados
                    resumen['espacio_liberado_mb'] += round(espacio_liberado / (1024 * 1024), 2)
                except Exception as e:
                    resumen['errores'].append(f"Error limpiando {nombre_dir}: {e}")
        
        self.logger.info(f"Limpieza completada: {resumen['archivos_eliminados']} archivos eliminados")
        return resumen
    
    def _limpiar_directorio(self, ruta_directorio: str, dias_antiguedad: int) -> Tuple[int, int]:
        """Limpia archivos antiguos de un directorio específico"""
        import os
        from datetime import datetime, timedelta
        
        fecha_limite = datetime.now() - timedelta(days=dias_antiguedad)
        archivos_eliminados = 0
        espacio_liberado = 0
        
        try:
            for filename in os.listdir(ruta_directorio):
                filepath = os.path.join(ruta_directorio, filename)
                if os.path.isfile(filepath):
                    # Verificar fecha de modificación
                    fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if fecha_modificacion < fecha_limite:
                        try:
                            tamano_archivo = os.path.getsize(filepath)
                            os.remove(filepath)
                            archivos_eliminados += 1
                            espacio_liberado += tamano_archivo
                        except Exception as e:
                            self.logger.warning(f"No se pudo eliminar {filepath}: {e}")
        except Exception as e:
            self.logger.warning(f"Error accediendo a {ruta_directorio}: {e}")
        
        return archivos_eliminados, espacio_liberado
    
    @log_funcion
    def generar_reporte_sistema(self) -> Dict[str, Any]:
        """
        Genera un reporte completo del sistema
        
        Returns:
            Dict: Reporte del sistema
        """
        reporte = {
            'fecha_reporte': obtener_fecha_actual(),
            'version_sistema': '2.0.1',
            'estadisticas': self.obtener_estadisticas_sistema(),
            'configuracion': {
                'tipos_procesamiento': TIPOS_PROCESAMIENTO,
                'directorios': DIRECTORIOS
            }
        }
        
        return reporte

# =============================================================================
# FUNCIONES DE CONVENIENCIA
# =============================================================================

def procesar_archivo(ruta_archivo: str, tipo_procesamiento: str, 
                    opciones: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any]]:
    """Función de conveniencia para procesar un archivo"""
    orquestador = OrquestadorPrincipal()
    return orquestador.procesar_archivo(ruta_archivo, tipo_procesamiento, opciones)

def procesar_lote(archivos: List[Tuple[str, str]], 
                 opciones: Optional[Dict[str, Any]] = None) -> List[Tuple[str, Dict[str, Any]]]:
    """Función de conveniencia para procesar múltiples archivos"""
    orquestador = OrquestadorPrincipal()
    return orquestador.procesar_lote(archivos, opciones)

def obtener_estadisticas_sistema() -> Dict[str, Any]:
    """Función de conveniencia para obtener estadísticas"""
    orquestador = OrquestadorPrincipal()
    return orquestador.obtener_estadisticas_sistema()

# =============================================================================
# INTERFAZ DE LÍNEA DE COMANDOS
# =============================================================================

def crear_parser_argumentos():
    """Crea el parser de argumentos para la línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Orquestador Principal del Sistema de Procesamiento de Cartera',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python orquestador_principal.py procesar archivo.xlsx --tipo cartera
  python orquestador_principal.py lote archivos.txt
  python orquestador_principal.py estadisticas
  python orquestador_principal.py limpiar --dias 30
  python orquestador_principal.py reporte
        """
    )
    
    subparsers = parser.add_subparsers(dest='comando', help='Comandos disponibles')
    
    # Comando procesar
    parser_procesar = subparsers.add_parser('procesar', help='Procesar un archivo')
    parser_procesar.add_argument('archivo', help='Ruta del archivo a procesar')
    parser_procesar.add_argument('--tipo', '-t', required=True, 
                                choices=['cartera', 'acumulado', 'formato_deuda', 'anticipos'],
                                help='Tipo de procesamiento')
    parser_procesar.add_argument('--opciones', '-o', help='Opciones adicionales (JSON)')
    
    # Comando lote
    parser_lote = subparsers.add_parser('lote', help='Procesar múltiples archivos')
    parser_lote.add_argument('archivo_lista', help='Archivo con lista de archivos a procesar')
    parser_lote.add_argument('--opciones', '-o', help='Opciones adicionales (JSON)')
    
    # Comando estadísticas
    subparsers.add_parser('estadisticas', help='Obtener estadísticas del sistema')
    
    # Comando limpiar
    parser_limpiar = subparsers.add_parser('limpiar', help='Limpiar archivos antiguos')
    parser_limpiar.add_argument('--dias', '-d', type=int, default=30,
                               help='Días de antigüedad para eliminar archivos')
    
    # Comando reporte
    subparsers.add_parser('reporte', help='Generar reporte completo del sistema')
    
    return parser

def main():
    """Función principal"""
    parser = crear_parser_argumentos()
    args = parser.parse_args()
    
    if not args.comando:
        parser.print_help()
        return
    
    try:
        orquestador = OrquestadorPrincipal()
        
        if args.comando == 'procesar':
            opciones = {}
            if args.opciones:
                import json
                opciones = json.loads(args.opciones)
            
            ruta_salida, resumen = orquestador.procesar_archivo(args.archivo, args.tipo, opciones)
            print(f"Procesamiento completado exitosamente")
            print(f"Archivo de salida: {ruta_salida}")
            print(f"Resumen: {resumen}")
            
        elif args.comando == 'lote':
            # Leer lista de archivos
            with open(args.archivo_lista, 'r') as f:
                archivos = []
                for linea in f:
                    linea = linea.strip()
                    if linea and not linea.startswith('#'):
                        partes = linea.split(',')
                        if len(partes) >= 2:
                            archivos.append((partes[0].strip(), partes[1].strip()))
            
            opciones = {}
            if args.opciones:
                import json
                opciones = json.loads(args.opciones)
            
            resultados = orquestador.procesar_lote(archivos, opciones)
            print(f"Procesamiento de lote completado: {len(resultados)} archivos")
            for i, (ruta_salida, resumen) in enumerate(resultados, 1):
                if ruta_salida:
                    print(f"  {i}. OK {ruta_salida}")
                else:
                    print(f"  {i}. ERROR: {resumen.get('error', 'Desconocido')}")
                    
        elif args.comando == 'estadisticas':
            estadisticas = orquestador.obtener_estadisticas_sistema()
            print("Estadisticas del Sistema:")
            print(f"  Procesadores disponibles: {estadisticas['procesadores_disponibles']}")
            print(f"  Procesadores pendientes: {estadisticas['procesadores_pendientes']}")
            print(f"  Total procesadores: {estadisticas['total_procesadores']}")
            
        elif args.comando == 'limpiar':
            resumen = orquestador.limpiar_sistema(args.dias)
            print(f"Limpieza completada:")
            print(f"  Archivos eliminados: {resumen['archivos_eliminados']}")
            print(f"  Espacio liberado: {resumen['espacio_liberado_mb']} MB")
            
        elif args.comando == 'reporte':
            reporte = orquestador.generar_reporte_sistema()
            print("Reporte del Sistema:")
            print(f"  Version: {reporte['version_sistema']}")
            print(f"  Fecha: {reporte['fecha_reporte']}")
            print(f"  Procesadores: {reporte['estadisticas']['procesadores_disponibles']}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
