#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🎯 SCRIPT RÁPIDO: Agregar nuevo autor al sistema
Ejecuta esto después de procesar_todo.py para confirmar que todo funcionó
"""

import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'colaborative/scripts'))

def verificar_autores():
    """Verifica cuántos autores hay en el sistema"""
    
    # Probar múltiples ubicaciones de BD
    db_paths = [
        Path("colaborative/bases_rag/cognitiva/autor_centrico.db"),  # Donde están los 4 autores
        Path("colaborative/bases_rag/cognitiva/pensamiento_integrado_v2.db"),  # Nuevo sistema
        Path("colaborative/bases_rag/cognitiva/metadatos.db"),  # Sistema antiguo
    ]
    
    db_path = None
    for path in db_paths:
        if path.exists():
            db_path = path
            break
    
    if not db_path:
        print("❌ Base de datos no encontrada. Ejecuta primero: python procesar_todo.py")
        return False
    
    print("\n" + "="*60)
    print("📊 ESTADO ACTUAL DEL SISTEMA DE AUTORES")
    print(f"📍 Base de datos: {db_path.name}")
    print("="*60)
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Obtener lista de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [t[0] for t in cursor.fetchall()]
        print(f"\n📋 Tablas disponibles: {tablas}")
        
        # Detectar cuál tabla tiene los perfiles
        tabla_perfil = None
        if 'perfiles_autorales_expandidos' in tablas:
            tabla_perfil = 'perfiles_autorales_expandidos'
        elif 'perfiles_integrales' in tablas:
            tabla_perfil = 'perfiles_integrales'
        elif 'perfiles_integrados_v2' in tablas:
            tabla_perfil = 'perfiles_integrados_v2'
        elif 'perfiles_cognitivos' in tablas:
            tabla_perfil = 'perfiles_cognitivos'
        elif 'perfiles_autorales' in tablas:
            tabla_perfil = 'perfiles_autorales'
        
        if not tabla_perfil:
            print("⚠️ No se encontró tabla de perfiles")
            conn.close()
            return False
        
        # Contar autores totales
        cursor.execute(f"SELECT COUNT(DISTINCT autor) FROM {tabla_perfil}")
        total_autores = cursor.fetchone()[0]
        print(f"\n✅ Total de autores en BD: {total_autores}")
        
        # Listar autores
        print("\n📝 Autores registrados:")
        cursor.execute(f"""
            SELECT DISTINCT autor, COUNT(*) as registros 
            FROM {tabla_perfil} 
            GROUP BY autor
            ORDER BY autor
        """)
        
        autores = cursor.fetchall()
        for i, (autor, registros) in enumerate(autores, 1):
            print(f"   {i}. {autor} ({registros} perfil/es)")
        
        # Verificar específicamente Jesús Alberto Aybar
        cursor.execute(
            f"SELECT COUNT(*) FROM {tabla_perfil} WHERE autor = ?",
            ("Jesús Alberto Aybar",)
        )
        count_aybar = cursor.fetchone()[0]
        
        if count_aybar > 0:
            print(f"\n✅ Jesús Alberto Aybar: {count_aybar} perfil/es encontrado(s)")
            
            # Mostrar detalles del perfil si existen las columnas
            try:
                cursor.execute(f"""
                    SELECT razonamiento_dominante, modalidad_dominante, 
                           nivel_abstraccion, creatividad, empirismo
                    FROM {tabla_perfil} 
                    WHERE autor = 'Jesús Alberto Aybar'
                    LIMIT 1
                """)
                perfil = cursor.fetchone()
                if perfil:
                    print(f"\n   Razonamiento: {perfil[0]}")
                    print(f"   Modalidad epistémica: {perfil[1]}")
                    print(f"   Nivel de abstracción: {perfil[2]:.2%}" if perfil[2] else "   Nivel de abstracción: N/A")
                    print(f"   Creatividad: {perfil[3]:.2%}" if perfil[3] else "   Creatividad: N/A")
                    print(f"   Empirismo: {perfil[4]:.2%}" if perfil[4] else "   Empirismo: N/A")
            except Exception as e:
                print(f"   (Detalles no disponibles: {e})")
        else:
            print(f"\n⚠️ Jesús Alberto Aybar NO encontrado en {tabla_perfil}")
            print("   → Necesitas ejecutar: python procesar_todo.py")
        
        conn.close()
        
        print("\n" + "="*60)
        if total_autores >= 5:
            print("✅ SISTEMA CON 5+ AUTORES - LISTO PARA USAR")
        elif total_autores >= 4:
            print(f"⚠️ SISTEMA CON {total_autores} AUTORES - CASI LISTO")
        else:
            print(f"❌ SISTEMA CON SOLO {total_autores} AUTORES - INCOMPLETO")
        print("="*60)
        
        return total_autores >= 4
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n🔍 Verificando estado del sistema de autores...")
    success = verificar_autores()
    
    if not success:
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Ejecuta: python procesar_todo.py")
        print("2. Espera a que complete")
        print("3. Luego ejecuta este script de nuevo: python verificar_autores.py")
    else:
        print("\n✅ Sistema listo. Próximos pasos:")
        print("1. Inicia la webapp: python colaborative/scripts/end2end_webapp.py")
        print("2. Abre: http://127.0.0.1:5002/autores")
        print("3. Verás todos los autores con sus análisis cognitivos")

if __name__ == '__main__':
    main()
