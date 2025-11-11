#!/usr/bin/env python3
"""Verificar registros con autor SEBAS"""
import sqlite3
import os

db = 'colaborative/bases_rag/cognitiva/metadatos.db'
if not os.path.exists(db):
    print(f"❌ No existe: {db}")
    exit(1)

conn = sqlite3.connect(db)
c = conn.cursor()

print("🔍 BUSCANDO REGISTROS CON 'SEBAS' COMO AUTOR")
print("="*70)

# Primero ver estructura de la tabla
c.execute("PRAGMA table_info(perfiles_cognitivos)")
columnas = c.fetchall()
print("\n📋 Columnas disponibles:")
for col in columnas:
    print(f"  - {col[1]} ({col[2]})")

# Buscar columnas que puedan contener archivo
col_archivo = None
for col in columnas:
    if 'archivo' in col[1].lower() or 'file' in col[1].lower():
        col_archivo = col[1]
        break

if not col_archivo:
    col_archivo = 'id'  # usar id como fallback

print(f"\n🔍 Usando columna: {col_archivo}\n")

# Buscar en perfiles_cognitivos
c.execute(f"""
    SELECT autor, {col_archivo}, COUNT(*) as cnt 
    FROM perfiles_cognitivos 
    WHERE UPPER(autor) LIKE '%SEBAS%' 
    GROUP BY autor, {col_archivo}
""")

results = c.fetchall()

if not results:
    print("✅ No se encontraron registros con 'SEBAS'")
else:
    print(f"📊 Encontrados {len(results)} grupos de registros:\n")
    for r in results:
        print(f"Autor: {r[0]}")
        print(f"Archivo: {r[1]}")
        print(f"Registros: {r[2]}")
        print("-"*50)
        
    # Mostrar snippet para identificar el autor real
    print("\n📄 CONTENIDO PARA IDENTIFICAR AUTOR REAL:\n")
    c.execute("""
        SELECT * FROM perfiles_cognitivos 
        WHERE UPPER(autor) LIKE '%SEBAS%' 
        LIMIT 1
    """)
    ejemplo = c.fetchone()
    if ejemplo:
        print("Ejemplo de registro completo:")
        col_names = [desc[0] for desc in c.description]
        for i, val in enumerate(ejemplo):
            if val and len(str(val)) < 200:
                print(f"{col_names[i]}: {val}")
            elif val:
                print(f"{col_names[i]}: {str(val)[:200]}...")
        print("-"*50)

conn.close()
print("\n🎯 Fin de la verificación")
