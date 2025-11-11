import sys
import sqlite3

sys.path.insert(0, 'colaborative/scripts')
from config_rutas import PENSAMIENTO_DB

conn = sqlite3.connect(PENSAMIENTO_DB)
cur = conn.cursor()

print("\n📋 TABLAS EN LA BASE DE DATOS:")
print("="*70)

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cur.fetchall()]

for table in sorted(tables):
    print(f"  ✓ {table}")

conn.close()
