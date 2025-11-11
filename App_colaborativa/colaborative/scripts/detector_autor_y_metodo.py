# -*- coding: utf-8 -*-
"""
===========================================================
  DETECTOR DE AUTOR Y MÉTODO JURÍDICO – ANALYSER MÉTODO
===========================================================

Objetivos:
    1️⃣ Detectar autor principal y distinguir autores citados.
    2️⃣ Analizar notas al pie y bibliografía.
    3️⃣ Clasificar tipo de razonamiento (según tópicos y retórica).
    4️⃣ Generar un perfil cognitivo extendido para integrar a FAISS / SQLite.

Dependencias:
    pip install PyMuPDF spacy regex numpy
    python -m spacy download es_core_news_md
===========================================================
"""

import re
import fitz  # PyMuPDF
import numpy as np
from pathlib import Path
from typing import Dict, List
import json

# Intentar cargar spaCy, con fallback si no está disponible
try:
    import spacy
    nlp = spacy.load("es_core_news_md")
    SPACY_AVAILABLE = True
except:
    print("⚠️ spaCy no disponible. Usando regex para NER básico.")
    SPACY_AVAILABLE = False

# ----------------------------------------------------------
# 🔹 1. UTILIDADES PDF
# ----------------------------------------------------------
def extraer_texto_y_notas(ruta_pdf: str) -> Dict:
    """Extrae texto completo y notas al pie del PDF."""
    try:
        doc = fitz.open(ruta_pdf)
        texto_completo = ""
        notas_pie = []

        for page in doc:
            ph = page.rect.height
            blocks = page.get_text("blocks")
            font_sizes = [b[7] for b in blocks if len(b) >= 8]
            font_mean = np.mean(font_sizes) if font_sizes else 10

            for b in blocks:
                x0, y0, x1, y1, txt, *_ = b
                if not txt.strip():
                    continue
                # Detectar notas al pie por posición y tamaño de fuente
                if y0 > 0.85 * ph and (len(b) >= 8 and b[7] < font_mean - 0.5):
                    notas_pie.append(txt)
                texto_completo += txt + "\n"

        doc.close()
        return {"texto": texto_completo, "notas_pie": "\n".join(notas_pie)}
    
    except Exception as e:
        print(f"❌ Error extrayendo PDF {ruta_pdf}: {e}")
        return {"texto": "", "notas_pie": ""}

# ----------------------------------------------------------
# 🔹 2. DETECCIÓN DE AUTORES
# ----------------------------------------------------------
def detectar_autor_principal(ruta_pdf: str, texto: str) -> Dict:
    """
    Detecta el autor principal mediante portada, metadatos y NER.
    Devuelve autor y nivel de confianza.
    """
    try:
        doc = fitz.open(ruta_pdf)
        meta = doc.metadata
        primera_pagina = doc.load_page(0).get_text("text")
        doc.close()
    except:
        primera_pagina = texto[:2000]  # Fallback: primeros 2000 caracteres
        meta = {}

    candidatos = []

    # 1️⃣ Metadatos del PDF
    if meta.get("author"):
        candidatos.append((meta["author"], 0.4))

    # 2️⃣ Portada: "Por/Autor"
    patron_portada = r"(?i)(por|autor(?:a)?|escrito\s+por)[\s:]+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})"
    match = re.search(patron_portada, primera_pagina)
    if match:
        candidatos.append((match.group(2), 0.6))

    # 3️⃣ Patrones de autoría en portada
    patrones_autor = [
        r"(?i)dr\.?\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,2})",
        r"(?i)prof\.?\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,2})",
        r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,2})(?=\s*\n.*\d{4})"  # Nombre antes de año
    ]
    
    for patron in patrones_autor:
        match = re.search(patron, primera_pagina)
        if match:
            candidatos.append((match.group(1), 0.7))

    # 4️⃣ NER con spaCy si está disponible
    if SPACY_AVAILABLE:
        doc_nlp = nlp(primera_pagina[:1500])  # Limitar para eficiencia
        personas = [ent.text for ent in doc_nlp.ents if ent.label_ == "PER"]
        if personas:
            autor = max(personas, key=len)
            candidatos.append((autor, 0.3))

    # 5️⃣ NER básico con regex si spaCy no está disponible
    else:
        patron_nombres = r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,2})"
        nombres = re.findall(patron_nombres, primera_pagina[:1000])
        if nombres:
            # Filtrar nombres comunes/palabras no válidas
            nombres_filtrados = [n for n in nombres if not re.search(r"(?i)(derecho|civil|penal|código|ley|artículo)", n)]
            if nombres_filtrados:
                autor = max(nombres_filtrados, key=len)
                candidatos.append((autor, 0.2))

    # Seleccionar mejor candidato
    if candidatos:
        # Eliminar duplicados similares
        candidatos_unicos = []
        for autor, conf in candidatos:
            if not any(autor.lower() in c[0].lower() or c[0].lower() in autor.lower() for c in candidatos_unicos):
                candidatos_unicos.append((autor, conf))
        
        autor_final, confianza = max(candidatos_unicos, key=lambda x: x[1])
        return {"autor_principal": autor_final.strip(), "confianza": round(confianza, 2)}
    
    return {"autor_principal": "Autor no identificado", "confianza": 0.0}

