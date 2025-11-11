#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico: Autores en diferentes bases de datos
"""

import sqlite3
import os

print("🔍 DIAGNÓSTICO DE BASES DE DATOS - AUTORES")
print("="*60)

# Base 1: metadatos.db
metadatos_db = 'colaborative/bases_rag/cognitiva/metadatos.db'
print(f"\n📊 1. metadatos.db")
print(f"   Existe: {os.path.exists(metadatos_db)}")

if os.path.exists(metadatos_db):
    conn1 = sqlite3.connect(metadatos_db)
    c1 = conn1.cursor()
    
    # Listar tablas
    c1.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [t[0] for t in c1.fetchall()]
    print(f"   Tablas: {tablas}")
    
    # Buscar tabla con autores
    for tabla in tablas:
        try:
            c1.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = c1.fetchone()[0]
            print(f"   - {tabla}: {count} registros")
            
            # Intentar obtener autores
            c1.execute(f"PRAGMA table_info({tabla})")
            columnas = [col[1] for col in c1.fetchall()]
            if 'autor' in columnas:
                c1.execute(f"SELECT DISTINCT autor FROM {tabla} WHERE autor IS NOT NULL AND autor != ''")
                autores = [a[0] for a in c1.fetchall()]
                print(f"     → Autores únicos: {len(autores)}")
                for autor in autores:
                    print(f"       • {autor}")
        except Exception as e:
            print(f"   - {tabla}: Error - {e}")
    
    conn1.close()

# Base 2: autor_centrico.db
autor_db = 'colaborative/bases_rag/cognitiva/autor_centrico.db'
print(f"\n📊 2. autor_centrico.db")
print(f"   Existe: {os.path.exists(autor_db)}")

if os.path.exists(autor_db):
    conn2 = sqlite3.connect(autor_db)
    c2 = conn2.cursor()
    
    # Listar tablas
    c2.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [t[0] for t in c2.fetchall()]
    print(f"   Tablas: {tablas}")
    
    # Buscar tabla con autores
    for tabla in tablas:
        try:
            c2.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = c2.fetchone()[0]
            print(f"   - {tabla}: {count} registros")
            
            # Intentar obtener autores
            c2.execute(f"PRAGMA table_info({tabla})")
            columnas = [col[1] for col in c2.fetchall()]
            if 'autor' in columnas:
                c2.execute(f"SELECT DISTINCT autor FROM {tabla} WHERE autor IS NOT NULL AND autor != ''")
                autores = [a[0] for a in c2.fetchall()]
                print(f"     → Autores únicos: {len(autores)}")
                for autor in autores:
                    print(f"       • {autor}")
        except Exception as e:
            print(f"   - {tabla}: Error - {e}")
    
    conn2.close()

print("\n" + "="*60)
print("✅ Diagnóstico completado")
