# -*- coding: utf-8 -*-
from pathlib import Path

# Bases de datos
PENSAMIENTO_DB = "colaborative/bases_rag/cognitiva/pensamiento_integrado_v2.db"
AUTOR_CENTRICO_DB = "colaborative/bases_rag/cognitiva/autor_centrico.db"

# Datos y artefactos
DATA_DIR = Path("colaborative/data/pdfs")
TXT_SENTENCIAS_DIR = DATA_DIR / "sentencias_texto"     # TXT pre-extraído (recomendado)
PDF_SENTENCIAS_DIR = DATA_DIR / "sentencias_pdf"       # PDFs originales
META_SENTENCIAS_JSON = DATA_DIR / "general" / "metadatos_sentencias.json"

# Índices FAISS
FAISS_IDX = "colaborative/bases_rag/cognitiva/faiss_sentencias.index"
FAISS_META = "colaborative/bases_rag/cognitiva/faiss_sentencias_meta.pkl"

# Modelo de embeddings (multilingüe sólido)
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

# --- DOCTRINA (nuevo v7.5) ---
DOCTRINA_PDF_DIR = Path("colaborative/data/pdfs/doctrina_pdf")
DOCTRINA_TXT_DIR = Path("colaborative/data/pdfs/doctrina_texto")  # TXT preextraído (recomendado)
DOCTRINA_META_JSON = Path("colaborative/data/pdfs/general/metadatos_doctrina.json")

DOCTRINA_VECTOR_NPY = "colaborative/bases_rag/cognitiva/vector_doctrina_base.npy"
DOCTRINA_FAISS_IDX = "colaborative/bases_rag/cognitiva/faiss_doctrina.index"
DOCTRINA_FAISS_META = "colaborative/bases_rag/cognitiva/faiss_doctrina_meta.pkl"