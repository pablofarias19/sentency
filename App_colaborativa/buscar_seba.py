#!/usr/bin/env python3
"""Buscar autor 'SEBA' o 'SEBAS' en todas las bases"""
import sqlite3
import os

bases = [
    'colaborative/bases_rag/cognitiva/metadatos.db',
    'colaborative/bases_rag/cognitiva/autor_centrico.db',
    'colaborative/bases_rag/cognitiva/multicapa_pensamiento.db',
    'colaborative/data/perfiles.db'
]

print("🔍 BUSCANDO 'SEBA' O 'SEBAS' EN TODAS LAS BASES")
print("="*70)

encontrados = []

for db_path in bases:
    if not os.path.exists(db_path):
        continue
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Ver tablas
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [r[0] for r in c.fetchall()]
        
        for tabla in tablas:
            # Ver si tiene columna autor
            c.execute(f"PRAGMA table_info({tabla})")
            cols = [r[1] for r in c.fetchall()]
            
            if 'autor' in cols or 'autor_detectado' in cols or 'nombre' in cols:
                col_autor = 'autor' if 'autor' in cols else ('autor_detectado' if 'autor_detectado' in cols else 'nombre')
                
                # Buscar variaciones de seba
                c.execute(f"""
                    SELECT {col_autor}, COUNT(*) 
                    FROM {tabla} 
                    WHERE LOWER({col_autor}) LIKE '%seba%' 
                    GROUP BY {col_autor}
                """)
                results = c.fetchall()
                
                if results:
                    for autor, cnt in results:
                        encontrados.append({
                            'db': db_path,
                            'tabla': tabla,
                            'autor': autor,
                            'registros': cnt
                        })
                        
        conn.close()
    except Exception as e:
        print(f"Error en {db_path}: {e}")

if encontrados:
    print(f"\n✅ Encontrados {len(encontrados)} resultados:\n")
    for e in encontrados:
        print(f"DB: {e['db']}")
        print(f"  Tabla: {e['tabla']}")
        print(f"  Autor: {e['autor']}")
        print(f"  Registros: {e['registros']}")
        print("-"*50)
        
    # Ver de qué archivo viene
    print("\n📄 ARCHIVOS ASOCIADOS:")
    for e in encontrados:
        conn = sqlite3.connect(e['db'])
        c = conn.cursor()
        cols_tabla = [r[1] for r in c.execute(f"PRAGMA table_info({e['tabla']})").fetchall()]
        col_archivo = None
        for col in ['archivo', 'fuente', 'archivo_fuente', 'file']:
            if col in cols_tabla:
                col_archivo = col
                break
        
        if col_archivo:
            col_autor = 'autor' if 'autor' in cols_tabla else ('autor_detectado' if 'autor_detectado' in cols_tabla else 'nombre')
            c.execute(f"SELECT DISTINCT {col_archivo} FROM {e['tabla']} WHERE LOWER({col_autor}) LIKE '%seba%'")
            archivos = c.fetchall()
            print(f"\nAutor '{e['autor']}' viene de:")
            for a in archivos:
                print(f"  📁 {a[0]}")
        conn.close()
else:
    print("\n⚠️ NO se encontró 'SEBA' o 'SEBAS' en ninguna base de datos")
    print("\n💡 Puede que esté en otra tabla o con otro nombre")
    print("Voy a listar TODOS los autores únicos disponibles:\n")
    
    # Listar todos los autores
    for db_path in bases:
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tablas = [r[0] for r in c.fetchall()]
                
                for tabla in tablas:
                    c.execute(f"PRAGMA table_info({tabla})")
                    cols = [r[1] for r in c.fetchall()]
                    
                    if 'autor' in cols:
                        c.execute(f"SELECT DISTINCT autor FROM {tabla} LIMIT 10")
                        autores = [r[0] for r in c.fetchall() if r[0]]
                        if autores:
                            print(f"\n📚 {os.path.basename(db_path)} - {tabla}:")
                            for a in autores:
                                print(f"   - {a}")
                conn.close()
            except:
                pass

print("\n🎯 Fin de la búsqueda")
