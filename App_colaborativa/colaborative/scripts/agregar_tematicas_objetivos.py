"""
═══════════════════════════════════════════════════════════════════════
🎯 EXTRACTOR DE TEMÁTICAS Y OBJETIVOS PRINCIPALES
═══════════════════════════════════════════════════════════════════════

Agrega y puebla columnas para capturar:
1. objetivo_central: El objetivo/propósito principal de la obra
2. tematicas_principales: Temas centrales tratados (JSON list)
3. palabras_tema: Términos clave temáticos más frecuentes
4. resumen_ejecutivo: Síntesis de 2-3 oraciones del contenido

Fecha: 11 de noviembre de 2025
"""

import sqlite3
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter

try:
    import fitz  # PyMuPDF
except:
    print("⚠️ PyMuPDF no disponible. Instalar con: pip install PyMuPDF")
    fitz = None


class ExtractorTematicasObjetivos:
    """
    Extrae temáticas principales y objetivos de obras jurídicas.
    Usa análisis de texto inteligente y patrones específicos.
    """
    
    def __init__(self):
        # Patrones para detectar objetivos
        self.patrones_objetivo = [
            r'el\s+(?:objeto|objetivo|propósito|fin)\s+(?:de\s+)?(?:este|este\s+trabajo|la\s+presente\s+obra|este\s+estudio)\s+(?:es|consiste\s+en|radica\s+en)\s+([^.]+)',
            r'(?:nos\s+)?proponemos\s+([^.]+)',
            r'(?:este\s+trabajo|la\s+obra)\s+(?:busca|pretende|intenta|tiene\s+por\s+finalidad)\s+([^.]+)',
            r'el\s+presente\s+(?:trabajo|estudio|análisis)\s+(?:tiene\s+como\s+objetivo|se\s+propone)\s+([^.]+)',
            r'en\s+este\s+trabajo\s+(?:analizaremos|estudiaremos|examinaremos|abordaremos)\s+([^.]+)',
        ]
        
        # Patrones para detectar temáticas en títulos/subtítulos
        self.patrones_tematica = [
            r'^\s*(?:CAPÍTULO|CAPÍTULO|CAP\.|TÍTULO|SECCIÓN)\s+[IVX\d]+[:\.\s]+(.+)$',
            r'^\s*\d+\.\s+([A-ZÁÉÍÓÚÑ][^.]{10,80})$',  # Títulos numerados
            r'^\s*([A-ZÁÉÍÓÚÑ\s]{15,80})$',  # Títulos todo mayúsculas
        ]
        
        # Términos jurídicos comunes para identificar áreas temáticas
        self.areas_tematicas = {
            'procesal': ['proceso', 'procedimiento', 'juicio', 'tutela', 'medida cautelar', 'acción', 'demanda', 'sentencia'],
            'civil': ['contrato', 'obligación', 'responsabilidad civil', 'daño', 'persona', 'patrimonio', 'familia'],
            'constitucional': ['derechos fundamentales', 'constitución', 'garantías', 'amparo', 'hábeas corpus'],
            'penal': ['delito', 'pena', 'imputado', 'tipo penal', 'culpabilidad', 'antijuridicidad'],
            'administrativo': ['acto administrativo', 'función pública', 'servicio público', 'potestad', 'procedimiento administrativo'],
            'comercial': ['sociedad', 'empresa', 'comerciante', 'título valor', 'quiebra', 'concurso'],
            'laboral': ['trabajo', 'empleador', 'trabajador', 'contrato de trabajo', 'convenio colectivo'],
        }
    
    def extraer_texto_completo(self, ruta_pdf: str) -> str:
        """Extrae todo el texto del PDF"""
        if not fitz or not Path(ruta_pdf).exists():
            return ""
        
        try:
            doc = fitz.open(ruta_pdf)
            texto_completo = ""
            for page in doc:
                texto_completo += page.get_text() + "\n"
            doc.close()
            return texto_completo
        except Exception as e:
            print(f"Error extrayendo texto: {e}")
            return ""
    
    def extraer_primeras_paginas(self, ruta_pdf: str, num_paginas: int = 3) -> str:
        """Extrae texto de las primeras páginas (donde suele estar la introducción)"""
        if not fitz or not Path(ruta_pdf).exists():
            return ""
        
        try:
            doc = fitz.open(ruta_pdf)
            texto = ""
            for i in range(min(num_paginas, len(doc))):
                texto += doc[i].get_text() + "\n"
            doc.close()
            return texto
        except Exception as e:
            print(f"Error extrayendo primeras páginas: {e}")
            return ""
    
    def detectar_objetivo_central(self, texto: str) -> str:
        """
        Detecta el objetivo central de la obra usando patrones lingüísticos.
        """
        texto_lower = texto.lower()
        
        # Buscar en las primeras 5000 caracteres (introducción típica)
        texto_intro = texto_lower[:5000]
        
        for patron in self.patrones_objetivo:
            matches = re.finditer(patron, texto_intro, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                objetivo = match.group(1).strip()
                # Limpiar y validar
                if 30 <= len(objetivo) <= 300:  # Longitud razonable
                    return objetivo.capitalize()
        
        # Si no se encuentra objetivo explícito, inferir del título y primeros párrafos
        lineas = texto[:2000].split('\n')
        posibles_titulos = [l.strip() for l in lineas if 20 <= len(l.strip()) <= 100 and l.strip().isupper()]
        
        if posibles_titulos:
            return f"Análisis de {posibles_titulos[0].lower()}"
        
        return "No especificado explícitamente en el documento"
    
    def detectar_tematicas_principales(self, texto: str, top_n: int = 5) -> List[str]:
        """
        Detecta las temáticas principales mediante:
        1. Análisis de títulos/capítulos
        2. Frecuencia de términos jurídicos especializados
        3. Clustering semántico de conceptos
        """
        tematicas = []
        
        # 1. Extraer títulos de capítulos/secciones
        lineas = texto.split('\n')
        for linea in lineas:
            for patron in self.patrones_tematica:
                match = re.match(patron, linea.strip())
                if match:
                    titulo = match.group(1).strip()
                    if 10 <= len(titulo) <= 80:
                        tematicas.append(titulo)
        
        # 2. Identificar áreas temáticas por frecuencia de términos
        texto_lower = texto.lower()
        areas_detectadas = {}
        
        for area, terminos in self.areas_tematicas.items():
            count = sum(texto_lower.count(termino.lower()) for termino in terminos)
            if count > 0:
                areas_detectadas[area] = count
        
        # Ordenar por frecuencia y agregar top 2 áreas
        top_areas = sorted(areas_detectadas.items(), key=lambda x: x[1], reverse=True)[:2]
        for area, _ in top_areas:
            tematicas.append(f"Derecho {area}")
        
        # 3. Eliminar duplicados y retornar top_n
        tematicas_unicas = []
        seen = set()
        for t in tematicas:
            t_lower = t.lower()
            if t_lower not in seen:
                seen.add(t_lower)
                tematicas_unicas.append(t)
        
        return tematicas_unicas[:top_n]
    
    def extraer_palabras_tema(self, texto: str, top_n: int = 30) -> List[Tuple[str, int]]:
        """
        Extrae las palabras temáticas más importantes (sustantivos jurídicos).
        """
        # Limpiar texto
        texto_lower = texto.lower()
        
        # Remover palabras comunes no temáticas
        stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'al', 
                     'por', 'para', 'con', 'se', 'un', 'una', 'su', 'como', 'es', 'son',
                     'más', 'este', 'esta', 'este', 'ese', 'esa', 'también', 'sobre'}
        
        # Extraer palabras de 4+ caracteres
        palabras = re.findall(r'\b[a-záéíóúñ]{4,}\b', texto_lower)
        
        # Filtrar stopwords
        palabras_filtradas = [p for p in palabras if p not in stopwords]
        
        # Contar frecuencias
        contador = Counter(palabras_filtradas)
        
        return contador.most_common(top_n)
    
    def generar_resumen_ejecutivo(self, texto: str, objetivo: str, tematicas: List[str]) -> str:
        """
        Genera un resumen ejecutivo de 2-3 oraciones.
        """
        # Extraer primeras oraciones significativas
        oraciones = re.split(r'[.!?]\s+', texto[:2000])
        oraciones_validas = [o.strip() for o in oraciones if 50 <= len(o.strip()) <= 300]
        
        if len(oraciones_validas) >= 2:
            resumen = f"{oraciones_validas[0]}. {oraciones_validas[1]}."
        elif objetivo != "No especificado explícitamente en el documento":
            temas_str = ", ".join(tematicas[:3]) if tematicas else "diversos aspectos jurídicos"
            resumen = f"La obra tiene como objetivo {objetivo}. Aborda temáticas relacionadas con {temas_str}."
        else:
            temas_str = ", ".join(tematicas[:3]) if tematicas else "diversos temas jurídicos"
            resumen = f"El documento analiza {temas_str} desde una perspectiva jurídica especializada."
        
        return resumen[:500]  # Limitar longitud
    
    def analizar_documento(self, ruta_pdf: str) -> Dict:
        """
        Análisis completo de temáticas y objetivos de un documento.
        """
        print(f"\n📄 Analizando: {Path(ruta_pdf).name}")
        
        # Extraer texto completo
        texto_completo = self.extraer_texto_completo(ruta_pdf)
        
        if not texto_completo or len(texto_completo) < 500:
            return {
                "objetivo_central": "Error: No se pudo extraer texto del documento",
                "tematicas_principales": [],
                "palabras_tema": [],
                "resumen_ejecutivo": "Error en extracción de texto"
            }
        
        # Detectar objetivo
        print("  🎯 Detectando objetivo central...")
        objetivo = self.detectar_objetivo_central(texto_completo)
        
        # Detectar temáticas
        print("  📚 Identificando temáticas principales...")
        tematicas = self.detectar_tematicas_principales(texto_completo, top_n=5)
        
        # Extraer palabras tema
        print("  🔑 Extrayendo palabras temáticas...")
        palabras = self.extraer_palabras_tema(texto_completo, top_n=30)
        
        # Generar resumen
        print("  📝 Generando resumen ejecutivo...")
        resumen = self.generar_resumen_ejecutivo(texto_completo, objetivo, tematicas)
        
        return {
            "objetivo_central": objetivo,
            "tematicas_principales": tematicas,
            "palabras_tema": palabras,
            "resumen_ejecutivo": resumen
        }


