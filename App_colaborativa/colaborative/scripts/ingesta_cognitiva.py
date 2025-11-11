# ==========================================================
# ⚖️ ANALYSER MÉTODO – INGESTA COGNITIVA AVANZADA (v3.1)
# ==========================================================
# VERSIÓN UNIFICADA Y OPTIMIZADA
# Este módulo fusiona lo mejor de las versiones anteriores e incluye:
#  - Análisis cognitivo-aristotélico completo
#  - Detección de autor por layout + contexto semántico
#  - Reconstrucción de índice teleológico
#  - Clasificación de párrafos por función lógica
#  - Análisis retórico (Ethos, Pathos, Logos)
#  - Detección de modalidades epistémicas y estructuras silogísticas
#  - Compatibilidad total con base de datos existente
# ==========================================================

from pathlib import Path
from datetime import datetime
import os
import sqlite3
import json
import re
import sys
from typing import Dict, List, Any, Optional

# -------- Import del detector (robusto a estructura de proyecto)
try:
    from detector_razonamiento_aristotelico import (
        analizar_pdf,
        extraer_autores_citados,
        clasificar_razonamiento_avanzado,
        detectar_modalidad_epistemica,
        detectar_estructura_silogistica,
        detectar_ethos_pathos_logos,
    )
except ImportError:
    try:
        sys.path.append(str(Path(__file__).parent))
        from detector_razonamiento_aristotelico import (
            analizar_pdf,
            extraer_autores_citados,
            clasificar_razonamiento_avanzado,
            detectar_modalidad_epistemica,
            detectar_estructura_silogistica,
            detectar_ethos_pathos_logos,
        )
    except ImportError as e:
        print(f"❌ Error importando detector_razonamiento_aristotelico: {e}")
        print("💡 Asegúrate de que el archivo esté en la misma carpeta")
        sys.exit(1)

# -------- Import del vectorizador cognitivo (CRÍTICO para los 8 rasgos)
try:
    from vectorizador_cognitivo import extraer_rasgos_cognitivos
except ImportError:
    try:
        sys.path.append(str(Path(__file__).parent))
        from vectorizador_cognitivo import extraer_rasgos_cognitivos
    except ImportError as e:
        print(f"⚠️ Advertencia: No se pudo importar vectorizador_cognitivo: {e}")
        print("💡 Los rasgos cognitivos se establecerán en 0")
        # Función dummy si no existe el vectorizador
        def extraer_rasgos_cognitivos(texto: str) -> dict:
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

# -------- Import del chunker inteligente (MEJORA para fragmentación semántica)
try:
    from chunker_inteligente import ChunkerInteligente
    USAR_CHUNKER_INTELIGENTE = True
    print("✅ Chunker Inteligente activado - Fragmentación semántica mejorada")
except ImportError:
    USAR_CHUNKER_INTELIGENTE = False
    print("ℹ️ Chunker Inteligente no disponible - Usando fragmentación estándar")

import fitz
import unicodedata
import numpy as np

# -------- Rutas base robustas
BASE_PATH = Path(__file__).resolve().parents[1]
if not (BASE_PATH / "data").exists():
    # fallback si el repo está un nivel más arriba
    BASE_PATH = Path(__file__).resolve().parents[2]

PDFS_DIR = BASE_PATH / "data" / "pdfs" / "general"
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# ==========================================================
# 🔹 UTILIDADES INTERNAS – AUTORÍA MEJORADA
# ==========================================================
def __normalizar_espacios(s: str) -> str:
    """Normaliza espacios múltiples en texto."""
    return re.sub(r"\s+", " ", s).strip()

