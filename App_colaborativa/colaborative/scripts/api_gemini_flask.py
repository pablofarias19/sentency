# -*- coding: utf-8 -*-
"""
🌐 API FLASK PARA INTERPRETACIÓN GEMINI - V7.6
==============================================

Endpoint Flask que expone la funcionalidad de interpretación doctrinal
usando GEMINI para análisis hermenéutico de sentencias.

ENDPOINTS:
- POST /interpretar-distancia: Interpreta un chunk específico
- GET /estado-api: Verifica estado del servicio
- POST /interpretar-lote: Interpreta múltiples chunks

AUTOR: Sistema Cognitivo v7.6
FECHA: 10 NOV 2025
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3
import os
from pathlib import Path
from datetime import datetime

from interpretador_gemini import interpretar_sentencia, interpretar_lote_sentencias, verificar_api_key
from config_rutas import PENSAMIENTO_DB

app = Flask(__name__)
CORS(app)  # Permitir CORS para integración web

def ensure_interpretacion_column():
    """Asegura que existe la columna interpretacion_doctrinal"""
    try:
        con = sqlite3.connect(PENSAMIENTO_DB)
        cur = con.cursor()
        
        # Verificar si la columna existe
        cur.execute("PRAGMA table_info(rag_sentencias_chunks)")
        columnas = [col[1] for col in cur.fetchall()]
        
        if 'interpretacion_doctrinal' not in columnas:
            print("🔧 Agregando columna interpretacion_doctrinal...")
            cur.execute("ALTER TABLE rag_sentencias_chunks ADD COLUMN interpretacion_doctrinal TEXT")
            con.commit()
            print("✅ Columna interpretacion_doctrinal agregada")
        
        con.close()
        return True
        
    except Exception as e:
        print(f"❌ Error configurando BD: {e}")
        return False

def get_chunk_by_id(chunk_id: str) -> dict:
    """Obtiene datos completos de un chunk por ID"""
    try:
        con = sqlite3.connect(PENSAMIENTO_DB)
        cur = con.cursor()
        
        cur.execute("""
            SELECT chunk_id, expediente, fuente_pdf, fecha_sentencia, tribunal,
                   jurisdiccion, materia, temas, formas_razonamiento, falacias,
                   citaciones_doctrina, citaciones_jurisprudencia, texto, 
                   distancia_doctrinal, interpretacion_doctrinal
            FROM rag_sentencias_chunks
            WHERE chunk_id = ?
        """, (chunk_id,))
        
        row = cur.fetchone()
        con.close()
        
        if not row:
            return None
            
        return {
            "chunk_id": row[0],
            "expediente": row[1],
            "fuente_pdf": row[2],
            "fecha_sentencia": row[3],
            "tribunal": row[4],
            "jurisdiccion": row[5],
            "materia": row[6],
            "temas": row[7],
            "formas_razonamiento": row[8],
            "falacias": row[9],
            "citaciones_doctrina": row[10],
            "citaciones_jurisprudencia": row[11],
            "texto_snippet": row[12][:2000] if row[12] else "",
            "distancia_doctrinal": row[13],
            "interpretacion_existente": row[14]
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo chunk {chunk_id}: {e}")
        return None

def guardar_interpretacion(chunk_id: str, interpretacion_data: dict) -> bool:
    """Guarda la interpretación en la base de datos"""
    try:
        con = sqlite3.connect(PENSAMIENTO_DB)
        cur = con.cursor()
        
        # Serializar datos de interpretación
        interpretacion_json = {
            "interpretacion": interpretacion_data.get("interpretacion", ""),
            "estado": interpretacion_data.get("estado", ""),
            "timestamp": interpretacion_data.get("timestamp", ""),
            "distancia_analizada": interpretacion_data.get("distancia_analizada", 0),
            "tokens_utilizados": interpretacion_data.get("tokens_utilizados", 0)
        }
        
        import json
        interpretacion_str = json.dumps(interpretacion_json, ensure_ascii=False)
        
        cur.execute(
            "UPDATE rag_sentencias_chunks SET interpretacion_doctrinal=? WHERE chunk_id=?",
            (interpretacion_str, chunk_id)
        )
        
        con.commit()
        con.close()
        return True
        
    except Exception as e:
        print(f"❌ Error guardando interpretación para {chunk_id}: {e}")
        return False

@app.route("/", methods=["GET"])
def home():
    """Página de inicio de la API"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API GEMINI Interpretación Doctrinal V7.6</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { padding: 15px; border-radius: 5px; margin: 10px 0; }
            .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .warning { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
            .endpoint { background: #e9ecef; padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: #f8f9fa; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 API GEMINI Interpretación Doctrinal V7.6</h1>
            <p>Servicio de interpretación hermenéutica para análisis de distancia doctrinal en sentencias judiciales.</p>
            
            <div class="status {{ status_class }}">
                <strong>Estado:</strong> {{ status_message }}
            </div>
            
            <h2>📋 Endpoints Disponibles</h2>
            
            <div class="endpoint">
                <h3>POST /interpretar-distancia</h3>
                <p>Interpreta un chunk específico de sentencia</p>
                <p><strong>Body:</strong> <code>{"chunk_id": "expediente_001_chunk_001"}</code></p>
            </div>
            
            <div class="endpoint">
                <h3>GET /estado-api</h3>
                <p>Verifica el estado del servicio y configuración</p>
            </div>
            
            <div class="endpoint">
                <h3>POST /interpretar-lote</h3>
                <p>Interpreta múltiples chunks en lote</p>
                <p><strong>Body:</strong> <code>{"chunk_ids": ["id1", "id2", "id3"]}</code></p>
            </div>
            
            <h2>🔧 Configuración</h2>
            <p>Asegúrate de configurar la variable de entorno <code>GEMINI_API_KEY</code> con tu clave de API de Google Gemini.</p>
            
            <p><em>Sistema Cognitivo v7.6 - {{ timestamp }}</em></p>
        </div>
    </body>
    </html>
    """
    
    # Verificar estado
    api_ok = verificar_api_key()
    db_ok = Path(PENSAMIENTO_DB).exists()
    
    if api_ok and db_ok:
        status_class = "success"
        status_message = "✅ Servicio operativo (API Key y BD configuradas)"
    elif not api_ok:
        status_class = "warning"
        status_message = "⚠️ API Key de GEMINI no configurada"
    else:
        status_class = "warning"
        status_message = "⚠️ Base de datos no encontrada"
    
    return render_template_string(html, 
                                  status_class=status_class,
                                  status_message=status_message,
                                  timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route("/estado-api", methods=["GET"])
def estado_api():
    """Endpoint para verificar estado del servicio"""
    
    estado = {
        "servicio": "API GEMINI Interpretación Doctrinal",
        "version": "v7.6",
        "timestamp": datetime.now().isoformat(),
        "gemini_api_configurada": verificar_api_key(),
        "base_datos_disponible": Path(PENSAMIENTO_DB).exists(),
        "base_datos_ruta": PENSAMIENTO_DB
    }
    
    # Verificar tabla y columnas
    if estado["base_datos_disponible"]:
        try:
            con = sqlite3.connect(PENSAMIENTO_DB)
            cur = con.cursor()
            
            # Contar chunks disponibles
            cur.execute("SELECT COUNT(*) FROM rag_sentencias_chunks")
            estado["chunks_disponibles"] = cur.fetchone()[0]
            
            # Verificar columna interpretacion_doctrinal
            cur.execute("PRAGMA table_info(rag_sentencias_chunks)")
            columnas = [col[1] for col in cur.fetchall()]
            estado["columna_interpretacion_existe"] = 'interpretacion_doctrinal' in columnas
            
            # Contar interpretaciones existentes
            if estado["columna_interpretacion_existe"]:
                cur.execute("SELECT COUNT(*) FROM rag_sentencias_chunks WHERE interpretacion_doctrinal IS NOT NULL")
                estado["interpretaciones_existentes"] = cur.fetchone()[0]
            
            con.close()
            
        except Exception as e:
            estado["error_bd"] = str(e)
    
    # Determinar estado general
    if estado["gemini_api_configurada"] and estado["base_datos_disponible"]:
        estado["estado_general"] = "operativo"
    else:
        estado["estado_general"] = "configuracion_pendiente"
    
    return jsonify(estado)

@app.route("/interpretar-distancia", methods=["POST"])
def interpretar_distancia():
    """Endpoint principal para interpretación de distancia doctrinal"""
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON requerido en el body"}), 400
        
        chunk_id = data.get("chunk_id")
        if not chunk_id:
            return jsonify({"error": "chunk_id requerido"}), 400
        
        # Verificar configuración
        if not verificar_api_key():
            return jsonify({
                "error": "API Key de GEMINI no configurada",
                "solucion": "Configura la variable de entorno GEMINI_API_KEY"
            }), 500
        
        # Obtener datos del chunk
        chunk_data = get_chunk_by_id(chunk_id)
        if not chunk_data:
            return jsonify({"error": f"Chunk {chunk_id} no encontrado"}), 404
        
        # Verificar si ya tiene interpretación (opcional: forzar reinterpretación)
        forzar = data.get("forzar_reinterpretacion", False)
        if not forzar and chunk_data.get("interpretacion_existente"):
            try:
                import json
                interpretacion_existente = json.loads(chunk_data["interpretacion_existente"])
                return jsonify({
                    "chunk_id": chunk_id,
                    "interpretacion_doctrinal": interpretacion_existente.get("interpretacion", ""),
                    "estado": "existente",
                    "timestamp_original": interpretacion_existente.get("timestamp", ""),
                    "mensaje": "Interpretación ya existe. Use forzar_reinterpretacion=true para regenerar"
                })
            except:
                pass  # Si hay error parseando, continuar con nueva interpretación
        
        # Interpretar con GEMINI
        print(f"🧠 Interpretando chunk {chunk_id}...")
        resultado = interpretar_sentencia(chunk_data)
        
        # Guardar en BD si fue exitoso
        if resultado.get("estado") == "exitoso":
            if guardar_interpretacion(chunk_id, resultado):
                resultado["guardado_en_bd"] = True
            else:
                resultado["guardado_en_bd"] = False
                resultado["warning"] = "Interpretación generada pero no guardada en BD"
        
        # Preparar respuesta
        response = {
            "chunk_id": chunk_id,
            "interpretacion_doctrinal": resultado.get("interpretacion", ""),
            "estado": resultado.get("estado", ""),
            "timestamp": resultado.get("timestamp", ""),
            "distancia_analizada": resultado.get("distancia_analizada", 0),
            "metadata": {
                "tokens_utilizados": resultado.get("tokens_utilizados", 0),
                "guardado_en_bd": resultado.get("guardado_en_bd", False)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route("/interpretar-lote", methods=["POST"])
def interpretar_lote():
    """Endpoint para interpretación en lote"""
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON requerido"}), 400
        
        chunk_ids = data.get("chunk_ids", [])
        if not chunk_ids or not isinstance(chunk_ids, list):
            return jsonify({"error": "chunk_ids debe ser una lista no vacía"}), 400
        
        if len(chunk_ids) > 20:  # Límite de seguridad
            return jsonify({"error": "Máximo 20 chunks por lote"}), 400
        
        # Verificar configuración
        if not verificar_api_key():
            return jsonify({"error": "API Key de GEMINI no configurada"}), 500
        
        # Obtener datos de chunks
        chunks_data = []
        chunks_no_encontrados = []
        
        for chunk_id in chunk_ids:
            chunk_data = get_chunk_by_id(chunk_id)
            if chunk_data:
                chunks_data.append(chunk_data)
            else:
                chunks_no_encontrados.append(chunk_id)
        
        if not chunks_data:
            return jsonify({"error": "Ningún chunk encontrado"}), 404
        
        # Procesar lote
        resultados = interpretar_lote_sentencias(chunks_data)
        
        # Guardar resultados exitosos
        guardados = 0
        for resultado in resultados:
            if resultado.get("estado") == "exitoso":
                if guardar_interpretacion(resultado["chunk_id"], resultado):
                    guardados += 1
        
        return jsonify({
            "chunks_procesados": len(resultados),
            "chunks_exitosos": len([r for r in resultados if r.get("estado") == "exitoso"]),
            "chunks_guardados": guardados,
            "chunks_no_encontrados": chunks_no_encontrados,
            "resultados": resultados
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Error procesando lote: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

if __name__ == "__main__":
    print("🌐 INICIANDO API GEMINI INTERPRETACIÓN V7.6")
    print("=" * 50)
    
    # Verificar configuración inicial
    if not Path(PENSAMIENTO_DB).exists():
        print(f"⚠️ Base de datos no encontrada: {PENSAMIENTO_DB}")
        print("   La BD se creará automáticamente al ingestar sentencias")
    else:
        ensure_interpretacion_column()
        print(f"✅ Base de datos: {PENSAMIENTO_DB}")
    
    if not verificar_api_key():
        print("⚠️ API Key de GEMINI no configurada")
        print("   Configura: set GEMINI_API_KEY=tu_clave_aqui")
    else:
        print("✅ API Key de GEMINI configurada")
    
    print(f"🚀 Servidor iniciando en http://127.0.0.1:5060")
    print("📋 Endpoints disponibles:")
    print("   - GET  / (página de estado)")
    print("   - GET  /estado-api")
    print("   - POST /interpretar-distancia")
    print("   - POST /interpretar-lote")
    
    app.run(host="127.0.0.1", port=5060, debug=True)