#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VERIFICADOR COMPLETO DEL SISTEMA
==================================
Analiza y verifica todo el flujo de datos del sistema RAG Cognitivo
"""

import os
import sqlite3
import json
from pathlib import Path
from datetime import datetime

def print_header(titulo):
    print("\n" + "=" * 70)
    print(f"🔍 {titulo}")
    print("=" * 70)

def verificar_estructura_archivos():
    """Verifica la estructura de archivos del sistema"""
    print_header("ESTRUCTURA DE ARCHIVOS")
    
    rutas_criticas = {
        "📁 PDFs de entrada": "colaborative/data/pdfs/general",
        "📊 Base cognitiva": "colaborative/bases_rag/cognitiva/metadatos.db", 
        "🧠 Base autoaprendizaje": "colaborative/data/autoaprendizaje.db",
        "📈 Índice FAISS": "colaborative/data/index/general/vector_index.faiss",
        "📝 Chunks de texto": "colaborative/data/chunks/general/chunks.txt",
        "🌐 Webapp principal": "colaborative/scripts/end2end_webapp.py",
        "⚙️ Procesador único": "procesar_todo.py"
    }
    
    for nombre, ruta in rutas_criticas.items():
        path = Path(ruta)
        if path.exists():
            if path.is_file():
                tamaño = path.stat().st_size
                print(f"✅ {nombre}: {ruta} ({tamaño:,} bytes)")
            else:
                archivos = len(list(path.glob("*")))
                print(f"✅ {nombre}: {ruta} ({archivos} archivos)")
        else:
            print(f"❌ {nombre}: {ruta} (NO ENCONTRADO)")

def verificar_base_cognitiva():
    """Verifica el contenido de la base de datos cognitiva"""
    print_header("BASE DE DATOS COGNITIVA")
    
    db_path = "colaborative/bases_rag/cognitiva/metadatos.db"
    if not Path(db_path).exists():
        print(f"❌ Base de datos no encontrada: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estructura de tabla
        cursor.execute("PRAGMA table_info(perfiles_cognitivos)")
        columnas = cursor.fetchall()
        print(f"📊 Estructura de tabla perfiles_cognitivos:")
        for col in columnas:
            print(f"   - {col[1]} ({col[2]})")
        
        # Verificar contenido
        cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
        total = cursor.fetchone()[0]
        print(f"\n👤 Total de perfiles cognitivos: {total}")
        
        # Mostrar muestra de datos
        cursor.execute("""
            SELECT autor, archivo, formalismo, creatividad, dogmatismo, 
                   empirismo, interdisciplinariedad, nivel_abstraccion,
                   complejidad_sintactica, uso_jurisprudencia
            FROM perfiles_cognitivos LIMIT 3
        """)
        
        perfiles = cursor.fetchall()
        print(f"\n📋 MUESTRA DE PERFILES COGNITIVOS:")
        for i, perfil in enumerate(perfiles, 1):
            autor, archivo, *rasgos = perfil
            print(f"\n   👤 Perfil {i}:")
            print(f"      Autor: {autor}")
            print(f"      Archivo: {archivo[:50]}...")
            print(f"      Rasgos: Formalismo={rasgos[0]:.2f}, Creatividad={rasgos[1]:.2f}")
            print(f"              Dogmatismo={rasgos[2]:.2f}, Empirismo={rasgos[3]:.2f}")
        
        # Verificar completitud de datos
        cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos WHERE autor IS NULL OR autor = ''")
        sin_autor = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos WHERE formalismo IS NULL")
        sin_rasgos = cursor.fetchone()[0]
        
        print(f"\n🔍 INTEGRIDAD DE DATOS:")
        print(f"   ❌ Perfiles sin autor: {sin_autor}")
        print(f"   ❌ Perfiles sin rasgos: {sin_rasgos}")
        print(f"   ✅ Perfiles completos: {total - max(sin_autor, sin_rasgos)}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando base cognitiva: {e}")

def verificar_autoaprendizaje():
    """Verifica el sistema de autoaprendizaje"""
    print_header("SISTEMA DE AUTOAPRENDIZAJE")
    
    db_path = "colaborative/data/autoaprendizaje.db"
    if not Path(db_path).exists():
        print(f"❌ Base de autoaprendizaje no encontrada: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM autoevaluaciones")
        total = cursor.fetchone()[0]
        print(f"📊 Total autoevaluaciones: {total}")
        
        # Últimas evaluaciones
        cursor.execute("""
            SELECT fecha, modelo, pregunta, puntaje 
            FROM autoevaluaciones 
            ORDER BY id DESC LIMIT 5
        """)
        
        evaluaciones = cursor.fetchall()
        print(f"\n📋 ÚLTIMAS EVALUACIONES:")
        for fecha, modelo, pregunta, puntaje in evaluaciones:
            print(f"   🕒 {fecha} | {modelo} | Score: {puntaje}")
            print(f"      Pregunta: {pregunta[:60]}...")
        
        # Estadísticas por modelo
        cursor.execute("""
            SELECT modelo, COUNT(*), AVG(puntaje)
            FROM autoevaluaciones 
            GROUP BY modelo
        """)
        
        stats = cursor.fetchall()
        print(f"\n📈 ESTADÍSTICAS POR MODELO:")
        for modelo, count, avg_score in stats:
            print(f"   🤖 {modelo}: {count} evaluaciones, promedio {avg_score:.2f}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando autoaprendizaje: {e}")

def verificar_indices_faiss():
    """Verifica los índices vectoriales FAISS"""
    print_header("ÍNDICES VECTORIALES FAISS")
    
    bases = ["general", "civil", "constitucional", "laboral"]
    
    for base in bases:
        index_path = Path(f"colaborative/data/index/{base}")
        if index_path.exists():
            faiss_file = index_path / "vector_index.faiss"
            chunks_file = index_path / "chunks.txt"
            fuentes_file = index_path / "fuentes.txt"
            
            print(f"\n📊 BASE: {base}")
            
            if faiss_file.exists():
                size = faiss_file.stat().st_size
                print(f"   ✅ Índice FAISS: {size:,} bytes")
            else:
                print(f"   ❌ Índice FAISS: No encontrado")
            
            if chunks_file.exists():
                with open(chunks_file, 'r', encoding='utf-8') as f:
                    chunks = len(f.readlines())
                print(f"   ✅ Chunks de texto: {chunks:,} fragmentos")
            else:
                print(f"   ❌ Chunks de texto: No encontrado")
            
            if fuentes_file.exists():
                with open(fuentes_file, 'r', encoding='utf-8') as f:
                    fuentes = len(set(f.readlines()))
                print(f"   ✅ Fuentes únicas: {fuentes} documentos")
            else:
                print(f"   ❌ Fuentes: No encontrado")
        else:
            print(f"\n❌ BASE: {base} - Directorio no encontrado")

def verificar_pdfs_procesados():
    """Verifica los PDFs y su estado de procesamiento"""
    print_header("PDFs Y PROCESAMIENTO")
    
    pdf_dir = Path("colaborative/data/pdfs/general")
    if not pdf_dir.exists():
        print(f"❌ Directorio de PDFs no encontrado: {pdf_dir}")
        return
    
    pdfs = list(pdf_dir.glob("*.pdf"))
    print(f"📄 PDFs encontrados: {len(pdfs)}")
    
    # Verificar cuáles están procesados
    db_path = "colaborative/bases_rag/cognitiva/metadatos.db"
    if Path(db_path).exists():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT archivo FROM perfiles_cognitivos")
        procesados = {row[0] for row in cursor.fetchall()}
        conn.close()
        
        print(f"\n📊 ESTADO DE PROCESAMIENTO:")
        for pdf in pdfs:
            if pdf.name in procesados:
                print(f"   ✅ {pdf.name} - PROCESADO")
            else:
                print(f"   ❌ {pdf.name} - PENDIENTE")
    else:
        print("❌ No se puede verificar estado de procesamiento (BD no encontrada)")

def verificar_webapp():
    """Verifica la estructura de la webapp"""
    print_header("WEBAPP Y RUTAS")
    
    webapp_path = Path("colaborative/scripts/end2end_webapp.py")
    if not webapp_path.exists():
        print(f"❌ Webapp no encontrada: {webapp_path}")
        return
    
    # Leer webapp y extraer rutas
    with open(webapp_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar rutas definidas
    import re
    rutas = re.findall(r'@app\.route\("([^"]+)"', content)
    
    print(f"🌐 Rutas disponibles en la webapp:")
    rutas_unicas = sorted(set(rutas))
    for ruta in rutas_unicas:
        print(f"   🔗 {ruta}")
    
    # Verificar funciones críticas
    funciones_criticas = [
        "generar_documento_contextual_gemini",
        "buscar",
        "panel_autoevaluaciones", 
        "fusion_contextual_directa"
    ]
    
    print(f"\n🔧 FUNCIONES CRÍTICAS:")
    for func in funciones_criticas:
        if f"def {func}" in content:
            print(f"   ✅ {func}")
        else:
            print(f"   ❌ {func}")

def generar_resumen_sistema():
    """Genera un resumen del estado completo del sistema"""
    print_header("RESUMEN DEL SISTEMA")
    
    print(f"📅 Fecha de verificación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Directorio de trabajo: {Path.cwd()}")
    
    # Contar elementos críticos
    elementos = {
        "PDFs": len(list(Path("colaborative/data/pdfs/general").glob("*.pdf"))) if Path("colaborative/data/pdfs/general").exists() else 0,
        "Perfiles cognitivos": 0,
        "Autoevaluaciones": 0,
        "Rutas webapp": 0
    }
    
    # Contar perfiles
    db_cognitiva = "colaborative/bases_rag/cognitiva/metadatos.db"
    if Path(db_cognitiva).exists():
        try:
            conn = sqlite3.connect(db_cognitiva)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
            elementos["Perfiles cognitivos"] = cursor.fetchone()[0]
            conn.close()
        except:
            pass
    
    # Contar autoevaluaciones
    db_auto = "colaborative/data/autoaprendizaje.db"
    if Path(db_auto).exists():
        try:
            conn = sqlite3.connect(db_auto)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM autoevaluaciones")
            elementos["Autoevaluaciones"] = cursor.fetchone()[0]
            conn.close()
        except:
            pass
    
    print(f"\n📊 MÉTRICAS DEL SISTEMA:")
    for elemento, cantidad in elementos.items():
        print(f"   📈 {elemento}: {cantidad:,}")
    
    # Estado general
    print(f"\n🎯 ESTADO GENERAL:")
    if elementos["PDFs"] > 0 and elementos["Perfiles cognitivos"] > 0:
        print(f"   ✅ Sistema operativo con datos procesados")
    elif elementos["PDFs"] > 0:
        print(f"   ⚠️ PDFs disponibles pero no procesados")
    else:
        print(f"   ❌ No hay PDFs para procesar")
    
    if elementos["Autoevaluaciones"] > 0:
        print(f"   ✅ Sistema de mejora continua activo")
    else:
        print(f"   ⚠️ Sistema de mejora continua sin datos")

def main():
    """Función principal de verificación"""
    print("🔍 VERIFICADOR COMPLETO DEL SISTEMA RAG COGNITIVO")
    print("=" * 70)
    print("Analizando integridad y funcionamiento del sistema completo...")
    
    verificar_estructura_archivos()
    verificar_pdfs_procesados()
    verificar_base_cognitiva()
    verificar_autoaprendizaje()
    verificar_indices_faiss()
    verificar_webapp()
    generar_resumen_sistema()
    
    print("\n" + "=" * 70)
    print("🎉 VERIFICACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 SIGUIENTE PASO: Revisar el reporte y corregir elementos marcados con ❌")

if __name__ == "__main__":
    main()