def extraer_autores_citados(texto: str, notas: str) -> List[Dict]:
    """
    Extrae autores doctrinarios o citados desde texto y notas al pie.
    """
    patrones = [
        r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+),\s*([A-ZÁÉÍÓÚÑ]\.(?:\s*[A-ZÁÉÍÓÚÑ]\.)*)",  # Apellido, N. N.
        r"(?i)(?:según|conforme|cfr\.?|ver|vid\.?)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)",
        r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)\s*\(\s*\d{4}\s*\)",  # Autor (año)
        r"(?i)doctrina(?:riamente)?\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",
        r"(?i)enseña\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",
        r"(?i)sostiene\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)"
    ]

    texto_combinado = texto + "\n" + notas
    coincidencias = []
    
    for patron in patrones:
        matches = re.findall(patron, texto_combinado)
        for match in matches:
            if isinstance(match, tuple):
                # Para patrones con grupos múltiples, tomar el primer grupo válido
                autor = next((m for m in match if m and len(m) > 2), None)
            else:
                autor = match
            
            if autor:
                coincidencias.append(autor)

    # Filtrar y limpiar autores
    autores_filtrados = []
    for autor in set(coincidencias):
        autor = autor.strip()
        # Filtrar palabras que no son nombres de autores
        if (len(autor) > 3 and 
            not re.search(r"(?i)(artículo|código|ley|derecho|civil|penal|según|conforme)", autor) and
            re.search(r"[A-ZÁÉÍÓÚÑ]", autor)):
            
            ubicacion = "nota_pie" if autor in notas else "texto"
            autores_filtrados.append({"autor_citado": autor, "ubicacion": ubicacion})

    return autores_filtrados[:20]  # Limitar a 20 para evitar ruido

# ----------------------------------------------------------
# 🔹 3. CLASIFICACIÓN DE RAZONAMIENTO
# ----------------------------------------------------------
def clasificar_razonamiento(texto: str) -> List[Dict]:
    """
    Clasifica el tipo de razonamiento jurídico según tópicos aristotélicos.
    Devuelve top 3 con scores.
    """
    texto_lower = texto.lower()

    patrones = {
        "Deductivo": [
            r"en consecuencia", r"por tanto", r"se concluye que", r"por ende",
            r"de ello se desprende", r"resulta que", r"se sigue que"
        ],
        "Inductivo": [
            r"por ejemplo", r"v\.gr\.", r"casos?", r"se desprende que",
            r"en base a", r"a partir de", r"considerando que"
        ],
        "Analógico": [
            r"por analog(í|i)a", r"semejanza", r"comparable", r"similar",
            r"del mismo modo", r"paralelamente", r"mutatis mutandis"
        ],
        "Teleológico": [
            r"finalidad", r"función", r"propósito", r"utilidad social",
            r"ratio legis", r"espíritu de la ley", r"bien jurídico"
        ],
        "Sistémico": [
            r"sistema", r"estructura", r"coherencia", r"subsistema",
            r"ordenamiento", r"conjunto normativo", r"unidad del derecho"
        ],
        "Autoritativo": [
            r"según", r"conforme", r"doctrina", r"jurisprudencia", r"fallos",
            r"art\.", r"artículo", r"tribunal", r"corte", r"csjn"
        ],
        "A contrario": [
            r"a contrario", r"a sensu contrario", r"salvo", r"excepto",
            r"por el contrario", r"inversamente", r"en sentido opuesto"
        ],
        "Consecuencialista": [
            r"consecuencia", r"efecto", r"impacto", r"resultado", r"beneficio",
            r"perjuicio", r"ventaja", r"inconveniente"
        ]
    }

    pesos = {
        "Deductivo": 1.0, "Autoritativo": 0.9, "Teleológico": 0.8, "Sistémico": 0.8,
        "Inductivo": 0.7, "Analógico": 0.6, "A contrario": 0.6, "Consecuencialista": 0.5
    }

    scores = {}
    for tipo, expresiones in patrones.items():
        count = sum(len(re.findall(expr, texto_lower)) for expr in expresiones)
        # Normalizar por longitud del texto
        score = (count / len(texto.split()) * 1000) * pesos[tipo] if texto.split() else 0
        scores[tipo] = min(score, 1.0)  # Limitar a 1.0

    top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    return [{"clase": c, "score": round(s, 3)} for c, s in top3 if s > 0]

