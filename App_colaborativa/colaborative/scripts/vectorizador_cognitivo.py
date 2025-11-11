# -*- coding: utf-8 -*-
"""
===========================================================
 MÓDULO DE VECTORIZACIÓN COGNITIVA – SISTEMA ANALYSER MÉTODO
===========================================================

Función:
    Extrae rasgos de razonamiento jurídico y genera vectores
    cognitivos para identificar patrones de pensamiento, estilo
    argumentativo y orientación doctrinaria.

Dependencias:
    pip install sentence-transformers faiss-cpu numpy sqlite3
===========================================================
"""

import os
import json
import sqlite3
import numpy as np
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, List, Optional

# Imports con manejo de errores
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("❌ Error: Instala sentence-transformers con: pip install sentence-transformers")
    raise

# ----------------------------------------------------------
# CONFIGURACIÓN DE RUTAS
# ----------------------------------------------------------
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"
FAISS_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "faiss_index"
CHROMA_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "chroma_index"

# Crear rutas si no existen
FAISS_PATH.mkdir(parents=True, exist_ok=True)
CHROMA_PATH.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

print(f"🔧 Configuración de rutas:")
print(f"  📁 Base: {BASE_PATH}")
print(f"  🗃️ DB: {DB_PATH}")
print(f"  📊 FAISS: {FAISS_PATH}")

# ----------------------------------------------------------
# INICIALIZACIÓN DE BASE DE DATOS
# ----------------------------------------------------------
def init_cognitive_db():
    """Inicializa la base de datos de perfiles cognitivos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS perfiles_cognitivos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        autor TEXT NOT NULL,
        fuente TEXT NOT NULL,
        tipo_pensamiento TEXT DEFAULT 'indeterminado',
        formalismo REAL DEFAULT 0.0,
        creatividad REAL DEFAULT 0.0,
        dogmatismo REAL DEFAULT 0.0,
        empirismo REAL DEFAULT 0.0,
        interdisciplinariedad REAL DEFAULT 0.0,
        nivel_abstraccion REAL DEFAULT 0.5,
        complejidad_sintactica REAL DEFAULT 0.0,
        uso_jurisprudencia REAL DEFAULT 0.0,
        tono TEXT DEFAULT 'neutro',
        fecha_analisis DATETIME DEFAULT CURRENT_TIMESTAMP,
        vector_path TEXT NOT NULL,
        texto_muestra TEXT,
        UNIQUE(autor, fuente)
    )
    """)
    
    # Índices para búsquedas eficientes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_autor ON perfiles_cognitivos(autor)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tipo ON perfiles_cognitivos(tipo_pensamiento)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fecha ON perfiles_cognitivos(fecha_analisis)")
    
    conn.commit()
    conn.close()
    print("✅ Base de datos cognitiva inicializada")

# Inicializar al importar
init_cognitive_db()

# ----------------------------------------------------------
# MODELO DE EMBEDDINGS
# ----------------------------------------------------------
print("🔹 Cargando modelo cognitivo (all-mpnet-base-v2)...")
try:
    model = SentenceTransformer('all-mpnet-base-v2')
    print("✅ Modelo cargado exitosamente")
except Exception as e:
    print(f"❌ Error cargando modelo: {e}")
    raise

