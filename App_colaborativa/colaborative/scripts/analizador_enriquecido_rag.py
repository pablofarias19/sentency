# =============================================================================
# --- EXTENSIÓN: Análisis de compilaciones con guardado y reporte ---
# =============================================================================
import sqlite3
import json
from datetime import datetime
from pathlib import Path

def analizar_compilacion_y_guardar(path_archivo: str, analizador, db_path: str = None, exportar_json: bool = True) -> dict:
    """
    Analiza una compilación de sentencias, guarda los resultados en la base de datos
    y genera un informe resumido para verificación.
    """
    print(f"\n⚖️ Analizando y registrando compilación: {path_archivo}")

    texto = analizador.extraer_texto_completo(path_archivo)
    if not texto:
        print("[!] No se pudo extraer texto del archivo.")
        return {"status": "error", "detalle": "no se extrajo texto"}

    sentencias = dividir_sentencias(texto)
    if not sentencias:
        print("[!] No se detectaron sentencias en la compilación.")
        return {"status": "error", "detalle": "no se detectaron sentencias"}

    print(f"📚 {len(sentencias)} sentencias detectadas. Iniciando análisis...")

    # Determinar ruta de base de datos
    if not db_path:
        base_path = Path(__file__).resolve().parents[1]
        db_path = base_path / "bases_rag" / "cognitiva" / "metadatos.db"
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    # Conexión a la base
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS perfiles_cognitivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            archivo TEXT,
            titulo_sentencia TEXT,
            autor TEXT,
            perfil_general TEXT,
            fecha_analisis TEXT,
            total_palabras INTEGER,
            palabras_clave TEXT,
            tipo_documento TEXT,
            metadata_json TEXT
        )
    """)

    resumen = {
        "archivo_compilacion": str(path_archivo),
        "fecha": datetime.now().isoformat(),
        "total_sentencias": len(sentencias),
        "registradas": 0,
        "errores": 0,
        "detalles": []
    }

    for i, s in enumerate(sentencias, 1):
        print(f"\n🧾 [{i}/{len(sentencias)}] Analizando: {s['titulo'][:80]}...")
        try:
            resultado = analizador.analizar_documento_completo(s['texto'], silent=True)
            discern = resultado.get("discernimiento", {})
            perfil = discern.get("perfil_general", "No determinado")
            palabras_clave = ", ".join(list(resultado.get("palabras_clave", {}).keys())[:10])
            total_palabras = resultado.get("estadisticas", {}).get("total_palabras", 0)

            cur.execute("""
                INSERT INTO perfiles_cognitivos
                (archivo, titulo_sentencia, autor, perfil_general, fecha_analisis,
                 total_palabras, palabras_clave, tipo_documento, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                Path(path_archivo).name,
                s['titulo'][:250],
                resultado.get("autor_referencia_principal", {}).get("nombre", "No identificado"),
                perfil,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                total_palabras,
                palabras_clave,
                "sentencia_compilada",
                json.dumps(resultado, ensure_ascii=False)[:5000]
            ))

            resumen["registradas"] += 1
            resumen["detalles"].append({
                "titulo": s["titulo"],
                "perfil": perfil,
                "autor": resultado.get("autor_referencia_principal", {}).get("nombre", "No identificado"),
                "palabras": total_palabras,
                "palabras_clave": palabras_clave.split(",")[:5],
                "analisis": resultado
            })
        except Exception as e:
            resumen["errores"] += 1
            resumen["detalles"].append({
                "titulo": s["titulo"],
                "error": str(e)
            })
            print(f"   [!] Error analizando sentencia: {e}")

    conn.commit()
    conn.close()

    print(f"\n✅ {resumen['registradas']} sentencias registradas correctamente ({resumen['errores']} con error).")

    # Informe TXT
    informe = (
        "\n📘 INFORME DE ANÁLISIS DE COMPILACIÓN\n"
        f"Archivo: {Path(path_archivo).name}\n"
        f"Fecha: {resumen['fecha']}\n"
        f"Sentencias analizadas: {resumen['total_sentencias']}\n"
        f"Registradas correctamente: {resumen['registradas']}\n"
        f"Con errores: {resumen['errores']}\n"
        "\n--- Detalle de sentencias ---\n"
    )
    for d in resumen["detalles"]:
        informe += f"• {d.get('titulo')[:100]} → Perfil: {d.get('perfil', 'N/A')} | Autor: {d.get('autor', '-')}\n"

    informe_path = Path(path_archivo).with_suffix(".informe.txt")
    with open(informe_path, "w", encoding="utf-8") as f:
        f.write(informe)
    print(f"\n🗂️ Informe generado en: {informe_path}")

    # Informe JSON
    if exportar_json:
        json_path = Path(path_archivo).with_suffix(".informe.json")
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(resumen, jf, ensure_ascii=False, indent=2)
        print(f"💾 Informe JSON generado: {json_path}")

    return resumen

# =============================================================================
# --- EXTENSIÓN: Verificación inteligente del informe por IA (segura) ---
# =============================================================================
import difflib

def verificar_informe_con_ia(reporte: dict, analizador, reanalizar_si_falla: bool = True) -> dict:
    """
    Verifica la coherencia y utilidad de los datos guardados.
    No inventa datos; solo marca, corrige o reanaliza fragmentos inválidos.
    """
    print("\n🤖 Iniciando verificación inteligente del informe...")
    if not reporte or "detalles" not in reporte:
        print("[!] No hay informe válido para verificar.")
        return {"estado": "error", "detalle": "informe inválido o vacío"}

    verificacion = {
        "total": len(reporte["detalles"]),
        "validos": 0,
        "invalidos": 0,
        "reanalizados": 0,
        "detalles": []
    }

    for item in reporte["detalles"]:
        titulo = item.get("titulo", "Sin título")
        perfil = item.get("perfil")
        palabras = item.get("palabras", 0)
        autor = item.get("autor", "No identificado")
        errores_previos = item.get("error")

        invalido = False
        razon = None

        if errores_previos:
            invalido = True
            razon = f"Error previo en análisis: {errores_previos}"
        elif palabras < 100:
            invalido = True
            razon = f"Texto demasiado breve ({palabras} palabras)"
        elif not perfil or perfil.strip() == "No determinado":
            invalido = True
            razon = "No se detectó perfil de discernimiento"
        elif titulo and any(
            difflib.SequenceMatcher(None, titulo.lower(), o["titulo"].lower()).ratio() > 0.9
            for o in verificacion["detalles"] if "titulo" in o
        ):
            invalido = True
            razon = "Título duplicado o redundante"

        if invalido:
            verificacion["invalidos"] += 1
            registro = {"titulo": titulo, "razon": razon, "accion": "Pendiente"}
            print(f"⚠️ Dato inválido: {titulo[:80]} → {razon}")

            if reanalizar_si_falla:
                try:
                    print(f"   🔄 Reanalizando sentencia: {titulo[:80]}...")
                    texto_reanalizado = item.get("analisis", {}).get("texto_completo", "")
                    if texto_reanalizado:
                        nuevo_resultado = analizador.analizar_documento_completo(texto_reanalizado, silent=True)
                        if nuevo_resultado and "discernimiento" in nuevo_resultado:
                            nuevo_perfil = nuevo_resultado["discernimiento"].get("perfil_general", "No determinado")
                            if nuevo_perfil != "No determinado":
                                registro["accion"] = f"Corregido (nuevo perfil: {nuevo_perfil})"
                                verificacion["reanalizados"] += 1
                            else:
                                registro["accion"] = "Reanalizado sin cambios"
                        else:
                            registro["accion"] = "Reanálisis sin resultado útil"
                    else:
                        registro["accion"] = "Texto no localizado"
                except Exception as e:
                    registro["accion"] = f"Error en reanálisis: {e}"

            verificacion["detalles"].append(registro)
        else:
            verificacion["validos"] += 1
            verificacion["detalles"].append({
                "titulo": titulo,
                "estado": "válido",
                "perfil": perfil,
                "autor": autor
            })

    resumen = (
        f"\n📊 VERIFICACIÓN FINAL\n"
        f"Total revisados: {verificacion['total']}\n"
        f"Válidos: {verificacion['validos']}\n"
        f"Inválidos: {verificacion['invalidos']}\n"
        f"Reanalizados exitosamente: {verificacion['reanalizados']}\n"
    )
    print(resumen)

    informe_path = Path(reporte["archivo_compilacion"]).with_suffix(".verificacion.txt")
    with open(informe_path, "w", encoding="utf-8") as f:
        f.write(resumen)
        for d in verificacion["detalles"]:
            linea = f"• {d['titulo'][:100]} → {d.get('accion', d.get('estado', ''))}\n"
            f.write(linea)
    print(f"🗂️ Verificación registrada en: {informe_path}")

    return verificacion
