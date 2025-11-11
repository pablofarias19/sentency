#!/usr/bin/env python3
"""
Verificador de Base de Datos Cognitiva
Comprueba la estructura y datos de la base ANALYSER MÉTODO v3.0
"""

import sqlite3
import os
from datetime import datetime

def verificar_base_datos():
    db_path = "colaborative/bases_rag/cognitiva/metadatos.db"
    
    print("🧠 VERIFICADOR DE BASE DE DATOS COGNITIVA")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🗃️ Base de datos: {os.path.abspath(db_path)}")
    print()
    
    if not os.path.exists(db_path):
        print("❌ ERROR: Base de datos no encontrada")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estructura de tabla
        print("📊 ESTRUCTURA DE LA TABLA 'metadatos_cognitivos':")
        print("-" * 60)
        cursor.execute("PRAGMA table_info(metadatos_cognitivos)")
        columns = cursor.fetchall()
        
        print(f"{'#':<3} {'COLUMNA':<25} {'TIPO':<12} {'NULL':<6} {'DEFAULT':<10}")
        print("-" * 60)
        
        for i, col in enumerate(columns, 1):
            col_name = col[1]
            col_type = col[2]
            not_null = "NO" if col[3] == 1 else "SI"
            default_val = col[4] if col[4] else ""
            print(f"{i:<3} {col_name:<25} {col_type:<12} {not_null:<6} {str(default_val):<10}")
        
        print("-" * 60)
        print(f"✅ Total columnas: {len(columns)}")
        print()
        
        # Verificar campos ANALYSER específicos
        analyser_fields = [
            'autor_principal', 'confianza_autor', 'autores_citados', 
            'razonamiento_tipo_1', 'razonamiento_score_1', 'razonamiento_tipo_2',
            'razonamiento_score_2', 'razonamiento_tipo_3', 'razonamiento_score_3',
            'ethos_score', 'pathos_score', 'logos_score', 'complejidad_sintactica_v2',
            'nivel_tecnico_latinismos', 'densidad_citas_legales', 'referencias_doctrinarias',
            'archivo', 'indice_teleologico', 'roles_parrafos', 'fecha_registro'
        ]
        
        print("🧠 CAMPOS ANALYSER MÉTODO v3.0:")
        print("-" * 40)
        existing_columns = [col[1] for col in columns]
        
        for field in analyser_fields:
            status = "✅" if field in existing_columns else "❌"
            print(f"{status} {field}")
        
        analyser_present = sum(1 for field in analyser_fields if field in existing_columns)
        print("-" * 40)
        print(f"Campos ANALYSER presentes: {analyser_present}/{len(analyser_fields)}")
        print()
        
        # Verificar datos existentes
        cursor.execute("SELECT COUNT(*) FROM metadatos_cognitivos")
        total_registros = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM metadatos_cognitivos WHERE autor_principal IS NOT NULL")
        registros_con_autor = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM metadatos_cognitivos WHERE archivo IS NOT NULL")
        registros_v3 = cursor.fetchone()[0]
        
        print("📈 ESTADÍSTICAS DE DATOS:")
        print("-" * 30)
        print(f"📁 Total registros: {total_registros}")
        print(f"👤 Con autor detectado: {registros_con_autor}")
        print(f"🧠 Procesados con v3.0: {registros_v3}")
        print()
        
        if total_registros > 0:
            print("📋 MUESTRA DE DATOS (últimos 3 registros):")
            print("-" * 50)
            cursor.execute("""
                SELECT documento, autor_principal, confianza_autor, archivo
                FROM metadatos_cognitivos 
                ORDER BY id DESC 
                LIMIT 3
            """)
            
            for row in cursor.fetchall():
                doc = row[0][:30] + "..." if row[0] and len(row[0]) > 30 else row[0]
                autor = row[1] if row[1] else "N/A"
                confianza = f"{row[2]:.2f}" if row[2] else "N/A"
                archivo = row[3] if row[3] else "N/A"
                print(f"📄 {doc}")
                print(f"   👤 Autor: {autor} (confianza: {confianza})")
                print(f"   📁 Archivo: {archivo}")
                print()
        
        conn.close()
        
        print("=" * 60)
        if analyser_present == len(analyser_fields):
            print("✅ BASE DE DATOS COMPLETAMENTE ACTUALIZADA")
        else:
            print("⚠️ BASE DE DATOS REQUIERE ACTUALIZACIÓN")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    verificar_base_datos()