# ----------------------------------------------------------
# ANÁLISIS COGNITIVO AVANZADO
# ----------------------------------------------------------
def extraer_rasgos_cognitivos(texto: str) -> Dict[str, float]:
    """
    Extrae rasgos cognitivos específicos del texto jurídico.
    Métricas más sofisticadas que la versión anterior.
    """
    if not texto or len(texto.strip()) < 50:
        return {
            "formalismo": 0.0,
            "creatividad": 0.0,
            "dogmatismo": 0.0,
            "empirismo": 0.0,
            "interdisciplinariedad": 0.0,
            "nivel_abstraccion": 0.5,
            "complejidad_sintactica": 0.0,
            "uso_jurisprudencia": 0.0
        }
    
    texto_lower = texto.lower()
    palabras = texto_lower.split()
    total_palabras = len(palabras) or 1
    oraciones = re.split(r'[.!?]+', texto)
    total_oraciones = len([s for s in oraciones if s.strip()]) or 1
    
    # 1. FORMALISMO JURÍDICO
    indicadores_formales = [
        r'\bart\.\s*\d+', r'\binc\.\s*\d+', r'\bley\s+\d+',
        r'\bcódigo\s+civil', r'\bcódigo\s+penal', r'\bconstituci[óo]n',
        r'\bdecreto\s+\d+', r'\bresoluci[óo]n\s+\d+'
    ]
    formalismo = sum(len(re.findall(patron, texto_lower)) for patron in indicadores_formales) / total_palabras
    
    # 2. CREATIVIDAD INTERPRETATIVA
    indicadores_creativos = [
        'interpretaci[óo]n', 'reinterpret', 'nueva perspectiva', 'enfoque innovador',
        'propone', 'sugiere', 'plantea', 'considera', 'podríamos entender',
        'cabe preguntarse', 'sería posible', 'alternativa'
    ]
    creatividad = sum(texto_lower.count(ind) for ind in indicadores_creativos) / total_palabras
    
    # 3. DOGMATISMO DOCTRINAL
    indicadores_dogmaticos = [
        'según la doctrina', 'la doctrina enseña', 'es incuestionable', 'sin duda',
        'claramente establece', 'definitivamente', 'incondicionalmente',
        'tradicionalmente', 'clásicamente', 'ortodoxamente'
    ]
    dogmatismo = sum(texto_lower.count(ind) for ind in indicadores_dogmaticos) / total_palabras
    
    # 4. EMPIRISMO (uso de casos, ejemplos)
    indicadores_empiricos = [
        r'\bcaso\b', r'\bejemplo\b', r'\bpráctica\b', r'\bexperiencia\b',
        r'\bfallo\b', r'\bsentencia\b', r'\bjurisprudencia\b',
        r'\btribunal\b', r'\bcorte\b', r'\bjuzgado\b'
    ]
    empirismo = sum(len(re.findall(patron, texto_lower)) for patron in indicadores_empiricos) / total_palabras
    
    # 5. INTERDISCIPLINARIEDAD
    disciplinas = [
        'sociolog[íi]a', 'econom[íi]a', 'filosofia', 'psicolog[íi]a',
        'antropolog[íi]a', 'ciencia pol[íi]tica', 'historia',
        'lingü[íi]stica', 'l[óo]gica', 'estadística'
    ]
    interdisciplinariedad = sum(len(re.findall(disc, texto_lower)) for disc in disciplinas) / total_palabras
    
    # 6. NIVEL DE ABSTRACCIÓN
    indicadores_abstractos = [
        'principio', 'concepto', 'teoría', 'fundamento', 'esencia',
        'naturaleza', 'categoría', 'noción', 'idea', 'pensamiento'
    ]
    indicadores_concretos = [
        'específicamente', 'concretamente', 'en particular', 'por ejemplo',
        'caso concreto', 'situación específica', 'aplicación práctica'
    ]
    abstraccion_score = sum(texto_lower.count(ind) for ind in indicadores_abstractos)
    concreto_score = sum(texto_lower.count(ind) for ind in indicadores_concretos)
    
    if abstraccion_score + concreto_score > 0:
        nivel_abstraccion = abstraccion_score / (abstraccion_score + concreto_score)
    else:
        nivel_abstraccion = 0.5
    
    # 7. COMPLEJIDAD SINTÁCTICA
    palabras_por_oracion = total_palabras / total_oraciones
    complejidad_sintactica = min(palabras_por_oracion / 20.0, 1.0)  # Normalizado a [0,1]
    
    # 8. USO DE JURISPRUDENCIA
    indicadores_jurisprudenciales = [
        r'c\.s\.j\.n\.', r'corte suprema', r'cámara nacional', r'tribunal superior',
        r'fallo\s+\w+', r'sentencia\s+del', r'decidió que', r'sostuvo que',
        r'in re\s+\w+', r'autos\s+\w+'
    ]
    uso_jurisprudencia = sum(len(re.findall(patron, texto_lower)) for patron in indicadores_jurisprudenciales) / total_palabras
    
    return {
        "formalismo": min(formalismo * 100, 1.0),  # Escalar apropiadamente
        "creatividad": min(creatividad * 50, 1.0),
        "dogmatismo": min(dogmatismo * 20, 1.0),
        "empirismo": min(empirismo * 30, 1.0),
        "interdisciplinariedad": min(interdisciplinariedad * 100, 1.0),
        "nivel_abstraccion": nivel_abstraccion,
        "complejidad_sintactica": complejidad_sintactica,
        "uso_jurisprudencia": min(uso_jurisprudencia * 50, 1.0)
    }

def detectar_tipo_pensamiento(rasgos: Dict[str, float]) -> str:
    """
    Clasifica el tipo de pensamiento jurídico basado en los rasgos extraídos.
    """
    if rasgos["formalismo"] > 0.3:
        return "Formalista"
    elif rasgos["empirismo"] > 0.2:
        return "Realista"
    elif rasgos["creatividad"] > 0.15:
        return "Interpretativo"
    elif rasgos["dogmatismo"] > 0.1:
        return "Tradicionalista"
    elif rasgos["interdisciplinariedad"] > 0.05:
        return "Interdisciplinario"
    elif rasgos["nivel_abstraccion"] > 0.7:
        return "Conceptualista"
    else:
        return "Pragmático"

