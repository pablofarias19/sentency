# -*- coding: utf-8 -*-
import json, hashlib, sqlite3
from pathlib import Path
from tqdm import tqdm
from config_rutas import (
    PENSAMIENTO_DB, META_SENTENCIAS_JSON,
    TXT_SENTENCIAS_DIR, PDF_SENTENCIAS_DIR
)
from utils_text_extractor import pdf_to_txt

CHUNK_TOKENS = 1000
STEP = 300

def sha1(s: str) -> str:
    import hashlib
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def simple_tokenize(text):
    return text.split()

def mk_chunks(text, chunk_tokens=CHUNK_TOKENS, step=STEP):
    toks = simple_tokenize(text)
    i = 0
    while i < len(toks):
        j = min(i + chunk_tokens, len(toks))
        yield " ".join(toks[i:j])
        if j == len(toks): break
        i += (chunk_tokens - step)

def ensure_tables(conn):
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS rag_sentencias_chunks (
      chunk_id TEXT PRIMARY KEY,
      expediente TEXT,
      fuente_pdf TEXT,
      fecha_sentencia TEXT,
      tribunal TEXT,
      jurisdiccion TEXT,
      materia TEXT,
      temas TEXT,
      formas_razonamiento TEXT,
      falacias TEXT,
      citaciones_doctrina TEXT,
      citaciones_jurisprudencia TEXT,
      texto TEXT,
      hash_texto TEXT
    )
    """)
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS rag_indices_meta (
      nombre_indice TEXT PRIMARY KEY,
      modelo TEXT,
      dimension INTEGER,
      total_chunks INTEGER,
      fecha_creacion TEXT
    )
    """)
    conn.commit()

def load_meta(path: Path):
    if not path.exists(): return {}
    return json.loads(path.read_text(encoding="utf-8"))

def load_or_extract_text(pdf_name: str) -> str:
    txt_path = TXT_SENTENCIAS_DIR / (Path(pdf_name).stem + ".txt")
    pdf_path = PDF_SENTENCIAS_DIR / pdf_name
    if txt_path.exists():
        return txt_path.read_text(encoding="utf-8", errors="ignore")
    if pdf_path.exists():
        pdf_to_txt(pdf_path, txt_path)
        return txt_path.read_text(encoding="utf-8", errors="ignore")
    return ""

def main():
    meta = load_meta(META_SENTENCIAS_JSON)
    conn = sqlite3.connect(PENSAMIENTO_DB)
    cur = conn.cursor()
    ensure_tables(conn)

    # Claves del JSON = nombre del PDF
    items = list(meta.items())
    print(f"🔍 Procesando {len(items)} sentencias...")
    
    for pdf_name, md in tqdm(items, desc="Ingesta de sentencias"):
        raw_text = load_or_extract_text(pdf_name)
        if not raw_text or len(raw_text) < 100:
            print(f"⚠️ Texto vacío o muy corto en: {pdf_name}")
            continue

        base_id = sha1(pdf_name)
        chunk_count = 0
        for k, chunk in enumerate(mk_chunks(raw_text)):
            chunk_id = f"{base_id}_{k:05d}"
            h = sha1(chunk)
            cur.execute("""
            INSERT OR REPLACE INTO rag_sentencias_chunks (
                chunk_id, expediente, fuente_pdf, fecha_sentencia, tribunal, jurisdiccion, materia,
                temas, formas_razonamiento, falacias, citaciones_doctrina, citaciones_jurisprudencia,
                texto, hash_texto
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chunk_id,
                md.get("numero_expediente"),
                pdf_name,
                md.get("fecha_sentencia"),
                md.get("tribunal"),
                md.get("jurisdiccion"),
                md.get("materia"),
                ", ".join(md.get("temas", [])),
                ", ".join(md.get("formas_razonamiento", [])),
                ", ".join(md.get("falacias", [])),
                json.dumps(md.get("citaciones", {}).get("doctrina", []), ensure_ascii=False),
                json.dumps(md.get("citaciones", {}).get("jurisprudencia", []), ensure_ascii=False),
                chunk,
                h
            ))
            chunk_count += 1

    conn.commit()
    conn.close()
    print("✅ Ingesta completada.")

if __name__ == "__main__":
    main()