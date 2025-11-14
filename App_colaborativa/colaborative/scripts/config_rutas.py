# -*- coding: utf-8 -*-
"""
CONFIGURACIÓN DE RUTAS - SISTEMA JUDICIAL
==========================================

Este archivo mantiene compatibilidad con scripts antiguos mientras
usa la configuración centralizada en config.py

DEPRECADO: Use config.py directamente para nuevos desarrollos
"""

import sys
import os
from pathlib import Path

# Importar configuración centralizada
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import (
    DATABASE_PATH,
    BASE_DIR,
    DATA_DIR,
    PDF_DIR,
    SENTENCIAS_PDF_DIR,
    TXT_DIR,
    CHUNKS_DIR,
    BASES_RAG_DIR,
    COGNITIVA_DIR,
    EMBEDDINGS_MODEL_NAME,
    INDEX_DIR
)

# Bases de datos (ahora apunta a BD centralizada)
PENSAMIENTO_DB = str(DATABASE_PATH)  # BD centralizada
AUTOR_CENTRICO_DB = str(DATABASE_PATH)  # BD centralizada
DB_JUDICIAL = str(DATABASE_PATH)  # BD centralizada

# Datos y artefactos (usando config centralizado)
TXT_SENTENCIAS_DIR = TXT_DIR / "sentencias_texto"
PDF_SENTENCIAS_DIR = SENTENCIAS_PDF_DIR
META_SENTENCIAS_JSON = DATA_DIR / "general" / "metadatos_sentencias.json"

# Índices FAISS
FAISS_IDX = str(COGNITIVA_DIR / "faiss_sentencias.index")
FAISS_META = str(COGNITIVA_DIR / "faiss_sentencias_meta.pkl")

# Modelo de embeddings
EMBEDDING_MODEL = EMBEDDINGS_MODEL_NAME

# --- DOCTRINA ---
DOCTRINA_PDF_DIR = PDF_DIR / "doctrina_pdf"
DOCTRINA_TXT_DIR = PDF_DIR / "doctrina_texto"
DOCTRINA_META_JSON = DATA_DIR / "general" / "metadatos_doctrina.json"

DOCTRINA_VECTOR_NPY = str(COGNITIVA_DIR / "vector_doctrina_base.npy")
DOCTRINA_FAISS_IDX = str(COGNITIVA_DIR / "faiss_doctrina.index")
DOCTRINA_FAISS_META = str(COGNITIVA_DIR / "faiss_doctrina_meta.pkl")