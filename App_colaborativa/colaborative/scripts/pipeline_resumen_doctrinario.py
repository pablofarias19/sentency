# -*- coding: utf-8 -*-
"""
Pipeline doctrinario-jurídico (mejorado)
- Recupera top-k chunks desde FAISS por base (general/civil/laboral/constitucional)
- Genera un concepto doctrinario coherente y técnico (modelo local o híbrido)
- Extrae entidades jurídicas (regex)
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
from pathlib import Path
import re
import pickle
import numpy as np
import faiss

# ====== Modelos locales (mismos paths que la webapp) ======
BASE_DIR = Path("colaborative")
DATA_DIR = BASE_DIR / "data"
INDEX_DIR = DATA_DIR / "index"
MODELS_DIR = BASE_DIR / "models"
EMBEDDINGS_PATH = MODELS_DIR / "embeddings" / "all-MiniLM-L6-v2"
GEN_PATH = MODELS_DIR / "generator" / "flan-t5-base"

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline as hf_pipeline

# ====== Estructura de datos ======
@dataclass
class DoctrinaRespuesta:
    pregunta: str
    concepto_consolidado: str
    citas: List[Dict]
    entidades: Dict
    fragmentos_usados: List[Dict]

# ====== Utilidades ======
def normalize_spanish(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())

def base_paths(base_name: str = "general") -> Tuple[Path, Path]:
    base_name = (base_name or "general").lower()
    idx_dir = INDEX_DIR / base_name
    idx_dir.mkdir(parents=True, exist_ok=True)
    return idx_dir / "vector_index.faiss", idx_dir / "metadata.pkl"

# ====== Carga perezosa ======
_embedder = None
_gen_pipe = None

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(str(EMBEDDINGS_PATH), local_files_only=True)
    return _embedder

def get_generator():
    global _gen_pipe
    if _gen_pipe is None:
        tok = AutoTokenizer.from_pretrained(str(GEN_PATH), local_files_only=True)
        mdl = AutoModelForSeq2SeqLM.from_pretrained(str(GEN_PATH), local_files_only=True)
        _gen_pipe = hf_pipeline("text2text-generation", model=mdl, tokenizer=tok)
    return _gen_pipe

# ====== Búsqueda RAG ======
def load_index_and_meta(base="general"):
    faiss_idx, meta_pkl = base_paths(base)
    if not faiss_idx.exists() or not meta_pkl.exists():
        raise FileNotFoundError(f"No existe índice/metadata para la base '{base}'. Ejecutá la ingesta.")
    index = faiss.read_index(str(faiss_idx))
    with open(meta_pkl, "rb") as f:
        meta = pickle.load(f)
    return index, meta["textos"], meta["fuentes"]

def embed_query(q: str) -> np.ndarray:
    return get_embedder().encode([q], convert_to_numpy=True)

def l2_to_score(d: float) -> float:
    return float(1.0 / (1.0 + np.sqrt(max(d, 0.0))))

def buscar(q: str, k:int=8, base:str="general"):
    idx, textos, fuentes = load_index_and_meta(base)
    v = embed_query(q)
    D, I = idx.search(v, k)
    out = []
    for d, i in zip(D[0], I[0]):
        if 0 <= i < len(textos):
            out.append({"idx": int(i), "dist": float(d), "texto": textos[i], "fuente": fuentes[i]})
    return out

def retrieve_top_chunks(query: str, k: int = 5, base: str = "general", min_score: float = 0.45):
    resultados = buscar(query, k, base)
    chunks = []
    for r in resultados:
        score = l2_to_score(r["dist"])
        if score >= min_score:
            chunks.append({
                "score": score,
                "dist": r["dist"],
                "fuente": r["fuente"],
                "chunk_id": r["idx"],
                "texto": normalize_spanish(r["texto"])[:700],  # limitar tamaño
                "metadata": {}
            })
    return chunks

# ====== Generación (Flan-T5 local o híbrido) ======
def llm_generate(system_prompt: str, user_prompt: str, temperature: float = 0.1, max_tokens: int = 420):
    gen = get_generator()
    prompt = f"{system_prompt}\n\n{user_prompt}"
    try:
        out = gen(prompt, max_length=max_tokens, do_sample=False)[0]["generated_text"]
    except Exception as e:
        out = f"[Error en generación doctrinaria: {e}]"
    return normalize_spanish(out)

# ====== NER (regex simple) ======
def ner_es(text: str) -> dict:
    leyes = re.findall(r"Ley\s+\d{4,6}", text, flags=re.IGNORECASE)
    articulos = re.findall(r"[Aa]rt[íi]culo\s+\d+[A-Za-z]?", text)
    constitucion = re.findall(r"[Cc]onstituci[oó]n\s+(?:Nacional|Provincial)", text)
    autores = re.findall(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+", text)
    obras = re.findall(r"['\"]([^'\"]+)['\"]", text)
    instituciones = re.findall(r"(?:C[oó]digo\s+[A-ZÁÉÍÓÚÑa-záéíóúñ]+)", text)
    return {
        "leyes": sorted(set(leyes)),
        "articulos": sorted(set(articulos)),
        "constitucion": sorted(set(constitucion)),
        "autores": list(dict.fromkeys(autores))[:10],
        "obras": list(dict.fromkeys(obras))[:10],
        "instituciones": sorted(set(instituciones)),
    }

def _construir_citas(chunks: List[dict]) -> List[dict]:
    return [{"fuente": c.get("fuente","s/d"), "chunk_id": c.get("chunk_id", 0)} for c in chunks]

def doctrina_respuesta_to_dict(obj: DoctrinaRespuesta) -> dict:
    return {
        "pregunta": obj.pregunta,
        "concepto_consolidado": obj.concepto_consolidado,
        "citas": obj.citas,
        "entidades": obj.entidades,
        "fragmentos_usados": obj.fragmentos_usados
    }

# ====== Prompts mejorados ======
_DOCTRINA_SYSTEM = (
    "Eres un jurista argentino experto en doctrina y jurisprudencia. "
    "Responde con precisión y lenguaje jurídico claro, "
    "basándote exclusivamente en los fragmentos doctrinarios provistos. "
    "No repitas instrucciones ni agregues comentarios fuera del análisis."
)

_DOCTRINA_USER_TPL = (
    "Consulta doctrinaria: {pregunta}\n\n"
    "Fragmentos relevantes:\n{base_texto}\n\n"
    "Elabora una respuesta doctrinaria breve (6–10 líneas), "
    "señalando criterios, excepciones y notas prácticas, "
    "manteniendo coherencia terminológica."
)

# ====== Pipeline principal ======
def run_doctrina_pipeline(pregunta: str, k: int = 3, base: str = "general") -> DoctrinaRespuesta:
    pregunta = normalize_spanish(pregunta)
    chunks = retrieve_top_chunks(pregunta, k=k, base=base)
    if not chunks:
        raise RuntimeError(f"No se recuperaron fragmentos relevantes (base='{base}'). Ingesta requerida o pregunta fuera de contexto.")

    # construir texto base acotado
    base_texto = "\n".join(
        f"- ({c['fuente']} #{c['chunk_id']}): {c['texto']}" for c in chunks
    )[:4000]  # limitar longitud total

    concepto = llm_generate(
        system_prompt=_DOCTRINA_SYSTEM,
        user_prompt=_DOCTRINA_USER_TPL.format(pregunta=pregunta, base_texto=base_texto),
        temperature=0.1,
        max_tokens=420
    )

    corpus = "\n".join([concepto] + [c["texto"] for c in chunks[:3]])
    entidades = ner_es(corpus)
    citas = _construir_citas(chunks[:3])

    return DoctrinaRespuesta(
        pregunta=pregunta,
        concepto_consolidado=concepto,
        citas=citas,
        entidades=entidades,
        fragmentos_usados=[
            {
                "fuente": c["fuente"],
                "chunk_id": c["chunk_id"],
                "score": c["score"],
                "dist": c["dist"],
                "resumen": c["texto"][:300]
            } for c in chunks
        ]
    )
