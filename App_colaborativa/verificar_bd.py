#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de estructura de base de datos
"""

import sqlite3
from pathlib import Path

# Rutas
BASE_PATH = Path(__file__).resolve().parents[0]
DB_PATH = BASE_PATH / "colaborative" / "bases_rag" / "cognitiva" / "metadatos.db"

def verificar_bd():
    """Verifica la estructura de la base de datos."""
    print(f"🔍 Verificando base de datos: {DB_PATH}")
    
    if not DB_PATH.exists():
        print("❌ La base de datos no existe")
        return
    
    try:
        with sqlite3.connect(str(DB_PATH)) as conn:
            cursor = conn.cursor()
            
            # Obtener todas las tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = cursor.fetchall()
            
            print(f"📊 Tablas encontradas: {len(tablas)}")
            for tabla in tablas:
                nombre_tabla = tabla[0]
                print(f"\n📋 Tabla: {nombre_tabla}")
                
                # Obtener estructura de la tabla
                cursor.execute(f"PRAGMA table_info({nombre_tabla})")
                columnas = cursor.fetchall()
                
                print("   Columnas:")
                for col in columnas:
                    print(f"   • {col[1]} ({col[2]})")
                
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla}")
                count = cursor.fetchone()[0]
                print(f"   📄 Registros: {count}")
                
                # Mostrar algunos datos de ejemplo
                if count > 0:
                    cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT 2")
                    registros = cursor.fetchall()
                    print("   📝 Ejemplos:")
                    for i, reg in enumerate(registros, 1):
                        print(f"     [{i}] {reg[:3]}...")  # Primeros 3 campos
                        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_bd()