def detectar_tono(texto: str) -> str:
    """
    Detecta el tono argumentativo del texto.
    """
    texto_lower = texto.lower()
    
    # Indicadores de tono
    critico = ['critica', 'cuestiona', 'refuta', 'objeta', 'contradice', 'erróneo', 'incorrecto']
    asertivo = ['afirma', 'sostiene', 'establece', 'demuestra', 'evidencia', 'claramente']
    cauteloso = ['quizás', 'posiblemente', 'podría', 'cabría', 'eventualmente', 'en principio']
    
    puntos_critico = sum(texto_lower.count(ind) for ind in critico)
    puntos_asertivo = sum(texto_lower.count(ind) for ind in asertivo)
    puntos_cauteloso = sum(texto_lower.count(ind) for ind in cauteloso)
    
    if puntos_critico > puntos_asertivo and puntos_critico > puntos_cauteloso:
        return "crítico"
    elif puntos_asertivo > puntos_cauteloso:
        return "asertivo"
    elif puntos_cauteloso > 2:
        return "cauteloso"
    else:
        return "neutro"

# ----------------------------------------------------------
# FUNCIÓN PRINCIPAL DE VECTORIZACIÓN
# ----------------------------------------------------------
def generar_vector_cognitivo(texto: str) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Genera un vector que representa el perfil cognitivo del texto.
    Combina embeddings semánticos con métricas cognitivas específicas.
    """
    if not texto or len(texto.strip()) < 100:
        raise ValueError("El texto es demasiado corto para análisis cognitivo (mínimo 100 caracteres).")

    # Embedding semántico base
    try:
        emb = model.encode(texto, normalize_embeddings=True)
    except Exception as e:
        raise ValueError(f"Error generando embedding: {e}")

    # Rasgos cognitivos específicos
    rasgos = extraer_rasgos_cognitivos(texto)

    # Vector combinado: embedding + rasgos cognitivos
    vector_cognitivo = np.concatenate([
        emb, 
        np.array(list(rasgos.values()), dtype=np.float32)
    ])
    
    return vector_cognitivo, rasgos

# ----------------------------------------------------------
# REGISTRO EN BASE DE DATOS
# ----------------------------------------------------------
def registrar_perfil(autor: str, texto: str, fuente: str, texto_muestra: Optional[str] = None, 
                    metadatos_extra: Optional[Dict] = None) -> str:
    """
    Registra un perfil cognitivo en la base de datos y guarda el vector
    en un archivo .npy dentro del índice FAISS.
    """
    if not autor or not texto or not fuente:
        raise ValueError("Autor, texto y fuente son obligatorios")
    
    try:
        vector, rasgos = generar_vector_cognitivo(texto)
        
        # Análisis adicional
        tipo_pensamiento = detectar_tipo_pensamiento(rasgos)
        tono = detectar_tono(texto)
        
        # Generar nombre único para el archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        autor_clean = re.sub(r'[^\w\s-]', '', autor).replace(' ', '_').lower()
        nombre_archivo = f"{autor_clean}_{timestamp}.npy"
        vector_path = FAISS_PATH / nombre_archivo
        
        # Guardar vector
        np.save(vector_path, vector)
        
        # Registrar en base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Usar texto_muestra si se proporciona, sino tomar una muestra del texto
        muestra = texto_muestra or texto[:500] + "..." if len(texto) > 500 else texto
        
        # Procesar metadatos extra si están disponibles
        metadatos_json = ""
        autor_confianza = 0.0
        razonamiento_dominante = ""
        modalidad_epistemica = ""
        estructura_silogistica = ""
        ethos = pathos = logos = 0.0
        
        if metadatos_extra:
            try:
                import json
                metadatos_json = json.dumps(metadatos_extra, ensure_ascii=False)
                
                # Extraer datos aristotélicos si están disponibles
                if "aristotelico" in metadatos_extra:
                    aristo = metadatos_extra["aristotelico"]
                    autor_principal = aristo.get("obra", {}).get("autor_principal", {})
                    autor_confianza = autor_principal.get("confianza", 0.0)
                    
                    analisis = aristo.get("analisis", {})
                    razonamiento = analisis.get("razonamiento", {})
                    if razonamiento.get("top3"):
                        razonamiento_dominante = razonamiento["top3"][0].get("clase", "")
                    
                    modalidad = analisis.get("modalidad_epistemica", {})
                    modalidad_epistemica = modalidad.get("predominante", {}).get("clase", "")
                    
                    silogismo = analisis.get("estructura_silogistica", {})
                    estructura_silogistica = silogismo.get("principal", {}).get("nombre", "")
                    
                    retorica = analisis.get("retorica", {})
                    ethos = retorica.get("ethos", 0.0)
                    pathos = retorica.get("pathos", 0.0)
                    logos = retorica.get("logos", 0.0)
            except Exception as e:
                print(f"⚠️ Error procesando metadatos extra: {e}")

        cursor.execute("""
            INSERT OR REPLACE INTO perfiles_cognitivos
            (autor, fuente, tipo_pensamiento, formalismo, creatividad, dogmatismo, 
             empirismo, interdisciplinariedad, nivel_abstraccion, complejidad_sintactica,
             uso_jurisprudencia, tono, vector_path, texto_muestra, fecha_analisis,
             metadatos_json, autor_confianza, razonamiento_dominante, modalidad_epistemica,
             estructura_silogistica, ethos, pathos, logos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            autor, fuente, tipo_pensamiento,
            rasgos["formalismo"], rasgos["creatividad"], rasgos["dogmatismo"],
            rasgos["empirismo"], rasgos["interdisciplinariedad"], rasgos["nivel_abstraccion"],
            rasgos["complejidad_sintactica"], rasgos["uso_jurisprudencia"],
            tono, str(vector_path), muestra, datetime.now().isoformat(),
            metadatos_json, autor_confianza, razonamiento_dominante, modalidad_epistemica,
            estructura_silogistica, ethos, pathos, logos
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Perfil cognitivo registrado:")
        print(f"  👤 Autor: {autor}")
        print(f"  📄 Fuente: {fuente}")
        print(f"  🧠 Tipo: {tipo_pensamiento}")
        print(f"  🎭 Tono: {tono}")
        print(f"  📊 Rasgos: {dict(list(rasgos.items())[:4])}")
        
        return str(vector_path)
        
    except Exception as e:
        print(f"❌ Error registrando perfil: {e}")
        raise

# ----------------------------------------------------------
# FUNCIONES DE CONSULTA
# ----------------------------------------------------------
def listar_perfiles(limit: int = 10) -> List[Tuple]:
    """Devuelve una lista de perfiles registrados en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, autor, tipo_pensamiento, tono, fecha_analisis, fuente
        FROM perfiles_cognitivos 
        ORDER BY fecha_analisis DESC 
        LIMIT ?
    """, (limit,))
    
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_estadisticas() -> Dict:
    """Retorna estadísticas generales de los perfiles"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Estadísticas básicas
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT tipo_pensamiento, COUNT(*) FROM perfiles_cognitivos GROUP BY tipo_pensamiento")
    tipos = dict(cursor.fetchall())
    
    cursor.execute("SELECT tono, COUNT(*) FROM perfiles_cognitivos GROUP BY tono")
    tonos = dict(cursor.fetchall())
    
    cursor.execute("SELECT AVG(formalismo), AVG(creatividad), AVG(empirismo) FROM perfiles_cognitivos")
    promedios = cursor.fetchone()
    
    conn.close()
    
    return {
        "total_perfiles": total,
        "tipos_pensamiento": tipos,
        "distribución_tonos": tonos,
        "promedios": {
            "formalismo": promedios[0] or 0,
            "creatividad": promedios[1] or 0,
            "empirismo": promedios[2] or 0
        }
    }

# ----------------------------------------------------------
# MODO DE USO DIRECTO
# ----------------------------------------------------------
if __name__ == "__main__":
    print("\n🧠 VECTORIZADOR COGNITIVO ACTIVO\n")
    
    # Ejemplo de uso
    ejemplo_texto = """
    La aplicación del artículo 1197 del Código Civil argentino establece claramente 
    que las convenciones hechas en los contratos forman para las partes una regla 
    a la cual deben someterse como a la ley misma. Sin embargo, la jurisprudencia 
    de la Corte Suprema ha sostenido que este principio debe interpretarse 
    conforme a los postulados de la buena fe contractual. En el caso "Banco de 
    Boston c/ García" la Corte decidió que la autonomía de la voluntad encuentra 
    límites en el orden público y las buenas costumbres.
    """
    
    autor_ejemplo = "Dr. Juan Pérez"
    fuente_ejemplo = "Manual de Derecho Civil - Contratos"
    
    try:
        path = registrar_perfil(autor_ejemplo, ejemplo_texto, fuente_ejemplo)
        print(f"\n🔗 Vector guardado en: {path}")
        
        print("\n📊 Estadísticas generales:")
        stats = obtener_estadisticas()
        for clave, valor in stats.items():
            print(f"  {clave}: {valor}")
        
        print("\n📋 Últimos perfiles registrados:")
        perfiles = listar_perfiles(5)
        for perfil in perfiles:
            print(f"  • {perfil[1]} ({perfil[2]}) - {perfil[4]}")
            
    except Exception as e:
        print(f"❌ Error en ejemplo: {e}")
        
    print("\n✅ Vectorizador cognitivo listo para uso.")