#!/usr/bin/env python3
"""
Configuración Centralizada - Sistema Judicial Argentino
========================================================

Este archivo centraliza todas las rutas y configuraciones del sistema.
TODOS los scripts deben importar sus rutas desde aquí.

Versión: 1.0
Fecha: 2025-11-14
"""

from pathlib import Path
import os

# =============================================================================
# RUTAS BASE
# =============================================================================

# Ruta base absoluta del proyecto
BASE_DIR = Path(__file__).parent.resolve()

# =============================================================================
# BASE DE DATOS CENTRALIZADA
# =============================================================================

# BD CENTRAL - ÚNICA FUENTE DE VERDAD
# Todas las tablas judiciales están aquí:
# - sentencias_por_juez_arg
# - perfiles_judiciales_argentinos
# - perfiles_cognitivos
# - lineas_jurisprudenciales
# - redes_influencia_judicial
# - factores_predictivos
DATABASE_PATH = BASE_DIR / "judicial_system.db"

# =============================================================================
# DIRECTORIOS PRINCIPALES
# =============================================================================

# Directorio de datos
DATA_DIR = BASE_DIR / "data"

# Directorio de PDFs
PDF_DIR = DATA_DIR / "pdfs"
SENTENCIAS_PDF_DIR = PDF_DIR / "sentencias_pdf"

# Directorio de textos procesados
TXT_DIR = DATA_DIR / "txt"

# Directorio de chunks
CHUNKS_DIR = DATA_DIR / "chunks"

# Directorio de índices FAISS
INDEX_DIR = DATA_DIR / "index"

# Directorio de resultados
RESULTADOS_DIR = DATA_DIR / "resultados"

# Directorio de cache
CACHE_DIR = DATA_DIR / "cache_informes"

# Directorio de bases RAG (para embeddings y metadatos)
BASES_RAG_DIR = BASE_DIR / "bases_rag"
COGNITIVA_DIR = BASES_RAG_DIR / "cognitiva"

# =============================================================================
# MODELOS
# =============================================================================

MODELS_DIR = BASE_DIR / "models"

# Modelo de embeddings
EMBEDDINGS_PATH = MODELS_DIR / "embeddings" / "all-MiniLM-L6-v2"
EMBEDDINGS_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Modelo NER (Named Entity Recognition)
NER_PATH = MODELS_DIR / "ner" / "bert-spanish-cased-finetuned-ner"
NER_MODEL_NAME = "mrm8488/bert-spanish-cased-finetuned-ner"

# Modelo generador
GENERATOR_PATH = MODELS_DIR / "generator" / "flan-t5-base"
GENERATOR_MODEL_NAME = "google/flan-t5-base"

# Modelo generador cloud
GENERATOR_CLOUD_MODEL = "gemini-2.5-pro"

# =============================================================================
# LOGGING
# =============================================================================

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True, parents=True)

# =============================================================================
# PARÁMETROS DEL SISTEMA
# =============================================================================

# Chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
CHUNK_TOKENS = 1000
STEP_TOKENS = 300

# Búsqueda
K_SEARCH_CONTENT = 5
K_SEARCH_PROFILES = 6

# Generación
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.1

# =============================================================================
# WEBAPP
# =============================================================================

WEBAPP_HOST = "127.0.0.1"
WEBAPP_PORT = 5002
WEBAPP_DEBUG = False

# Plantillas
TEMPLATES_DIR = BASE_DIR / "templates"

# Prompts
PROMPTS_DIR = BASE_DIR / "prompts"

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def ensure_directories():
    """Crea todos los directorios necesarios si no existen"""
    directories = [
        DATA_DIR,
        PDF_DIR,
        SENTENCIAS_PDF_DIR,
        TXT_DIR,
        CHUNKS_DIR,
        INDEX_DIR,
        RESULTADOS_DIR,
        CACHE_DIR,
        BASES_RAG_DIR,
        COGNITIVA_DIR,
        MODELS_DIR,
        LOG_DIR,
        TEMPLATES_DIR,
        PROMPTS_DIR,
    ]

    for directory in directories:
        directory.mkdir(exist_ok=True, parents=True)

    print(f"✓ Directorios verificados/creados")


def get_db_connection():
    """
    Retorna una conexión a la base de datos centralizada

    Returns:
        sqlite3.Connection: Conexión a la BD centralizada
    """
    import sqlite3

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Base de datos centralizada no encontrada: {DATABASE_PATH}\n"
            f"Ejecute primero: python crear_bd_centralizada.py"
        )

    return sqlite3.connect(str(DATABASE_PATH))


def print_config():
    """Imprime la configuración actual del sistema"""
    print("=" * 80)
    print("CONFIGURACIÓN DEL SISTEMA JUDICIAL ARGENTINO")
    print("=" * 80)
    print(f"\nBASE_DIR:        {BASE_DIR}")
    print(f"DATABASE_PATH:   {DATABASE_PATH}")
    print(f"DATA_DIR:        {DATA_DIR}")
    print(f"MODELS_DIR:      {MODELS_DIR}")
    print(f"LOG_DIR:         {LOG_DIR}")
    print(f"\nEstado de BD:    {'✓ Existe' if DATABASE_PATH.exists() else '✗ No existe'}")
    print("=" * 80)


if __name__ == "__main__":
    # Si se ejecuta directamente, muestra la configuración
    print_config()
    ensure_directories()
