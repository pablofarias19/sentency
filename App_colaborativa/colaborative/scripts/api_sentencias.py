# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import sys
import os

# Agregar ruta para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from query_rag_sentencias import buscar
    from analyser_metodo_mejorado import detectar_ethos_pathos_logos
    RAG_DISPONIBLE = True
except ImportError as e:
    print(f"⚠️ Advertencia: {e}")
    RAG_DISPONIBLE = False

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "servicio": "API Sentencias v7.4",
        "endpoints": [
            "POST /buscar-sentencias",
            "POST /analizar-contenido-autoral"
        ],
        "estado": "activo" if RAG_DISPONIBLE else "parcial"
    })

@app.route("/buscar-sentencias", methods=["POST"])
def api_buscar_sentencias():
    if not RAG_DISPONIBLE:
        return jsonify({"error": "Sistema RAG no disponible"}), 503
        
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()
    filtros = {
        "tema": data.get("tema"),
        "falacia": data.get("falacia"),
        "razonamiento": data.get("razonamiento"),
        "tribunal": data.get("tribunal"),
        "desde": data.get("desde"),
        "hasta": data.get("hasta"),
    }
    if not query:
        return jsonify({"error": "query es requerido"}), 400

    try:
        res = buscar(query, filtros=filtros, topk=data.get("topk", 30))
        out = []
        for boost, r in res[:data.get("limit", 20)]:
            out.append({
                "chunk_id": r[0],
                "expediente": r[1],
                "fuente_pdf": r[2],
                "fecha_sentencia": r[3],
                "tribunal": r[4],
                "jurisdiccion": r[5],
                "materia": r[6],
                "temas": r[7],
                "formas_razonamiento": r[8],
                "falacias": r[9],
                "citaciones_doctrina": r[10],
                "citaciones_jurisprudencia": r[11],
                "texto_snippet": (r[12][:500] + "…") if r[12] and len(r[12]) > 500 else r[12],
                "distancia_doctrinal": r[13],  # <--- NUEVO V7.5
                "boost": boost
            })
        return jsonify({"resultados": out, "total": len(out)})
    except Exception as e:
        return jsonify({"error": f"Error en búsqueda: {str(e)}"}), 500

@app.route("/analizar-contenido-autoral", methods=["POST"])
def api_analizar_autoral():
    data = request.get_json(silent=True) or {}
    texto = (data.get("texto") or "").strip()
    if not texto or len(texto) < 100:
        return jsonify({"error": "texto insuficiente (>=100 caracteres)"}), 400
    
    try:
        analisis = detectar_ethos_pathos_logos(texto)
        return jsonify({"analisis_autoral": analisis})
    except Exception as e:
        return jsonify({"error": f"Error en análisis: {str(e)}"}), 500

if __name__ == "__main__":
    print("🚀 Iniciando API Sentencias v7.4")
    print("📍 Endpoints disponibles:")
    print("   GET  /                     → Info del servicio")
    print("   POST /buscar-sentencias    → Búsqueda RAG con filtros")
    print("   POST /analizar-contenido-autoral → Análisis retórico")
    print()
    print("🌐 Servidor en: http://127.0.0.1:5010")
    print("🔧 Modo desarrollo activado")
    
    # Modo desarrollo
    app.run(host="127.0.0.1", port=5010, debug=True)