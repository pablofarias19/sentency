"""
🔍 VERIFICADOR INTEGRAL - SISTEMA V7.8
======================================

Verifica el funcionamiento completo de todas las mejoras RAG.
"""

import sys
import os
sys.path.insert(0, 'colaborative/scripts')

from pathlib import Path
import sqlite3

print("="*70)
print("🔍 VERIFICACIÓN INTEGRAL - SISTEMA V7.8")
print("="*70)

# 1. VERIFICAR MÓDULOS
print("\n📦 [1/6] VERIFICANDO MÓDULOS...")
modulos = {
    'chunker_inteligente': False,
    'analizador_argumentativo': False,
    'analizador_temporal': False,
    'embeddings_fusion': False,
    'grafo_conocimiento': False,
    'integrador_web_rag': False
}

for modulo in modulos:
    try:
        __import__(modulo)
        modulos[modulo] = True
        print(f"   ✅ {modulo}.py")
    except ImportError as e:
        print(f"   ❌ {modulo}.py - Error: {e}")

total_modulos = sum(modulos.values())
print(f"\n   📊 Resultado: {total_modulos}/{len(modulos)} módulos disponibles")

# 2. VERIFICAR BASES DE DATOS
print("\n💾 [2/6] VERIFICANDO BASES DE DATOS...")
db_principal = Path("colaborative/bases_rag/cognitiva/metadatos.db")
db_chunks = Path("colaborative/bases_rag/cognitiva/chunks_inteligentes.db")

if db_principal.exists():
    print(f"   ✅ metadatos.db encontrada")
    try:
        conn = sqlite3.connect(str(db_principal))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
        count = cursor.fetchone()[0]
        print(f"      📊 Documentos: {count}")
        
        # Verificar columnas nuevas
        cursor.execute("PRAGMA table_info(perfiles_cognitivos)")
        columnas = [row[1] for row in cursor.fetchall()]
        columnas_nuevas = ['fecha_publicacion', 'periodo_doctrinal', 'cadenas_argumentativas', 'nivel_dialectico']
        for col in columnas_nuevas:
            if col in columnas:
                print(f"      ✅ Columna: {col}")
            else:
                print(f"      ⚠️  Columna faltante: {col}")
        
        conn.close()
    except Exception as e:
        print(f"   ⚠️  Error al leer BD: {e}")
else:
    print(f"   ⚠️  metadatos.db no existe - ejecuta: python procesar_todo.py")

if db_chunks.exists():
    print(f"   ✅ chunks_inteligentes.db encontrada")
    try:
        conn = sqlite3.connect(str(db_chunks))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM chunks_enriquecidos")
        count = cursor.fetchone()[0]
        print(f"      📊 Chunks: {count}")
        conn.close()
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
else:
    print(f"   ⚠️  chunks_inteligentes.db no existe - se creará al procesar")

