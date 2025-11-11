# -*- coding: utf-8 -*-
"""
Reprocesar TODOS los autores con perfiles incompletos
"""
import os
import sys
import sqlite3
import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime

# Agregar ruta de scripts
sys.path.insert(0, str(Path(__file__).parent / "colaborative" / "scripts"))

# Importar vectorizador cognitivo
from vectorizador_cognitivo import extraer_rasgos_cognitivos

# Configuración
BASE_PATH = Path(__file__).parent / "colaborative"
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"
PDF_DIR = BASE_PATH / "data" / "pdfs" / "general"

def extraer_texto_pdf(ruta_pdf):
    """Extrae texto completo del PDF"""
    try:
        doc = fitz.open(ruta_pdf)
        texto_completo = ""
        
        for pagina in doc:
            texto_completo += pagina.get_text()
        
        doc.close()
        return texto_completo
    except Exception as e:
        print(f"  ❌ Error extrayendo texto: {e}")
        return ""

def reprocesar_todos_los_autores():
    """Reprocesa todos los autores con campos cognitivos vacíos"""
    
    print(f"\n{'='*70}")
    print("🔄 REPROCESANDO TODOS LOS PERFILES INCOMPLETOS")
    print(f"{'='*70}\n")
    
    # 1. Identificar perfiles incompletos
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, autor, archivo, fuente
        FROM perfiles_cognitivos
        WHERE formalismo IS NULL 
           OR creatividad IS NULL 
           OR total_palabras IS NULL
        ORDER BY autor
    """)
    
    perfiles_incompletos = cur.fetchall()
    total = len(perfiles_incompletos)
    
    if total == 0:
        print("✅ Todos los perfiles están completos. No hay nada que reprocesar.\n")
        conn.close()
        return True
    
    print(f"📋 Encontrados {total} perfiles incompletos:\n")
    for _, autor, archivo, _ in perfiles_incompletos:
        print(f"  • {autor} ({archivo})")
    
    print(f"\n{'─'*70}\n")
    
    # 2. Reprocesar cada perfil
    procesados = 0
    errores = 0
    
    for perfil_id, autor, archivo, fuente in perfiles_incompletos:
        print(f"🔄 [{procesados+1}/{total}] Procesando: {autor}")
        print(f"   📄 Archivo: {archivo}")
        
        # Buscar el PDF
        pdf_path = Path(fuente) if Path(fuente).exists() else PDF_DIR / archivo
        
        if not pdf_path.exists():
            print(f"   ❌ ERROR: No se encuentra el archivo {pdf_path}")
            errores += 1
            print()
            continue
        
        # Extraer texto
        texto = extraer_texto_pdf(str(pdf_path))
        
        if not texto:
            print(f"   ❌ ERROR: No se pudo extraer texto")
            errores += 1
            print()
            continue
        
        total_palabras = len(texto.split())
        print(f"   📊 Extraídas: {total_palabras:,} palabras")
        
        # Calcular rasgos cognitivos
        rasgos = extraer_rasgos_cognitivos(texto)
        
        print(f"   🧠 Rasgos calculados:")
        print(f"      Formalismo: {rasgos['formalismo']:.3f} | Creatividad: {rasgos['creatividad']:.3f}")
        print(f"      Abstracción: {rasgos['nivel_abstraccion']:.3f} | Complejidad: {rasgos['complejidad_sintactica']:.3f}")
        
        # Actualizar base de datos
        try:
            cur.execute("""
                UPDATE perfiles_cognitivos
                SET formalismo = ?,
                    creatividad = ?,
                    dogmatismo = ?,
                    empirismo = ?,
                    interdisciplinariedad = ?,
                    nivel_abstraccion = ?,
                    complejidad_sintactica = ?,
                    uso_jurisprudencia = ?,
                    total_palabras = ?,
                    fecha_analisis = ?
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
                total_palabras,
                datetime.now().isoformat(),
                perfil_id
            ))
            
            conn.commit()
            procesados += 1
            print(f"   ✅ Actualizado correctamente\n")
            
        except Exception as e:
            print(f"   ❌ ERROR actualizando: {e}\n")
            errores += 1
    
    conn.close()
    
    # 3. Resumen final
    print(f"{'='*70}")
    print(f"📊 RESUMEN FINAL:")
    print(f"{'='*70}")
    print(f"  ✅ Procesados exitosamente: {procesados}/{total}")
    print(f"  ❌ Errores:                 {errores}/{total}")
    
    if procesados == total:
        print(f"\n  🎉 ¡TODOS LOS PERFILES COMPLETADOS!")
    elif procesados > 0:
        print(f"\n  ⚠️ Se completaron {procesados} perfiles, pero hubo {errores} errores")
    else:
        print(f"\n  ❌ No se pudo completar ningún perfil")
    
    print(f"{'='*70}\n")
    
    return procesados > 0

if __name__ == "__main__":
    exito = reprocesar_todos_los_autores()
    
    if exito:
        print("💡 Los perfiles actualizados están disponibles en:")
        print("   http://127.0.0.1:5002/autores\n")
    
    sys.exit(0 if exito else 1)
