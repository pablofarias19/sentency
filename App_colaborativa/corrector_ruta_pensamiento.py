#!/usr/bin/env python3
"""
🔧 CORRECTOR DE RUTA /PENSAMIENTO EN FLASK
==========================================

Reemplaza la función panel_pensamiento_multicapa() con una versión simplificada
que use integrador_pensamiento_flask para consistencia de datos.
"""

from pathlib import Path
import re

print("\n" + "="*80)
print("🔧 CORRECTOR DE RUTA /PENSAMIENTO")
print("="*80 + "\n")

# Archivo a modificar
app_file = Path(__file__).parent / "colaborative" / "scripts" / "end2end_webapp.py"

if not app_file.exists():
    print(f"❌ Archivo no encontrado: {app_file}")
    exit(1)

print(f"📝 Leyendo archivo: {app_file.name}")

# Leer contenido
with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Nueva implementación de la ruta
nueva_ruta = '''@app.route('/pensamiento', methods=['GET'])
def panel_pensamiento_multicapa():
    """
    Panel especializado en análisis multi-capa del pensamiento autoral
    VERSIÓN INTEGRADA: Usa datos de metadatos.db
    """
    try:
        from integrador_pensamiento_flask import integrador as pensamiento_integrador
        return pensamiento_integrador.generar_html_pensamiento()
    except ImportError as e:
        return f"""
        <html><body style='font-family: Arial; padding: 20px;'>
        <h1>❌ Integrador no disponible</h1>
        <p>Error: {e}</p>
        <a href="/" style="background: #007bff; color: white; padding: 10px; text-decoration: none;">🏠 Volver</a>
        </body></html>
        """
    except Exception as e:
        return f"""
        <html><body style='font-family: Arial; padding: 20px;'>
        <h1>❌ Error en /pensamiento</h1>
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
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''

# Buscar y reemplazar la ruta antigua
# Patrón: @app.route('/pensamiento' hasta la siguiente @app.route
pattern = r'@app\.route\([\'"]\/pensamiento[\'"],.*?\)[\s\n]*def panel_pensamiento_multicapa\(\):.*?(?=@app\.route|if __name__|$)'

if re.search(pattern, content, re.DOTALL):
    print("✅ Encontrada ruta antigua /pensamiento")
    content_nuevo = re.sub(pattern, nueva_ruta + '\n\n', content, flags=re.DOTALL)
    
    # Verificar que se hizo el cambio
    if content_nuevo != content:
        # Guardar backup
        backup_file = app_file.with_stem(app_file.stem + "_backup")
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Backup guardado: {backup_file.name}")
        
        # Guardar archivo modificado
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(content_nuevo)
        print(f"✅ Archivo actualizado: {app_file.name}")
        
        print("\n" + "="*80)
        print("✅ RUTA /PENSAMIENTO CORREGIDA")
        print("="*80)
        print("\nLa ruta /pensamiento ahora usará:")
        print("  - Datos de: metadatos.db")
        print("  - Integrador: integrador_pensamiento_flask.py")
        print("  - Mismo formato que: http://127.0.0.1:8888/biblioteca_multicapa.html")
        print("\n🌐 Accede a: http://127.0.0.1:5002/pensamiento")
        print("="*80 + "\n")
    else:
        print("⚠️ No se pudo hacer el reemplazo")
else:
    print("⚠️ No se encontró la ruta antigua en el patrón especificado")
    print("   El archivo puede haber sido ya modificado")
