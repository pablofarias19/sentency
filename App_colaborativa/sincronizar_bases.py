#!/usr/bin/env python3
"""
SINCRONIZADOR DE BASES DE DATOS
===============================
Sincroniza la base de datos de perfiles con la base cognitiva principal
para corregir el problema de "Autor no identificado"
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Rutas de las bases de datos
DB_COGNITIVA = Path("colaborative/bases_rag/cognitiva/metadatos.db")
DB_PERFILES = Path("colaborative/data/perfiles.db")

def sincronizar_bases_datos():
    """Sincroniza los datos de autores entre las dos bases"""
    print("🔄 SINCRONIZADOR DE BASES DE DATOS")
    print("=" * 40)
    
    # Verificar que ambas bases existan
    if not DB_COGNITIVA.exists():
        print(f"❌ Base cognitiva no encontrada: {DB_COGNITIVA}")
        return False
    
    if not DB_PERFILES.exists():
        print(f"❌ Base de perfiles no encontrada: {DB_PERFILES}")
        return False
    
    # 1. Leer datos correctos de la base cognitiva
    print("📊 Leyendo datos de base cognitiva principal...")
    conn_cog = sqlite3.connect(DB_COGNITIVA)
    cursor_cog = conn_cog.cursor()
    
    cursor_cog.execute("""
        SELECT autor, archivo, formalismo, creatividad, dogmatismo, 
               empirismo, interdisciplinariedad, nivel_abstraccion,
               complejidad_sintactica, uso_jurisprudencia, fecha_registro
        FROM perfiles_cognitivos
        WHERE formalismo IS NOT NULL
    """)
    
    perfiles_correctos = cursor_cog.fetchall()
    print(f"✅ Encontrados {len(perfiles_correctos)} perfiles correctos")
    
    # 2. Actualizar base de perfiles
    print("🔄 Actualizando base de perfiles...")
    conn_perf = sqlite3.connect(DB_PERFILES)
    cursor_perf = conn_perf.cursor()
    
    # Verificar estructura de la tabla perfiles_cognitivos
    cursor_perf.execute("PRAGMA table_info(perfiles_cognitivos)")
    columnas_perfiles = cursor_perf.fetchall()
    print(f"📋 Columnas en perfiles_cognitivos: {len(columnas_perfiles)}")
    
    actualizaciones = 0
    
    for perfil in perfiles_correctos:
        autor, archivo, formalismo, creatividad, dogmatismo, empirismo, interdisciplinariedad, nivel_abstraccion, complejidad_sintactica, uso_jurisprudencia, fecha_registro = perfil
        
        # Buscar registro correspondiente por archivo
        cursor_perf.execute("""
            SELECT id FROM perfiles_cognitivos 
            WHERE doc_titulo LIKE ? OR doc_titulo LIKE ?
        """, (f"%{archivo}%", f"%{archivo.replace('.pdf', '')}%"))
        
        registro = cursor_perf.fetchone()
        
        if registro:
            # Actualizar registro existente
            cursor_perf.execute("""
                UPDATE perfiles_cognitivos 
                SET autor_detectado = ?
                WHERE id = ?
            """, (autor, registro[0]))
            
            actualizaciones += 1
            print(f"   ✅ Actualizado: {autor} - {archivo}")
        else:
            print(f"   ⚠️ No encontrado en perfiles: {archivo}")
    
    conn_perf.commit()
    conn_cog.close()
    conn_perf.close()
    
    print(f"\n🎉 SINCRONIZACIÓN COMPLETADA:")
    print(f"   ✅ Registros actualizados: {actualizaciones}")
    print(f"   📊 Total perfiles procesados: {len(perfiles_correctos)}")
    
    return actualizaciones > 0

def verificar_sincronizacion():
    """Verifica que la sincronización fue exitosa"""
    print("\n🔍 VERIFICACIÓN POST-SINCRONIZACIÓN:")
    print("=" * 40)
    
    if not DB_PERFILES.exists():
        print("❌ Base de perfiles no encontrada")
        return
    
    conn = sqlite3.connect(DB_PERFILES)
    cursor = conn.cursor()
    
    # Contar autores identificados vs no identificados
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos WHERE autor_detectado != 'Autor no identificado' AND autor_detectado IS NOT NULL")
    identificados = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos WHERE autor_detectado = 'Autor no identificado' OR autor_detectado IS NULL")
    no_identificados = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
    total = cursor.fetchone()[0]
    
    print(f"📊 RESULTADOS:")
    print(f"   ✅ Autores identificados: {identificados}")
    print(f"   ❌ Autores no identificados: {no_identificados}")
    print(f"   📈 Total registros: {total}")
    print(f"   📊 Tasa de éxito: {(identificados/total*100):.1f}%" if total > 0 else "   📊 Tasa de éxito: 0%")
    
    # Mostrar algunos ejemplos
    cursor.execute("SELECT doc_titulo, autor_detectado FROM perfiles_cognitivos LIMIT 5")
    ejemplos = cursor.fetchall()
    
    print(f"\n📄 EJEMPLOS (primeros 5):")
    for doc, autor in ejemplos:
        estado = "✅" if autor and autor != "Autor no identificado" else "❌"
        print(f"   {estado} {doc} -> {autor}")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 INICIANDO SINCRONIZACIÓN DE BASES DE DATOS")
    
    if sincronizar_bases_datos():
        verificar_sincronizacion()
        print("\n✅ Proceso completado exitosamente")
        print("💡 Ahora la ruta /perfiles debería mostrar los autores correctos")
    else:
        print("\n❌ Error en la sincronización")