def detectar_componentes_retóricos(texto: str) -> Dict:
    """
    Evalúa la presencia de Ethos, Pathos y Logos (retórica aristotélica).
    """
    t = texto.lower()
    
    # Ethos: Autoridad, credibilidad
    ethos_patterns = [
        r"doctrina", r"autoridad", r"tribunal", r"jurisprudencia", r"csjn", r"scba",
        r"profesor", r"doctor", r"especialista", r"experto", r"catedrático"
    ]
    ethos = sum(len(re.findall(p, t)) for p in ethos_patterns)
    
    # Pathos: Emoción, valores
    pathos_patterns = [
        r"injusticia", r"grave", r"alarmante", r"daño", r"moral", r"ético",
        r"inadmisible", r"repudiable", r"lesivo", r"perjudicial", r"dramático"
    ]
    pathos = sum(len(re.findall(p, t)) for p in pathos_patterns)
    
    # Logos: Lógica, razón
    logos_patterns = [
        r"porque", r"por tanto", r"si", r"entonces", r"en consecuencia", r"según",
        r"debido a", r"en virtud de", r"fundamentalmente", r"racionalmente"
    ]
    logos = sum(len(re.findall(p, t)) for p in logos_patterns)
    
    total = ethos + pathos + logos or 1
    return {
        "ethos": round(ethos / total, 3),
        "pathos": round(pathos / total, 3),
        "logos": round(logos / total, 3)
    }

# ----------------------------------------------------------
# 🔹 4. ANÁLISIS ADICIONAL
# ----------------------------------------------------------
def analizar_complejidad_sintactica(texto: str) -> float:
    """Analiza la complejidad sintáctica del texto."""
    oraciones = re.split(r'[.!?]+', texto)
    if not oraciones:
        return 0.0
    
    palabras_por_oracion = [len(oracion.split()) for oracion in oraciones if oracion.strip()]
    if not palabras_por_oracion:
        return 0.0
    
    complejidad = np.mean(palabras_por_oracion) / 20.0  # Normalizar
    return min(round(complejidad, 3), 1.0)

def detectar_nivel_tecnico(texto: str) -> Dict:
    """Detecta el nivel técnico del documento."""
    t = texto.lower()
    
    # Términos técnicos jurídicos
    terminos_tecnicos = [
        r"ratio decidendi", r"obiter dicta", r"res iudicata", r"ultra petita",
        r"iura novit curia", r"ne bis in idem", r"habeas corpus", r"mandamus",
        r"certiorari", r"amicus curiae", r"stare decisis", r"per se"
    ]
    
    # Latinismos
    latinismos = sum(len(re.findall(p, t)) for p in terminos_tecnicos)
    
    # Citas de artículos y leyes
    citas_legales = len(re.findall(r"art(?:ículo)?\.?\s*\d+", t))
    
    # Referencias doctrinarias
    referencias = len(re.findall(r"(?:cfr\.|ver|vid\.|según)", t))
    
    total_palabras = len(texto.split())
    if total_palabras == 0:
        return {"nivel_tecnico": 0.0, "latinismos": 0, "citas_legales": 0, "referencias": 0}
    
    nivel = min((latinismos + citas_legales + referencias) / total_palabras * 100, 1.0)
    
    return {
        "nivel_tecnico": round(nivel, 3),
        "latinismos": latinismos,
        "citas_legales": citas_legales,
        "referencias": referencias
    }

