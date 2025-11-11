#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 GENERADOR DE INFORMES AUTORALES CON GEMINI
=============================================

Sistema que toma:
- Datos cognitivos del autor (8 rasgos + aristotélico)
- Fragmentos textuales reales de sus documentos
- Metadatos de las bases RAG
- Comparaciones con otros autores

Y genera con Gemini:
- Informe fundamentado y bien estructurado
- Citas textuales directas del autor
- Justificación del análisis cognitivo
- Visualización explicativa

FECHA: 11 NOV 2025
"""

import os
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Importar analizador enriquecido y gestor unificado
import sys
sys.path.append(str(Path(__file__).parent))
from analizador_enriquecido_rag import AnalizadorEnriquecidoRAG
from gestor_unificado_autores import gestor_autores

# Cargar variables de entorno desde .env
load_dotenv(Path(__file__).parent.parent / '.env')

class GeneradorInformesGemini:
    """
    Genera informes autorales usando Gemini con datos reales
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.metadatos_db = self.base_path / "colaborative/bases_rag/cognitiva/metadatos.db"
        self.autor_centrico_db = self.base_path / "colaborative/bases_rag/cognitiva/autor_centrico.db"
        
        # Inicializar analizador enriquecido
        self.analizador_rag = AnalizadorEnriquecidoRAG()
        
        # Configurar Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
            print("⚠️ GEMINI_API_KEY no configurada")
    
    def obtener_datos_completos_autor(self, nombre_autor: str) -> Optional[Dict]:
        """Obtiene todos los datos disponibles del autor"""
        try:
            conn_meta = sqlite3.connect(self.metadatos_db)
            conn_autor = sqlite3.connect(self.autor_centrico_db)
            
            c_meta = conn_meta.cursor()
            c_autor = conn_autor.cursor()
            
            # 📊 EXTRAER TODAS LAS COLUMNAS DISPONIBLES (52 columnas)
            c_meta.execute("""
                SELECT * FROM perfiles_cognitivos
                WHERE autor = ?
                LIMIT 1
            """, (nombre_autor,))
            
            perfil_meta = c_meta.fetchone()
            
            # Obtener nombres de columnas
            c_meta.execute("PRAGMA table_info(perfiles_cognitivos)")
            columnas_meta = [col[1] for col in c_meta.fetchall()]
            
            # Si no está en metadatos.db, intentar solo con autor_centrico.db
            usar_solo_autor_centrico = False
            if not perfil_meta:
                print(f"⚠️ Autor no encontrado en metadatos.db, buscando en autor_centrico.db...")
                usar_solo_autor_centrico = True
            
            # Datos de autor_centrico.db
            c_autor.execute("""
                SELECT 
                    metodologia_principal,
                    patron_razonamiento_dominante,
                    estilo_argumentativo,
                    estructura_discursiva,
                    densidad_conceptual,
                    originalidad_score,
                    coherencia_interna
                FROM perfiles_autorales_expandidos
                WHERE autor = ?
                LIMIT 1
            """, (nombre_autor,))
            
            perfil_autor = c_autor.fetchone()
            
            # Verificar que al menos uno de los dos perfiles exista
            if not perfil_meta and not perfil_autor:
                print(f"❌ Autor '{nombre_autor}' no encontrado en ninguna base de datos")
                conn_meta.close()
                conn_autor.close()
                return None
            
            # 📄 OBTENER INFORMACIÓN COMPLETA DEL DOCUMENTO
            # Si no hay perfil_meta, buscar ruta desde perfil_autor
            if perfil_meta:
                ruta_pdf = perfil_meta[2]  # fuente (PDF)
            else:
                # Intentar obtener ruta del documento desde autor_centrico.db
                c_autor.execute("""
                    SELECT archivo_origen 
                    FROM perfiles_autorales_expandidos 
                    WHERE autor = ?
                """, (nombre_autor,))
                ruta_result = c_autor.fetchone()
                ruta_pdf = ruta_result[0] if ruta_result else None
            
            if not ruta_pdf:
                print(f"⚠️ No se encontró ruta del PDF para {nombre_autor}")
                info_documento = {}
                fragmentos = []
                introduccion = ""
                conclusiones = ""
                analisis_enriquecido = {}
            else:
                print(f"📄 Documento ubicado en: {ruta_pdf}")
                info_documento = self._obtener_info_documento(ruta_pdf)
                
                # 📖 EXTRAER FRAGMENTOS TEXTUALES AMPLIADOS (10 en lugar de 5)
                print(f"📖 Extrayendo fragmentos textuales del PDF...")
                fragmentos = self._extraer_fragmentos_textuales(ruta_pdf, max_fragmentos=10)
                
                # 🔍 EXTRAER SECCIONES ESPECÍFICAS
                print(f"🔍 Buscando introducción y conclusiones...")
                introduccion = self._extraer_seccion_especifica(
                    ruta_pdf, 
                    ["introducción", "introduction", "presentación", "objeto", "planteamiento"],
                    max_chars=1500
                )
                
                conclusiones = self._extraer_seccion_especifica(
                    ruta_pdf,
                    ["conclusión", "conclusiones", "conclusion", "reflexiones finales", "consideraciones finales"],
                    max_chars=1500
                )
                
                # 🔍 ANÁLISIS ENRIQUECIDO RAG
                print(f"🔍 Analizando documento completo con RAG enriquecido...")
                if perfil_meta and len(perfil_meta) > 1:
                    analisis_enriquecido = self.analizador_rag.analizar_documento_completo(perfil_meta[1])
                else:
                    analisis_enriquecido = {}
            
            # Obtener comparativas con otros autores  
            try:
                c_autor.execute("""
                    SELECT autor_b, tipo_analisis, resultado_json
                    FROM comparativas_autorales
                    WHERE autor_a = ?
                    LIMIT 5
                """, (nombre_autor,))
                comparativas = c_autor.fetchall()
            except:
                comparativas = []
            
            
            conn_meta.close()
            conn_autor.close()
            
            # 📊 CONSTRUIR DICCIONARIO COMPLETO CON TODAS LAS COLUMNAS RAG
            # Crear diccionario dinámico con todas las 52 columnas
            datos = {}
            
            # Agregar TODAS las columnas de metadatos.db (si existen)
            if perfil_meta:
                for i, columna in enumerate(columnas_meta):
                    valor = perfil_meta[i] if i < len(perfil_meta) else None
                    # Convertir valores para evitar errores de serialización
                    if isinstance(valor, bytes):
                        valor = valor.decode('utf-8', errors='ignore')
                    datos[f"rag_{columna}"] = valor
            else:
                # Si no hay perfil_meta, inicializar con valores por defecto
                datos["rag_autor"] = nombre_autor
                datos["rag_archivo"] = "N/A"
            
            # Agregar datos procesados adicionales
            datos["fragmentos_textuales"] = fragmentos
            datos["info_documento"] = info_documento
            datos["seccion_introduccion"] = introduccion
            datos["seccion_conclusiones"] = conclusiones
            
            # Datos de autor_centrico.db
            datos.update({
                "metodologia": perfil_autor[0] if perfil_autor else "N/A",
                "patron_razonamiento": perfil_autor[1] if perfil_autor else "N/A",
                "estilo_argumentativo": perfil_autor[2] if perfil_autor else "N/A",
                "estructura_discursiva": perfil_autor[3] if perfil_autor else "N/A",
                "densidad_conceptual": perfil_autor[4] if perfil_autor else 0,
                "originalidad": perfil_autor[5] if perfil_autor else 0,
                "coherencia": perfil_autor[6] if perfil_autor else 0,
            })
            
            # Comparativas
            datos["comparativas"] = [
                {"autor_b": c[0], "tipo": c[1], "resultado": c[2]}
                for c in comparativas
            ]
            
            # 🔍 ANÁLISIS ENRIQUECIDO RAG
            datos["analisis_enriquecido"] = analisis_enriquecido
            
            return datos
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de {nombre_autor}: {e}")
            return None
    
    def _extraer_fragmentos_textuales(self, ruta_pdf: str, max_fragmentos: int = 10) -> List[str]:
        """
        Extrae fragmentos textuales representativos y diversos del PDF.
        AUMENTADO: Ahora extrae 10 fragmentos en lugar de 5 para mayor riqueza.
        """
        try:
            import fitz  # PyMuPDF
            
            if not os.path.exists(ruta_pdf):
                return []
            
            doc = fitz.open(ruta_pdf)
            fragmentos = []
            
            # 📊 ESTRATEGIA DE EXTRACCIÓN AMPLIADA
            total_paginas = len(doc)
            
            # 1. Páginas de muestreo distribuidas (más granular)
            if total_paginas >= 10:
                paginas_muestreo = [
                    0, 1,  # Inicio (posible introducción)
                    total_paginas // 5,
                    total_paginas // 3,
                    total_paginas // 2,  # Mitad
                    2 * total_paginas // 3,
                    4 * total_paginas // 5,
                    total_paginas - 2, total_paginas - 1  # Final (posibles conclusiones)
                ]
            else:
                paginas_muestreo = list(range(total_paginas))
            
            # 2. Extraer múltiples párrafos por página
            for num_pagina in paginas_muestreo[:max_fragmentos]:
                if num_pagina < total_paginas and len(fragmentos) < max_fragmentos:
                    page = doc[num_pagina]
                    texto = page.get_text()
                    
                    # Buscar párrafos de diferentes longitudes para diversidad
                    parrafos = texto.split('\n\n')
                    for parrafo in parrafos:
                        parrafo_limpio = parrafo.strip()
                        # Aceptar párrafos entre 200 y 1000 caracteres
                        if 200 <= len(parrafo_limpio) <= 1000 and not parrafo_limpio.isupper():
                            fragmentos.append(parrafo_limpio)
                            if len(fragmentos) >= max_fragmentos:
                                break
                    
                    if len(fragmentos) >= max_fragmentos:
                        break
            
            doc.close()
            return fragmentos[:max_fragmentos]
            
        except Exception as e:
            print(f"⚠️ Error extrayendo fragmentos: {e}")
            return []
    
    def _extraer_seccion_especifica(self, ruta_pdf: str, palabras_clave: List[str], max_chars: int = 2000) -> str:
        """
        Extrae sección específica del PDF buscando palabras clave.
        Útil para encontrar introducción, conclusiones, metodología, etc.
        """
        try:
            import fitz
            
            if not os.path.exists(ruta_pdf):
                return ""
            
            doc = fitz.open(ruta_pdf)
            texto_encontrado = ""
            
            for num_pagina in range(len(doc)):
                page = doc[num_pagina]
                texto_pagina = page.get_text()
                
                # Buscar si alguna palabra clave está en esta página
                texto_lower = texto_pagina.lower()
                for palabra in palabras_clave:
                    if palabra.lower() in texto_lower:
                        # Extraer contexto alrededor de la palabra clave
                        inicio = texto_pagina.lower().find(palabra.lower())
                        if inicio != -1:
                            # Tomar desde inicio de párrafo hasta max_chars
                            inicio_parrafo = texto_pagina.rfind('\n\n', 0, inicio)
                            if inicio_parrafo == -1:
                                inicio_parrafo = 0
                            
                            texto_encontrado = texto_pagina[inicio_parrafo:inicio_parrafo + max_chars].strip()
                            doc.close()
                            return texto_encontrado
            
            doc.close()
            return ""
            
        except Exception as e:
            print(f"⚠️ Error extrayendo sección: {e}")
            return ""
    
    def _obtener_info_documento(self, ruta_pdf: str) -> Dict:
        """
        Obtiene información completa del documento PDF.
        """
        try:
            import fitz
            
            if not os.path.exists(ruta_pdf):
                return {
                    "ubicacion": ruta_pdf,
                    "existe": False,
                    "error": "Archivo no encontrado"
                }
            
            doc = fitz.open(ruta_pdf)
            metadata = doc.metadata or {}
            
            info = {
                "ubicacion_completa": os.path.abspath(ruta_pdf),
                "nombre_archivo": os.path.basename(ruta_pdf),
                "existe": True,
                "paginas": len(doc),
                "titulo": metadata.get("title", "N/A"),
                "autor_metadata": metadata.get("author", "N/A"),
                "fecha_creacion": metadata.get("creationDate", "N/A"),
                "fecha_modificacion": metadata.get("modDate", "N/A"),
                "tamano_kb": os.path.getsize(ruta_pdf) // 1024
            }
            
            doc.close()
            return info
            
        except Exception as e:
            return {
                "ubicacion": ruta_pdf,
                "existe": False,
                "error": str(e)
            }
    
    def generar_informe_con_gemini(self, nombre_autor: str, forzar_regenerar: bool = False) -> Optional[Dict]:
        """Genera informe completo usando Gemini con sistema de caché"""
        
        print(f"\n[GEMINI] Generando informe para: {nombre_autor}")
        
        # 1. Verificar si existe en caché (a menos que se fuerce regeneración)
        if not forzar_regenerar:
            informe_cacheado = gestor_autores.obtener_informe_cacheado(nombre_autor)
            if informe_cacheado:
                print("✅ Informe recuperado desde caché")
                return informe_cacheado
        
        # 2. Buscar autor en todas las bases usando gestor unificado
        print("🔍 Buscando autor en todas las bases...")
        datos_unificados = gestor_autores.buscar_autor_todas_bases(nombre_autor)
        
        if not datos_unificados or len(datos_unificados['encontrado_en']) == 0:
            print(f"❌ Autor '{nombre_autor}' no encontrado en ninguna base")
            return {"error": f"No se encontraron datos para {nombre_autor}"}
        
        print(f"✅ Encontrado en {len(datos_unificados['encontrado_en'])} base(s)")
        
        # 3. Obtener todos los datos (método legacy para compatibilidad)
        datos = self.obtener_datos_completos_autor(nombre_autor)
        
        if not datos:
            return {"error": f"No se encontraron datos para {nombre_autor}"}
        
        if not self.model:
            return {"error": "Gemini no está configurado. Configure GEMINI_API_KEY"}
        
        # Construir prompt enriquecido
        prompt = self._construir_prompt_analisis(datos)
        
        # Reintentos con backoff exponencial para error 429
        max_intentos = 3
        tiempo_espera = 2  # segundos iniciales
        
        for intento in range(max_intentos):
            try:
                print(f"[GEMINI] Intento {intento + 1}/{max_intentos}...")
                
                # Generar con Gemini
                response = self.model.generate_content(prompt)
                informe_texto = response.text
                
                print(f"✅ Informe generado exitosamente")
                
                resultado = {
                    "autor": nombre_autor,
                    "informe_gemini": informe_texto,
                    "datos_originales": datos,
                    "fragmentos_citados": datos["fragmentos_textuales"],
                    "metricas_clave": self._extraer_metricas_clave(datos),
                    "bases_consultadas": datos_unificados['encontrado_en']
                }
                
                # 4. Guardar en caché para evitar regeneración
                gestor_autores.guardar_informe_cache(nombre_autor, resultado)
                
                return resultado
                
            except Exception as e:
                error_str = str(e)
                
                # Si es error 429 (quota exceeded) y no es el último intento, reintenta
                if "429" in error_str or "Resource exhausted" in error_str:
                    if intento < max_intentos - 1:
                        print(f"⚠️ Error 429 (cuota agotada). Esperando {tiempo_espera}s antes de reintentar...")
                        import time
                        time.sleep(tiempo_espera)
                        tiempo_espera *= 2  # Backoff exponencial
                        continue
                    else:
                        print(f"❌ Cuota de Gemini agotada después de {max_intentos} intentos")
                        return {
                            "error": "Cuota de Google Gemini agotada. Por favor, espera unos minutos e intenta nuevamente.",
                            "error_tipo": "429_quota_exceeded",
                            "sugerencia": "La API de Gemini tiene límites de uso. Espera 1-2 minutos y vuelve a intentar."
                        }
                else:
                    # Otro tipo de error
                    print(f"❌ Error generando con Gemini: {e}")
                    return {"error": str(e)}
        
        # Si llegamos aquí, fallaron todos los intentos
        return {
            "error": "No se pudo generar el informe después de varios intentos",
            "sugerencia": "Por favor, intenta nuevamente en unos minutos"
        }
    
    def _construir_prompt_analisis(self, datos: Dict) -> str:
        """Construye prompt detallado para Gemini"""
        
        # Extraer datos principales (con prefijo rag_)
        autor = datos.get('rag_autor', 'Desconocido')
        archivo = datos.get('rag_archivo', 'N/A')
        
        # Información del documento
        info_doc = datos.get('info_documento', {})
        
        prompt = f"""
Eres un experto en análisis cognitivo-metodológico de autores jurídicos. 

**AUTOR ANALIZADO:** {autor}

**DOCUMENTO ANALIZADO:** {archivo}

═══════════════════════════════════════════════════════════════════════
📄 INFORMACIÓN DEL DOCUMENTO FUENTE
═══════════════════════════════════════════════════════════════════════

**Ubicación del archivo:** {info_doc.get('ubicacion_completa', 'N/A')}
**Nombre del archivo:** {info_doc.get('nombre_archivo', 'N/A')}
**Páginas totales:** {info_doc.get('paginas', 'N/A')}
**Tamaño:** {info_doc.get('tamano_kb', 0)} KB
**Título (metadata PDF):** {info_doc.get('titulo', 'N/A')}
**Fecha creación:** {info_doc.get('fecha_creacion', 'N/A')}

⚠️ IMPORTANTE: Esta es la obra COMPLETA que debes analizar. Todos los fragmentos
textuales y citas que se proporcionan a continuación provienen de este documento.
Cada vez que cites algo, puedes referenciar que proviene de este archivo específico.

═══════════════════════════════════════════════════════════════════════
📊 BASE RAG COMPLETA - INFORMACIÓN DISPONIBLE (52 CAMPOS)
═══════════════════════════════════════════════════════════════════════

Tienes acceso a TODA la información de la base RAG del autor. Usa TODOS estos datos
para hacer un análisis completo y profundo. NO te limites solo a lo que aparece 
resumido abajo - explora y menciona cualquier dato relevante de estos campos:

"""
        
        # 🔍 AGREGAR TODOS LOS DATOS RAG DISPONIBLES
        prompt += "\n**DATOS COMPLETOS DE LA BASE RAG:**\n\n"
        
        for key, value in datos.items():
            if key.startswith('rag_') and value is not None:
                campo = key.replace('rag_', '')
                # Formatear valores según tipo
                if isinstance(value, float):
                    if 0 <= value <= 1:
                        prompt += f"   • {campo}: {value:.3f}\n"
                    else:
                        prompt += f"   • {campo}: {value:.2f}\n"
                elif isinstance(value, str) and len(value) > 200:
                    prompt += f"   • {campo}: {value[:200]}...\n"
                else:
                    prompt += f"   • {campo}: {value}\n"
        
        prompt += "\n\n**RESUMEN INTERPRETATIVO DE MÉTRICAS PRINCIPALES:**\n\n"
        
        # Extraer valores principales con manejo de errores
        def get_val(key, default=0):
            val = datos.get(f'rag_{key}', default)
            try:
                return float(val) if val is not None else default
            except:
                return default
        
        prompt += f"""
1. **Rasgos Cognitivos (escala 0-1):**
   - Formalismo jurídico: {get_val('formalismo'):.3f}
   - Creatividad conceptual: {get_val('creatividad'):.3f}
   - Dogmatismo: {get_val('dogmatismo'):.3f}
   - Empirismo evidencial: {get_val('empirismo'):.3f}
   - Interdisciplinariedad: {get_val('interdisciplinariedad'):.3f}
   - Nivel de abstracción: {get_val('nivel_abstraccion'):.3f}
   - Complejidad sintáctica: {get_val('complejidad_sintactica'):.3f}
   - Uso de jurisprudencia: {get_val('uso_jurisprudencia'):.3f}

2. **Análisis Aristotélico:**
   - Ethos (autoridad): {get_val('ethos'):.3f}
   - Pathos (emoción): {get_val('pathos'):.3f}
   - Logos (lógica): {get_val('logos'):.3f}

3. **Metodología:**
   - Tipo de pensamiento: {datos.get('rag_tipo_pensamiento', 'N/A')}
   - Razonamiento dominante: {datos.get('rag_razonamiento_dominante', 'N/A')}
   - Modalidad epistémica: {datos.get('rag_modalidad_epistemica', 'N/A')}
   - Densidad de citas: {get_val('densidad_citas'):.2f}%
   - Uso de ejemplos: {get_val('uso_ejemplos'):.2f}%

4. **Perfil Autor-Céntrico:**
   - Metodología principal: {datos.get('metodologia', 'N/A')}
   - Patrón de razonamiento: {datos.get('patron_razonamiento', 'N/A')}
   - Estilo argumentativo: {datos.get('estilo_argumentativo', 'N/A')}
   - Originalidad: {datos.get('originalidad', 0):.3f}
   - Coherencia interna: {datos.get('coherencia', 0):.3f}

═══════════════════════════════════════════════════════════════════════
📖 SECCIONES ESPECÍFICAS EXTRAÍDAS DEL DOCUMENTO
═══════════════════════════════════════════════════════════════════════

"""
        
        # Agregar introducción si está disponible
        introduccion = datos.get('seccion_introduccion', '')
        if introduccion and len(introduccion) > 100:
            prompt += f"""
**🎯 INTRODUCCIÓN DEL DOCUMENTO:**

"{introduccion}"

Esta sección establece el marco conceptual y objetivos del autor.
Úsala para identificar su tesis principal y planteamiento inicial.

"""
        
        # Agregar conclusiones si están disponibles
        conclusiones = datos.get('seccion_conclusiones', '')
        if conclusiones and len(conclusiones) > 100:
            prompt += f"""
**🎯 CONCLUSIONES DEL DOCUMENTO:**

"{conclusiones}"

Esta sección resume las reflexiones finales y posicionamiento del autor.
Úsala para identificar sus aportes principales y cierre argumentativo.

"""
        
        # ═════════════════ AGREGAR OBJETIVO Y TEMÁTICAS ═════════════════
        prompt += """

═══════════════════════════════════════════════════════════════════════
🎯 OBJETIVO Y TEMÁTICAS PRINCIPALES DE LA OBRA
═══════════════════════════════════════════════════════════════════════

"""
        
        # Agregar objetivo central y temáticas si están disponibles
        objetivo_central = datos.get('rag_objetivo_central')
        if objetivo_central and len(str(objetivo_central)) > 20:
            prompt += f"\n**Objetivo Central de la Obra:**\n{objetivo_central}\n"
        
        tematicas = datos.get('rag_tematicas_principales')
        if tematicas:
            try:
                import json
                temas_list = json.loads(tematicas) if isinstance(tematicas, str) else tematicas
                if temas_list and len(temas_list) > 0:
                    prompt += f"\n**Temáticas Principales Tratadas:**\n"
                    for i, tema in enumerate(temas_list[:5], 1):
                        prompt += f"   {i}. {tema}\n"
            except:
                pass
        
        resumen = datos.get('rag_resumen_ejecutivo')
        if resumen and len(str(resumen)) > 50:
            prompt += f"\n**Resumen Ejecutivo:**\n{resumen}\n"
        
        prompt += """

⚠️ CRÍTICO: El objetivo central y las temáticas principales son EL CORAZÓN de la obra.
Debes mencionarlos explícitamente en tu análisis y relacionarlos con las métricas cognitivas.
Pregúntate: ¿Cómo contribuyen el formalismo, creatividad, etc. a lograr este objetivo específico?

═══════════════════════════════════════════════════════════════════════
📚 FRAGMENTOS TEXTUALES ADICIONALES DEL DOCUMENTO (10 extractos)
═══════════════════════════════════════════════════════════════════════

⚠️ ESTOS SON TEXTOS LITERALES DISTRIBUIDOS A LO LARGO DE LA OBRA
    ÚSALOS EXTENSIVAMENTE PARA CITAR Y FUNDAMENTAR CADA AFIRMACIÓN
    Cada fragmento proviene del PDF identificado arriba

"""
        
        # Agregar fragmentos textuales (ahora 10 en lugar de 5)
        fragmentos = datos.get('fragmentos_textuales', [])
        if fragmentos:
            for i, fragmento in enumerate(fragmentos, 1):
                prompt += f"\n**Fragmento {i}:**\n\"{fragmento}\"\n"
        else:
            prompt += "\n(No hay fragmentos textuales disponibles)\n"
        
        # Agregar texto_muestra si está disponible
        texto_muestra = datos.get('rag_texto_muestra')
        if texto_muestra and len(str(texto_muestra)) > 50:
            prompt += f"\n\n**Texto Muestra Adicional (del campo RAG):**\n\"{texto_muestra[:1500]}...\"\n"
        
        # 🔍 AGREGAR ANÁLISIS ENRIQUECIDO RAG
        if datos.get('analisis_enriquecido'):
            enriq = datos['analisis_enriquecido']
            
            prompt += f"""

**📊 ANÁLISIS ENRIQUECIDO DEL DOCUMENTO:**

"""
            
            # Estadísticas textuales
            if enriq.get('estadisticas'):
                stats = enriq['estadisticas']
                prompt += f"""
**Estadísticas Textuales:**
- Total de palabras: {stats.get('total_palabras', 0):,}
- Total de oraciones: {stats.get('total_oraciones', 0)}
- Palabras por oración (promedio): {stats.get('promedio_palabras_oracion', 0):.1f}
- Vocabulario único: {stats.get('vocabulario_unico', 0):,} palabras
- Riqueza léxica: {stats.get('riqueza_lexica', 0):.3f}
"""
            
            # Autores citados
            if enriq.get('autores_citados'):
                prompt += f"\n**👥 Autores Citados (Top 10):**\n"
                for autor, freq in list(enriq['autores_citados'].items())[:10]:
                    prompt += f"- {autor}: {freq} menciones\n"
                
                if enriq.get('autor_referencia_principal'):
                    ref = enriq['autor_referencia_principal']
                    prompt += f"\n⭐ **Autor de referencia principal:** {ref['nombre']} ({ref['menciones']} menciones)\n"
            
            # Palabras clave jurídicas
            if enriq.get('palabras_clave'):
                prompt += f"\n**🔑 Palabras Clave Jurídicas (Top 15):**\n"
                for palabra, freq in list(enriq['palabras_clave'].items())[:15]:
                    prompt += f"- '{palabra}': {freq} ocurrencias\n"
            
            # Posiciones doctrinales
            if enriq.get('posiciones_doctrinales'):
                prompt += f"\n**📍 Posicionamiento Doctrinal Detectado:**\n"
                for tipo, fragmentos in enriq['posiciones_doctrinales'].items():
                    prompt += f"- **{tipo.upper()}** ({len(fragmentos)} instancias):\n"
                    if fragmentos:
                        prompt += f"  Ejemplo: '{fragmentos[0][:150]}...'\n"
            
            # 🎯 MARCADORES DE AUTORIDAD
            if enriq.get('marcadores_autoridad'):
                autoridad = enriq['marcadores_autoridad']
                prompt += f"\n**🎯 Marcadores de Autoridad y Relevancia:**\n"
                prompt += f"- Total de marcadores de autoridad: {autoridad.get('total_marcadores', 0)}\n"
                
                if autoridad.get('citas_libros'):
                    prompt += f"- Citas de libros/artículos: {len(autoridad['citas_libros'])}\n"
                    for cita in autoridad['citas_libros'][:3]:
                        prompt += f"  * {cita['autor']} ({cita['año']})\n"
                
                if autoridad.get('citas_normas'):
                    from collections import Counter
                    normas = [f"{c['tipo']} {c['numero']}" for c in autoridad['citas_normas']]
                    normas_freq = Counter(normas)
                    prompt += f"- Citas normativas: {len(autoridad['citas_normas'])}\n"
                    for norma, freq in normas_freq.most_common(3):
                        prompt += f"  * {norma}: {freq} referencias\n"
                
                if autoridad.get('doctrina_establecida'):
                    prompt += f"- Referencias a doctrina establecida: {len(autoridad['doctrina_establecida'])}\n"
                
                if autoridad.get('autoridad_reconocida'):
                    prompt += f"- Autoridades reconocidas mencionadas: {len(set(autoridad['autoridad_reconocida']))}\n"
            
            # 💬 ESTILO DISCURSIVO
            if enriq.get('estilo_discursivo'):
                estilo = enriq['estilo_discursivo']
                prompt += f"\n**💬 Análisis del Estilo Discursivo:**\n"
                
                prompt += f"\n*Uso de Imperativos y Obligaciones:*\n"
                prompt += f"- Verbos imperativos: {estilo['verbos_imperativos']['total']} "
                prompt += f"({estilo['verbos_imperativos']['densidad']:.2f} por 100 palabras)\n"
                if estilo['verbos_imperativos']['mas_frecuentes']:
                    prompt += f"- Más frecuentes: {', '.join([v for v, c in estilo['verbos_imperativos']['mas_frecuentes'][:3]])}\n"
                
                prompt += f"\n*Afirmaciones Universales:*\n"
                prompt += f"- Total: {estilo['afirmaciones_universales']['total']} "
                prompt += f"({estilo['afirmaciones_universales']['densidad']:.2f} por 100 palabras)\n"
                if estilo['afirmaciones_universales']['mas_frecuentes']:
                    prompt += f"- Más usadas: {', '.join([v for v, c in estilo['afirmaciones_universales']['mas_frecuentes'][:3]])}\n"
                
                prompt += f"\n*Lenguaje Valorativo:*\n"
                prompt += f"- Adjetivos valorativos: {estilo['adjetivos_valorativos']['total']} "
                prompt += f"({estilo['adjetivos_valorativos']['densidad']:.2f} por 100 palabras)\n"
                if estilo['adjetivos_valorativos']['mas_frecuentes']:
                    top_adj = ', '.join([v for v, c in estilo['adjetivos_valorativos']['mas_frecuentes'][:5]])
                    prompt += f"- Más usados: {top_adj}\n"
                
                prompt += f"\n*Marcadores de Énfasis:*\n"
                prompt += f"- Total: {estilo['marcadores_enfasis']['total']} "
                prompt += f"({estilo['marcadores_enfasis']['densidad']:.2f} por 100 palabras)\n"
                
                prompt += f"\n*Uso de Ejemplos:*\n"
                prompt += f"- Total de ejemplificaciones: {estilo['uso_ejemplos']['total']} "
                prompt += f"({estilo['uso_ejemplos']['densidad']:.2f} por 100 palabras)\n"
                
                prompt += f"\n*Índices Calculados:*\n"
                prompt += f"- **Índice de Asertividad:** {estilo['indice_asertividad']:.2f} (imperativo + universal + énfasis)\n"
                prompt += f"- **Índice de Subjetividad:** {estilo['indice_subjetividad']:.2f} (valorativo + énfasis)\n"
        
        prompt += f"""

**COMPARATIVAS CON OTROS AUTORES:**

"""
        
        # Agregar comparativas
        for comp in datos['comparativas']:
            prompt += f"- Comparado con {comp['autor_b']} ({comp['tipo']}): {comp['resultado']}\n"
        
        prompt += """

═══════════════════════════════════════════════════════════════════════
🎯 INSTRUCCIONES CRÍTICAS - FUNDAMENTACIÓN OBLIGATORIA
═══════════════════════════════════════════════════════════════════════

**REGLAS ABSOLUTAS QUE DEBES SEGUIR:**

1. ❌ PROHIBIDO usar términos técnicos SIN definirlos primero
   ✅ OBLIGATORIO: Define CADA término técnico la primera vez que lo uses
   Ejemplo CORRECTO: "El autor presenta un estilo *autoritativo* (es decir, 
   fundamenta sus afirmaciones mediante citas de autoridad reconocida, normas 
   y jurisprudencia establecida), como se evidencia en..."

2. ❌ PROHIBIDO hacer afirmaciones sin citas textuales
   ✅ OBLIGATORIO: Cada caracterización debe incluir AL MENOS 1-2 citas literales
   Ejemplo CORRECTO: El alto formalismo (0.85) se manifiesta cuando afirma: 
   "La tutela preventiva constituye un mecanismo procesal específicamente regulado..."

3. ❌ PROHIBIDO presentar métricas sin explicar qué significan
   ✅ OBLIGATORIO: Explica qué mide cada métrica y qué implica su valor
   Ejemplo CORRECTO: "Formalismo jurídico: 0.85 (escala 0-1). Este valor elevado 
   indica que el autor prioriza la estructura normativa formal, los conceptos 
   dogmáticos establecidos y el análisis sistemático del derecho positivo, en 
   lugar de aproximaciones sociológicas o críticas."

4. ❌ PROHIBIDO mencionar autores citados sin contexto
   ✅ OBLIGATORIO: Explica POR QUÉ y PARA QUÉ el autor los cita
   Ejemplo CORRECTO: "Cita frecuentemente a Calamandrei (12 menciones) para 
   fundamentar la naturaleza cautelar de la tutela preventiva, como cuando 
   afirma: 'Siguiendo a Calamandrei, entendemos que...'"

5. ❌ PROHIBIDO usar abstracciones vagas
   ✅ OBLIGATORIO: Proporciona evidencia textual CONCRETA de cada rasgo
   Ejemplo MAL: "El autor es dogmático"
   Ejemplo BIEN: "El autor presenta alta dogmaticidad (0.78), manifestada en 
   afirmaciones categóricas como: 'La tutela preventiva ES necesariamente una 
   medida cautelar' (énfasis agregado), sin considerar posturas alternativas."

6. 🔍 DATOS DISPONIBLES - ÚSALOS TODOS:
   - 52 campos completos de la base RAG (ver arriba)
   - Fragmentos textuales literales del documento
   - Autores citados, referencias doctrinarias, cadenas argumentativas
   - Estructura retórica, conectores, tipos de silogismo, mapa de fuerza
   - Metadatos JSON completos

**TAREA - INFORME FUNDAMENTADO:**

Genera un informe de 1800-2200 palabras siguiendo ESTRICTAMENTE este formato:

## 1. INTRODUCCIÓN CONTEXTUALIZADA (200 palabras)

**DEBES INCLUIR:**
- Autor y obra completa analizada
- Contexto de publicación (fecha, periodo doctrinal si disponible)
- Extensión del trabajo: [X] palabras, [Y] oraciones promedio
- Riqueza léxica: [Z] vocabulario único
- **Tesis central del autor** (extraída de los fragmentos textuales)
- Perfil cognitivo general resumido en 2-3 características principales

## 2. ANÁLISIS COGNITIVO FUNDAMENTADO (400 palabras)

**ESTRUCTURA OBLIGATORIA para CADA rasgo:**

### [RASGO]: [Valor numérico] - [Interpretación del valor]

**Definición:** [Explica qué significa este rasgo en términos simples]

**Evidencia textual:** [2-3 citas literales entrecomilladas que demuestren el rasgo]

**Análisis:** [Relaciona las citas con el valor numérico y otros indicadores]

**RASGOS A ANALIZAR:**
a) Formalismo jurídico [valor]
b) Creatividad conceptual [valor]
c) Dogmatismo [valor]
d) Empirismo evidencial [valor]
e) Nivel de abstracción [valor]
f) Uso de jurisprudencia [valor]

## 3. ANÁLISIS METODOLÓGICO CON EVIDENCIA (300 palabras)

**DEBES INCLUIR:**
- Tipo de razonamiento dominante (deductivo/inductivo/abductivo/analógico)
  → DEFINICIÓN del tipo identificado
  → 2 ejemplos textuales que lo demuestren
  
- Modalidad epistémica (asertiva/dubitativa/condicional)
  → DEFINICIÓN de la modalidad
  → Ejemplos de verbos/expresiones que la caracterizan en el texto
  
- Vocabulario jurídico especializado:
  → Lista de 10-15 términos clave más frecuentes
  → Para 3-5 términos: mostrar CÓMO los usa (con cita textual)

## 4. CONSTRUCCIÓN DE AUTORIDAD Y FUNDAMENTACIÓN (350 palabras)

**ESTRUCTURA:**

### a) Fuentes de Autoridad Utilizadas

**Citas normativas:** [Cantidad e importancia]
- Ejemplos: "[Cita textual donde menciona norma X]"
- Función: [¿Para qué las usa? ¿Fundamento? ¿Ilustración?]

**Citas doctrinarias:** [Cantidad y autores principales]
- Top 3 autores citados: [Nombres con frecuencia]
- Ejemplo de uso: "[Cita textual donde cita a autor Y]"
- Rol argumentativo: [¿Apoya su tesis? ¿Refuta? ¿Actualiza?]

**Jurisprudencia:** [Nivel de uso: alto/medio/bajo]
- Ejemplos: "[Cita textual de referencia jurisprudencial]"

### b) Tipo de Autoridad Construida

**DEFINE primero qué significa cada tipo, luego justifica:**

- **Autoritativo** = fundamenta mediante citas de autoridad externa
- **Original** = construye argumentos propios sin apoyo constante
- **Ecléctico** = combina autoridad externa y razonamiento propio

**Clasificación del autor:** [Tipo identificado]
**Justificación:** [Citas + análisis de densidad de citas vs. argumentación propia]

## 5. ANÁLISIS DEL ESTILO DISCURSIVO CON EJEMPLOS (300 palabras)

**NO digas "es asertivo" sin demostrar CÓMO:**

### Asertividad [Índice: X.XX]

**Definición:** Grado en que el autor hace afirmaciones categóricas, imperativas o universales

**Indicadores encontrados:**
- Verbos imperativos: [Cantidad] - Ejemplos: "[debe/corresponde/es necesario]"
  → Cita: "[Fragmento textual donde usa imperativo]"
  
- Afirmaciones universales: [Cantidad] - Ejemplos: "[siempre/nunca/todos]"
  → Cita: "[Fragmento con afirmación universal]"
  
- Marcadores de énfasis: [Cantidad] - Ejemplos: "[claramente/obviamente]"
  → Cita: "[Fragmento con énfasis]"

### Subjetividad [Índice: X.XX]

**Definición:** Presencia de valoraciones personales, juicios éticos o adjetivos evaluativos

**Evidencia:**
- Adjetivos valorativos: [Lista de 5-10 más frecuentes]
- Ejemplos en contexto: "[Citas mostrando uso de valorativos]"
- Interpretación: ¿Evalúa moralmente? ¿Crítica? ¿Elogia?

### Uso de Ejemplos [Frecuencia: X por cada 100 palabras]

**Función pedagógica:**
- Ejemplo típico: "[Cita donde introduce un ejemplo]"
- Propósito: ¿Ilustrar? ¿Demostrar? ¿Persuadir?

## 6. MAPA DE INFLUENCIAS INTELECTUALES (250 palabras)

**ESTRUCTURA:**

### Autor de Referencia Principal: [NOMBRE]

**Frecuencia:** [X menciones]
**Contexto de uso:** [¿Para qué lo cita? ¿Qué toma de él?]
**Cita representativa:** "[Fragmento mostrando cómo lo usa]"

### Red de Influencias Secundarias

Top 10 autores citados con frecuencia:
1. [Autor] - [X veces] - [Rol: ¿Base teórica? ¿Contraste? ¿Actualización?]
2. [...]

### Corriente Doctrinal Identificada

**Posicionamiento:** [A favor de X / Contra Y / Neutral / Crítico]
**DEFINICIÓN de la corriente:** [Explica brevemente qué es]
**Evidencia:** "[Citas textuales que muestren su posición]"

## 7. PERFIL ARISTOTÉLICO FUNDAMENTADO (200 palabras)

**NO digas "alto ethos" sin explicar POR QUÉ:**

### Ethos (Credibilidad): [Valor numérico]

**Definición:** Autoridad moral/intelectual que proyecta el autor

**CÓMO construye credibilidad:**
- "[Cita mostrando construcción de ethos]"
- Estrategia: [¿Por citas? ¿Por cargo? ¿Por razonamiento?]

### Pathos (Apelación emocional): [Valor numérico]

**Definición:** Grado de apelación a emociones, valores o urgencia

**Evidencia:** "[Citas con carga emocional/valorativa]"

### Logos (Lógica argumentativa): [Valor numérico]

**Definición:** Rigor lógico, estructura silogística, coherencia

**Evidencia:** "[Fragmento mostrando razonamiento lógico]"

## 8. SÍNTESIS INTEGRADORA (300 palabras)

**Perfil intelectual único:**
- Características cognitivas distintivas [con evidencia]
- Estilo discursivo característico [con ejemplos]
- Influencias principales [con nombres]
- Vocabulario técnico recurrente [lista]
- Rol en el campo: [¿Innovador? ¿Sistematizador? ¿Divulgador? ¿Crítico?]
  → JUSTIFICA con evidencia concreta

## 9. POSICIONAMIENTO COMPARATIVO (150 palabras)

**Comparado con otros autores del corpus:**
- Similitudes: [Con quiénes y en qué]
- Diferencias: [Rasgos únicos o distintivos]
- Aporte específico: [Qué contribuye que otros no]

═══════════════════════════════════════════════════════════════════════
📋 CHECKLIST FINAL - VERIFICA ANTES DE ENTREGAR:
═══════════════════════════════════════════════════════════════════════

□ Cada término técnico está DEFINIDO la primera vez
□ Cada afirmación tiene AL MENOS 1 cita textual literal entrecomillada
□ Cada métrica numérica está EXPLICADA (qué mide, qué implica su valor)
□ Los autores citados tienen CONTEXTO (por qué y para qué se citan)
□ NO hay abstracciones vagas sin evidencia concreta
□ Total 1800-2200 palabras
□ Formato markdown con ## y ###
□ Palabras clave en *cursiva*
- Resalta datos numéricos importantes en **negrita**
- Sé MUY específico, fundamentado y académico
- Usa evidencia textual concreta para cada afirmación
- Relaciona todas las métricas entre sí (busca coherencia o contradicciones)
- Longitud total: 1500-1800 palabras

**IMPORTANTE:**
- Analiza cómo los marcadores de autoridad se relacionan con el índice de formalismo
- Explica si la asertividad coincide con el tipo de razonamiento detectado
- Interpreta la subjetividad en relación con dogmatismo/empirismo
- Conecta el uso de ejemplos con la claridad argumentativa

Genera el informe exhaustivo y profundamente analítico ahora:
"""
        
        return prompt
    
    def _extraer_metricas_clave(self, datos: Dict) -> Dict:
        """Extrae métricas clave para visualización"""
        def get_rag(key, default=0):
            return float(datos.get(f'rag_{key}', default))
        
        return {
            "rasgos_cognitivos": {
                "formalismo": get_rag('formalismo'),
                "creatividad": get_rag('creatividad'),
                "dogmatismo": get_rag('dogmatismo'),
                "empirismo": get_rag('empirismo'),
                "interdisciplinariedad": get_rag('interdisciplinariedad'),
                "abstraccion": get_rag('nivel_abstraccion'),
                "sintaxis": get_rag('complejidad_sintactica'),
                "jurisprudencia": get_rag('uso_jurisprudencia')
            },
            "aristotelico": {
                "ethos": get_rag('ethos'),
                "pathos": get_rag('pathos'),
                "logos": get_rag('logos')
            },
            "metodologico": {
                "razonamiento": datos.get('rag_razonamiento_dominante', 'N/A'),
                "modalidad": datos.get('rag_modalidad_epistemica', 'N/A'),
                "densidad_citas": get_rag('densidad_citas'),
                "uso_ejemplos": get_rag('uso_ejemplos')
            }
        }

# Instancia global
generador_informes = GeneradorInformesGemini()

if __name__ == "__main__":
    # Test
    import sys
    if len(sys.argv) > 1:
        autor = " ".join(sys.argv[1:])
        resultado = generador_informes.generar_informe_con_gemini(autor)
        
        if "error" in resultado:
            print(f"❌ {resultado['error']}")
        else:
            print("\n" + "="*70)
            print(f"📄 INFORME PARA: {resultado['autor']}")
            print("="*70)
            print(resultado['informe_gemini'])
    else:
        print("Uso: python generador_informes_gemini.py 'Nombre del Autor'")
