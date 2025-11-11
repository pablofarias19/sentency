#!/usr/bin/env python3
import sqlite3
from pathlib import Path
import PyPDF2

db_path = r'C:\Users\USUARIO\Programacion\modelos\App_colaborativa\colaborative\bases_rag\cognitiva\metadatos.db'
pdf_dir = Path(r'C:\Users\USUARIO\Programacion\modelos\App_colaborativa\colaborative\data\pdfs\general')

def contar_palabras_pdf(archivo_nombre):
    """Cuenta palabras en un PDF buscando en la carpeta general"""
    # Buscar primero en la carpeta general
    ruta_pdf = pdf_dir / archivo_nombre
    
    if not ruta_pdf.exists():
        # Si no existe, buscar el archivo completo en la BD
        return 0
    
    try:
        with open(ruta_pdf, 'rb') as f:
            lector = PyPDF2.PdfReader(f)
            total_palabras = 0
            for pagina in lector.pages:
                texto = pagina.extract_text()
                total_palabras += len(texto.split())
            return total_palabras
    except Exception as e:
        print(f"   ❌ Error leyendo {archivo_nombre}: {e}")
        return 0

print("📊 ACTUALIZANDO CONTEO DE PALABRAS")
print("=" * 80)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Obtener todos los perfiles
cursor.execute("SELECT id, autor, archivo FROM perfiles_cognitivos")
perfiles = cursor.fetchall()

for profile_id, autor, archivo_completo in perfiles:
    # Extraer solo el nombre del archivo si es una ruta completa
    if "\\" in archivo_completo:
        archivo_nombre = archivo_completo.split("\\")[-1]
    else:
        archivo_nombre = archivo_completo
    
    print(f"\n👤 {autor}")
    print(f"   📄 {archivo_nombre}")
    print(f"   🔍 Buscando en: {pdf_dir / archivo_nombre}")
    
    # Contar palabras
    total_pal = contar_palabras_pdf(archivo_nombre)
    print(f"   ✅ Palabras contadas: {total_pal:,}")
    
    # Actualizar BD
    cursor.execute("UPDATE perfiles_cognitivos SET total_palabras = ? WHERE id = ?", (total_pal, profile_id))
    conn.commit()

print("\n" + "=" * 80)
print("✅ Conteo actualizado en BD")

# Verificar
cursor.execute("SELECT autor, total_palabras FROM perfiles_cognitivos ORDER BY autor")
print("\n📋 RESULTADO FINAL:")
total_general = 0
for autor, pal in cursor.fetchall():
    print(f"   👤 {autor:30} | 📝 {pal:,} palabras")
    total_general += pal if pal else 0

print(f"\n   📊 TOTAL GENERAL: {total_general:,} palabras")

conn.close()
