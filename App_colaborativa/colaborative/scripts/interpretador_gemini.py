# -*- coding: utf-8 -*-
"""
🧠 INTERPRETADOR DE DISTANCIA DOCTRINAL USANDO GEMINI - V7.6
===========================================================

Analiza las sentencias judiciales en base a su distancia doctrinal FAISS
y produce un texto explicativo de por qué existe (o no) un apartamiento
respecto de la base doctrinal consolidada.

CARACTERÍSTICAS:
- Análisis hermenéutico profundo
- Explicación de apartamientos doctrinales
- Evaluación de coherencia sistémica
- Impacto en la seguridad jurídica

AUTOR: Sistema Cognitivo v7.6
FECHA: 10 NOV 2025
"""

import os
import json
import requests
from typing import Dict, Optional
from datetime import datetime

# Configuración GEMINI - buscar en múltiples variables
def obtener_api_key():
    """Busca API Key en múltiples variables de entorno"""
    api_key_sources = [
        os.getenv("GEMINI_API_KEY"),
        os.getenv("GOOGLE_API_KEY"), 
        os.getenv("GOOGLE_AI_API_KEY")
    ]
    
    for api_key in api_key_sources:
        if api_key and api_key != "TU_API_KEY_AQUI":
            return api_key
    
    return None

GEMINI_API_KEY = obtener_api_key()
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

def verificar_api_key():
    """Verifica si la API key está configurada"""
    if not GEMINI_API_KEY:
        print("❌ API Key no encontrada en: GEMINI_API_KEY, GOOGLE_API_KEY, GOOGLE_AI_API_KEY")
        return False
    
    print(f"✅ API Key encontrada: {GEMINI_API_KEY[:8]}...{GEMINI_API_KEY[-4:]}")
    return True

def identificar_seccion_sentencia(texto: str) -> str:
    """Identifica en qué sección de la sentencia se encuentra el texto"""
    texto_upper = texto.upper()
    
    # Buscar indicadores de cada sección
    if any(patron in texto_upper for patron in ['VISTO', 'DEMANDA INTERPUESTA', 'AUTOS:']):
        return 'VISTO'
    elif any(patron in texto_upper for patron in ['CONSIDERANDO', 'QUE SURGE DE AUTOS', 'DOCTRINA', 'JURISPRUDENCIA']):
        return 'CONSIDERANDO'
    elif any(patron in texto_upper for patron in ['RESUELVO', 'FALLO', 'HACER LUGAR', 'RECHAZAR']):
        return 'RESUELVO'
    else:
        return 'INDETERMINADA'

