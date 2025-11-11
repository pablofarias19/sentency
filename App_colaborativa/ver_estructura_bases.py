# -*- coding: utf-8 -*-
import sqlite3

# Verificar estructura de autor_centrico.db
conn = sqlite3.connect('colaborative/data/autor_centrico.db')
cursor = conn.cursor()

cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = [t[0] for t in cursor.fetchall()]

print("Tablas en autor_centrico.db:")
for table in tables:
    print(f"\n  - {table}")
    cursor.execute(f'SELECT * FROM {table} LIMIT 1')
    if cursor.description:
        columnas = [d[0] for d in cursor.description]
        print(f"    Columnas: {', '.join(columnas[:10])}")
        if len(columnas) > 10:
            print(f"    ... y {len(columnas) - 10} mas")
    
    cursor.execute(f'SELECT COUNT(*) FROM {table}')
    count = cursor.fetchone()[0]
    print(f"    Registros: {count}")

# Buscar columnas con rutas PDF
print("\n\nBuscando columnas con PDFs...")
for table in tables:
    cursor.execute(f'PRAGMA table_info({table})')
    columnas = cursor.fetchall()
    pdf_cols = [col[1] for col in columnas if 'pdf' in col[1].lower() or 'ruta' in col[1].lower() or 'fuente' in col[1].lower()]
    if pdf_cols:
        print(f"\n{table}: {pdf_cols}")
        for col in pdf_cols:
            cursor.execute(f'SELECT {col} FROM {table} WHERE {col} IS NOT NULL LIMIT 3')
            valores = cursor.fetchall()
            if valores:
                print(f"  Ejemplos de {col}:")
                for v in valores:
                    print(f"    - {v[0][:80] if v[0] else 'NULL'}")

conn.close()
