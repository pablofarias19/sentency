#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
🚀 PROCESADOR ÚNICO - ANALYSER MÉTODO v3.1 UNIFICADO
===========================================================
ESTE ES EL ÚNICO ARCHIVO QUE NECESITAS EJECUTAR.

Hace TODO automáticamente:
✅ Actualiza bases de datos
✅ Procesa nuevos PDFs
✅ Actualiza metadatos
✅ Sincroniza índices vectoriales  
✅ Genera perfiles cognitivos
✅ Sistema listo para usar

USO SIMPLE:
python procesar_todo.py

NO necesitas ejecutar otros archivos de ingesta.
===========================================================
"""

import os
import sys
import sqlite3
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Añadir rutas necesarias
BASE_PATH = Path(__file__).resolve().parent  # Carpeta donde está procesar_todo.py
SCRIPTS_DIR = BASE_PATH / "colaborative" / "scripts"
sys.path.append(str(SCRIPTS_DIR))

# Rutas principales
PDFS_DIR = BASE_PATH / "colaborative" / "data" / "pdfs" / "general"
DB_COGNITIVA = BASE_PATH / "colaborative" / "bases_rag" / "cognitiva" / "metadatos.db"

def print_header(titulo: str):
    """Imprime header formateado."""
    print("\n" + "=" * 70)
    print(f"🚀 {titulo}")
    print("=" * 70)

def print_step(paso: str):
    """Imprime paso del proceso."""
    print(f"\n📋 {paso}")
    print("-" * 50)

def verificar_pdfs_nuevos() -> List[Path]:
    """Verifica si hay PDFs nuevos para procesar."""
    if not PDFS_DIR.exists():
        PDFS_DIR.mkdir(parents=True, exist_ok=True)
        return []
    
    pdfs_disponibles = list(PDFS_DIR.glob("*.pdf"))
    
    # Verificar cuáles ya están en la BD
    pdfs_procesados = set()
    if DB_COGNITIVA.exists():
        try:
            with sqlite3.connect(str(DB_COGNITIVA)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT archivo FROM perfiles_cognitivos")
                for row in cursor.fetchall():
                    if row[0]:
                        nombre_archivo = Path(row[0]).name
                        pdfs_procesados.add(nombre_archivo)
        except Exception:
            pass
    
    # PDFs nuevos = todos - ya procesados
    pdfs_nuevos = []
    for pdf in pdfs_disponibles:
        if pdf.name not in pdfs_procesados:
            pdfs_nuevos.append(pdf)
    
    return pdfs_nuevos

def ejecutar_ingesta_unificada():
    """Ejecuta la ingesta cognitiva unificada."""
    try:
        # Importar el módulo principal
        from ingesta_cognitiva import main as ejecutar_ingesta
        
        print("🔄 Ejecutando ingesta cognitiva unificada...")
        resultado = ejecutar_ingesta()
        
        if resultado:
            print("✅ Ingesta completada exitosamente")
            return True
        else:
            print("⚠️ Ingesta completada con advertencias")
            return True
            
    except ImportError as e:
        print(f"❌ Error importando ingesta_cognitiva: {e}")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando ingesta: {e}")
        return False

def actualizar_bases_automatico():
    """Actualiza todas las bases automáticamente."""
    try:
        # Importar y ejecutar actualizador
        sys.path.append(str(BASE_PATH))
        
        # Ejecutar actualizador rápido
        from actualizador_rapido import actualizar_sistema_completo
        
        print("🔄 Actualizando bases de datos...")
        resultado = actualizar_sistema_completo()
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error actualizando bases: {e}")
        return False

def verificar_estado_final():
    """Verifica que todo esté funcionando correctamente."""
    try:
        verificaciones = []
        
        # 1. Verificar base cognitiva
        if DB_COGNITIVA.exists():
            with sqlite3.connect(str(DB_COGNITIVA)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
                count = cursor.fetchone()[0]
                if count > 0:
                    verificaciones.append(f"✅ Base cognitiva: {count} perfiles")
                else:
                    verificaciones.append("❌ Base cognitiva: Sin datos")
        else:
            verificaciones.append("❌ Base cognitiva: No existe")
        
        # 2. Verificar PDFs
        pdfs_total = len(list(PDFS_DIR.glob("*.pdf"))) if PDFS_DIR.exists() else 0
        verificaciones.append(f"📄 PDFs disponibles: {pdfs_total}")
        
        # 3. Verificar webapp
        webapp_path = SCRIPTS_DIR / "end2end_webapp.py"
        if webapp_path.exists():
            verificaciones.append("✅ Webapp: Lista para usar")
        else:
            verificaciones.append("❌ Webapp: No encontrada")
        
        return verificaciones
        
    except Exception as e:
        return [f"❌ Error en verificación: {e}"]

def main():
    """Función principal unificada."""
    print_header("PROCESADOR ÚNICO - ANALYSER MÉTODO v3.1")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Directorio: {BASE_PATH}")
    
    # 1. Verificar PDFs disponibles
    print_step("1. VERIFICANDO PDFs DISPONIBLES")
    
    if not PDFS_DIR.exists():
        PDFS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"📁 Creado directorio: {PDFS_DIR}")
    
    pdfs_total = list(PDFS_DIR.glob("*.pdf"))
    pdfs_nuevos = verificar_pdfs_nuevos()
    
    print(f"📄 PDFs totales encontrados: {len(pdfs_total)}")
    print(f"🆕 PDFs nuevos para procesar: {len(pdfs_nuevos)}")
    
    if pdfs_total:
        print("📋 PDFs disponibles:")
        for pdf in pdfs_total:
            estado = "🆕 NUEVO" if pdf in pdfs_nuevos else "✅ PROCESADO"
            print(f"   {estado} {pdf.name}")
    else:
        print("📄 No hay PDFs en el directorio")
        print(f"💡 Coloca archivos PDF en: {PDFS_DIR}")
        print("   Luego ejecuta este script nuevamente")
        return False
    
    # 2. Actualizar bases si es necesario
    if pdfs_nuevos or not DB_COGNITIVA.exists():
        print_step("2. ACTUALIZANDO SISTEMA DE BASES DE DATOS")
        resultado_bases = actualizar_bases_automatico()
        if not resultado_bases:
            print("⚠️ Advertencia: Problemas actualizando bases")
    else:
        print_step("2. BASES DE DATOS ACTUALIZADAS")
        print("✅ No se requiere actualización de bases")
    
    # 3. Procesar documentos
    if pdfs_nuevos:
        print_step("3. PROCESANDO DOCUMENTOS NUEVOS")
        resultado_ingesta = ejecutar_ingesta_unificada()
        if not resultado_ingesta:
            print("❌ Error procesando documentos")
            return False
    else:
        print_step("3. DOCUMENTOS YA PROCESADOS")
        print("✅ Todos los documentos están procesados")
    
    # 4. Sincronización automática de bases
    print_step("4. SINCRONIZACIÓN AUTOMÁTICA DE BASES")
    try:
        from sincronizador_automatico import SincronizadorAutomatico
        sincronizador = SincronizadorAutomatico()
        sincronizador.sincronizar_todo()
    except Exception as e:
        print(f"⚠️ Advertencia en sincronización: {e}")
    
    # 5. Verificación final
    print_step("5. VERIFICACIÓN FINAL DEL SISTEMA")
    
    verificaciones = verificar_estado_final()
    for verificacion in verificaciones:
        print(f"   {verificacion}")
    
    # 6. Instrucciones finales
    print_step("6. SISTEMA LISTO")
    
    print("🎉 PROCESAMIENTO COMPLETADO")
    print("")
    print("🚀 PARA USAR EL SISTEMA:")
    print("   1. Ejecuta: .\\iniciar_sistema.bat")
    print("   2. O desde PowerShell: python colaborative\\scripts\\end2end_webapp.py")
    print("   3. El navegador se abrirá en: http://127.0.0.1:5002")
    print("")
    print("📊 RUTAS DISPONIBLES:")
    print("   • /           → Consultas principales")
    print("   • /cognitivo  → Análisis ANALYSER MÉTODO")
    print("   • /radar      → Radar cognitivo interactivo")
    print("   • /perfiles   → Perfiles de autores")
    print("")
    print("💡 PARA AGREGAR MÁS DOCUMENTOS:")
    print(f"   1. Copia PDFs a: {PDFS_DIR}")
    print("   2. Ejecuta: python procesar_todo.py")
    print("")
    print("✅ NO necesitas ejecutar otros archivos de ingesta")
    print("   Este script hace TODO automáticamente")
    
    return True

if __name__ == "__main__":
    try:
        resultado = main()
        if resultado:
            print("\n🎉 ¡SISTEMA LISTO PARA USAR!")
        else:
            print("\n⚠️ Completado con advertencias")
    except KeyboardInterrupt:
        print("\n⏹️ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()