def construir_prompt_interpretativo(data: dict) -> str:
    """
    Construye el prompt específico para análisis doctrinal considerando
    la estructura tripartita de la sentencia (VISTO-CONSIDERANDO-RESUELVO)
    """
    distancia = data.get("distancia_doctrinal", 0)
    texto = data.get("texto_snippet", "")[:2000]  # Límite de seguridad
    temas = data.get("temas", "")
    razonamiento = data.get("formas_razonamiento", "")
    falacias = data.get("falacias", "") 
    doctrina = data.get("citaciones_doctrina", "")
    jurisprudencia = data.get("citaciones_jurisprudencia", "")
    tribunal = data.get("tribunal", "")
    materia = data.get("materia", "")
    
    # Identificar sección de la sentencia
    seccion_detectada = identificar_seccion_sentencia(texto)
    
    # Categorizar distancia para contexto
    if distancia <= 0.20:
        categoria = "ALINEACIÓN DOCTRINAL (coherente con doctrina consolidada)"
    elif distancia <= 0.50:
        categoria = "RELECTURA MODERADA (apartamiento controlado)"
    else:
        categoria = "APARTAMIENTO SIGNIFICATIVO (requiere justificación reforzada)"
    
    # Contexto específico según la sección
    contexto_seccion = {
        'VISTO': 'Esta es la sección inicial que identifica la demanda, partes y objeto del proceso.',
        'CONSIDERANDO': 'Esta es la sección donde se explican los hechos y el razonamiento jurídico del tribunal. AQUÍ SE MIDE PRINCIPALMENTE LA DISTANCIA DOCTRINAL.',
        'RESUELVO': 'Esta es la parte dispositiva donde se definen las cuestiones desde la óptica del tribunal.',
        'INDETERMINADA': 'Sección no identificada claramente.'
    }
    
    enfoque_seccion = {
        'VISTO': 'Analiza cómo se presenta el caso y si hay elementos procesales relevantes.',
        'CONSIDERANDO': 'FOCO PRINCIPAL: Analiza el razonamiento jurídico, citas doctrinales, y apartamientos de la doctrina consolidada.',
        'RESUELVO': 'Analiza las decisiones finales y su coherencia con el razonamiento previo.',
        'INDETERMINADA': 'Realiza análisis general del contenido jurídico.'
    }

    prompt = f"""
Eres un experto en hermenéutica jurídica especializado en análisis de sentencias argentinas. Analiza el siguiente fragmento considerando la estructura tripartita de las sentencias (VISTO-CONSIDERANDO-RESUELVO).

CONTEXTO PROCESAL:
- Tribunal: {tribunal}
- Materia: {materia}
- Sección identificada: {seccion_detectada}
- Distancia doctrinal calculada: {distancia:.4f}
- Categoría: {categoria}

CONTEXTO ESTRUCTURAL:
{contexto_seccion[seccion_detectada]}

FRAGMENTO DE SENTENCIA:
{texto}

METADATOS COGNITIVOS:
- Temas identificados: {temas}
- Formas de razonamiento: {razonamiento}
- Falacias detectadas: {falacias}
- Citaciones doctrinarias: {doctrina}
- Citaciones jurisprudenciales: {jurisprudencia}

ANÁLISIS REQUERIDO ({enfoque_seccion[seccion_detectada]}):
Proporciona un comentario técnico y sintético (máximo 400 palabras) que explique:

1. DIAGNÓSTICO DOCTRINAL: ¿Por qué la distancia doctrinal es {distancia:.2f}? ¿Qué principios o doctrinas se reinterpretan?

2. HERMENÉUTICA JUDICIAL: ¿El razonamiento mantiene coherencia con el sistema jurídico? ¿Hay innovación jurisprudencial justificada?

3. IMPACTO SISTÉMICO: ¿Qué efectos puede tener esta interpretación en la seguridad jurídica y predictibilidad del derecho?

4. ANÁLISIS SECCIONAL: Considerando que esto pertenece a la sección {seccion_detectada}, ¿es apropiado el nivel de apartamiento doctrinal aquí?

4. VALORACIÓN CRÍTICA: ¿Se mantiene proporcionalidad, racionalidad y fundamento axiológico?

Responde con rigor técnico pero lenguaje claro, priorizando la utilidad práctica para operadores jurídicos.
"""
    
    return prompt