# ----------------------------------------------------------
# 🔹 5. PERFIL COGNITIVO EXTENDIDO
# ----------------------------------------------------------
def generar_perfil_cognitivo_extendido(ruta_pdf: str) -> Dict:
    """
    Extrae texto, notas, autores, razonamiento y componentes retóricos.
    Genera un perfil cognitivo completo e integrable.
    """
    print(f"🔍 Analizando: {Path(ruta_pdf).name}")
    
    # Extraer contenido
    data = extraer_texto_y_notas(ruta_pdf)
    texto = data["texto"]
    notas = data["notas_pie"]
    
    if not texto.strip():
        print("⚠️ No se pudo extraer texto del PDF")
        return {"error": "No se pudo procesar el PDF"}
    
    print(f"📄 Texto extraído: {len(texto)} caracteres")
    print(f"📝 Notas al pie: {len(notas)} caracteres")
    
    # Análisis principal
    autor_ppal = detectar_autor_principal(ruta_pdf, texto)
    autores_citados = extraer_autores_citados(texto, notas)
    razonamiento = clasificar_razonamiento(texto)
    retorica = detectar_componentes_retóricos(texto)
    complejidad = analizar_complejidad_sintactica(texto)
    nivel_tecnico = detectar_nivel_tecnico(texto)
    
    # Construir perfil integrado
    perfil = {
        "metadata": {
            "archivo": Path(ruta_pdf).name,
            "total_palabras": len(texto.split()),
            "total_caracteres": len(texto),
            "notas_pie_detectadas": len(notas.split("\n")) if notas else 0
        },
        "autor_principal": autor_ppal,
        "autores_citados": autores_citados,
        "razonamiento_top3": razonamiento,
        "retorica": retorica,
        "complejidad_sintactica": complejidad,
        "nivel_tecnico": nivel_tecnico,
        "timestamp": str(np.datetime64('now'))
    }
    
    print(f"✅ Análisis completado:")
    print(f"   👤 Autor: {autor_ppal['autor_principal']} (confianza: {autor_ppal['confianza']})")
    print(f"   📚 Autores citados: {len(autores_citados)}")
    print(f"   🧭 Razonamiento principal: {razonamiento[0]['clase'] if razonamiento else 'No detectado'}")
    print(f"   🎭 Retórica dominante: {max(retorica, key=retorica.get) if retorica else 'No detectada'}")
    
    return perfil

# ----------------------------------------------------------
# 🔹 6. FUNCIONES DE INTEGRACIÓN
# ----------------------------------------------------------
def integrar_con_perfil_cognitivo_existente(perfil_extendido: Dict, perfil_base: Dict) -> Dict:
    """
    Integra el perfil extendido con un perfil cognitivo base existente.
    """
    perfil_integrado = perfil_base.copy()
    
    # Agregar campos del perfil extendido
    perfil_integrado.update({
        "autor_principal": perfil_extendido.get("autor_principal", {}),
        "autores_citados": perfil_extendido.get("autores_citados", []),
        "razonamiento_dominante": perfil_extendido.get("razonamiento_top3", [{}])[0].get("clase", "No detectado"),
        "ethos": perfil_extendido.get("retorica", {}).get("ethos", 0),
        "pathos": perfil_extendido.get("retorica", {}).get("pathos", 0),
        "logos": perfil_extendido.get("retorica", {}).get("logos", 0),
        "complejidad_sintactica": perfil_extendido.get("complejidad_sintactica", 0),
        "nivel_tecnico": perfil_extendido.get("nivel_tecnico", {}).get("nivel_tecnico", 0)
    })
    
    return perfil_integrado

