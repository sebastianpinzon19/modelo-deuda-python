#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas del Sistema de Gestión de Cartera
"""

import os
import sys
import unittest
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

class TestSistemaCartera(unittest.TestCase):
    """Pruebas del sistema de cartera"""
    
    def setUp(self):
        """Configuración inicial"""
        self.base_dir = Path(__file__).parent
        self.uploads_dir = self.base_dir / 'uploads'
        self.outputs_dir = self.base_dir / 'outputs'
        
        # Crear directorios si no existen
        self.uploads_dir.mkdir(exist_ok=True)
        self.outputs_dir.mkdir(exist_ok=True)
    
    def test_imports(self):
        """Probar que todos los módulos se pueden importar"""
        try:
            from app import app
            from config import config
            from utils import validate_csv_file, validate_excel_file
            from PROVCA.trm_config import TRMConfig
            from PROVCA.procesador_cartera import procesar_cartera
            from PROVCA.procesador_anticipos import procesar_anticipos
            from PROVCA.modelo_deuda import procesar_modelo_deuda
            from PROVCA.procesador_unificado import procesar_balance
            print("✅ Todos los módulos se importaron correctamente")
        except ImportError as e:
            self.fail(f"Error importando módulos: {e}")
    
    def test_config(self):
        """Probar configuración"""
        from config import config
        
        # Verificar que la configuración existe
        self.assertIn('default', config)
        self.assertIn('development', config)
        self.assertIn('production', config)
        
        # Verificar configuración por defecto
        default_config = config['default']
        self.assertTrue(hasattr(default_config, 'SECRET_KEY'))
        self.assertTrue(hasattr(default_config, 'UPLOAD_FOLDER'))
        self.assertTrue(hasattr(default_config, 'OUTPUT_FOLDER'))
        
        print("✅ Configuración correcta")
    
    def test_trm_config(self):
        """Probar configuración TRM"""
        from PROVCA.trm_config import TRMConfig
        
        trm = TRMConfig()
        
        # Probar cargar configuración
        config = trm.cargar_configuracion()
        self.assertIsInstance(config, dict)
        
        # Probar guardar configuración
        test_config = {'trm_usd': 4000.0, 'trm_eur': 4700.0}
        trm.guardar_configuracion(test_config)
        
        # Verificar que se guardó
        loaded_config = trm.cargar_configuracion()
        self.assertEqual(loaded_config.get('trm_usd'), 4000.0)
        self.assertEqual(loaded_config.get('trm_eur'), 4700.0)
        
        print("✅ Configuración TRM funciona correctamente")
    
    def test_utils(self):
        """Probar utilidades"""
        from utils import validate_csv_file, validate_excel_file, validate_date_format, validate_trm_value
        
        # Probar validación de archivos CSV
        self.assertTrue(validate_csv_file('test.csv'))
        self.assertFalse(validate_csv_file('test.txt'))
        self.assertFalse(validate_csv_file('test.xlsx'))
        
        # Probar validación de archivos Excel
        self.assertTrue(validate_excel_file('test.xlsx'))
        self.assertTrue(validate_excel_file('test.xls'))
        self.assertFalse(validate_excel_file('test.csv'))
        
        # Probar validación de fechas
        self.assertTrue(validate_date_format('2024-12-31'))
        self.assertFalse(validate_date_format('31-12-2024'))
        self.assertFalse(validate_date_format('invalid'))
        
        # Probar validación de TRM
        self.assertTrue(validate_trm_value('4000'))
        self.assertTrue(validate_trm_value('4000.50'))
        self.assertTrue(validate_trm_value('4,000.50'))
        self.assertFalse(validate_trm_value('0'))
        self.assertFalse(validate_trm_value('-100'))
        self.assertFalse(validate_trm_value('invalid'))
        
        print("✅ Utilidades funcionan correctamente")
    
    def test_directories(self):
        """Probar que los directorios necesarios existen"""
        required_dirs = [
            self.base_dir / 'uploads',
            self.base_dir / 'outputs',
            self.base_dir / 'templates',
            self.base_dir / 'PROVCA'
        ]
        
        for dir_path in required_dirs:
            self.assertTrue(dir_path.exists(), f"Directorio {dir_path} no existe")
        
        print("✅ Todos los directorios necesarios existen")
    
    def test_files(self):
        """Probar que los archivos necesarios existen"""
        required_files = [
            self.base_dir / 'app.py',
            self.base_dir / 'config.py',
            self.base_dir / 'utils.py',
            self.base_dir / 'requirements.txt',
            self.base_dir / 'templates' / 'index.html',
            self.base_dir / 'PROVCA' / 'trm_config.py',
            self.base_dir / 'PROVCA' / 'procesador_cartera.py',
            self.base_dir / 'PROVCA' / 'procesador_anticipos.py',
            self.base_dir / 'PROVCA' / 'modelo_deuda.py',
            self.base_dir / 'PROVCA' / 'procesador_unificado.py'
        ]
        
        for file_path in required_files:
            self.assertTrue(file_path.exists(), f"Archivo {file_path} no existe")
        
        print("✅ Todos los archivos necesarios existen")

def run_tests():
    """Ejecutar todas las pruebas"""
    print("🧪 Ejecutando pruebas del Sistema de Gestión de Cartera...")
    print("=" * 60)
    
    # Crear suite de pruebas
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSistemaCartera)
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 60)
    if result.wasSuccessful():
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("✅ El sistema está listo para usar")
        return True
    else:
        print("❌ Algunas pruebas fallaron")
        print("🔧 Revisa los errores antes de usar el sistema")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
