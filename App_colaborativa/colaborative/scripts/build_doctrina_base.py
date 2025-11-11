# -*- coding: utf-8 -*-
"""
🏛️ CONSTRUCCIÓN DE BASE DOCTRINAL - V7.5
===============================================

Construye el vector doctrinal base y el índice FAISS para:
- Calcular distancia de sentencias a la doctrina consolidada
- Detectar apartamientos significativos del corpus doctrinal
- Proporcionar contexto doctrinal relevante

AUTOR: Sistema Cognitivo v7.5
FECHA: 10 NOV 2025
"""

import json
import pickle
import numpy as np
import faiss
from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from config_rutas import (
    EMBEDDING_MODEL,
    DOCTRINA_TXT_DIR, DOCTRINA_PDF_DIR, DOCTRINA_META_JSON,
    DOCTRINA_VECTOR_NPY, DOCTRINA_FAISS_IDX, DOCTRINA_FAISS_META
)
from utils_text_extractor import pdf_to_txt

CHUNK_TOKENS = 800
STEP = 250

def simple_tokenize(text): 
    """Tokenización simple por espacios"""
    return text.split()

def mk_chunks(text, chunk_tokens=CHUNK_TOKENS, step=STEP):
    """Genera chunks con solapamiento"""
    toks = simple_tokenize(text)
    i = 0
    while i < len(toks):
        j = min(i + chunk_tokens, len(toks))
        yield " ".join(toks[i:j])
        if j == len(toks): 
            break
        i += (chunk_tokens - step)

def load_or_extract_txt():
    """Carga textos de doctrina desde TXT o extrae de PDF"""
    DOCTRINA_TXT_DIR.mkdir(parents=True, exist_ok=True)
    DOCTRINA_PDF_DIR.mkdir(parents=True, exist_ok=True)
    
    txt_files = list(DOCTRINA_TXT_DIR.glob("*.txt"))
    
    if not txt_files:
        print("📄 No hay archivos TXT, buscando PDFs para extraer...")
        pdf_files = list(DOCTRINA_PDF_DIR.glob("*.pdf"))
        
        if pdf_files:
            print(f"🔄 Extrayendo texto de {len(pdf_files)} PDFs...")
            for pdf in tqdm(pdf_files, desc="Extrayendo PDFs"):
                try:
                    output_txt = DOCTRINA_TXT_DIR / (pdf.stem + ".txt")
                    pdf_to_txt(pdf, output_txt)
                except Exception as e:
                    print(f"⚠️ Error extrayendo {pdf.name}: {e}")
            
            txt_files = list(DOCTRINA_TXT_DIR.glob("*.txt"))
        else:
            print("📁 Creando directorios de ejemplo...")
            print(f"   - {DOCTRINA_PDF_DIR}")
            print(f"   - {DOCTRINA_TXT_DIR}")
    
    return txt_files

def main():
    """Proceso principal de construcción de base doctrinal"""
    print("🏛️ CONSTRUCCIÓN DE BASE DOCTRINAL V7.5")
    print("=" * 50)
    
    # Inicializar modelo
    print(f"🤖 Cargando modelo: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Cargar textos doctrinales
    txt_files = load_or_extract_txt()
    
    if not txt_files:
        print("⚠️ No hay doctrina (TXT o PDF). Pasos:")
        print("   1. Colocá archivos PDF en: colaborative/data/pdfs/doctrina_pdf/")
        print("   2. O archivos TXT en: colaborative/data/pdfs/doctrina_texto/")
        print("   3. Ejecutá nuevamente este script")
        return

    print(f"📚 Procesando {len(txt_files)} archivos doctrinales...")
    
    all_vectors = []
    ids = []
    textos = []
    metadatos = []

    # Procesar cada archivo
    for t in tqdm(txt_files, desc="Doctrina: chunking+embeddings"):
        try:
            raw = t.read_text(encoding="utf-8", errors="ignore")
            
            if not raw.strip():
                print(f"⚠️ Archivo vacío: {t.name}")
                continue
                
            chunk_count = 0
            for k, chunk in enumerate(mk_chunks(raw)):
                if len(chunk.strip()) < 50:  # Filtrar chunks muy pequeños
                    continue
                    
                textos.append(chunk)
                chunk_id = f"{t.stem}_{k:05d}"
                ids.append(chunk_id)
                
                # Metadatos básicos
                metadatos.append({
                    "archivo": t.name,
                    "chunk_id": chunk_id,
                    "chunk_index": k,
                    "longitud": len(chunk),
                    "tokens_aprox": len(simple_tokenize(chunk))
                })
                chunk_count += 1
            
            print(f"  📖 {t.name}: {chunk_count} chunks")
            
        except Exception as e:
            print(f"❌ Error procesando {t.name}: {e}")

    if not textos:
        print("⚠️ Doctrina vacía después del procesamiento.")
        return

    print(f"🔢 Total chunks procesados: {len(textos)}")
    
    # Generar embeddings
    print("🧠 Generando embeddings...")
    embs = model.encode(
        textos, 
        batch_size=64, 
        show_progress_bar=True, 
        normalize_embeddings=True
    )
    embs = np.asarray(embs, dtype="float32")
    all_vectors = embs

    # Calcular vector doctrinal base (promedio)
    print("📊 Calculando vector doctrinal base...")
    doctrinal_mean = np.mean(all_vectors, axis=0, dtype=np.float32)
    
    # Normalizar para usar similitud coseno
    norm = np.linalg.norm(doctrinal_mean)
    if norm > 1e-9:
        doctrinal_mean /= norm
    
    # Guardar vector base
    Path(DOCTRINA_VECTOR_NPY).parent.mkdir(parents=True, exist_ok=True)
    np.save(DOCTRINA_VECTOR_NPY, doctrinal_mean)
    print(f"✅ Vector doctrinal base guardado → {DOCTRINA_VECTOR_NPY}")

    # Crear índice FAISS para recuperación
    print("🔍 Construyendo índice FAISS...")
    dim = all_vectors.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner Product para coseno normalizado
    index.add(all_vectors)
    
    # Guardar índice FAISS
    Path(DOCTRINA_FAISS_IDX).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, DOCTRINA_FAISS_IDX)
    
    # Guardar metadatos del índice
    metadata_index = {
        "ids": ids,
        "metadatos": metadatos,
        "total_chunks": len(ids),
        "total_archivos": len(txt_files),
        "embedding_model": EMBEDDING_MODEL,
        "fecha_construccion": str(Path(__file__).stat().st_mtime)
    }
    
    with open(DOCTRINA_FAISS_META, "wb") as f:
        pickle.dump(metadata_index, f)
    
    print(f"✅ Índice FAISS doctrina listo: {len(ids)} chunks")
    print(f"   📄 Archivos procesados: {len(txt_files)}")
    print(f"   🔍 Índice: {DOCTRINA_FAISS_IDX}")
    print(f"   📋 Metadatos: {DOCTRINA_FAISS_META}")
    
    # Guardar estadísticas en JSON
    stats = {
        "total_chunks": len(ids),
        "total_archivos": len(txt_files),
        "promedio_chunks_por_archivo": len(ids) / len(txt_files) if txt_files else 0,
        "dimension_embeddings": dim,
        "modelo_utilizado": EMBEDDING_MODEL,
        "archivos_procesados": [t.name for t in txt_files]
    }
    
    stats_path = Path(DOCTRINA_META_JSON)
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Estadísticas guardadas: {stats_path}")
    print("\n🎉 ¡Base doctrinal construida exitosamente!")

if __name__ == "__main__":
    main()