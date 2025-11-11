#!/usr/bin/env python3
"""
REGENERADOR COMPLETO DE BASE DE PERFILES
=========================================
Regenera completamente la base de perfiles desde la base cognitiva principal
para tener todos los registros correctos y completos.
"""

import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime

# Rutas de las bases de datos
DB_COGNITIVA = Path("colaborative/bases_rag/cognitiva/metadatos.db")
DB_PERFILES = Path("colaborative/data/perfiles.db")

def regenerar_base_perfiles_completa():
    """Regenera completamente la base de perfiles desde la base cognitiva"""
    print("🔄 REGENERADOR COMPLETO DE BASE DE PERFILES")
    print("=" * 50)
    
    # Verificar que la base cognitiva exista
    if not DB_COGNITIVA.exists():
        print(f"❌ Base cognitiva no encontrada: {DB_COGNITIVA}")
        return False
    
    # 1. Leer todos los datos de la base cognitiva
    print("📊 Leyendo datos completos de la base cognitiva...")
    conn_cog = sqlite3.connect(DB_COGNITIVA)
    cursor_cog = conn_cog.cursor()
    
    cursor_cog.execute("""
        SELECT 
            autor, archivo, fuente, tipo_pensamiento,
            formalismo, creatividad, dogmatismo, empirismo, interdisciplinariedad,
            nivel_abstraccion, complejidad_sintactica, uso_jurisprudencia,
            tono, fecha_analisis, texto_muestra, autor_confianza,
            autores_citados, razonamiento_top3, razonamiento_dominante,
            ethos, pathos, logos, nivel_tecnico, latinismos,
            citas_legales, referencias_doctrinarias, total_palabras,
            notas_pie_detectadas, metadatos_json, modalidad_epistemica,
            estructura_silogistica, silogismo_confianza, conectores_logicos,
            razonamiento_ejemplos, perfil_aristotelico_json
        FROM perfiles_cognitivos
        WHERE autor IS NOT NULL AND archivo IS NOT NULL
    """)
    
    perfiles_cognitivos = cursor_cog.fetchall()
    conn_cog.close()
    
    print(f"✅ Encontrados {len(perfiles_cognitivos)} perfiles cognitivos completos")
    
    if len(perfiles_cognitivos) == 0:
        print("❌ No hay perfiles cognitivos para procesar")
        return False
    
    # 2. Crear nueva base de perfiles desde cero
    print("🗄️ Creando nueva base de perfiles...")
    
    # Eliminar base anterior si existe
    if DB_PERFILES.exists():
        backup_path = DB_PERFILES.with_suffix('.backup.db')
        DB_PERFILES.rename(backup_path)
        print(f"📦 Backup creado: {backup_path}")
    
    # Crear nueva base
    conn_perf = sqlite3.connect(DB_PERFILES)
    cursor_perf = conn_perf.cursor()
    
    # Crear tabla con estructura completa
    cursor_perf.execute("""
    CREATE TABLE IF NOT EXISTS perfiles_cognitivos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_hash TEXT NOT NULL,
        doc_titulo TEXT,
        autor_detectado TEXT,
        nivel TEXT NOT NULL DEFAULT 'documento',
        perfil_json TEXT NOT NULL,
        firma TEXT NOT NULL,
        embedding BLOB,
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        
        -- Campos adicionales de análisis cognitivo
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
        autor_confianza REAL,
        
        -- Campos aristotélicos
        modalidad_epistemica TEXT,
        estructura_silogistica TEXT,
        ethos REAL,
        pathos REAL,
        logos REAL,
        
        -- Metadatos adicionales
        archivo_fuente TEXT,
        total_palabras INTEGER,
        notas_pie_detectadas INTEGER,
        metadatos_completos TEXT
    )
    """)
    
    # Crear tabla de autores si no existe
    cursor_perf.execute("""
    CREATE TABLE IF NOT EXISTS perfiles_autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        documentos_analizados INTEGER DEFAULT 0,
        promedio_formalismo REAL,
        promedio_creatividad REAL,
        promedio_empirismo REAL,
        primera_aparicion DATETIME,
        ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 3. Insertar todos los perfiles
    print("📝 Insertando perfiles regenerados...")
    registros_insertados = 0
    autores_procesados = set()
    
    for perfil in perfiles_cognitivos:
        (autor, archivo, fuente, tipo_pensamiento, formalismo, creatividad, 
         dogmatismo, empirismo, interdisciplinariedad, nivel_abstraccion,
         complejidad_sintactica, uso_jurisprudencia, tono, fecha_analisis,
         texto_muestra, autor_confianza, autores_citados, razonamiento_top3,
         razonamiento_dominante, ethos, pathos, logos, nivel_tecnico,
         latinismos, citas_legales, referencias_doctrinarias, total_palabras,
         notas_pie_detectadas, metadatos_json, modalidad_epistemica,
         estructura_silogistica, silogismo_confianza, conectores_logicos,
         razonamiento_ejemplos, perfil_aristotelico_json) = perfil
        
        # Generar hash del documento
        doc_content = f"{autor}_{archivo}_{fecha_analisis or datetime.now()}"
        doc_hash = hashlib.md5(doc_content.encode()).hexdigest()
        
        # Crear perfil JSON completo
        perfil_json = {
            "autor": autor,
            "archivo": archivo,
            "tipo_pensamiento": tipo_pensamiento,
            "rasgos_cognitivos": {
                "formalismo": formalismo or 0.0,
                "creatividad": creatividad or 0.0,
                "dogmatismo": dogmatismo or 0.0,
                "empirismo": empirismo or 0.0,
                "interdisciplinariedad": interdisciplinariedad or 0.0,
                "nivel_abstraccion": nivel_abstraccion or 0.0,
                "complejidad_sintactica": complejidad_sintactica or 0.0,
                "uso_jurisprudencia": uso_jurisprudencia or 0.0
            },
            "retorica_aristotelica": {
                "ethos": ethos or 0.0,
                "pathos": pathos or 0.0,
                "logos": logos or 0.0
            },
            "modalidad_epistemica": modalidad_epistemica,
            "estructura_silogistica": estructura_silogistica,
            "fecha_analisis": fecha_analisis
        }
        
        # Crear firma textual para embedding
        firma = f"{autor} - {tipo_pensamiento or 'Jurídico'} - Formalismo:{formalismo:.3f} Creatividad:{creatividad:.3f} Empirismo:{empirismo:.3f}"
        
        # Insertar registro completo
        cursor_perf.execute("""
            INSERT INTO perfiles_cognitivos (
                doc_hash, doc_titulo, autor_detectado, nivel, perfil_json, firma,
                tipo_pensamiento, formalismo, creatividad, dogmatismo, empirismo,
                interdisciplinariedad, nivel_abstraccion, complejidad_sintactica,
                uso_jurisprudencia, tono, autor_confianza, modalidad_epistemica,
                estructura_silogistica, ethos, pathos, logos, archivo_fuente,
                total_palabras, notas_pie_detectadas, metadatos_completos
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc_hash, archivo, autor, 'documento', json.dumps(perfil_json, ensure_ascii=False),
            firma, tipo_pensamiento, formalismo, creatividad, dogmatismo, empirismo,
            interdisciplinariedad, nivel_abstraccion, complejidad_sintactica,
            uso_jurisprudencia, tono, autor_confianza, modalidad_epistemica,
            estructura_silogistica, ethos, pathos, logos, fuente,
            total_palabras, notas_pie_detectadas, metadatos_json
        ))
        
        registros_insertados += 1
        autores_procesados.add(autor)
        print(f"   ✅ {autor} - {archivo}")
    
    # 4. Crear tabla de resumen de autores
    print("👥 Creando resumen de autores...")
    for autor in autores_procesados:
        cursor_perf.execute("""
            INSERT OR REPLACE INTO perfiles_autores (
                nombre, documentos_analizados, promedio_formalismo,
                promedio_creatividad, promedio_empirismo, primera_aparicion
            )
            SELECT 
                ?, COUNT(*), AVG(formalismo), AVG(creatividad), AVG(empirismo), MIN(fecha_registro)
            FROM perfiles_cognitivos 
            WHERE autor_detectado = ?
        """, (autor, autor))
    
    conn_perf.commit()
    conn_perf.close()
    
    print(f"\n🎉 REGENERACIÓN COMPLETADA:")
    print(f"   ✅ Registros insertados: {registros_insertados}")
    print(f"   👥 Autores procesados: {len(autores_procesados)}")
    print(f"   📊 Tasa de éxito: 100%")
    
    return True

