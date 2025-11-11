# -*- coding: utf-8 -*-
import sqlite3, numpy as np, faiss, pickle, datetime
from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from config_rutas import PENSAMIENTO_DB, FAISS_IDX, FAISS_META, EMBEDDING_MODEL

def load_chunks():
    con = sqlite3.connect(PENSAMIENTO_DB)
    cur = con.cursor()
    cur.execute("SELECT chunk_id, texto FROM rag_sentencias_chunks ORDER BY chunk_id")
    rows = cur.fetchall()
    con.close()
    return rows

def main():
    rows = load_chunks()
    if not rows:
        print("⚠️ No hay chunks en la base. Corré ingesta_sentencias.py primero.")
        return

    texts = [t for _, t in rows]
    ids = [i for i, _ in rows]

    print(f"📊 Procesando {len(texts)} chunks para embeddings...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    embs = model.encode(texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True)
    embs = np.asarray(embs, dtype="float32")

    dim = embs.shape[1]
    print(f"🔧 Construyendo índice FAISS (dimensión: {dim})...")
    index = faiss.IndexFlatIP(dim)
    index.add(embs)

    # Crear directorios si no existen
    Path(FAISS_IDX).parent.mkdir(parents=True, exist_ok=True)
    Path(FAISS_META).parent.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, FAISS_IDX)
    with open(FAISS_META, "wb") as f:
        pickle.dump({
            "ids": ids,
            "modelo": EMBEDDING_MODEL,
            "dimension": dim,
            "total_chunks": len(ids),
            "fecha_creacion": datetime.datetime.now().isoformat(timespec="seconds")
        }, f)
    print(f"✅ FAISS listo: {len(ids)} chunks, dim={dim}, modelo={EMBEDDING_MODEL}")

if __name__ == "__main__":
    main()