# =============================================================================
# --- EXTENSIÓN: Auditoría cruzada entre informe y base de datos (RAG-DB) ---
# =============================================================================
def auditar_informe_vs_base(reporte: dict, db_path: str = None) -> dict:
    """
    Audita la coherencia entre el informe de análisis y los registros guardados
    en la base 'metadatos.db'. No modifica datos: solo compara y reporta.
    """
    print("\n🧮 Iniciando auditoría cruzada RAG ↔ Base de Datos")
    import sqlite3
    from pathlib import Path

    if not reporte or "detalles" not in reporte:
        print("[!] Informe inválido o vacío.")
        return {"estado": "error", "detalle": "informe inválido"}

    if not db_path:
        base_path = Path(__file__).resolve().parents[1]
        db_path = base_path / "bases_rag" / "cognitiva" / "metadatos.db"

    if not Path(db_path).exists():
        print(f"[!] No se encontró la base en {db_path}")
        return {"estado": "error", "detalle": "base no encontrada"}

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT titulo_sentencia, perfil_general, autor, archivo FROM perfiles_cognitivos")
    registros_db = cur.fetchall()
    conn.close()

    resumen = {
        "total_informe": len(reporte["detalles"]),
        "total_db": len(registros_db),
        "coincidencias": 0,
        "faltantes_en_db": 0,
        "diferencias": 0,
        "detalles": []
    }

    def buscar_en_db(titulo):
        for (t, perfil, autor, archivo) in registros_db:
            if titulo.lower() in t.lower() or t.lower() in titulo.lower():
                return {"titulo": t, "perfil": perfil, "autor": autor, "archivo": archivo}
        return None

    for d in reporte["detalles"]:
        titulo = d.get("titulo", "Sin título")
        perfil_rag = d.get("perfil", "No determinado")
        autor_rag = d.get("autor", "No identificado")

        registro_db = buscar_en_db(titulo)

        if registro_db is None:
            resumen["faltantes_en_db"] += 1
            resumen["detalles"].append({
                "titulo": titulo,
                "estado": "❌ No encontrado en DB"
            })
            print(f"⚠️ No se encontró en DB: {titulo[:80]}")
            continue

        perfil_db = registro_db["perfil"]
        autor_db = registro_db["autor"]

        if perfil_db == perfil_rag and autor_db == autor_rag:
            resumen["coincidencias"] += 1
        else:
            resumen["diferencias"] += 1
            razon = []
            if perfil_db != perfil_rag:
                razon.append(f"Perfil distinto (DB: {perfil_db} / RAG: {perfil_rag})")
            if autor_db != autor_rag:
                razon.append(f"Autor distinto (DB: {autor_db} / RAG: {autor_rag})")
            resumen["detalles"].append({
                "titulo": titulo,
                "estado": "⚠️ Diferencias detectadas",
                "razon": "; ".join(razon)
            })
            print(f"⚠️ Diferencias en {titulo[:80]} → {razon}")

    informe_audit = (
        "\n📋 AUDITORÍA CRUZADA RAG ↔ BASE DE DATOS\n"
        f"Archivo: {Path(reporte['archivo_compilacion']).name}\n"
        f"Registros en informe: {resumen['total_informe']}\n"
        f"Registros en base: {resumen['total_db']}\n"
        f"Coincidencias exactas: {resumen['coincidencias']}\n"
        f"Faltantes en DB: {resumen['faltantes_en_db']}\n"
        f"Diferencias detectadas: {resumen['diferencias']}\n"
        "\n--- Detalle ---\n"
    )
    for d in resumen["detalles"]:
        informe_audit += f"• {d['titulo'][:100]} → {d['estado']}"
        if "razon" in d:
            informe_audit += f" ({d['razon']})"
        informe_audit += "\n"

    audit_path = Path(reporte["archivo_compilacion"]).with_suffix(".audit.txt")
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write(informe_audit)

    print(f"\n🗂️ Auditoría completada → {audit_path}")
    return resumen
# =============================================================================
# --- UTILIDAD: División automática de sentencias en compilaciones ---
# =============================================================================
import re

def dividir_sentencias(texto: str) -> list:
    """
    Divide un texto de compilación en sentencias individuales usando:
    - Títulos/capítulos/temas (CAPÍTULO, TEMA, CASO, SENTENCIA, Expediente, Causa, Autos)
    - Estructura de sentencia (VISTO, CONSIDERANDO, RESUELVO, FALLO)
    Devuelve una lista de dicts: {'titulo': ..., 'texto': ...}
    """
    # Patrón para títulos/capítulos/temas/expediente
    patron_titulo = re.compile(
        r'(CAP[IÍ]TULO\s+\d+|TEMA\s*:\s*[^\n]+|CASO\s*:\s*[^\n]+|SENTENCIA\s*\d+|Expediente\s*[^\n]+|Causa\s*[^\n]+|Autos\s*[^\n]+)',
        re.IGNORECASE
    )
    # Patrón para estructura de sentencia
    patron_sentencia = re.compile(
        r'(VISTO[\s\S]{0,500}?CONSIDERANDO[\s\S]{0,500}?RESUELVO[\s\S]{0,500}?FALLO[\s\S]{0,500}?)',
        re.IGNORECASE
    )

    # Buscar títulos y posiciones
    titulos = [(m.start(), m.group()) for m in patron_titulo.finditer(texto)]
    fragmentos = []

    if titulos:
        # Dividir por títulos
        for i, (pos, titulo) in enumerate(titulos):
            inicio = pos
            fin = titulos[i+1][0] if i+1 < len(titulos) else len(texto)
            fragmento = texto[inicio:fin]
            fragmentos.append({'titulo': titulo.strip(), 'texto': fragmento.strip()})
    else:
        # Si no hay títulos, buscar por estructura de sentencia
        for m in patron_sentencia.finditer(texto):
            fragmentos.append({'titulo': 'Sentencia detectada', 'texto': m.group().strip()})

    return fragmentos
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ANALIZADOR ENRIQUECIDO PARA INFORMES GEMINI
===============================================

Extrae información adicional de los PDFs para informes más completos:
- Autores citados y frecuencia de menciones
- Palabras clave jurídicas y frecuencias
- Conceptos centrales
- Posiciones doctrinales detectadas
- Estadísticas textuales avanzadas

