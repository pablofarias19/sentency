# -*- coding: utf-8 -*-
"""
Extractor PDF Enriquecido con Perfil Cognitivo-Autoral (PCA)
Analiza estructura, metodología y perfiles cognitivos de documentos jurídicos.
"""

import os
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import PyPDF2
from collections import Counter

# ==========================================================
# 🔹 PERFIL COGNITIVO-AUTORAL
# ==========================================================
def analyze_author_thinking(section_text: str) -> Dict[str, Any]:
    """
    Analiza el perfil cognitivo-autoral de una sección de texto.
    Detecta: marco de referencia, críticas, motivo intelectual, estrategia y autores mencionados.
    """
    s = section_text.lower()
    perfil = {
        "marco_referencia": None,
        "critica_a": [],
        "motivo_intelectual": None,
        "estrategia": None,
        "autores_mencionados": []
    }

    # 1) Marco de referencia
    if re.search(r"foucault|habermas|weber|durkheim|bourdieu|luhmann", s):
        perfil["marco_referencia"] = "Sociológico / Filosófico"
    elif re.search(r"hayek|friedman|keynes|smith|schumpeter|becker", s):
        perfil["marco_referencia"] = "Económico / Liberal"
    elif re.search(r"kelsen|hart|ross|dworkin|ferrajoli|rawls|alexy", s):
        perfil["marco_referencia"] = "Jurídico / Garantista"
    elif re.search(r"marx|gramsci|lenin|althusser", s):
        perfil["marco_referencia"] = "Crítico / Materialista"
    elif re.search(r"arendt|heidegger|husserl|nietzsche", s):
        perfil["marco_referencia"] = "Filosófico / Existencial"
    elif re.search(r"constitucional|penal|civil|comercial|procesal|administrativo", s):
        perfil["marco_referencia"] = "Jurídico / Dogmático"
    else:
        perfil["marco_referencia"] = "No identificado"

    # 2) Crítica u oposición
    criticas = re.findall(r"(critica|cuestiona|refuta|rechaza|contradice)\s+(a\s+)?([A-Z][a-z]+)", s)
    if criticas:
        perfil["critica_a"] = list(set([c[2] for c in criticas]))

    # 3) Motivo intelectual
    if "problema" in s or "cuestión" in s or "dilema" in s:
        match = re.search(r"(problema|cuestión|dilema)\s+(central|principal|de|sobre)\s+([^\.]+)", s)
        if match:
            perfil["motivo_intelectual"] = clean_text(match.group(3))

    # 4) Estrategia intelectual
    if re.search(r"compara|contrasta|diferenc|analoga", s):
        perfil["estrategia"] = "Comparativa"
    elif re.search(r"propone|plantea|postula|formula|sugiere", s):
        perfil["estrategia"] = "Propositiva"
    elif re.search(r"describe|analiza|examina|explora", s):
        perfil["estrategia"] = "Analítica"
    elif re.search(r"critica|cuestiona|refuta", s):
        perfil["estrategia"] = "Crítica"
    elif re.search(r"expone|presenta|resume", s):
        perfil["estrategia"] = "Expositiva"
    else:
        perfil["estrategia"] = "No determinada"

    # 5) Autores mencionados (filtrado simple de nombres)
    autores = re.findall(r"\b([A-Z][a-z]{2,})\b", section_text)
    stop = {"El","La","Los","Las","Por","De","Del","En","Con","Para","Como","Y","Que","Sin","Son","Ser","Ver","Más","Una","Uno","Dos","Tres","Art","Inc","Ley","Cód","Cap","Tit","Sec"}
    perfil["autores_mencionados"] = list({a for a in autores if a not in stop})[:10]
    return perfil

