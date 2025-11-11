#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 REPROCESADOR DE AUTORES CITADOS
====================================
Recalcula los autores citados para todos los autores en la base
"""

import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, 'colaborative/scripts')
from analizador_enriquecido_rag import AnalizadorEnriquecidoRAG

print("\n" + "="*70)
print("🔄 REPROCESADOR DE AUTORES CITADOS")
print("="*70 + "\n")

# Conectar a metadatos.db
db_path = r"C:\Users\USUARIO\Programacion\modelos\App_colaborativa\colaborative\bases_rag\cognitiva\metadatos.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Obtener todos los autores con sus PDFs
cursor.execute("""
    SELECT autor, fuente
    FROM perfiles_cognitivos
    WHERE fuente IS NOT NULL AND fuente != ''
""")

autores_pdfs = cursor.fetchall()
print(f"📚 Encontrados {len(autores_pdfs)} autores con PDFs\n")

# Verificar columna autores_citados_json
cursor.execute("PRAGMA table_info(perfiles_cognitivos)")
columnas = [col[1] for col in cursor.fetchall()]

if 'autores_citados_json' not in columnas:
    print("➕ Agregando columna autores_citados_json...")
    cursor.execute("""
        ALTER TABLE perfiles_cognitivos 
        ADD COLUMN autores_citados_json TEXT
    """)
    conn.commit()
    print("   ✅ Columna agregada\n")

# Procesar cada autor
analizador = AnalizadorEnriquecidoRAG()
import json

for i, (autor, ruta_pdf) in enumerate(autores_pdfs, 1):
    print(f"\n[{i}/{len(autores_pdfs)}] 👤 {autor}")
    print(f"📄 PDF: {ruta_pdf}")
    
    # Verificar si el PDF existe
    pdf_path = Path(ruta_pdf)
    if not pdf_path.exists():
        print(f"   ⚠️ PDF no encontrado, buscando en ubicaciones alternativas...")
        # Intentar ubicaciones comunes
        rutas_alternativas = [
            Path(f"colaborative/data/pdfs/general/{pdf_path.name}"),
            Path(f"colaborative/data/pdfs/{pdf_path.name}"),
            Path(pdf_path.name)
        ]
        for ruta_alt in rutas_alternativas:
            if ruta_alt.exists():
                pdf_path = ruta_alt
                print(f"   ✅ Encontrado en: {pdf_path}")
                break
        else:
            print(f"   ❌ PDF no encontrado en ninguna ubicación")
            continue
    
    try:
        # Analizar con el método mejorado
        print("   🔍 Extrayendo autores citados...")
        resultado = analizador.analizar_documento_completo(str(pdf_path))
        
        autores_citados = resultado.get('autores_citados', {})
        
        if autores_citados:
            print(f"   ✅ Encontrados {len(autores_citados)} autores citados:")
            for j, (autor_citado, freq) in enumerate(list(autores_citados.items())[:5], 1):
                print(f"      {j}. {autor_citado}: {freq} menciones")
            if len(autores_citados) > 5:
                print(f"      ... y {len(autores_citados) - 5} más")
            
            # Guardar en base de datos
            autores_json = json.dumps(autores_citados, ensure_ascii=False)
            cursor.execute("""
                UPDATE perfiles_cognitivos
                SET autores_citados_json = ?
                WHERE autor = ?
            """, (autores_json, autor))
            conn.commit()
            print(f"   💾 Guardado en base de datos")
        else:
            print(f"   ⚠️ No se encontraron autores citados")
            
    except Exception as e:
        print(f"   ❌ Error procesando: {e}")
        import traceback
        traceback.print_exc()

conn.close()

print("\n" + "="*70)
print("✅ PROCESAMIENTO COMPLETADO")
print("="*70)
print("\n💡 Ahora regenera los informes para ver los autores citados")
print("   Puedes eliminar el caché en: colaborative/data/cache_informes/")
