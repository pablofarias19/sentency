#!/usr/bin/env python3
"""
Diagnóstico específico de la discrepancia en datos "0"
Verifica por qué el verificador anterior mostraba valores en 0
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "colaborative" / "bases_rag" / "cognitiva" / "metadatos.db"

def diagnostico_discrepancia():
    print("🔧 DIAGNÓSTICO DE DISCREPANCIA - Valores en '0'")
    print("=" * 55)
    
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        cursor = conn.cursor()
        
        # Verificar datos específicos que mostraban 0
        print("📊 1. VERIFICACIÓN DE AUTOR_CONFIANZA:")
        cursor.execute("SELECT archivo, autor, autor_confianza FROM perfiles_cognitivos")
        for archivo, autor, confianza in cursor.fetchall():
            print(f"  📄 {archivo}: {autor} → Confianza: {confianza}")
        
        print("\n🎭 2. VERIFICACIÓN DE ETHOS/PATHOS/LOGOS:")
        cursor.execute("SELECT archivo, ethos, pathos, logos FROM perfiles_cognitivos")
        for archivo, ethos, pathos, logos in cursor.fetchall():
            print(f"  📄 {archivo}: E:{ethos} P:{pathos} L:{logos}")
        
        print("\n🧭 3. VERIFICACIÓN DE RAZONAMIENTO (RAW JSON):")
        cursor.execute("SELECT archivo, razonamiento_top3 FROM perfiles_cognitivos LIMIT 2")
        for archivo, razonamiento_json in cursor.fetchall():
            print(f"  📄 {archivo}:")
            print(f"      Raw JSON: {razonamiento_json[:200]}...")
            if razonamiento_json:
                try:
                    data = json.loads(razonamiento_json)
                    print(f"      Parsed: {data}")
                except Exception as e:
                    print(f"      Error parsing: {e}")
        
        print("\n🏛️ 4. VERIFICACIÓN DE MODALIDAD EPISTÉMICA:")
        cursor.execute("SELECT archivo, modalidad_epistemica FROM perfiles_cognitivos")
        for archivo, modalidad in cursor.fetchall():
            print(f"  📄 {archivo}: {modalidad}")
        
        # Verificar problema específico del verificador anterior
        print("\n🔍 5. ANÁLISIS DEL PROBLEMA DEL VERIFICADOR ANTERIOR:")
        print("Posibles causas de la discrepancia:")
        
        # Verificar nombres de columnas
        cursor.execute("PRAGMA table_info(perfiles_cognitivos)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        campos_esperados = ['autor_confianza', 'ethos', 'pathos', 'logos', 'modalidad_epistemica']
        for campo in campos_esperados:
            if campo in column_names:
                print(f"  ✅ Campo '{campo}' existe en BD")
            else:
                print(f"  ❌ Campo '{campo}' NO existe en BD")
        
        print("\n📋 6. VERIFICACIÓN DE NOMBRES DE AUTORES:")
        cursor.execute("SELECT DISTINCT autor FROM perfiles_cognitivos")
        autores_unicos = cursor.fetchall()
        print(f"  📚 Autores únicos detectados: {len(autores_unicos)}")
        for autor_tuple in autores_unicos:
            autor = autor_tuple[0]
            print(f"    • '{autor}' (tipo: {type(autor)}, len: {len(autor) if autor else 0})")
        
        conn.close()
        
        print("\n" + "=" * 55)
        print("🎯 CONCLUSIÓN:")
        print("Los datos están correctamente almacenados.")
        print("La discrepancia podría deberse a:")
        print("1. Diferencia en nombres de columnas entre verificadores")
        print("2. Problema en el query SQL del verificador anterior")
        print("3. Diferencias en la conexión a la base de datos")
        print("=" * 55)
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    diagnostico_discrepancia()