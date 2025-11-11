# -*- coding: utf-8 -*-
"""
===========================================================
 DETECTOR ARISTOTÉLICO – ANALYSER MÉTODO (v2.0 Mejorada)
===========================================================

Funcionalidad:
  1️⃣ Detectar autor principal usando layout (posición, tamaño, centrado).
  2️⃣ Detectar autores citados (texto + notas al pie).
  3️⃣ Analizar razonamientos y modalidad epistémica.
  4️⃣ Detectar estructura silogística y métricas retóricas.
  5️⃣ Generar perfil cognitivo aristotélico completo y explicable.
===========================================================
"""

from __future__ import annotations
import re
import json
import math
import unicodedata
from pathlib import Path
from typing import Dict, List, Tuple, Any

import fitz  # PyMuPDF
import numpy as np

# Cargar modelo spaCy español
try:
    import spacy
    _NLP = spacy.load("es_core_news_md")
    SPACY_AVAILABLE = True
except Exception as e:
    print(f"⚠️ spaCy no disponible: {e}")
    print("💡 Instala con: pip install spacy && python -m spacy download es_core_news_md")
    _NLP = None
    SPACY_AVAILABLE = False

# ==========================================================
# 🔹 UTILIDADES PDF
# ==========================================================
def analizar_pdf(ruta_pdf: str) -> Dict[str, Any]:
    """Extrae texto, portada, notas al pie y metadatos del PDF."""
    try:
        doc = fitz.open(ruta_pdf)
        meta = doc.metadata or {}
        texto_completo = []
        notas_pie = []
        portada_text = ""

        for i, page in enumerate(doc):
            ph = page.rect.height
            blocks = page.get_text("blocks")
            font_sizes = [b[7] for b in blocks if len(b) >= 8 and isinstance(b[7], (int, float))]
            font_mean = float(np.mean(font_sizes)) if font_sizes else 10.0

            for b in blocks:
                if len(b) < 5:
                    continue
                x0, y0, x1, y1, txt = b[:5]
                if not isinstance(txt, str) or not txt.strip():
                    continue
                texto_completo.append(txt)
                fs = b[7] if len(b) >= 8 and isinstance(b[7], (int, float)) else font_mean
                if y0 > 0.85 * ph and fs < font_mean - 0.5:
                    notas_pie.append(txt)
            if i == 0:
                portada_text = page.get_text("text")

        doc.close()
        return {
            "metadata": meta,
            "portada": portada_text,
            "texto": "\n".join(texto_completo),
            "notas_pie": "\n".join(notas_pie)
        }
    except Exception as e:
        print(f"❌ Error procesando PDF {ruta_pdf}: {e}")
        return {
            "metadata": {},
            "portada": "",
            "texto": "",
            "notas_pie": "",
            "error": str(e)
        }

# ==========================================================
# 🔹 DETECCIÓN DE AUTOR (layout + texto)
# ==========================================================
def __normalizar_espacios(s: str) -> str:
    """Normaliza espacios en blanco múltiples."""
    return re.sub(r"\s+", " ", s).strip()