def verificar_regeneracion():
    """Verifica que la regeneración fue exitosa"""
    print("\n🔍 VERIFICACIÓN DE REGENERACIÓN:")
    print("=" * 40)
    
    if not DB_PERFILES.exists():
        print("❌ Base de perfiles no encontrada")
        return
    
    conn = sqlite3.connect(DB_PERFILES)
    cursor = conn.cursor()
    
    # Estadísticas generales
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
    total_perfiles = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT autor_detectado) FROM perfiles_cognitivos")
    total_autores = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perfiles_autores")
    autores_tabla = cursor.fetchone()[0]
    
    print(f"📊 ESTADÍSTICAS FINALES:")
    print(f"   📄 Total perfiles: {total_perfiles}")
    print(f"   👤 Total autores: {total_autores}")
    print(f"   👥 Autores en tabla resumen: {autores_tabla}")
    
    # Mostrar algunos ejemplos
    cursor.execute("SELECT doc_titulo, autor_detectado, formalismo, creatividad, empirismo FROM perfiles_cognitivos LIMIT 5")
    ejemplos = cursor.fetchall()
    
    print(f"\n📄 EJEMPLOS (primeros 5):")
    for doc, autor, form, creat, emp in ejemplos:
        doc_corto = doc[:40] + "..." if len(doc) > 40 else doc
        print(f"   ✅ {doc_corto}")
        print(f"      👤 {autor}")
        print(f"      📊 F:{form:.3f} C:{creat:.3f} E:{emp:.3f}")
    
    # Verificar integridad
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos WHERE autor_detectado IS NULL OR autor_detectado = ''")
    sin_autor = cursor.fetchone()[0]
    
    if sin_autor == 0:
        print(f"\n✅ INTEGRIDAD PERFECTA: Todos los registros tienen autor identificado")
    else:
        print(f"\n⚠️ {sin_autor} registros sin autor identificado")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 INICIANDO REGENERACIÓN COMPLETA DE BASE DE PERFILES")
    
    if regenerar_base_perfiles_completa():
        verificar_regeneracion()
        print("\n✅ Regeneración completada exitosamente")
        print("💡 Ahora todos los registros están correctos y completos")
        print("🌐 Puedes probar /perfiles y /radar en la interfaz web")
    else:
        print("\n❌ Error en la regeneración")