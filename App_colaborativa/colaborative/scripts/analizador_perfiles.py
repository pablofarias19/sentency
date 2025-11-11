# -*- coding: utf-8 -*-
"""
===========================================================
  MÓDULO DE ANÁLISIS DE PERFILES COGNITIVOS
===========================================================

Función:
    Permite cargar, comparar y buscar similitud entre los
    perfiles cognitivos vectorizados almacenados en la base
    /bases_rag/cognitiva/ (SQLite + FAISS).

Dependencias:
    pip install faiss-cpu numpy tabulate
===========================================================
"""

import os
import sqlite3
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from datetime import datetime
import json

# Imports con manejo de errores
try:
    import faiss
except ImportError:
    print("❌ Error: Instala FAISS con: pip install faiss-cpu")
    raise

try:
    from tabulate import tabulate
except ImportError:
    print("⚠️ Advertencia: tabulate no disponible. Instala con: pip install tabulate")
    def tabulate(data, headers=None, tablefmt="grid"):
        return str(data)  # Fallback simple

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("❌ Error: Instala sentence-transformers")
    raise

# ----------------------------------------------------------
# CONFIGURACIÓN DE RUTAS
# ----------------------------------------------------------
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"
FAISS_INDEX_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "faiss_index" / "cognitiva.idx"
FAISS_DIR = BASE_PATH / "bases_rag" / "cognitiva" / "faiss_index"

print(f"🔧 Configuración del analizador:")
print(f"  🗃️ DB: {DB_PATH}")
print(f"  📊 FAISS: {FAISS_INDEX_PATH}")

# ----------------------------------------------------------
# MODELO BASE (para búsqueda por texto)
# ----------------------------------------------------------
print("🔹 Cargando modelo de embeddings (all-mpnet-base-v2)...")
try:
    model = SentenceTransformer('all-mpnet-base-v2')
    print("✅ Modelo cargado exitosamente")
except Exception as e:
    print(f"❌ Error cargando modelo: {e}")
    model = None

