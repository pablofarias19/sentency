#!/usr/bin/env python3
"""
REPARADOR DE RASGOS COGNITIVOS
===============================
Analiza los PDFs existentes y calcula los rasgos cognitivos faltantes.
Conecta el procesamiento de PDFs con el análisis cognitivo.
"""

import sqlite3
import sys
import os
from pathlib import Path
import PyPDF2

# Agregar ruta de scripts
sys.path.append(str(Path(__file__).parent / "colaborative" / "scripts"))

from vectorizador_cognitivo import extraer_rasgos_cognitivos
from detector_autor_y_metodo import extraer_texto_y_notas

# Rutas
DB_PATH = Path("colaborative/bases_rag/cognitiva/metadatos.db")
PDF_DIRS = [
    Path("colaborative/data/pdfs/civil"),
    Path("colaborative/data/pdfs/general")
]

def extraer_texto_de_pdf(ruta_pdf: str) -> str:
    """Extrae texto completo de un PDF usando PyPDF2"""
    try:
        with open(ruta_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto = ""
            for page in reader.pages:
                texto += page.extract_text() + "\n"
            return texto.strip()
    except Exception as e:
        print(f"❌ Error extrayendo texto de {ruta_pdf}: {e}")
        # Fallback: usar la función del detector
        try:
            data = extraer_texto_y_notas(ruta_pdf)
            return data.get("texto", "")
        except:
            return ""

def encontrar_pdf_por_autor(autor: str, archivo: str) -> str:
    """Encuentra el PDF correspondiente a un autor y archivo"""
    for pdf_dir in PDF_DIRS:
        if not pdf_dir.exists():
            continue
        
        # Buscar archivos PDF
        for pdf_file in pdf_dir.glob("*.pdf"):
            if archivo.lower() in pdf_file.name.lower():
                return str(pdf_file)
    
    # Si no se encuentra, buscar por similitud de autor
    for pdf_dir in PDF_DIRS:
        if not pdf_dir.exists():
            continue
            
        for pdf_file in pdf_dir.glob("*.pdf"):
            # Extraer nombre del archivo sin extensión
            nombre_archivo = pdf_file.stem.lower()
            autor_clean = autor.lower().replace(" ", "").replace(".", "")
            
            if any(parte in nombre_archivo for parte in autor_clean.split() if len(parte) > 3):
                return str(pdf_file)
    
    return None

def reparar_rasgos_cognitivos():
    """Repara los rasgos cognitivos faltantes en la base de datos"""
    print("🔧 REPARADOR DE RASGOS COGNITIVOS")
    print("=" * 50)
    
    # Conectar a la base de datos
    if not DB_PATH.exists():
        print(f"❌ Base de datos no encontrada: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Obtener perfiles con rasgos cognitivos faltantes
    cursor.execute("""
        SELECT id, autor, archivo, texto_muestra 
        FROM perfiles_cognitivos 
        WHERE formalismo IS NULL OR formalismo = 0.0
    """)
    
    perfiles_pendientes = cursor.fetchall()
    print(f"📊 Encontrados {len(perfiles_pendientes)} perfiles con rasgos cognitivos faltantes")
    
    if not perfiles_pendientes:
        print("✅ Todos los perfiles ya tienen rasgos cognitivos calculados")
        conn.close()
        return
    
    actualizaciones_exitosas = 0
    
    for perfil_id, autor, archivo, texto_muestra in perfiles_pendientes:
        print(f"\n🔍 Procesando: {autor} - {archivo}")
        
        # Buscar el PDF correspondiente
        pdf_path = encontrar_pdf_por_autor(autor, archivo)
        
        if not pdf_path:
            print(f"⚠️ No se encontró PDF para {autor} - {archivo}")
            
            # Si hay texto_muestra, usarlo para calcular rasgos
            if texto_muestra and len(texto_muestra.strip()) > 100:
                print("📝 Usando texto_muestra para análisis")
                texto_para_analisis = texto_muestra
            else:
                print("❌ No hay texto suficiente para análisis")
                continue
        else:
            print(f"📄 PDF encontrado: {pdf_path}")
            # Extraer texto del PDF
            texto_para_analisis = extraer_texto_de_pdf(pdf_path)
            
            if not texto_para_analisis or len(texto_para_analisis.strip()) < 100:
                print("❌ No se pudo extraer texto suficiente del PDF")
                continue
        
        # Calcular rasgos cognitivos
        try:
            rasgos = extraer_rasgos_cognitivos(texto_para_analisis)
            print(f"✅ Rasgos calculados:")
            print(f"   📏 Formalismo: {rasgos['formalismo']:.3f}")
            print(f"   🎨 Creatividad: {rasgos['creatividad']:.3f}")
            print(f"   📚 Dogmatismo: {rasgos['dogmatismo']:.3f}")
            print(f"   🔬 Empirismo: {rasgos['empirismo']:.3f}")
            print(f"   🌐 Interdisciplinariedad: {rasgos['interdisciplinariedad']:.3f}")
            
            # Actualizar base de datos
            cursor.execute("""
                UPDATE perfiles_cognitivos 
                SET 
                    formalismo = ?,
                    creatividad = ?,
                    dogmatismo = ?,
                    empirismo = ?,
                    interdisciplinariedad = ?,
                    nivel_abstraccion = ?,
                    complejidad_sintactica = ?,
                    uso_jurisprudencia = ?
                WHERE id = ?
            """, (
                rasgos['formalismo'],
                rasgos['creatividad'], 
                rasgos['dogmatismo'],
                rasgos['empirismo'],
                rasgos['interdisciplinariedad'],
                rasgos['nivel_abstraccion'],
                rasgos['complejidad_sintactica'],
                rasgos['uso_jurisprudencia'],
                perfil_id
            ))
            
            conn.commit()
            actualizaciones_exitosas += 1
            print(f"💾 Perfil actualizado en base de datos")
            
        except Exception as e:
            print(f"❌ Error calculando rasgos para {autor}: {e}")
            continue
    
    conn.close()
    
    print(f"\n🎉 RESUMEN:")
    print(f"   ✅ Perfiles actualizados: {actualizaciones_exitosas}")
    print(f"   📊 Total procesados: {len(perfiles_pendientes)}")
    print(f"   📈 Tasa de éxito: {(actualizaciones_exitosas/len(perfiles_pendientes)*100):.1f}%")

def verificar_pdfs_disponibles():
    """Verifica qué PDFs están disponibles en el sistema"""
    print("\n📁 VERIFICACIÓN DE PDFs DISPONIBLES:")
    print("=" * 40)
    
    total_pdfs = 0
    for pdf_dir in PDF_DIRS:
        if pdf_dir.exists():
            pdfs = list(pdf_dir.glob("*.pdf"))
            print(f"📂 {pdf_dir}: {len(pdfs)} PDFs")
            for pdf in pdfs:
                print(f"   📄 {pdf.name}")
            total_pdfs += len(pdfs)
        else:
            print(f"❌ {pdf_dir}: Directorio no existe")
    
    print(f"\n📊 Total PDFs encontrados: {total_pdfs}")

if __name__ == "__main__":
    print("🚀 INICIANDO REPARACIÓN DE RASGOS COGNITIVOS")
    verificar_pdfs_disponibles()
    reparar_rasgos_cognitivos()
    print("\n✅ Proceso completado")