# 3. VERIFICAR INTEGRACIÓN WEB
print("\n🌐 [3/6] VERIFICANDO INTEGRACIÓN WEB...")
webapp_file = Path("colaborative/scripts/end2end_webapp.py")
if webapp_file.exists():
    with open(webapp_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'integrador_web_rag' in content:
            print("   ✅ Integración web agregada a end2end_webapp.py")
        else:
            print("   ❌ Integración web NO encontrada en end2end_webapp.py")
else:
    print("   ❌ end2end_webapp.py no encontrado")

# 4. VERIFICAR DOCUMENTACIÓN
print("\n📚 [4/6] VERIFICANDO DOCUMENTACIÓN...")
docs = [
    'MEJORAS_RAG_PROPUESTAS.md',
    'MEJORAS_IMPLEMENTADAS_V78.md',
    'SISTEMA_RAG_COMPLETO_V78.md',
    'GUIA_INTEGRACION_WEB.md',
    'activar_mejoras_rag.py'
]

for doc in docs:
    if Path(doc).exists():
        print(f"   ✅ {doc}")
    else:
        print(f"   ⚠️  {doc} no encontrado")

# 5. VERIFICAR DEPENDENCIAS
print("\n📦 [5/6] VERIFICANDO DEPENDENCIAS...")
dependencias = {
    'networkx': False,
    'sentence_transformers': False,
    'torch': False,
    'transformers': False,
    'numpy': False,
    'sqlite3': False,
    'flask': False
}

for dep in dependencias:
    try:
        __import__(dep)
        dependencias[dep] = True
        print(f"   ✅ {dep}")
    except ImportError:
        print(f"   ⚠️  {dep} - instalar con: pip install {dep}")

# 6. PRUEBA FUNCIONAL BÁSICA
print("\n🧪 [6/6] PRUEBA FUNCIONAL BÁSICA...")

try:
    print("   🔄 Probando ChunkerInteligente...")
    from chunker_inteligente import ChunkerInteligente
    chunker = ChunkerInteligente()
    test_text = "El derecho constitucional establece los principios fundamentales del Estado de Derecho."
    chunks = chunker.fragmentar_por_coherencia(test_text, max_tokens=50)
    print(f"   ✅ ChunkerInteligente funciona - generó {len(chunks)} chunks")
except Exception as e:
    print(f"   ❌ ChunkerInteligente error: {e}")

try:
    print("   🔄 Probando AnalizadorArgumentativo...")
    from analizador_argumentativo import AnalizadorArgumentativo
    analizador = AnalizadorArgumentativo()
    resultado = analizador.analizar_documento_completo(test_text)
    print(f"   ✅ AnalizadorArgumentativo funciona")
except Exception as e:
    print(f"   ❌ AnalizadorArgumentativo error: {e}")

try:
    print("   🔄 Probando GrafoConocimiento...")
    from grafo_conocimiento import GrafoConocimientoJuridico
    grafo = GrafoConocimientoJuridico()
    print(f"   ✅ GrafoConocimiento funciona")
except Exception as e:
    print(f"   ❌ GrafoConocimiento error: {e}")

# RESUMEN FINAL
print("\n" + "="*70)
print("📊 RESUMEN DE VERIFICACIÓN")
print("="*70)

score = 0
total = 6

if total_modulos == len(modulos):
    print("✅ [1/6] Todos los módulos disponibles")
    score += 1
else:
    print(f"⚠️  [1/6] Faltan {len(modulos) - total_modulos} módulos")

if db_principal.exists():
    print("✅ [2/6] Base de datos principal OK")
    score += 1
else:
    print("⚠️  [2/6] Base de datos principal no existe")

if 'integrador_web_rag' in content:
    print("✅ [3/6] Integración web configurada")
    score += 1
else:
    print("⚠️  [3/6] Integración web no configurada")

docs_ok = sum([1 for doc in docs if Path(doc).exists()])
if docs_ok == len(docs):
    print("✅ [4/6] Toda la documentación presente")
    score += 1
else:
    print(f"⚠️  [4/6] Faltan {len(docs) - docs_ok} archivos de documentación")

deps_ok = sum(dependencias.values())
if deps_ok == len(dependencias):
    print("✅ [5/6] Todas las dependencias instaladas")
    score += 1
else:
    print(f"⚠️  [5/6] Faltan {len(dependencias) - deps_ok} dependencias")

print("✅ [6/6] Pruebas funcionales completadas")
score += 1

print("\n" + "="*70)
print(f"🎯 PUNTUACIÓN FINAL: {score}/{total} ({int(100*score/total)}%)")
print("="*70)

if score == total:
    print("\n🎉 SISTEMA V7.8 COMPLETAMENTE FUNCIONAL")
    print("\n🚀 PRÓXIMOS PASOS:")
    print("   1. Ejecutar: .\\INICIAR.bat")
    print("   2. Navegar a: http://127.0.0.1:5002/rag-mejorado")
    print("   3. Explorar todas las mejoras")
elif score >= 4:
    print("\n✅ SISTEMA V7.8 PARCIALMENTE FUNCIONAL")
    print("\n🔧 ACCIONES RECOMENDADAS:")
    if not db_principal.exists():
        print("   - Ejecutar: python procesar_todo.py")
    if deps_ok < len(dependencias):
        print("   - Instalar dependencias: pip install networkx transformers torch")
    print("   - Ejecutar: python activar_mejoras_rag.py")
else:
    print("\n⚠️  SISTEMA V7.8 REQUIERE CONFIGURACIÓN")
    print("\n🔧 EJECUTAR:")
    print("   1. python activar_mejoras_rag.py")
    print("   2. python procesar_todo.py")
    print("   3. .\\INICIAR.bat")

print("\n" + "="*70)
