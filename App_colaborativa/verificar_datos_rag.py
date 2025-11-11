#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificar datos RAG disponibles"""

import sqlite3
import json

conn = sqlite3.connect('colaborative/bases_rag/cognitiva/metadatos.db')
c = conn.cursor()

# Buscar autor
c.execute('SELECT * FROM perfiles_cognitivos WHERE autor LIKE ? LIMIT 1', ('%CARLOS%',))
columns = [desc[0] for desc in c.description]
row = c.fetchone()

if row:
    datos = dict(zip(columns, row))
    print("\n📊 DATOS RAG DISPONIBLES PARA CARLOS PANDIELLA MOLINA:\n")
    print(f"✅ Palabras totales: {datos.get('total_palabras', 0)}")
    autores = datos.get('autores_citados') or 'N/A'
    print(f"✅ Autores citados: {autores[:200] if isinstance(autores, str) else autores}")
    print(f"✅ Referencias doctrinarias: {datos.get('referencias_doctrinarias', 0)}")
    print(f"✅ Citas legales: {datos.get('citas_legales', 0)}")
    print(f"✅ Latinismos: {datos.get('latinismos', 0)}")
    print(f"✅ Notas al pie: {datos.get('notas_pie_detectadas', 0)}")
    print(f"✅ Razonamiento dominante: {datos.get('razonamiento_dominante') or 'N/A'}")
    print(f"✅ Top 3 razonamientos: {datos.get('razonamiento_top3') or 'N/A'}")
    
    # Metadatos JSON
    if datos.get('metadatos_json'):
        meta = json.loads(datos['metadatos_json'])
        print(f"\n📋 METADATOS ADICIONALES:")
        for k, v in list(meta.items())[:10]:
            print(f"  • {k}: {str(v)[:100]}")
    
    # Texto muestra
    texto = datos.get('texto_muestra', '')
    if texto:
        print(f"\n📝 TEXTO MUESTRA ({len(texto)} chars):")
        print(f"  {texto[:500]}...")
else:
    print("❌ Autor no encontrado")

conn.close()