def __es_posible_nombre(s: str) -> bool:
    """Evalúa si un string parece un nombre de persona."""
    toks = s.strip().split()
    if not (2 <= len(toks) <= 6):
        return False
    cap = sum(1 for t in toks if re.match(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ.-]*$", t))
    init = any(re.match(r"^[A-ZÁÉÍÓÚÑ]\.$", t) for t in toks)
    return cap >= 2 or init

def __score_centrado(x0, x1, pw):
    """Calcula qué tan centrado está un elemento en la página."""
    cx = (x0 + x1) / 2.0
    return 1.0 - min(1.0, abs(cx - pw/2.0) / (pw/2.0))

def __candidatos_autor_por_portada(page) -> list:
    """Busca spans en el tercio superior que parezcan nombres usando análisis de layout."""
    pw, ph = page.rect.width, page.rect.height
    data = page.get_text("dict")
    spans = []
    max_fs = 0.0
    
    # Recopilar todos los spans con metadata
    for b in data.get("blocks", []):
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                txt = __normalizar_espacios(s.get("text", ""))
                if not txt:
                    continue
                x0, y0, x1, y1 = s.get("bbox", [0,0,0,0])
                fs = float(s.get("size", 0.0))
                max_fs = max(max_fs, fs)
                spans.append((txt, fs, (x0,y0,x1,y1)))

    # Filtrar y puntuar candidatos
    cand = []
    for txt, fs, (x0,y0,x1,y1) in spans:
        # Solo considerar tercio superior
        if y0 > ph * 0.38:
            continue
        if not re.search(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]", txt):
            continue
            
        # Calcular score compuesto
        rel = 0.0 if max_fs == 0 else fs / max_fs  # Tamaño relativo
        cent = __score_centrado(x0, x1, pw)        # Centrado
        looks = 1.0 if __es_posible_nombre(txt) else 0.0  # Parece nombre
        score = 0.45*cent + 0.35*rel + 0.20*looks
        cand.append((txt, fs, (x0,y0,x1,y1), score))
    
    # Filtrar por tamaño mínimo o que parezca nombre
    cand = [c for c in cand if c[1] >= max_fs*0.5 or __es_posible_nombre(c[0])]
    cand.sort(key=lambda c: (c[2][1], c[2][0]))  # Ordenar por posición
    
    if not cand:
        return []

    # Combinar spans contiguos (nombres en múltiples líneas)
    comb = []
    buf = None
    for c in cand:
        txt, fs, (x0,y0,x1,y1), sc = c
        if buf and abs(y0 - buf[3]) < 3.0:  # Misma línea aproximadamente
            buf[0] = __normalizar_espacios(buf[0] + " " + txt)
            buf[2] = min(buf[2], x0)
            buf[4] = max(buf[4], x1)
            buf[6] = max(buf[6], sc)
        else:
            if buf:
                comb.append((buf[0], buf[1], (buf[2],buf[3],buf[4],buf[5]), buf[6]))
            buf = [txt, fs, x0,y0,x1,y1, sc]
    if buf:
        comb.append((buf[0], buf[1], (buf[2],buf[3],buf[4],buf[5]), buf[6]))

    # Re-puntuar con bonificaciones
    fin = []
    for txt, fs, bbox, sc in comb:
        toks = txt.split()
        bonus = 0.0
        if any(re.match(r"^[A-ZÁÉÍÓÚÑ]\.$", t) for t in toks):  # Iniciales
            bonus += 0.1
        if 2 <= len(toks) <= 6:  # Longitud apropiada
            bonus += 0.1
        if len(txt) > 40:  # Penalizar textos muy largos
            bonus -= 0.15
        fin.append((txt, fs, bbox, max(0.0, min(1.0, sc+bonus))))
    
    fin.sort(key=lambda c: c[3], reverse=True)
    return fin

def detectar_autor_principal(ruta_pdf: str, portada: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Versión mejorada: layout + fallback metadata/regex/NER."""
    
    # 1️⃣ DETECCIÓN POR LAYOUT (PRIORIDAD MÁXIMA)
    try:
        doc = fitz.open(ruta_pdf)
        cand = __candidatos_autor_por_portada(doc.load_page(0))
        doc.close()
    except Exception as e:
        print(f"⚠️ Error en análisis de layout: {e}")
        cand = []

    if cand:
        txt, fs, bbox, score = cand[0]
        txt = __normalizar_espacios(unicodedata.normalize("NFKC", txt))
        
        # Normalizar texto en mayúsculas (OCR-ready)
        if txt.isupper():
            parts = [t if re.match(r"^[A-ZÁÉÍÓÚÑ]\.$", t) else t.capitalize()
                     for t in txt.split()]
            txt = " ".join(parts)
        
        # Bonificar si realmente parece nombre
        if __es_posible_nombre(txt):
            score = min(1.0, score + 0.15)
            
        return {"nombre": txt, "confianza": round(score,2), "fuente": "portada_layout"}

    # 2️⃣ METADATA DEL PDF
    autor_meta = (metadata or {}).get("author") or (metadata or {}).get("Author")
    if autor_meta and isinstance(autor_meta, str) and autor_meta.strip():
        return {"nombre": autor_meta.strip(), "confianza": 0.45, "fuente": "metadata"}

    # 3️⃣ "POR/AUTOR" EN PORTADA
    m = re.search(r"(?i)\b(por|autor(?:a)?)\s*[:]*\s+([A-ZÁÉÍÓÚÑ][^\n]+)", portada or "")
    if m:
        nombre = __normalizar_espacios(m.group(2))
        return {"nombre": nombre, "confianza": 0.50, "fuente": "portada_label"}

    # 4️⃣ NER CON SPACY (SI ESTÁ DISPONIBLE)
    if portada and SPACY_AVAILABLE:
        try:
            doc_nlp = _NLP(portada)
            persons = [ent.text.strip() for ent in doc_nlp.ents if ent.label_ == "PER"]
            if persons:
                return {"nombre": max(persons, key=len), "confianza": 0.30, "fuente": "portada_ner"}
        except Exception as e:
            print(f"⚠️ Error en NER: {e}")

    return {"nombre": "Autor no identificado", "confianza": 0.0, "fuente": None}

# ==========================================================
# 🔹 DETECCIÓN DE AUTORES CITADOS
# ==========================================================
def extraer_autores_citados(texto: str, notas: str) -> List[Dict[str, Any]]:
    """Busca patrones típicos de citas doctrinarias simplificado."""
    corpus = (texto or "") + "\n" + (notas or "")
    patrones = [
        r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+,\s*[A-ZÁÉÍÓÚÑ]\.",
        r"(?<=cfr\.\s)[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+",
        r"(?<=según\s)[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+"
    ]
    matches = []
    for p in patrones:
        matches += re.findall(p, corpus)
    unicos = sorted(set(matches))
    return [{"autor": a, "ubicacion": "nota_pie" if a in (notas or "") else "texto"} for a in unicos]

# ==========================================================
# 🔹 RAZONAMIENTOS, MODALIDAD, RETÓRICA, SILOGISMOS
# ==========================================================
def detectar_ethos_pathos_logos(texto: str) -> Dict[str, float]:
    """Análisis retórico aristotélico simplificado y eficiente."""
    t = (texto or "").lower()
    ethos = len(re.findall(r"(doctrina|autoridad|tribunal|csjn|scba|fallos)", t))
    pathos = len(re.findall(r"(injusticia|grave|moral|daño|alarma)", t))
    logos = len(re.findall(r"(porque|si|entonces|por tanto|en consecuencia)", t))
    total = max(1, ethos + pathos + logos)
    return {"ethos": round(ethos/total,2), "pathos": round(pathos/total,2), "logos": round(logos/total,2)}

# -----------------------------
# Clasificación de razonamiento (patrones avanzados)
# -----------------------------
_PATRONES_RAZ = {
    "Deductivo": r"(por tanto|en consecuencia|se concluye que|por ende|se sigue que|resulta que)",
    "Inductivo": r"(por ejemplo|v\.gr\.|en la mayoría de los casos|se desprende de|en general)",
    "Abductivo": r"(podría explicarse si|la hipótesis más plausible|mejor explicación|lo más razonable es suponer|probablemente)",
    "Analógico": r"(por analog(í|i)a|semejanza|comparable|similarmente|de modo similar|paralelamente)",
    "Teleológico": r"(finalidad|propósito|fin|función|utilidad social|para lograr|con el fin de|objetivo)",
    "Sistémico": r"(sistema|estructura|coherencia|subsistema|articulación normativa|conjunto|ordenamiento)",
    "Autoritativo": r"(según|conforme|doctrina|jurisprudencia|fallos|art\.|como sostiene|tribunal)",
    "A contrario": r"(a contrario|a sensu contrario|salvo|excepto|por el contrario|inversamente)",
    "Consecuencialista": r"(consecuencia|efecto|impacto|resultado|costo|beneficio|ventaja|desventaja)"
}

_PESOS_RAZ = {
    "Deductivo": 1.0, "Autoritativo": 0.9, "Abductivo": 0.85,
    "Inductivo": 0.8, "Analógico": 0.7, "Teleológico": 0.75,
    "Sistémico": 0.75, "A contrario": 0.6, "Consecuencialista": 0.6
}

def clasificar_razonamiento_avanzado(texto: str) -> Dict[str, Any]:
    """Clasificación aristotélica de tipos de razonamiento con explicaciones."""
    t = (texto or "").lower()
    scores = {}
    activaciones = {}
    ejemplos = {}
    
    for clase, patron in _PATRONES_RAZ.items():
        matches = re.findall(patron, t)
        hit = len(matches)
        activaciones[clase] = hit > 0
        # Normalizar por longitud del texto
        palabras = len(texto.split()) if texto else 1
        score_norm = min(1.0, (hit / palabras) * 1000 * _PESOS_RAZ[clase])
        scores[clase] = round(score_norm, 3)
        
        # Guardar ejemplo si hay match
        if matches and hit > 0:
            match_ejemplo = re.search(patron, t)
            if match_ejemplo:
                contexto = t[max(0, match_ejemplo.start()-50):match_ejemplo.end()+50]
                ejemplos[clase] = contexto.strip()

    top3 = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:3]
    explicacion = []
    
    for clase, score in top3:
        if score > 0:
            detalle = f"{clase} ({score})"
            if clase in ejemplos:
                detalle += f" - ej: '...{ejemplos[clase][:80]}...'"
            explicacion.append(detalle)
    
    if not explicacion:
        explicacion = ["Sin activaciones fuertes (texto neutro/ambivalente)"]

    return {
        "top3": [{"clase": c, "score": s} for c, s in top3],
        "activaciones": activaciones,
        "ejemplos": ejemplos,
        "explicacion": "; ".join(explicacion)
    }

# -----------------------------
# Modalidad epistémica (apodíctico, dialéctico, retórico, sofístico)
# -----------------------------
_PATRONES_EPIST = {
    "Apodíctico": r"(necesariamente|inevitablemente|no puede ser de otro modo|demuestra que|se prueba que|indudablemente)",
    "Dialéctico": r"(probable|plausible|opinión común|en la mayoría de los casos|razonable que|verosímil)",
    "Retórico": r"(es evidente para todos|como es sabido|resulta claro|obviamente|persuasivo|convincente)",
    "Sofístico": r"(falaz|sofisma|apariencia de verdad|aparentemente válido|engañoso|especioso)"
}

_PESOS_EPIST = {"Apodíctico": 1.0, "Dialéctico": 0.8, "Retórico": 0.6, "Sofístico": 0.5}

def detectar_modalidad_epistemica(texto: str) -> Dict[str, Any]:
    """Determina la modalidad epistémica predominante del razonamiento."""
    t = (texto or "").lower()
    scores = {}
    activaciones = {}
    ejemplos = {}
    
    for clase, patron in _PATRONES_EPIST.items():
        matches = re.findall(patron, t)
        hit = len(matches)
        activaciones[clase] = hit > 0
        palabras = len(texto.split()) if texto else 1
        score_norm = min(1.0, (hit / palabras) * 1000 * _PESOS_EPIST[clase])
        scores[clase] = round(score_norm, 3)
        
        # Ejemplo
        if matches and hit > 0:
            match_ejemplo = re.search(patron, t)
            if match_ejemplo:
                contexto = t[max(0, match_ejemplo.start()-30):match_ejemplo.end()+30]
                ejemplos[clase] = contexto.strip()
    
    top = max(scores.items(), key=lambda kv: kv[1]) if scores else ("No determinado", 0)
    
    return {
        "predominante": {"clase": top[0], "score": top[1]},
        "activaciones": activaciones,
        "ejemplos": ejemplos,
        "todas_puntuaciones": scores
    }

# -----------------------------
# Estructura silogística (heurística)
# -----------------------------
_QUANT_RE = {
    "A": r"\b(todos?|toda|todo|cada|cualquier)\b",
    "E": r"\b(ningún|ninguna|ninguno|jamás)\b", 
    "I": r"\b(algunos?|alguna|algun|ciertos?|varios?)\b",
}

def _conteo(patron: str, texto: str) -> int:
    return len(re.findall(patron, texto, flags=re.IGNORECASE))

def detectar_estructura_silogistica(texto: str) -> Dict[str, Any]:
    """
    Heurística textual para detectar estructuras silogísticas:
      - Busca combinaciones de cuantificadores y negaciones.
      - Estima figura por presencia de 'ningún', 'todos', 'algunos', y conectores.
    Nota: Es aproximado (texto natural ≠ forma lógica pura).
    """
    t = (texto or "")
    A = _conteo(_QUANT_RE["A"], t)
    E = _conteo(_QUANT_RE["E"], t)
    I = _conteo(_QUANT_RE["I"], t)
    # O aproximado: "algunos... no"
    ONO = len(re.findall(r"\balgunos?[^\.]{0,40}\bno\b", t, flags=re.IGNORECASE))

    # Suma de señales
    señales = {"A": A, "E": E, "I": I, "O": ONO}

    # Heurística de candidatos silogísticos clásicos:
    candidatos = []
    
    # Barbara (AAA-1): predominan 'Todos' y estructura conclusiva
    if A >= 2 and re.search(r"(por tanto|en consecuencia|se concluye)", t, re.I):
        candidatos.append(("Barbara (AAA-1)", 0.9))
    
    # Cesare (EAE-2): aparece 'Ningún' y 'Todos' con negación
    if E >= 1 and A >= 1:
        candidatos.append(("Cesare (EAE-2)", 0.75))
    
    # Darapti (AAI-3): dos premisas universales, conclusión particular
    if A >= 2 and I >= 1:
        candidatos.append(("Darapti (AAI-3)", 0.65))
    
    # Bramantip (AAI-4): similar a 4ta figura con condicionales
    if A >= 2 and I >= 1 and re.search(r"\b(si|entonces|si.*entonces)\b", t, re.I):
        candidatos.append(("Bramantip (AAI-4)", 0.6))
    
    # Ferio (EIO-1): premisa mayor negativa universal
    if E >= 1 and I >= 1 and ONO >= 1:
        candidatos.append(("Ferio (EIO-1)", 0.7))
    
    # Camestres (AEE-2): universal afirmativa + negativa
    if A >= 1 and E >= 2:
        candidatos.append(("Camestres (AEE-2)", 0.65))

    candidatos.sort(key=lambda kv: kv[1], reverse=True)
    principal = candidatos[0] if candidatos else ("No identificado", 0.0)

    # Análisis de conectores lógicos
    conectores = {
        "por_tanto": _conteo(r"por tanto", t),
        "si_entonces": _conteo(r"si.*entonces", t),
        "porque": _conteo(r"porque", t),
        "dado_que": _conteo(r"dado que", t)
    }

    return {
        "principal": {"nombre": principal[0], "confianza": principal[1]},
        "candidatos": [{"nombre": n, "confianza": s} for n, s in candidatos],
        "señales_cuantificadores": señales,
        "conectores_logicos": conectores,
        "total_señales": sum(señales.values()) + sum(conectores.values())
    }

# -----------------------------
# Perfil Aristotélico integral
# -----------------------------
def generar_perfil_aristotelico(path_pdf: str) -> Dict[str, Any]:
    """
    Genera un análisis aristotélico completo del documento PDF.
    Incluye autoría, razonamiento, modalidad epistémica, estructura silogística y retórica.
    """
    print(f"🏛️ Iniciando análisis aristotélico: {Path(path_pdf).name}")
    
    try:
        data = analizar_pdf(path_pdf)
        
        if "error" in data:
            return {
                "error": f"No se pudo procesar el PDF: {data['error']}",
                "archivo": str(Path(path_pdf).name)
            }
        
        texto = data["texto"]
        portada = data["portada"]
        meta = data["metadata"]

        if not texto.strip():
            return {
                "error": "No se pudo extraer texto del PDF",
                "archivo": str(Path(path_pdf).name)
            }

        print(f"📄 Texto extraído: {len(texto)} caracteres")
        
        # Análisis completo
        autor = detectar_autor_principal(path_pdf, portada, meta)
        citados = extraer_autores_citados(texto, data["notas_pie"])
        razonamiento = clasificar_razonamiento_avanzado(texto)
        epistemica = detectar_modalidad_epistemica(texto)
        silogismo = detectar_estructura_silogistica(texto)
        retorica = detectar_ethos_pathos_logos(texto)

        print(f"👤 Autor: {autor['nombre']} (confianza: {autor['confianza']})")
        print(f"📚 Autores citados: {len(citados)}")
        print(f"🧭 Razonamiento principal: {razonamiento['top3'][0]['clase'] if razonamiento['top3'] else 'No detectado'}")
        print(f"🏛️ Modalidad epistémica: {epistemica['predominante']['clase']}")
        print(f"📐 Estructura silogística: {silogismo['principal']['nombre']}")

        perfil = {
            "obra": {
                "archivo": str(Path(path_pdf).name),
                "autor_principal": autor,
                "autores_citados": citados,
                "estadisticas": {
                    "total_caracteres": len(texto),
                    "total_palabras": len(texto.split()),
                    "notas_pie": len(data["notas_pie"].split()) if data["notas_pie"] else 0
                }
            },
            "analisis": {
                "razonamiento": razonamiento,
                "modalidad_epistemica": epistemica,
                "estructura_silogistica": silogismo,
                "retorica": retorica,
            },
            "metadata": {
                "version": "v1.2-aristotelico-analyser",
                "timestamp": str(np.datetime64('now')),
                "notas": "Análisis heurístico sobre texto natural; para máxima precisión usar segmentación y lógica simbólica."
            }
        }
        
        print("✅ Análisis aristotélico completado")
        return perfil
        
    except Exception as e:
        print(f"❌ Error en análisis aristotélico: {e}")
        import traceback
        traceback.print_exc()
        return {
            "error": f"Error durante análisis: {str(e)}",
            "archivo": str(Path(path_pdf).name)
        }

# -----------------------------
# CLI
# -----------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("\n" + "="*70)
        print("🏛️ DETECTOR ARISTOTÉLICO - RAZONAMIENTOS Y SILOGISMOS")
        print("="*70)
        print("\nUso: python detector_razonamiento_aristotelico.py archivo.pdf")
        print("\nEjemplo:")
        print("  python detector_razonamiento_aristotelico.py documento_juridico.pdf")
        print("\nEste módulo analiza:")
        print("  🧠 Tipos de razonamiento (deductivo, inductivo, abductivo, etc.)")
        print("  🏛️ Modalidad epistémica (apodíctico, dialéctico, retórico)")
        print("  📐 Estructura silogística (Barbara, Cesare, Darapti, etc.)")
        print("  🎭 Retórica aristotélica (Ethos/Pathos/Logos)")
        print("  👤 Detección de autores (principal y citados)")
        sys.exit(0)

    ruta = sys.argv[1]
    if not Path(ruta).exists():
        print(f"❌ Archivo no encontrado: {ruta}")
        sys.exit(1)
    
    perfil = generar_perfil_aristotelico(ruta)
    print("\n" + "="*70)
    print("📋 RESULTADO DEL ANÁLISIS ARISTOTÉLICO")
    print("="*70)
    print(json.dumps(perfil, ensure_ascii=False, indent=2))