def __es_posible_nombre(s: str) -> bool:
    """Evalúa si un string parece ser un nombre de autor."""
    toks = s.strip().split()
    if not (2 <= len(toks) <= 6):
        return False
        
    # Contar palabras capitalizadas correctamente
    cap = sum(1 for t in toks if re.match(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ.-]*$", t))
    # Contar iniciales
    init = any(re.match(r"^[A-ZÁÉÍÓÚÑ]\.$", t) for t in toks)
    
    # Filtrar palabras que claramente no son nombres
    palabras_prohibidas = ['amparo', 'derecho', 'ley', 'código', 'teoría', 'práctica', 
                          'tutela', 'abc', 'incidentes', 'recursos', 'capítulo', 'título',
                          'índice', 'página', 'parte', 'sección', 'artículo']
    
    texto_lower = s.lower()
    if any(palabra in texto_lower for palabra in palabras_prohibidas):
        return False
    
    return cap >= 2 or init

def __score_centrado(x0, x1, pw):
    """Calcula score de centrado horizontal."""
    cx = (x0 + x1) / 2.0
    return 1.0 - min(1.0, abs(cx - pw/2.0) / (pw/2.0))

def __candidatos_autor_por_portada(page):
    """Detecta posibles autores en la portada usando análisis de layout."""
    pw, ph = page.rect.width, page.rect.height
    data = page.get_text("dict")
    spans = []
    max_fs = 0.0
    
    # Extraer todos los spans con sus propiedades
    for b in data.get("blocks", []):
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                txt = __normalizar_espacios(s.get("text", ""))
                if not txt:
                    continue
                x0, y0, x1, y1 = s.get("bbox", [0, 0, 0, 0])
                fs = float(s.get("size", 0.0))
                max_fs = max(max_fs, fs)
                spans.append((txt, fs, (x0, y0, x1, y1)))

    # Calcular scores para cada candidato
    cand = []
    for txt, fs, (x0, y0, x1, y1) in spans:
        if y0 > ph * 0.38:  # Solo tercio superior
            continue
        rel = 0.0 if max_fs == 0 else fs / max_fs
        cent = __score_centrado(x0, x1, pw)
        looks = 1.0 if __es_posible_nombre(txt) else 0.0
        score = 0.45 * cent + 0.35 * rel + 0.20 * looks
        cand.append((txt, fs, (x0, y0, x1, y1), score))

    # Filtrar candidatos relevantes
    cand = [c for c in cand if c[1] >= max_fs * 0.5 or __es_posible_nombre(c[0])]
    cand.sort(key=lambda c: (c[2][1], c[2][0]))

    if not cand:
        return []

    # Combinar spans contiguos (misma línea)
    comb = []
    buf = None
    for c in cand:
        txt, fs, (x0, y0, x1, y1), sc = c
        if buf and abs(y0 - buf[3]) < 3.0:
            buf[0] = __normalizar_espacios(buf[0] + " " + txt)
            buf[2] = min(buf[2], x0)
            buf[4] = max(buf[4], x1)
            buf[6] = max(buf[6], sc)
        else:
            if buf:
                comb.append((buf[0], buf[1], (buf[2], buf[3], buf[4], buf[5]), buf[6]))
            buf = [txt, fs, x0, y0, x1, y1, sc]
    if buf:
        comb.append((buf[0], buf[1], (buf[2], buf[3], buf[4], buf[5]), buf[6]))

    # Aplicar bonus adicionales
    fin = []
    for txt, fs, bbox, sc in comb:
        toks = txt.split()
        bonus = 0.0
        if any(re.match(r"^[A-ZÁÉÍÓÚÑ]\.$", t) for t in toks):
            bonus += 0.1
        if 2 <= len(toks) <= 6:
            bonus += 0.1
        if len(txt) > 40:
            bonus -= 0.15
        fin.append((txt, fs, bbox, max(0.0, min(1.0, sc + bonus))))
    
    fin.sort(key=lambda c: c[3], reverse=True)
    return fin

def consolidar_autoria_layout_semantica(ruta_pdf: str, portada_text: str, metadata: dict) -> dict:
    """Fusiona análisis de metadatos, contexto semántico y layout para detectar autor principal."""
    
    # 1. PRIORIDAD MÁXIMA: METADATOS DEL PDF
    autor_meta = (metadata or {}).get("author") or (metadata or {}).get("Author") or ""
    if isinstance(autor_meta, str) and autor_meta.strip():
        autor_limpio = autor_meta.strip()
        # Validar que no sea software/sistema
        if (len(autor_limpio) > 3 and 
            not re.search(r'(microsoft|adobe|system|pdf|creator|producer|foxit|phantom)', autor_limpio.lower()) and
            not re.match(r'^(unknown|user|admin|\d+)$', autor_limpio.lower())):
            return {
                "nombre": autor_limpio, 
                "confianza": 0.95, 
                "fuente": "metadata_pdf"
            }

    # 2. ANÁLISIS SEMÁNTICO DEL CONTEXTO COMPLETO
    try:
        doc = fitz.open(ruta_pdf)
        texto_completo = ""
        
        # Analizar hasta 3 páginas
        for i in range(min(3, len(doc))):
            texto_completo += doc[i].get_text("text") + "\n"
        
        doc.close()
        
        # Buscar patrones específicos de autoría
        patrones_autor = [
            r'(?:Por|Autor|Author):\s*([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ\s\.]{8,50})',
            r'(?:Dr|Dra|Mg|Prof|Esp)\.\s*([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ\s\.]{8,50})',
            r'^([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ]+)*)\s*$',
            r'([A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][A-Za-záéíóúñ]+)\s*\n(?=(?:[A-Z\s]{8,}|ÍNDICE|CAPÍTULO))'
        ]
        
        for patron in patrones_autor:
            for match in re.finditer(patron, texto_completo, re.MULTILINE):
                autor_encontrado = match.group(1).strip()
                # Filtrar falsos positivos
                if (len(autor_encontrado) > 8 and len(autor_encontrado) < 60 and
                    not re.search(r'(capítulo|índice|página|titulo|amparo|derecho|ley|tutela|teoria|practica|recursos)', autor_encontrado.lower()) and
                    not re.search(r'(buenos aires|república argentina|ciudad autónoma)', autor_encontrado.lower())):
                    return {
                        "nombre": autor_encontrado,
                        "confianza": 0.92,
                        "fuente": "patron_contexto"
                    }
        
        # Buscar nombres específicos mencionados
        nombres_candidatos = re.findall(r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){2,4})\b', texto_completo)
        for nombre in nombres_candidatos:
            if (len(nombre) > 12 and len(nombre) < 50 and
                __es_posible_nombre(nombre) and
                not re.search(r'(buenos aires|república argentina|ciudad autónoma|juzgados federales)', nombre.lower())):
                return {
                    "nombre": nombre,
                    "confianza": 0.88,
                    "fuente": "nombre_contexto"
                }
                
    except Exception as e:
        print(f"⚠️ Error en análisis semántico: {e}")

    # 3. ANÁLISIS DE LAYOUT MEJORADO
    try:
        doc = fitz.open(ruta_pdf)
        cand = __candidatos_autor_por_portada(doc.load_page(0))
        doc.close()
        
        if cand:
            # Filtrar candidatos que parecen títulos
            candidatos_filtrados = []
            for txt, fs, bbox, score in cand:
                txt_normalizado = __normalizar_espacios(unicodedata.normalize("NFKC", txt))
                
                # Filtrar títulos obvios
                es_titulo = any(palabra in txt_normalizado.lower() for palabra in 
                              ['amparo', 'derecho', 'ley', 'código', 'teoría', 'práctica', 'tutela', 'abc', 'incidentes', 'recursos'])
                
                # Si parece un nombre, darle prioridad
                if __es_posible_nombre(txt_normalizado) and not es_titulo:
                    score += 0.3  # Bonus por parecer nombre
                elif es_titulo:
                    score *= 0.4  # Penalizar títulos
                
                candidatos_filtrados.append((txt_normalizado, fs, bbox, score))
            
            candidatos_filtrados.sort(key=lambda c: c[3], reverse=True)
            
            if candidatos_filtrados:
                txt, fs, bbox, score = candidatos_filtrados[0]
                
                # Normalizar mayúsculas completas
                if txt.isupper():
                    parts = [
                        t if re.match(r"^[A-ZÁÉÍÓÚÑ]\.$", t) else t.capitalize()
                        for t in txt.split()
                    ]
                    txt = " ".join(parts)
                
                # Solo aceptar si tiene confianza mínima y no es obviamente un título
                if score > 0.4 and not any(palabra in txt.lower() for palabra in 
                                         ['amparo', 'derecho', 'ley', 'tutela', 'abc', 'recursos']):
                    return {
                        "nombre": txt, 
                        "confianza": round(min(0.75, score), 2), 
                        "fuente": "layout_mejorado"
                    }
                    
    except Exception as e:
        print(f"⚠️ Error analizando layout: {e}")

    # 4. FALLBACK FINAL: METADATA BÁSICO
    if isinstance(autor_meta, str) and autor_meta.strip() and len(autor_meta.strip()) > 2:
        return {
            "nombre": autor_meta.strip(), 
            "confianza": 0.35, 
            "fuente": "metadata_fallback"
        }

    return {
        "nombre": "Autor no identificado", 
        "confianza": 0.0, 
        "fuente": None
    }

