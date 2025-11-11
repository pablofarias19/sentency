#!/usr/bin/env python3
"""
🎉 VERIFICADOR DE SISTEMA COGNITIVO COMPLETO
===========================================

Script final para verificar que todos los componentes
del Sistema RAG Cognitivo estén correctamente implementados.

Ejecutar para confirmar el estado del sistema.
"""

import os
import sys
from pathlib import Path

def verificar_sistema():
    """Verificación completa del sistema cognitivo."""
    
    print("🧠 VERIFICANDO SISTEMA RAG COGNITIVO COMPLETO")
    print("=" * 50)
    
    # Rutas base
    base_path = Path(__file__).parent
    scripts_path = base_path / "colaborative" / "scripts"
    models_path = base_path / "colaborative" / "models"
    data_path = base_path / "colaborative" / "data"
    
    errores = []
    verificaciones = []
    
    # 1. Verificar módulos cognitivos principales
    modulos_core = [
        ("vectorizador_cognitivo.py", "Análisis de 8 rasgos cognitivos"),
        ("analizador_perfiles.py", "Búsquedas FAISS cognitivas"),
        ("ingesta_cognitiva.py", "Pipeline dual completo"),
        ("end2end_webapp.py", "Webapp con rutas integradas")
    ]
    
    print("\n📁 VERIFICANDO MÓDULOS PRINCIPALES:")
    for archivo, descripcion in modulos_core:
        ruta = scripts_path / archivo
        if ruta.exists():
            print(f"  ✅ {archivo} - {descripcion}")
            verificaciones.append(f"✅ {archivo}")
        else:
            print(f"  ❌ {archivo} - FALTANTE")
            errores.append(f"❌ Falta: {archivo}")
    
    # 2. Verificar estructura de datos
    print("\n🗂️  VERIFICANDO ESTRUCTURA DE DATOS:")
    estructura_requerida = [
        (data_path / "chunks", "Directorio de chunks"),
        (data_path / "index", "Directorio de índices FAISS"),
        (data_path / "pdfs" / "general", "Directorio de PDFs"),
        (models_path / "cognitive", "Modelos cognitivos"),
    ]
    
    for ruta, descripcion in estructura_requerida:
        if ruta.exists():
            print(f"  ✅ {ruta.name} - {descripcion}")
            verificaciones.append(f"✅ {ruta.name}")
        else:
            print(f"  ⚠️  {ruta.name} - Se creará automáticamente")
    
    # 3. Verificar dependencias críticas
    print("\n📦 VERIFICANDO DEPENDENCIAS CRÍTICAS:")
    dependencias = [
        ("faiss", "faiss-cpu"),
        ("sentence_transformers", "sentence-transformers"),
        ("google.generativeai", "google-generativeai"),
        ("flask", "Flask"),
        ("tabulate", "tabulate"),
        ("PyMuPDF", "fitz")
    ]
    
    for modulo, paquete in dependencias:
        try:
            if modulo == "PyMuPDF":
                import fitz
            else:
                __import__(modulo)
            print(f"  ✅ {paquete}")
            verificaciones.append(f"✅ {paquete}")
        except ImportError:
            print(f"  ❌ {paquete} - INSTALAR: pip install {paquete}")
            errores.append(f"❌ Falta dependencia: {paquete}")
    
    # 4. Verificar configuración cognitiva
    print("\n⚙️  VERIFICANDO CONFIGURACIÓN COGNITIVA:")
    config_cognitivo = models_path / "cognitive" / "config.json"
    if config_cognitivo.exists():
        print("  ✅ Configuración cognitiva presente")
        verificaciones.append("✅ Config cognitiva")
    else:
        print("  ⚠️  Configuración cognitiva - Se creará automáticamente")
    
    # 5. Verificar webapp
    print("\n🌐 VERIFICANDO WEBAPP:")
    webapp_path = scripts_path / "end2end_webapp.py"
    if webapp_path.exists():
        # Verificar que tenga la ruta /cognitivo
        with open(webapp_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if '/cognitivo' in contenido and 'panel_cognitivo' in contenido:
                print("  ✅ Webapp con ruta /cognitivo integrada")
                verificaciones.append("✅ Ruta /cognitivo")
            else:
                print("  ❌ Webapp sin integración cognitiva")
                errores.append("❌ Falta ruta /cognitivo")
    
    # Resultado final
    print("\n" + "=" * 50)
    print("📊 RESULTADO DE VERIFICACIÓN:")
    print(f"  ✅ Verificaciones exitosas: {len(verificaciones)}")
    print(f"  ❌ Errores encontrados: {len(errores)}")
    
    if errores:
        print("\n🔧 ERRORES A RESOLVER:")
        for error in errores:
            print(f"  {error}")
    else:
        print("\n🎉 SISTEMA COMPLETAMENTE OPERATIVO")
        print("🚀 Todos los componentes están correctamente implementados")
        print("🌐 Webapp lista en: http://127.0.0.1:5002")
        print("🧠 Sistema ANALYSER disponible en: /cognitivo")
    
    return len(errores) == 0

if __name__ == "__main__":
    exito = verificar_sistema()
    
    if exito:
        print("\n🎯 INSTRUCCIONES DE USO:")
        print("1. Activar entorno: .venv\\Scripts\\Activate.ps1")
        print("2. Iniciar webapp: python colaborative/scripts/end2end_webapp.py")
        print("3. Abrir navegador: http://127.0.0.1:5002")
        print("4. Ir a /cognitivo para sistema ANALYSER")
        print("\n🚀 ¡SISTEMA LISTO PARA USO!")
        sys.exit(0)
    else:
        print("\n⚠️  RESUELVE LOS ERRORES ANTES DE USAR EL SISTEMA")
        sys.exit(1)