#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 MIGRADOR DE DATOS AL SISTEMA AUTOR-CÉNTRICO
============================================

Migra datos existentes desde perfiles.db hacia las nuevas bases autor-céntricas
y llena las bases de datos que aparecen vacías.

AUTOR: Sistema Cognitivo v5.0 - Migración Inteligente  
FECHA: 9 NOV 2025
"""

import os
import sys
import sqlite3
import json
from datetime import datetime

def crear_directorios():
    """Asegurar que existan los directorios necesarios"""
    dirs = [
        'colaborative/bases_rag',
        'colaborative/bases_rag/cognitiva'
    ]
    
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"✅ Directorio creado: {dir_path}")

def migrar_perfiles_autorales():
    """Migrar perfiles desde perfiles.db a autor_centrico.db"""
    
    print("🔄 INICIANDO MIGRACIÓN DE PERFILES AUTORALES...")
    
    # Conectar a base de datos fuente
    conn_fuente = sqlite3.connect('colaborative/data/perfiles.db')
    cursor_fuente = conn_fuente.cursor()
    
    # Conectar a base de datos destino
    conn_destino = sqlite3.connect('colaborative/bases_rag/cognitiva/autor_centrico.db')
    cursor_destino = conn_destino.cursor()
    
    # Obtener perfiles existentes
    cursor_fuente.execute('''
        SELECT autor_detectado, doc_titulo, formalismo, creatividad, dogmatismo, 
               empirismo, interdisciplinariedad, nivel_abstraccion, 
               complejidad_sintactica, uso_jurisprudencia, tono, ethos, pathos, logos,
               archivo_fuente, total_palabras, metadatos_completos
        FROM perfiles_cognitivos 
        WHERE autor_detectado IS NOT NULL AND autor_detectado != 'No identificado'
    ''')
    
    perfiles = cursor_fuente.fetchall()
    
    print(f"📊 Encontrados {len(perfiles)} perfiles para migrar")
    
    for perfil in perfiles:
        autor, titulo, formalismo, creatividad, dogmatismo, empirismo, \
        interdisciplinariedad, nivel_abstraccion, sintaxis, jurisprudencia, tono, \
        ethos, pathos, logos, archivo, palabras, metadatos = perfil
        
        # Crear metodología detectada basada en las características
        metodologia = []
        if formalismo > 0.7:
            metodologia.append("Formal-Deductivo")
        if empirismo > 0.6:
            metodologia.append("Empírico-Inductivo")
        if creatividad > 0.5:
            metodologia.append("Creativo-Exploratorio")
        if dogmatismo > 0.6:
            metodologia.append("Doctrinal-Normativo")
        
        metodologia_str = ", ".join(metodologia) if metodologia else "Mixto"
        
        # Crear perfil expandido
        perfil_expandido = {
            "cognitivo": {
                "formalismo": formalismo,
                "creatividad": creatividad,
                "empirismo": empirismo,
                "abstraccion": nivel_abstraccion
            },
            "retórico": {
                "ethos": ethos,
                "pathos": pathos,
                "logos": logos
            },
            "metodología": metodologia_str,
            "complejidad_sintáctica": sintaxis,
            "uso_jurisprudencia": jurisprudencia,
            "tono": tono
        }
        
        # Insertar en tabla autor-céntrica
        cursor_destino.execute('''
            INSERT OR REPLACE INTO perfiles_autorales_expandidos 
            (autor, metodologia_principal, patron_razonamiento_dominante, 
             estilo_argumentativo, estructura_discursiva, uso_ethos, uso_pathos, uso_logos,
             complejidad_sintactica, densidad_conceptual, total_documentos, 
             fecha_ultima_actualizacion, version_perfil)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            autor,
            metodologia_str,
            "Deductivo" if formalismo > 0.6 else "Inductivo" if empirismo > 0.6 else "Abductivo",
            "Formal" if formalismo > 0.6 else "Retórico",
            "Sistemática" if formalismo > 0.5 else "Narrativa",
            ethos if ethos else 0.5,
            pathos if pathos else 0.5,
            logos if logos else 0.5,
            sintaxis if sintaxis else 0.5,
            nivel_abstraccion if nivel_abstraccion else 0.5,
            1,  # total_documentos
            datetime.now().isoformat(),
            'v5.0_migrado'
        ))
        
        print(f"✅ Migrado: {autor} - {metodologia_str}")
    
    # Crear algunas comparativas automáticas
    cursor_destino.execute('SELECT autor, metodologia_principal FROM perfiles_autorales_expandidos')
    autores = cursor_destino.fetchall()
    
    comparativas_creadas = 0
    for i, (autor_a, met_a) in enumerate(autores):
        for autor_b, met_b in autores[i+1:]:
            # Calcular similitud basada en metodología
            similitud = 0.8 if met_a == met_b else 0.3
            
            cursor_destino.execute('''
                INSERT OR REPLACE INTO comparativas_autorales 
                (autor_a, autor_b, similitud_metodologica, diferencias_clave, fecha_analisis)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                autor_a, autor_b, similitud,
                f"Autor A: {met_a} | Autor B: {met_b}",
                datetime.now().isoformat()
            ))
            comparativas_creadas += 1
    
    conn_destino.commit()
    conn_fuente.close()
    conn_destino.close()
    
    print(f"✅ MIGRACIÓN COMPLETADA:")
    print(f"   - {len(perfiles)} perfiles autorales migrados")
    print(f"   - {comparativas_creadas} comparativas generadas")

def poblar_multicapa():
    """Poblar la base de datos multi-capa con análisis iniciales"""
    
    print("🧠 POBLANDO BASE DE DATOS MULTI-CAPA...")
    
    conn = sqlite3.connect('colaborative/bases_rag/cognitiva/multicapa_pensamiento.db')
    cursor = conn.cursor()
    
    # Verificar si existe la tabla
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='patrones_pensamiento_profundo'
    ''')
    
    if not cursor.fetchone():
        print("⚠️  Tabla multi-capa no existe, creándola...")
        
        # Crear tabla básica si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patrones_pensamiento_profundo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT NOT NULL,
                patron_razonamiento TEXT,
                estructura_argumentativa TEXT,
                evolucion_temporal TEXT,
                conexiones_intelectuales TEXT,
                marcadores_cognitivos TEXT,
                fecha_analisis DATETIME DEFAULT CURRENT_TIMESTAMP,
                version_sistema TEXT DEFAULT 'v5.0'
            )
        ''')
    
    # Obtener datos de los perfiles para crear análisis multi-capa
    conn_perfiles = sqlite3.connect('colaborative/data/perfiles.db')
    cursor_perfiles = conn_perfiles.cursor()
    
    cursor_perfiles.execute('''
        SELECT autor_detectado, formalismo, creatividad, dogmatismo, empirismo,
               ethos, pathos, logos, tono, complejidad_sintactica
        FROM perfiles_cognitivos 
        WHERE autor_detectado IS NOT NULL AND autor_detectado != 'No identificado'
    ''')
    
    perfiles = cursor_perfiles.fetchall()
    
    for perfil in perfiles:
        autor, formalismo, creatividad, dogmatismo, empirismo, \
        ethos, pathos, logos, tono, sintaxis = perfil
        
        # Crear patrones de razonamiento profundo
        patron_razonamiento = {
            "dominante": "Deductivo" if formalismo > 0.6 else "Inductivo" if empirismo > 0.6 else "Abductivo",
            "secundario": "Analógico" if creatividad > 0.5 else "Sistemático",
            "velocidad_inferencia": "Rápida" if sintaxis < 0.5 else "Deliberada",
            "tolerancia_ambigüedad": "Alta" if creatividad > 0.6 else "Media"
        }
        
        estructura_argumentativa = {
            "arquitectura_principal": "Silogística" if formalismo > 0.6 else "Retórica",
            "uso_premisas": "Explícitas" if formalismo > 0.5 else "Implícitas",
            "desarrollo_conclusion": "Gradual" if logos > 0.6 else "Directo",
            "integración_evidencia": "Sistemática" if empirismo > 0.6 else "Selectiva"
        }
        
        marcadores_cognitivos = {
            "flexibilidad_mental": creatividad,
            "rigor_lógico": formalismo,
            "apertura_experiencia": empirismo,
            "coherencia_interna": 1.0 - dogmatismo,
            "complejidad_procesamiento": sintaxis
        }
        
        # Insertar análisis multi-capa
        cursor.execute('''
            INSERT OR REPLACE INTO patrones_pensamiento_profundo 
            (autor, patron_razonamiento, estructura_argumentativa, marcadores_cognitivos, fecha_analisis, version_sistema)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            autor,
            json.dumps(patron_razonamiento, ensure_ascii=False),
            json.dumps(estructura_argumentativa, ensure_ascii=False),
            json.dumps(marcadores_cognitivos, ensure_ascii=False),
            datetime.now().isoformat(),
            'v5.0_inicial'
        ))
        
        print(f"🧠 Análisis multi-capa creado para: {autor}")
    
    conn.commit()
    conn_perfiles.close()
    conn.close()
    
    print("✅ BASE MULTI-CAPA POBLADA EXITOSAMENTE")

def verificar_migracion():
    """Verificar que la migración fue exitosa"""
    
    print("\n🔍 VERIFICANDO MIGRACIÓN...")
    
    # Verificar autor-céntrico
    conn_autor = sqlite3.connect('colaborative/bases_rag/cognitiva/autor_centrico.db')
    cursor_autor = conn_autor.cursor()
    
    cursor_autor.execute('SELECT COUNT(*) FROM perfiles_autorales_expandidos')
    total_perfiles = cursor_autor.fetchone()[0]
    
    cursor_autor.execute('SELECT COUNT(*) FROM comparativas_autorales')
    total_comparativas = cursor_autor.fetchone()[0]
    
    conn_autor.close()
    
    # Verificar multi-capa
    conn_multi = sqlite3.connect('colaborative/bases_rag/cognitiva/multicapa_pensamiento.db')
    cursor_multi = conn_multi.cursor()
    
    cursor_multi.execute('SELECT COUNT(*) FROM patrones_pensamiento_profundo')
    total_patrones = cursor_multi.fetchone()[0]
    
    conn_multi.close()
    
    print(f"📊 RESULTADOS DE MIGRACIÓN:")
    print(f"   🧠 Sistema Autor-Céntrico:")
    print(f"     - Perfiles autorales: {total_perfiles}")
    print(f"     - Comparativas generadas: {total_comparativas}")
    print(f"   🔍 Sistema Multi-Capa:")
    print(f"     - Patrones de pensamiento: {total_patrones}")
    
    return total_perfiles > 0 and total_patrones > 0

def main():
    """Función principal de migración"""
    print("🚀 INICIANDO MIGRACIÓN COMPLETA AL SISTEMA AUTOR-CÉNTRICO")
    print("=" * 60)
    
    try:
        # 1. Crear directorios necesarios
        crear_directorios()
        
        # 2. Migrar perfiles autorales
        migrar_perfiles_autorales()
        
        # 3. Poblar base multi-capa
        poblar_multicapa()
        
        # 4. Verificar migración
        if verificar_migracion():
            print("\n✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print("🌟 El sistema autor-céntrico ahora tiene datos para trabajar")
        else:
            print("\n❌ ERROR EN LA MIGRACIÓN")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LA MIGRACIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    if main():
        print("\n🎯 Ahora puedes usar el sistema autor-céntrico con datos reales!")
        print("🌐 Accede a: http://127.0.0.1:5002/autores")
        print("🧠 Y también: http://127.0.0.1:5002/pensamiento")
    else:
        print("\n💥 La migración falló. Revisa los errores arriba.")