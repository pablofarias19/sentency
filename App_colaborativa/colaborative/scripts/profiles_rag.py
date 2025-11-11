# -*- coding: utf-8 -*-
"""
PCA: RAG de Perfiles Cognitivo-Autoral (FAISS_B)
Sistema de búsqueda vectorial de "firmas intelectuales" y gemelos cognitivos.
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import numpy as np

# Imports con manejo de errores
try:
    from sentence_transformers import SentenceTransformer
    import faiss
except ImportError as e:
    print(f"⚠️ Error importing dependencies: {e}")
    print("Instala con: pip install sentence-transformers faiss-cpu")
    raise

# ==========================================================
# 🔹 CONFIGURACIÓN
# ==========================================================
DB_PROFILES = "colaborative/data/perfiles.db"
INDEX_PROFILES = "colaborative/data/faiss_profiles.index"
META_PROFILES = "colaborative/data/faiss_profiles_meta.json"
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Modelo compatible con tu sistema

# Crear directorio si no existe
os.makedirs("colaborative/data", exist_ok=True)

# ==========================================================
# 🔹 BASE DE DATOS DE PERFILES
# ==========================================================
def init_db_profiles():
    """Inicializa la base de datos de perfiles cognitivos"""
    conn = sqlite3.connect(DB_PROFILES)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS perfiles_cognitivos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      doc_hash TEXT NOT NULL,
      doc_titulo TEXT,
      autor_detectado TEXT,
      nivel TEXT NOT NULL,           -- 'seccion' | 'documento' | 'autor'
      perfil_json TEXT NOT NULL,     -- dict cognitivo serializado
      firma TEXT NOT NULL,           -- string canónico para embedding
      fecha_registro TEXT NOT NULL,
      UNIQUE(doc_hash, nivel, firma)  -- Evitar duplicados
    )
    """)
    
    # Índices para búsquedas eficientes
    c.execute("CREATE INDEX IF NOT EXISTS idx_doc_hash ON perfiles_cognitivos(doc_hash)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_nivel ON perfiles_cognitivos(nivel)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_autor ON perfiles_cognitivos(autor_detectado)")
    
    conn.commit()
    conn.close()

# ==========================================================
# 🔹 FAISS_B: ÍNDICE VECTORIAL DE PERFILES
# ==========================================================
def _load_index(dim: int) -> faiss.IndexFlatIP:
    """Carga o crea el índice FAISS de perfiles"""
    if not os.path.exists(INDEX_PROFILES):
        # Crear índice nuevo (similitud coseno con vectores normalizados)
        index = faiss.IndexFlatIP(dim)
        faiss.write_index(index, INDEX_PROFILES)
        return index
    return faiss.read_index(INDEX_PROFILES)

def _save_index(index):
    """Guarda el índice FAISS"""
    faiss.write_index(index, INDEX_PROFILES)

