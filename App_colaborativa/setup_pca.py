# -*- coding: utf-8 -*-
"""
Setup del Sistema RAG Enriquecido con PCA
Configura dependencias y estructura inicial
"""

import os
import sys
from pathlib import Path
import subprocess
import json

print("🚀 CONFIGURACIÓN DEL SISTEMA RAG ENRIQUECIDO CON PCA")
print("=" * 60)

# ==========================================================
# 🔹 VERIFICAR DEPENDENCIAS BÁSICAS
# ==========================================================
def check_python_version():
    """Verifica versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_pip():
    """Verifica que pip esté disponible"""
    try:
        import pip
        print("✅ pip disponible")
        return True
    except ImportError:
        print("❌ pip no encontrado")
        return False

# ==========================================================
# 🔹 INSTALAR DEPENDENCIAS
# ==========================================================
def install_requirements():
    """Instala las dependencias necesarias"""
    requirements = [
        "flask",
        "sentence-transformers", 
        "faiss-cpu",
        "PyPDF2",
        "python-docx",
        "transformers",
        "torch",
        "numpy",
        "scikit-learn",
        "google-generativeai"
    ]
    
    print("\n📦 Instalando dependencias...")
    
    for package in requirements:
        try:
            print(f"  Instalando {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True, check=True)
            print(f"  ✅ {package} instalado")
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️ Error instalando {package}: {e}")
            print(f"     Salida: {e.stdout}")
            print(f"     Error: {e.stderr}")

# ==========================================================
# 🔹 CREAR ESTRUCTURA DE DIRECTORIOS
# ==========================================================
def create_directory_structure():
    """Crea la estructura de directorios necesaria"""
    print("\n📁 Creando estructura de directorios...")
    
    directories = [
        "colaborative/data",
        "colaborative/data/pdfs/general",
        "colaborative/data/pdfs/civil", 
        "colaborative/data/index",
        "colaborative/data/logs",
        "colaborative/data/chunks",
        "colaborative/models/cache",
        "colaborative/models/huggingface",
        "colaborative/templates",
        "colaborative/static"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {dir_path}")

# ==========================================================
# 🔹 CREAR ARCHIVOS DE CONFIGURACIÓN
# ==========================================================
def create_config_files():
    """Crea archivos de configuración básicos"""
    print("\n⚙️ Creando archivos de configuración...")
    
    # 1. Archivo .env de ejemplo
    env_content = """# Configuración del Sistema RAG Enriquecido
# Copia este archivo como .env y configura tus claves

# Google Gemini API (opcional pero recomendado)
GOOGLE_API_KEY=tu_api_key_aqui

# HuggingFace Token (opcional)
HF_TOKEN=tu_hf_token_aqui

# Configuración del sistema
USE_GEMINI=True
FLASK_DEBUG=False
TOKENIZERS_PARALLELISM=false
"""
    
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_content)
    print("  ✅ .env.example creado")
    
    # 2. Archivo de configuración JSON
    config = {
        "system": {
            "name": "RAG Enriquecido con PCA",
            "version": "1.0.0",
            "description": "Sistema de Recuperación Aumentada con Perfiles Cognitivo-Autorales"
        },
        "models": {
            "embedding": "sentence-transformers/all-MiniLM-L6-v2",
            "generator_local": "google/flan-t5-base",
            "generator_cloud": "gemini-2.5-pro",
            "ner": "mrm8488/bert-spanish-cased-finetuned-ner"
        },
        "parameters": {
            "chunk_size": 800,
            "chunk_overlap": 100,
            "k_search_content": 5,
            "k_search_profiles": 6,
            "max_new_tokens": 256,
            "temperature": 0.1
        },
        "webapp": {
            "host": "127.0.0.1",
            "port": 5002,
            "debug": False
        }
    }
    
    with open("colaborative/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("  ✅ colaborative/config.json creado")

# ==========================================================
# 🔹 CREAR ARCHIVOS DE AYUDA
# ==========================================================
def create_help_files():
    """Crea archivos de documentación y ayuda"""
    print("\n📚 Creando documentación...")
    
    # README para PDFs
    readme_pdf = """INSTRUCCIONES PARA CARGAR DOCUMENTOS

