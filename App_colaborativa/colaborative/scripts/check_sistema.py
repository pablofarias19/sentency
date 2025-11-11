# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('../bases_rag/cognitiva/metadatos.db')
cur = conn.cursor()

# Total de perfiles
cur.execute('SELECT COUNT(*) FROM perfiles_cognitivos')
total = cur.fetchone()[0]
print(f'Total perfiles en BD: {total}')

# Últimos archivos procesados
cur.execute('SELECT autor, archivo, fecha_registro FROM perfiles_cognitivos WHERE archivo IS NOT NULL ORDER BY id DESC LIMIT 5')
rows = cur.fetchall()
print('\nÚltimos archivos procesados:')
for row in rows:
    fecha = row[2] or "sin fecha"
    print(f'  - {row[0]} | {row[1]} | {fecha}')

# Estadísticas de autores
cur.execute('SELECT autor, COUNT(*) as total FROM perfiles_cognitivos GROUP BY autor ORDER BY total DESC LIMIT 10')
rows = cur.fetchall()
print('\nAutores más frecuentes:')
for row in rows:
    print(f'  - {row[0]}: {row[1]} documentos')

conn.close()