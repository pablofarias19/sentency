#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inspeccionar estructura de metadatos.db
"""

import sqlite3

conn = sqlite3.connect('colaborative/bases_rag/cognitiva/metadatos.db')
c = conn.cursor()

print("📊 ESTRUCTURA DE perfiles_cognitivos")
print("="*60)

c.execute("PRAGMA table_info(perfiles_cognitivos)")
columnas = c.fetchall()

print("\nColumnas disponibles:")
for col in columnas:
    print(f"  {col[1]:30s} {col[2]}")

print("\n📋 MUESTRA DE DATOS (primer registro):")
c.execute("SELECT * FROM perfiles_cognitivos LIMIT 1")
registro = c.fetchone()

if registro:
    for i, col in enumerate(columnas):
        valor = registro[i]
        if isinstance(valor, str) and len(str(valor)) > 100:
            valor = str(valor)[:100] + "..."
        print(f"  {col[1]:30s} = {valor}")

conn.close()
