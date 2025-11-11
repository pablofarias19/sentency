import sqlite3
from pathlib import Path

# Ruta a la base de datos
db_path = Path("colaborative/bases_rag/cognitiva/metadatos.db")

if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Ver estructura de la tabla
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    print("📊 TABLAS DISPONIBLES:")
    for tabla in tablas:
        print(f"  • {tabla[0]}")
    
    # Ver estructura de cada tabla
    for tabla in tablas:
        tabla_nombre = tabla[0]
        print(f"\n🔍 ESTRUCTURA DE {tabla_nombre}:")
        cursor.execute(f"PRAGMA table_info({tabla_nombre})")
        columnas = cursor.fetchall()
        for col in columnas:
            print(f"  - {col[1]} ({col[2]})")
        
        # Ver algunas filas de ejemplo
        print(f"\n📋 DATOS DE EJEMPLO ({tabla_nombre}):")
        cursor.execute(f"SELECT * FROM {tabla_nombre} LIMIT 3")
        filas = cursor.fetchall()
        for fila in filas:
            print(f"  {fila}")
    
    conn.close()
else:
    print("❌ Base de datos no encontrada")