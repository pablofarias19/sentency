#!/usr/bin/env python3
"""
🔗 SERVIDOR FLASK SIMPLIFICADO PARA ANÁLISIS MULTICAPA
======================================================

Servidor Flask que sirve las mismas funciones que:
- http://127.0.0.1:8888/biblioteca_multicapa.html (HTML estático)
- Pero con rutas dinámicas en Flask

PUERTOS:
  - 5002: Servidor Flask (rutas dinámicas)
  - 8888: Servidor HTTP simple (HTML estático)

AUTOR: Sistema de Integración
FECHA: 10 NOV 2025
"""

from flask import Flask, jsonify, render_template_string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "colaborative" / "scripts"))

from integrador_pensamiento_flask import integrador

# Crear aplicación Flask
app = Flask(__name__)

# ====================================
# RUTAS PÚBLICAS
# ====================================

@app.route('/')
def index():
    """Página principal con enlaces"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Sistema de Pensamiento Multi-Capa</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h1 { color: #667eea; }
            .enlace { display: inline-block; margin: 10px; padding: 15px 25px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }
            .enlace:hover { background: #764ba2; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 Sistema de Pensamiento Multi-Capa</h1>
            <p>Selecciona un endpoint:</p>
            <div>
                <a href="/pensamiento" class="enlace">📊 Panel de Análisis Multi-Capa</a>
                <a href="/api/autores" class="enlace">👥 Lista de Autores (JSON)</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/pensamiento', methods=['GET'])
def panel_pensamiento():
    """Panel interactivo de análisis multicapa"""
    return integrador.generar_html_pensamiento()

@app.route('/api/autores', methods=['GET'])
def api_autores():
    """API: Lista de autores disponibles"""
    autores = integrador.obtener_autores_disponibles()
    return jsonify({
        "total": len(autores),
        "autores": autores
    })

@app.route('/api/pensamiento/<autor>', methods=['GET'])
def api_autor_analisis(autor):
    """API: Análisis completo de un autor"""
    analisis = integrador.obtener_analisis_autor(autor)
    if analisis:
        return jsonify(analisis)
    else:
        return jsonify({"error": "Autor no encontrado"}), 404

# ====================================
# MANEJO DE ERRORES
# ====================================

@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(500)
def error_servidor(error):
    return jsonify({"error": "Error del servidor"}), 500

# ====================================
# MAIN
# ====================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 SERVIDOR FLASK - ANÁLISIS MULTICAPA")
    print("="*80)
    print("\n✅ Rutas disponibles:")
    print("   🌐 http://127.0.0.1:5002/")
    print("   📊 http://127.0.0.1:5002/pensamiento")
    print("   👥 http://127.0.0.1:5002/api/autores")
    print("   📈 http://127.0.0.1:5002/api/pensamiento/<autor>")
    print("\n" + "="*80 + "\n")
    
    app.run(
        host='127.0.0.1',
        port=5002,
        debug=True,
        use_reloader=False
    )
