#!/usr/bin/env python3
"""
Limpiador de Base de Datos Cognitiva
Reinicia la tabla para permitir procesamiento completo con v3.1
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "colaborative" / "bases_rag" / "cognitiva" / "metadatos.db"

def limpiar_base_datos():
    print("🧹 LIMPIADOR DE BASE DE DATOS COGNITIVA")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🗃️ Base de datos: {DB_PATH}")
    print()
    
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        cursor = conn.cursor()
        
        # Contar registros actuales
        cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
        total_antes = cursor.fetchone()[0]
        print(f"📊 Registros existentes: {total_antes}")
        
        # Crear backup de tabla si tiene datos
        if total_antes > 0:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS perfiles_cognitivos_backup AS 
                SELECT * FROM perfiles_cognitivos
            """)
            print(f"💾 Backup creado: perfiles_cognitivos_backup")
        
        # Eliminar tabla actual
        cursor.execute("DROP TABLE IF EXISTS perfiles_cognitivos")
        print("🗑️ Tabla eliminada")
        
        # Recrear tabla con estructura optimizada (sin restricciones UNIQUE problemáticas)
        cursor.execute("""
            CREATE TABLE perfiles_cognitivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT,
                fuente TEXT,
                tipo_pensamiento TEXT,
                formalismo REAL,
                creatividad REAL,
                dogmatismo REAL,
                empirismo REAL,
                interdisciplinariedad REAL,
                nivel_abstraccion REAL,
                complejidad_sintactica REAL,
                uso_jurisprudencia REAL,
                tono TEXT,
                fecha_analisis DATETIME,
                vector_path TEXT,
                texto_muestra TEXT,
                autor_confianza REAL,
                autores_citados TEXT,
                razonamiento_top3 TEXT,
                razonamiento_dominante TEXT,
                ethos REAL,
                pathos REAL,
                logos REAL,
                nivel_tecnico REAL,
                latinismos INTEGER,
                citas_legales INTEGER,
                referencias_doctrinarias INTEGER,
                total_palabras INTEGER,
                notas_pie_detectadas INTEGER,
                metadatos_json TEXT,
                modalidad_epistemica TEXT,
                estructura_silogistica TEXT,
                silogismo_confianza REAL,
                conectores_logicos TEXT,
                razonamiento_ejemplos TEXT,
                perfil_aristotelico_json TEXT,
                archivo TEXT,
                indice_teleologico TEXT,
                roles_parrafos TEXT,
                fecha_registro TEXT
            )
        """)
        
        # Crear índices para mejor rendimiento
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_archivo ON perfiles_cognitivos(archivo)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_autor ON perfiles_cognitivos(autor)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fecha ON perfiles_cognitivos(fecha_registro)")
        
        conn.commit()
        conn.close()
        
        print("✅ Tabla recreada con estructura optimizada")
        print("📊 Registros actuales: 0")
        print("🔧 Base de datos lista para ingesta v3.1")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    limpiar_base_datos()
    print("\n🎯 Ahora puedes ejecutar: python ingesta_cognitiva.py")
    print("=" * 50)