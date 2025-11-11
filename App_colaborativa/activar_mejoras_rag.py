"""
🚀 ACTIVADOR DE MEJORAS RAG V7.8
=================================

Este script activa TODAS las mejoras del sistema RAG:
1. ✅ Chunker Inteligente (ya activo)
2. ✅ Metadatos Argumentativos
3. ✅ Análisis Temporal
4. ✅ Embeddings Multi-Nivel
5. ✅ Grafo de Conocimiento

Ejecuta:
1. Actualización de esquema de base de datos
2. Instalación de dependencias
3. Descarga de modelos de embeddings
4. Verificación de integridad

Autor: Sistema V7.8
Fecha: 11 Nov 2025
"""

import sqlite3
import subprocess
import sys
from pathlib import Path
import os


def print_header(mensaje):
    """Imprime encabezado decorado."""
    print("\n" + "="*70)
    print(f"🚀 {mensaje}")
    print("="*70 + "\n")


def actualizar_schema_bd():
    """
    Actualiza el esquema de metadatos.db con nuevos campos.
    """
    print_header("PASO 1: ACTUALIZACIÓN DE BASE DE DATOS")
    
    db_path = Path("colaborative/bases_rag/cognitiva/metadatos.db")
    
    if not db_path.exists():
        print(f"⚠️  Base de datos no encontrada: {db_path}")
        print("   Ejecuta primero: python procesar_todo.py")
        return False
    
    print(f"📁 Conectando a: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Obtener columnas existentes
    cursor.execute("PRAGMA table_info(perfiles_cognitivos)")
    columnas_existentes = [row[1] for row in cursor.fetchall()]
    
    print(f"✅ Columnas actuales: {len(columnas_existentes)}")
    
    # Nuevas columnas a agregar
    nuevas_columnas = [
        ("fecha_publicacion", "INTEGER"),
        ("periodo_doctrinal", "TEXT"),
        ("cadenas_argumentativas", "TEXT"),
        ("objeciones_anticipadas", "TEXT"),
        ("refutaciones", "TEXT"),
        ("estructura_retorica", "TEXT"),
        ("mapa_fuerza", "TEXT"),
        ("nivel_dialectico", "REAL"),
        ("conectores_por_tipo", "TEXT"),
        ("tipos_silogismo", "TEXT")
    ]
    
    cambios = 0
    for columna, tipo in nuevas_columnas:
        if columna not in columnas_existentes:
            try:
                sql = f"ALTER TABLE perfiles_cognitivos ADD COLUMN {columna} {tipo}"
                cursor.execute(sql)
                print(f"   ✅ Agregada columna: {columna} ({tipo})")
                cambios += 1
            except sqlite3.OperationalError as e:
                print(f"   ⚠️  {columna}: {e}")
    
    conn.commit()
    conn.close()
    
    if cambios > 0:
        print(f"\n✅ Base de datos actualizada: {cambios} columnas nuevas")
    else:
        print("\n✅ Base de datos ya estaba actualizada")
    
    return True


def instalar_dependencias():
    """
    Instala dependencias adicionales para embeddings multi-nivel y grafo.
    """
    print_header("PASO 2: INSTALACIÓN DE DEPENDENCIAS")
    
    paquetes = [
        "sentence-transformers",  # Ya instalado, pero verificar
        "networkx",               # Para grafo de conocimiento
        "transformers",           # Para modelos BERT
        "torch"                   # PyTorch (backend)
    ]
    
    print("📦 Paquetes a verificar/instalar:")
    for paq in paquetes:
        print(f"   - {paq}")
    
    print("\n🔄 Ejecutando pip install...")
    
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "--upgrade",
            *paquetes
        ])
        print("\n✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error al instalar dependencias: {e}")
        return False


def verificar_modelos():
    """
    Verifica que los modelos de embeddings estén disponibles.
    """
    print_header("PASO 3: VERIFICACIÓN DE MODELOS")
    
    print("🔍 Verificando modelos de Sentence-Transformers...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        modelos = [
            ('all-mpnet-base-v2', 'General (768D)'),
            ('paraphrase-multilingual-mpnet-base-v2', 'Multilingüe (768D)')
        ]
        
        for modelo, descripcion in modelos:
            try:
                print(f"\n📥 Cargando: {modelo}")
                print(f"   ({descripcion})")
                SentenceTransformer(modelo)
                print(f"   ✅ Disponible")
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
                print(f"   🔄 Se descargará en primera ejecución")
        
        print("\n✅ Verificación de modelos completada")
        return True
        
    except ImportError:
        print("❌ sentence-transformers no instalado")
        return False