def exportar_para_sqlite(perfil_extendido: Dict) -> Dict:
    """
    Prepara el perfil para inserción en SQLite.
    """
    return {
        "autor_principal": perfil_extendido.get("autor_principal", {}).get("autor_principal", ""),
        "autor_confianza": perfil_extendido.get("autor_principal", {}).get("confianza", 0.0),
        "autores_citados": json.dumps(perfil_extendido.get("autores_citados", []), ensure_ascii=False),
        "razonamiento_top3": json.dumps(perfil_extendido.get("razonamiento_top3", []), ensure_ascii=False),
        "ethos": perfil_extendido.get("retorica", {}).get("ethos", 0.0),
        "pathos": perfil_extendido.get("retorica", {}).get("pathos", 0.0),
        "logos": perfil_extendido.get("retorica", {}).get("logos", 0.0),
        "complejidad_sintactica": perfil_extendido.get("complejidad_sintactica", 0.0),
        "nivel_tecnico": perfil_extendido.get("nivel_tecnico", {}).get("nivel_tecnico", 0.0)
    }

# ----------------------------------------------------------
# 🔹 7. USO DIRECTO
# ----------------------------------------------------------
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("\n" + "="*60)
        print("🧠 DETECTOR DE AUTOR Y MÉTODO JURÍDICO – ANALYSER MÉTODO")
        print("="*60)
        print("\nUso: python detector_autor_y_metodo.py archivo.pdf")
        print("\nEjemplo:")
        print("  python detector_autor_y_metodo.py documento_juridico.pdf")
        print("\nEste módulo integra con tu sistema ANALYSER para:")
        print("  • Detectar autores principales y citados")
        print("  • Clasificar tipos de razonamiento jurídico")
        print("  • Analizar componentes retóricos (Ethos/Pathos/Logos)")
        print("  • Generar perfiles cognitivos extendidos")
        sys.exit(0)

    ruta = sys.argv[1]
    if not Path(ruta).exists():
        print(f"❌ Archivo no encontrado: {ruta}")
        sys.exit(1)

    print(f"\n📘 ANÁLISIS MÁSTER - ANALYSER MÉTODO")
    print("="*60)
    
    try:
        perfil = generar_perfil_cognitivo_extendido(ruta)
        
        if "error" in perfil:
            print(f"❌ {perfil['error']}")
            sys.exit(1)
        
        print(f"\n🧠 PERFIL COGNITIVO EXTENDIDO")
        print("-"*40)
        
        # Mostrar resultados organizados
        print(f"\n👤 AUTORÍA:")
        autor_info = perfil['autor_principal']
        print(f"   Autor principal: {autor_info['autor_principal']}")
        print(f"   Confianza: {autor_info['confianza']}")
        
        if perfil['autores_citados']:
            print(f"\n📚 AUTORES CITADOS ({len(perfil['autores_citados'])}):")
            for autor in perfil['autores_citados'][:5]:  # Mostrar primeros 5
                print(f"   • {autor['autor_citado']} ({autor['ubicacion']})")
        
        if perfil['razonamiento_top3']:
            print(f"\n🧭 RAZONAMIENTO JURÍDICO:")
            for i, r in enumerate(perfil['razonamiento_top3'], 1):
                print(f"   {i}. {r['clase']}: {r['score']}")
        
        print(f"\n🎭 RETÓRICA ARISTOTÉLICA:")
        ret = perfil['retorica']
        print(f"   Ethos (autoridad): {ret['ethos']}")
        print(f"   Pathos (emoción): {ret['pathos']}")
        print(f"   Logos (lógica): {ret['logos']}")
        
        print(f"\n📊 MÉTRICAS ADICIONALES:")
        print(f"   Complejidad sintáctica: {perfil['complejidad_sintactica']}")
        print(f"   Nivel técnico: {perfil['nivel_tecnico']['nivel_tecnico']}")
        print(f"   Latinismos: {perfil['nivel_tecnico']['latinismos']}")
        print(f"   Citas legales: {perfil['nivel_tecnico']['citas_legales']}")
        
        # Exportar resultado completo
        output_file = Path(ruta).stem + "_perfil_extendido.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(perfil, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Perfil completo guardado en: {output_file}")
        print("\n✅ Análisis completado exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)