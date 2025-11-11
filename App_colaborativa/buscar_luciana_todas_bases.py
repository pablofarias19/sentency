import sys
import sqlite3
from pathlib import Path

# Buscar en todas las bases de datos
bases = [
    "colaborative/data/pensamiento_integrado_v2.db",
    "colaborative/bases_rag/cognitiva/pensamiento_integrado_v2.db",
    "colaborative/bases_rag/cognitiva/perfiles_autorales.db",
    "colaborative/bases_rag/cognitiva/autor_centrico.db"
]

print("\n" + "="*70)
print("🔍 BUSCANDO 'Luciana B. Scotti' EN TODAS LAS BASES")
print("="*70 + "\n")

for db_path in bases:
    if not Path(db_path).exists():
        continue
    
    print(f"📂 {db_path}")
    print("-" * 70)
    
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Listar tablas
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cur.fetchall()]
        
        for table in tables:
            # Obtener columnas de la tabla
            cur.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cur.fetchall()]
            
            # Buscar columnas de autor
            autor_cols = [col for col in columns if 'autor' in col.lower()]
            
            if autor_cols:
                for col in autor_cols:
                    try:
                        cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} LIKE ?", ('%Luciana%',))
                        count = cur.fetchone()[0]
                        if count > 0:
                            print(f"  ✅ Tabla '{table}', columna '{col}': {count} registros")
                            
                            # Obtener el nombre exacto
                            cur.execute(f"SELECT DISTINCT {col} FROM {table} WHERE {col} LIKE ?", ('%Luciana%',))
                            nombres = cur.fetchall()
                            for nombre in nombres:
                                print(f"     → '{nombre[0]}'")
                    except:
                        pass
        
        conn.close()
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
    
    print()

print("="*70)
print("FIN DE LA BÚSQUEDA")
print("="*70 + "\n")
