#!/usr/bin/env python3
"""
DIAGNÓSTICO ESPECÍFICO - DETECCIÓN DE AUTORÍA
Analiza por qué el sistema no detecta autores reales correctamente
"""

import fitz
import json
from pathlib import Path
import re
import unicodedata
from datetime import datetime

PDFS_DIR = Path(__file__).resolve().parent / "colaborative" / "data" / "pdfs" / "general"

def analizar_deteccion_autor_especifico(pdf_path):
    """Análisis paso a paso de la detección de autoría en un PDF específico"""
    
    print(f"🔍 ANÁLISIS DETALLADO DE AUTORÍA: {Path(pdf_path).name}")
    print("=" * 60)
    
    try:
        doc = fitz.open(pdf_path)
        
        # 1. ANÁLISIS DE METADATOS
        print("📋 1. METADATOS DEL PDF:")
        metadata = doc.metadata
        for key, value in metadata.items():
            if value:
                print(f"   {key}: {value}")
        
        if not any(metadata.values()):
            print("   ⚠️ Sin metadatos útiles")
        
        # 2. ANÁLISIS DE LA PRIMERA PÁGINA (PORTADA)
        print(f"\n📄 2. ANÁLISIS DE PORTADA:")
        page = doc.load_page(0)
        page_text = page.get_text()
        
        print(f"   📏 Dimensiones: {page.rect.width} x {page.rect.height}")
        print(f"   📝 Caracteres en portada: {len(page_text)}")
        
        # Mostrar primeras líneas de la portada
        lines = page_text.split('\n')[:15]
        print(f"   📖 Primeras 15 líneas:")
        for i, line in enumerate(lines, 1):
            if line.strip():
                print(f"      {i:2d}: '{line.strip()}'")
        
        # 3. ANÁLISIS DE SPANS (LAYOUT DETALLADO)
        print(f"\n🎨 3. ANÁLISIS DE LAYOUT (SPANS):")
        data = page.get_text("dict")
        all_spans = []
        max_font_size = 0
        
        for block in data.get("blocks", []):
            if "lines" in block:  # Es un bloque de texto
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span.get("text", "").strip()
                        if text:
                            font_size = float(span.get("size", 0))
                            bbox = span.get("bbox", [0, 0, 0, 0])
                            font = span.get("font", "")
                            
                            all_spans.append({
                                "text": text,
                                "font_size": font_size,
                                "bbox": bbox,
                                "font": font
                            })
                            max_font_size = max(max_font_size, font_size)
        
        # Ordenar spans por posición y tamaño de fuente
        all_spans.sort(key=lambda x: (-x["font_size"], x["bbox"][1], x["bbox"][0]))
        
        print(f"   📊 Total spans encontrados: {len(all_spans)}")
        print(f"   📏 Tamaño de fuente máximo: {max_font_size}")
        print(f"   🔤 Top 10 spans por tamaño de fuente:")
        
        for i, span in enumerate(all_spans[:10], 1):
            font_rel = span["font_size"] / max_font_size if max_font_size > 0 else 0
            y_pos = span["bbox"][1]
            print(f"      {i:2d}: '{span['text'][:40]}' | Tamaño: {span['font_size']:.1f} ({font_rel:.2f}) | Y: {y_pos:.1f}")
        
        # 4. BUSCAR PATRONES DE NOMBRE
        print(f"\n👤 4. BÚSQUEDA DE PATRONES DE NOMBRE:")
        
        # Patrones comunes de nombres de autor
        nombre_patterns = [
            r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+",  # Nombre Apellido
            r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ]\.\s*[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+",  # Nombre A. Apellido
            r"^[A-ZÁÉÍÓÚÑ]+\s+[A-ZÁÉÍÓÚÑ]+",  # NOMBRE APELLIDO (mayúsculas)
            r"^Dr\.\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+",  # Dr. Nombre
            r"^Prof\.\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+",  # Prof. Nombre
        ]
        
        candidatos_nombre = []
        
        for span in all_spans:
            text = span["text"]
            for pattern in nombre_patterns:
                if re.match(pattern, text):
                    candidatos_nombre.append({
                        "texto": text,
                        "font_size": span["font_size"],
                        "posicion_y": span["bbox"][1],
                        "pattern": pattern
                    })
        
        if candidatos_nombre:
            print(f"   ✅ Candidatos encontrados: {len(candidatos_nombre)}")
            for i, candidato in enumerate(candidatos_nombre, 1):
                print(f"      {i}: '{candidato['texto']}' | Tamaño: {candidato['font_size']:.1f} | Y: {candidato['posicion_y']:.1f}")
        else:
            print(f"   ❌ No se encontraron patrones de nombre típicos")
        
        # 5. ANÁLISIS DE PRIMERAS 3 PÁGINAS (CONTEXTO)
        print(f"\n📚 5. ANÁLISIS DE CONTEXTO (3 primeras páginas):")
        
        context_text = ""
        for page_num in range(min(3, len(doc))):
            context_text += doc[page_num].get_text() + "\n"
        
        # Buscar patrones de autoría en el contexto
        author_context_patterns = [
            r"(?:por|autor|escrito por|de)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)",
            r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)(?:\s*\n|\s*$)",
            r"^\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)\s*$"
        ]
        
        autores_contexto = []
        for pattern in author_context_patterns:
            matches = re.findall(pattern, context_text, re.MULTILINE | re.IGNORECASE)
            autores_contexto.extend(matches)
        
        if autores_contexto:
            print(f"   ✅ Posibles autores en contexto:")
            for autor in set(autores_contexto):
                print(f"      • '{autor}'")
        else:
            print(f"   ❌ No se detectaron autores en el contexto")
        
        # 6. VERIFICAR QUÉ HACE EL ALGORITMO ACTUAL
        print(f"\n🤖 6. SIMULACIÓN DEL ALGORITMO ACTUAL:")
        
        # Simular el algoritmo de candidatos_autor_por_portada
        pw, ph = page.rect.width, page.rect.height
        candidatos_algoritmo = []
        
        for span in all_spans:
            text = span["text"]
            font_size = span["font_size"]
            bbox = span["bbox"]
            x0, y0, x1, y1 = bbox
            
            # Solo tercio superior
            if y0 <= ph * 0.38:
                # Calcular score
                rel = font_size / max_font_size if max_font_size > 0 else 0
                cx = (x0 + x1) / 2.0
                cent = 1.0 - min(1.0, abs(cx - pw/2.0) / (pw/2.0))
                
                # Verificar si parece nombre
                toks = text.split()
                if 2 <= len(toks) <= 6:
                    cap = sum(1 for t in toks if re.match(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ.-]*$", t))
                    init = any(re.match(r"^[A-ZÁÉÍÓÚÑ]\.$", t) for t in toks)
                    looks = 1.0 if cap >= 2 or init else 0.0
                else:
                    looks = 0.0
                
                score = 0.45 * cent + 0.35 * rel + 0.20 * looks
                
                if score > 0.3:  # Umbral mínimo
                    candidatos_algoritmo.append({
                        "texto": text,
                        "score": score,
                        "rel": rel,
                        "cent": cent,
                        "looks": looks,
                        "font_size": font_size,
                        "y": y0
                    })
        
        # Ordenar por score
        candidatos_algoritmo.sort(key=lambda x: x["score"], reverse=True)
        
        if candidatos_algoritmo:
            print(f"   ✅ Candidatos del algoritmo: {len(candidatos_algoritmo)}")
            for i, cand in enumerate(candidatos_algoritmo[:5], 1):
                print(f"      {i}: '{cand['texto'][:40]}' | Score: {cand['score']:.3f} | R:{cand['rel']:.2f} C:{cand['cent']:.2f} L:{cand['looks']:.2f}")
        else:
            print(f"   ❌ El algoritmo no encuentra candidatos válidos")
        
        doc.close()
        
        # 7. RECOMENDACIONES
        print(f"\n💡 7. DIAGNÓSTICO Y RECOMENDACIONES:")
        
        if candidatos_algoritmo:
            mejor_candidato = candidatos_algoritmo[0]
            if mejor_candidato["score"] > 0.7:
                print(f"   ✅ Detección probablemente correcta: '{mejor_candidato['texto']}'")
            elif mejor_candidato["score"] > 0.4:
                print(f"   ⚠️ Detección incierta: '{mejor_candidato['texto']}'")
            else:
                print(f"   ❌ Detección poco confiable: '{mejor_candidato['texto']}'")
        
        if not candidatos_nombre and not autores_contexto:
            print(f"   🔧 PROBLEMA: PDF sin patrones claros de autoría")
            print(f"   💡 Solución: Mejorar algoritmo para este tipo de documento")
        elif candidatos_nombre and not candidatos_algoritmo:
            print(f"   🔧 PROBLEMA: Algoritmo no detecta patrones visibles")
            print(f"   💡 Solución: Ajustar parámetros de score o umbral")
        
        print("=" * 60)
        
        return {
            "metadata": metadata,
            "candidatos_visuales": candidatos_nombre,
            "candidatos_contexto": autores_contexto,
            "candidatos_algoritmo": candidatos_algoritmo
        }
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None

def diagnostico_masivo_autoria():
    """Diagnóstico de todos los PDFs"""
    print("📊 DIAGNÓSTICO MASIVO DE DETECCIÓN DE AUTORÍA")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Carpeta: {PDFS_DIR}")
    print("=" * 70)
    
    pdfs = list(PDFS_DIR.glob("*.pdf"))
    
    if not pdfs:
        print("❌ No se encontraron PDFs para analizar")
        return
    
    for i, pdf_path in enumerate(pdfs, 1):
        print(f"\n[{i}/{len(pdfs)}] {pdf_path.name}")
        resultado = analizar_deteccion_autor_especifico(str(pdf_path))
        
        if i < len(pdfs):
            print("\n" + "-" * 70 + "\n")

if __name__ == "__main__":
    diagnostico_masivo_autoria()