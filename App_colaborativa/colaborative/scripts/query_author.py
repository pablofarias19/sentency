#!/usr/bin/env python3
"""
query_author.py
Consulta rápida en las DB principales para un autor dado y muestra conteo + ejemplos.
"""
import sqlite3, os
from textwrap import shorten

def query_author(author):
    author_normal = author.upper()
    dbs = [
        'colaborative/bases_rag/cognitiva/metadatos.db',
        'colaborative/bases_rag/cognitiva/autor_centrico.db',
        'colaborative/bases_rag/cognitiva/multicapa_pensamiento.db',
        'colaborative/data/perfiles.db'
    ]

    results = []
    for db in dbs:
        if not os.path.exists(db):
            continue
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = [r[0] for r in c.fetchall()]
            for tabla in tablas:
                try:
                    c.execute(f'PRAGMA table_info("{tabla}")')
                    cols = [r[1] for r in c.fetchall()]
                    if not cols:
                        continue
                    possible_author_cols = [col for col in cols if 'autor' in col.lower() or 'author' in col.lower() or 'autor_detectado' in col.lower()]
                    if not possible_author_cols:
                        possible_author_cols = [col for col in cols if 'archivo' in col.lower() or 'file' in col.lower()]
                    for col in possible_author_cols:
                        try:
                            q = f"SELECT COUNT(*) FROM \"{tabla}\" WHERE upper(COALESCE({col},'')) LIKE ?"
                            c.execute(q, (f'%{author_normal}%',))
                            cnt = c.fetchone()[0]
                            if cnt>0:
                                ex_field = None
                                if 'archivo_fuente' in cols:
                                    ex_field = 'archivo_fuente'
                                else:
                                    ex_field = col
                                try:
                                    c.execute(f"SELECT DISTINCT {ex_field} FROM \"{tabla}\" WHERE upper(COALESCE({col},'')) LIKE ? LIMIT 5", (f'%{author_normal}%',))
                                    examples = [r[0] for r in c.fetchall()]
                                except Exception:
                                    examples = []
                                results.append({'db': db, 'tabla': tabla, 'columna_busqueda': col, 'count': cnt, 'ejemplos': examples})
                        except Exception:
                            continue
                except Exception:
                    continue
            conn.close()
        except Exception as e:
            print('Error abriendo', db, e)

    return results

if __name__ == '__main__':
    author = 'Carlos Pandiella Molina'
    print(f"\n🔎 CONSULTA RÁPIDA: {author}\n{'='*70}")
    res = query_author(author)
    if not res:
        print('⚠️ No se encontraron registros para el autor en las DB consultadas.')
    else:
        total = sum(r['count'] for r in res)
        print(f'📊 Coincidencias totales (suma en todas las tablas): {total}\n')
        for r in res:
            print(f"DB: {r['db']}")
            print(f" Tabla: {r['tabla']}")
            print(f" Campo buscado: {r['columna_busqueda']}")
            print(f" Coincidencias en tabla: {r['count']}")
            if r['ejemplos']:
                print(' Ejemplos:')
                for ex in r['ejemplos']:
                    print('   -', shorten(str(ex), 200))
            print('-'*50)
    print('\n🎯 Fin de la consulta')