FECHA: 11 NOV 2025
"""

import re
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import Counter
import json
from dataclasses import dataclass

try:
    import fitz  # PyMuPDF
except ImportError:
    print("⚠️ PyMuPDF no instalado. Ejecutar: pip install PyMuPDF")
    fitz = None


@dataclass
class PerfilHeuristico:
    """
    Estructura para ajustar pesos del análisis de discernimiento.
    Permite tunear la sensibilidad de cada indicador.
    """
    w_coherencia: float = 0.40
    w_resolutividad: float = 0.30
    w_tension: float = 0.50
    w_tension_pru: float = 0.50
    w_reflexividad_pru: float = 0.40
    w_principialismo_pru: float = 0.20


class AnalizadorEnriquecidoRAG:
    """Analiza documentos PDF para extraer información enriquecida"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.pdfs_path = self.base_path / "colaborative/data/pdfs/general"
        
        # Patrones para detectar autores
        self.patron_autores = re.compile(
            r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\b',
            re.UNICODE
        )
        
        # Palabras clave jurídicas comunes
        self.terminos_juridicos = {
            'tutela', 'derecho', 'norma', 'ley', 'código', 'constitución',
            'jurisprudencia', 'doctrina', 'tribunal', 'sentencia', 'fallo',
            'proceso', 'procedimiento', 'acción', 'recurso', 'demanda',
            'prueba', 'juicio', 'jurisdicción', 'competencia', 'legitimación',
            'responsabilidad', 'obligación', 'contrato', 'acuerdo', 'daño',
            'reparación', 'indemnización', 'sanción', 'pena', 'delito',
            'principio', 'garantía', 'protección', 'amparo', 'defensa',
            'derechos fundamentales', 'debido proceso', 'seguridad jurídica'
        }
        
        # Patrones de posicionamiento doctrinal
        self.patrones_posicion = {
            'a favor': re.compile(r'\b(estamos?\s+de\s+acuerdo|sostenemos?\s+que|consideramos?\s+que|propone?mos|defendemos?)\b', re.I),
            'en contra': re.compile(r'\b(rechaza?mos|nos\s+oponemos|criticamos?|cuestionamos?|discrepamos?)\b', re.I),
            'neutral': re.compile(r'\b(se\s+puede\s+sostener|algunos?\s+autores?|la\s+doctrina|existen\s+diferentes)\b', re.I),
            'critico': re.compile(r'\b(sin\s+embargo|no\s+obstante|por\s+el\s+contrario|a\s+pesar\s+de|cabe\s+señalar)\b', re.I)
        }
        
        # 🔍 PATRONES DE AUTORIDAD Y ÉNFASIS
        self.marcadores_autoridad = {
            'cita_libro': re.compile(r'"([^"]+)"\s*(?:\(|\[)([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+),?\s*(\d{4})', re.UNICODE),
            'cita_norma': re.compile(r'\b(ley|código|constitución|decreto|resolución|artículo|art\.?)\s+(?:n[°º]?\.?\s*)?(\d+)', re.I),
            'doctrina_establecida': re.compile(r'\b(doctrina\s+(?:mayoritaria|dominante|consolidada)|jurisprudencia\s+(?:constante|reiterada|pacífica))\b', re.I),
            'autoridad_reconocida': re.compile(r'\b(?:como\s+(?:bien\s+)?(?:señala|indica|sostiene|afirma|enseña)|según\s+la\s+(?:opinión|tesis)\s+de)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+)\b', re.I)
        }
        
        # Verbos imperativos y de obligación
        self.verbos_imperativos = re.compile(
            r'\b(debe[rn]?|tiene[n]?\s+que|es\s+(?:necesario|obligatorio|imperativo|imprescindible)|'
            r'hay\s+que|corresponde|procede|cabe|resulta\s+(?:necesario|obligatorio))\b', 
            re.I
        )
        
        # Afirmaciones universales
        self.afirmaciones_universales = re.compile(
            r'\b(siempre|nunca|todos?|ningún|jamás|en\s+todos?\s+los\s+casos|'
            r'invariablemente|necesariamente|indudablemente|evidentemente)\b',
            re.I
        )
        
        # Adjetivos de valoración personal
        self.adjetivos_valorativos = re.compile(
            r'\b(importante|fundamental|esencial|crucial|relevante|significativo|'
            r'trascendental|decisivo|determinante|valioso|inadecuado|erróneo|'
            r'incorrecto|acertado|correcto|apropiado|pertinente)\b',
            re.I
        )
        
        # Marcadores de énfasis
        self.marcadores_enfasis = re.compile(
            r'\b(muy|sumamente|extremadamente|altamente|especialmente|particularmente|'
            r'notablemente|significativamente|ciertamente|claramente|obviamente|'
            r'indiscutiblemente|sin\s+duda)\b',
            re.I
        )
        
        # Uso de "ejemplo/s"
        self.patron_ejemplos = re.compile(
            r'\b(por\s+ejemplo|v\.?\s*gr?\.?|verbigracia|así|tal\s+como|como\s+(?:ser|puede\s+verse)|'
            r'ejemplificando|a\s+modo\s+de\s+ejemplo|ilustrando)\b',
            re.I
        )
    
    def extraer_texto_completo(self, archivo_pdf: str, autoanalizar: bool = False) -> Optional[str]:
        """
        Extrae el texto completo de un PDF o TXT, con detección automática de tipo documental
        (sentencia vs doctrina), rutas absolutas o relativas compatibles con Windows y Linux,
        y opción para análisis automático integrado con AnalizadorIntegralRAG.

        Args:
            archivo_pdf: Ruta absoluta o relativa al documento (.pdf o .txt)
            autoanalizar: Si True, realiza el análisis completo automáticamente.

        Returns:
            str: Texto extraído limpio, o None si falla la lectura.
        """

        import os
        import re
        from pathlib import Path

        if not fitz:
            print("[!] PyMuPDF (fitz) no está disponible. Instalar con: pip install PyMuPDF")
            return None

        if not archivo_pdf or not isinstance(archivo_pdf, str):
            print("[!] No se proporcionó una ruta válida de archivo.")
            return None

        # 🔧 1️⃣ Normalizar ruta para compatibilidad multiplataforma
        archivo_pdf = archivo_pdf.strip().replace("\\", "/")
        pdf_path = Path(archivo_pdf)

        # Si la ruta es absoluta, resolverla directamente
        posibles_rutas = []
        if pdf_path.is_absolute():
            posibles_rutas.append(pdf_path.expanduser().resolve())
        else:
            # Buscar en ubicaciones posibles
            posibles_rutas.extend([
                self.pdfs_path / pdf_path.name,
                self.pdfs_path / archivo_pdf,
                Path.cwd() / pdf_path.name,
                Path.cwd() / archivo_pdf
            ])

        # Buscar la primera ruta válida
        pdf_final = next((p for p in posibles_rutas if p.exists()), None)

        if not pdf_final:
            print(f"[!] No se encontró el archivo: {archivo_pdf}")
            print(f"    🔎 Rutas probadas: {[str(p) for p in posibles_rutas]}")
            return None

        try:
            ext = pdf_final.suffix.lower()
            texto_completo = ""

            # 📘 2️⃣ Leer según el tipo de archivo
            if ext == ".pdf":
                with fitz.open(str(pdf_final)) as doc:
                    texto_completo = "\n".join(page.get_text("text") for page in doc)

            elif ext == ".txt":
                with open(pdf_final, "r", encoding="utf-8", errors="ignore") as f:
                    texto_completo = f.read()

            else:
                print(f"[!] Extensión no soportada ({ext}). Se admite solo .pdf o .txt")
                return None

            # 🧹 3️⃣ Limpieza avanzada del texto
            texto_completo = re.sub(r"\s+", " ", texto_completo)
            texto_completo = texto_completo.replace("ﬁ", "fi").replace("ﬂ", "fl")
            texto_completo = texto_completo.replace("¬", "").replace("–", "-")
            texto_completo = texto_completo.strip()

            if not texto_completo or len(texto_completo) < 50:
                print(f"[!] No se pudo extraer texto legible de {pdf_final}")
                return None

            # ⚖️ 4️⃣ Detección automática de tipo documental
            tipo_doc = "doctrina"
            patrones_sentencia = ["VISTO", "CONSIDERANDO", "RESUELVO", "FALLO", "AUTOS", "RESULTANDO"]
            if any(re.search(rf"\b{p}\b", texto_completo, re.IGNORECASE) for p in patrones_sentencia):
                tipo_doc = "sentencia"

            print(f"📄 Documento detectado: {tipo_doc.upper()} → {pdf_final.name}")

            # 🧠 5️⃣ Opción de análisis automático integrado
            if autoanalizar:
                try:
                    from colaborative.scripts.analizador_enriquecido_rag import AnalizadorIntegralRAGConMetadatos
                    analizador = AnalizadorIntegralRAGConMetadatos()
                    resultado = analizador.analizar_completo_texto(texto_completo, tipo=tipo_doc)
                    resultado["archivo"] = str(pdf_final)
                    print(f"✅ Análisis completado: {pdf_final.name}")
                    return resultado
                except Exception as e:
                    print(f"[!] Error en análisis automático: {e}")
                    return texto_completo

            return texto_completo

        except Exception as e:
            print(f"[!] Error leyendo {pdf_final}: {e}")
            return None
    
    def extraer_autores_citados(self, texto: str) -> Dict[str, int]:
        """
        Extrae autores mencionados y cuenta frecuencias
        Returns: {nombre_autor: frecuencia}
        """
        if not texto:
            return {}
        
        # Lista de palabras a excluir (artículos, preposiciones, términos comunes)
        palabras_excluidas = {
            'el artículo', 'la ley', 'el contrato', 'el cual', 'el caso', 'la cual',
            'el presente', 'la presente', 'el mismo', 'la misma', 'los cuales',
            'las cuales', 'el autor', 'la autora', 'los autores', 'las autoras',
            'la doctrina', 'la jurisprudencia', 'el tribunal', 'la sentencia',
            'el ordenamiento', 'la normativa', 'el derecho', 'la obligación',
            'el juez', 'la corte', 'el juzgado', 'la sala', 'el consejo',
            'se trate', 'se debe', 'se puede', 'se refiere', 'se establece'
        }
        
        # Buscar patrones de citación académica
        patrones_cita = [
            # Formato: "según Nombre Apellido"
            r'según\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})',
            # Formato: "Nombre Apellido sostiene/afirma/señala"
            r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\s+(?:sostiene|afirma|señala|considera|expresa|indica|manifiesta|argumenta|plantea)',
            # Formato: "como indica Nombre Apellido"
            r'como\s+(?:indica|señala|sostiene)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})',
            # Formato: "(Apellido, 2024)" - citas entre paréntesis
            r'\(([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,2}),\s*\d{4}\)',
            # Formato: "cfr. Nombre Apellido" o "v. Nombre Apellido"
            r'(?:cfr\.|cf\.|v\.|vid\.|véase)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})',
            # Formato: "en opinión de Nombre Apellido"
            r'en\s+opinión\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})',
            # Formato: "De Apellido" (nombres compuestos comunes)
            r'\b(De\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,2})\b',
        ]
        
        autores_encontrados = []
        for patron in patrones_cita:
            matches = re.findall(patron, texto, re.UNICODE)
            autores_encontrados.extend(matches)
        
        # Contar frecuencias
        contador = Counter(autores_encontrados)
        
        # Filtrar nombres muy cortos, palabras excluidas y comunes
        filtrados = {}
        for nombre, freq in contador.items():
            nombre_limpio = nombre.strip()
            nombre_lower = nombre_limpio.lower()
            
            # Excluir si:
            # 1. Es muy corto (menos de 6 caracteres)
            # 2. Está en la lista de exclusión
            # 3. Empieza con artículo ("el", "la", "los", "las")
            # 4. Solo aparece 1 vez (probablemente no es relevante)
            if (len(nombre_limpio) > 5 and 
                nombre_lower not in palabras_excluidas and
                not nombre_lower.startswith(('el ', 'la ', 'los ', 'las ', 'se ')) and
                freq > 1):
                filtrados[nombre_limpio] = freq
        
        return dict(sorted(filtrados.items(), key=lambda x: x[1], reverse=True))
    
    def extraer_palabras_clave(self, texto: str, top_n: int = 30) -> Dict[str, int]:
        """
        Extrae palabras clave jurídicas y su frecuencia
        Returns: {palabra: frecuencia}
        """
        if not texto:
            return {}
        
        texto_lower = texto.lower()
        palabras_encontradas = {}
        
        # Buscar términos jurídicos predefinidos
        for termino in self.terminos_juridicos:
            frecuencia = len(re.findall(r'\b' + re.escape(termino) + r'\b', texto_lower))
            if frecuencia > 0:
                palabras_encontradas[termino] = frecuencia
        
        # Buscar bigramas jurídicos comunes
        bigramas = re.findall(r'\b([a-záéíóúñ]+\s+[a-záéíóúñ]+)\b', texto_lower)
        contador_bigramas = Counter(bigramas)
        
        # Filtrar bigramas jurídicos (al menos 3 apariciones)
        for bigrama, freq in contador_bigramas.most_common(50):
            if freq >= 3 and any(term in bigrama for term in self.terminos_juridicos):
                palabras_encontradas[bigrama] = freq
        
        # Retornar top N
        return dict(sorted(palabras_encontradas.items(), key=lambda x: x[1], reverse=True)[:top_n])
    
    def detectar_posiciones_doctrinales(self, texto: str) -> Dict[str, List[str]]:
        """
        Detecta posicionamiento doctrinal del autor
        Returns: {tipo_posicion: [fragmentos_textuales]}
        """
        if not texto:
            return {}
        
        posiciones = {}
        
        for tipo, patron in self.patrones_posicion.items():
            matches = patron.finditer(texto)
            fragmentos = []
            
            for match in matches:
                # Extraer contexto (50 caracteres antes y después)
                start = max(0, match.start() - 50)
                end = min(len(texto), match.end() + 150)
                fragmento = texto[start:end].strip()
                fragmentos.append(fragmento)
            
            if fragmentos:
                posiciones[tipo] = fragmentos[:5]  # Máximo 5 ejemplos por tipo
        
        return posiciones
    
    def calcular_estadisticas_avanzadas(self, texto: str) -> Dict:
        """Calcula estadísticas textuales avanzadas"""
        if not texto:
            return {}
        
        palabras = texto.split()
        oraciones = re.split(r'[.!?]+', texto)
        parrafos = texto.split('\n\n')
        
        return {
            'total_palabras': len(palabras),
            'total_oraciones': len([o for o in oraciones if len(o.strip()) > 10]),
            'total_parrafos': len([p for p in parrafos if len(p.strip()) > 50]),
            'promedio_palabras_oracion': len(palabras) / max(len(oraciones), 1),
            'promedio_palabras_parrafo': len(palabras) / max(len(parrafos), 1),
            'vocabulario_unico': len(set(palabras)),
            'riqueza_lexica': len(set(palabras)) / max(len(palabras), 1)
        }
    
    def analizar_marcadores_autoridad(self, texto: str) -> Dict:
        """Analiza marcadores que indican autoridad y peso argumentativo"""
        if not texto:
            return {}
        
        resultado = {
            'citas_libros': [],
            'citas_normas': [],
            'doctrina_establecida': [],
            'autoridad_reconocida': [],
            'total_marcadores': 0
        }
        
        # Citas de libros/artículos
        for match in self.marcadores_autoridad['cita_libro'].finditer(texto):
            resultado['citas_libros'].append({
                'texto': match.group(1)[:100],
                'autor': match.group(2),
                'año': match.group(3)
            })
        
        # Citas normativas
        for match in self.marcadores_autoridad['cita_norma'].finditer(texto):
            resultado['citas_normas'].append({
                'tipo': match.group(1),
                'numero': match.group(2)
            })
        
        # Referencias a doctrina establecida
        resultado['doctrina_establecida'] = [
            match.group(0) 
            for match in self.marcadores_autoridad['doctrina_establecida'].finditer(texto)
        ]
        
        # Autoridades reconocidas
        for match in self.marcadores_autoridad['autoridad_reconocida'].finditer(texto):
            resultado['autoridad_reconocida'].append(match.group(1).strip())
        
        resultado['total_marcadores'] = (
            len(resultado['citas_libros']) +
            len(resultado['citas_normas']) +
            len(resultado['doctrina_establecida']) +
            len(resultado['autoridad_reconocida'])
        )
        
        return resultado
    
    def analizar_estilo_discursivo(self, texto: str) -> Dict:
        """Analiza el estilo discursivo: imperativos, afirmaciones, énfasis, valoraciones"""
        if not texto:
            return {}
        
        # Contar ocurrencias
        verbos_imperativos = self.verbos_imperativos.findall(texto)
        afirmaciones = self.afirmaciones_universales.findall(texto)
        adjetivos = self.adjetivos_valorativos.findall(texto)
        enfasis = self.marcadores_enfasis.findall(texto)
        ejemplos = self.patron_ejemplos.findall(texto)
        
        # Calcular densidad (por cada 100 palabras)
        total_palabras = len(texto.split())
        factor = 100.0 / max(total_palabras, 1)
        
        resultado = {
            'verbos_imperativos': {
                'total': len(verbos_imperativos),
                'densidad': len(verbos_imperativos) * factor,
                'mas_frecuentes': Counter(verbos_imperativos).most_common(5)
            },
            'afirmaciones_universales': {
                'total': len(afirmaciones),
                'densidad': len(afirmaciones) * factor,
                'mas_frecuentes': Counter(afirmaciones).most_common(5)
            },
            'adjetivos_valorativos': {
                'total': len(adjetivos),
                'densidad': len(adjetivos) * factor,
                'mas_frecuentes': Counter(adjetivos).most_common(10)
            },
            'marcadores_enfasis': {
                'total': len(enfasis),
                'densidad': len(enfasis) * factor,
                'mas_frecuentes': Counter(enfasis).most_common(5)
            },
            'uso_ejemplos': {
                'total': len(ejemplos),
                'densidad': len(ejemplos) * factor,
                'patrones': Counter(ejemplos).most_common(5)
            }
        }
        
        # Calcular índice de asertividad (imperativo + universal + énfasis)
        resultado['indice_asertividad'] = (
            resultado['verbos_imperativos']['densidad'] +
            resultado['afirmaciones_universales']['densidad'] +
            resultado['marcadores_enfasis']['densidad']
        ) / 3.0
        
        # Calcular índice de subjetividad (valoraciones + énfasis)
        resultado['indice_subjetividad'] = (
            resultado['adjetivos_valorativos']['densidad'] +
            resultado['marcadores_enfasis']['densidad']
        ) / 2.0
        
        return resultado
    
    def analizar_documento_completo(self, archivo_pdf: str, silent: bool = False) -> Dict:
        """
        Análisis completo del documento
        Args:
            archivo_pdf: Ruta al archivo PDF
            silent: Si es True, no imprime mensajes (util para Windows sin soporte emoji)
        Returns: Diccionario con toda la información enriquecida
        """
        if not silent:
            print(f"[*] Analizando: {archivo_pdf}")
        
        texto = self.extraer_texto_completo(archivo_pdf)
        if not texto:
            return {}
        
        if not silent:
            print("  [*] Extrayendo autores citados...")
        autores_citados = self.extraer_autores_citados(texto)
        
        if not silent:
            print("  [*] Analizando palabras clave juridicas...")
        palabras_clave = self.extraer_palabras_clave(texto)
        
        if not silent:
            print("  [*] Detectando posicionamiento doctrinal...")
        posiciones = self.detectar_posiciones_doctrinales(texto)
        
        if not silent:
            print("  [*] Analizando marcadores de autoridad...")
        autoridad = self.analizar_marcadores_autoridad(texto)
        
        if not silent:
            print("  [*] Analizando estilo discursivo...")
        estilo = self.analizar_estilo_discursivo(texto)
        
        if not silent:
            print("  [*] Calculando estadisticas avanzadas...")
        stats = self.calcular_estadisticas_avanzadas(texto)
        
        if not silent:
            print("  [*] Analizando discernimiento cognitivo/retorico...")
        try:
            discernimiento = AnalizadorDiscernimientoRAG().analizar_discernimiento(texto)
        except Exception as e:
            if not silent:
                print(f"     [!] Error en analisis de discernimiento: {e}")
            discernimiento = {}
        
        # ANALISIS DE CONDUCTA JUDICIAL (Psicologia Judicial Aplicada)
        if not silent:
            print("  [*] Analizando conducta y decision judicial...")
        try:
            conducta_judicial = AnalizadorConductaJudicialRAG().analizar_conducta(texto)
        except Exception as e:
            if not silent:
                print(f"     [!] Error en analisis de conducta judicial: {e}")
            conducta_judicial = {}
        
        resultado = {
            'archivo': archivo_pdf,
            'autores_citados': autores_citados,
            'palabras_clave': palabras_clave,
            'posiciones_doctrinales': posiciones,
            'marcadores_autoridad': autoridad,
            'estilo_discursivo': estilo,
            'discernimiento': discernimiento,
            'conducta_judicial': conducta_judicial,  # 🆕 NUEVO
            'estadisticas': stats,
            'texto_completo_disponible': True
        }
        
        # Identificar autor más citado
        if resultado['autores_citados']:
            mas_citado = max(resultado['autores_citados'].items(), key=lambda x: x[1])
            resultado['autor_referencia_principal'] = {
                'nombre': mas_citado[0],
                'menciones': mas_citado[1]
            }
        
        return resultado