# ==========================================================
# 🔹 DETECCIÓN DEL ÍNDICE Y ORDEN TELEOLÓGICO
# ==========================================================
def detectar_estructura_teleologica(texto: str) -> dict:
    """Detecta la estructura conceptual y el orden teleológico del documento."""
    lineas = texto.splitlines()
    estructura = []
    teleologica = []
    
    # Detectar elementos estructurales
    for l in lineas:
        l_clean = l.strip()
        if re.match(r"^(CAP[IÍ]TULO|T[IÍ]TULO|SECCI[ÓO]N|[IVXLC]+\.)", l_clean.upper()):
            estructura.append(l_clean)
        elif re.match(r"^(\d+(\.\d+)*\s)", l_clean):
            estructura.append(l_clean)
            
        # Detectar elementos teleológicos
        if re.search(r"(objeto|propósito|finalidad|conclusi[oó]n|resultado)", l_clean.lower()):
            teleologica.append(l_clean)
    
    return {
        "nodos_detectados": estructura[:50],
        "teleologicos": teleologica[:20],
        "profundidad": len(estructura),
        "indicadores": {
            "tiene_prólogo": any("prólogo" in l.lower() for l in lineas[:40]),
            "tiene_conclusiones": any("conclusión" in l.lower() for l in lineas[-80:])
        }
    }