# ==========================================================
# 🔹 ANÁLISIS METODOLÓGICO Y ESTRUCTURAL
# ==========================================================
def classify_methodology(text: str) -> str:
    """Clasifica la metodología jurídica predominante"""
    t = text.lower()
    
    # Metodologías jurídicas argentinas
    if re.search(r"jurisprudencia|fallo|sentencia|tribunal|corte|suprema", t):
        return "Jurisprudencial"
    elif re.search(r"doctrina|doctrinario|autor|doctrinarios|enseña", t):
        return "Doctrinaria"
    elif re.search(r"constitución|constitucional|derechos fundamentales|garantías", t):
        return "Constitucional"
    elif re.search(r"código civil|código penal|código procesal|normativa", t):
        return "Normativa"
    elif re.search(r"comparado|comparative|derecho extranjero", t):
        return "Comparada"
    elif re.search(r"histórico|historia del derecho|evolución|antecedentes", t):
        return "Histórica"
    else:
        return "Dogmática general"

def analyze_reasoning(text: str) -> str:
    """Analiza el tipo de razonamiento jurídico"""
    t = text.lower()
    
    if re.search(r"por lo tanto|en consecuencia|por ende|luego|entonces", t):
        return "Deductivo"
    elif re.search(r"casos similares|analogía|por ejemplo|análogamente", t):
        return "Analógico"
    elif re.search(r"principio|principios|fundamento|fundamentos", t):
        return "Principialista"
    elif re.search(r"finalidad|propósito|ratio|teleológico", t):
        return "Teleológico"
    elif re.search(r"literal|textual|expresamente|dice la ley", t):
        return "Literal"
    else:
        return "Mixto"

def evaluate_result_quality(text: str) -> str:
    """Evalúa la calidad argumentativa del resultado"""
    t = text.lower()
    
    score = 0
    if re.search(r"fundament|justific|razón|argumento", t): score += 1
    if re.search(r"cita|referencia|fuente|doctrina|jurisprudencia", t): score += 1
    if re.search(r"conclusión|concluye|resultado|por tanto", t): score += 1
    if re.search(r"crítica|análisis|evaluación|considera", t): score += 1
    
    if score >= 3: return "Sólido"
    elif score >= 2: return "Adecuado"
    else: return "Básico"

def clean_text(text: str) -> str:
    """Limpia y normaliza texto"""
    if not text:
        return ""
    # Remover caracteres especiales excesivos
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
    return text.strip()

