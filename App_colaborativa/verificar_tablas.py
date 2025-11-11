#!/usr/bin/env python3
"""
Verificador de tablas en base de datos
"""

import sqlite3
import os

def verificar_tablas():
    db_path = "colaborative/bases_rag/cognitiva/metadatos.db"
    
    if not os.path.exists(db_path):
        print("❌ ERROR: Base de datos no encontrada")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Listar todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📊 TABLAS EN LA BASE DE DATOS:")
        print("-" * 40)
        for table in tables:
            print(f"  📋 {table[0]}")
        
        # Si hay tablas, mostrar estructura de cada una
        for table in tables:
            table_name = table[0]
            print(f"\n🔍 ESTRUCTURA DE '{table_name}':")
            print("-" * 50)
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for col in columns:
                print(f"  • {col[1]} ({col[2]})")
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  📈 Registros: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    verificar_tablas()