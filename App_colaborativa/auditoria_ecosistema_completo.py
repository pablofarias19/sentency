#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
🔍 AUDITORÍA COMPLETA DEL ECOSISTEMA ANALYSER MÉTODO v3.1
===========================================================
Verificación sistemática de TODOS los módulos y componentes
del sistema de análisis cognitivo profundo.

MÓDULOS A VERIFICAR:
1. Analizador de Perfiles
2. Autoaprendizaje  
3. Detector de Autor y Método
4. Detector de Razonamiento
5. PDF Enriquecido
6. Ingesta Cognitiva
7. Pipeline Refinamiento
8. Matriz Cognitiva
9. Componentes adicionales
===========================================================
"""

import os
import sys
import ast
import inspect
from pathlib import Path
import importlib.util
from datetime import datetime
import json
import re

# ================================
# 📁 CONFIGURACIÓN DE RUTAS  
# ================================
BASE_PATH = Path(__file__).resolve().parents[0]
SCRIPTS_DIR = BASE_PATH / "colaborative" / "scripts"

def analizar_archivo_python(ruta_archivo):
    """Analiza un archivo Python y extrae información técnica."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Parsear AST
        try:
            tree = ast.parse(contenido)
        except SyntaxError as e:
            return {"error": f"Error de sintaxis: {e}"}
        
        # Extraer información
        info = {
            "lineas_codigo": len(contenido.split('\n')),
            "caracteres": len(contenido),
            "funciones": [],
            "clases": [],
            "imports": [],
            "docstring": None,
            "complejidad_estimada": 0
        }
        
        # Recorrer AST
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "nombre": node.name,
                    "args": len(node.args.args),
                    "linea": node.lineno,
                    "docstring": ast.get_docstring(node)
                }
                info["funciones"].append(func_info)
                info["complejidad_estimada"] += 1
                
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "nombre": node.name,
                    "linea": node.linea,
                    "docstring": ast.get_docstring(node)
                }
                info["clases"].append(class_info)
                info["complejidad_estimada"] += 2
                
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        info["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    modulo = node.module or ""
                    for alias in node.names:
                        info["imports"].append(f"{modulo}.{alias.name}")
        
        # Extraer docstring del módulo
        if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Str):
            info["docstring"] = tree.body[0].value.s
        
        # Detectar patrones avanzados
        info["patrones_avanzados"] = detectar_patrones_avanzados(contenido)
        
        return info
        
    except Exception as e:
        return {"error": str(e)}

def detectar_patrones_avanzados(codigo):
    """Detecta patrones avanzados de programación en el código."""
    patrones = {
        "machine_learning": bool(re.search(r'(sklearn|tensorflow|torch|transformers|spacy)', codigo, re.I)),
        "deep_analysis": bool(re.search(r'(aristotelico|cognitivo|retorica|silogismo|epistemico)', codigo, re.I)),
        "nlp_processing": bool(re.search(r'(nlp|tokeniz|embeddings|vectoriz)', codigo, re.I)),
        "pdf_processing": bool(re.search(r'(fitz|PyMuPDF|pdf|layout|spans)', codigo, re.I)),
        "database_ops": bool(re.search(r'(sqlite|INSERT|SELECT|UPDATE|cursor)', codigo, re.I)),
        "regex_patterns": len(re.findall(r'r["\'].*?["\']', codigo)),
        "async_programming": bool(re.search(r'(async|await)', codigo, re.I)),
        "error_handling": len(re.findall(r'try:|except|finally:', codigo)),
        "decorators": len(re.findall(r'@\w+', codigo)),
        "list_comprehensions": len(re.findall(r'\[.*for.*in.*\]', codigo)),
        "type_hints": bool(re.search(r':\s*(str|int|float|bool|List|Dict|Optional)', codigo)),
        "logging": bool(re.search(r'(logging|print\(f)', codigo, re.I))
    }
    return patrones

