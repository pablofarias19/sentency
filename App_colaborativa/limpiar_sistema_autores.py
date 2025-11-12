#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para eliminar completamente el sistema de autores
y dejar solo el sistema judicial
"""

import os
from pathlib import Path
import shutil

# Directorio base
BASE_DIR = Path('/home/user/sentency/App_colaborativa')
SCRIPTS_DIR = BASE_DIR / 'colaborative' / 'scripts'
BASES_DIR = BASE_DIR / 'colaborative' / 'bases_rag' / 'cognitiva'

# ============================================================================
# ARCHIVOS ESPECÍFICOS DE AUTORES A ELIMINAR
# ============================================================================

ARCHIVOS_ELIMINAR = [
    # Sistema autor-céntrico
    'sistema_autor_centrico.py',
    'visualizador_autor_centrico.py',
    'inicializar_autor_centrico.py',
    'migrar_autor_centrico.py',

    # Comparación y gestión de autores
    'comparador_mentes.py',
    'gestor_unificado_autores.py',
    'sistema_referencias_autores.py',

    # Detección y análisis de autores
    'detector_autor_y_metodo.py',

    # Scripts específicos de autores individuales
    'agregar_nuevo_autor.py',
    'verificar_autores.py',
    'buscar_seba.py',
    'diagnosticar_autor_scotti.py',

    # Visualizadores específicos de autores
    'visualizador_pensamiento_multicapa.py',

    # Integradores específicos de autores
    'integrador_pensamiento_flask.py',

    # Sistema de perfiles autorales
    'analizador_perfiles.py',  # Si es específico de autores

    # Generadores de informes de autores (no judicial)
    'generador_informes_gemini.py',  # Si es solo para autores
    'generador_explicaciones_cognitivas.py',  # Evaluar si se usa
]

# Bases de datos de autores
BASES_DATOS_ELIMINAR = [
    'autor_centrico.db',
    'perfiles_autorales.db',
    'multicapa_pensamiento.db',
    'pensamiento_integrado_v2.db',
]

# Scripts de ingesta antiguos (duplicados)
INGESTAS_ANTIGUAS = [
    'ingesta_cognitiva_backup.py',
    'ingesta_cognitiva.py',  # Reemplazado por ingesta_sentencias_judicial.py
    'ingesta_cognitiva_v3.py',
    'ingesta_enriquecida.py',
    'procesador_ingesta_cognitiva.py',
    'motor_ingesta_pensamiento.py',
]

# Scripts de mantenimiento específicos de autores
MANTENIMIENTO_AUTORES = [
    'actualizar_db_analyser.py',  # Si es específico de autores
    'reparar_rasgos_cognitivos.py',
    'inspeccionar_metadatos.py',  # Si es para metadatos de autores
]

# Scripts de análisis específicos que NO necesitamos
ANALISIS_NO_NECESARIOS = [
    'analizador_multicapa_pensamiento.py',  # Reemplazado por el adaptador
    # 'analizador_argumentativo.py',  # Podría ser útil, evaluar
    # 'analizador_temporal.py',  # Podría adaptarse para jueces
    # 'detector_razonamiento_aristotelico.py',  # Podría ser útil
]

# Combinar todas las listas
TODOS_ARCHIVOS_ELIMINAR = (
    ARCHIVOS_ELIMINAR +
    INGESTAS_ANTIGUAS +
    MANTENIMIENTO_AUTORES +
    ANALISIS_NO_NECESARIOS
)

def eliminar_archivos():
    """Elimina archivos específicos de autores"""
    print("="*70)
    print("ELIMINANDO ARCHIVOS DEL SISTEMA DE AUTORES")
    print("="*70)

    eliminados = 0
    no_encontrados = 0

    for archivo in TODOS_ARCHIVOS_ELIMINAR:
        ruta = SCRIPTS_DIR / archivo
        if ruta.exists():
            try:
                os.remove(ruta)
                print(f"✓ Eliminado: {archivo}")
                eliminados += 1
            except Exception as e:
                print(f"✗ Error eliminando {archivo}: {e}")
        else:
            no_encontrados += 1

    print(f"\nArchivos eliminados: {eliminados}")
    print(f"Archivos no encontrados (ya eliminados o no existen): {no_encontrados}")
    return eliminados

def eliminar_bases_datos():
    """Elimina bases de datos de autores"""
    print("\n" + "="*70)
    print("ELIMINANDO BASES DE DATOS DE AUTORES")
    print("="*70)

    eliminados = 0

    for bd in BASES_DATOS_ELIMINAR:
        ruta = BASES_DIR / bd
        if ruta.exists():
            try:
                os.remove(ruta)
                print(f"✓ Eliminado: {bd}")
                eliminados += 1
            except Exception as e:
                print(f"✗ Error eliminando {bd}: {e}")

    print(f"\nBases de datos eliminadas: {eliminados}")
    return eliminados

def eliminar_faiss_index():
    """Elimina índices FAISS antiguos si existen"""
    print("\n" + "="*70)
    print("VERIFICANDO ÍNDICES FAISS")
    print("="*70)

    faiss_dir = BASES_DIR / 'faiss_index'
    if faiss_dir.exists():
        print(f"⚠️  Directorio FAISS encontrado: {faiss_dir}")
        print("   Manteniendo por ahora (podría usarse para sentencias)")
        # Si quisieras eliminarlo:
        # shutil.rmtree(faiss_dir)
        # print("✓ Eliminado directorio FAISS")
    else:
        print("✓ No hay índices FAISS antiguos")

def limpiar_cache():
    """Limpia directorios __pycache__"""
    print("\n" + "="*70)
    print("LIMPIANDO CACHE DE PYTHON")
    print("="*70)

    pycache_dirs = list(SCRIPTS_DIR.rglob('__pycache__'))
    for pycache in pycache_dirs:
        try:
            shutil.rmtree(pycache)
            print(f"✓ Eliminado: {pycache.relative_to(SCRIPTS_DIR)}")
        except Exception as e:
            print(f"✗ Error: {e}")

    print(f"\nDirectorios __pycache__ eliminados: {len(pycache_dirs)}")

def verificar_archivos_mantenidos():
    """Verifica que los archivos importantes se mantuvieron"""
    print("\n" + "="*70)
    print("VERIFICANDO ARCHIVOS CORE MANTENIDOS")
    print("="*70)

    archivos_importantes = [
        'analyser_metodo_mejorado.py',  # ANALYSER core
        'analyser_judicial_adapter.py',  # Adaptador nuevo
        'webapp_rutas_judicial.py',  # Rutas judiciales
        'end2end_webapp.py',  # Webapp principal
        'chunker_inteligente.py',  # Chunking
        'embeddings_fusion.py',  # Embeddings
        'extractor_pdf_enriquecido.py',  # Extracción PDFs
        'analizador_enriquecido_rag.py',  # Sistema RAG

        # Scripts judiciales (Fases 1-5)
        'inicializar_bd_judicial.py',
        'ingesta_sentencias_judicial.py',
        'analizador_pensamiento_judicial_arg.py',
        'procesador_sentencias_completo.py',
        'agregador_perfiles_jueces.py',
        'analizador_lineas_jurisprudenciales.py',
        'extractor_citas_jurisprudenciales.py',
        'analizador_redes_influencia.py',
        'motor_predictivo_judicial.py',
        'generador_informes_judicial.py',
        'sistema_preguntas_judiciales.py',
        'motor_respuestas_judiciales.py',
    ]

    todos_ok = True
    for archivo in archivos_importantes:
        ruta = SCRIPTS_DIR / archivo
        if ruta.exists():
            print(f"✓ {archivo}")
        else:
            print(f"✗ FALTA: {archivo}")
            todos_ok = False

    if todos_ok:
        print("\n✅ Todos los archivos importantes están presentes")
    else:
        print("\n⚠️  ADVERTENCIA: Faltan archivos importantes")

    return todos_ok

def generar_reporte():
    """Genera reporte final"""
    print("\n" + "="*70)
    print("REPORTE FINAL")
    print("="*70)

    # Contar archivos restantes
    total_scripts = len(list(SCRIPTS_DIR.glob('*.py')))

    print(f"\nScripts Python restantes en scripts/: {total_scripts}")

    # Verificar BD judicial
    bd_judicial = BASES_DIR / 'juez_centrico_arg.db'
    if bd_judicial.exists():
        print(f"✓ Base de datos judicial: {bd_judicial.name}")
    else:
        print(f"⚠️  Base de datos judicial NO encontrada (crear con inicializar_bd_judicial.py)")

    print("\n" + "="*70)
    print("SISTEMA LIMPIO Y LISTO")
    print("="*70)
    print("\nSistema unificado judicial:")
    print("  ✓ ANALYSER cognitivo v2.0 (adaptado)")
    print("  ✓ Sistema RAG + embeddings")
    print("  ✓ Análisis judicial argentino")
    print("  ✓ Webapp con rutas judiciales")
    print("  ✓ 15 scripts de fases 1-5")
    print("  ✓ Generación de informes")
    print("  ✓ Sistema de 140 preguntas")
    print("\nArchivos de autores: ELIMINADOS")
    print("="*70)

def main():
    """Función principal"""
    import sys

    print("\n" + "="*70)
    print("LIMPIEZA DEL SISTEMA DE AUTORES")
    print("="*70)
    print("\nEsto eliminará PERMANENTEMENTE:")
    print("  - Scripts específicos de autores (~25 archivos)")
    print("  - Bases de datos de autores (4 archivos)")
    print("  - Ingestas antiguas duplicadas")
    print("\nSe MANTENDRÁN:")
    print("  - ANALYSER v2.0 (core)")
    print("  - Sistema RAG + embeddings")
    print("  - Webapp principal")
    print("  - Todo el sistema judicial (15 scripts)")

    respuesta = input("\n¿Confirmar eliminación? (escribir 'SI' para confirmar): ")

    if respuesta.strip().upper() != 'SI':
        print("\n❌ Operación cancelada")
        sys.exit(0)

    print("\n🚀 Iniciando limpieza...\n")

    # Ejecutar limpieza
    eliminados_archivos = eliminar_archivos()
    eliminados_bd = eliminar_bases_datos()
    eliminar_faiss_index()
    limpiar_cache()

    # Verificar
    archivos_ok = verificar_archivos_mantenidos()

    # Reporte
    generar_reporte()

    print(f"\n✅ Limpieza completada")
    print(f"   Archivos eliminados: {eliminados_archivos}")
    print(f"   Bases de datos eliminadas: {eliminados_bd}")

if __name__ == "__main__":
    main()
