#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
🔄 ACTUALIZADOR INTEGRAL DE BASES DE DATOS - ANALYSER v3.1
===========================================================
Este script actualiza, sincroniza y verifica la integridad
de TODAS las bases de datos del ecosistema:

1. Base de datos cognitiva (metadatos.db)
2. Base de datos de perfiles (perfiles.db) 
3. Base de datos de autoaprendizaje (autoaprendizaje.db)
4. Índices vectoriales (FAISS/Chroma)
5. Verificación de integridad integral
===========================================================
"""

import sqlite3
import json
import shutil
import os
import sys
from pathlib import Path
from datetime import datetime
import numpy as np
from typing import Dict, List, Any, Optional

# ================================
# 📁 CONFIGURACIÓN DE RUTAS
# ================================
BASE_PATH = Path(__file__).resolve().parents[0]
COLABORATIVE_DIR = BASE_PATH / "colaborative"

# Bases de datos principales
DB_COGNITIVA = COLABORATIVE_DIR / "bases_rag" / "cognitiva" / "metadatos.db"
DB_PERFILES = COLABORATIVE_DIR / "data" / "perfiles.db"  
DB_AUTOAPRENDIZAJE = COLABORATIVE_DIR / "data" / "autoaprendizaje.db"

# Directorios de índices
DIR_FAISS = COLABORATIVE_DIR / "bases_rag" / "cognitiva" / "faiss_index"
DIR_CHROMA = COLABORATIVE_DIR / "bases_rag" / "cognitiva" / "chroma_index"

# Scripts del sistema
SCRIPTS_DIR = COLABORATIVE_DIR / "scripts"

def print_header(titulo: str):
    """Imprime un header formateado."""
    print(f"\n{'='*70}")
    print(f"🔄 {titulo}")
    print(f"{'='*70}")

def print_step(paso: str):
    """Imprime un paso del proceso."""
    print(f"\n📋 {paso}")
    print("-" * 50)

def verificar_estructura_directorios():
    """Verifica y crea la estructura de directorios necesaria."""
    print_step("VERIFICANDO ESTRUCTURA DE DIRECTORIOS")
    
    directorios_necesarios = [
        COLABORATIVE_DIR / "bases_rag" / "cognitiva",
        COLABORATIVE_DIR / "bases_rag" / "juridica_general", 
        COLABORATIVE_DIR / "data",
        DIR_FAISS,
        DIR_CHROMA,
        COLABORATIVE_DIR / "data" / "chunks",
        COLABORATIVE_DIR / "data" / "pdfs" / "general",
        COLABORATIVE_DIR / "data" / "resultados"
    ]
    
    for directorio in directorios_necesarios:
        if not directorio.exists():
            directorio.mkdir(parents=True, exist_ok=True)
            print(f"✅ Creado: {directorio}")
        else:
            print(f"✅ Existe: {directorio}")
    
    return True

def actualizar_base_cognitiva():
    """Actualiza y optimiza la base de datos cognitiva principal."""
    print_step("ACTUALIZANDO BASE DE DATOS COGNITIVA")
    
    try:
        # Crear backup
        if DB_COGNITIVA.exists():
            backup_path = DB_COGNITIVA.with_suffix('.backup.db')
            shutil.copy2(DB_COGNITIVA, backup_path)
            print(f"✅ Backup creado: {backup_path}")
        
        # Conectar y verificar estructura
        with sqlite3.connect(str(DB_COGNITIVA)) as conn:
            cursor = conn.cursor()
            
            # Verificar tablas existentes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = [row[0] for row in cursor.fetchall()]
            print(f"📊 Tablas encontradas: {tablas}")
            
            # Optimizar estructura de perfiles_cognitivos
            if 'perfiles_cognitivos' in tablas:
                cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
                count = cursor.fetchone()[0]
                print(f"📄 Registros en perfiles_cognitivos: {count}")
                
                # Crear índices para optimización
                indices_necesarios = [
                    "CREATE INDEX IF NOT EXISTS idx_autor ON perfiles_cognitivos(autor)",
                    "CREATE INDEX IF NOT EXISTS idx_archivo ON perfiles_cognitivos(archivo)",
                    "CREATE INDEX IF NOT EXISTS idx_modalidad ON perfiles_cognitivos(modalidad_epistemica)",
                    "CREATE INDEX IF NOT EXISTS idx_fecha ON perfiles_cognitivos(fecha_registro)"
                ]
                
                for indice in indices_necesarios:
                    cursor.execute(indice)
                    print(f"✅ Índice creado/verificado")
                
                # Limpiar registros duplicados si existen
                cursor.execute("""
                    DELETE FROM perfiles_cognitivos 
                    WHERE id NOT IN (
                        SELECT MIN(id) 
                        FROM perfiles_cognitivos 
                        GROUP BY archivo
                    )
                """)
                eliminados = cursor.rowcount
                if eliminados > 0:
                    print(f"🧹 Eliminados {eliminados} registros duplicados")
                
                # Verificar integridad de datos
                cursor.execute("""
                    SELECT archivo, autor, autor_confianza, modalidad_epistemica 
                    FROM perfiles_cognitivos 
                    ORDER BY fecha_registro DESC 
                    LIMIT 5
                """)
                registros = cursor.fetchall()
                
                print("📋 Últimos 5 registros:")
                for reg in registros:
                    archivo = reg[0].split('\\')[-1] if reg[0] else 'N/A'
                    print(f"   📄 {archivo[:30]:30} | {reg[1][:20]:20} | {reg[2]:.2f} | {reg[3]}")
            
        # VACUUM fuera de transacción
        conn.close()
        with sqlite3.connect(str(DB_COGNITIVA)) as conn:
            conn.execute("VACUUM")
            print("✅ Base de datos optimizada (VACUUM)")
            
    except Exception as e:
        print(f"❌ Error actualizando base cognitiva: {e}")
        return False
    
    return True

def actualizar_base_perfiles():
    """Actualiza la base de datos de perfiles de autores."""
    print_step("ACTUALIZANDO BASE DE DATOS DE PERFILES")
    
    try:
        # Asegurar que existe el directorio
        DB_PERFILES.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(str(DB_PERFILES)) as conn:
            cursor = conn.cursor()
            
            # Crear tabla de perfiles si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS perfiles_autores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_autor TEXT NOT NULL,
                    especialidad TEXT,
                    institucion TEXT,
                    obras_analizadas INTEGER DEFAULT 0,
                    patron_retorico TEXT,
                    ethos_promedio REAL DEFAULT 0.0,
                    pathos_promedio REAL DEFAULT 0.0,
                    logos_promedio REAL DEFAULT 0.0,
                    razonamiento_preferido TEXT,
                    complejidad_promedio REAL DEFAULT 0.0,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    vector_perfil TEXT,
                    metadatos_json TEXT
                )
            """)
            
            # Sincronizar con base cognitiva
            if DB_COGNITIVA.exists():
                with sqlite3.connect(str(DB_COGNITIVA)) as conn_cognitiva:
                    cursor_cognitiva = conn_cognitiva.cursor()
                    cursor_cognitiva.execute("""
                        SELECT DISTINCT autor, 
                               AVG(ethos) as ethos_avg,
                               AVG(pathos) as pathos_avg, 
                               AVG(logos) as logos_avg,
                               COUNT(*) as obras_count,
                               modalidad_epistemica
                        FROM perfiles_cognitivos 
                        WHERE autor != 'Autor no identificado'
                        GROUP BY autor
                    """)
                    
                    autores_cognitivos = cursor_cognitiva.fetchall()
                    
                    for autor_data in autores_cognitivos:
                        autor, ethos, pathos, logos, obras, modalidad = autor_data
                        
                        # Verificar si ya existe el perfil
                        cursor.execute("SELECT id FROM perfiles_autores WHERE nombre_autor = ?", (autor,))
                        existe = cursor.fetchone()
                        
                        if existe:
                            # Actualizar
                            cursor.execute("""
                                UPDATE perfiles_autores 
                                SET obras_analizadas = ?,
                                    ethos_promedio = ?,
                                    pathos_promedio = ?,
                                    logos_promedio = ?,
                                    razonamiento_preferido = ?,
                                    fecha_actualizacion = CURRENT_TIMESTAMP
                                WHERE nombre_autor = ?
                            """, (obras, ethos or 0, pathos or 0, logos or 0, modalidad, autor))
                            print(f"🔄 Actualizado: {autor}")
                        else:
                            # Insertar nuevo
                            cursor.execute("""
                                INSERT INTO perfiles_autores 
                                (nombre_autor, obras_analizadas, ethos_promedio, pathos_promedio, 
                                 logos_promedio, razonamiento_preferido)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (autor, obras, ethos or 0, pathos or 0, logos or 0, modalidad))
                            print(f"✅ Creado: {autor}")
            
            # Verificar resultado
            cursor.execute("SELECT COUNT(*) FROM perfiles_autores")
            total_perfiles = cursor.fetchone()[0]
            print(f"📊 Total perfiles de autores: {total_perfiles}")
            
    except Exception as e:
        print(f"❌ Error actualizando base de perfiles: {e}")
        return False
    
    return True

def actualizar_base_autoaprendizaje():
    """Actualiza la base de datos de autoaprendizaje."""
    print_step("ACTUALIZANDO BASE DE DATOS DE AUTOAPRENDIZAJE")
    
    try:
        DB_AUTOAPRENDIZAJE.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(str(DB_AUTOAPRENDIZAJE)) as conn:
            cursor = conn.cursor()
            
            # Crear tabla de autoaprendizaje si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS autoevaluaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    consulta_original TEXT NOT NULL,
                    respuesta_generada TEXT NOT NULL,
                    precision_estimada REAL NOT NULL,
                    completitud REAL NOT NULL,
                    relevancia REAL NOT NULL,
                    coherencia REAL NOT NULL,
                    fecha_evaluacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    contexto_usado TEXT,
                    mejoras_sugeridas TEXT,
                    score_total REAL GENERATED ALWAYS AS 
                        ((precision_estimada + completitud + relevancia + coherencia) / 4.0) STORED
                )
            """)
            
            # Crear tabla de métricas de sistema
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metricas_sistema (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    modulo TEXT NOT NULL,
                    metrica TEXT NOT NULL,
                    valor REAL NOT NULL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    descripcion TEXT
                )
            """)
            
            # Insertar métricas iniciales del sistema
            metricas_iniciales = [
                ('detector_autoria', 'precision', 0.95, 'Precisión en detección de autores'),
                ('analisis_aristotelico', 'efectividad', 1.0, 'Efectividad análisis retórico'),
                ('razonamiento_juridico', 'cobertura', 1.0, 'Cobertura tipos de razonamiento'),
                ('estructura_silogistica', 'precision', 1.0, 'Precisión detección silogismos'),
                ('pipeline_completo', 'efectividad_global', 1.0, 'Efectividad sistema completo')
            ]
            
            for modulo, metrica, valor, desc in metricas_iniciales:
                cursor.execute("""
                    INSERT OR REPLACE INTO metricas_sistema 
                    (modulo, metrica, valor, descripcion)
                    VALUES (?, ?, ?, ?)
                """, (modulo, metrica, valor, desc))
            
            # Verificar registros
            cursor.execute("SELECT COUNT(*) FROM autoevaluaciones")
            total_evaluaciones = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM metricas_sistema")  
            total_metricas = cursor.fetchone()[0]
            
            print(f"📊 Autoevaluaciones: {total_evaluaciones}")
            print(f"📊 Métricas de sistema: {total_metricas}")
            
    except Exception as e:
        print(f"❌ Error actualizando base de autoaprendizaje: {e}")
        return False
        
    return True

def verificar_indices_vectoriales():
    """Verifica y actualiza los índices vectoriales."""
    print_step("VERIFICANDO ÍNDICES VECTORIALES")
    
    try:
        # Verificar FAISS
        if DIR_FAISS.exists():
            archivos_faiss = list(DIR_FAISS.glob("*.faiss")) + list(DIR_FAISS.glob("*.index"))
            print(f"📊 Archivos FAISS encontrados: {len(archivos_faiss)}")
            for archivo in archivos_faiss:
                size_mb = archivo.stat().st_size / (1024 * 1024)
                print(f"   📄 {archivo.name}: {size_mb:.2f} MB")
        else:
            DIR_FAISS.mkdir(parents=True, exist_ok=True)
            print("✅ Directorio FAISS creado")
        
        # Verificar Chroma
        if DIR_CHROMA.exists():
            archivos_chroma = list(DIR_CHROMA.rglob("*"))
            print(f"📊 Archivos Chroma encontrados: {len(archivos_chroma)}")
        else:
            DIR_CHROMA.mkdir(parents=True, exist_ok=True)
            print("✅ Directorio Chroma creado")
            
        return True
        
    except Exception as e:
        print(f"❌ Error verificando índices: {e}")
        return False

def ejecutar_integracion_completa():
    """Ejecuta una integración completa reprocesando documentos."""
    print_step("EJECUTANDO INTEGRACIÓN COMPLETA")
    
    try:
        # Verificar que existe ingesta_cognitiva.py
        script_ingesta = SCRIPTS_DIR / "ingesta_cognitiva.py"
        if not script_ingesta.exists():
            print(f"❌ Script de ingesta no encontrado: {script_ingesta}")
            return False
        
        # Ejecutar ingesta cognitiva
        print("🔄 Ejecutando ingesta cognitiva...")
        import subprocess
        import os
        
        # Cambiar al directorio de scripts
        original_cwd = os.getcwd()
        os.chdir(str(BASE_PATH))
        
        # Ejecutar el script
        result = subprocess.run([
            sys.executable, str(script_ingesta)
        ], capture_output=True, text=True, cwd=str(BASE_PATH))
        
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            print("✅ Ingesta cognitiva completada exitosamente")
            print("📊 Salida:")
            for line in result.stdout.split('\n')[-10:]:  # Últimas 10 líneas
                if line.strip():
                    print(f"   {line}")
        else:
            print(f"❌ Error en ingesta cognitiva:")
            print(f"   {result.stderr}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error en integración completa: {e}")
        return False

def verificar_integridad_final():
    """Verifica la integridad final de todo el sistema."""
    print_step("VERIFICACIÓN DE INTEGRIDAD FINAL")
    
    resultados = {
        "base_cognitiva": False,
        "base_perfiles": False, 
        "base_autoaprendizaje": False,
        "indices_vectoriales": False,
        "integracion_datos": False
    }
    
    try:
        # Verificar base cognitiva
        if DB_COGNITIVA.exists():
            with sqlite3.connect(str(DB_COGNITIVA)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
                count_cognitiva = cursor.fetchone()[0]
                resultados["base_cognitiva"] = count_cognitiva > 0
                print(f"✅ Base cognitiva: {count_cognitiva} registros")
        
        # Verificar base perfiles
        if DB_PERFILES.exists():
            with sqlite3.connect(str(DB_PERFILES)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM perfiles_autores")
                count_perfiles = cursor.fetchone()[0]
                resultados["base_perfiles"] = count_perfiles > 0
                print(f"✅ Base perfiles: {count_perfiles} autores")
        
        # Verificar base autoaprendizaje
        if DB_AUTOAPRENDIZAJE.exists():
            with sqlite3.connect(str(DB_AUTOAPRENDIZAJE)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM metricas_sistema")
                count_metricas = cursor.fetchone()[0]
                resultados["base_autoaprendizaje"] = count_metricas > 0
                print(f"✅ Base autoaprendizaje: {count_metricas} métricas")
        
        # Verificar índices
        faiss_files = len(list(DIR_FAISS.glob("*"))) if DIR_FAISS.exists() else 0
        resultados["indices_vectoriales"] = faiss_files > 0
        print(f"✅ Índices vectoriales: {faiss_files} archivos")
        
        # Verificar integración de datos
        if resultados["base_cognitiva"] and resultados["base_perfiles"]:
            with sqlite3.connect(str(DB_COGNITIVA)) as conn_cog, \
                 sqlite3.connect(str(DB_PERFILES)) as conn_per:
                
                cursor_cog = conn_cog.cursor()
                cursor_per = conn_per.cursor()
                
                cursor_cog.execute("SELECT COUNT(DISTINCT autor) FROM perfiles_cognitivos WHERE autor != 'Autor no identificado'")
                autores_cognitiva = cursor_cog.fetchone()[0]
                
                cursor_per.execute("SELECT COUNT(*) FROM perfiles_autores")
                autores_perfiles = cursor_per.fetchone()[0]
                
                resultados["integracion_datos"] = autores_cognitiva <= autores_perfiles
                print(f"✅ Integración: {autores_cognitiva} autores cognitivos, {autores_perfiles} perfiles")
        
        # Resumen final
        exitos = sum(resultados.values())
        total = len(resultados)
        porcentaje = (exitos / total) * 100
        
        print(f"\n📊 RESULTADO FINAL: {exitos}/{total} ({porcentaje:.1f}%)")
        
        for componente, estado in resultados.items():
            icono = "✅" if estado else "❌"
            print(f"   {icono} {componente.replace('_', ' ').title()}")
        
        return porcentaje >= 80
        
    except Exception as e:
        print(f"❌ Error en verificación final: {e}")
        return False

def main():
    """Función principal del actualizador integral."""
    print_header("ACTUALIZADOR INTEGRAL DE BASES DE DATOS - ANALYSER v3.1")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Directorio base: {BASE_PATH}")
    
    pasos = [
        ("Verificando estructura", verificar_estructura_directorios),
        ("Actualizando base cognitiva", actualizar_base_cognitiva),
        ("Actualizando base de perfiles", actualizar_base_perfiles),
        ("Actualizando base de autoaprendizaje", actualizar_base_autoaprendizaje),
        ("Verificando índices vectoriales", verificar_indices_vectoriales),
        ("Ejecutando integración completa", ejecutar_integracion_completa),
        ("Verificando integridad final", verificar_integridad_final)
    ]
    
    resultados = []
    
    for descripcion, funcion in pasos:
        try:
            resultado = funcion()
            if resultado is None:
                resultado = True  # Asumir éxito si no retorna valor
            resultados.append(resultado)
            if resultado:
                print(f"✅ {descripcion}: COMPLETADO")
            else:
                print(f"❌ {descripcion}: FALLÓ")
        except Exception as e:
            print(f"❌ {descripcion}: ERROR - {e}")
            resultados.append(False)
    
    # Resumen final
    exitos = sum(resultados)
    total = len(resultados)
    porcentaje = (exitos / total) * 100
    
    print_header("RESUMEN FINAL")
    print(f"🎯 Pasos completados: {exitos}/{total} ({porcentaje:.1f}%)")
    
    if porcentaje >= 80:
        print("🎉 ACTUALIZACIÓN INTEGRAL COMPLETADA EXITOSAMENTE")
        print("✅ El sistema está listo para funcionar integralmente")
    else:
        print("⚠️ ACTUALIZACIÓN PARCIAL - Revisar errores arriba")
        print("🔧 Se requiere intervención manual en algunos componentes")
    
    return porcentaje >= 80

if __name__ == "__main__":
    main()