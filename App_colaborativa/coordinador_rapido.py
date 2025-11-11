#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 COORDINADOR RÁPIDO Y SIMPLE v1.0
===================================
Implementación directa de la OPCIÓN D sin complicaciones

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
BASE_PATH = Path(__file__).parent  # Solo un parent porque el archivo está en la raíz
SCRIPTS_PATH = BASE_PATH / "colaborative" / "scripts"
PDFS_PATH = BASE_PATH / "colaborative" / "data" / "pdfs" / "general"

class CoordinadorRapido:
    """Coordinador simplificado que solo usa 2 procesadores"""
    
    def __init__(self):
        self.version = "v1.0_rapido"
        print(f"🚀 COORDINADOR RÁPIDO {self.version}")
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
    
    def procesar_con_optimizado(self, ruta_pdf: str) -> bool:
        """Ejecuta procesador_cognitivo_optimizado.py"""
        
        print("\\n🚀 Ejecutando procesador optimizado con chunking...")
        
        try:
            # Cambiar al directorio correcto
            os.chdir(BASE_PATH)
            
            # Comando directo
            comando = f"python colaborative/scripts/procesador_cognitivo_optimizado.py"
            
            print(f"🔧 Comando: {comando}")
            resultado = os.system(comando)
            
            if resultado == 0:
                print("✅ Procesador optimizado completado exitosamente")
                return True
            else:
                print(f"❌ Error en procesador optimizado: código {resultado}")
                return False
                
        except Exception as e:
            print(f"💥 Excepción en procesador optimizado: {e}")
            return False
    
    def procesar_con_ligero(self, ruta_pdf: str) -> bool:
        """Ejecuta ingesta_cognitiva.py"""
        
        print("\\n⚡ Ejecutando ingesta cognitiva ligera...")
        
        try:
            # Cambiar al directorio correcto
            os.chdir(BASE_PATH)
            
            # Comando directo
            comando = f"python colaborative/scripts/ingesta_cognitiva.py"
            
            print(f"🔧 Comando: {comando}")
            resultado = os.system(comando)
            
            if resultado == 0:
                print("✅ Ingesta cognitiva completada exitosamente")
                return True
            else:
                print(f"❌ Error en ingesta cognitiva: código {resultado}")
                return False
                
        except Exception as e:
            print(f"💥 Excepción en ingesta cognitiva: {e}")
            return False
    
    def procesar_documento(self, nombre_pdf: str) -> dict:
        """Procesa un documento específico"""
        
        ruta_pdf = PDFS_PATH / nombre_pdf
        
        if not ruta_pdf.exists():
            return {
                "error": f"Archivo no encontrado: {nombre_pdf}",
                "ruta_buscada": str(ruta_pdf)
            }
        
        print(f"\\n🎯 PROCESANDO: {nombre_pdf}")
        print("=" * 60)
        
        # 1. Estimar tamaño
        tamano_estimado = self.estimar_tamano_archivo(str(ruta_pdf))
        
        # 2. Seleccionar procesador
        procesador = self.seleccionar_procesador(tamano_estimado)
        
        # 3. Ejecutar procesamiento
        inicio = time.time()
        
        if procesador == "optimizado":
            exito = self.procesar_con_optimizado(str(ruta_pdf))
        else:
            exito = self.procesar_con_ligero(str(ruta_pdf))
        
        tiempo_total = time.time() - inicio
        
        # 4. Resultado
        resultado = {
            "archivo": nombre_pdf,
            "tamano_estimado": tamano_estimado,
            "procesador_usado": procesador,
            "tiempo_segundos": tiempo_total,
            "exitoso": exito
        }
        
        print("\\n" + "=" * 60)
        print("📊 RESULTADO:")
        print(f"   📄 Archivo: {nombre_pdf}")
        print(f"   📏 Tamaño estimado: {tamano_estimado:,} caracteres")
        print(f"   🚀 Procesador: {procesador}")
        print(f"   ⏱️ Tiempo: {tiempo_total:.1f} segundos")
        print(f"   ✅ Estado: {'EXITOSO' if exito else 'ERROR'}")
        print("=" * 60)
        
        return resultado

def main():
    """Función principal"""
    
    if len(sys.argv) < 2:
        print("❌ Uso: python coordinador_rapido.py 'nombre_archivo.pdf'")
        print("\\n📁 Archivos disponibles en:")
        print(f"   {PDFS_PATH}")
        
        if PDFS_PATH.exists():
            pdfs = list(PDFS_PATH.glob("*.pdf"))
            for pdf in pdfs[:5]:  # Mostrar solo los primeros 5
                print(f"   📄 {pdf.name}")
        
        return
    
    nombre_pdf = sys.argv[1]
    
    coordinador = CoordinadorRapido()
    resultado = coordinador.procesar_documento(nombre_pdf)
    
    if "error" in resultado:
        print(f"💥 ERROR: {resultado['error']}")
        print(f"📁 Ruta buscada: {resultado['ruta_buscada']}")
    
    print("\\n🎉 Coordinación completada")

if __name__ == "__main__":
    main()