def _load_metadata() -> List[Dict]:
    """Carga metadatos de vectores"""
    if os.path.exists(META_PROFILES):
        try:
            with open(META_PROFILES, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def _save_metadata(meta: List[Dict]):
    """Guarda metadatos de vectores"""
    with open(META_PROFILES, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

# ==========================================================
# 🔹 CLASE PRINCIPAL: ProfilesStore
# ==========================================================
class ProfilesStore:
    """
    Almacén de perfiles cognitivos con búsqueda vectorial.
    Permite encontrar 'gemelos cognitivos' para enriquecer prompts.
    """
    
    def __init__(self):
        print("🧠 Inicializando ProfilesStore...")
        
        # Cargar modelo de embeddings (mismo que RAG principal)
        try:
            self.model = SentenceTransformer(EMB_MODEL)
            self.dim = self.model.get_sentence_embedding_dimension()
            print(f"✅ Modelo cargado: {EMB_MODEL} (dim={self.dim})")
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            raise
        
        # Cargar índice FAISS
        self.index = _load_index(self.dim)
        self.meta = _load_metadata()
        
        print(f"📊 Perfiles cargados: {self.index.ntotal}")

    def _embed(self, texts: List[str]) -> np.ndarray:
        """Genera embeddings normalizados"""
        try:
            vecs = self.model.encode(
                texts, 
                normalize_embeddings=True, 
                show_progress_bar=False,
                convert_to_numpy=True
            )
            return np.array(vecs, dtype="float32")
        except Exception as e:
            print(f"❌ Error generando embeddings: {e}")
            raise

    def add_profiles(self, rows: List[Dict]):
        """
        Añade perfiles al almacén vectorial.
        
        Args:
            rows: Lista de diccionarios con:
                - firma: str (texto canónico para embedding)
                - doc_hash: str
                - doc_titulo: str
                - autor_detectado: str
                - nivel: str ('seccion'|'documento'|'autor')
                - perfil_json: dict (perfil cognitivo)
        """
        if not rows:
            return
        
        print(f"📥 Añadiendo {len(rows)} perfiles...")
        
        # Inicializar BD
        init_db_profiles()
        
        # Generar embeddings
        firmas = [r["firma"] for r in rows]
        try:
            vecs = self._embed(firmas)
        except Exception as e:
            print(f"❌ Error generando embeddings: {e}")
            return
        
        # Añadir a FAISS
        self.index.add(vecs)
        
        # Guardar en BD SQLite
        conn = sqlite3.connect(DB_PROFILES)
        c = conn.cursor()
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for i, r in enumerate(rows):
            try:
                c.execute("""INSERT OR IGNORE INTO perfiles_cognitivos
                (doc_hash, doc_titulo, autor_detectado, nivel, perfil_json, firma, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    r["doc_hash"], 
                    r["doc_titulo"], 
                    r.get("autor_detectado", "No identificado"),
                    r["nivel"], 
                    json.dumps(r["perfil_json"], ensure_ascii=False),
                    r["firma"], 
                    created
                ))
                
                # Actualizar metadatos para FAISS
                self.meta.append({
                    "id": len(self.meta),
                    "doc_hash": r["doc_hash"],
                    "doc_titulo": r["doc_titulo"],
                    "autor_detectado": r.get("autor_detectado", "No identificado"),
                    "nivel": r["nivel"],
                    "firma": r["firma"],
                    "fecha_registro": created
                })
                
            except sqlite3.IntegrityError:
                print(f"⚠️ Perfil duplicado ignorado: {r['doc_hash']}")
                continue
        
        conn.commit()
        conn.close()
        
        # Guardar índice y metadatos
        _save_index(self.index)
        _save_metadata(self.meta)
        
        print(f"✅ {len(rows)} perfiles añadidos. Total: {self.index.ntotal}")

    def search_profiles(self, query_firma: str, k: int = 8) -> List[Tuple[float, Dict]]:
        """
        Busca perfiles similares (gemelos cognitivos).
        
        Args:
            query_firma: Firma de consulta
            k: Número de vecinos a retornar
            
        Returns:
            Lista de (score, metadata) ordenada por similitud
        """
        if self.index.ntotal == 0:
            return []
        
        try:
            # Generar embedding de consulta
            qv = self._embed([query_firma])
            
            # Búsqueda en FAISS
            D, I = self.index.search(qv, min(k, self.index.ntotal))
            
            # Construir resultados
            results = []
            for score, idx in zip(D[0], I[0]):
                if idx < 0 or idx >= len(self.meta):
                    continue
                results.append((float(score), self.meta[idx]))
            
            return results
            
        except Exception as e:
            print(f"❌ Error en búsqueda de perfiles: {e}")
            return []

    def get_stats(self) -> Dict:
        """Retorna estadísticas del almacén"""
        return {
            "total_perfiles": self.index.ntotal,
            "dimension": self.dim,
            "modelo": EMB_MODEL,
            "metadatos": len(self.meta)
        }

# ==========================================================
# 🔹 UTILIDADES DE FIRMA COGNITIVA
# ==========================================================
def build_firma(perfil: Dict, meta_doc: Dict, titulo_seccion: str = "", palabras_clave: List[str] = None) -> str:
    """
    Construye una 'firma cognitiva' canónica para embedding.
    Combina elementos del perfil cognitivo-autoral con metadatos documentales.
    """
    if palabras_clave is None:
        palabras_clave = []
    
    # Extraer elementos del perfil
    marco = perfil.get("marco_referencia", "No identificado")
    estrat = perfil.get("estrategia", "No determinada")
    motivo = perfil.get("motivo_intelectual", "No identificado")
    
    # Listas como strings
    crit = ", ".join(sorted(set(perfil.get("critica_a", [])))) or "Ninguna"
    autores = ", ".join(sorted(set(perfil.get("autores_mencionados", [])))) or "Sin autores"
    topicos = ", ".join(sorted(set(palabras_clave))) or "Sin tópicos"
    
    # Construir firma estructurada
    firma = (
        f"MARCO:{marco} | ESTRATEGIA:{estrat} | MOTIVO:{motivo} | "
        f"CRITICA:{crit} | AUTORES:{autores} | TOPICOS:{topicos} | "
        f"SECCION:{titulo_seccion} | FUENTE:{meta_doc.get('titulo', 'Sin título')} | "
        f"AUTOR:{meta_doc.get('autor', 'Sin autor')} | ANIO:{meta_doc.get('anio', 'Sin año')}"
    )
    
    return firma

# ==========================================================
# 🔹 ENRIQUECEDOR DE PROMPTS
# ==========================================================
def enrich_prompt_with_profiles(pregunta: str, base_titulo: str = "Base General", k: int = 5) -> str:
    """
    Enriquece un prompt con contexto de 'gemelos cognitivos'.
    
    Args:
        pregunta: Consulta del usuario
        base_titulo: Título de la base de conocimiento
        k: Número de perfiles afines a buscar
        
    Returns:
        Contexto cognitivo formateado para injection en prompt
    """
    try:
        store = ProfilesStore()
        
        # Construir firma de consulta
        query_firma = f"CONSULTA:{pregunta} | FUENTE:{base_titulo}"
        
        # Buscar vecinos cognitivos
        vecinos = store.search_profiles(query_firma, k=k)
        
        if not vecinos:
            return "Sin contexto cognitivo previo disponible."
        
        # Formatear contexto
        resumen = "🧠 CONTEXTO COGNITIVO (Perfiles más afines):\n"
        
        for i, (score, meta) in enumerate(vecinos, 1):
            autor = meta.get('autor_detectado', 'Sin autor')
            titulo = meta.get('doc_titulo', 'Sin título')[:50]
            nivel = meta.get('nivel', 'desconocido')
            
            resumen += f"{i}. {autor} — {titulo}... [{nivel}] (sim:{score:.3f})\n"
        
        resumen += "\n💡 INDICACIÓN: Mantener coherencia con marcos y estrategias detectados.\n"
        return resumen
        
    except Exception as e:
        print(f"❌ Error enriqueciendo prompt: {e}")
        return "Error recuperando contexto cognitivo."

# ==========================================================
# 🔹 FUNCIONES DE AUDITORÍA
# ==========================================================
def listar_perfiles(limite: int = 20) -> List[Dict]:
    """Lista perfiles almacenados para auditoría"""
    init_db_profiles()
    conn = sqlite3.connect(DB_PROFILES)
    c = conn.cursor()
    
    c.execute("""
        SELECT doc_titulo, autor_detectado, nivel, perfil_json, fecha_registro 
        FROM perfiles_cognitivos 
        ORDER BY fecha_registro DESC 
        LIMIT ?
    """, (limite,))
    
    results = []
    for row in c.fetchall():
        try:
            perfil = json.loads(row[3])
            results.append({
                "titulo": row[0],
                "autor": row[1],
                "nivel": row[2],
                "perfil": perfil,
                "fecha": row[4]
            })
        except:
            continue
    
    conn.close()
    return results

def buscar_por_autor(autor: str) -> List[Dict]:
    """Busca perfiles por autor específico"""
    init_db_profiles()
    conn = sqlite3.connect(DB_PROFILES)
    c = conn.cursor()
    
    c.execute("""
        SELECT doc_titulo, perfil_json, firma
        FROM perfiles_cognitivos 
        WHERE autor_detectado LIKE ?
        ORDER BY fecha_registro DESC
    """, (f"%{autor}%",))
    
    results = []
    for row in c.fetchall():
        try:
            results.append({
                "titulo": row[0],
                "perfil": json.loads(row[1]),
                "firma": row[2]
            })
        except:
            continue
    
    conn.close()
    return results

def obtener_perfiles_recientes(limite: int = 20) -> List[Dict]:
    """Obtiene perfiles recientes con todos los campos para la tabla HTML"""
    init_db_profiles()
    conn = sqlite3.connect(DB_PROFILES)
    c = conn.cursor()
    
    c.execute("""
        SELECT 
            fecha_registro,
            doc_titulo,
            autor_detectado,
            modalidad_epistemica,
            estructura_silogistica,
            nivel
        FROM perfiles_cognitivos 
        ORDER BY fecha_registro DESC 
        LIMIT ?
    """, (limite,))
    
    results = []
    for row in c.fetchall():
        results.append({
            "fecha": row[0],
            "titulo": row[1],
            "autor": row[2],
            "modalidad_epistemica": row[3],
            "estructura_silogistica": row[4],
            "nivel": row[5]
        })
    
    conn.close()
    return results

# ==========================================================
# 🔹 FUNCIÓN DE PRUEBA
# ==========================================================
if __name__ == "__main__":
    print("🧠 Probando ProfilesStore...")
    
    # Crear instancia
    store = ProfilesStore()
    print(f"📊 Stats: {store.get_stats()}")
    
    # Datos de prueba
    test_profiles = [
        {
            "firma": "MARCO:Jurídico | ESTRATEGIA:Analítica | CONSULTA:derecho civil | AUTOR:Alterini",
            "doc_hash": "test123",
            "doc_titulo": "Derecho de Obligaciones",
            "autor_detectado": "Alterini",
            "nivel": "seccion",
            "perfil_json": {
                "marco_referencia": "Jurídico / Dogmático",
                "estrategia": "Analítica",
                "autores_mencionados": ["Alterini", "López"]
            }
        }
    ]
    
    # Añadir perfiles de prueba
    store.add_profiles(test_profiles)
    
    # Buscar
    consulta = "¿Qué es una obligación en derecho civil?"
    contexto = enrich_prompt_with_profiles(consulta, "Base Civil")
    print(f"\n🔍 Consulta: {consulta}")
    print(f"📝 Contexto generado:\n{contexto}")
    
    print("\n✅ Prueba completada.")