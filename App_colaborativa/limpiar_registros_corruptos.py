#!/usr/bin/env python3
"""
LIMPIADOR DE REGISTROS CORRUPTOS
================================
Elimina registros corruptos y mal formados de la base de perfiles
"""

import sqlite3
from pathlib import Path

DB_PERFILES = Path("colaborative/data/perfiles.db")

def limpiar_registros_corruptos():
    """Limpia registros corruptos de la base de perfiles"""
    print("🧹 LIMPIADOR DE REGISTROS CORRUPTOS")
    print("=" * 40)
    
    if not DB_PERFILES.exists():
        print(f"❌ Base de perfiles no encontrada: {DB_PERFILES}")
        return False
    
    conn = sqlite3.connect(DB_PERFILES)
    cursor = conn.cursor()
    
    # 1. Mostrar registros problemáticos
    print("🔍 IDENTIFICANDO REGISTROS PROBLEMÁTICOS:")
    cursor.execute("""
        SELECT id, doc_titulo, autor_detectado 
        FROM perfiles_cognitivos 
        WHERE autor_detectado = 'Autor no identificado' 
           OR autor_detectado IS NULL
           OR doc_titulo LIKE '%•%'
           OR doc_titulo LIKE '%~%'
    """)
    
    registros_problematicos = cursor.fetchall()
    print(f"📊 Encontrados {len(registros_problematicos)} registros problemáticos:")
    
    for reg_id, titulo, autor in registros_problematicos:
        print(f"   ❌ ID {reg_id}: {titulo} -> {autor}")
    
    if len(registros_problematicos) == 0:
        print("✅ No se encontraron registros corruptos")
        conn.close()
        return True
    
    # 2. Eliminar registros corruptos
    respuesta = input(f"\n¿Eliminar estos {len(registros_problematicos)} registros problemáticos? (s/n): ")
    
    if respuesta.lower() in ['s', 'si', 'y', 'yes']:
        eliminados = 0
        for reg_id, titulo, autor in registros_problematicos:
            cursor.execute("DELETE FROM perfiles_cognitivos WHERE id = ?", (reg_id,))
            eliminados += 1
            print(f"   🗑️ Eliminado: {titulo}")
        
        conn.commit()
        print(f"\n✅ Eliminados {eliminados} registros corruptos")
    else:
        print("❌ Operación cancelada")
        conn.close()
        return False
    
    # 3. Verificar estado final
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
    total_restante = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos WHERE autor_detectado != 'Autor no identificado' AND autor_detectado IS NOT NULL")
    identificados = cursor.fetchone()[0]
    
    print(f"\n📊 ESTADO FINAL:")
    print(f"   📈 Total registros: {total_restante}")
    print(f"   ✅ Autores identificados: {identificados}")
    print(f"   📊 Tasa de éxito: {(identificados/total_restante*100):.1f}%" if total_restante > 0 else "   📊 Tasa de éxito: 0%")
    
    conn.close()
    return True

def mostrar_registros_finales():
    """Muestra el estado final de los registros"""
    if not DB_PERFILES.exists():
        return
    
    conn = sqlite3.connect(DB_PERFILES)
    cursor = conn.cursor()
    
    cursor.execute("SELECT doc_titulo, autor_detectado FROM perfiles_cognitivos ORDER BY id")
    registros = cursor.fetchall()
    
    print(f"\n📄 REGISTROS FINALES ({len(registros)}):")
    for titulo, autor in registros:
        estado = "✅" if autor and autor != "Autor no identificado" else "❌"
        titulo_corto = titulo[:50] + "..." if len(titulo) > 50 else titulo
        print(f"   {estado} {titulo_corto} -> {autor}")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 INICIANDO LIMPIEZA DE REGISTROS CORRUPTOS")
    
    if limpiar_registros_corruptos():
        mostrar_registros_finales()
        print("\n✅ Limpieza completada")
    else:
        print("\n❌ Error en la limpieza")