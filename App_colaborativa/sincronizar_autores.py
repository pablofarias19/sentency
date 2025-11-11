#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 SINCRONIZADOR - metadatos.db → autor_centrico.db
===================================================

Sincroniza todos los autores de metadatos.db hacia autor_centrico.db
para que /autores muestre los 9 perfiles completos.

FECHA: 11 NOV 2025
"""

import sqlite3
import json
from datetime import datetime

print("🔄 SINCRONIZACIÓN DE AUTORES - metadatos.db → autor_centrico.db")
print("="*70)

# Conectar a ambas bases
conn_meta = sqlite3.connect('colaborative/bases_rag/cognitiva/metadatos.db')
conn_autor = sqlite3.connect('colaborative/bases_rag/cognitiva/autor_centrico.db')

c_meta = conn_meta.cursor()
c_autor = conn_autor.cursor()

# Obtener todos los autores de metadatos.db
c_meta.execute("""
    SELECT 
        autor, fuente, archivo,
        formalismo, creatividad, dogmatismo, empirismo,
        interdisciplinariedad, nivel_abstraccion, complejidad_sintactica, uso_jurisprudencia,
        tono, tipo_pensamiento, ethos, pathos, logos,
        razonamiento_dominante,
        total_palabras, fecha_analisis
    FROM perfiles_cognitivos
    WHERE autor IS NOT NULL AND autor != ''
""")

autores_meta = c_meta.fetchall()
print(f"\n📊 Autores en metadatos.db: {len(autores_meta)}")

# Obtener autores existentes en autor_centrico.db
c_autor.execute("SELECT autor FROM perfiles_autorales_expandidos")
autores_existentes = [a[0] for a in c_autor.fetchall()]
print(f"📊 Autores en autor_centrico.db: {len(autores_existentes)}")

# Insertar o actualizar cada autor
insertados = 0
actualizados = 0

for row in autores_meta:
    (autor, fuente, archivo, 
     formalismo, creatividad, dogmatismo, empirismo,
     interdisciplina, abstraccion, sintaxis, jurisprudencia,
     tono, pensamiento, ethos, pathos, logos,
     razonamiento,
     palabras, fecha) = row
    
    # Generar título desde archivo o fuente
    titulo = archivo if archivo else fuente.split('\\')[-1] if fuente else "Sin título"
    
    # Preparar datos para inserción
    timestamp_now = datetime.now().isoformat()
    
    # Verificar si ya existe
    if autor in autores_existentes:
        # Actualizar
        c_autor.execute("""
            UPDATE perfiles_autorales_expandidos
            SET
                archivo_fuente = ?,
                doc_titulo = ?,
                formalismo = ?, creatividad = ?, dogmatismo = ?, empirismo = ?,
                interdisciplinariedad = ?, abstraccion = ?, complejidad_sintactica = ?,
                uso_jurisprudencia = ?, tono = ?, tipo_pensamiento = ?,
                ethos = ?, pathos = ?, logos = ?,
                razonamiento_predominante = ?,
                total_palabras = ?, fecha_procesamiento = ?,
                ultimo_analisis = ?
            WHERE autor = ?
        """, (
            fuente, titulo,
            formalismo, creatividad, dogmatismo, empirismo,
            interdisciplina, abstraccion, sintaxis, jurisprudencia,
            tono, pensamiento, ethos, pathos, logos,
            razonamiento,
            palabras, fecha, timestamp_now,
            autor
        ))
        actualizados += 1
        print(f"  ✏️  {autor} (actualizado)")
    else:
        # Insertar nuevo
        c_autor.execute("""
            INSERT INTO perfiles_autorales_expandidos (
                autor, archivo_fuente, doc_titulo,
                formalismo, creatividad, dogmatismo, empirismo,
                interdisciplinariedad, abstraccion, complejidad_sintactica,
                uso_jurisprudencia, tono, tipo_pensamiento,
                ethos, pathos, logos,
                razonamiento_predominante,
                metodo_principal, razonamiento_secundario, razonamiento_terciario,
                total_palabras, fecha_procesamiento, ultimo_analisis,
                palabras_clave
            ) VALUES (
                ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?,
                'Deductivo', 'Inductivo', 'Analógico',
                ?, ?, ?,
                '[]'
            )
        """, (
            autor, fuente, titulo,
            formalismo, creatividad, dogmatismo, empirismo,
            interdisciplina, abstraccion, sintaxis, jurisprudencia,
            tono, pensamiento, ethos, pathos, logos,
            razonamiento,
            palabras, fecha, timestamp_now
        ))
        insertados += 1
        print(f"  ➕ {autor} (nuevo)")

# Commit y verificar
conn_autor.commit()

# Verificar resultado final
c_autor.execute("SELECT COUNT(DISTINCT autor) FROM perfiles_autorales_expandidos")
total_final = c_autor.fetchone()[0]

print("\n" + "="*70)
print(f"✅ SINCRONIZACIÓN COMPLETADA")
print(f"   Autores nuevos insertados: {insertados}")
print(f"   Autores actualizados: {actualizados}")
print(f"   Total en autor_centrico.db: {total_final}")
print("\n🌐 Ahora http://127.0.0.1:5002/autores mostrará todos los perfiles")

# Listar autores finales
c_autor.execute("SELECT autor FROM perfiles_autorales_expandidos ORDER BY autor")
autores_finales = [a[0] for a in c_autor.fetchall()]
print("\n📋 Autores disponibles en /autores:")
for i, autor in enumerate(autores_finales, 1):
    print(f"   {i}. {autor}")

conn_meta.close()
conn_autor.close()