# ==========================================================
# 🔹 CLASIFICACIÓN DE PÁRRAFOS POR FUNCIÓN LÓGICA
# ==========================================================
def clasificar_parrafos_por_intencion(texto: str) -> List[dict]:
    """Clasifica párrafos según su función lógica en el argumento."""
    parrafos = [p.strip() for p in texto.split("\n\n") if len(p.strip()) > 60]
    roles = []
    
    for p in parrafos:
        low = p.lower()
        if re.search(r"(introducci[oó]n|se presenta|a continuaci[oó]n)", low):
            rol = "Expositivo"
        elif re.search(r"(por tanto|se concluye|en consecuencia|por ende)", low):
            rol = "Conclusivo"
        elif re.search(r"(demuestra|justifica|argumenta|fundamenta|analiza)", low):
            rol = "Argumentativo"
        elif re.search(r"(prop[oó]sito|objeto|fin|para lograr)", low):
            rol = "Teleológico"
        else:
            rol = "Neutro"
        
        roles.append({
            "texto": p[:120] + "..." if len(p) > 120 else p,
            "rol": rol
        })
    
    return roles

# ==========================================================
# 🔹 PERFIL COGNITIVO COMPLETO Y REGISTRO
# ==========================================================
def generar_perfil_aristotelico(path_pdf: str) -> dict:
    """Genera el perfil cognitivo-aristotélico completo del documento."""
    print(f"🔍 Analizando estructura cognitiva de {Path(path_pdf).name}")
    
    # Análisis base del PDF
    d = analizar_pdf(path_pdf)
    
    # Detección de autoría avanzada
    autor = consolidar_autoria_layout_semantica(path_pdf, d["portada"], d["metadata"])
    
    # Análisis de contenido
    citados = extraer_autores_citados(d["texto"], d["notas_pie"])
    razon = clasificar_razonamiento_avanzado(d["texto"])
    epist = detectar_modalidad_epistemica(d["texto"])
    silog = detectar_estructura_silogistica(d["texto"])
    reto = detectar_ethos_pathos_logos(d["texto"])
    
    # Análisis estructural
    estructura = detectar_estructura_teleologica(d["texto"])
    parrafos = clasificar_parrafos_por_intencion(d["texto"])
    
    return {
        "obra": {
            "archivo": Path(path_pdf).name,
            "autor_principal": autor,
            "autores_citados": citados,
            "estructura_teleologica": estructura,
        },
        "analisis": {
            "razonamiento": razon,
            "modalidad_epistemica": epist,
            "silogismo": silog,
            "retorica": reto,
            "parrafos_clasificados": parrafos[:50],
        },
    }