def extract_metadata_from_text(text: str, filename: str) -> Dict[str, Any]:
    """Extrae metadatos del texto del PDF"""
    lines = text.split('\n')[:20]  # Primeras 20 líneas
    text_sample = ' '.join(lines).lower()
    
    # Detectar autor
    autor_match = re.search(r"autor[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+)", text_sample, re.IGNORECASE)
    autor = autor_match.group(1).title() if autor_match else "Autor no identificado"
    
    # Detectar año
    anio_match = re.search(r"(19|20)\d{2}", text_sample)
    anio = anio_match.group(0) if anio_match else "Sin año"
    
    # Detectar título (usar filename si no se encuentra)
    titulo_match = re.search(r"^(.{10,80})", text.strip())
    titulo = titulo_match.group(1).strip() if titulo_match else Path(filename).stem
    
    # Hash del documento
    doc_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:12]
    
    return {
        "titulo": titulo,
        "autor": autor,
        "anio": anio,
        "hash": doc_hash,
        "archivo": filename,
        "fecha_procesamiento": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def split_into_sections(text: str, chunk_size: int = 800) -> List[Dict[str, Any]]:
    """Divide el texto en secciones lógicas y chunks"""
    # Dividir por párrafos
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    sections = []
    current_section = ""
    current_title = "Introducción"
    
    for i, para in enumerate(paragraphs):
        # Detectar posibles títulos de sección
        if len(para) < 150 and (
            para.isupper() or 
            re.match(r'^[IVX]+\.', para) or 
            re.match(r'^\d+\.', para) or
            re.match(r'^[A-Z][a-z]+:', para)
        ):
            # Guardar sección anterior si tiene contenido
            if current_section.strip():
                sections.append({
                    "titulo": current_title,
                    "texto": current_section.strip(),
                    "posicion": len(sections) + 1
                })
            # Iniciar nueva sección
            current_title = para[:100]  # Limitar título
            current_section = ""
        else:
            current_section += para + "\n\n"
            
            # Si la sección es muy larga, crear chunk
            if len(current_section) > chunk_size:
                sections.append({
                    "titulo": current_title,
                    "texto": current_section.strip(),
                    "posicion": len(sections) + 1
                })
                current_title = f"{current_title} (cont.)"
                current_section = ""
    
    # Agregar última sección
    if current_section.strip():
        sections.append({
            "titulo": current_title,
            "texto": current_section.strip(),
            "posicion": len(sections) + 1
        })
    
    return sections

# ==========================================================
# 🔹 FUNCIÓN PRINCIPAL: EXTRACTOR ENRIQUECIDO
# ==========================================================
def extract_from_pdf_enriquecido(pdf_path: str) -> Dict[str, Any]:
    """
    Extrae contenido de PDF con análisis estructural y perfil cognitivo-autoral.
    Retorna formato compatible con el sistema RAG existente.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF no encontrado: {pdf_path}")
    
    # Extraer texto del PDF
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            for page in reader.pages:
                texto_completo += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error al leer PDF {pdf_path}: {str(e)}")
    
    if not texto_completo.strip():
        raise Exception(f"PDF vacío o sin texto extraíble: {pdf_path}")
    
    # Extraer metadatos
    meta = extract_metadata_from_text(texto_completo, pdf_path)
    
    # Dividir en secciones
    secciones = split_into_sections(texto_completo)
    
    # Procesar cada sección con análisis completo
    chunks_procesados = []
    for sec in secciones:
        # Análisis metodológico tradicional
        metodo = classify_methodology(sec["texto"])
        razon = analyze_reasoning(sec["texto"])
        resultado = evaluate_result_quality(sec["texto"])
        
        # 🆕 PERFIL COGNITIVO-AUTORAL
        perfil_autor = analyze_author_thinking(sec["texto"])
        
        # Crear labels completos
        labels = {
            "metodologia": metodo,
            "razonamiento": razon,
            "resultado_adjetivo": resultado,
            "tema_especifico": sec["titulo"],
            "palabras_clave": []  # Se puede expandir con NLP más avanzado
        }
        
        # Integrar perfil cognitivo-autoral
        labels.update(perfil_autor)
        
        # Formato compatible con RAG existente
        chunk = {
            "texto": sec["texto"],
            "metadata": {
                "fuente": meta["archivo"],
                "titulo": sec["titulo"],
                "autor": meta["autor"],
                "anio": meta["anio"],
                "hash": meta["hash"],
                "seccion": sec["posicion"]
            },
            "labels": labels
        }
        chunks_procesados.append(chunk)
    
    # Estructura de retorno compatible
    return {
        "meta": meta,
        "chunks": chunks_procesados,
        "stats": {
            "total_chunks": len(chunks_procesados),
            "metodologias": Counter([c["labels"]["metodologia"] for c in chunks_procesados]),
            "marcos_referencia": Counter([c["labels"]["marco_referencia"] for c in chunks_procesados]),
            "estrategias": Counter([c["labels"]["estrategia"] for c in chunks_procesados])
        }
    }

# ==========================================================
# 🔹 FUNCIÓN DE PRUEBA
# ==========================================================
if __name__ == "__main__":
    # Crear directorio de prueba
    test_dir = Path("colaborative/data/pdfs/general")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    print("📄 Extractor PDF Enriquecido con PCA")
    print("Para probar, coloca un PDF en:", test_dir)
    
    # Buscar PDFs de prueba
    for pdf_file in test_dir.glob("*.pdf"):
        try:
            print(f"\n🔍 Procesando: {pdf_file}")
            resultado = extract_from_pdf_enriquecido(str(pdf_file))
            
            print(f"✅ Extraído: {resultado['meta']['titulo']}")
            print(f"📊 Chunks: {resultado['stats']['total_chunks']}")
            print(f"🎯 Metodologías: {dict(resultado['stats']['metodologias'])}")
            print(f"🧠 Marcos: {dict(resultado['stats']['marcos_referencia'])}")
            print(f"⚡ Estrategias: {dict(resultado['stats']['estrategias'])}")
            
        except Exception as e:
            print(f"❌ Error procesando {pdf_file}: {e}")