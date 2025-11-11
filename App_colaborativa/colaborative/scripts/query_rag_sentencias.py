# -*- coding: utf-8 -*-
import sqlite3, numpy as np, faiss, pickle, json
from sentence_transformers import SentenceTransformer
from config_rutas import PENSAMIENTO_DB, FAISS_IDX, FAISS_META, EMBEDDING_MODEL

def faiss_search(query, topk=30):
    model = SentenceTransformer(EMBEDDING_MODEL)
    q = model.encode([query], normalize_embeddings=True)
    index = faiss.read_index(FAISS_IDX)
    D, I = index.search(np.array(q, dtype="float32"), topk)
    with open(FAISS_META, "rb") as f:
        meta = pickle.load(f)
    ids = [meta["ids"][int(i)] for i in I[0]]
    return ids, D[0].tolist()

def fetch_chunks(ids, filtros=None):
    con = sqlite3.connect(PENSAMIENTO_DB)
    cur = con.cursor()
    if not ids: return []
    placeholders = ",".join(["?"]*len(ids))
    cur.execute(f"""
      SELECT chunk_id, expediente, fuente_pdf, fecha_sentencia, tribunal, jurisdiccion,
             materia, temas, formas_razonamiento, falacias,
             citaciones_doctrina, citaciones_jurisprudencia, texto,
             distancia_doctrinal
      FROM rag_sentencias_chunks
      WHERE chunk_id IN ({placeholders})
    """, ids)
    rows = cur.fetchall()
    con.close()

    if filtros:
        def ok(r):
            m = True
            if filtros.get("tema"):
                m &= (filtros["tema"].lower() in (r[7] or "").lower())
            if filtros.get("falacia"):
                m &= (filtros["falacia"].lower() in (r[9] or "").lower())
            if filtros.get("razonamiento"):
                m &= (filtros["razonamiento"].lower() in (r[8] or "").lower())
            if filtros.get("tribunal"):
                m &= (filtros["tribunal"].lower() in (r[4] or "").lower())
            if filtros.get("desde") and filtros.get("hasta"):
                f = (r[3] or "")
                m &= (f >= filtros["desde"] and f <= filtros["hasta"])
            return m
        rows = [r for r in rows if ok(r)]
    return rows

def buscar(query, filtros=None, topk=30):
    ids, _ = faiss_search(query, topk=topk)
    rows = fetch_chunks(ids, filtros=filtros)

    # re-rank simple: boosts por coincidencia en metadatos
    scored = []
    for r in rows:
        boost = 0.0
        if filtros:
            if filtros.get("tema") and (filtros["tema"].lower() in (r[7] or "").lower()):
                boost += 0.2
            if filtros.get("falacia") and (filtros["falacia"].lower() in (r[9] or "").lower()):
                boost += 0.2
            if filtros.get("razonamiento") and (filtros["razonamiento"].lower() in (r[8] or "").lower()):
                boost += 0.2
        scored.append((boost, r))
    scored.sort(key=lambda x: -x[0])
    return scored

if __name__ == "__main__":
    # Ejemplo
    filtros = {"falacia": "non sequitur", "razonamiento": "analógico", "desde":"2020-01-01", "hasta":"2025-12-31"}
    res = buscar("límite racional intereses moratorios punitorios", filtros=filtros, topk=60)
    print(f"🔍 Encontrados {len(res)} resultados")
    for boost, r in res[:8]:
        dist_doc = r[13] if r[13] is not None else "N/A"
        print(f"[{r[0]}] {r[1]} {r[3]} {r[4]} | temas={r[7]} | raz={r[8]} | falacias={r[9]} | dist_doc={dist_doc} | boost={boost:.2f}")
        print(f"   Texto: {(r[12][:200] + '...' if len(r[12]) > 200 else r[12])}")
        print()