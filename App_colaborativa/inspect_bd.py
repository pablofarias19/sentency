#!/usr/bin/env python3
import sqlite3

db_path = r'C:\Users\USUARIO\Programacion\modelos\App_colaborativa\colaborative\bases_rag\cognitiva\metadatos.db'

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("📋 DATOS DE AUTORES EN BD")
print("=" * 100)

cursor.execute("SELECT * FROM perfiles_cognitivos")
for row in cursor.fetchall():
    print(f"\n👤 {row['autor']}")
    print(f"   📄 Archivo: {row['archivo']}")
    print(f"   📝 Total palabras: {row['total_palabras']}")
    print(f"   📖 Fuente: {row['fuente']}")
    print(f"   🧠 Tipo pensamiento: {row['tipo_pensamiento']}")
    print(f"   📊 Formalismo: {row['formalismo']}, Creatividad: {row['creatividad']}")

conn.close()
