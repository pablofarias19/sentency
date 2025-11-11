# -*- coding: utf-8 -*-
"""
Pipeline de autoevaluación doctrinaria con historial
Permite refinar respuestas y guardar el historial de aprendizaje.
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from transformers import pipeline
from pipeline_resumen_doctrinario import run_doctrina_pipeline, DoctrinaRespuesta

# Imports robustos para autoaprendizaje y perfiles cognitivos
try:
    from autoaprendizaje import guardar_autoevaluacion, generar_contexto_adaptativo
    from profiles_rag import enrich_prompt_with_profiles
    print("✅ Módulos de autoaprendizaje y PCA cargados")
except ImportError:
    # Añadir directorio actual para imports
    sys.path.append(os.path.dirname(__file__))
    try:
        from autoaprendizaje import guardar_autoevaluacion, generar_contexto_adaptativo
        from profiles_rag import enrich_prompt_with_profiles
        print("✅ Módulos de autoaprendizaje y PCA cargados (path local)")
    except ImportError as e:
        print(f"⚠️ Error cargando módulos PCA: {e}")
        # Función fallback si no está disponible
        def enrich_prompt_with_profiles(pregunta, base_titulo="", k=5):
            return "Sistema de perfiles cognitivos no disponible."

# ============================================================
# 🔹 Integración híbrida: Gemini 2.5-Pro + Flan-T5 fallback
# ============================================================
import google.generativeai as genai
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Configurar la API Key de Gemini
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

def obtener_modelo_gemini():
    """
    Intenta usar el modelo Gemini 2.5-Pro si está disponible.
    Si no, retorna None para forzar el uso del modelo local.
    """
    try:
        modelos_disponibles = [m.name for m in genai.list_models()]
        for preferido in [
            "models/gemini-2.5-pro",
            "models/gemini-2.5-flash",
            "models/gemini-pro-latest",
        ]:
            if preferido in modelos_disponibles:
                print(f"✅ Gemini activo — modelo seleccionado: {preferido}")
                return genai.GenerativeModel(preferido)
        print("⚠️ Gemini no disponible — se usará Flan-T5-Base local.")
        return None
    except Exception as e:
        print(f"⚠️ Error al verificar Gemini: {e}")
        return None

# Instanciar el modelo híbrido
model_gemini = obtener_modelo_gemini()

# ============================================================
# 🔹 Modelo local (Flan-T5) de respaldo
# ============================================================
tokenizer_t5 = AutoTokenizer.from_pretrained("google/flan-t5-base")
model_t5 = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# ====== CONFIG ======
LOGS_DIR = Path("colaborative/data/logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
HISTORIAL_PATH = LOGS_DIR / "refinamiento.json"

# ====== FUNCIONES AUXILIARES ======
def guardar_historial(entry: dict):
    """Guarda un registro JSON en el historial"""
    data = []
    if HISTORIAL_PATH.exists():
        try:
            data = json.loads(HISTORIAL_PATH.read_text(encoding="utf-8"))
        except:
            data = []
    data.append(entry)
    HISTORIAL_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def cargar_historial():
    """Devuelve la lista de registros del historial"""
    if HISTORIAL_PATH.exists():
        try:
            return json.loads(HISTORIAL_PATH.read_text(encoding="utf-8"))
        except:
            return []
    return []

# ===============================================================
# 📘 FUNCIÓN: self_refine_doctrina
# ===============================================================
# Combina el pipeline local (RAG + Flan-T5) con revisión lingüística de Gemini.
# Si Gemini no responde o no hay conexión, usa Flan-T5 como fallback automático.
# ===============================================================

def self_refine_doctrina(pregunta: str, base: str = "general"):
    """
    Ejecuta el flujo doctrinario completo:
    1️⃣ Ejecuta el pipeline local RAG (Embeddings → FAISS → Generador)
    2️⃣ Hace una autoevaluación con Flan-T5 (versión rápida)
    3️⃣ Intenta mejorar la redacción con Gemini-Pro (gratuito)
    4️⃣ Si Gemini falla, mantiene la versión local
    5️⃣ Guarda todo en el historial para trazabilidad
    """

    # ===========================================================
    # 🔹 Paso 1: Pipeline doctrinario local
    # ===========================================================
    respuesta: DoctrinaRespuesta = run_doctrina_pipeline(pregunta, k=3, base=base)

    # ===========================================================
    # 🔹 Paso 2: Autoevaluación con modelo local (Flan-T5-Base)
    # ===========================================================
    prompt_eval = f"""
Evalúa el siguiente texto doctrinario y propón una mejora jurídica breve.
Pregunta: {respuesta.pregunta}
Texto original:
{respuesta.concepto_consolidado}
Fragmentos doctrinarios:
{''.join([c['resumen'] for c in respuesta.fragmentos_usados[:3]])}
    """
    try:
        model_eval = pipeline("text2text-generation", model="google/flan-t5-base")
        texto_mejorado = model_eval(prompt_eval, max_new_tokens=256, do_sample=False)[0]["generated_text"].strip()
    except Exception as e:
        print(f"⚠️ Error en modelo local (Flan-T5): {e}")
        texto_mejorado = respuesta.concepto_consolidado

    # ===========================================================
    # 🔹 Paso 3: Refinamiento con autoaprendizaje + perfiles cognitivos
    # ===========================================================
    # Generar contexto adaptativo basado en autoevaluaciones previas
    contexto_adaptativo = generar_contexto_adaptativo()
    
    # 🆕 Generar contexto cognitivo basado en gemelos cognitivos
    contexto_cognitivo = enrich_prompt_with_profiles(pregunta, base.title(), k=6)
    
    prompt_refinamiento = f"""