def registrar_perfil_cognitivo_avanzado(ruta_pdf: str) -> bool:
    """Guarda el resultado en la base SQLite con manejo robusto de errores."""
    print(f"\n📘 Analizando {Path(ruta_pdf).name} ...")
    
    try:
        perfil = generar_perfil_aristotelico(ruta_pdf)
        
        # Extracción segura de datos (previene errores si algún campo falta)
        autor_info = perfil.get("obra", {}).get("autor_principal") or {}
        autor = autor_info.get("nombre", "Desconocido")
        confianza = float(autor_info.get("confianza", 0.0))
        
        razonamiento = (perfil.get("analisis", {}).get("razonamiento") or {}).get("top3", [])
        razonamiento_json = json.dumps(razonamiento, ensure_ascii=False)
        
        modalidad_info = (perfil.get("analisis", {}).get("modalidad_epistemica") or {}).get("predominante", {})
        modalidad = modalidad_info.get("clase", "No detectada")
        
        silog_principal = (perfil.get("analisis", {}).get("silogismo") or {}).get("principal")
        silogismo_json = json.dumps(silog_principal, ensure_ascii=False)
        
        ret = perfil.get("analisis", {}).get("retorica") or {}
        ethos = float(ret.get("ethos", 0.0))
        pathos = float(ret.get("pathos", 0.0))
        
        # 🧠 NUEVO: Extraer texto completo y calcular rasgos cognitivos
        print(f"   🧠 Calculando rasgos cognitivos...")
        try:
            doc = fitz.open(ruta_pdf)
            texto_completo = ""
            for pagina in doc:
                texto_completo += pagina.get_text()
            doc.close()
            
            total_palabras = len(texto_completo.split())
            rasgos = extraer_rasgos_cognitivos(texto_completo)
            print(f"   📊 Procesadas {total_palabras:,} palabras")
        except Exception as e:
            print(f"   ⚠️ Error calculando rasgos: {e}")
            total_palabras = 0
            rasgos = {
                "formalismo": 0.0, "creatividad": 0.0, "dogmatismo": 0.0,
                "empirismo": 0.0, "interdisciplinariedad": 0.0,
                "nivel_abstraccion": 0.5, "complejidad_sintactica": 0.0,
                "uso_jurisprudencia": 0.0
            }
        logos = float(ret.get("logos", 0.0))
        
        estructura_json = json.dumps(perfil.get("obra", {}).get("estructura_teleologica") or {}, ensure_ascii=False)
        parrafos_json = json.dumps(perfil.get("analisis", {}).get("parrafos_clasificados") or [], ensure_ascii=False)
        
        # Asegurar que la base de datos existe con la estructura correcta
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        cur = conn.cursor()
        
        # Crear tabla si no existe (compatible con estructura existente)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS perfiles_cognitivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT,
                fuente TEXT,
                tipo_pensamiento TEXT,
                formalismo REAL,
                creatividad REAL,
                dogmatismo REAL,
                empirismo REAL,
                interdisciplinariedad REAL,
                nivel_abstraccion REAL,
                complejidad_sintactica REAL,
                uso_jurisprudencia REAL,
                tono TEXT,
                fecha_analisis DATETIME,
                vector_path TEXT,
                texto_muestra TEXT,
                autor_confianza REAL,
                autores_citados TEXT,
                razonamiento_top3 TEXT,
                razonamiento_dominante TEXT,
                ethos REAL,
                pathos REAL,
                logos REAL,
                nivel_tecnico REAL,
                latinismos INTEGER,
                citas_legales INTEGER,
                referencias_doctrinarias INTEGER,
                total_palabras INTEGER,
                notas_pie_detectadas INTEGER,
                metadatos_json TEXT,
                modalidad_epistemica TEXT,
                estructura_silogistica TEXT,
                silogismo_confianza REAL,
                conectores_logicos TEXT,
                razonamiento_ejemplos TEXT,
                perfil_aristotelico_json TEXT,
                archivo TEXT,
                indice_teleologico TEXT,
                roles_parrafos TEXT,
                fecha_registro TEXT
            )
        """)
        
        # Verificar si ya existe un registro para este archivo
        cur.execute("SELECT id FROM perfiles_cognitivos WHERE archivo = ?", (Path(ruta_pdf).name,))
        existing = cur.fetchone()
        
        if existing:
            # Actualizar registro existente
            cur.execute("""
                UPDATE perfiles_cognitivos SET
                    autor = ?, razonamiento_top3 = ?, modalidad_epistemica = ?,
                    estructura_silogistica = ?, ethos = ?, pathos = ?, logos = ?,
                    autor_confianza = ?, indice_teleologico = ?, roles_parrafos = ?, 
                    fecha_registro = ?, fecha_analisis = ?, fuente = ?, tipo_pensamiento = ?,
                    vector_path = COALESCE(vector_path, ?), 
                    texto_muestra = COALESCE(texto_muestra, ?),
                    formalismo = ?, creatividad = ?, dogmatismo = ?,
                    empirismo = ?, interdisciplinariedad = ?,
                    nivel_abstraccion = ?, complejidad_sintactica = ?,
                    uso_jurisprudencia = ?, total_palabras = ?
                WHERE archivo = ?
            """, (
                autor, razonamiento_json, modalidad, silogismo_json,
                ethos, pathos, logos, confianza, estructura_json, parrafos_json,
                datetime.now().isoformat(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                str(ruta_pdf), "Jurídico-Aristotélico",
                f"vectores/{Path(ruta_pdf).stem}.npy",
                f"Análisis cognitivo de {autor}"[:200],
                rasgos['formalismo'], rasgos['creatividad'], rasgos['dogmatismo'],
                rasgos['empirismo'], rasgos['interdisciplinariedad'],
                rasgos['nivel_abstraccion'], rasgos['complejidad_sintactica'],
                rasgos['uso_jurisprudencia'], total_palabras,
                Path(ruta_pdf).name
            ))
            print(f"🔄 Actualizado registro existente")
        else:
            # Insertar nuevo registro
            cur.execute("""
                INSERT INTO perfiles_cognitivos
                (archivo, autor, razonamiento_top3, modalidad_epistemica,
                 estructura_silogistica, ethos, pathos, logos,
                 autor_confianza, indice_teleologico, roles_parrafos, 
                 fecha_registro, fecha_analisis, fuente, tipo_pensamiento,
                 vector_path, texto_muestra,
                 formalismo, creatividad, dogmatismo, empirismo,
                 interdisciplinariedad, nivel_abstraccion,
                 complejidad_sintactica, uso_jurisprudencia, total_palabras)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                Path(ruta_pdf).name, autor, razonamiento_json, modalidad, silogismo_json,
                ethos, pathos, logos, confianza, estructura_json, parrafos_json,
                datetime.now().isoformat(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                str(ruta_pdf), "Jurídico-Aristotélico",
                f"vectores/{Path(ruta_pdf).stem}.npy",
                f"Análisis cognitivo de {autor}"[:200],
                rasgos['formalismo'], rasgos['creatividad'], rasgos['dogmatismo'],
                rasgos['empirismo'], rasgos['interdisciplinariedad'],
                rasgos['nivel_abstraccion'], rasgos['complejidad_sintactica'],
                rasgos['uso_jurisprudencia'], total_palabras
            ))
            print(f"➕ Creado nuevo registro")
        
        conn.commit()
        conn.close()
        
        print(f"✅ Guardado perfil cognitivo: {autor} ({Path(ruta_pdf).name})")
        print(f"   🎭 Retórica - E:{ethos:.2f} P:{pathos:.2f} L:{logos:.2f}")
        print(f"   🏛️ Modalidad: {modalidad}")
        print(f"   👤 Confianza autor: {confianza:.2f}")
        print(f"   🧠 Rasgos - F:{rasgos['formalismo']:.2f} C:{rasgos['creatividad']:.2f} A:{rasgos['nivel_abstraccion']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error procesando {Path(ruta_pdf).name}: {str(e)}")
        return False