class AnalizadorDiscernimientoRAG:
    """
    🧠 ANALIZADOR DE DISCERNIMIENTO COGNITIVO/RETÓRICO
    ===================================================
    
    Analiza criterios de discernimiento intelectual, ético, político y lógico.
    Se apoya en el análisis lingüístico para determinar:
    
    - Lógica argumentativa (coherencia, tensión dialéctica, resolutividad)
    - Discernimiento ético (juicio valorativo, equilibrio retórico)
    - Discernimiento jurídico (ratio decidendi, principialismo)
    - Discernimiento político/estratégico (pragmatismo, dogmatismo ideológico)
    - Autopercepción cognitiva (autoafirmación, reflexividad)
    
    Todas las métricas están normalizadas por 1000 palabras.
    """
    
    def __init__(self, perfil: Optional[PerfilHeuristico] = None):
        self.perfil = perfil or PerfilHeuristico()
        
        # 🔍 PATRONES PARA LÓGICA ARGUMENTATIVA
        self.conectores_condicionales = re.compile(
            r'\b(si|cuando|mientras|en\s+caso\s+de|de\s+modo\s+que|por\s+cuanto|'
            r'siempre\s+que|dado\s+que|puesto\s+que)\b', 
            re.I
        )
        
        self.conectores_concesivos = re.compile(
            r'\b(sin\s+embargo|aunque|no\s+obstante|a\s+pesar\s+de|pero|'
            r'pese\s+a|aun\s+cuando|si\s+bien)\b', 
            re.I
        )
        
        self.verbos_resolutivos = re.compile(
            r'\b(resuelve|dispone|determina|ordena|declara|concede|deniega|'
            r'establece|falla|sentencia|condena|absuelve)\b', 
            re.I
        )
        
        # 🎯 PATRONES PARA DISCERNIMIENTO JURÍDICO
        self.verbos_normativos = re.compile(
            r'\b(regula|norma|prescribe|estipula|consagra|reconoce|garantiza|'
            r'protege|tutela|ampara)\b', 
            re.I
        )
        
        self.principialismo = re.compile(
            r'\b(principio|valor|finalidad|proporcionalidad|justicia|razonabilidad|'
            r'equidad|axiología|teleología|bien\s+jurídico)\b', 
            re.I
        )
        
        # 💼 PATRONES PARA DISCERNIMIENTO POLÍTICO/ESTRATÉGICO
        self.verbos_pragmaticos = re.compile(
            r'\b(aplica|ejecuta|negocia|gestiona|implementa|propone|actúa|'
            r'desarrolla|concreta|materializa|instrumenta)\b', 
            re.I
        )
        
        self.ideologemas = re.compile(
            r'\b(siempre\s+se\s+debe|nunca\s+se\s+puede|es\s+evidente\s+que|'
            r'no\s+cabe\s+duda|resulta\s+claro|es\s+indiscutible)\b', 
            re.I
        )
        
        # 🤔 PATRONES PARA AUTOPERCEPCIÓN COGNITIVA
        self.reflexividad = re.compile(
            r'\b(puede\s+verse|parecería|cabe\s+preguntarse|conviene\s+analizar|'
            r'no\s+es\s+claro|podría|eventualmente|posiblemente|quizás?)\b', 
            re.I
        )
        
        self.pronombres_personales = re.compile(
            r'\b(yo|mi|me|mío|nosotros|nuestro|nuestra|nos)\b', 
            re.I
        )
        
        # 📊 PATRONES PARA JUICIO VALORATIVO
        self.adjetivos_etico_morales = re.compile(
            r'\b(justo|injusto|legítimo|ilegítimo|correcto|incorrecto|'
            r'apropiado|inapropiado|ético|inmoral|razonable|irrazonable|'
            r'prudente|imprudente|adecuado|inadecuado)\b', 
            re.I
        )
    
    def _dens(self, n: int, total_palabras: int) -> float:
        """Calcula densidad normalizada por 1000 palabras"""
        return (n * 1000.0) / max(total_palabras, 1)
    
    def analizar_discernimiento(self, texto: str) -> Dict[str, float]:
        """
        Análisis completo de discernimiento cognitivo/retórico
        Returns: Dict con todas las métricas normalizadas
        """
        if not texto:
            return {}
        
        total_palabras = len(texto.split())
        
        # 🔍 LÓGICA ARGUMENTATIVA
        condicionales = len(self.conectores_condicionales.findall(texto))
        concesivos = len(self.conectores_concesivos.findall(texto))
        resolutivos = len(self.verbos_resolutivos.findall(texto))
        
        # 🎯 DISCERNIMIENTO JURÍDICO
        normativos = len(self.verbos_normativos.findall(texto))
        principios = len(self.principialismo.findall(texto))
        
        # 💼 DISCERNIMIENTO POLÍTICO/ESTRATÉGICO
        pragmaticos = len(self.verbos_pragmaticos.findall(texto))
        ideologicos = len(self.ideologemas.findall(texto))
        
        # 🤔 AUTOPERCEPCIÓN COGNITIVA
        reflexivos = len(self.reflexividad.findall(texto))
        personales = len(self.pronombres_personales.findall(texto))
        
        # 📊 JUICIO VALORATIVO
        valorativos = len(self.adjetivos_etico_morales.findall(texto))
        
        # Calcular densidades
        metricas = {
            # Lógica Argumentativa
            'coherencia_interna': self._dens(condicionales, total_palabras),
            'tension_dialectica': self._dens(concesivos, total_palabras),
            'resolutividad': self._dens(resolutivos, total_palabras),
            
            # Discernimiento Jurídico
            'ratio_decidendi': self._dens(normativos, total_palabras),
            'principialismo': self._dens(principios, total_palabras),
            
            # Discernimiento Político/Estratégico
            'pragmatismo': self._dens(pragmaticos, total_palabras),
            'dogmatismo_ideologico': self._dens(ideologicos, total_palabras),
            
            # Autopercepción Cognitiva
            'reflexividad': self._dens(reflexivos, total_palabras),
            'autoafirmacion': self._dens(personales, total_palabras),
            
            # Discernimiento Ético
            'juicio_valorativo': self._dens(valorativos, total_palabras),
        }
        
        # 📈 ÍNDICES DERIVADOS (usando pesos del perfil heurístico)
        p = self.perfil
        
        # Dogmatismo general (coherencia + resolutividad - tensión dialéctica)
        metricas['dogmatismo_general'] = (
            metricas['coherencia_interna'] * p.w_coherencia +
            metricas['resolutividad'] * p.w_resolutividad -
            metricas['tension_dialectica'] * p.w_tension
        )
        
        # Discernimiento prudencial (tensión + reflexividad + principios)
        metricas['discernimiento_prudencial'] = (
            metricas['tension_dialectica'] * p.w_tension_pru +
            metricas['reflexividad'] * p.w_reflexividad_pru +
            metricas['principialismo'] * p.w_principialismo_pru
        )
        
        # Equilibrio retórico (relación entre crítica y afirmación)
        # Alto concesivo + bajo ideológico = equilibrado
        metricas['equilibrio_retorico'] = (
            metricas['tension_dialectica'] - 
            metricas['dogmatismo_ideologico']
        )
        
        # Clasificar perfil general
        metricas['perfil_general'] = self._clasificar_perfil(metricas)
        
        return metricas
    
    def _clasificar_perfil(self, m: Dict[str, float]) -> str:
        """
        Clasifica el perfil intelectual general basándose en las métricas
        
        Perfiles posibles:
        - Dogmático-normativo: Alta coherencia, baja tensión
        - Reflexivo-principialista: Alta reflexividad y principialismo
        - Pragmático-ejecutivo: Alto pragmatismo y resolutividad
        - Crítico-analítico: Alta tensión dialéctica
        - Balanceado: Sin predominancia clara
        """
        
        # Reglas de clasificación (ajustables)
        if m['dogmatismo_general'] > 2.0 and m['tension_dialectica'] < 1.0:
            return "Dogmático-normativo"
        
        if m['reflexividad'] > 2.0 and m['principialismo'] > 1.5:
            return "Reflexivo-principialista"
        
        if m['pragmatismo'] > 2.0 and m['resolutividad'] > 2.0:
            return "Pragmático-ejecutivo"
        
        if m['tension_dialectica'] > 2.5:
            return "Crítico-analítico"
        
        if m['ratio_decidendi'] > 2.5 and m['coherencia_interna'] > 2.0:
            return "Técnico-jurídico"
        
        if m['juicio_valorativo'] > 2.0 and m['principialismo'] > 2.0:
            return "Axiológico-valorativo"
        
        return "Balanceado"