1. ESTRUCTURA DE CARPETAS:
   - colaborative/data/pdfs/general/  → Documentos generales
   - colaborative/data/pdfs/civil/    → Documentos de derecho civil

2. FORMATO SOPORTADO:
   - Solo archivos PDF con texto extraíble
   - Evitar PDFs escaneados sin OCR

3. PROCESO DE INGESTA:
   a) Coloca archivos PDF en las carpetas correspondientes
   b) Ejecuta: python colaborative/scripts/ingesta_enriquecida.py
   c) El sistema procesará automáticamente todos los PDFs

4. QUÉ HACE LA INGESTA ENRIQUECIDA:
   - Extrae texto y estructura del documento
   - Analiza metodología jurídica y razonamiento
   - Detecta perfil cognitivo-autoral (marco, estrategia, autores)
   - Crea embeddings para búsqueda tradicional (FAISS_A)
   - Crea embeddings para perfiles cognitivos (FAISS_B)
   - Registra estadísticas en base de autoaprendizaje

5. VERIFICACIÓN:
   - Revisa logs en: colaborative/data/logs/
   - Consulta estadísticas en: http://127.0.0.1:5002/autoevaluaciones
"""
    
    with open("colaborative/data/pdfs/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_pdf)
    print("  ✅ colaborative/data/pdfs/README.txt")
    
    # Guía de uso rápido
    quick_start = """GUÍA DE USO RÁPIDO - RAG ENRIQUECIDO CON PCA

🔧 CONFIGURACIÓN INICIAL:
1. python setup_pca.py  (este archivo)
2. Configurar .env con tu GOOGLE_API_KEY (opcional)
3. Colocar PDFs en colaborative/data/pdfs/general/

🚀 EJECUTAR SISTEMA:
1. python colaborative/scripts/ingesta_enriquecida.py
2. python colaborative/scripts/end2end_webapp.py
3. Abrir: http://127.0.0.1:5002

🎯 FUNCIONALIDADES:
• Consultas doctrinarias con contexto cognitivo
• Autoaprendizaje continuo basado en evaluaciones
• Detección de marcos de referencia y estrategias
• Búsqueda por "gemelos cognitivos" similares
• Auditoría completa de procesos

🔍 RUTAS PRINCIPALES:
• /                    → Consultas doctrinarias
• /autoevaluaciones    → Historial de aprendizaje
• /refinamientos       → Historial de refinamientos

💡 MEJORAS INCLUIDAS:
1. Perfil Cognitivo-Autoral (PCA) en extracción
2. Base vectorial paralela (FAISS_B) para perfiles
3. Enriquecimiento de prompts con gemelos cognitivos
4. Registro completo en sistema de autoaprendizaje
"""
    
    with open("GUIA_RAPIDA.txt", "w", encoding="utf-8") as f:
        f.write(quick_start)
    print("  ✅ GUIA_RAPIDA.txt")

# ==========================================================
# 🔹 FUNCIÓN PRINCIPAL
# ==========================================================
def main():
    """Ejecuta la configuración completa"""
    
    # Verificaciones básicas
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    print("\n🎯 Iniciando configuración...")
    
    # Instalaciones y configuración
    install_requirements()
    create_directory_structure()
    create_config_files()
    create_help_files()
    
    # Mensaje final
    print("\n" + "=" * 60)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print()
    print("📋 PRÓXIMOS PASOS:")
    print("1. Configurar .env con tu GOOGLE_API_KEY (opcional)")
    print("2. Colocar PDFs en: colaborative/data/pdfs/general/")
    print("3. Ejecutar ingesta: python colaborative/scripts/ingesta_enriquecida.py")
    print("4. Iniciar webapp: python colaborative/scripts/end2end_webapp.py")
    print("5. Abrir navegador: http://127.0.0.1:5002")
    print()
    print("📚 Lee GUIA_RAPIDA.txt para más detalles")
    print("🔧 Configuración guardada en colaborative/config.json")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Configuración falló. Revisa los errores anteriores.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Configuración cancelada por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)