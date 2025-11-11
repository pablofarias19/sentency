# ==========================================================
# ⚖️ ANALYSER MÉTODO – INGESTA COGNITIVA AVANZADA (v3.0)
# ==========================================================
# Este módulo:
#  - Analiza los PDF jurídicos desde una perspectiva cognitiva-aristotélica
#  - Detecta autor principal (layout + contexto semántico)
#  - Reconstruye índice teleológico (estructura conceptual)
#  - Clasifica párrafos por función lógica (expositivo, argumentativo, conclusivo, teleológico)
#  - Guarda resultados en SQLite + vector FAISS
# ==========================================================

from pathlib import Path
from datetime import datetime
import sqlite3
import json
import re
import fitz
import numpy as np
import unicodedata
from typing import Dict, List, Any

# Importar el analizador aristotélico mejorado
from detector_razonamiento_aristotelico import (
    analizar_pdf,
    extraer_autores_citados,
    clasificar_razonamiento_avanzado,
    detectar_modalidad_epistemica,
    detectar_estructura_silogistica,
    detectar_ethos_pathos_logos,
)

BASE_PATH = Path(__file__).resolve().parents[1]
PDFS_DIR = BASE_PATH / "data" / "pdfs" / "general"
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"

# ==========================================================
# 🔹 UTILIDADES INTERNAS – AUTORÍA MEJORADA
# ==========================================================
def __normalizar_espacios(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def __es_posible_nombre(s: str) -> bool:
    toks = s.strip().split()
    if not (2 <= len(toks) <= 6):
        return False
    cap = sum(1 for t in toks if re.match(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ.-]*$", t))
    init = any(re.match(r"^[A-ZÁÉÍÓÚÑ]\.$", t) for t in toks)
    return cap >= 2 or init

def __score_centrado(x0, x1, pw):
    cx = (x0 + x1) / 2.0
    return 1.0 - min(1.0, abs(cx - pw/2.0) / (pw/2.0))

def __candidatos_autor_por_portada(page):
    """Detecta posibles autores en la portada (layout)."""
    pw, ph = page.rect.width, page.rect.height
    data = page.get_text("dict")
    spans = []
    max_fs = 0.0
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

    cand = []
    for txt, fs, (x0, y0, x1, y1) in spans:
        if y0 > ph * 0.38:
            continue
        rel = 0.0 if max_fs == 0 else fs / max_fs
        cent = __score_centrado(x0, x1, pw)
        looks = 1.0 if __es_posible_nombre(txt) else 0.0
        score = 0.45 * cent + 0.35 * rel + 0.20 * looks
        cand.append((txt, fs, (x0, y0, x1, y1), score))

    cand = [c for c in cand if c[1] >= max_fs * 0.5 or __es_posible_nombre(c[0])]
    cand.sort(key=lambda c: (c[2][1], c[2][0]))

    if not cand:
        return []

    # Combinar spans contiguos
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

def consolidar_autoria_layout_semantica(ruta_pdf, portada_text, metadata):
    """Funde layout + texto de primeras páginas para validar el autor."""
    try:
        doc = fitz.open(ruta_pdf)
        cand = __candidatos_autor_por_portada(doc.load_page(0))
        doc.close()
    except Exception:
        cand = []

    if cand:
        txt, fs, bbox, score = cand[0]
        txt = __normalizar_espacios(unicodedata.normalize("NFKC", txt))
        if txt.isupper():
            parts = [
                t if re.match(r"^[A-ZÁÉÍÓÚÑ]\.$", t) else t.capitalize()
                for t in txt.split()
            ]
            txt = " ".join(parts)
        autor_layout = {"nombre": txt, "confianza": round(score, 2), "fuente": "layout"}

        # validar por contexto
        try:
            doc = fitz.open(ruta_pdf)
            primeras = "\n".join([doc[i].get_text("text") for i in range(min(3, len(doc)))])
            doc.close()
            if autor_layout["nombre"].lower() in primeras.lower():
                autor_layout["confianza"] = min(1.0, autor_layout["confianza"] + 0.15)
                autor_layout["fuente"] = "layout+semantica"
        except:
            pass
        return autor_layout

    return {"nombre": "Autor no identificado", "confianza": 0.0, "fuente": "ninguna"}

# ==========================================================
# 🔹 DETECCIÓN DEL ÍNDICE Y ORDEN TELEOLÓGICO
# ==========================================================
def detectar_estructura_teleologica(texto: str):
    lineas = texto.splitlines()
    estructura = []
    teleologica = []
    for l in lineas:
        l_clean = l.strip()
        if re.match(r"^(CAP[IÍ]TULO|T[IÍ]TULO|SECCI[ÓO]N|[IVXLC]+\.)", l_clean.upper()):
            estructura.append(l_clean)
        elif re.match(r"^(\d+(\.\d+)*\s)", l_clean):
            estructura.append(l_clean)
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
def clasificar_parrafos_por_intencion(texto: str):
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
        roles.append({"texto": p[:120] + "...", "rol": rol})
    return roles

# ==========================================================
# 🔹 PERFIL COGNITIVO COMPLETO Y REGISTRO
# ==========================================================
def generar_perfil_aristotelico(path_pdf: str):
    d = analizar_pdf(path_pdf)
    autor = consolidar_autoria_layout_semantica(path_pdf, d["portada"], d["metadata"])
    citados = extraer_autores_citados(d["texto"], d["notas_pie"])
    razon = clasificar_razonamiento_avanzado(d["texto"])
    epist = detectar_modalidad_epistemica(d["texto"])
    silog = detectar_estructura_silogistica(d["texto"])
    reto = detectar_ethos_pathos_logos(d["texto"])
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

def registrar_perfil_cognitivo_avanzado(ruta_pdf: str):
    """Guarda el resultado en la base SQLite existente."""
    print(f"\n📘 Analizando {Path(ruta_pdf).name} ...")
    perfil = generar_perfil_aristotelico(ruta_pdf)
    
    # Extraer datos para inserción
    archivo = Path(ruta_pdf).name
    autor = perfil["obra"]["autor_principal"]["nombre"]
    fuente = perfil["obra"]["autor_principal"]["fuente"] or "desconocida"
    autor_confianza = perfil["obra"]["autor_principal"]["confianza"]
    
    razonamiento_json = json.dumps(perfil["analisis"]["razonamiento"]["top3"], ensure_ascii=False)
    modalidad = perfil["analisis"]["modalidad_epistemica"]["predominante"]["clase"]
    silogismo_json = json.dumps(perfil["analisis"]["silogismo"]["principal"], ensure_ascii=False)
    
    ethos = perfil["analisis"]["retorica"]["ethos"]
    pathos = perfil["analisis"]["retorica"]["pathos"] 
    logos = perfil["analisis"]["retorica"]["logos"]
    
    estructura_json = json.dumps(perfil["obra"]["estructura_teleologica"], ensure_ascii=False)
    parrafos_json = json.dumps(perfil["analisis"]["parrafos_clasificados"], ensure_ascii=False)
    autores_citados_json = json.dumps(perfil["obra"]["autores_citados"], ensure_ascii=False)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Insertar en la tabla existente con todos los campos requeridos
    vector_path = f"cognitivo_v3_{archivo}.npy"  # Generar nombre de vector
    
    cur.execute("""
        INSERT INTO perfiles_cognitivos
        (archivo, autor, fuente, vector_path, razonamiento_top3, modalidad_epistemica,
         estructura_silogistica, ethos, pathos, logos, autor_confianza,
         indice_teleologico, roles_parrafos, autores_citados, fecha_registro,
         tipo_pensamiento, formalismo, creatividad, dogmatismo, empirismo,
         interdisciplinariedad, nivel_abstraccion, complejidad_sintactica, 
         uso_jurisprudencia, tono, fecha_analisis)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        archivo, autor, fuente, vector_path, razonamiento_json, modalidad,
        silogismo_json, ethos, pathos, logos, autor_confianza,
        estructura_json, parrafos_json, autores_citados_json, datetime.now().isoformat(),
        "Aristotélico-Cognitivo", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "Formal", datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()
    print(f"✅ Guardado perfil cognitivo v3.0: {autor} ({archivo})")

# ==========================================================
# 🔹 PROCESAMIENTO MASIVO
# ==========================================================
def procesar_carpeta_cognitiva_avanzada(carpeta_pdfs: str = None):
    carpeta = Path(carpeta_pdfs or PDFS_DIR)
    pdfs = list(carpeta.glob("*.pdf"))
    if not pdfs:
        print("⚠️ No se encontraron archivos PDF.")
        return
    print(f"\n📚 Iniciando análisis cognitivo v3.0 de {len(pdfs)} archivos...")
    
    procesados = 0
    errores = 0
    
    for pdf in pdfs:
        try:
            registrar_perfil_cognitivo_avanzado(str(pdf))
            procesados += 1
        except Exception as e:
            print(f"❌ Error procesando {pdf.name}: {e}")
            errores += 1
    
    print(f"\n🎯 Análisis v3.0 completado: {procesados} exitosos, {errores} errores")

# ==========================================================
# 🔹 EJECUCIÓN DIRECTA
# ==========================================================
if __name__ == "__main__":
    print("🏛️ ANALYSER MÉTODO v3.0 - Sistema Cognitivo Integrado")
    print("="*60)
    procesar_carpeta_cognitiva_avanzada(str(PDFS_DIR))