# ══════════════════════════════════════════════════════════════════════════
# 🧠 MÓDULO DE PSICOLOGÍA JUDICIAL APLICADA
# ══════════════════════════════════════════════════════════════════════════

class AnalizadorConductaJudicialRAG:
    """
    🎯 ANALIZADOR DE CONDUCTA Y DECISIÓN JUDICIAL
    
    Analiza el comportamiento intelectual, emocional y decisional del juez 
    o autor jurídico a partir de patrones lingüísticos, estructuras lógicas 
    y elecciones de vocabulario.
    
    📊 DIMENSIONES ANALIZADAS:
    1. Cognitiva: Racionalidad jurídica y estructura mental
    2. Emocional: Tono, empatía, irritación, prudencia
    3. Decisional: Estilo resolutivo, consistencia, proporcionalidad
    4. Valorativa: Justicia, ética, derechos humanos, poder
    
    Permite detectar CÓMO DECIDE, CÓMO RAZONA y CÓMO SE EXPRESA un juez
    con precisión analítica y trazabilidad cuantitativa.
    """
    
    def __init__(self):
        # 🔍 PATRONES LINGÜÍSTICOS CLAVE PARA CONDUCTA JUDICIAL
        
        # Autoridad institucional (invocación al poder judicial)
        self.patron_autoridad = re.compile(
            r'\b(el\s+tribunal|esta\s+sala|este\s+juzgado|se\s+resuelve|'
            r'se\s+dispone|se\s+declara|esta\s+magistratura|este\s+órgano)\b',
            re.IGNORECASE
        )
        
        # Empatía humanista (sensibilidad hacia personas)
        self.patron_empatia = re.compile(
            r'\b(vulnerable|dignidad|humanidad|sufrimiento|equidad|'
            r'empat[ií]a|atento\s+a|comprensi[oó]n|situaci[oó]n\s+personal|'
            r'contexto\s+vital|realidad\s+de)\b',
            re.IGNORECASE
        )
        
        # Irritación/tono negativo (emotividad reactiva)
        self.patron_irritacion = re.compile(
            r'\b(inaceptable|inadmisible|repudia|grave|escandaloso|'
            r'irregular|falta\s+de\s+respeto|abuso|negligente|'
            r'intolerable|censurable|reprochable)\b',
            re.IGNORECASE
        )
        
        # Proporcionalidad (equilibrio y ponderación)
        self.patron_proporcionalidad = re.compile(
            r'\b(proporcional|razonable|equilibrado|ponderado|moderado|'
            r'en\s+justa\s+medida|adecuado|balance|sopesar|ponderar)\b',
            re.IGNORECASE
        )
        
        # Referencia a derechos (orientación ética-garantista)
        self.patron_derechos = re.compile(
            r'\b(derechos\s+humanos|garant[ií]as|igualdad|'
            r'no\s+discriminaci[oó]n|debido\s+proceso|justicia|'
            r'derechos\s+fundamentales|convencionalidad|tutela\s+efectiva)\b',
            re.IGNORECASE
        )
        
        # Formalismo jurídico (apego a la norma textual)
        self.patron_formalismo = re.compile(
            r'\b(conforme\s+a|seg[uú]n\s+lo\s+previsto|art[ií]culo|'
            r'ley\s+n[úu]m|disposici[oó]n|norma|c[oó]digo|literal|'
            r'textualmente|expresamente)\b',
            re.IGNORECASE
        )
        
        # Mitigación retórica (concesiones, matices)
        self.patron_mitigacion = re.compile(
            r'\b(sin\s+perjuicio\s+de|sin\s+embargo|a\s+pesar\s+de|'
            r'no\s+obstante|si\s+bien|aun\s+cuando|aunque)\b',
            re.IGNORECASE
        )
        
        # Autocontrol discursivo (prudencia, mesura)
        self.patron_autocontrol = re.compile(
            r'\b(cautela|prudencia|mesura|considera|pondera|'
            r'eval[uú]a|examina|analiza|reflexiona|medita)\b',
            re.IGNORECASE
        )
    
    def analizar_conducta(self, texto: str) -> Dict[str, float]:
        """
        Análisis completo de conducta judicial.
        Retorna métricas normalizadas por 1000 palabras + perfil decisional.
        """
        if not texto or len(texto) < 100:
            return {
                "error": "Texto insuficiente para análisis de conducta",
                "perfil_decisional": "No determinado"
            }
        
        total_palabras = len(texto.split())
        factor = 1000.0 / max(total_palabras, 1)
        
        # 📊 CONTEO DE PATRONES
        c_autoridad = len(self.patron_autoridad.findall(texto))
        c_empatia = len(self.patron_empatia.findall(texto))
        c_irritacion = len(self.patron_irritacion.findall(texto))
        c_proporcionalidad = len(self.patron_proporcionalidad.findall(texto))
        c_derechos = len(self.patron_derechos.findall(texto))
        c_formalismo = len(self.patron_formalismo.findall(texto))
        c_mitigacion = len(self.patron_mitigacion.findall(texto))
        c_autocontrol = len(self.patron_autocontrol.findall(texto))
        
        # 📈 MÉTRICAS BASE (normalizadas por 1000 palabras)
        resultados = {
            # Dimensión institucional
            "autoridad_institucional": c_autoridad * factor,
            
            # Dimensión emocional
            "empatia_humanista": c_empatia * factor,
            "tono_irritativo": c_irritacion * factor,
            "autocontrol_discursivo": c_autocontrol * factor,
            
            # Dimensión argumentativa
            "proporcionalidad_argumental": c_proporcionalidad * factor,
            "mitigacion_retorica": c_mitigacion * factor,
            
            # Dimensión valorativa
            "referencia_derechos": c_derechos * factor,
            "formalismo_juridico": c_formalismo * factor,
        }
        
        # 🧮 ÍNDICES DERIVADOS COMPLEJOS
        
        # Equilibrio emocional (autocontrol + ponderación - irritación)
        resultados["equilibrio_emocional"] = (
            (resultados["autocontrol_discursivo"] + 
             resultados["proporcionalidad_argumental"]) -
            resultados["tono_irritativo"]
        )
        
        # Predisposición humanista (empatía + derechos humanos)
        resultados["predisposicion_humanista"] = (
            resultados["empatia_humanista"] + 
            resultados["referencia_derechos"]
        ) / 2.0
        
        # Orientación normativa vs eticidad
        # Positivo = más formalista, Negativo = más axiológico
        resultados["orientacion_normativa_vs_eticidad"] = (
            resultados["formalismo_juridico"] - 
            resultados["referencia_derechos"]
        )
        
        # Índice de templanza judicial (mitigación + autocontrol - irritación)
        resultados["templanza_judicial"] = (
            resultados["mitigacion_retorica"] + 
            resultados["autocontrol_discursivo"] -
            resultados["tono_irritativo"]
        )
        
        # 🏆 CLASIFICACIÓN DE PERFIL DECISIONAL
        resultados["perfil_decisional"] = self._clasificar_decision(resultados)
        
        return resultados
    
    def _clasificar_decision(self, r: Dict[str, float]) -> str:
        """
        Clasifica el tipo de pensamiento decisional del juez/autor:
        
        - Técnico-formalista: Apegado a la ley, riguroso, textualista
        - Ético-garantista: Orientado a derechos, protección de garantías
        - Autoritario-reactivo: Tono fuerte, irritable, impositivo
        - Prudente-equilibrado: Ponderado, mesurado, balanceado
        - Emotivo-humanista: Empático, sensible, contextualizado
        - Mixto o indefinido: Sin predominancia clara
        """
        
        # Reglas de clasificación basadas en umbrales empíricos
        
        # Técnico-formalista: Alto formalismo + Baja referencia a derechos
        if r["formalismo_juridico"] > 4.0 and r["referencia_derechos"] < 1.0:
            return "Técnico-formalista"
        
        # Emotivo-humanista: Alta empatía + Bajo formalismo
        if r["predisposicion_humanista"] > 3.0 and r["formalismo_juridico"] < 2.0:
            return "Emotivo-humanista"
        
        # Autoritario-reactivo: Alto tono irritativo + Bajo autocontrol
        if r["tono_irritativo"] > 3.0 and r["autocontrol_discursivo"] < 1.0:
            return "Autoritario-reactivo"
        
        # Prudente-equilibrado: Alto equilibrio emocional + Alta proporcionalidad
        if r["equilibrio_emocional"] > 3.0 and r["proporcionalidad_argumental"] > 2.0:
            return "Prudente-equilibrado"
        
        # Ético-garantista: Alta referencia a derechos + Alto formalismo
        # (combina normatividad con valores)
        if r["referencia_derechos"] > 3.0 and r["formalismo_juridico"] > 2.0:
            return "Ético-garantista"
        
        # Normativo-moderado: Formalismo moderado sin extremos
        if 2.0 < r["formalismo_juridico"] < 4.0 and r["tono_irritativo"] < 1.5:
            return "Normativo-moderado"
        
        return "Mixto o indefinido"


