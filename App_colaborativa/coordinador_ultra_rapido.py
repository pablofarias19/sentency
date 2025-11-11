#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 COORDINADOR ULTRA RÁPIDO - SOLO UN ARCHIVO
=============================================
Procesa específicamente un solo PDF usando la OPCIÓN D

CRITERIO SIMPLE:
📏 < 100k caracteres  → ingesta_cognitiva.py (RÁPIDO)
📏 ≥ 100k caracteres  → procesador_cognitivo_optimizado.py (CHUNKING)

AUTOR: Sistema de Coordinación Optimizada
FECHA: 10 NOV 2025
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Configuración de rutas
BASE_PATH = Path(__file__).parent
SCRIPTS_PATH = BASE_PATH / "colaborative" / "scripts"
PDFS_PATH = BASE_PATH / "colaborative" / "data" / "pdfs" / "general"

class CoordinadorUltraRapido:
    """Coordinador que procesa un solo archivo específico"""
    
    def __init__(self):
        self.version = "v1.0_ultra_rapido"
        print(f"⚡ COORDINADOR ULTRA RÁPIDO {self.version}")
        print("=" * 50)
    
    def estimar_tamano_archivo(self, ruta_pdf: str) -> int:
        """Estima caracteres basándose en el tamaño del archivo"""
        
        try:
            nombre_archivo = os.path.basename(ruta_pdf).lower()
            tamano_archivo = os.path.getsize(ruta_pdf)
            
            # Casos específicos conocidos
            if "daniel_brola" in nombre_archivo or "teoria_y_practica_del_amparo" in nombre_archivo:
                print("📚 Documento Daniel Brola detectado: ~729,000 caracteres")
                return 729000
            
            # Estimación simple: ~1800 caracteres por cada 50KB
            caracteres_estimados = int((tamano_archivo / 50000) * 1800)
            
            print(f"📏 Archivo: {tamano_archivo:,} bytes → Estimado: {caracteres_estimados:,} caracteres")
            return caracteres_estimados
            
        except Exception as e:
            print(f"⚠️ Error estimando: {e}")
            return 50000
    
    def seleccionar_procesador(self, tamano_caracteres: int) -> str:
        """Selecciona procesador según criterio simple"""
        
        if tamano_caracteres >= 100000:
            print("📊 DOCUMENTO GRANDE → procesador_cognitivo_optimizado.py")
            return "optimizado"
        else:
            print("⚡ DOCUMENTO PEQUEÑO → ingesta_cognitiva.py")
            return "ligero"
    
    def procesar_con_optimizado(self, nombre_pdf: str) -> bool:
        """Ejecuta procesador optimizado modificado para un solo archivo"""
        
        print("\\n🚀 Ejecutando procesador optimizado con chunking...")
        
        try:
            # Importar el procesador directamente
            sys.path.append(str(SCRIPTS_PATH))
            from procesador_cognitivo_optimizado import ProcesadorCognitivoOptimizado
            
            procesador = ProcesadorCognitivoOptimizado()
            ruta_completa = PDFS_PATH / nombre_pdf
            
            print(f"📄 Procesando: {nombre_pdf}")
            resultado = procesador.procesar_documento_optimizado(str(ruta_completa))
            
            if resultado:
                print(f"✅ Documento procesado exitosamente: {resultado}")
                return True
            else:
                print("❌ Error en el procesamiento")
                return False
                
        except Exception as e:
            print(f"💥 Excepción en procesador optimizado: {e}")
            return False
    
    def procesar_con_ligero(self, nombre_pdf: str) -> bool:
        """Ejecuta ingesta cognitiva para un solo archivo"""
        
        print("\\n⚡ Ejecutando ingesta cognitiva ligera...")
        
        try:
            # Cambiar al directorio base y ejecutar solo para este archivo
            os.chdir(BASE_PATH)
            
            # Copiar temporalmente el archivo a una carpeta temporal
            import shutil
            import tempfile
            
            # Crear directorio temporal
            temp_dir = Path(tempfile.mkdtemp())
            temp_pdf_dir = temp_dir / "pdfs" / "general"
            temp_pdf_dir.mkdir(parents=True, exist_ok=True)
            
            # Copiar solo el archivo específico
            archivo_original = PDFS_PATH / nombre_pdf
            archivo_temp = temp_pdf_dir / nombre_pdf
            shutil.copy2(archivo_original, archivo_temp)
            
            print(f"📄 Archivo copiado a directorio temporal: {archivo_temp}")
            
            # Modificar la variable de entorno para que apunte al directorio temporal
            env = os.environ.copy()
            env['PDFS_PATH'] = str(temp_pdf_dir)
            
            comando = f"python colaborative/scripts/ingesta_cognitiva.py"
            print(f"🔧 Comando: {comando}")
            
            resultado = os.system(comando)
            
            # Limpiar directorio temporal
            shutil.rmtree(temp_dir)
            
            if resultado == 0:
                print("✅ Ingesta cognitiva completada exitosamente")
                return True
            else:
                print(f"❌ Error en ingesta cognitiva: código {resultado}")
                return False
                
        except Exception as e:
            print(f"💥 Excepción en ingesta cognitiva: {e}")
            return False
    
    def procesar_documento_especifico(self, nombre_pdf: str) -> dict:
        """Procesa un documento específico"""
        
        ruta_pdf = PDFS_PATH / nombre_pdf
        
        if not ruta_pdf.exists():
            return {
                "error": f"Archivo no encontrado: {nombre_pdf}",
                "ruta_buscada": str(ruta_pdf)
            }
        
        print(f"\\n🎯 PROCESANDO ESPECÍFICAMENTE: {nombre_pdf}")
        print("=" * 70)
        
        # 1. Estimar tamaño
        tamano_estimado = self.estimar_tamano_archivo(str(ruta_pdf))
        
        # 2. Seleccionar procesador
        procesador = self.seleccionar_procesador(tamano_estimado)
        
        # 3. Ejecutar procesamiento
        inicio = time.time()
        
        if procesador == "optimizado":
            exito = self.procesar_con_optimizado(nombre_pdf)
        else:
            exito = self.procesar_con_ligero(nombre_pdf)
        
        tiempo_total = time.time() - inicio
        
        # 4. Resultado
        resultado = {
            "archivo": nombre_pdf,
            "tamano_estimado": tamano_estimado,
            "procesador_usado": procesador,
            "tiempo_segundos": tiempo_total,
            "exitoso": exito
        }
        
        print("\\n" + "=" * 70)
        print("📊 RESULTADO FINAL:")
        print(f"   📄 Archivo: {nombre_pdf}")
        print(f"   📏 Tamaño estimado: {tamano_estimado:,} caracteres")
        print(f"   🚀 Procesador usado: {procesador}")
        print(f"   ⏱️ Tiempo total: {tiempo_total:.1f} segundos")
        print(f"   ✅ Estado: {'EXITOSO' if exito else 'ERROR'}")
        print("=" * 70)
        
        return resultado

def main():
    """Función principal"""
    
    if len(sys.argv) < 2:
        print("❌ Uso: python coordinador_ultra_rapido.py 'nombre_archivo.pdf'")
        print("\\n📁 Archivos disponibles:")
        
        if PDFS_PATH.exists():
            pdfs = list(PDFS_PATH.glob("*.pdf"))
            for pdf in pdfs:
                print(f"   📄 {pdf.name}")
        
        return
    
    nombre_pdf = sys.argv[1]
    
    coordinador = CoordinadorUltraRapido()
    resultado = coordinador.procesar_documento_especifico(nombre_pdf)
    
    if "error" in resultado:
        print(f"\\n💥 ERROR: {resultado['error']}")
        print(f"📁 Ruta buscada: {resultado['ruta_buscada']}")
    else:
        print("\\n🎉 Coordinación específica completada")
        print("🌐 Para ver resultados: python colaborative/scripts/end2end_webapp.py")

if __name__ == "__main__":
    main()