# ==========================================================
# 🔹 PROCESAMIENTO MASIVO
# ==========================================================
def procesar_carpeta_cognitiva_avanzada(carpeta_pdfs: str = None) -> dict:
    """Procesa todos los PDFs de una carpeta con análisis cognitivo completo."""
    carpeta = Path(carpeta_pdfs or PDFS_DIR)
    pdfs = list(carpeta.glob("*.pdf"))
    
    if not pdfs:
        print(f"⚠️ No se encontraron PDFs en: {carpeta}")
        return {
            "estado": "sin_archivos", 
            "carpeta": str(carpeta), 
            "total": 0, 
            "procesados_ok": 0, 
            "errores": 0
        }

    print(f"\n📚 Iniciando análisis cognitivo de {len(pdfs)} archivos...")
    print(f"📁 Carpeta: {carpeta}")
    print(f"🗃️ Base de datos: {DB_PATH}")
    print("=" * 70)
    
    stats = {
        "estado": "procesando", 
        "procesados_ok": 0, 
        "errores": 0, 
        "total": len(pdfs),
        "carpeta": str(carpeta)
    }
    resultados = []

    for i, pdf in enumerate(pdfs, 1):
        print(f"\n[{i}/{len(pdfs)}] Procesando: {pdf.name}")
        try:
            success = registrar_perfil_cognitivo_avanzado(str(pdf))
            if success:
                resultados.append({"archivo": pdf.name, "estado": "completado_full"})
                stats["procesados_ok"] += 1
            else:
                resultados.append({"archivo": pdf.name, "estado": "error", "detalle": "Procesamiento falló"})
                stats["errores"] += 1
        except Exception as e:
            resultados.append({"archivo": pdf.name, "estado": "error", "detalle": str(e)})
            stats["errores"] += 1
            print(f"❌ Error inesperado: {e}")

    stats.update({"estado": "completado", "resultados": resultados})
    
    print("\n" + "=" * 70)
    print("🎯 RESUMEN DE PROCESAMIENTO:")
    print(f"✅ Completados: {stats['procesados_ok']}")
    print(f"❌ Errores: {stats['errores']}")
    print(f"📊 Total: {stats['total']}")
    print(f"📈 Éxito: {(stats['procesados_ok']/stats['total']*100):.1f}%" if stats['total'] > 0 else "N/A")
    print("=" * 70)
    
    return stats

