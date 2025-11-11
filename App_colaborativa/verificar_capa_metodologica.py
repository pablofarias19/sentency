#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar capa metodológica en autor_centrico.db
"""

import sqlite3
import json

db_path = 'colaborative/bases_rag/cognitiva/autor_centrico.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Listar tablas
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = [t[0] for t in c.fetchall()]
print(f"📊 Tablas en autor_centrico.db:")
for t in tablas:
    print(f"   - {t}")

# Buscar tabla con densidad_citas
print("\n🔍 Buscando campos densidad_citas y uso_ejemplos...")
for tabla in tablas:
    c.execute(f"PRAGMA table_info({tabla})")
    columnas = [col[1] for col in c.fetchall()]
    
    if 'densidad_citas' in columnas or 'uso_ejemplos' in columnas:
        print(f"\n✅ Encontrado en tabla: {tabla}")
        print(f"   Columnas: {columnas}")
        
        # Ver datos
        c.execute(f"SELECT autor, densidad_citas, uso_ejemplos FROM {tabla} LIMIT 3")
        datos = c.fetchall()
        print(f"\n   Muestra de datos:")
        for autor, dens, uso in datos:
            print(f"     {autor}: densidad={dens}, uso_ejemplos={uso}")

conn.close()