# ----------------------------------------------------------
# FUNCIONES DE CARGA Y GESTIÓN DE VECTORES
# ----------------------------------------------------------
def verificar_base_datos() -> bool:
    """Verifica si la base de datos existe y tiene datos"""
    if not DB_PATH.exists():
        print(f"❌ Base de datos no encontrada: {DB_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count == 0:
            print("⚠️ Base de datos vacía. Registra perfiles primero.")
            return False
        
        print(f"✅ Base de datos encontrada con {count} perfiles")
        return True
        
    except Exception as e:
        print(f"❌ Error accediendo a la base de datos: {e}")
        return False

def cargar_vectores() -> Tuple[np.ndarray, List[Dict]]:
    """
    Carga los vectores almacenados en los archivos .npy registrados en la base.
    Retorna matriz de vectores y metadatos asociados.
    """
    if not verificar_base_datos():
        return np.array([]), []
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, autor, vector_path, tipo_pensamiento, tono, fuente, fecha_analisis
        FROM perfiles_cognitivos 
        ORDER BY id
    """)
    registros = cursor.fetchall()
    conn.close()
    
    vectores = []
    metadatos = []
    
    for id_, autor, vector_path, tipo, tono, fuente, fecha in registros:
        if Path(vector_path).exists():
            try:
                vector = np.load(vector_path).astype('float32')
                vectores.append(vector)
                metadatos.append({
                    'id': id_,
                    'autor': autor,
                    'tipo_pensamiento': tipo,
                    'tono': tono,
                    'fuente': fuente,
                    'fecha': fecha,
                    'vector_path': vector_path
                })
            except Exception as e:
                print(f"⚠️ Error cargando vector {vector_path}: {e}")
                continue
        else:
            print(f"⚠️ Vector no encontrado: {vector_path}")
    
    if vectores:
        matriz_vectores = np.vstack(vectores)
        print(f"✅ Cargados {len(vectores)} vectores ({matriz_vectores.shape})")
        return matriz_vectores, metadatos
    else:
        print("❌ No se pudieron cargar vectores")
        return np.array([]), []

def crear_indice_faiss(force_rebuild: bool = False) -> bool:
    """
    Crea un índice FAISS desde los vectores cognitivos almacenados.
    
    Args:
        force_rebuild: Si True, reconstruye el índice aunque ya exista
    """
    if FAISS_INDEX_PATH.exists() and not force_rebuild:
        print(f"✅ Índice FAISS ya existe: {FAISS_INDEX_PATH}")
        return True
    
    print("🔄 Creando índice FAISS...")
    vectores, metadatos = cargar_vectores()
    
    if len(vectores) == 0:
        print("❌ No hay vectores cognitivos para indexar.")
        return False
    
    try:
        dim = vectores.shape[1]
        
        # Crear índice con normalización L2 para similitud coseno
        index = faiss.IndexFlatIP(dim)  # Inner Product para vectores normalizados
        
        # Normalizar vectores
        faiss.normalize_L2(vectores)
        index.add(vectores)
        
        # Crear directorio si no existe
        FAISS_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar índice
        faiss.write_index(index, str(FAISS_INDEX_PATH))
        
        # Guardar metadatos correspondientes
        metadata_path = FAISS_INDEX_PATH.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadatos, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Índice FAISS creado con {len(metadatos)} perfiles")
        print(f"  📊 Dimensión: {dim}")
        print(f"  💾 Guardado en: {FAISS_INDEX_PATH}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando índice FAISS: {e}")
        return False

# ----------------------------------------------------------
# FUNCIONES DE BÚSQUEDA
# ----------------------------------------------------------
def buscar_perfiles_por_texto(texto_consulta: str, top_k: int = 5) -> List[Dict]:
    """
    Busca los perfiles más similares a un texto nuevo.
    Compara embeddings con el índice FAISS.
    """
    if not model:
        print("❌ Modelo de embeddings no disponible")
        return []
    
    if not FAISS_INDEX_PATH.exists():
        print("⚠️ No se encontró el índice FAISS. Creando uno nuevo...")
        if not crear_indice_faiss():
            return []
    
    try:
        # Cargar índice FAISS y metadatos
        index = faiss.read_index(str(FAISS_INDEX_PATH))
        metadata_path = FAISS_INDEX_PATH.with_suffix('.json')
        
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadatos = json.load(f)
        else:
            print("⚠️ Metadatos no encontrados, recargando...")
            _, metadatos = cargar_vectores()
        
        # Generar embedding de consulta
        emb = model.encode([texto_consulta], normalize_embeddings=True).astype('float32')
        
        # Búsqueda
        scores, indices = index.search(emb, min(top_k, len(metadatos)))
        
        resultados = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < len(metadatos):
                resultado = metadatos[idx].copy()
                resultado['similarity_score'] = float(score)
                resultados.append(resultado)
        
        # Mostrar resultados
        print(f"\n🔍 Resultados de similitud cognitiva para: '{texto_consulta[:60]}...'")
        print("=" * 80)
        
        if resultados:
            tabla_datos = []
            for r in resultados:
                tabla_datos.append([
                    r['autor'][:20],
                    r['tipo_pensamiento'],
                    r['tono'],
                    r['fuente'][:30] + '...' if len(r['fuente']) > 30 else r['fuente'],
                    f"{r['similarity_score']:.4f}"
                ])
            
            print(tabulate(
                tabla_datos,
                headers=["Autor", "Tipo", "Tono", "Fuente", "Score"],
                tablefmt="fancy_grid"
            ))
        else:
            print("No se encontraron resultados similares.")
        
        return resultados
        
    except Exception as e:
        print(f"❌ Error en búsqueda por texto: {e}")
        return []

def buscar_por_autor(nombre_autor: str) -> List[Dict]:
    """Busca todos los perfiles de un autor específico"""
    if not verificar_base_datos():
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT autor, tipo_pensamiento, tono, fuente, formalismo, creatividad, 
                   empirismo, interdisciplinariedad, fecha_analisis
            FROM perfiles_cognitivos 
            WHERE autor LIKE ? 
            ORDER BY fecha_analisis DESC
        """, (f"%{nombre_autor}%",))
        
        resultados = cursor.fetchall()
        conn.close()
        
        if resultados:
            print(f"\n👤 Perfiles encontrados para '{nombre_autor}':")
            print("=" * 60)
            
            tabla_datos = []
            for r in resultados:
                tabla_datos.append([
                    r[0],  # autor
                    r[1],  # tipo_pensamiento
                    r[2],  # tono
                    f"{r[4]:.3f}",  # formalismo
                    f"{r[5]:.3f}",  # creatividad
                    f"{r[6]:.3f}",  # empirismo
                    r[8][:10]  # fecha (solo fecha)
                ])
            
            print(tabulate(
                tabla_datos,
                headers=["Autor", "Tipo", "Tono", "Form.", "Creat.", "Emp.", "Fecha"],
                tablefmt="grid"
            ))
            
            return [dict(zip([
                'autor', 'tipo_pensamiento', 'tono', 'fuente', 'formalismo',
                'creatividad', 'empirismo', 'interdisciplinariedad', 'fecha'
            ], r)) for r in resultados]
        else:
            print(f"No se encontraron perfiles para '{nombre_autor}'")
            return []
            
    except Exception as e:
        print(f"❌ Error buscando por autor: {e}")
        return []

