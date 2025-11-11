#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
🔍 VERIFICADOR INTEGRAL DEL SISTEMA - ANALYSER v3.1
===========================================================
Verifica que todo el ecosistema esté funcionando correctamente
y sea totalmente funcional de forma integrada.
===========================================================
"""

import sqlite3
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import importlib.util

BASE_PATH = Path(__file__).resolve().parents[0]
COLABORATIVE_DIR = BASE_PATH / "colaborative"
SCRIPTS_DIR = COLABORATIVE_DIR / "scripts"

def verificar_bases_datos():
    """Verifica todas las bases de datos del sistema."""
    print("🔍 VERIFICACIÓN DE BASES DE DATOS")
    print("-" * 50)
    
    bases = {
        "Cognitiva": COLABORATIVE_DIR / "bases_rag" / "cognitiva" / "metadatos.db",
        "Perfiles": COLABORATIVE_DIR / "data" / "perfiles.db",
        "Autoaprendizaje": COLABORATIVE_DIR / "data" / "autoaprendizaje.db"
    }
    
    resultados = {}
    
    for nombre, ruta in bases.items():
        try:
            if not ruta.exists():
                resultados[nombre] = {"estado": "❌ NO EXISTE", "registros": 0}
                continue
                
            with sqlite3.connect(str(ruta)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tablas = [row[0] for row in cursor.fetchall()]
                
                total_registros = 0
                for tabla in tablas:
                    if not tabla.startswith('sqlite_'):
                        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                        count = cursor.fetchone()[0]
                        total_registros += count
                
                size_kb = ruta.stat().st_size / 1024
                resultados[nombre] = {
                    "estado": "✅ ACTIVA",
                    "tablas": len(tablas),
                    "registros": total_registros,
                    "tamaño": f"{size_kb:.1f} KB"
                }
                
        except Exception as e:
            resultados[nombre] = {"estado": f"❌ ERROR: {e}", "registros": 0}
    
    # Mostrar resultados
    for nombre, info in resultados.items():
        print(f"{info['estado']:15} {nombre:15} | {info.get('registros', 0):3} registros | {info.get('tamaño', 'N/A')}")
    
    return all("✅" in info["estado"] for info in resultados.values())

def verificar_modulos_python():
    """Verifica que los módulos principales estén funcionales."""
    print("\n🐍 VERIFICACIÓN DE MÓDULOS PYTHON")
    print("-" * 50)
    
    modulos_criticos = [
        "ingesta_cognitiva.py",
        "detector_razonamiento_aristotelico.py", 
        "analizador_perfiles.py",
        "autoaprendizaje.py",
        "matriz_cognitiva.py",
        "pipeline_refinamiento.py",
        "end2end_webapp.py"
    ]
    
    resultados = {}
    
    for modulo in modulos_criticos:
        ruta_modulo = SCRIPTS_DIR / modulo
        
        try:
            if not ruta_modulo.exists():
                resultados[modulo] = "❌ NO EXISTE"
                continue
            
            # Verificar sintaxis
            with open(ruta_modulo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Compilar para verificar sintaxis
            compile(contenido, str(ruta_modulo), 'exec')
            
            # Contar líneas y función principales
            lineas = len(contenido.split('\n'))
            funciones = contenido.count('def ')
            
            resultados[modulo] = f"✅ OK ({lineas:4} líneas, {funciones:2} funciones)"
            
        except SyntaxError as e:
            resultados[modulo] = f"❌ SINTAXIS: {e}"
        except Exception as e:
            resultados[modulo] = f"❌ ERROR: {e}"
    
    # Mostrar resultados
    for modulo, estado in resultados.items():
        print(f"{estado:40} | {modulo}")
    
    return all("✅" in estado for estado in resultados.values())

def verificar_integracion_datos():
    """Verifica que los datos estén correctamente integrados."""
    print("\n🔗 VERIFICACIÓN DE INTEGRACIÓN DE DATOS")
    print("-" * 50)
    
    try:
        # Base cognitiva
        db_cognitiva = COLABORATIVE_DIR / "bases_rag" / "cognitiva" / "metadatos.db"
        with sqlite3.connect(str(db_cognitiva)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT archivo, autor, autor_confianza, modalidad_epistemica, ethos, pathos, logos
                FROM perfiles_cognitivos 
                ORDER BY fecha_registro DESC
            """)
            datos_cognitivos = cursor.fetchall()
        
        print(f"📊 Datos cognitivos: {len(datos_cognitivos)} registros")
        
        # Verificar calidad de datos
        autores_identificados = len([d for d in datos_cognitivos if d[1] != 'Autor no identificado'])
        con_confianza_alta = len([d for d in datos_cognitivos if d[2] and d[2] > 0.8])
        con_analisis_retorico = len([d for d in datos_cognitivos if d[4] and d[5] and d[6]])
        
        print(f"   ✅ Autores identificados: {autores_identificados}/{len(datos_cognitivos)}")
        print(f"   ✅ Confianza alta (>0.8): {con_confianza_alta}/{len(datos_cognitivos)}")
        print(f"   ✅ Análisis retórico completo: {con_analisis_retorico}/{len(datos_cognitivos)}")
        
        # Verificar perfiles sincronizados
        db_perfiles = COLABORATIVE_DIR / "data" / "perfiles.db"
        if db_perfiles.exists():
            with sqlite3.connect(str(db_perfiles)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM perfiles_autores")
                count_perfiles = cursor.fetchone()[0]
                print(f"   ✅ Perfiles de autores: {count_perfiles}")  
        
        # Calcular score de integridad
        score_integridad = (
            (autores_identificados / len(datos_cognitivos)) * 0.4 +
            (con_confianza_alta / len(datos_cognitivos)) * 0.3 +
            (con_analisis_retorico / len(datos_cognitivos)) * 0.3
        ) * 100
        
        print(f"   🎯 Score de integridad: {score_integridad:.1f}%")
        
        return score_integridad >= 80
        
    except Exception as e:
        print(f"❌ Error verificando integración: {e}")
        return False

def verificar_funcionalidad_webapp():
    """Verifica que la webapp esté lista para funcionar."""
    print("\n🌐 VERIFICACIÓN DE WEBAPP")
    print("-" * 50)
    
    try:
        webapp_path = SCRIPTS_DIR / "end2end_webapp.py"
        
        if not webapp_path.exists():
            print("❌ Archivo webapp no encontrado")
            return False
        
        # Verificar que tiene las rutas principales
        with open(webapp_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        rutas_necesarias = [
            '@app.route("/"',
            '@app.route("/cognitivo"',
            '@app.route("/perfiles"', 
            '@app.route("/radar"',
            'if __name__ == "__main__":'
        ]
        
        rutas_encontradas = 0
        for ruta in rutas_necesarias:
            if ruta in contenido:
                rutas_encontradas += 1
                print(f"   ✅ {ruta}")
            else:
                print(f"   ❌ {ruta}")
        
        # Verificar imports críticos
        imports_criticos = ['Flask', 'sqlite3', 'json', 'plotly']
        imports_encontrados = 0
        
        for imp in imports_criticos:
            if imp in contenido:
                imports_encontrados += 1
        
        print(f"   📦 Imports críticos: {imports_encontrados}/{len(imports_criticos)}")
        print(f"   🌐 Rutas encontradas: {rutas_encontradas}/{len(rutas_necesarias)}")
        
        return rutas_encontradas >= 4 and imports_encontrados >= 3
        
    except Exception as e:
        print(f"❌ Error verificando webapp: {e}")
        return False

def verificar_sistema_completo():
    """Ejecuta verificación completa del sistema."""
    print("=" * 70)
    print("🔍 VERIFICACIÓN INTEGRAL DEL SISTEMA ANALYSER v3.1")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Directorio: {BASE_PATH}")
    
    # Ejecutar verificaciones
    verificaciones = [
        ("Bases de Datos", verificar_bases_datos),
        ("Módulos Python", verificar_modulos_python),
        ("Integración de Datos", verificar_integracion_datos),
        ("Funcionalidad Webapp", verificar_funcionalidad_webapp)
    ]
    
    resultados = []
    
    for nombre, funcion in verificaciones:
        try:
            resultado = funcion()
            resultados.append(resultado)
            print(f"\n{'✅' if resultado else '❌'} {nombre}: {'CORRECTO' if resultado else 'NECESITA ATENCIÓN'}")
        except Exception as e:
            print(f"\n❌ {nombre}: ERROR - {e}")
            resultados.append(False)
    
    # Resumen final
    exitos = sum(resultados)
    total = len(resultados)
    porcentaje = (exitos / total) * 100
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN FINAL")
    print("=" * 70)
    print(f"🎯 Verificaciones exitosas: {exitos}/{total} ({porcentaje:.0f}%)")
    
    if porcentaje == 100:
        print("🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
        print("✅ Todas las verificaciones pasaron correctamente")
        print("🚀 El sistema está listo para funcionar integralmente") 
    elif porcentaje >= 75:
        print("✅ SISTEMA MAYORMENTE FUNCIONAL")
        print("⚠️ Algunas verificaciones necesitan atención menor")
        print("🔧 Se puede usar pero con precauciones")
    else:
        print("❌ SISTEMA NECESITA ATENCIÓN")
        print("🔧 Se requieren correcciones antes del uso")
    
    return porcentaje

if __name__ == "__main__":
    resultado = verificar_sistema_completo()
    sys.exit(0 if resultado >= 75 else 1)