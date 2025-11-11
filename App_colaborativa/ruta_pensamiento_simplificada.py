#!/usr/bin/env python3
"""
🔗 RUTA FLASK SIMPLIFICADA PARA /PENSAMIENTO
================================================
 
Reemplaza la ruta /pensamiento en Flask para usar los mismos datos
que funciona en http://127.0.0.1:8888/biblioteca_multicapa.html

AUTOR: Sistema de Integración
FECHA: 10 NOV 2025
"""

# Esta es una ruta que debe insertarse en end2end_webapp.py después de @app.route
# Reemplaza la ruta antigua /pensamiento

route_pensamiento_code = '''
@app.route('/pensamiento', methods=['GET'])
def panel_pensamiento_multicapa():
    """
    Panel especializado en análisis multi-capa del pensamiento autoral
    VERSIÓN INTEGRADA: Usa datos de metadatos.db como biblioteca_multicapa.html
    """
    try:
        from integrador_pensamiento_flask import integrador as pensamiento_integrador
        return pensamiento_integrador.generar_html_pensamiento()
    except ImportError:
        return """
        <html><body style='font-family: Arial; padding: 20px;'>
        <h1>❌ Integrador no disponible</h1>
        <p>No se puede importar integrador_pensamiento_flask</p>
        <a href="/" style="background: #007bff; color: white; padding: 10px; text-decoration: none;">🏠 Volver</a>
        </body></html>
        """
    except Exception as e:
        return f"""
        <html><body style='font-family: Arial; padding: 20px;'>
        <h1>❌ Error</h1>
        <p>{str(e)}</p>
        <a href="/" style="background: #007bff; color: white; padding: 10px; text-decoration: none;">🏠 Volver</a>
        </body></html>
        """

@app.route('/api/pensamiento/<autor>', methods=['GET'])
def api_pensamiento_autor(autor):
    """API endpoint para obtener análisis multicapa de un autor"""
    try:
        from integrador_pensamiento_flask import integrador as pensamiento_integrador
        analisis = pensamiento_integrador.obtener_analisis_autor(autor)
        if analisis:
            return jsonify(analisis)
        else:
            return jsonify({"error": "Autor no encontrado"}), 404
    except:
        return jsonify({"error": "Error en servidor"}), 500
'''

print("✅ Código de ruta generado")
print("\nEsta ruta debe reemplazar la antigua en end2end_webapp.py")
print("Simplemente copia el contenido de 'route_pensamiento_code' en tu archivo Flask")
