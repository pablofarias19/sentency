#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICACIÓN COMPLETA DE LA MIGRACIÓN AL SISTEMA JUDICIAL
Comprueba que todo se implementó correctamente
"""

import os
from pathlib import Path
import sqlite3

BASE_DIR = Path('/home/user/sentency')
APP_DIR = BASE_DIR / 'App_colaborativa'
SCRIPTS_DIR = APP_DIR / 'colaborative' / 'scripts'
BASES_DIR = APP_DIR / 'colaborative' / 'bases_rag' / 'cognitiva'

# Colores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_section(title):
    print(f"\n{'='*70}")
    print(f"{BLUE}{title}{RESET}")
    print('='*70)

def check_item(condition, message):
    if condition:
        print(f"{GREEN}✓{RESET} {message}")
        return True
    else:
        print(f"{RED}✗{RESET} {message}")
        return False

def warn_item(message):
    print(f"{YELLOW}⚠{RESET} {message}")

# ============================================================================
# 1. VERIFICAR ELIMINACIÓN DE ARCHIVOS DE AUTORES
# ============================================================================

def verificar_archivos_autores_eliminados():
    print_section("1. VERIFICACIÓN: Archivos de Autores Eliminados")

    archivos_autor = [
        'sistema_autor_centrico.py',
        'visualizador_autor_centrico.py',
        'comparador_mentes.py',
        'gestor_unificado_autores.py',
        'detector_autor_y_metodo.py',
        'agregar_nuevo_autor.py',
        'verificar_autores.py',
        'analizador_perfiles.py',
        'ingesta_cognitiva.py',
        'ingesta_cognitiva_v3.py',
    ]

    todos_eliminados = True
    for archivo in archivos_autor:
        ruta = SCRIPTS_DIR / archivo
        if not ruta.exists():
            check_item(True, f"{archivo} - ELIMINADO")
        else:
            check_item(False, f"{archivo} - TODAVÍA EXISTE (debería eliminarse)")
            todos_eliminados = False

    return todos_eliminados

# ============================================================================
# 2. VERIFICAR BASES DE DATOS
# ============================================================================

def verificar_bases_datos():
    print_section("2. VERIFICACIÓN: Bases de Datos")

    # Bases que NO deben existir (autores)
    print("\nBases de autores (deben estar eliminadas):")
    bases_autor = [
        'autor_centrico.db',
        'perfiles_autorales.db',
        'multicapa_pensamiento.db',
        'pensamiento_integrado_v2.db',
    ]

    autor_ok = True
    for bd in bases_autor:
        ruta = BASES_DIR / bd
        if not ruta.exists():
            check_item(True, f"{bd} - ELIMINADA")
        else:
            check_item(False, f"{bd} - TODAVÍA EXISTE (debería eliminarse)")
            autor_ok = False

    # Base que DEBE existir (judicial)
    print("\nBase de datos judicial (debe existir):")
    bd_judicial = BASES_DIR / 'juez_centrico_arg.db'

    judicial_ok = False
    if bd_judicial.exists():
        check_item(True, f"juez_centrico_arg.db - EXISTE")

        # Verificar estructura
        try:
            conn = sqlite3.connect(bd_judicial)
            cursor = conn.cursor()

            # Verificar tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = [row[0] for row in cursor.fetchall()]

            tablas_esperadas = [
                'jueces_argentinos',
                'sentencias_argentinas',
                'analisis_pensamiento_judicial',
                'perfiles_judiciales_argentinos',
                'contexto_judicial_argentino'
            ]

            print("\n  Tablas en la base de datos:")
            for tabla in tablas_esperadas:
                if tabla in tablas:
                    check_item(True, f"    Tabla '{tabla}' presente")
                else:
                    check_item(False, f"    Tabla '{tabla}' FALTA")

            conn.close()
            judicial_ok = True
        except Exception as e:
            warn_item(f"Error verificando estructura de BD: {e}")
    else:
        check_item(False, f"juez_centrico_arg.db - NO EXISTE (crear con inicializar_bd_judicial.py)")

    return autor_ok and judicial_ok

# ============================================================================
# 3. VERIFICAR ARCHIVOS JUDICIALES NUEVOS
# ============================================================================

def verificar_archivos_judiciales():
    print_section("3. VERIFICACIÓN: Archivos del Sistema Judicial")

    archivos_judiciales = {
        # Fase 1
        'inicializar_bd_judicial.py': 'Fase 1 - Inicialización BD',
        'ingesta_sentencias_judicial.py': 'Fase 1 - Ingesta',
        'extractor_metadata_argentina.py': 'Fase 1 - Extractor metadata',

        # Fase 2
        'analizador_pensamiento_judicial_arg.py': 'Fase 2 - Análisis pensamiento',
        'procesador_sentencias_completo.py': 'Fase 2 - Procesador',
        'agregador_perfiles_jueces.py': 'Fase 2 - Agregador perfiles',

        # Fase 3
        'analizador_lineas_jurisprudenciales.py': 'Fase 3 - Líneas',
        'extractor_citas_jurisprudenciales.py': 'Fase 3 - Citas',
        'analizador_redes_influencia.py': 'Fase 3 - Redes',

        # Fase 4
        'motor_predictivo_judicial.py': 'Fase 4 - Predictivo',

        # Fase 5
        'generador_informes_judicial.py': 'Fase 5 - Informes',
        'sistema_preguntas_judiciales.py': 'Fase 5 - Preguntas',
        'motor_respuestas_judiciales.py': 'Fase 5 - Respuestas',

        # Adaptador
        'analyser_judicial_adapter.py': 'Adaptador ANALYSER-Judicial',
        'webapp_rutas_judicial.py': 'Rutas Flask judiciales',
    }

    todos_presentes = True
    for archivo, descripcion in archivos_judiciales.items():
        ruta = SCRIPTS_DIR / archivo
        if ruta.exists():
            check_item(True, f"{archivo} - {descripcion}")
        else:
            check_item(False, f"{archivo} - FALTA ({descripcion})")
            todos_presentes = False

    return todos_presentes

# ============================================================================
# 4. VERIFICAR INFRAESTRUCTURA CORE MANTENIDA
# ============================================================================

def verificar_infraestructura_core():
    print_section("4. VERIFICACIÓN: Infraestructura Core Mantenida")

    archivos_core = {
        'analyser_metodo_mejorado.py': 'ANALYSER v2.0 (100+ patrones)',
        'chunker_inteligente.py': 'Chunking inteligente',
        'embeddings_fusion.py': 'Sistema de embeddings',
        'extractor_pdf_enriquecido.py': 'Extracción PDF',
        'analizador_enriquecido_rag.py': 'Sistema RAG',
        'end2end_webapp.py': 'Webapp principal',
    }

    todos_presentes = True
    for archivo, descripcion in archivos_core.items():
        ruta = SCRIPTS_DIR / archivo
        if ruta.exists():
            check_item(True, f"{archivo} - {descripcion}")
        else:
            check_item(False, f"{archivo} - FALTA ({descripcion})")
            todos_presentes = False

    return todos_presentes

# ============================================================================
# 5. VERIFICAR WEBAPP INTEGRADA
# ============================================================================

def verificar_webapp_integrada():
    print_section("5. VERIFICACIÓN: Webapp con Rutas Judiciales")

    webapp_path = SCRIPTS_DIR / 'end2end_webapp.py'

    if not webapp_path.exists():
        check_item(False, "end2end_webapp.py NO EXISTE")
        return False

    with open(webapp_path, 'r', encoding='utf-8') as f:
        contenido = f.read()

    checks = {
        'from webapp_rutas_judicial import': 'Import de rutas judiciales',
        'registrar_rutas_judicial': 'Registro de rutas judiciales',
        'init_sistema_judicial': 'Inicialización sistema judicial',
    }

    todos_ok = True
    for check, descripcion in checks.items():
        if check in contenido:
            check_item(True, f"{descripcion}")
        else:
            check_item(False, f"{descripcion} - FALTA")
            todos_ok = False

    return todos_ok

# ============================================================================
# 6. VERIFICAR LIMPIEZA DEL DIRECTORIO RAÍZ
# ============================================================================

def verificar_limpieza_directorio_raiz():
    print_section("6. VERIFICACIÓN: Limpieza Directorio Raíz")

    archivos_py = list(APP_DIR.glob('*.py'))

    archivos_permitidos = {
        'limpiar_sistema_autores.py',
        'integrar_sistema_judicial.py',
        'limpieza_final_repositorio.py',
    }

    print(f"\nArchivos Python en App_colaborativa/: {len(archivos_py)}")

    todos_ok = True
    for archivo in archivos_py:
        if archivo.name in archivos_permitidos:
            check_item(True, f"{archivo.name} - Script de utilidad (OK)")
        else:
            check_item(False, f"{archivo.name} - Archivo obsoleto (debería eliminarse)")
            todos_ok = False

    if len(archivos_py) == 3:
        check_item(True, f"Solo {len(archivos_py)} archivos de utilidad (correcto)")
    elif len(archivos_py) < 3:
        warn_item(f"Solo {len(archivos_py)} archivos (faltan scripts de utilidad)")
    else:
        check_item(False, f"{len(archivos_py)} archivos (deberían ser 3)")
        todos_ok = False

    return todos_ok

# ============================================================================
# 7. VERIFICAR DOCUMENTACIÓN
# ============================================================================

def verificar_documentacion():
    print_section("7. VERIFICACIÓN: Documentación")

    docs = {
        'README.md': 'Guía principal del sistema',
        'PLAN_MIGRACION_SISTEMA_JUDICIAL.md': 'Plan de migración',
        'LIMPIEZA_FINAL.md': 'Documentación de limpieza',
        'PASOS_FINALES.md': 'Pasos finales',
    }

    # README en raíz
    readme_raiz = BASE_DIR / 'README.md'
    if readme_raiz.exists():
        check_item(True, f"README.md en raíz")
    else:
        check_item(False, f"README.md en raíz - FALTA")

    # Otros docs
    todos_ok = True
    for doc, descripcion in docs.items():
        if doc == 'README.md':
            continue

        ruta = BASE_DIR / doc
        if ruta.exists():
            check_item(True, f"{doc} - {descripcion}")
        else:
            warn_item(f"{doc} - NO EXISTE ({descripcion})")

    # Docs de fases en App_colaborativa
    print("\nDocumentación de Fases:")
    for i in range(1, 6):
        doc = APP_DIR / f'FASE{i}_README.md'
        if doc.exists():
            check_item(True, f"FASE{i}_README.md")
        else:
            warn_item(f"FASE{i}_README.md - NO EXISTE")

    return todos_ok

# ============================================================================
# 8. VERIFICAR SCHEMA SQL
# ============================================================================

def verificar_schema_sql():
    print_section("8. VERIFICACIÓN: Schema SQL Judicial")

    schema_path = SCRIPTS_DIR / 'schema_juez_centrico_arg.sql'

    if schema_path.exists():
        check_item(True, "schema_juez_centrico_arg.sql - EXISTE")

        with open(schema_path, 'r', encoding='utf-8') as f:
            contenido = f.read()

        tablas = [
            'jueces_argentinos',
            'sentencias_argentinas',
            'analisis_pensamiento_judicial',
            'perfiles_judiciales_argentinos',
            'contexto_judicial_argentino'
        ]

        print("\n  Tablas definidas en schema:")
        for tabla in tablas:
            if tabla in contenido:
                check_item(True, f"    CREATE TABLE {tabla}")
            else:
                check_item(False, f"    CREATE TABLE {tabla} - FALTA")

        return True
    else:
        check_item(False, "schema_juez_centrico_arg.sql - NO EXISTE")
        return False

# ============================================================================
# 9. ESTADÍSTICAS FINALES
# ============================================================================

def generar_estadisticas():
    print_section("9. ESTADÍSTICAS DEL REPOSITORIO")

    # Contar archivos Python
    scripts_totales = len(list(SCRIPTS_DIR.glob('*.py')))
    raiz_totales = len(list(APP_DIR.glob('*.py')))

    # Contar archivos judiciales
    judiciales = len(list(SCRIPTS_DIR.glob('*judicial*.py')))

    # Contar bases de datos
    bases = list(BASES_DIR.glob('*.db'))

    print(f"\n📊 Archivos Python:")
    print(f"   Scripts en colaborative/scripts/: {scripts_totales}")
    print(f"   Scripts judiciales: {judiciales}")
    print(f"   Scripts en App_colaborativa/: {raiz_totales}")

    print(f"\n📊 Bases de Datos:")
    for bd in bases:
        size_mb = bd.stat().st_size / (1024 * 1024)
        print(f"   {bd.name}: {size_mb:.2f} MB")

    print(f"\n📊 Documentación:")
    docs_totales = len(list(BASE_DIR.glob('*.md'))) + len(list(APP_DIR.glob('*.md')))
    print(f"   Archivos Markdown: {docs_totales}")

# ============================================================================
# REPORTE FINAL
# ============================================================================

def generar_reporte_final(resultados):
    print_section("REPORTE FINAL DE VERIFICACIÓN")

    total = len(resultados)
    exitosos = sum(resultados.values())
    porcentaje = (exitosos / total) * 100

    print(f"\n{'='*70}")
    for check, resultado in resultados.items():
        simbolo = f"{GREEN}✓{RESET}" if resultado else f"{RED}✗{RESET}"
        print(f"{simbolo} {check}")

    print(f"\n{'='*70}")
    print(f"Verificaciones exitosas: {exitosos}/{total} ({porcentaje:.1f}%)")
    print(f"{'='*70}")

    if exitosos == total:
        print(f"\n{GREEN}🎉 ¡MIGRACIÓN COMPLETADA AL 100%!{RESET}")
        print(f"{GREEN}El sistema está completamente migrado y optimizado.{RESET}")
    elif porcentaje >= 80:
        print(f"\n{YELLOW}⚠️  Migración casi completa ({porcentaje:.1f}%){RESET}")
        print(f"{YELLOW}Revisa los puntos marcados con ✗{RESET}")
    else:
        print(f"\n{RED}❌ Migración incompleta ({porcentaje:.1f}%){RESET}")
        print(f"{RED}Hay varios problemas que resolver.{RESET}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "="*70)
    print(f"{BLUE}VERIFICACIÓN COMPLETA DE LA MIGRACIÓN AL SISTEMA JUDICIAL{RESET}")
    print("="*70)
    print("\nComprobando todos los cambios implementados...\n")

    resultados = {}

    # Ejecutar verificaciones
    resultados['Archivos de autores eliminados'] = verificar_archivos_autores_eliminados()
    resultados['Bases de datos correctas'] = verificar_bases_datos()
    resultados['Archivos judiciales presentes'] = verificar_archivos_judiciales()
    resultados['Infraestructura core mantenida'] = verificar_infraestructura_core()
    resultados['Webapp integrada'] = verificar_webapp_integrada()
    resultados['Directorio raíz limpio'] = verificar_limpieza_directorio_raiz()
    resultados['Documentación presente'] = verificar_documentacion()
    resultados['Schema SQL correcto'] = verificar_schema_sql()

    # Estadísticas
    generar_estadisticas()

    # Reporte final
    generar_reporte_final(resultados)

    print(f"\n{'='*70}")
    print("Verificación completada.")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