def probar_analizador():
    """Función de prueba"""
    analizador = AnalizadorEnriquecidoRAG()
    
    # Buscar PDF de ejemplo
    conn = sqlite3.connect('colaborative/bases_rag/cognitiva/metadatos.db')
    c = conn.cursor()
    c.execute('SELECT archivo FROM perfiles_cognitivos WHERE autor LIKE ? LIMIT 1', ('%CARLOS%',))
    result = c.fetchone()
    conn.close()
    
    if result and result[0]:
        print(f"\n📄 Probando con: {result[0]}\n")
        analisis = analizador.analizar_documento_completo(result[0])
        
        print("\n" + "="*70)
        print("📊 RESULTADOS DEL ANÁLISIS ENRIQUECIDO")
        print("="*70)
        
        if analisis.get('autores_citados'):
            print("\n👥 AUTORES CITADOS (Top 10):")
            for autor, freq in list(analisis['autores_citados'].items())[:10]:
                print(f"   • {autor}: {freq} menciones")
        
        if analisis.get('palabras_clave'):
            print("\n🔑 PALABRAS CLAVE JURÍDICAS (Top 15):")
            for palabra, freq in list(analisis['palabras_clave'].items())[:15]:
                print(f"   • {palabra}: {freq} veces")
        
        if analisis.get('autor_referencia_principal'):
            ref = analisis['autor_referencia_principal']
            print(f"\n⭐ AUTOR DE REFERENCIA PRINCIPAL:")
            print(f"   {ref['nombre']} ({ref['menciones']} menciones)")
        
        if analisis.get('estadisticas'):
            stats = analisis['estadisticas']
            print(f"\n📈 ESTADÍSTICAS:")
            print(f"   • Total palabras: {stats['total_palabras']:,}")
            print(f"   • Total oraciones: {stats['total_oraciones']}")
            print(f"   • Palabras/oración: {stats['promedio_palabras_oracion']:.1f}")
            print(f"   • Vocabulario único: {stats['vocabulario_unico']:,}")
            print(f"   • Riqueza léxica: {stats['riqueza_lexica']:.3f}")
        
        if analisis.get('posiciones_doctrinales'):
            print(f"\n📍 POSICIONES DOCTRINALES:")
            for tipo, fragmentos in analisis['posiciones_doctrinales'].items():
                print(f"   • {tipo.upper()}: {len(fragmentos)} instancias")
                if fragmentos:
                    print(f"     Ejemplo: '{fragmentos[0][:100]}...'")
        
        # NUEVOS ANÁLISIS
        if analisis.get('marcadores_autoridad'):
            autoridad = analisis['marcadores_autoridad']
            print(f"\n🎯 MARCADORES DE AUTORIDAD:")
            print(f"   • Total marcadores: {autoridad.get('total_marcadores', 0)}")
            
            if autoridad.get('citas_libros'):
                print(f"\n   📚 Citas de libros/artículos: {len(autoridad['citas_libros'])}")
                for cita in autoridad['citas_libros'][:3]:
                    print(f"      - {cita['autor']} ({cita['año']}): \"{cita['texto']}...\"")
            
            if autoridad.get('citas_normas'):
                print(f"\n   ⚖️ Citas normativas: {len(autoridad['citas_normas'])}")
                normas_contador = Counter([f"{c['tipo']} {c['numero']}" for c in autoridad['citas_normas']])
                for norma, freq in normas_contador.most_common(5):
                    print(f"      - {norma}: {freq} veces")
            
            if autoridad.get('doctrina_establecida'):
                print(f"\n   📖 Referencias a doctrina establecida: {len(autoridad['doctrina_establecida'])}")
                for ref in autoridad['doctrina_establecida'][:3]:
                    print(f"      - \"{ref}\"")
            
            if autoridad.get('autoridad_reconocida'):
                print(f"\n   ⭐ Autoridades reconocidas: {len(set(autoridad['autoridad_reconocida']))}")
                for aut in list(set(autoridad['autoridad_reconocida']))[:5]:
                    print(f"      - {aut}")
        
        if analisis.get('estilo_discursivo'):
            estilo = analisis['estilo_discursivo']
            print(f"\n💬 ESTILO DISCURSIVO:")
            
            print(f"\n   🔹 Verbos Imperativos:")
            print(f"      Total: {estilo['verbos_imperativos']['total']}")
            print(f"      Densidad: {estilo['verbos_imperativos']['densidad']:.2f} por 100 palabras")
            if estilo['verbos_imperativos']['mas_frecuentes']:
                print(f"      Más usados: {', '.join([f'{v} ({c})' for v, c in estilo['verbos_imperativos']['mas_frecuentes'][:3]])}")
            
            print(f"\n   🔹 Afirmaciones Universales:")
            print(f"      Total: {estilo['afirmaciones_universales']['total']}")
            print(f"      Densidad: {estilo['afirmaciones_universales']['densidad']:.2f} por 100 palabras")
            if estilo['afirmaciones_universales']['mas_frecuentes']:
                print(f"      Más usados: {', '.join([f'{v} ({c})' for v, c in estilo['afirmaciones_universales']['mas_frecuentes'][:3]])}")
            
            print(f"\n   🔹 Adjetivos Valorativos:")
            print(f"      Total: {estilo['adjetivos_valorativos']['total']}")
            print(f"      Densidad: {estilo['adjetivos_valorativos']['densidad']:.2f} por 100 palabras")
            if estilo['adjetivos_valorativos']['mas_frecuentes']:
                print(f"      Más usados: {', '.join([f'{v} ({c})' for v, c in estilo['adjetivos_valorativos']['mas_frecuentes'][:5]])}")
            
            print(f"\n   🔹 Marcadores de Énfasis:")
            print(f"      Total: {estilo['marcadores_enfasis']['total']}")
            print(f"      Densidad: {estilo['marcadores_enfasis']['densidad']:.2f} por 100 palabras")
            
            print(f"\n   🔹 Uso de Ejemplos:")
            print(f"      Total: {estilo['uso_ejemplos']['total']}")
            print(f"      Densidad: {estilo['uso_ejemplos']['densidad']:.2f} por 100 palabras")
            if estilo['uso_ejemplos']['patrones']:
                print(f"      Patrones: {', '.join([f'{v} ({c})' for v, c in estilo['uso_ejemplos']['patrones'][:3]])}")
            
            print(f"\n   📊 ÍNDICES CALCULADOS:")
            print(f"      • Índice de Asertividad: {estilo['indice_asertividad']:.2f}")
            print(f"      • Índice de Subjetividad: {estilo['indice_subjetividad']:.2f}")
        
        if analisis.get('discernimiento'):
            d = analisis['discernimiento']
            print(f"\n🧠 ANÁLISIS DE DISCERNIMIENTO COGNITIVO/RETÓRICO:")
            print(f"   (Métricas por 1000 palabras)")
            
            print(f"\n   🔍 Lógica Argumentativa:")
            print(f"      • Coherencia interna: {d.get('coherencia_interna', 0):.2f}")
            print(f"      • Tensión dialéctica: {d.get('tension_dialectica', 0):.2f}")
            print(f"      • Resolutividad: {d.get('resolutividad', 0):.2f}")
            
            print(f"\n   🎯 Discernimiento Jurídico:")
            print(f"      • Ratio decidendi: {d.get('ratio_decidendi', 0):.2f}")
            print(f"      • Principialismo: {d.get('principialismo', 0):.2f}")
            
            print(f"\n   💼 Discernimiento Político/Estratégico:")
            print(f"      • Pragmatismo: {d.get('pragmatismo', 0):.2f}")
            print(f"      • Dogmatismo ideológico: {d.get('dogmatismo_ideologico', 0):.2f}")
            
            print(f"\n   🤔 Autopercepción Cognitiva:")
            print(f"      • Reflexividad: {d.get('reflexividad', 0):.2f}")
            print(f"      • Autoafirmación: {d.get('autoafirmacion', 0):.2f}")
            
            print(f"\n   📊 Discernimiento Ético:")
            print(f"      • Juicio valorativo: {d.get('juicio_valorativo', 0):.2f}")
            
            print(f"\n   🎭 ÍNDICES DERIVADOS:")
            print(f"      • Dogmatismo general: {d.get('dogmatismo_general', 0):.2f}")
            print(f"      • Discernimiento prudencial: {d.get('discernimiento_prudencial', 0):.2f}")
            print(f"      • Equilibrio retórico: {d.get('equilibrio_retorico', 0):.2f}")
            
            perfil = d.get('perfil_general', 'No determinado')
            print(f"\n   🏆 PERFIL INTELECTUAL GENERAL: {perfil}")
        
        # 🆕 MÓDULO DE PSICOLOGÍA JUDICIAL APLICADA
        if analisis.get('conducta_judicial'):
            cj = analisis['conducta_judicial']
            print(f"\n{'='*70}")
            print(f"⚖️ PSICOLOGÍA JUDICIAL APLICADA - CONDUCTA Y DECISIÓN")
            print(f"{'='*70}")
            print(f"   (Métricas normalizadas por 1000 palabras)\n")
            
            print(f"   🏛️ DIMENSIÓN INSTITUCIONAL:")
            print(f"      • Autoridad institucional: {cj.get('autoridad_institucional', 0):.2f}")
            print(f"        ↳ Invocación al poder judicial y función institucional")
            
            print(f"\n   💚 DIMENSIÓN EMOCIONAL:")
            print(f"      • Empatía humanista: {cj.get('empatia_humanista', 0):.2f}")
            print(f"        ↳ Sensibilidad hacia personas y situaciones vitales")
            print(f"      • Tono irritativo: {cj.get('tono_irritativo', 0):.2f}")
            print(f"        ↳ Lenguaje reactivo, condenatorio o autoritario")
            print(f"      • Autocontrol discursivo: {cj.get('autocontrol_discursivo', 0):.2f}")
            print(f"        ↳ Control emocional y racionalidad en la expresión")
            
            print(f"\n   ⚖️ DIMENSIÓN ARGUMENTATIVA:")
            print(f"      • Proporcionalidad argumental: {cj.get('proporcionalidad_argumental', 0):.2f}")
            print(f"        ↳ Equilibrio y ponderación en razonamientos")
            print(f"      • Mitigación retórica: {cj.get('mitigacion_retorica', 0):.2f}")
            print(f"        ↳ Uso de concesiones y matices ('sin embargo', 'no obstante')")
            
            print(f"\n   📜 DIMENSIÓN VALORATIVA:")
            print(f"      • Referencia a derechos: {cj.get('referencia_derechos', 0):.2f}")
            print(f"        ↳ Inclusión de derechos humanos y garantías")
            print(f"      • Formalismo jurídico: {cj.get('formalismo_juridico', 0):.2f}")
            print(f"        ↳ Apego a la norma textual y legalismo")
            
            print(f"\n   📊 ÍNDICES DERIVADOS:")
            eq_em = cj.get('equilibrio_emocional', 0)
            print(f"      • Equilibrio emocional: {eq_em:.2f}")
            interp_eq = "🟢 Alto" if eq_em > 3 else "🟡 Moderado" if eq_em > 1 else "🔴 Bajo"
            print(f"        ↳ (Autocontrol + Ponderación − Irritación) = {interp_eq}")
            
            pred_h = cj.get('predisposicion_humanista', 0)
            print(f"      • Predisposición humanista: {pred_h:.2f}")
            interp_ph = "🟢 Alta" if pred_h > 3 else "🟡 Moderada" if pred_h > 1 else "🔴 Baja"
            print(f"        ↳ (Empatía + Derechos humanos) / 2 = {interp_ph}")
            
            orient = cj.get('orientacion_normativa_vs_eticidad', 0)
            print(f"      • Orientación normativa vs eticidad: {orient:.2f}")
            interp_or = "⚖️ Legalista" if orient > 2 else "⚖️ Axiológico" if orient < -2 else "⚖️ Balanceado"
            print(f"        ↳ (Formalismo − Derechos) = {interp_or}")
            
            temp = cj.get('templanza_judicial', 0)
            print(f"      • Templanza judicial: {temp:.2f}")
            interp_te = "🟢 Alta" if temp > 3 else "🟡 Moderada" if temp > 1 else "🔴 Baja"
            print(f"        ↳ (Mitigación + Autocontrol − Irritación) = {interp_te}")
            
            perfil_dec = cj.get('perfil_decisional', 'No determinado')
            print(f"\n   🏆 PERFIL DECISIONAL: {perfil_dec}")
            print(f"      ↳ Tipo de razonamiento y conducta judicial predominante\n")
    else:
        print("❌ No se encontró PDF para analizar")


