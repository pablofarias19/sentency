#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE MIGRACIÓN DEL SISTEMA JUDICIAL AL REPOSITORIO ORIGINAL

Este script te ayuda a migrar de forma controlada y segura.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import sys

# Colores
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

ESTE_REPO = Path('/home/user/sentency')

# ============================================================================
# ARCHIVOS A MIGRAR
# ============================================================================

ARCHIVOS_JUDICIALES_SCRIPTS = [
    # Fase 1
    'inicializar_bd_judicial.py',
    'ingesta_sentencias_judicial.py',
    'extractor_metadata_argentina.py',
    'schema_juez_centrico_arg.sql',

    # Fase 2
    'analizador_pensamiento_judicial_arg.py',
    'procesador_sentencias_completo.py',
    'agregador_perfiles_jueces.py',

    # Fase 3
    'analizador_lineas_jurisprudenciales.py',
    'extractor_citas_jurisprudenciales.py',
    'analizador_redes_influencia.py',

    # Fase 4
    'motor_predictivo_judicial.py',

    # Fase 5
    'generador_informes_judicial.py',
    'sistema_preguntas_judiciales.py',
    'motor_respuestas_judiciales.py',

    # Adaptador y webapp
    'analyser_judicial_adapter.py',
    'webapp_rutas_judicial.py',
]

ARCHIVOS_UTILIDAD_RAIZ = [
    'limpiar_sistema_autores.py',
    'integrar_sistema_judicial.py',
    'limpieza_final_repositorio.py',
]

DOCUMENTACION = [
    'README.md',  # En raíz del repo
    'PLAN_MIGRACION_SISTEMA_JUDICIAL.md',
    'LIMPIEZA_FINAL.md',
    'PASOS_FINALES.md',
    'GUIA_MIGRACION_A_ORIGINAL.md',
]

DOCUMENTACION_FASES = [
    'FASE1_README.md',
    'FASE2_README.md',
    'FASE3_README.md',
    'FASE4_README.md',
    'FASE5_README.md',
    'PROPUESTA_AJUSTADA_JUECES_ARG.md',
]

# ============================================================================
# FUNCIONES
# ============================================================================

def print_section(title):
    print(f"\n{'='*70}")
    print(f"{BLUE}{title}{RESET}")
    print('='*70)

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def confirmar(pregunta):
    """Pide confirmación al usuario"""
    respuesta = input(f"\n{pregunta} (SI/no): ")
    return respuesta.strip().upper() in ['SI', 'S', 'YES', 'Y', '']

def crear_backup(repo_original):
    """Crea backup del repositorio original"""
    print_section("PASO 1: Crear Backup del Original")

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = repo_original.parent / f"{repo_original.name}_backup_{timestamp}"

    print(f"\nCreando backup en: {backup_dir}")

    try:
        shutil.copytree(repo_original, backup_dir)
        print_success(f"Backup creado exitosamente")
        print(f"  Ubicación: {backup_dir}")
        return backup_dir
    except Exception as e:
        print_error(f"Error creando backup: {e}")
        return None

def analizar_original(repo_original):
    """Analiza el repositorio original"""
    print_section("PASO 2: Analizar Repositorio Original")

    app_dir = repo_original / 'App_colaborativa'

    if not app_dir.exists():
        print_error(f"No se encontró App_colaborativa/ en {repo_original}")
        return False

    scripts_dir = app_dir / 'colaborative' / 'scripts'

    if not scripts_dir.exists():
        print_error(f"No se encontró colaborative/scripts/ en {repo_original}")
        return False

    # Contar archivos
    archivos_raiz = list(app_dir.glob('*.py'))
    archivos_scripts = list(scripts_dir.glob('*.py'))

    print(f"\n📊 Estadísticas del original:")
    print(f"   Archivos Python en raíz: {len(archivos_raiz)}")
    print(f"   Archivos Python en scripts/: {len(archivos_scripts)}")

    # Buscar archivos de autores
    archivos_autor = [f for f in archivos_scripts if 'autor' in f.name.lower()]
    if archivos_autor:
        print_warning(f"\nArchivos de autores encontrados: {len(archivos_autor)}")
        print("  Estos serán eliminados durante la migración:")
        for f in archivos_autor[:5]:
            print(f"    - {f.name}")
        if len(archivos_autor) > 5:
            print(f"    ... y {len(archivos_autor) - 5} más")

    # Buscar archivos únicos (que no están en este repo)
    scripts_este = ESTE_REPO / 'App_colaborativa' / 'colaborative' / 'scripts'
    archivos_unicos = []

    for f in archivos_scripts:
        archivo_este = scripts_este / f.name
        if not archivo_este.exists() and 'autor' not in f.name.lower():
            archivos_unicos.append(f.name)

    if archivos_unicos:
        print_warning(f"\nArchivos únicos en el original (no están en este repo): {len(archivos_unicos)}")
        print("  Estos NO serán eliminados:")
        for f in archivos_unicos[:5]:
            print(f"    - {f}")
        if len(archivos_unicos) > 5:
            print(f"    ... y {len(archivos_unicos) - 5} más")

    return True