def comparar_perfiles(autor1: str, autor2: str) -> Optional[float]:
    """
    Calcula la distancia cognitiva entre dos perfiles de autores.
    """
    if not verificar_base_datos():
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Buscar vectores de ambos autores
        cursor.execute("SELECT vector_path, autor FROM perfiles_cognitivos WHERE autor LIKE ?", (f"%{autor1}%",))
        resultado1 = cursor.fetchone()
        
        cursor.execute("SELECT vector_path, autor FROM perfiles_cognitivos WHERE autor LIKE ?", (f"%{autor2}%",))
        resultado2 = cursor.fetchone()
        
        conn.close()
        
        if not resultado1:
            print(f"❌ No se encontró perfil para '{autor1}'")
            return None
        if not resultado2:
            print(f"❌ No se encontró perfil para '{autor2}'")
            return None
        
        # Cargar vectores
        v1_path, nombre1 = resultado1
        v2_path, nombre2 = resultado2
        
        if not Path(v1_path).exists() or not Path(v2_path).exists():
            print("❌ Archivos de vectores no encontrados")
            return None
        
        v1 = np.load(v1_path).astype('float32')
        v2 = np.load(v2_path).astype('float32')
        
        # Calcular similitud coseno (más apropiada que distancia euclidiana)
        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            similarity = 0.0
        else:
            similarity = dot_product / (norm1 * norm2)
        
        distance = 1.0 - similarity  # Convertir similitud a distancia
        
        print(f"\n📊 Comparación cognitiva:")
        print(f"  👤 Autor 1: {nombre1}")
        print(f"  👤 Autor 2: {nombre2}")
        print(f"  📏 Distancia cognitiva: {distance:.4f}")
        print(f"  🔗 Similitud cognitiva: {similarity:.4f}")
        
        # Interpretación
        if similarity > 0.8:
            interpretacion = "Muy similar - Estilos cognitivos prácticamente idénticos"
        elif similarity > 0.6:
            interpretacion = "Similar - Enfoques cognitivos compatibles"
        elif similarity > 0.4:
            interpretacion = "Moderadamente similar - Algunas coincidencias"
        elif similarity > 0.2:
            interpretacion = "Poco similar - Estilos cognitivos diferentes"
        else:
            interpretacion = "Muy diferente - Enfoques cognitivos opuestos"
        
        print(f"  💡 Interpretación: {interpretacion}")
        
        return distance
        
    except Exception as e:
        print(f"❌ Error en comparación de perfiles: {e}")
        return None