# ══════════════════════════════════════════════════════════════════════════
# ⚖️ SISTEMA COGNITIVO JURÍDICO – PARCHE INTEGRAL
# Autor: Dr. Pablo N. Farías
# Fecha: 2025-11-11
# Módulo: analizador_enriquecido_rag.py
# Funciones:
#   • Análisis argumentativo (razonamiento, falacias, fuerza argumental)
#   • Integración con estructura judicial (VISTO, CONSIDERANDO, RESUELVO)
#   • Conexión con metadatos de doctrina y sentencias (JSON unificado)
#   • Lectura directa desde PDF/TXT o bases RAG
# ══════════════════════════════════════════════════════════════════════════

import os

# ──────────────────────────────────────────────────────────────────────────
# UTILIDADES DE ENTRADA
# ──────────────────────────────────────────────────────────────────────────
def _leer_texto_desde_pdf(ruta_pdf: str) -> str:
    """Extrae texto de PDF usando PyMuPDF (fitz)."""
    try:
        import fitz
    except Exception:
        return ""
    try:
        doc = fitz.open(ruta_pdf)
        texto = "\n".join(page.get_text() for page in doc)
        doc.close()
        return texto
    except Exception:
        return ""


def _leer_texto_fallback(ruta: str) -> str:
    """Lee texto plano o PDF; retorna vacío si falla."""
    if not os.path.exists(ruta):
        return ""
    ext = os.path.splitext(ruta)[1].lower()
    if ext == ".txt":
        try:
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return ""
    if ext == ".pdf":
        return _leer_texto_desde_pdf(ruta)
    return ""


def _recuperar_texto_desde_base_stub(ruta_pdf: str) -> str:
    """Stub para integración RAG; reemplazar con función real."""
    return ""


