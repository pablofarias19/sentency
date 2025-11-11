#!/usr/bin/env python3
import sqlite3
from pathlib import Path

base_dir = Path(__file__).parent / "colaborative" / "bases_rag" / "cognitiva"

print("\n" + "="*80)
print("📊 VERIFICACIÓN DE BASES DE DATOS")
print("="*80 + "\n")

# Verificar metadatos.db
print("📍 METADATOS.DB")
print("-" * 40)
try:
    conn = sqlite3.connect(base_dir / "metadatos.db")
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [row[0] for row in c.fetchall()]
    print(f"Tablas: {len(tablas)}")
    for tabla in tablas:
        c.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = c.fetchone()[0]
        print(f"  - {tabla}: {count} registros")
    
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")

print("\n📍 MULTICAPA_PENSAMIENTO.DB")
print("-" * 40)
try:
    conn = sqlite3.connect(base_dir / "multicapa_pensamiento.db")
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [row[0] for row in c.fetchall()]
    print(f"Tablas: {len(tablas)}")
    for tabla in tablas:
        c.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = c.fetchone()[0]
        print(f"  - {tabla}: {count} registros")
    
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*80)
