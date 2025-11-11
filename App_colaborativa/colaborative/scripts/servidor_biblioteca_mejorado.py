#!/usr/bin/env python3
"""
🧪 SERVIDOR BIBLIOTECA MEJORADA v2.0
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask
from biblioteca_cognitiva_mejorada import BibliotecaCognitivaMejorada
import webbrowser
import threading
import time

app = Flask(__name__)
biblioteca = BibliotecaCognitivaMejorada()

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Biblioteca Cognitiva v2.0</title>
        <style>
            body { 
                font-family: Arial; 
                margin: 0; 
                padding: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container { 
                background: white; 
                padding: 40px; 
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                text-align: center;
            }
            h1 { color: #333; font-size: 2.5em; margin-bottom: 20px; }
            p { color: #666; font-size: 1.1em; margin-bottom: 30px; }
            a { 
                color: white; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                text-decoration: none; 
                font-size: 1.2em; 
                padding: 15px 40px; 
                border-radius: 8px;
                display: inline-block;
                transition: transform 0.3s;
            }
            a:hover { transform: scale(1.05); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 Biblioteca Cognitiva de Autores v2.0</h1>
            <p>Sistema integral de análisis del pensamiento autoral</p>
            <p>✅ 4 Autores | 4 Obras | 233,792 Palabras</p>
            <a href="/biblioteca">📖 Abrir Biblioteca →</a>
        </div>
    </body>
    </html>
    """

@app.route('/biblioteca')
def pagina_biblioteca():
    """Página principal de la biblioteca cognitiva mejorada"""
    return biblioteca.generar_pagina_principal_html()

def abrir_navegador():
    """Abre el navegador después de 2 segundos"""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:5003/biblioteca')

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🧪 BIBLIOTECA COGNITIVA MEJORADA v2.0")
    print("="*80)
    print("\n✅ Iniciando servidor en http://127.0.0.1:5003")
    print("📖 Biblioteca en: http://127.0.0.1:5003/biblioteca")
    print("⏰ Abriendo navegador en 2 segundos...\n")
    
    # Abrir navegador en thread separado
    thread = threading.Thread(target=abrir_navegador, daemon=True)
    thread.start()
    
    # Iniciar Flask
    app.run(host='127.0.0.1', port=5003, debug=False)