def interpretar_sentencia(data: dict) -> dict:
    """
    Genera análisis hermenéutico sobre la distancia doctrinal
    
    Args:
        data: Diccionario con datos del chunk de sentencia
        
    Returns:
        Dict con interpretación y metadatos
    """
    
    # Verificar API key
    if not verificar_api_key():
        return {
            "interpretacion": "⚠️ API Key de GEMINI no configurada. Configura la variable de entorno GEMINI_API_KEY",
            "estado": "error_config",
            "timestamp": datetime.now().isoformat()
        }
    
    # Validar datos de entrada
    if not data.get("texto_snippet"):
        return {
            "interpretacion": "⚠️ No hay texto disponible para interpretar",
            "estado": "error_datos",
            "timestamp": datetime.now().isoformat()
        }
    
    # Construir prompt
    prompt = construir_prompt_interpretativo(data)
    
    # Configurar request a GEMINI
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,  # Bajo para mantener consistencia técnica
            "maxOutputTokens": 500,
            "topP": 0.8,
            "topK": 40
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH", 
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    }
    
    try:
        print(f"🧠 Consultando GEMINI para chunk {data.get('chunk_id', 'desconocido')}...")
        
        response = requests.post(
            GEMINI_URL, 
            headers=headers, 
            params=params, 
            data=json.dumps(payload),
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extraer texto de respuesta
        candidates = result.get("candidates", [])
        if not candidates:
            return {
                "interpretacion": "⚠️ GEMINI no generó respuesta válida",
                "estado": "error_respuesta",
                "timestamp": datetime.now().isoformat()
            }
        
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if not parts:
            return {
                "interpretacion": "⚠️ Respuesta de GEMINI vacía", 
                "estado": "error_vacio",
                "timestamp": datetime.now().isoformat()
            }
        
        interpretacion = parts[0].get("text", "").strip()
        
        if not interpretacion:
            return {
                "interpretacion": "⚠️ Texto de interpretación vacío",
                "estado": "error_contenido",
                "timestamp": datetime.now().isoformat()
            }
        
        # Respuesta exitosa
        return {
            "interpretacion": interpretacion,
            "estado": "exitoso",
            "timestamp": datetime.now().isoformat(),
            "distancia_analizada": data.get("distancia_doctrinal", 0),
            "tokens_utilizados": len(prompt.split()) + len(interpretacion.split())
        }
        
    except requests.exceptions.Timeout:
        return {
            "interpretacion": "⚠️ Timeout consultando GEMINI (>30s)",
            "estado": "error_timeout", 
            "timestamp": datetime.now().isoformat()
        }
    except requests.exceptions.RequestException as e:
        return {
            "interpretacion": f"⚠️ Error de conexión con GEMINI: {str(e)}",
            "estado": "error_conexion",
            "timestamp": datetime.now().isoformat()
        }
    except json.JSONDecodeError as e:
        return {
            "interpretacion": f"⚠️ Error decodificando respuesta GEMINI: {str(e)}",
            "estado": "error_json",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "interpretacion": f"⚠️ Error inesperado: {str(e)}",
            "estado": "error_general",
            "timestamp": datetime.now().isoformat()
        }

def interpretar_lote_sentencias(chunks_data: list) -> list:
    """
    Interpreta múltiples chunks en lote
    
    Args:
        chunks_data: Lista de diccionarios con datos de chunks
        
    Returns:
        Lista de resultados de interpretación
    """
    resultados = []
    
    print(f"🧠 Iniciando interpretación de {len(chunks_data)} chunks...")
    
    for i, chunk_data in enumerate(chunks_data, 1):
        print(f"   Procesando {i}/{len(chunks_data)}...")
        
        resultado = interpretar_sentencia(chunk_data)
        resultado["chunk_id"] = chunk_data.get("chunk_id")
        resultado["orden_procesamiento"] = i
        
        resultados.append(resultado)
        
        # Pausa entre requests para no saturar API
        import time
        time.sleep(1)
    
    print("✅ Interpretación en lote completada")
    return resultados

if __name__ == "__main__":
    # Test básico
    print("🧠 TEST INTERPRETADOR GEMINI V7.6")
    print("=" * 40)
    
    if not verificar_api_key():
        print("❌ Configura GEMINI_API_KEY como variable de entorno")
        print("   Ejemplo: set GEMINI_API_KEY=tu_clave_aqui")
    else:
        print("✅ API Key configurada")
        
        # Test con datos de ejemplo
        test_data = {
            "chunk_id": "test_001",
            "texto_snippet": "La aplicación del principio de proporcionalidad requiere un análisis integral de las circunstancias del caso, considerando tanto la finalidad perseguida como los medios empleados para alcanzarla.",
            "distancia_doctrinal": 0.35,
            "temas": "proporcionalidad, análisis integral",
            "formas_razonamiento": "deductivo, sistemático",
            "falacias": "",
            "citaciones_doctrina": "Alexy, R. - Teoría de los Derechos Fundamentales",
            "tribunal": "Tribunal Superior de Justicia",
            "materia": "constitucional"
        }
        
        resultado = interpretar_sentencia(test_data)
        print(f"Estado: {resultado['estado']}")
        print(f"Interpretación: {resultado['interpretacion'][:200]}...")