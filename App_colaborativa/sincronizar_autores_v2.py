#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 SINCRONIZADOR INTELIGENTE - metadatos.db → autor_centrico.db
================================================================

Mapea campos de perfiles_cognitivos a perfiles_autorales_expandidos
respetando la estructura metodológica del sistema autor-céntrico.

FECHA: 11 NOV 2025
"""

import sqlite3
import json
from datetime import datetime

print("🔄 SINCRONIZACIÓN INTELIGENTE DE AUTORES")
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
        razonamiento_dominante, modalidad_epistemica,
        total_palabras, fecha_analisis
    FROM perfiles_cognitivos
    WHERE autor IS NOT NULL AND autor != ''
""")

autores_meta = c_meta.fetchall()
print(f"\n📊 Autores en metadatos.db: {len(autores_meta)}")

# Obtener autores existentes en autor_centrico.db
c_autor.execute("SELECT autor FROM perfiles_autorales_expandidos")
autores_existentes = [a[0] for a in c_autor.fetchall()]
print(f"📊 Autores en autor_centrico.db (antes): {len(autores_existentes)}")

# Insertar o actualizar cada autor
insertados = 0
actualizados = 0

for row in autores_meta:
    (autor, fuente, archivo, 
     formalismo, creatividad, dogmatismo, empirismo,
     interdisciplina, abstraccion, sintaxis, jurisprudencia,
     tono, pensamiento, ethos, pathos, logos,
     razonamiento, modalidad,
     palabras, fecha) = row
    
    # MAPEO INTELIGENTE: Cognitivo → Metodológico
    
    # Metodología principal (basada en razonamiento_dominante)
    metodologia = razonamiento if razonamiento else "Mixto"
    
    # Patrón de razonamiento (del tipo_pensamiento)
    patron = pensamiento if pensamiento else "Analítico-Jurídico"
    
    # Estilo argumentativo (basado en ethos/pathos/logos)
    if logos and logos > 0.7:
        estilo = "Lógico-Racional"
    elif ethos and ethos > 0.5:
        estilo = "Autoritativo"
    elif pathos and pathos > 0.5:
        estilo = "Persuasivo-Emocional"
    else:
        estilo = "Equilibrado"
    
    # Estructura discursiva (basada en tono)
    estructura = tono if tono else "Formal-Académico"
    
    # Marcadores lingüísticos (JSON simple)
    marcadores = json.dumps({
        "formalismo": float(formalismo) if formalismo else 0.5,
        "creatividad": float(creatividad) if creatividad else 0.3,
        "complejidad": float(sintaxis) if sintaxis else 0.5
    })
    
    # Vocabulario especializado (JSON)
    vocabulario = json.dumps({
        "nivel_tecnico": "alto" if formalismo and formalismo > 0.7 else "medio",
        "uso_latinismos": "frecuente" if formalismo and formalismo > 0.8 else "ocasional",
        "jurisprudencia": float(jurisprudencia) if jurisprudencia else 0.0
    })
    
    # Densidad conceptual (abstracción)
    densidad = float(abstraccion) if abstraccion else 0.5
    
    # Complejidad sintáctica
    complejidad = float(sintaxis) if sintaxis else 0.5
    
    # Modalidad epistémica
    modalidad_ep = modalidad if modalidad else "Dialéctico"
    
    # Obras (de archivo/fuente)
    titulo = archivo if archivo else (fuente.split('\\')[-1] if fuente else "Sin título")
    
    # Originalidad (creatividad)
    originalidad = float(creatividad) if creatividad else 0.5
    
    # Coherencia (dogmatismo inverso = mayor dogmatismo = menor coherencia flexible)
    coherencia = 1.0 - float(dogmatismo) if dogmatismo else 0.7
    
    # Impacto (combinación de factores)
    impacto = (float(formalismo) + float(jurisprudencia) + float(ethos)) / 3.0 if all([formalismo, jurisprudencia, ethos]) else 0.5
    
    # Timestamp
    timestamp_now = datetime.now().isoformat()
    
    # Verificar si ya existe
    if autor in autores_existentes:
        # ACTUALIZAR registro existente
        c_autor.execute("""
            UPDATE perfiles_autorales_expandidos
            SET
                metodologia_principal = ?,
                patron_razonamiento_dominante = ?,
                estilo_argumentativo = ?,
                estructura_discursiva = ?,
                marcadores_linguisticos = ?,
                vocabulario_especializado = ?,
                densidad_conceptual = ?,
                complejidad_sintactica = ?,
                uso_ethos = ?,
                uso_pathos = ?,
                uso_logos = ?,
                modalidad_epistemica = ?,
                primera_obra = ?,
                ultima_obra = ?,
                originalidad_score = ?,
                coherencia_interna = ?,
                impacto_metodologico = ?,
                total_documentos = 1,
                fecha_ultima_actualizacion = ?
            WHERE autor = ?
        """, (
            metodologia, patron, estilo, estructura,
            marcadores, vocabulario,
            densidad, complejidad,
            float(ethos) if ethos else 0.0,
            float(pathos) if pathos else 0.0,
            float(logos) if logos else 0.0,
            modalidad_ep,
            titulo, titulo,
            originalidad, coherencia, impacto,
            timestamp_now,
            autor
        ))
        actualizados += 1
        print(f"  ✏️  {autor}")
    else:
        # INSERTAR nuevo registro
        c_autor.execute("""
            INSERT INTO perfiles_autorales_expandidos (
                autor,
                metodologia_principal,
                patron_razonamiento_dominante,
                estilo_argumentativo,
                estructura_discursiva,
                marcadores_linguisticos,
                vocabulario_especializado,
                densidad_conceptual,
                complejidad_sintactica,
                uso_ethos,
                uso_pathos,
                uso_logos,
                modalidad_epistemica,
                primera_obra,
                ultima_obra,
                originalidad_score,
                coherencia_interna,
                impacto_metodologico,
                total_documentos,
                fecha_primer_analisis,
                fecha_ultima_actualizacion
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            autor,
            metodologia, patron, estilo, estructura,
            marcadores, vocabulario,
            densidad, complejidad,
            float(ethos) if ethos else 0.0,
            float(pathos) if pathos else 0.0,
            float(logos) if logos else 0.0,
            modalidad_ep,
            titulo, titulo,
            originalidad, coherencia, impacto,
            1,
            timestamp_now, timestamp_now
        ))
        insertados += 1
        print(f"  ➕ {autor}")

# Commit
conn_autor.commit()

# Verificar resultado final
c_autor.execute("SELECT COUNT(DISTINCT autor) FROM perfiles_autorales_expandidos")
total_final = c_autor.fetchone()[0]

print("\n" + "="*70)
print(f"✅ SINCRONIZACIÓN COMPLETADA")
print(f"   Autores nuevos: {insertados}")
print(f"   Autores actualizados: {actualizados}")
print(f"   Total en autor_centrico.db: {total_final}")

# Listar autores finales
c_autor.execute("SELECT autor, metodologia_principal FROM perfiles_autorales_expandidos ORDER BY autor")
autores_finales = c_autor.fetchall()

print("\n📋 Autores disponibles en /autores:")
for i, (autor, metod) in enumerate(autores_finales, 1):
    print(f"   {i}. {autor:40s} → {metod}")

print("\n🌐 Reinicia el servidor y accede a:")
print("   http://127.0.0.1:5002/autores")

conn_meta.close()
conn_autor.close()
