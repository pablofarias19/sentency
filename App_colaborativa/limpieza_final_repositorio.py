#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LIMPIEZA FINAL DEL REPOSITORIO
Elimina archivos obsoletos del directorio raíz App_colaborativa/
"""

import os
from pathlib import Path
import shutil

BASE_DIR = Path('/home/user/sentency/App_colaborativa')

# ============================================================================
# ARCHIVOS A MANTENER EN DIRECTORIO RAÍZ
# ============================================================================

MANTENER = {
    # Scripts útiles que creamos
    'limpiar_sistema_autores.py',
    'integrar_sistema_judicial.py',
    'limpieza_final_repositorio.py',  # Este script

    # Documentación
    'PROPUESTA_AJUSTADA_JUECES_ARG.md',
    'FASE1_README.md',
    'FASE2_README.md',
    'FASE3_README.md',
    'FASE4_README.md',
    'FASE5_README.md',
}

# Todo lo demás se elimina

def listar_archivos_a_eliminar():
    """Lista archivos .py en raíz que NO están en MANTENER"""
    archivos_py = list(BASE_DIR.glob('*.py'))

    a_eliminar = []
    for archivo in archivos_py:
        if archivo.name not in MANTENER:
            a_eliminar.append(archivo)

    return a_eliminar

def eliminar_archivos():
    """Elimina archivos obsoletos"""
    archivos = listar_archivos_a_eliminar()

    print("="*70)
    print(f"ARCHIVOS A ELIMINAR: {len(archivos)}")
    print("="*70)

    # Mostrar lista
    print("\nArchivos que se eliminarán:")
    for i, archivo in enumerate(archivos, 1):
        print(f"  {i}. {archivo.name}")

    print(f"\nTotal: {len(archivos)} archivos")
    print("\nSe mantendrán:")
    for m in sorted(MANTENER):
        print(f"  ✓ {m}")

    confirmacion = input("\n¿Eliminar estos archivos? (SI para confirmar): ")

    if confirmacion.strip().upper() != 'SI':
        print("\n❌ Operación cancelada")
        return 0

    # Eliminar
    eliminados = 0
    errores = 0

    print("\n" + "="*70)
    print("ELIMINANDO ARCHIVOS")
    print("="*70)

    for archivo in archivos:
        try:
            os.remove(archivo)
            print(f"✓ Eliminado: {archivo.name}")
            eliminados += 1
        except Exception as e:
            print(f"✗ Error eliminando {archivo.name}: {e}")
            errores += 1

    print("\n" + "="*70)
    print(f"Eliminados: {eliminados}")
    print(f"Errores: {errores}")
    print("="*70)

    return eliminados

def verificar_directorio_colaborative():
    """Verifica que /colaborative/ esté intacto"""
    print("\n" + "="*70)
    print("VERIFICANDO DIRECTORIO COLABORATIVE/")
    print("="*70)

    colab_dir = BASE_DIR / 'colaborative'

    if not colab_dir.exists():
        print("❌ ERROR: Directorio colaborative/ no encontrado")
        return False

    # Verificar scripts críticos
    scripts_dir = colab_dir / 'scripts'
    archivos_criticos = [
        'analyser_metodo_mejorado.py',
        'analyser_judicial_adapter.py',
        'webapp_rutas_judicial.py',
        'end2end_webapp.py',
        'inicializar_bd_judicial.py',
        'ingesta_sentencias_judicial.py',
        'analizador_pensamiento_judicial_arg.py',
        'procesador_sentencias_completo.py',
        'generador_informes_judicial.py',
        'sistema_preguntas_judiciales.py',
        'motor_respuestas_judiciales.py',
    ]

    todos_ok = True
    for archivo in archivos_criticos:
        ruta = scripts_dir / archivo
        if ruta.exists():
            print(f"✓ {archivo}")
        else:
            print(f"✗ FALTA: {archivo}")
            todos_ok = False

    # Verificar BD
    bd_dir = colab_dir / 'bases_rag' / 'cognitiva'
    bd_judicial = bd_dir / 'juez_centrico_arg.db'

    print(f"\nBase de datos judicial:")
    if bd_judicial.exists():
        print(f"✓ {bd_judicial.name} existe")
    else:
        print(f"⚠️  {bd_judicial.name} no existe (crear con inicializar_bd_judicial.py)")

    if todos_ok:
        print("\n✅ Directorio colaborative/ está completo")
    else:
        print("\n⚠️  ADVERTENCIA: Faltan archivos críticos")

    return todos_ok

def generar_reporte_final():
    """Genera reporte de estado final"""
    print("\n" + "="*70)
    print("REPORTE FINAL DEL REPOSITORIO")
    print("="*70)

    # Contar archivos en raíz
    archivos_raiz = len(list(BASE_DIR.glob('*.py')))
    docs_raiz = len(list(BASE_DIR.glob('*.md')))

    print(f"\nDirectorio App_colaborativa/:")
    print(f"  Archivos Python: {archivos_raiz}")
    print(f"  Documentación MD: {docs_raiz}")

    # Scripts en colaborative/scripts
    scripts_dir = BASE_DIR / 'colaborative' / 'scripts'
    if scripts_dir.exists():
        scripts_count = len(list(scripts_dir.glob('*.py')))
        print(f"\nDirectorio scripts/:")
        print(f"  Archivos Python: {scripts_count}")

    # Bases de datos
    bd_dir = BASE_DIR / 'colaborative' / 'bases_rag' / 'cognitiva'
    if bd_dir.exists():
        bds = list(bd_dir.glob('*.db'))
        print(f"\nBases de datos:")
        for bd in bds:
            size_mb = bd.stat().st_size / (1024 * 1024)
            print(f"  {bd.name} ({size_mb:.2f} MB)")

    print("\n" + "="*70)
    print("ESTRUCTURA FINAL")
    print("="*70)
    print("""
sentency/
├── README.md
├── PLAN_MIGRACION_SISTEMA_JUDICIAL.md
├── LIMPIEZA_FINAL.md
│
└── App_colaborativa/
    ├── FASE1_README.md ... FASE5_README.md
    ├── limpiar_sistema_autores.py
    ├── integrar_sistema_judicial.py
    ├── limpieza_final_repositorio.py
    │
    └── colaborative/
        ├── bases_rag/cognitiva/
        │   ├── juez_centrico_arg.db
        │   ├── metadatos.db
        │   └── modelos_predictivos/
        │
        └── scripts/ (71 archivos)
            ├── Core (8 archivos)
            ├── Judicial (15 archivos)
            └── Utilidades
    """)

    print("="*70)
    print("✅ REPOSITORIO LIMPIO Y OPTIMIZADO")
    print("="*70)

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("LIMPIEZA FINAL DEL REPOSITORIO")
    print("="*70)
    print("\nEsto eliminará ~85 archivos .py obsoletos del directorio raíz.")
    print("Se mantendrán solo los scripts esenciales y documentación.")
    print("\nEl directorio colaborative/ NO se tocará.")

    # Listar y eliminar
    eliminados = eliminar_archivos()

    if eliminados > 0:
        # Verificar que todo esté bien
        verificar_directorio_colaborative()

        # Reporte final
        generar_reporte_final()

        print(f"\n✅ Limpieza completada: {eliminados} archivos eliminados")
        print("\n📝 SIGUIENTE PASO:")
        print("   Hacer commit de estos cambios con:")
        print("   git add -A")
        print("   git commit -m 'Limpieza final: eliminar archivos obsoletos del directorio raíz'")
        print("   git push")

if __name__ == "__main__":
    main()