# ==========================================================
# 🔹 EJECUCIÓN DIRECTA
# ==========================================================
if __name__ == "__main__":
    print("🚀 INGESTA COGNITIVA - ANALYSER MÉTODO v3.1")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Directorio PDFs: {PDFS_DIR}")
    print(f"🗃️ Base de datos: {DB_PATH}")
    print("=" * 70)
    
    # Verificar que existe el directorio de PDFs
    if not PDFS_DIR.exists():
        print(f"❌ ERROR: Directorio de PDFs no encontrado: {PDFS_DIR}")
        print("💡 Asegúrate de colocar los PDFs en colaborative/data/pdfs/general/")
        sys.exit(1)
    
    # Procesar todos los archivos
    resultado_masivo = procesar_carpeta_cognitiva_avanzada(str(PDFS_DIR))
    
    estado_masivo = resultado_masivo.get("estado", "desconocido")
    if estado_masivo != "sin_archivos":
        try:
            ok = resultado_masivo.get("procesados_ok", 0)
            total = resultado_masivo.get("total", 0)
            err = resultado_masivo.get("errores", 0)
            
            print(f"\n🧾 ESTADÍSTICAS FINALES:")
            print(f"   📊 Procesados exitosamente: {ok}/{total}")
            print(f"   ❌ Errores: {err}")
            print(f"   📈 Tasa de éxito: {(ok/total*100):.1f}%" if total > 0 else "N/A")
            
            if err > 0:
                print(f"\n⚠️ ARCHIVOS CON ERRORES:")
                for r in resultado_masivo.get("resultados", []):
                    if r.get("estado") == "error":
                        print(f"   • {r['archivo']}: {r.get('detalle', 'Error desconocido')}")
            
        except Exception as e:
            print(f"⚠️ Error registrando estadísticas: {e}")
    else:
        print(f"ℹ️ No se encontraron archivos para procesar ({resultado_masivo.get('carpeta')}).")
        print("💡 Coloca archivos PDF en colaborative/data/pdfs/general/")

    # 🚀 NUEVO: Procesamiento con chunker inteligente si está disponible
    if USAR_CHUNKER_INTELIGENTE and estado_masivo != "sin_archivos":
        print("\n🔬 PROCESAMIENTO AVANZADO CON CHUNKER INTELIGENTE")
        print("=" * 70)
        try:
            procesar_chunks_inteligentes(str(PDFS_DIR))
        except Exception as e:
            print(f"⚠️ Error en procesamiento avanzado: {e}")
            print("💡 Sistema funcional con fragmentación estándar")
    
    print("\n🎉 Procesamiento completado.")
    print("🌐 Para ver los resultados, ejecuta: python end2end_webapp.py")
    print("=" * 70)


