#!/usr/bin/env python3
"""
Servidor HTTP simple para la Biblioteca Mejorada
"""
import os
import webbrowser
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suprimir logs
        pass

def start_server():
    """Inicia un servidor HTTP simple"""
    os.chdir(str(Path(__file__).parent))
    
    server_address = ('127.0.0.1', 8888)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    
    print("\n" + "="*80)
    print("🌐 SERVIDOR HTTP SIMPLE")
    print("="*80)
    print(f"\n✅ Servidor corriendo en http://127.0.0.1:8888")
    print(f"📖 Biblioteca en: http://127.0.0.1:8888/biblioteca_mejorada_completa.html")
    print("\n⏰ Abriendo navegador en 2 segundos...")
    print("🛑 Presiona Ctrl+C para detener el servidor\n")
    
    # Abrir navegador en thread
    def abrir():
        time.sleep(2)
        webbrowser.open('http://127.0.0.1:8888/biblioteca_mejorada_completa.html')
    
    thread = threading.Thread(target=abrir, daemon=True)
    thread.start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Servidor detenido")
        httpd.shutdown()

if __name__ == '__main__':
    start_server()