# ----------------------------------------------------------
# FUNCIONES DE ANÁLISIS Y ESTADÍSTICAS
# ----------------------------------------------------------
def listar_perfiles(limit: int = 10) -> List[Tuple]:
    """Lista los perfiles disponibles en la base."""
    if not verificar_base_datos():
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, autor, tipo_pensamiento, tono, fecha_analisis, fuente
            FROM perfiles_cognitivos
            ORDER BY fecha_analisis DESC LIMIT ?
        """, (limit,))
        
        filas = cursor.fetchall()
        conn.close()
        
        if filas:
            print(f"\n📋 Últimos {len(filas)} perfiles registrados:")
            print("=" * 80)
            
            tabla_datos = []
            for fila in filas:
                tabla_datos.append([
                    fila[0],  # id
                    fila[1][:20],  # autor (truncado)
                    fila[2],  # tipo_pensamiento
                    fila[3],  # tono
                    fila[4][:16],  # fecha (truncada)
                    fila[5][:30] + '...' if len(fila[5]) > 30 else fila[5]  # fuente
                ])
            
            print(tabulate(
                tabla_datos,
                headers=["ID", "Autor", "Tipo", "Tono", "Fecha", "Fuente"],
                tablefmt="grid"
            ))
        else:
            print("No hay perfiles registrados.")
        
        return filas
        
    except Exception as e:
        print(f"❌ Error listando perfiles: {e}")
        return []

def generar_estadisticas_cognitivas() -> Dict:
    """Genera estadísticas detalladas de los perfiles cognitivos"""
    if not verificar_base_datos():
        return {}
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Estadísticas básicas
        cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
        total = cursor.fetchone()[0]
        
        # Distribución por tipos
        cursor.execute("""
            SELECT tipo_pensamiento, COUNT(*) 
            FROM perfiles_cognitivos 
            GROUP BY tipo_pensamiento 
            ORDER BY COUNT(*) DESC
        """)
        tipos = dict(cursor.fetchall())
        
        # Distribución por tonos
        cursor.execute("""
            SELECT tono, COUNT(*) 
            FROM perfiles_cognitivos 
            GROUP BY tono 
            ORDER BY COUNT(*) DESC
        """)
        tonos = dict(cursor.fetchall())
        
        # Promedios de rasgos cognitivos
        cursor.execute("""
            SELECT 
                AVG(formalismo) as avg_formalismo,
                AVG(creatividad) as avg_creatividad,
                AVG(dogmatismo) as avg_dogmatismo,
                AVG(empirismo) as avg_empirismo,
                AVG(interdisciplinariedad) as avg_interdisciplinariedad,
                AVG(nivel_abstraccion) as avg_abstraccion,
                AVG(complejidad_sintactica) as avg_complejidad,
                AVG(uso_jurisprudencia) as avg_jurisprudencia
            FROM perfiles_cognitivos
        """)
        promedios_raw = cursor.fetchone()
        
        conn.close()
        
        promedios = {
            'formalismo': promedios_raw[0] or 0,
            'creatividad': promedios_raw[1] or 0,
            'dogmatismo': promedios_raw[2] or 0,
            'empirismo': promedios_raw[3] or 0,
            'interdisciplinariedad': promedios_raw[4] or 0,
            'nivel_abstraccion': promedios_raw[5] or 0,
            'complejidad_sintactica': promedios_raw[6] or 0,
            'uso_jurisprudencia': promedios_raw[7] or 0
        }
        
        estadisticas = {
            'total_perfiles': total,
            'tipos_pensamiento': tipos,
            'distribucion_tonos': tonos,
            'promedios_rasgos': promedios
        }
        
        # Mostrar estadísticas
        print(f"\n📊 ESTADÍSTICAS COGNITIVAS")
        print("=" * 50)
        print(f"Total de perfiles: {total}")
        
        print(f"\n🧠 Tipos de pensamiento:")
        for tipo, count in tipos.items():
            porcentaje = (count / total) * 100 if total > 0 else 0
            print(f"  • {tipo}: {count} ({porcentaje:.1f}%)")
        
        print(f"\n🎭 Distribución de tonos:")
        for tono, count in tonos.items():
            porcentaje = (count / total) * 100 if total > 0 else 0
            print(f"  • {tono}: {count} ({porcentaje:.1f}%)")
        
        print(f"\n📈 Promedios de rasgos cognitivos:")
        for rasgo, promedio in promedios.items():
            print(f"  • {rasgo}: {promedio:.3f}")
        
        return estadisticas
        
    except Exception as e:
        print(f"❌ Error generando estadísticas: {e}")
        return {}

# ----------------------------------------------------------
# FUNCIONES DE MANTENIMIENTO
# ----------------------------------------------------------
def limpiar_vectores_huerfanos():
    """Elimina archivos de vectores que no tienen entrada en la base de datos"""
    if not FAISS_DIR.exists():
        print("❌ Directorio de vectores no existe")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT vector_path FROM perfiles_cognitivos")
        paths_registrados = {Path(row[0]) for row in cursor.fetchall()}
        conn.close()
        
        archivos_vectores = set(FAISS_DIR.glob("*.npy"))
        huerfanos = archivos_vectores - paths_registrados
        
        if huerfanos:
            print(f"🧹 Encontrados {len(huerfanos)} vectores huérfanos:")
            for archivo in huerfanos:
                print(f"  • {archivo.name}")
                archivo.unlink()  # Eliminar archivo
            print("✅ Vectores huérfanos eliminados")
        else:
            print("✅ No se encontraron vectores huérfanos")
            
    except Exception as e:
        print(f"❌ Error limpiando vectores: {e}")

def reconstruir_indice():
    """Reconstruye completamente el índice FAISS"""
    print("🔄 Reconstruyendo índice FAISS...")
    if FAISS_INDEX_PATH.exists():
        FAISS_INDEX_PATH.unlink()
    return crear_indice_faiss(force_rebuild=True)

# ----------------------------------------------------------
# MODO DE USO DIRECTO
# ----------------------------------------------------------
if __name__ == "__main__":
    print("\n🧠 ANALIZADOR DE PERFILES COGNITIVOS ACTIVO")
    print("=" * 60)
    
    # Verificar sistema
    if not verificar_base_datos():
        print("\n💡 Para empezar, registra algunos perfiles con vectorizador_cognitivo.py")
        exit(1)
    
    # Mostrar estadísticas
    generar_estadisticas_cognitivas()
    
    # Listar perfiles recientes  
    listar_perfiles(5)
    
    # Crear índice si no existe
    if not FAISS_INDEX_PATH.exists():
        crear_indice_faiss()
    
    # Ejemplo de búsqueda por texto
    print("\n" + "=" * 60)
    print("🔍 EJEMPLO DE BÚSQUEDA COGNITIVA")
    
    texto_demo = """
    La aplicación del principio de buena fe en la etapa precontractual
    ha sido interpretada por la doctrina moderna como un límite funcional
    a la autonomía de la voluntad, según establece el artículo 961 del
    Código Civil y Comercial. La jurisprudencia de la Corte Suprema
    en el caso "Banco Francés c/ Rossi" sostuvo que este principio debe
    ser aplicado considerando las circunstancias específicas de cada
    situación contractual.
    """
    
    resultados = buscar_perfiles_por_texto(texto_demo, top_k=3)
    
    print(f"\n✅ Análisis completado - {len(resultados)} perfiles similares encontrados")
    print("\n💡 Comandos disponibles:")
    print("  • listar_perfiles(n)")
    print("  • buscar_perfiles_por_texto('texto', k)")
    print("  • buscar_por_autor('nombre')")
    print("  • comparar_perfiles('autor1', 'autor2')")
    print("  • generar_estadisticas_cognitivas()")
    print("  • reconstruir_indice()")