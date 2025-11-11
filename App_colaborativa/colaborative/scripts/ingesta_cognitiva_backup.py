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
        doc = fitz.open(ruta_pdf)
        primeras = "\n".join([doc[i].get_text("text") for i in range(min(3, len(doc)))])
        doc.close()
        if autor_layout["nombre"].lower() in primeras.lower():
            autor_layout["confianza"] = min(1.0, autor_layout["confianza"] + 0.15)
            autor_layout["fuente"] = "layout+semantica"
        return autor_layout

    return {"nombre": "Autor no identificado", "confianza": 0.0, "fuente": None}

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
    """Guarda el resultado en la base SQLite."""
    print(f"\n📘 Analizando {Path(ruta_pdf).name} ...")
    perfil = generar_perfil_aristotelico(ruta_pdf)
    autor = perfil["obra"]["autor_principal"]["nombre"]
    confianza = perfil["obra"]["autor_principal"]["confianza"]
    razonamiento = perfil["analisis"]["razonamiento"]["top3"]
    razonamiento_json = json.dumps(razonamiento, ensure_ascii=False)
    modalidad = perfil["analisis"]["modalidad_epistemica"]["predominante"]["clase"]
    silogismo_json = json.dumps(perfil["analisis"]["silogismo"]["principal"], ensure_ascii=False)
    ethos = perfil["analisis"]["retorica"]["ethos"]
    pathos = perfil["analisis"]["retorica"]["pathos"]
    logos = perfil["analisis"]["retorica"]["logos"]
    estructura_json = json.dumps(perfil["obra"]["estructura_teleologica"], ensure_ascii=False)
    parrafos_json = json.dumps(perfil["analisis"]["parrafos_clasificados"], ensure_ascii=False)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS perfiles_cognitivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            archivo TEXT,
            autor TEXT,
            razonamiento_top3 TEXT,
            modalidad_epistemica TEXT,
            estructura_silogistica TEXT,
            ethos REAL,
            pathos REAL,
            logos REAL,
            autor_confianza REAL,
            indice_teleologico TEXT,
            roles_parrafos TEXT,
            fecha_registro TEXT
        )
    """)
    cur.execute("""
        INSERT INTO perfiles_cognitivos
        (archivo, autor, razonamiento_top3, modalidad_epistemica,
         estructura_silogistica, ethos, pathos, logos,
         autor_confianza, indice_teleologico, roles_parrafos, fecha_registro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        Path(ruta_pdf).name,
        autor,
        razonamiento_json,
        modalidad,
        silogismo_json,
        ethos, pathos, logos,
        confianza,
        estructura_json,
        parrafos_json,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    print(f"✅ Guardado perfil cognitivo: {autor} ({Path(ruta_pdf).name})")

# ==========================================================
# 🔹 PROCESAMIENTO MASIVO
# ==========================================================
def procesar_carpeta_cognitiva_avanzada(carpeta_pdfs: str = None):
    carpeta = Path(carpeta_pdfs or PDFS_DIR)
    pdfs = list(carpeta.glob("*.pdf"))
    if not pdfs:
        print("⚠️ No se encontraron archivos PDF.")
        return
    print(f"\n📚 Iniciando análisis cognitivo de {len(pdfs)} archivos...")
    for pdf in pdfs:
        try:
            registrar_perfil_cognitivo_avanzado(str(pdf))
        except Exception as e:
            print(f"❌ Error procesando {pdf.name}: {e}")
    print("\n🎯 Análisis completado. Resultados registrados en la base cognitiva.")

# ==========================================================
# 🔹 EJECUCIÓN DIRECTA
# ==========================================================
if __name__ == "__main__":
    procesar_carpeta_cognitiva_avanzada(str(PDFS_DIR))

    try:
        doc = fitz.open(ruta_pdf)
        metadatos["paginas"] = len(doc)
        for page_num in range(len(doc)):
            texto_pagina = doc.load_page(page_num).get_text()
            texto_completo += f"\n[Página {page_num + 1}]\n{texto_pagina}\n"
        doc.close()
    except Exception as e:
        print(f"⚠️ Error con PyMuPDF: {e}")
# ----------------------------------------------------------
# ANÁLISIS COGNITIVO COMPLETO
# ----------------------------------------------------------
def calcular_densidad_juridica(texto: str) -> float:
    terminos = ['derecho', 'ley', 'código', 'artículo', 'jurisprudencia', 'sentencia']
    palabras = texto.lower().split()
    if not palabras:
        return 0.0
    return min(sum(palabras.count(t) for t in terminos) / len(palabras), 1.0)

def calcular_complejidad_terminologica(texto: str) -> float:
    palabras = re.findall(r'\b\w+\b', texto.lower())
    if not palabras:
        return 0.0
    complejas = [p for p in palabras if len(p) > 8]
    return min(len(complejas) / len(palabras), 1.0)

def analizar_estructura_cognitiva(texto: str) -> Dict:
    return {
        "longitud": len(texto),
        "palabras": len(texto.split()),
        "densidad_juridica": calcular_densidad_juridica(texto),
        "complejidad_terminologica": calcular_complejidad_terminologica(texto)
    }

# ----------------------------------------------------------
# PROCESAMIENTO INDIVIDUAL
# ----------------------------------------------------------
def procesar_documento_completo(ruta_pdf: str) -> Dict:
    print(f"\n🔍 Procesando {Path(ruta_pdf).name}")
    resultado = {"archivo": ruta_pdf, "estado": "iniciado", "errores": []}

    try:
        # 1️⃣ Extracción básica
        texto, meta = extraer_texto_pdf(ruta_pdf)
        analisis_base = analizar_estructura_cognitiva(texto)
        vector = generar_embeddings_seguro(texto)

        # 2️⃣ 🧠 ANÁLISIS EXTENDIDO CON ANALYSER MÉTODO
        print("🧠 Aplicando ANALYSER MÉTODO...")
        perfil_extendido = generar_perfil_cognitivo_extendido(ruta_pdf)
        
        # 3️⃣ 🏛️ ANÁLISIS ARISTOTÉLICO AVANZADO
        print("🏛️ Aplicando DETECTOR ARISTOTÉLICO...")
        perfil_aristotelico = generar_perfil_aristotelico(ruta_pdf)
        
        if "error" not in perfil_extendido and "error" not in perfil_aristotelico:
            # Integrar ambos análisis con análisis base
            analisis_integrado = integrar_con_perfil_cognitivo_existente(perfil_extendido, analisis_base)
            
            # Obtener autor detectado (priorizar el aristotélico por mayor precisión)
            autor_aristotelico = perfil_aristotelico.get("obra", {}).get("autor_principal", {})
            autor_detectado = autor_aristotelico.get("nombre", "Desconocido")
            confianza_autor = autor_aristotelico.get("confianza", 0.0)
            
            # Información de razonamiento aristotélico
            razonamiento_info = perfil_aristotelico.get("analisis", {}).get("razonamiento", {})
            modalidad_info = perfil_aristotelico.get("analisis", {}).get("modalidad_epistemica", {})
            silogismos_info = perfil_aristotelico.get("analisis", {}).get("estructura_silogistica", {})
            retorica_info = perfil_aristotelico.get("analisis", {}).get("retorica", {})
            
            print(f"👤 Autor detectado: {autor_detectado} (confianza: {confianza_autor})")
            print(f"📚 Autores citados: {len(perfil_aristotelico.get('obra', {}).get('autores_citados', []))}")
            print(f"🧭 Razonamiento: {razonamiento_info.get('top3', [{}])[0].get('clase', 'No detectado')}")
            print(f"🏛️ Modalidad: {modalidad_info.get('predominante', {}).get('clase', 'No detectada')}")
            print(f"📐 Silogismo: {silogismos_info.get('principal', {}).get('nombre', 'No identificado')}")
            
            # Registrar perfil con información completa
            metadatos_completos = {
                "analyser_metodo": perfil_extendido,
                "aristotelico": perfil_aristotelico
            }
            
            path_vector = registrar_perfil(
                autor=autor_detectado,
                texto=texto,
                fuente=ruta_pdf,
                metadatos_extra=metadatos_completos
            )
            
            resultado.update({
                "estado": "completado_full",
                "analisis": analisis_integrado,
                "perfil_extendido": perfil_extendido,
                "perfil_aristotelico": perfil_aristotelico,
                "vector": path_vector,
                "autor_detectado": autor_detectado,
                "confianza_autor": confianza_autor,
                "razonamiento_principal": razonamiento_info.get('top3', [{}])[0].get('clase', 'No detectado'),
                "modalidad_epistemica": modalidad_info.get('predominante', {}).get('clase', 'No detectada'),
                "estructura_silogistica": silogismos_info.get('principal', {}).get('nombre', 'No identificado')
            })
            print(f"✅ Documento procesado con ANALYSER COMPLETO: {Path(ruta_pdf).name}")
            
        elif "error" not in perfil_extendido:
            # Solo ANALYSER MÉTODO disponible
            print("⚠️ Solo análisis MÉTODO disponible")
            analisis_integrado = integrar_con_perfil_cognitivo_existente(perfil_extendido, analisis_base)
            
            autor_detectado = perfil_extendido.get("autor_principal", {}).get("autor_principal", "Desconocido")
            confianza_autor = perfil_extendido.get("autor_principal", {}).get("confianza", 0.0)
            
            path_vector = registrar_perfil(
                autor=autor_detectado,
                texto=texto,
                fuente=ruta_pdf,
                metadatos_extra=perfil_extendido
            )
            
            resultado.update({
                "estado": "completado_metodo",
                "analisis": analisis_integrado,
                "perfil_extendido": perfil_extendido,
                "vector": path_vector,
                "autor_detectado": autor_detectado,
                "confianza_autor": confianza_autor
            })
            print(f"✅ Documento procesado con ANALYSER MÉTODO: {Path(ruta_pdf).name}")
            
        else:
            # Fallback al análisis básico
            print("⚠️ Usando análisis básico como fallback")
            path_vector = registrar_perfil(
                autor="Desconocido",
                texto=texto,
                fuente=ruta_pdf
            )
            
            resultado.update({
                "estado": "completado_basico",
                "analisis": analisis_base,
                "vector": path_vector,
                "advertencia": "Análisis avanzados fallaron, usando análisis básico"
            })
            print(f"✅ Documento procesado (modo básico): {Path(ruta_pdf).name}")

    except Exception as e:
        resultado["estado"] = "error"
        resultado["errores"].append(str(e))
        print(f"❌ Error procesando {ruta_pdf}: {e}")
        import traceback
        traceback.print_exc()

    return resultado

# ----------------------------------------------------------
# PROCESAMIENTO MASIVO
# ----------------------------------------------------------
def procesar_carpeta_cognitiva(carpeta_pdfs: str = None) -> Dict:
    carpeta = Path(carpeta_pdfs or PDFS_DIR)
    pdfs = list(carpeta.glob("*.pdf"))
    if not pdfs:
        return {"estado": "sin_archivos", "carpeta": str(carpeta)}

    print(f"\n📚 Iniciando ingesta cognitiva ({len(pdfs)} archivos)")
    stats = {"estado": "procesando", "procesados_ok": 0, "errores": 0, "total": len(pdfs)}

    resultados = []
    for pdf in pdfs:
        r = procesar_documento_completo(str(pdf))
        resultados.append(r)
        if r["estado"] == "completado":
            stats["procesados_ok"] += 1
        else:
            stats["errores"] += 1

    stats.update({
        "estado": "completado",
        "resultados": resultados
    })
    print(f"\n✅ Finalizado: {stats['procesados_ok']} OK, {stats['errores']} errores")
    return stats

# ----------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------------------------
if __name__ == "__main__":
    print("🚀 INGESTA COGNITIVA - ANALYSER MÉTODO")
    print("=" * 70)

    resultado_masivo = procesar_carpeta_cognitiva(str(PDFS_DIR))

    # --- 🔹 BLOQUE FINAL SEGURO ---
    estado_masivo = resultado_masivo.get("estado", "desconocido")

    if estado_masivo != "sin_archivos":
        try:
            procesados_ok = resultado_masivo.get("procesados_ok", 0)
            total_archivos = resultado_masivo.get("total", 0)
            errores = resultado_masivo.get("errores", 0)

            print(f"\n🧾 Estadísticas: {procesados_ok}/{total_archivos} completados, {errores} errores")
        except Exception as e:
            print(f"⚠️ Error registrando estadísticas: {e}")
    else:
        print(f"ℹ️ No se encontraron archivos para procesar ({estado_masivo}).")

    print("=" * 70)