# ──────────────────────────────────────────────────────────────────────────
# ANALIZADOR ARGUMENTATIVO JURÍDICO
# ──────────────────────────────────────────────────────────────────────────
class AnalizadorArgumentativoJuridico:
    """Detecta falacias, tipo de razonamiento y fuerza argumental."""

    def __init__(self):
        self.patrones_falacias = {
            "ad_hominem": r"(no\s+es\s+creíble\s+porque|su\s+conducta|carece\s+de\s+autoridad)",
            "ad_populum": r"(todo\s+el\s+mundo\s+sabe|es\s+evidente\s+para\s+todos)",
            "petitio_principii": r"(porque\s+es\s+así|ya\s+que\s+es\s+cierto\s+que)",
            "ad_authoritatem": r"(según\s+(la\s+CSJN|la\s+Corte|el\s+autor)|como\s+dijo)",
            "falsa_causa": r"(después\s+de\s+que\s+ocurrió|por\s+haber\s+ocurrido)",
            "falsa_dicotomia": r"(no\s+hay\s+otra\s+opción|solo\s+existen\s+dos\s+posibilidades)",
            "apelacion_a_la_emocion": r"(injusto\s+para\s+las\s+víctimas|cruel|indignante)",
            "non_sequitur": r"(no\s+se\s+sigue\s+lógicamente|sin\s+fundamento\s+lógico)"
        }
        self.patrones_razonamiento = {
            "deductivo": r"(por\s+tanto|en\s+consecuencia|se\s+sigue\s+que)",
            "inductivo": r"(en\s+muchos\s+casos|se\s+observa\s+que)",
            "analógico": r"(así\s+como|del\s+mismo\s+modo|análogamente)",
            "axiológico": r"(justicia|equidad|razonabilidad|valor)",
            "pragmático": r"(en\s+la\s+práctica|eficacia|conveniencia)"
        }
        self.tipo_argumento_juridico = {
            "normativo": r"(art\.|artículo|ley\s+\d+|c[oó]digo|constitución)",
            "axiológico": r"(principio|valor|razonabilidad|teleología)",
            "fáctico": r"(hecho|prueba|evidencia|testimonio|pericia)",
            "comparativo": r"(así\s+como|de\s+modo\s+semejante)"
        }

    def detectar_falacias(self, texto: str):
        hallazgos = []
        for tipo, patron in self.patrones_falacias.items():
            for m in re.finditer(patron, texto, re.IGNORECASE):
                contexto = texto[max(0, m.start() - 60):m.end() + 60]
                hallazgos.append({"tipo": tipo, "fragmento": contexto.strip()})
        return hallazgos

    def clasificar_razonamiento(self, texto: str) -> str:
        conteos = {k: len(re.findall(v, texto, re.IGNORECASE))
                   for k, v in self.patrones_razonamiento.items()}
        return max(conteos, key=conteos.get) if any(conteos.values()) else "indeterminado"

    def clasificar_tipo_argumento(self, texto: str) -> str:
        conteos = {k: len(re.findall(v, texto, re.IGNORECASE))
                   for k, v in self.tipo_argumento_juridico.items()}
        return max(conteos, key=conteos.get) if any(conteos.values()) else "indeterminado"

    def analizar_documento_completo(self, texto: str) -> Dict:
        """Método auxiliar para compatibilidad con clase base."""
        palabras = len(texto.split())
        oraciones = len(re.split(r'[.!?]+', texto))
        promedio = palabras / max(1, oraciones)
        
        return {
            "nivel_dialectico": min(1.0, promedio / 25.0),
            "palabras": palabras,
            "oraciones": oraciones
        }

    def evaluar_argumentacion_juridica(self, texto: str) -> Dict:
        base = self.analizar_documento_completo(texto)
        falacias = self.detectar_falacias(texto)
        tipo_r = self.clasificar_razonamiento(texto)
        tipo_a = self.clasificar_tipo_argumento(texto)
        penal = min(0.35, len(falacias) * 0.04)
        irj = max(0.0, min(1.0, base.get("nivel_dialectico", 0.5) + 0.5 - penal))
        return {
            "tipo_razonamiento": tipo_r,
            "tipo_argumento": tipo_a,
            "falacias": falacias,
            "indice_razonamiento_juridico": round(irj, 3),
            "nivel_dialectico": base.get("nivel_dialectico", 0.5)
        }


# ──────────────────────────────────────────────────────────────────────────
# ANALIZADOR ESTRUCTURAL DE SENTENCIAS
# ──────────────────────────────────────────────────────────────────────────
class AnalizadorEstructuralSentencias:
    """Analiza estructura judicial: VISTO, CONSIDERANDO, RESUELVO."""
    
    def __init__(self):
        self.secciones = ["VISTO", "CONSIDERANDO", "RESUELVO"]
    
    def analizar_sentencia_completa(self, texto: str) -> Dict:
        """Detecta secciones estructurales de la sentencia."""
        resultado = {}
        for seccion in self.secciones:
            patron = rf'\b{seccion}\b'
            if re.search(patron, texto, re.IGNORECASE):
                resultado[seccion.lower()] = True
            else:
                resultado[seccion.lower()] = False
        
        resultado["estructura_completa"] = all(resultado.values())
        return resultado


# ──────────────────────────────────────────────────────────────────────────
# ANALIZADOR INTEGRAL RAG
# ──────────────────────────────────────────────────────────────────────────
class AnalizadorIntegralRAG(AnalizadorEnriquecidoRAG):
    """Integra análisis enriquecido, argumentativo y estructural."""

    def __init__(self, directorio_bases: Optional[str] = None):
        super().__init__()
        self.argumentativo = AnalizadorArgumentativoJuridico()
        self.estructural = AnalizadorEstructuralSentencias()
        self.directorio_bases = directorio_bases or "colaborative/vector_bases"

    def analizar_completo_texto(self, texto: str, tipo: str = "doctrina") -> Dict:
        if not texto or len(texto.strip()) < 30:
            return {"error": "Texto insuficiente", "tipo": tipo}

        enr = super().analizar_documento_completo(texto)
        arg = self.argumentativo.evaluar_argumentacion_juridica(texto)
        est = self.estructural.analizar_sentencia_completa(texto) if tipo == "sentencia" else {}
        irj, dial = arg.get("indice_razonamiento_juridico", 0), arg.get("nivel_dialectico", 0)
        return {
            "tipo": tipo,
            "analisis_enriquecido": enr,
            "analisis_argumentativo": arg,
            "analisis_estructural": est,
            "indice_integridad_argumental": round((irj + dial) / 2, 3),
            "numero_falacias": len(arg.get("falacias", []))
        }

    def analizar_documento_ruta(self, ruta_doc: str, tipo: str = "sentencia") -> Dict:
        texto = _recuperar_texto_desde_base_stub(ruta_doc) or _leer_texto_fallback(ruta_doc)
        if not texto:
            return {"error": f"No se pudo leer {ruta_doc}"}
        resultado = self.analizar_completo_texto(texto, tipo)
        resultado["archivo"] = os.path.basename(ruta_doc)
        return resultado


# ──────────────────────────────────────────────────────────────────────────
# GESTOR DE METADATOS
# ──────────────────────────────────────────────────────────────────────────
class GestorMetadatosSentencias:
    def __init__(self, ruta_json: str = "colaborative/data/pdfs/general/metadatos_sentencias.json"):
        self.ruta_json = ruta_json
        self.datos = {}
        if os.path.exists(ruta_json):
            with open(ruta_json, "r", encoding="utf-8") as f:
                self.datos = json.load(f)

    def obtener_para_archivo(self, nombre_archivo: str) -> dict:
        """Obtiene metadatos para un archivo específico."""
        base = os.path.basename(nombre_archivo)
        # Buscar directamente por nombre de archivo (estructura plana)
        if base in self.datos and not base.startswith('_'):
            return self.datos[base]
        return {}


class AnalizadorIntegralRAGConMetadatos(AnalizadorIntegralRAG):
    """Analizador integral con enriquecimiento por metadatos JSON."""

    def __init__(self, ruta_metadatos: str = "colaborative/data/pdfs/general/metadatos_sentencias.json"):
        super().__init__()
        self.metadatos = GestorMetadatosSentencias(ruta_metadatos)

    def analizar_documento_ruta(self, ruta_doc: str, tipo: str = "sentencia") -> dict:
        resultado = super().analizar_documento_ruta(ruta_doc, tipo)
        meta = self.metadatos.obtener_para_archivo(ruta_doc)
        if meta:
            resultado["metadatos"] = meta
            if "ponderacion_manual" in meta:
                resultado["ponderacion_manual"] = meta["ponderacion_manual"]
        return resultado


# ──────────────────────────────────────────────────────────────────────────
# TEST DE INTEGRACIÓN
# ──────────────────────────────────────────────────────────────────────────
def test_analizador_integral():
    """Test del analizador integral con metadatos."""
    print("\n" + "="*70)
    print("🧪 TEST ANALIZADOR INTEGRAL RAG CON METADATOS")
    print("="*70 + "\n")
    
    ruta_demo = "colaborative/data/pdfs/pdfs_civil_general/Banco_Provincia_c_Laborda_Walter_Gaston.pdf"
    
    if not os.path.exists(ruta_demo):
        print(f"⚠️ Archivo de prueba no encontrado: {ruta_demo}")
        print("📝 Para probar, coloca el PDF en la ruta indicada")
        return
    
    analizador = AnalizadorIntegralRAGConMetadatos()
    print(f"📄 Analizando: {os.path.basename(ruta_demo)}\n")
    
    res = analizador.analizar_documento_ruta(ruta_demo, tipo="sentencia")
    
    print("📊 RESULTADOS:")
    print(json.dumps(res, indent=2, ensure_ascii=False))
    
    if "metadatos" in res:
        print("\n✅ Metadatos cargados correctamente desde JSON")
    else:
        print("\n⚠️ No se encontraron metadatos para este archivo")


if __name__ == "__main__":
    # Ejecutar test original
    probar_analizador()
    
    # Ejecutar test de integración si se descomenta:
    # test_analizador_integral()