def eliminar_archivos_autores(repo_original):
    """Elimina archivos específicos de autores"""
    print_section("PASO 3: Eliminar Archivos de Autores")

    scripts_dir = repo_original / 'App_colaborativa' / 'colaborative' / 'scripts'

    archivos_a_eliminar = [
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
        'ingesta_enriquecida.py',
        'motor_ingesta_pensamiento.py',
    ]

    eliminados = 0

    for archivo in archivos_a_eliminar:
        ruta = scripts_dir / archivo
        if ruta.exists():
            try:
                os.remove(ruta)
                print_success(f"Eliminado: {archivo}")
                eliminados += 1
            except Exception as e:
                print_error(f"Error eliminando {archivo}: {e}")

    print(f"\n{eliminados} archivos de autores eliminados")
    return eliminados

def eliminar_bases_datos_autores(repo_original):
    """Elimina bases de datos de autores"""
    print_section("PASO 4: Eliminar Bases de Datos de Autores")

    bases_dir = repo_original / 'App_colaborativa' / 'colaborative' / 'bases_rag' / 'cognitiva'

    if not bases_dir.exists():
        print_warning("Directorio de bases de datos no encontrado")
        return 0

    bases_a_eliminar = [
        'autor_centrico.db',
        'perfiles_autorales.db',
        'multicapa_pensamiento.db',
        'pensamiento_integrado_v2.db',
    ]

    eliminados = 0

    for bd in bases_a_eliminar:
        ruta = bases_dir / bd
        if ruta.exists():
            try:
                os.remove(ruta)
                print_success(f"Eliminada: {bd}")
                eliminados += 1
            except Exception as e:
                print_error(f"Error eliminando {bd}: {e}")

    print(f"\n{eliminados} bases de datos de autores eliminadas")
    return eliminados

def copiar_archivos_judiciales(repo_original):
    """Copia archivos del sistema judicial"""
    print_section("PASO 5: Copiar Archivos del Sistema Judicial")

    scripts_origen = ESTE_REPO / 'App_colaborativa' / 'colaborative' / 'scripts'
    scripts_destino = repo_original / 'App_colaborativa' / 'colaborative' / 'scripts'

    copiados = 0
    actualizados = 0

    for archivo in ARCHIVOS_JUDICIALES_SCRIPTS:
        origen = scripts_origen / archivo
        destino = scripts_destino / archivo

        if not origen.exists():
            print_warning(f"No encontrado en origen: {archivo}")
            continue

        try:
            if destino.exists():
                shutil.copy2(origen, destino)
                print_success(f"Actualizado: {archivo}")
                actualizados += 1
            else:
                shutil.copy2(origen, destino)
                print_success(f"Copiado: {archivo}")
                copiados += 1
        except Exception as e:
            print_error(f"Error con {archivo}: {e}")

    print(f"\nArchivos copiados: {copiados}")
    print(f"Archivos actualizados: {actualizados}")

    return copiados + actualizados

def copiar_scripts_utilidad(repo_original):
    """Copia scripts de utilidad a la raíz"""
    print_section("PASO 6: Copiar Scripts de Utilidad")

    origen_dir = ESTE_REPO / 'App_colaborativa'
    destino_dir = repo_original / 'App_colaborativa'

    copiados = 0

    for archivo in ARCHIVOS_UTILIDAD_RAIZ:
        origen = origen_dir / archivo
        destino = destino_dir / archivo

        if origen.exists():
            try:
                shutil.copy2(origen, destino)
                print_success(f"Copiado: {archivo}")
                copiados += 1
            except Exception as e:
                print_error(f"Error con {archivo}: {e}")

    print(f"\n{copiados} scripts de utilidad copiados")
    return copiados

def copiar_documentacion(repo_original):
    """Copia documentación"""
    print_section("PASO 7: Copiar Documentación")

    copiados = 0

    # Docs en raíz del repo
    for doc in DOCUMENTACION:
        origen = ESTE_REPO / doc
        destino = repo_original / doc

        if origen.exists():
            try:
                shutil.copy2(origen, destino)
                print_success(f"Copiado: {doc}")
                copiados += 1
            except Exception as e:
                print_error(f"Error con {doc}: {e}")

    # Docs de fases en App_colaborativa
    for doc in DOCUMENTACION_FASES:
        origen = ESTE_REPO / 'App_colaborativa' / doc
        destino = repo_original / 'App_colaborativa' / doc

        if origen.exists():
            try:
                shutil.copy2(origen, destino)
                print_success(f"Copiado: {doc}")
                copiados += 1
            except Exception as e:
                print_error(f"Error con {doc}: {e}")

    print(f"\n{copiados} archivos de documentación copiados")
    return copiados

