#!/usr/bin/env python3
import sqlite3

db_path = r'C:\Users\USUARIO\Programacion\modelos\App_colaborativa\colaborative\bases_rag\cognitiva\metadatos.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ver qué hay realmente en total_palabras
cursor.execute("""
    SELECT autor, total_palabras, archivo 
    FROM perfiles_cognitivos 
    WHERE total_palabras IS NOT NULL
    ORDER BY autor
""")

print("📊 PALABRAS POR AUTOR")
print("=" * 80)
for autor, total_pal, archivo in cursor.fetchall():
    filename = archivo.split("\\")[-1] if archivo else "N/A"
    print(f"👤 {autor:30} | 📝 {total_pal:6,} palabras | 📄 {filename}")

conn.close()