def agregar_columnas_bd():
    """Agrega las nuevas columnas a la base de datos si no existen"""
    db_path = Path("colaborative/bases_rag/cognitiva/metadatos.db")
    
    if not db_path.exists():
        print(f"❌ No se encontró la base de datos en {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Verificar columnas existentes
    c.execute("PRAGMA table_info(perfiles_cognitivos)")
    columnas_existentes = [col[1] for col in c.fetchall()]
    
    nuevas_columnas = [
        ("objetivo_central", "TEXT"),
        ("tematicas_principales", "TEXT"),  # JSON array
        ("palabras_tema", "TEXT"),  # JSON array de tuplas (palabra, frecuencia)
        ("resumen_ejecutivo", "TEXT"),
        ("uso_ejemplos", "REAL")  # Esta faltaba
    ]
    
    columnas_agregadas = []
    
    for nombre_col, tipo_col in nuevas_columnas:
        if nombre_col not in columnas_existentes:
            try:
                c.execute(f"ALTER TABLE perfiles_cognitivos ADD COLUMN {nombre_col} {tipo_col}")
                columnas_agregadas.append(nombre_col)
                print(f"  ✅ Columna '{nombre_col}' agregada")
            except sqlite3.OperationalError as e:
                if "duplicate column name" not in str(e):
                    print(f"  ⚠️ Error agregando '{nombre_col}': {e}")
        else:
            print(f"  ℹ️ Columna '{nombre_col}' ya existe")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Proceso completado. {len(columnas_agregadas)} columnas agregadas.")
    return True


def actualizar_documentos_existentes():
    """Procesa todos los documentos existentes para extraer temáticas y objetivos"""
    db_path = Path("colaborative/bases_rag/cognitiva/metadatos.db")
    
    if not db_path.exists():
        print(f"❌ No se encontró la base de datos")
        return
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Obtener todos los documentos
    c.execute("SELECT id, autor, fuente FROM perfiles_cognitivos WHERE fuente IS NOT NULL")
    documentos = c.fetchall()
    
    print(f"\n📚 Encontrados {len(documentos)} documentos para procesar\n")
    
    extractor = ExtractorTematicasObjetivos()
    procesados = 0
    errores = 0
    
    for doc_id, autor, fuente in documentos:
        try:
            if not Path(fuente).exists():
                print(f"⚠️ Archivo no encontrado: {fuente}")
                errores += 1
                continue
            
            # Analizar documento
            resultado = extractor.analizar_documento(fuente)
            
            # Actualizar base de datos
            c.execute("""
                UPDATE perfiles_cognitivos 
                SET objetivo_central = ?,
                    tematicas_principales = ?,
                    palabras_tema = ?,
                    resumen_ejecutivo = ?
                WHERE id = ?
            """, (
                resultado['objetivo_central'],
                json.dumps(resultado['tematicas_principales'], ensure_ascii=False),
                json.dumps(resultado['palabras_tema'][:20], ensure_ascii=False),
                resultado['resumen_ejecutivo'],
                doc_id
            ))
            
            conn.commit()
            procesados += 1
            print(f"  ✅ Actualizado: {autor}")
            
        except Exception as e:
            print(f"  ❌ Error procesando {autor}: {e}")
            errores += 1
    
    conn.close()
    
    print(f"\n{'='*70}")
    print(f"📊 RESUMEN:")
    print(f"   • Documentos procesados: {procesados}")
    print(f"   • Errores: {errores}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    print("="*70)
    print("🎯 EXTRACTOR DE TEMÁTICAS Y OBJETIVOS")
    print("="*70)
    
    # Paso 1: Agregar columnas
    print("\n1️⃣ Agregando columnas a la base de datos...")
    if agregar_columnas_bd():
        # Paso 2: Actualizar documentos existentes
        print("\n2️⃣ Actualizando documentos existentes...")
        actualizar_documentos_existentes()
    
    print("\n✅ Proceso completado. Las nuevas columnas están disponibles en la base RAG.")