CONTEXTO DE APRENDIZAJE CONTINUO:
{contexto_adaptativo}

{contexto_cognitivo}

INSTRUCCIÓN:
Redacta un concepto doctrinario en español jurídico argentino, con precisión técnica y coherencia metodológica.
Usa EXCLUSIVAMENTE los fragmentos proporcionados; si falta base, indícalo.
Diferencia de lege lata / de lege ferenda cuando corresponda. Mantén consistencia terminológica.
Considera los marcos y estrategias de referencia del contexto cognitivo.

PREGUNTA: {pregunta}

TEXTO A REFINAR:
\"\"\"{texto_mejorado}\"\"\"

FRAGMENTOS DOCTRINARIOS DE BASE:
{''.join([f"• {c['resumen']}\n" for c in respuesta.fragmentos_usados[:3]])}
"""

    try:
        if model_gemini and os.getenv("USE_GEMINI", "True") == "True":
            # Usar Gemini con contexto adaptativo
            result = model_gemini.generate_content(prompt_refinamiento)
            revision_gemini = getattr(result, "text", None)
            
            if revision_gemini:
                print("✅ Texto refinado con Gemini + contexto adaptativo")
                
                # Segunda pasada: autoevaluación del texto generado
                evaluacion = model_gemini.generate_content(
                    f"Evalúa la calidad técnica y terminológica del siguiente texto doctrinario, asigna una puntuación de 1 a 10 y explica brevemente tu criterio:\n\n{revision_gemini}"
                )
                texto_eval = evaluacion.text.strip()
                
                # Extraer puntaje si existe
                import re
                match = re.search(r"(\d+(\.\d+)?)", texto_eval)
                puntaje = float(match.group(1)) if match else 0.0
                
                # Guardar en base de datos de autoaprendizaje
                guardar_autoevaluacion(
                    "Gemini-2.5-Pro", 
                    respuesta.pregunta, 
                    revision_gemini, 
                    texto_eval, 
                    puntaje, 
                    prompt_refinamiento
                )
                
                print(f"📊 Autoevaluación guardada: {puntaje}/10")
                revision_gemini += f"\n\n🧭 Autoevaluación ({puntaje}/10):\n{texto_eval}"
            else:
                print("⚠️ Gemini devolvió texto vacío; usando Flan-T5 local.")
                # Fallback a Flan-T5
                input_ids = tokenizer_t5(prompt_refinamiento, return_tensors="pt", truncation=True, max_length=512).input_ids
                outputs = model_t5.generate(input_ids, max_new_tokens=256, do_sample=False)
                revision_gemini = tokenizer_t5.decode(outputs[0], skip_special_tokens=True).strip()
                
                # Guardar sin autoevaluación
                guardar_autoevaluacion(
                    "Flan-T5-Base", 
                    respuesta.pregunta, 
                    revision_gemini, 
                    "Sin autoevaluación (modo local)", 
                    0, 
                    prompt_refinamiento
                )
        else:
            # Usar Flan-T5 local como fallback
            print("ℹ️ Usando Flan-T5 local para refinamiento")
            input_ids = tokenizer_t5(prompt_refinamiento, return_tensors="pt", truncation=True, max_length=512).input_ids
            outputs = model_t5.generate(input_ids, max_new_tokens=256, do_sample=False)
            revision_gemini = tokenizer_t5.decode(outputs[0], skip_special_tokens=True).strip()
            
            # Guardar sin autoevaluación
            guardar_autoevaluacion(
                "Flan-T5-Base", 
                respuesta.pregunta, 
                revision_gemini, 
                "Sin autoevaluación (modo local)", 
                0, 
                prompt_refinamiento
            )
    except Exception as e:
        print(f"⚠️ Error en refinamiento híbrido: {e}")
        revision_gemini = texto_mejorado

    # ===========================================================
    # 🔹 Paso 4: Guardar resultado en historial (auto-auditoría)
    # ===========================================================
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "fecha": fecha,
        "pregunta": respuesta.pregunta,
        "concepto_original": respuesta.concepto_consolidado,
        "concepto_refinado": revision_gemini,
        "entidades": respuesta.entidades,
        "base": base,
        "fuentes": [c["fuente"] for c in respuesta.fragmentos_usados[:3]],
        "modelo_final": "Gemini-2.5-Pro" if model_gemini and revision_gemini != texto_mejorado else "Flan-T5-Base",
    }
    guardar_historial(entry)

    # ===========================================================
    # 🔹 Paso 5: Devolver respuesta refinada al front-end
    # ===========================================================
    respuesta.concepto_consolidado = revision_gemini
    return respuesta