# ==========================================================
# 🔬 PROCESAMIENTO CON CHUNKER INTELIGENTE
# ==========================================================
def procesar_chunks_inteligentes(directorio_pdfs: str):
    """
    Procesa PDFs con chunker inteligente y guarda metadatos enriquecidos.
    Crea una base de datos secundaria con fragmentos contextuales.
    """
    if not USAR_CHUNKER_INTELIGENTE:
        print("ℹ️ Chunker inteligente no disponible")
        return
    
    print("📊 Generando fragmentos semánticos enriquecidos...")
    
    # Base de datos para chunks inteligentes
    chunks_db = DB_PATH.parent / "chunks_inteligentes.db"
    
    conn = sqlite3.connect(chunks_db)
    cur = conn.cursor()
    
    # Crear tabla para chunks enriquecidos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chunks_enriquecidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            archivo TEXT NOT NULL,
            autor TEXT,
            chunk_id INTEGER,
            texto TEXT NOT NULL,
            tema_principal TEXT,
            tipo_contenido TEXT,
            coherencia_interna REAL,
            nivel_tecnico REAL,
            palabras_clave TEXT,
            entidades_juridicas TEXT,
            inicio INTEGER,
            fin INTEGER,
            fecha_procesamiento DATETIME,
            embedding_disponible INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    
    chunker = ChunkerInteligente()
    pdfs_procesados = 0
    chunks_totales = 0
    
    # Procesar cada PDF
    for pdf_path in Path(directorio_pdfs).glob("*.pdf"):
        try:
            print(f"\n   📄 Procesando: {pdf_path.name}")
            
            # Extraer texto completo
            doc = fitz.open(str(pdf_path))
            texto_completo = ""
            for pagina in doc:
                texto_completo += pagina.get_text()
            doc.close()
            
            if len(texto_completo.strip()) < 100:
                print(f"      ⚠️ Texto insuficiente, omitiendo")
                continue
            
            # Obtener autor desde BD principal
            cur_autor = sqlite3.connect(DB_PATH).cursor()
            cur_autor.execute(
                "SELECT autor FROM perfiles_cognitivos WHERE archivo = ? LIMIT 1",
                (pdf_path.name,)
            )
            resultado = cur_autor.fetchone()
            autor = resultado[0] if resultado else "Desconocido"
            
            # Fragmentar con chunker inteligente
            chunks = chunker.fragmentar_por_coherencia(texto_completo)
            
            print(f"      ✅ {len(chunks)} fragmentos semánticos generados")
            
            # Guardar cada chunk
            for chunk in chunks:
                cur.execute("""
                    INSERT INTO chunks_enriquecidos 
                    (archivo, autor, chunk_id, texto, tema_principal, tipo_contenido,
                     coherencia_interna, nivel_tecnico, palabras_clave, entidades_juridicas,
                     inicio, fin, fecha_procesamiento)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pdf_path.name,
                    autor,
                    chunk['id'],
                    chunk['texto'],
                    chunk['tema_principal'],
                    chunk['tipo_contenido'],
                    chunk['coherencia_interna'],
                    chunk['nivel_tecnico'],
                    json.dumps(chunk['palabras_clave'], ensure_ascii=False),
                    json.dumps(chunk['entidades_juridicas'], ensure_ascii=False),
                    chunk['inicio'],
                    chunk['fin'],
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ))
            
            conn.commit()
            pdfs_procesados += 1
            chunks_totales += len(chunks)
            
        except Exception as e:
            print(f"      ❌ Error: {e}")
            continue
    
    conn.close()
    
    print(f"\n📊 RESUMEN CHUNKER INTELIGENTE:")
    print(f"   📄 PDFs procesados: {pdfs_procesados}")
    print(f"   🧩 Chunks generados: {chunks_totales}")
    print(f"   💾 Base de datos: {chunks_db}")
    print(f"   ✅ Fragmentación semántica completada")