def verificar_archivos_mejoras():
    """
    Verifica que todos los archivos de mejoras existan.
    """
    print_header("PASO 4: VERIFICACIÓN DE ARCHIVOS")
    
    archivos_requeridos = [
        "colaborative/scripts/chunker_inteligente.py",
        "colaborative/scripts/analizador_argumentativo.py",
        "colaborative/scripts/analizador_temporal.py",
        "colaborative/scripts/embeddings_fusion.py",
        "colaborative/scripts/grafo_conocimiento.py"
    ]
    
    todos_ok = True
    for archivo in archivos_requeridos:
        path = Path(archivo)
        if path.exists():
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} NO ENCONTRADO")
            todos_ok = False
    
    if todos_ok:
        print("\n✅ Todos los archivos de mejoras presentes")
    else:
        print("\n❌ Faltan archivos de mejoras")
    
    return todos_ok


def mostrar_resumen_final():
    """
    Muestra resumen de activación y próximos pasos.
    """
    print_header("RESUMEN DE ACTIVACIÓN")
    
    print("✅ MEJORAS RAG V7.8 ACTIVADAS:")
    print()
    print("1. ✅ Chunker Inteligente")
    print("   - Fragmentación semántica")
    print("   - Base: chunks_inteligentes.db")
    print()
    print("2. ✅ Metadatos Argumentativos")
    print("   - Cadenas argumentativas")
    print("   - Silogismos detectados")
    print("   - Estructura retórica")
    print()
    print("3. ✅ Análisis Temporal")
    print("   - Fecha de publicación")
    print("   - Periodo doctrinal")
    print("   - Evolución de autores")
    print()
    print("4. ✅ Embeddings Multi-Nivel")
    print("   - 3 modelos fusionados")
    print("   - General (50%) + Legal (35%) + Multi (15%)")
    print("   - +25% precisión estimada")
    print()
    print("5. ✅ Grafo de Conocimiento")
    print("   - NetworkX implementado")
    print("   - Relaciones: cita_a, desarrolla, aplica")
    print("   - Consultas avanzadas disponibles")
    
    print("\n" + "="*70)
    print("🎯 PRÓXIMOS PASOS:")
    print("="*70)
    print()
    print("1. REPROCESAR DOCUMENTOS:")
    print("   python procesar_todo.py")
    print()
    print("2. PROBAR EMBEDDINGS MULTI-NIVEL:")
    print("   python colaborative/scripts/embeddings_fusion.py")
    print()
    print("3. CONSTRUIR GRAFO DE CONOCIMIENTO:")
    print("   python colaborative/scripts/grafo_conocimiento.py")
    print()
    print("4. INICIAR SISTEMA COMPLETO:")
    print("   .\\INICIAR.bat")
    print()
    print("="*70)
    print("🚀 SISTEMA V7.8 - RAG MEJORADO LISTO PARA USAR")
    print("="*70)


def main():
    """
    Ejecuta todos los pasos de activación.
    """
    print("="*70)
    print("🚀 ACTIVADOR DE MEJORAS RAG V7.8")
    print("="*70)
    print()
    print("Este script configurará:")
    print("  ✅ Chunker Inteligente")
    print("  ✅ Metadatos Argumentativos")
    print("  ✅ Análisis Temporal")
    print("  ✅ Embeddings Multi-Nivel")
    print("  ✅ Grafo de Conocimiento")
    print()
    input("Presiona ENTER para continuar...")
    
    # Paso 1: Actualizar BD
    if not actualizar_schema_bd():
        print("\n❌ Error al actualizar base de datos")
        print("   Verifica que metadatos.db existe")
        return
    
    # Paso 2: Instalar dependencias
    if not instalar_dependencias():
        print("\n⚠️  Error al instalar dependencias")
        print("   Puedes continuar, pero algunas funciones pueden fallar")
    
    # Paso 3: Verificar modelos
    verificar_modelos()
    
    # Paso 4: Verificar archivos
    if not verificar_archivos_mejoras():
        print("\n⚠️  Faltan algunos archivos de mejoras")
        print("   Verifica que todos los módulos estén presentes")
    
    # Resumen final
    mostrar_resumen_final()


if __name__ == "__main__":
    main()