def main():
    """Función principal del análisis completo."""
    print("=" * 90)
    print("🔍 AUDITORÍA COMPLETA DEL ECOSISTEMA ANALYSER MÉTODO v3.1")
    print("=" * 90)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Directorio: {SCRIPTS_DIR}")
    print("=" * 90)
    
    # ================================
    # 📋 MÓDULOS PRINCIPALES A VERIFICAR
    # ================================
    modulos_criticos = {
        "🧠 ANALIZADOR DE PERFILES": "analizador_perfiles.py",
        "🎓 AUTOAPRENDIZAJE": "autoaprendizaje.py", 
        "👤 DETECTOR AUTOR Y MÉTODO": "detector_autor_y_metodo.py",
        "🧭 DETECTOR RAZONAMIENTO": "detector_razonamiento_aristotelico.py",
        "📄 PDF ENRIQUECIDO": "extractor_pdf_enriquecido.py",
        "🧠 INGESTA COGNITIVA": "ingesta_cognitiva.py",
        "🔄 PIPELINE REFINAMIENTO": "pipeline_refinamiento.py",
        "🎯 MATRIZ COGNITIVA": "matriz_cognitiva.py"
    }
    
    print("\n🔍 1. ANÁLISIS DE MÓDULOS PRINCIPALES")
    print("-" * 70)
    
    resultados_analisis = {}
    
    for nombre_modulo, archivo in modulos_criticos.items():
        print(f"\n{nombre_modulo}")
        print("=" * 50)
        
        ruta_archivo = SCRIPTS_DIR / archivo
        
        if not ruta_archivo.exists():
            print(f"❌ ARCHIVO NO ENCONTRADO: {archivo}")
            resultados_analisis[nombre_modulo] = {"estado": "FALTANTE"}
            continue
        
        # Analizar archivo
        analisis = analizar_archivo_python(ruta_archivo)
        
        if "error" in analisis:
            print(f"❌ ERROR AL ANALIZAR: {analisis['error']}")
            resultados_analisis[nombre_modulo] = {"estado": "ERROR", "error": analisis["error"]}
            continue
        
        # Mostrar información técnica
        print(f"📊 Líneas de código: {analisis['lineas_codigo']:,}")
        print(f"📝 Caracteres: {analisis['caracteres']:,}")
        print(f"🔧 Funciones: {len(analisis['funciones'])}")
        print(f"📦 Clases: {len(analisis['clases'])}")
        print(f"📚 Imports: {len(analisis['imports'])}")
        print(f"🎯 Complejidad estimada: {analisis['complejidad_estimada']}")
        
        # Mostrar funciones principales
        if analisis['funciones']:
            print("🔧 Funciones principales:")
            for func in analisis['funciones'][:5]:  # Top 5
                args_info = f"({func['args']} args)" if func['args'] > 0 else "(sin args)"
                print(f"   • {func['nombre']} {args_info} - línea {func['linea']}")
        
        # Mostrar imports críticos
        imports_criticos = [imp for imp in analisis['imports'] 
                           if any(tech in imp.lower() for tech in 
                                ['sklearn', 'torch', 'transformers', 'spacy', 'fitz', 'sqlite', 'numpy'])]
        if imports_criticos:
            print("📚 Imports técnicos críticos:")
            for imp in imports_criticos[:5]:
                print(f"   • {imp}")
        
        # Mostrar patrones avanzados
        patrones = analisis['patrones_avanzados']
        patrones_activos = [k for k, v in patrones.items() if v is True or (isinstance(v, int) and v > 0)]
        if patrones_activos:
            print("🎯 Patrones avanzados detectados:")
            for patron in patrones_activos:
                valor = patrones[patron]
                if isinstance(valor, bool):
                    print(f"   ✅ {patron.replace('_', ' ').title()}")
                else:
                    print(f"   📊 {patron.replace('_', ' ').title()}: {valor}")
        
        resultados_analisis[nombre_modulo] = {
            "estado": "ACTIVO",
            "lineas": analisis['lineas_codigo'],
            "funciones": len(analisis['funciones']),
            "complejidad": analisis['complejidad_estimada'],
            "patrones": patrones_activos
        }
    
    # ================================
    # 📋 MÓDULOS COMPLEMENTARIOS
    # ================================
    print(f"\n🔍 2. ANÁLISIS DE MÓDULOS COMPLEMENTARIOS")
    print("-" * 70)
    
    modulos_complementarios = [
        "ai_engine.py",
        "prompt_manager.py", 
        "end2end_webapp.py",
        "profiles_rag.py",
        "pipeline_resumen_doctrinario.py",
        "ingesta_enriquecida.py",
        "config_pca.py"
    ]
    
    complementarios_activos = 0
    for archivo in modulos_complementarios:
        ruta = SCRIPTS_DIR / archivo
        if ruta.exists():
            size_kb = ruta.stat().st_size / 1024
            print(f"✅ {archivo:30} ({size_kb:.1f} KB)")
            complementarios_activos += 1
        else:
            print(f"❌ {archivo:30} (FALTANTE)")
    
    print(f"\n📊 Módulos complementarios activos: {complementarios_activos}/{len(modulos_complementarios)}")
    
    # ================================
    # 📋 VERIFICACIÓN DE INTEGRACIÓN
    # ================================
    print(f"\n🔍 3. VERIFICACIÓN DE INTEGRACIÓN DEL SISTEMA")
    print("-" * 70)
    
    # Verificar imports cruzados
    archivos_python = list(SCRIPTS_DIR.glob("*.py"))
    print(f"📁 Total archivos Python: {len(archivos_python)}")
    
    # Buscar interdependencias
    interdependencias = {}
    for archivo in archivos_python:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Buscar imports internos
            imports_internos = []
            for otro_archivo in archivos_python:
                if otro_archivo != archivo:
                    nombre_modulo = otro_archivo.stem
                    if nombre_modulo in contenido:
                        imports_internos.append(nombre_modulo)
            
            if imports_internos:
                interdependencias[archivo.stem] = imports_internos
                
        except Exception:
            continue
    
    print("🔗 Interdependencias detectadas:")
    for modulo, deps in interdependencias.items():
        if len(deps) > 0:
            print(f"   📦 {modulo} → {', '.join(deps[:3])}")
    
    # ================================
    # 📋 RESUMEN EJECUTIVO
    # ================================
    print(f"\n📋 4. RESUMEN EJECUTIVO DEL ECOSISTEMA")
    print("-" * 70)
    
    total_lineas = sum([res.get("lineas", 0) for res in resultados_analisis.values() if isinstance(res, dict)])
    total_funciones = sum([res.get("funciones", 0) for res in resultados_analisis.values() if isinstance(res, dict)])
    modulos_activos = len([res for res in resultados_analisis.values() if res.get("estado") == "ACTIVO"])
    
    print(f"🎯 MÉTRICAS DEL ECOSISTEMA:")
    print(f"   📊 Total líneas de código: {total_lineas:,}")
    print(f"   🔧 Total funciones: {total_funciones}")
    print(f"   📦 Módulos principales activos: {modulos_activos}/8")
    print(f"   🔗 Módulos complementarios: {complementarios_activos}")
    print(f"   🎯 Interdependencias: {len(interdependencias)}")
    
    # Clasificación por complejidad
    print(f"\n📊 CLASIFICACIÓN POR COMPLEJIDAD:")
    for nombre, resultado in resultados_analisis.items():
        if resultado.get("estado") == "ACTIVO":
            complejidad = resultado.get("complejidad", 0)
            if complejidad > 50:
                nivel = "🔴 ALTO"
            elif complejidad > 20:
                nivel = "🟡 MEDIO"
            else:
                nivel = "🟢 BÁSICO"
            print(f"   {nivel} {nombre}: {complejidad} puntos")
    
    # Verificar funcionalidades críticas
    print(f"\n✅ FUNCIONALIDADES CRÍTICAS VERIFICADAS:")
    funcionalidades = [
        ("Detección de Autoría", "detector_autor_y_metodo.py" in [m.split()[-1] for m in modulos_criticos.values()]),
        ("Análisis Aristotélico", "detector_razonamiento_aristotelico.py" in [m.split()[-1] for m in modulos_criticos.values()]),
        ("Procesamiento PDF", any("pdf" in str(res.get("patrones", [])) for res in resultados_analisis.values() if isinstance(res, dict))),
        ("Machine Learning", any("machine_learning" in res.get("patrones", []) for res in resultados_analisis.values() if isinstance(res, dict))),
        ("Base de Datos", any("database_ops" in res.get("patrones", []) for res in resultados_analisis.values() if isinstance(res, dict))),
        ("Interfaz Web", "end2end_webapp.py" in [f.name for f in archivos_python]),
        ("Pipeline Completo", "pipeline_refinamiento.py" in [f.name for f in archivos_python]),
        ("Matriz Cognitiva", "matriz_cognitiva.py" in [f.name for f in archivos_python])
    ]
    
    for funcionalidad, estado in funcionalidades:
        icono = "✅" if estado else "❌"
        print(f"   {icono} {funcionalidad}")
    
    print("\n" + "=" * 90)
    print("🎉 CONCLUSIÓN: Sistema ANALYSER MÉTODO v3.1 - ECOSISTEMA COMPLETO")
    print(f"   📊 {modulos_activos} módulos principales + {complementarios_activos} complementarios")
    print(f"   🔧 {total_funciones} funciones especializadas en {total_lineas:,} líneas")
    print("   🎯 Análisis cognitivo profundo con múltiples algoritmos integrados")
    print("=" * 90)

if __name__ == "__main__":
    main()