#!/usr/bin/env python3
"""
Verificador de integridad de datos cognitivos
Analiza la calidad y completitud de los datos v3.0
"""

import sqlite3
import json
from datetime import datetime

def verificar_datos_v3():
    db_path = "colaborative/bases_rag/cognitiva/metadatos.db"
    
    print("🧠 VERIFICADOR DE INTEGRIDAD DE DATOS v3.0")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Estadísticas generales
        cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
        total_registros = cursor.fetchone()[0]
        
        print(f"📊 ESTADÍSTICAS GENERALES:")
        print("-" * 40)
        print(f"📁 Total registros: {total_registros}")
        
        # Verificar campos v3.0
        campos_v3 = [
            ('archivo', 'Archivos procesados'),
            ('autor_confianza', 'Autores con confianza'),
            ('razonamiento_top3', 'Análisis razonamiento'),
            ('ethos', 'Análisis retórico (Ethos)'),
            ('pathos', 'Análisis retórico (Pathos)'),
            ('logos', 'Análisis retórico (Logos)'),
            ('modalidad_epistemica', 'Modalidad epistémica'),
            ('estructura_silogistica', 'Estructura silogística'),
            ('indice_teleologico', 'Índice teleológico'),
            ('roles_parrafos', 'Roles de párrafos')
        ]
        
        print(f"\n🔍 COMPLETITUD DE CAMPOS v3.0:")
        print("-" * 40)
        
        for campo, descripcion in campos_v3:
            cursor.execute(f"SELECT COUNT(*) FROM perfiles_cognitivos WHERE {campo} IS NOT NULL AND {campo} != ''")
            count = cursor.fetchone()[0]
            porcentaje = (count / total_registros * 100) if total_registros > 0 else 0
            status = "✅" if porcentaje > 80 else "⚠️" if porcentaje > 50 else "❌"
            print(f"{status} {descripcion:<25}: {count:2d}/{total_registros} ({porcentaje:5.1f}%)")
        
        # Verificar autores detectados
        print(f"\n👤 ANÁLISIS DE AUTORES:")
        print("-" * 30)
        cursor.execute("SELECT autor, autor_confianza FROM perfiles_cognitivos WHERE autor IS NOT NULL ORDER BY autor_confianza DESC")
        autores = cursor.fetchall()
        
        autores_unicos = {}
        for autor, confianza in autores:
            if autor not in autores_unicos:
                autores_unicos[autor] = []
            if confianza:
                autores_unicos[autor].append(confianza)
        
        print(f"📚 Autores únicos detectados: {len(autores_unicos)}")
        for autor, confianzas in list(autores_unicos.items())[:5]:  # Top 5
            avg_conf = sum(confianzas) / len(confianzas) if confianzas else 0
            print(f"  • {autor:<20} ({len(confianzas)} docs, conf: {avg_conf:.2f})")
        
        # Verificar razonamiento aristotélico
        print(f"\n🏛️ ANÁLISIS ARISTOTÉLICO:")
        print("-" * 30)
        cursor.execute("SELECT modalidad_epistemica, COUNT(*) FROM perfiles_cognitivos WHERE modalidad_epistemica IS NOT NULL GROUP BY modalidad_epistemica")
        modalidades = cursor.fetchall()
        
        for modalidad, count in modalidades:
            print(f"  📐 {modalidad:<15}: {count} documentos")
        
        # Verificar estructura silogística
        cursor.execute("SELECT estructura_silogistica, COUNT(*) FROM perfiles_cognitivos WHERE estructura_silogistica IS NOT NULL GROUP BY estructura_silogistica")
        estructuras = cursor.fetchall()
        
        print(f"\n📊 ESTRUCTURAS SILOGÍSTICAS:")
        for estructura, count in estructuras[:5]:  # Top 5
            estructura_clean = estructura.split('(')[0].strip() if '(' in estructura else estructura
            print(f"  🔹 {estructura_clean:<15}: {count} documentos")
        
        # Análisis de calidad
        print(f"\n📈 ANÁLISIS DE CALIDAD:")
        print("-" * 30)
        
        # Documentos con análisis completo v3.0
        cursor.execute("""
            SELECT COUNT(*) FROM perfiles_cognitivos 
            WHERE archivo IS NOT NULL 
            AND autor_confianza IS NOT NULL 
            AND modalidad_epistemica IS NOT NULL 
            AND ethos IS NOT NULL
        """)
        completos_v3 = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM perfiles_cognitivos 
            WHERE indice_teleologico IS NOT NULL 
            AND roles_parrafos IS NOT NULL
        """)
        con_teleologico = cursor.fetchone()[0]
        
        print(f"✅ Análisis v3.0 completo: {completos_v3}/{total_registros} ({completos_v3/total_registros*100:.1f}%)")
        print(f"🎯 Con análisis teleológico: {con_teleologico}/{total_registros} ({con_teleologico/total_registros*100:.1f}%)")
        
        # Mostrar muestra de datos recientes
        print(f"\n📋 MUESTRA DE DATOS RECIENTES:")
        print("-" * 50)
        cursor.execute("""
            SELECT autor, archivo, modalidad_epistemica, ethos, pathos, logos
            FROM perfiles_cognitivos 
            WHERE archivo IS NOT NULL
            ORDER BY id DESC 
            LIMIT 3
        """)
        
        for row in cursor.fetchall():
            autor = row[0] if row[0] else "N/A"
            archivo = row[1][:30] + "..." if row[1] and len(row[1]) > 30 else row[1]
            modalidad = row[2] if row[2] else "N/A"
            ethos = f"{row[3]:.2f}" if row[3] else "N/A"
            pathos = f"{row[4]:.2f}" if row[4] else "N/A"
            logos = f"{row[5]:.2f}" if row[5] else "N/A"
            
            print(f"👤 Autor: {autor}")
            print(f"📁 Archivo: {archivo}")
            print(f"🏛️ Modalidad: {modalidad}")
            print(f"🎭 Retórica: E:{ethos} P:{pathos} L:{logos}")
            print()
        
        conn.close()
        
        # Evaluación final
        print("=" * 60)
        if completos_v3 >= total_registros * 0.8:
            print("✅ BASE DE DATOS EN EXCELENTE ESTADO")
            print("🎯 Todos los sistemas v3.0 operativos")
        elif completos_v3 >= total_registros * 0.5:
            print("⚠️ BASE DE DATOS PARCIALMENTE ACTUALIZADA")
            print("💡 Recomendación: Ejecutar ingesta v3.0")
        else:
            print("❌ BASE DE DATOS REQUIERE ACTUALIZACIÓN COMPLETA")
            print("🔧 Acción requerida: Ingesta completa v3.0")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    verificar_datos_v3()