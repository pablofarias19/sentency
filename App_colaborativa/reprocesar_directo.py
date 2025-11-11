# -*- coding: utf-8 -*-
"""
REPROCESADOR DIRECTO - Sin prints con emojis
"""

import sys
import sqlite3
from pathlib import Path
import json
import re
from collections import Counter

sys.path.insert(0, 'colaborative/scripts')
from analizador_enriquecido_rag import AnalizadorEnriquecidoRAG

print("\n" + "="*70)
print("EXTRACCION DIRECTA DE AUTORES CITADOS")
print("="*70 + "\n")

# Conectar a metadatos.db
db_path = r"C:\Users\USUARIO\Programacion\modelos\App_colaborativa\colaborative\bases_rag\cognitiva\metadatos.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verificar/agregar columna
cursor.execute("PRAGMA table_info(perfiles_cognitivos)")
columnas = [col[1] for col in cursor.fetchall()]

if 'autores_citados_json' not in columnas:
    print("Agregando columna autores_citados_json...")
    cursor.execute("ALTER TABLE perfiles_cognitivos ADD COLUMN autores_citados_json TEXT")
    conn.commit()

# Obtener todos los autores
cursor.execute("SELECT autor, fuente FROM perfiles_cognitivos WHERE fuente IS NOT NULL")
autores_pdfs = cursor.fetchall()
print(f"Encontrados {len(autores_pdfs)} autores\n")

analizador = AnalizadorEnriquecidoRAG()

for i, (autor, ruta_pdf) in enumerate(autores_pdfs, 1):
    print(f"[{i}/{len(autores_pdfs)}] {autor}")
    
    pdf_path = Path(ruta_pdf)
    if not pdf_path.exists():
        print("   PDF no encontrado")
        continue
    
    try:
        # Extraer texto DIRECTAMENTE sin prints
        import fitz
        doc = fitz.open(str(pdf_path))
        texto = ""
        for page in doc:
            texto += page.get_text()
        doc.close()
        
        # Usar SOLO el método de extracción sin análisis completo
        autores_citados = analizador.extraer_autores_citados(texto)
        
        if autores_citados:
            print(f"   {len(autores_citados)} autores:")
            for j, (autor_c, freq) in enumerate(list(autores_citados.items())[:3], 1):
                print(f"      {j}. {autor_c} ({freq})")
            
            # Guardar
            autores_json = json.dumps(autores_citados, ensure_ascii=False)
            cursor.execute(
                "UPDATE perfiles_cognitivos SET autores_citados_json = ? WHERE autor = ?",
                (autores_json, autor)
            )
            conn.commit()
        else:
            print("   Sin autores citados")
            
    except Exception as e:
        print(f"   Error: {e}")

conn.close()
print("\n" + "="*70)
print("COMPLETADO")
print("="*70)
