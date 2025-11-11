#!/usr/bin/env python3
"""
Script: find_authors_in_dbs.py
Busca autores en todas las bases de datos (.db) del repo y muestra en qué archivo .db y tabla aparecen.
Ejecutar: python colaborative/scripts/find_authors_in_dbs.py
"""
import os
import sqlite3

# Autores a buscar (tomados de la interfaz que reportaste)
autores_buscados = ['CARLOS PANDIELLA MOLINA', 'Citlalli', 'DANIEL ESTEBAN BROLA', 'Noelia Malvina Cofrè']
# Normalizar a mayúsculas para búsqueda insensible a mayúsc/minúsc
autores_norm = [a.upper() for a in autores_buscados]

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print('🔍 Buscando archivos .db bajo:', repo_root)
print('='*70)

matches = []

for root, dirs, files in os.walk(repo_root):
    for file in files:
        if file.endswith('.db'):
            db_path = os.path.join(root, file)
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()

                # Obtener tablas
                c.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tablas = [r[0] for r in c.fetchall()]

                for tabla in tablas:
                    try:
                        # Obtener info de columnas
                        c.execute(f'PRAGMA table_info("{tabla}")')
                        cols = [row[1] for row in c.fetchall()]
                        if not cols:
                            continue

                        # Buscar columnas que puedan contener autores
                        candidate_cols = [col for col in cols if 'autor' in col.lower() or 'author' in col.lower() or 'archivo' in col.lower()]

                        # Si no hay columna clara, también intentar columnas de texto
                        if not candidate_cols:
                            candidate_cols = cols

                        # Probar cada columna candidata para ver si contiene autores buscados
                        for col in candidate_cols:
                            try:
                                # Evitar tablas con muchos tipos binarios — limitar resultados
                                q = f'SELECT DISTINCT {col} FROM "{tabla}" LIMIT 200'
                                c.execute(q)
                                valores = [str(r[0]) for r in c.fetchall() if r[0] is not None]
                                for val in valores:
                                    val_norm = val.upper()
                                    for busc in autores_norm:
                                        if busc in val_norm:
                                            matches.append({'db': db_path, 'tabla': tabla, 'columna': col, 'valor_ejemplo': val})
                            except Exception:
                                # columna no apta para select DISTINCT o produce error, seguir
                                continue
                    except Exception:
                        continue

                conn.close()
            except Exception as e:
                print(f'❌ Error abriendo {db_path}: {e}')

# Reportar resultados
if matches:
    print('\n✅ Coincidencias encontradas:')
    for m in matches:
        print(f"- DB: {m['db']}\n  Tabla: {m['tabla']}\n  Columna: {m['columna']}\n  Ejemplo: {m['valor_ejemplo']}\n")
else:
    print('\n⚠️ No se encontraron coincidencias exactas para los autores buscados (search was case-insensitive and substring-based).')

print('\n🎯 Fin de la búsqueda')