def integrar_webapp(repo_original):
    """Integra las rutas judiciales en la webapp"""
    print_section("PASO 8: Integrar Webapp con Rutas Judiciales")

    script_integrador = repo_original / 'App_colaborativa' / 'integrar_sistema_judicial.py'

    if not script_integrador.exists():
        print_error("Script integrador no encontrado")
        return False

    print("\n¿Ejecutar script de integración de webapp?")
    print("Esto modificará end2end_webapp.py para agregar rutas judiciales.")

    if confirmar("¿Continuar?"):
        try:
            import subprocess
            result = subprocess.run(
                ['python', str(script_integrador)],
                cwd=str(repo_original / 'App_colaborativa'),
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print_success("Webapp integrada exitosamente")
                return True
            else:
                print_error(f"Error integrando webapp: {result.stderr}")
                return False
        except Exception as e:
            print_error(f"Error ejecutando integración: {e}")
            return False
    else:
        print_warning("Integración de webapp omitida")
        return False

def generar_reporte(repo_original, stats):
    """Genera reporte final de la migración"""
    print_section("REPORTE FINAL DE MIGRACIÓN")

    print(f"\n📊 Estadísticas:")
    print(f"   Archivos de autores eliminados: {stats['archivos_eliminados']}")
    print(f"   Bases de datos eliminadas: {stats['bases_eliminadas']}")
    print(f"   Archivos judiciales copiados: {stats['judiciales_copiados']}")
    print(f"   Scripts de utilidad copiados: {stats['utilidad_copiados']}")
    print(f"   Documentación copiada: {stats['docs_copiados']}")
    print(f"   Webapp integrada: {'Sí' if stats['webapp_integrada'] else 'No'}")

    print(f"\n📁 Ubicaciones:")
    print(f"   Repositorio original: {repo_original}")
    print(f"   Backup creado en: {stats['backup_dir']}")

    print(f"\n✅ MIGRACIÓN COMPLETADA")

    print(f"\n🔍 Verificación recomendada:")
    print(f"   cd {repo_original}")
    print(f"   python verificar_migracion_completa.py")

    print(f"\n🚀 Iniciar sistema:")
    print(f"   cd {repo_original}/App_colaborativa/colaborative/scripts")
    print(f"   python inicializar_bd_judicial.py")
    print(f"   python end2end_webapp.py")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "="*70)
    print(f"{BLUE}MIGRACIÓN DEL SISTEMA JUDICIAL AL REPOSITORIO ORIGINAL{RESET}")
    print("="*70)

    # Solicitar ruta del repositorio original
    if len(sys.argv) > 1:
        repo_original = Path(sys.argv[1])
    else:
        ruta = input("\nRuta del repositorio original: ").strip()
        repo_original = Path(ruta)

    if not repo_original.exists():
        print_error(f"Repositorio no encontrado: {repo_original}")
        sys.exit(1)

    print(f"\nRepositorio original: {repo_original}")
    print(f"Este repositorio: {ESTE_REPO}")

    # Confirmar
    if not confirmar("\n¿Continuar con la migración?"):
        print("\n❌ Migración cancelada")
        sys.exit(0)

    stats = {
        'backup_dir': None,
        'archivos_eliminados': 0,
        'bases_eliminadas': 0,
        'judiciales_copiados': 0,
        'utilidad_copiados': 0,
        'docs_copiados': 0,
        'webapp_integrada': False,
    }

    # Ejecutar pasos

    # 1. Backup
    stats['backup_dir'] = crear_backup(repo_original)
    if not stats['backup_dir']:
        print_error("No se pudo crear backup. Abortando.")
        sys.exit(1)

    # 2. Analizar
    if not analizar_original(repo_original):
        print_error("Error analizando repositorio original. Abortando.")
        sys.exit(1)

    if not confirmar("\n¿Proceder con los cambios?"):
        print("\n❌ Migración cancelada")
        sys.exit(0)

    # 3. Eliminar archivos de autores
    stats['archivos_eliminados'] = eliminar_archivos_autores(repo_original)

    # 4. Eliminar bases de datos de autores
    stats['bases_eliminadas'] = eliminar_bases_datos_autores(repo_original)

    # 5. Copiar archivos judiciales
    stats['judiciales_copiados'] = copiar_archivos_judiciales(repo_original)

    # 6. Copiar scripts de utilidad
    stats['utilidad_copiados'] = copiar_scripts_utilidad(repo_original)

    # 7. Copiar documentación
    stats['docs_copiados'] = copiar_documentacion(repo_original)

    # 8. Integrar webapp
    stats['webapp_integrada'] = integrar_webapp(repo_original)

    # 9. Copiar script de verificación
    script_verif_origen = ESTE_REPO / 'verificar_migracion_completa.py'
    script_verif_destino = repo_original / 'verificar_migracion_completa.py'
    if script_verif_origen.exists():
        shutil.copy2(script_verif_origen, script_verif_destino)
        print_success("Script de verificación copiado")

    # Reporte final
    generar_reporte(repo_original, stats)

if __name__ == "__main__":
    main()
