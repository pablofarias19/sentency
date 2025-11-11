#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inspeccionar estructura de autor_centrico.db
"""

import sqlite3

conn = sqlite3.connect('colaborative/bases_rag/cognitiva/autor_centrico.db')
c = conn.cursor()

print("📊 ESTRUCTURA DE perfiles_autorales_expandidos")
print("="*60)

c.execute("PRAGMA table_info(perfiles_autorales_expandidos)")
columnas = c.fetchall()

print("\nColumnas disponibles:")
for col in columnas:
    print(f"  {col[1]:35s} {col[2]}")

conn.close()
