# -*- coding: utf-8 -*-
"""
📏 ACTUALIZACIÓN DE DISTANCIAS DOCTRINALES - V7.5
================================================

Recalcula la distancia doctrinal de todos los chunks de sentencias
respecto al vector base de la doctrina consolidada.

Distancia = 1 - similitud_coseno
- 0.0 = Perfectamente alineado con doctrina
- 1.0 = Completamente apartado de doctrina

AUTOR: Sistema Cognitivo v7.5
FECHA: 10 NOV 2025
"""

import sqlite3
import numpy as np
from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from config_rutas import PENSAMIENTO_DB, EMBEDDING_MODEL, DOCTRINA_VECTOR_NPY

def ensure_column(conn):
    """Asegura que existe la columna distancia_doctrinal"""
    cur = conn.cursor()
    try:
        cur.execute("SELECT distancia_doctrinal FROM rag_sentencias_chunks LIMIT 1")
        print("✅ Columna distancia_doctrinal ya existe")
    except sqlite3.OperationalError:
        print("🔧 Agregando columna distancia_doctrinal...")
        cur.execute("ALTER TABLE rag_sentencias_chunks ADD COLUMN distancia_doctrinal REAL")
        conn.commit()
        print("✅ Columna distancia_doctrinal agregada")

def verificar_base_doctrinal():
    """Verifica que existe el vector base doctrinal"""
    if not Path(DOCTRINA_VECTOR_NPY).exists():
        print(f"❌ Vector doctrinal base no encontrado: {DOCTRINA_VECTOR_NPY}")
        print("📋 Ejecutá primero: python build_doctrina_base.py")
        return False
    
    print(f"✅ Vector doctrinal encontrado: {DOCTRINA_VECTOR_NPY}")
    return True

def main():
    """Proceso principal de actualización de distancias"""
    print("📏 ACTUALIZACIÓN DE DISTANCIAS DOCTRINALES V7.5")
    print("=" * 55)
    
    # Verificar prerrequisitos
    if not verificar_base_doctrinal():
        return
    
    if not Path(PENSAMIENTO_DB).exists():
        print(f"❌ Base de datos no encontrada: {PENSAMIENTO_DB}")
        print("📋 Ejecutá primero la ingesta de sentencias")
        return
    
    # Cargar vector doctrinal base
    print("📚 Cargando vector doctrinal base...")
    try:
        doctrinal_vec = np.load(DOCTRINA_VECTOR_NPY).astype("float32")
        print(f"   Dimensión: {doctrinal_vec.shape}")
        
        # Verificar normalización
        norm = np.linalg.norm(doctrinal_vec)
        print(f"   Norma: {norm:.6f}")
        
        if abs(norm - 1.0) > 0.01:
            print("⚠️ Vector no normalizado, normalizando...")
            doctrinal_vec /= (norm + 1e-9)
            
    except Exception as e:
        print(f"❌ Error cargando vector doctrinal: {e}")
        return
    
    # Cargar modelo de embeddings
    print(f"🤖 Cargando modelo: {EMBEDDING_MODEL}")
    try:
        model = SentenceTransformer(EMBEDDING_MODEL)
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return
    
    # Conectar a base de datos
    print("🗃️ Conectando a base de datos...")
    try:
        con = sqlite3.connect(PENSAMIENTO_DB)
        ensure_column(con)
        cur = con.cursor()
        
        # Obtener estadísticas
        cur.execute("SELECT COUNT(*) FROM rag_sentencias_chunks")
        total_chunks = cur.fetchone()[0]
        print(f"   Total chunks en BD: {total_chunks}")
        
        if total_chunks == 0:
            print("⚠️ No hay chunks de sentencias en la base de datos")
            con.close()
            return
            
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        return
    
    # Procesar chunks en lotes para eficiencia
    print("🔄 Calculando distancias doctrinales...")
    
    batch_size = 100
    processed = 0
    updated = 0
    errors = 0
    
    try:
        # Procesar por lotes
        cur.execute("SELECT chunk_id, texto FROM rag_sentencias_chunks ORDER BY chunk_id")
        
        while True:
            rows = cur.fetchmany(batch_size)
            if not rows:
                break
            
            # Preparar textos para embedding
            chunk_ids = []
            textos = []
            
            for chunk_id, texto in rows:
                chunk_ids.append(chunk_id)
                textos.append(texto if texto else "")
            
            try:
                # Generar embeddings del lote
                if textos:
                    embeddings = model.encode(
                        textos, 
                        normalize_embeddings=True,
                        show_progress_bar=False
                    ).astype("float32")
                    
                    # Calcular distancias
                    for i, (chunk_id, emb) in enumerate(zip(chunk_ids, embeddings)):
                        try:
                            if len(textos[i].strip()) < 10:  # Texto muy corto
                                dist = None
                            else:
                                # Similitud coseno
                                cos_sim = float(np.dot(emb, doctrinal_vec))
                                # Distancia = 1 - similitud
                                dist = float(1.0 - cos_sim)
                                
                                # Clamp entre 0 y 1
                                dist = max(0.0, min(1.0, dist))
                            
                            # Actualizar en BD
                            cur.execute(
                                "UPDATE rag_sentencias_chunks SET distancia_doctrinal=? WHERE chunk_id=?",
                                (dist, chunk_id)
                            )
                            updated += 1
                            
                        except Exception as e:
                            print(f"⚠️ Error procesando chunk {chunk_id}: {e}")
                            errors += 1
                            
                    processed += len(rows)
                    
                    # Mostrar progreso
                    if processed % 500 == 0:
                        print(f"   Procesados: {processed}/{total_chunks} ({processed/total_chunks*100:.1f}%)")
                        con.commit()  # Commit intermedio
                        
            except Exception as e:
                print(f"❌ Error procesando lote: {e}")
                errors += len(rows)
                processed += len(rows)
        
        # Commit final
        con.commit()
        
        # Estadísticas finales
        print(f"\n📊 ESTADÍSTICAS FINALES:")
        print(f"   Chunks procesados: {processed}")
        print(f"   Chunks actualizados: {updated}")
        print(f"   Errores: {errors}")
        
        # Obtener estadísticas de distancias
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                AVG(distancia_doctrinal) as promedio,
                MIN(distancia_doctrinal) as minima,
                MAX(distancia_doctrinal) as maxima,
                COUNT(CASE WHEN distancia_doctrinal <= 0.20 THEN 1 END) as alineados,
                COUNT(CASE WHEN distancia_doctrinal > 0.50 THEN 1 END) as apartados
            FROM rag_sentencias_chunks 
            WHERE distancia_doctrinal IS NOT NULL
        """)
        
        stats = cur.fetchone()
        if stats and stats[0] > 0:
            total, promedio, minima, maxima, alineados, apartados = stats
            print(f"\n📈 DISTRIBUCIÓN DE DISTANCIAS:")
            print(f"   Promedio: {promedio:.4f}")
            print(f"   Rango: {minima:.4f} - {maxima:.4f}")
            print(f"   🟢 Alineados (≤0.20): {alineados} ({alineados/total*100:.1f}%)")
            print(f"   🔴 Apartados (>0.50): {apartados} ({apartados/total*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error durante procesamiento: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        con.close()
        print("✅ Base de datos cerrada")
    
    if errors == 0:
        print("\n🎉 ¡Distancias doctrinales recalculadas exitosamente!")
    else:
        print(f"\n⚠️ Proceso completado con {errors} errores")

if __name__ == "__main__":
    main()