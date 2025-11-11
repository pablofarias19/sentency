#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
 SCRIPT DE ACTUALIZACIÓN DE BASE DE DATOS - ANALYSER MÉTODO
===========================================================

Función:
    Actualiza la base de datos cognitiva para soportar los nuevos
    campos del módulo ANALYSER MÉTODO:
    - Detección de autores avanzada
    - Clasificación de razonamiento jurídico  
    - Análisis retórico (Ethos/Pathos/Logos)
    - Métricas de complejidad extendidas

Uso:
    python actualizar_db_analyser.py
===========================================================
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

# ----------------------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------------------
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"

# Crear directorio si no existe
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------
# ACTUALIZACIONES DE ESQUEMA
# ----------------------------------------------------------
def actualizar_esquema_analyser():
    """Añade las nuevas columnas para ANALYSER MÉTODO."""
    
    print("🔧 ACTUALIZANDO BASE DE DATOS PARA ANALYSER MÉTODO")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar si la tabla existe
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='perfiles_cognitivos'
    """)
    
    if not cursor.fetchone():
        print("📋 Creando tabla perfiles_cognitivos...")
        crear_tabla_completa(cursor)
    else:
        print("📋 Tabla existe, añadiendo columnas nuevas...")
        añadir_columnas_analyser(cursor)
    
    conn.commit()
    conn.close()
    
    print("✅ Base de datos actualizada exitosamente")
    print("🧠 ANALYSER MÉTODO está listo para usar")

def crear_tabla_completa(cursor):
    """Crea la tabla completa con todos los campos de ANALYSER MÉTODO."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perfiles_cognitivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor TEXT NOT NULL,
            fuente TEXT NOT NULL,
            
            -- Campos originales del sistema cognitivo
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
            
            -- NUEVOS CAMPOS ANALYSER MÉTODO
            autor_confianza REAL DEFAULT 0.0,
            autores_citados TEXT,  -- JSON array
            razonamiento_top3 TEXT,  -- JSON array
            razonamiento_dominante TEXT,
            
            -- Retórica aristotélica
            ethos REAL DEFAULT 0.0,
            pathos REAL DEFAULT 0.0,
            logos REAL DEFAULT 0.0,
            
            -- Métricas técnicas extendidas
            nivel_tecnico REAL DEFAULT 0.0,
            latinismos INTEGER DEFAULT 0,
            citas_legales INTEGER DEFAULT 0,
            referencias_doctrinarias INTEGER DEFAULT 0,
            
            -- CAMPOS ARISTOTÉLICOS AVANZADOS
            modalidad_epistemica TEXT,  -- Apodíctico, Dialéctico, Retórico, Sofístico
            estructura_silogistica TEXT,  -- Barbara, Cesare, Darapti, etc.
            silogismo_confianza REAL DEFAULT 0.0,
            conectores_logicos TEXT,  -- JSON de conectores detectados
            razonamiento_ejemplos TEXT,  -- JSON con ejemplos textuales
            perfil_aristotelico_json TEXT,  -- JSON completo del análisis aristotélico
            
            -- Metadatos del documento
            total_palabras INTEGER DEFAULT 0,
            notas_pie_detectadas INTEGER DEFAULT 0,
            
            -- Sistema
            vector_path TEXT,
            texto_muestra TEXT,
            fecha_analisis TEXT,
            metadatos_json TEXT,  -- JSON completo del análisis extendido
            
            UNIQUE(autor, fuente)
        )
    """)
    print("✅ Tabla perfiles_cognitivos creada con esquema completo ANALYSER")

def añadir_columnas_analyser(cursor):
    """Añade las nuevas columnas a una tabla existente."""
    
    # Lista de columnas nuevas con sus tipos
    nuevas_columnas = [
        ("autor_confianza", "REAL DEFAULT 0.0"),
        ("autores_citados", "TEXT"),
        ("razonamiento_top3", "TEXT"),
        ("razonamiento_dominante", "TEXT"),
        ("ethos", "REAL DEFAULT 0.0"),
        ("pathos", "REAL DEFAULT 0.0"),
        ("logos", "REAL DEFAULT 0.0"),
        ("nivel_tecnico", "REAL DEFAULT 0.0"),
        ("latinismos", "INTEGER DEFAULT 0"),
        ("citas_legales", "INTEGER DEFAULT 0"),
        ("referencias_doctrinarias", "INTEGER DEFAULT 0"),
        ("total_palabras", "INTEGER DEFAULT 0"),
        ("notas_pie_detectadas", "INTEGER DEFAULT 0"),
        ("metadatos_json", "TEXT"),
        # NUEVAS COLUMNAS ARISTOTÉLICAS
        ("modalidad_epistemica", "TEXT"),
        ("estructura_silogistica", "TEXT"),
        ("silogismo_confianza", "REAL DEFAULT 0.0"),
        ("conectores_logicos", "TEXT"),
        ("razonamiento_ejemplos", "TEXT"),
        ("perfil_aristotelico_json", "TEXT")
    ]
    
    # Verificar qué columnas ya existen
    cursor.execute("PRAGMA table_info(perfiles_cognitivos)")
    columnas_existentes = {row[1] for row in cursor.fetchall()}
    
    # Añadir solo las columnas que no existen
    columnas_añadidas = 0
    for nombre, tipo in nuevas_columnas:
        if nombre not in columnas_existentes:
            try:
                cursor.execute(f"ALTER TABLE perfiles_cognitivos ADD COLUMN {nombre} {tipo}")
                print(f"  ✅ Añadida columna: {nombre}")
                columnas_añadidas += 1
            except Exception as e:
                print(f"  ⚠️ Error añadiendo {nombre}: {e}")
    
    if columnas_añadidas == 0:
        print("  ℹ️ Todas las columnas ANALYSER ya existen")
    else:
        print(f"  📊 Total columnas añadidas: {columnas_añadidas}")

# ----------------------------------------------------------
# FUNCIÓN DE VERIFICACIÓN
# ----------------------------------------------------------
def verificar_actualizacion():
    """Verifica que la actualización fue exitosa."""
    
    print("\n🔍 VERIFICANDO ACTUALIZACIÓN...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Obtener información de la tabla
    cursor.execute("PRAGMA table_info(perfiles_cognitivos)")
    columnas = cursor.fetchall()
    
    # Campos esperados del ANALYSER MÉTODO + ARISTOTÉLICO
    campos_analyser = [
        "autor_confianza", "autores_citados", "razonamiento_top3", 
        "razonamiento_dominante", "ethos", "pathos", "logos",
        "nivel_tecnico", "latinismos", "citas_legales", 
        "referencias_doctrinarias", "metadatos_json",
        # Campos aristotélicos
        "modalidad_epistemica", "estructura_silogistica", "silogismo_confianza",
        "conectores_logicos", "razonamiento_ejemplos", "perfil_aristotelico_json"
    ]
    
    columnas_db = [col[1] for col in columnas]
    campos_presentes = [campo for campo in campos_analyser if campo in columnas_db]
    campos_faltantes = [campo for campo in campos_analyser if campo not in columnas_db]
    
    print(f"📊 Total columnas en tabla: {len(columnas_db)}")
    print(f"✅ Campos ANALYSER presentes: {len(campos_presentes)}/{len(campos_analyser)}")
    
    if campos_faltantes:
        print(f"❌ Campos faltantes: {', '.join(campos_faltantes)}")
        return False
    else:
        print("🎯 Todos los campos ANALYSER están presentes")
        return True
    
    conn.close()

# ----------------------------------------------------------
# FUNCIÓN DE MIGRACIÓN DE DATOS
# ----------------------------------------------------------
def migrar_datos_existentes():
    """Migra datos existentes al nuevo formato si es necesario."""
    
    print("\n🔄 VERIFICANDO DATOS EXISTENTES...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Contar registros existentes
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
    total_registros = cursor.fetchone()[0]
    
    if total_registros > 0:
        print(f"📁 Encontrados {total_registros} registros existentes")
        
        # Verificar si hay registros sin los nuevos campos
        cursor.execute("""
            SELECT COUNT(*) FROM perfiles_cognitivos 
            WHERE metadatos_json IS NULL OR metadatos_json = ''
        """)
        sin_metadatos = cursor.fetchone()[0]
        
        if sin_metadatos > 0:
            print(f"⚠️ {sin_metadatos} registros necesitan migración")
            print("💡 Recomendación: Ejecuta la ingesta cognitiva nuevamente para aprovechar ANALYSER MÉTODO")
        else:
            print("✅ Todos los registros tienen metadatos ANALYSER")
    else:
        print("📭 No hay registros existentes - Base lista para nuevos análisis")
    
    conn.close()

# ----------------------------------------------------------
# FUNCIÓN PRINCIPAL
# ----------------------------------------------------------
def main():
    """Ejecuta la actualización completa."""
    
    print("🧠 ACTUALIZADOR DE BASE DE DATOS - ANALYSER MÉTODO")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🗃️ Base de datos: {DB_PATH}")
    print()
    
    try:
        # 1. Actualizar esquema
        actualizar_esquema_analyser()
        
        # 2. Verificar actualización
        if verificar_actualizacion():
            print("\n🎉 ACTUALIZACIÓN EXITOSA")
            
            # 3. Migrar datos existentes
            migrar_datos_existentes()
            
            print("\n" + "=" * 70)
            print("✅ BASE DE DATOS LISTA PARA ANALYSER MÉTODO")
            print("=" * 70)
            print()
            print("🚀 PRÓXIMOS PASOS:")
            print("1. Ejecuta: python colaborative/scripts/ingesta_cognitiva.py")
            print("2. Los nuevos análisis usarán automáticamente ANALYSER MÉTODO")
            print("3. Ve a http://127.0.0.1:5002/radar para ver visualizaciones")
            print()
        else:
            print("\n❌ ACTUALIZACIÓN FALLIDA")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR DURANTE ACTUALIZACIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

# ----------------------------------------------------------
# EJECUCIÓN
# ----------------------------------------------------------
if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)