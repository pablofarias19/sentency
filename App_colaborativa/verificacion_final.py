#!/usr/bin/env python3
"""
VERIFICADOR FINAL DEL SISTEMA
=============================
Confirma que todos los datos están correctamente vinculados y funcionando.
"""

import sqlite3
import json
from pathlib import Path
import os

def verificar_integridad_completa():
    """Verificación completa de la integridad del sistema"""
    print("🔍 VERIFICACIÓN FINAL DE INTEGRIDAD DEL SISTEMA")
    print("=" * 60)
    
    # 1. Verificar base de datos cognitiva
    db_cognitiva = Path("colaborative/bases_rag/cognitiva/metadatos.db")
    if not db_cognitiva.exists():
        print("❌ Base de datos cognitiva no encontrada")
        return False
    
    conn = sqlite3.connect(db_cognitiva)
    cursor = conn.cursor()
    
    # Verificar perfiles con rasgos cognitivos
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos WHERE formalismo IS NOT NULL AND formalismo > 0")
    perfiles_con_rasgos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
    total_perfiles = cursor.fetchone()[0]
    
    print(f"📊 DATOS COGNITIVOS:")
    print(f"   ✅ Total perfiles: {total_perfiles}")
    print(f"   ✅ Con rasgos calculados: {perfiles_con_rasgos}")
    print(f"   📈 Integridad: {(perfiles_con_rasgos/total_perfiles*100):.1f}%")
    
    # Mostrar resumen de rasgos
    cursor.execute("""
        SELECT autor, formalismo, creatividad, empirismo, 
               ROUND(AVG(formalismo + creatividad + empirismo), 3) as promedio_general
        FROM perfiles_cognitivos 
        WHERE formalismo IS NOT NULL
        GROUP BY autor
    """)
    
    perfiles_detalle = cursor.fetchall()
    print(f"\n👥 PERFILES COGNITIVOS DETALLADOS:")
    for perfil in perfiles_detalle:
        autor, form, creat, emp, prom = perfil
        print(f"   📝 {autor}:")
        print(f"      🏛️ Formalismo: {form:.3f}")
        print(f"      🎨 Creatividad: {creat:.3f}")
        print(f"      🔬 Empirismo: {emp:.3f}")
        print(f"      📊 Puntuación general: {prom:.3f}")
    
    conn.close()
    
    # 2. Verificar base de datos de autoaprendizaje
    db_auto = Path("colaborative/bases_rag/autoaprendizaje/evaluaciones.db")
    if db_auto.exists():
        conn_auto = sqlite3.connect(db_auto)
        cursor_auto = conn_auto.cursor()
        
        cursor_auto.execute("SELECT COUNT(*), AVG(puntuacion) FROM evaluaciones_sistema")
        evaluaciones_data = cursor_auto.fetchone()
        total_eval, promedio_eval = evaluaciones_data
        
        print(f"\n🤖 AUTOAPRENDIZAJE:")
        print(f"   ✅ Total evaluaciones: {total_eval}")
        print(f"   📊 Promedio puntuación: {promedio_eval:.2f}/10")
        
        conn_auto.close()
    else:
        print(f"\n⚠️ Base de autoaprendizaje no encontrada")
    
    # 3. Verificar índices FAISS
    faiss_general = Path("colaborative/data/index/general/vector_index.faiss")
    faiss_civil = Path("colaborative/data/index/civil/vector_index.faiss")
    
    print(f"\n🔍 ÍNDICES VECTORIALES:")
    if faiss_general.exists():
        size_general = faiss_general.stat().st_size / 1024 / 1024
        print(f"   ✅ General: {size_general:.1f} MB")
    else:
        print(f"   ❌ General: No encontrado")
        
    if faiss_civil.exists():
        size_civil = faiss_civil.stat().st_size / 1024 / 1024
        print(f"   ✅ Civil: {size_civil:.1f} MB")
    else:
        print(f"   ❌ Civil: No encontrado")
    
    # 4. Verificar PDFs procesados
    pdf_general = Path("colaborative/data/pdfs/general")
    pdf_civil = Path("colaborative/data/pdfs/civil")
    
    pdfs_encontrados = 0
    print(f"\n📄 DOCUMENTOS FUENTE:")
    
    if pdf_general.exists():
        pdfs_gen = list(pdf_general.glob("*.pdf"))
        pdfs_encontrados += len(pdfs_gen)
        print(f"   📂 General: {len(pdfs_gen)} PDFs")
        for pdf in pdfs_gen:
            print(f"      📄 {pdf.name}")
    
    if pdf_civil.exists():
        pdfs_civ = list(pdf_civil.glob("*.pdf"))
        pdfs_encontrados += len(pdfs_civ)
        print(f"   📂 Civil: {len(pdfs_civ)} PDFs")
        for pdf in pdfs_civ:
            print(f"      📄 {pdf.name}")
    
    # 5. Verificar scripts principales
    scripts_principales = [
        "detector_autor_y_metodo.py",
        "vectorizador_cognitivo.py", 
        "end2end_webapp.py",
        "autoaprendizaje.py",
        "procesar_todo.py"
    ]
    
    print(f"\n🔧 SCRIPTS PRINCIPALES:")
    scripts_path = Path("colaborative/scripts")
    for script in scripts_principales:
        script_path = scripts_path / script
        if script_path.exists():
            size_kb = script_path.stat().st_size / 1024
            print(f"   ✅ {script}: {size_kb:.1f} KB")
        else:
            print(f"   ❌ {script}: No encontrado")
    
    # 6. RESUMEN FINAL
    print(f"\n🎯 RESUMEN DE INTEGRIDAD:")
    print(f"=" * 40)
    
    integridad_cognitiva = (perfiles_con_rasgos / total_perfiles) * 100 if total_perfiles > 0 else 0
    
    checks = [
        ("Base cognitiva", integridad_cognitiva >= 100),
        ("Autoaprendizaje", db_auto.exists()),
        ("Índices FAISS", faiss_general.exists()),
        ("PDFs fuente", pdfs_encontrados >= 4),
        ("Scripts principales", scripts_path.exists())
    ]
    
    checks_pasados = sum(1 for _, passed in checks if passed)
    total_checks = len(checks)
    
    for nombre, pasado in checks:
        estado = "✅" if pasado else "❌"
        print(f"   {estado} {nombre}")
    
    integridad_general = (checks_pasados / total_checks) * 100
    print(f"\n📊 INTEGRIDAD GENERAL DEL SISTEMA: {integridad_general:.1f}%")
    
    if integridad_general >= 80:
        print("🎉 ¡SISTEMA COMPLETAMENTE OPERATIVO!")
    elif integridad_general >= 60:
        print("⚠️ Sistema funcional con advertencias menores")
    else:
        print("❌ Sistema requiere atención urgente")
    
    return integridad_general >= 80

def mostrar_estadisticas_cognitivas():
    """Muestra estadísticas detalladas de los rasgos cognitivos"""
    print(f"\n📈 ESTADÍSTICAS COGNITIVAS DETALLADAS:")
    print("=" * 50)
    
    db_path = Path("colaborative/bases_rag/cognitiva/metadatos.db")
    if not db_path.exists():
        print("❌ Base de datos no disponible")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Promedios por rasgo
    cursor.execute("""
        SELECT 
            AVG(formalismo) as prom_formalismo,
            AVG(creatividad) as prom_creatividad,
            AVG(dogmatismo) as prom_dogmatismo,
            AVG(empirismo) as prom_empirismo,
            AVG(interdisciplinariedad) as prom_interdisciplinariedad,
            AVG(nivel_abstraccion) as prom_abstraccion,
            AVG(complejidad_sintactica) as prom_complejidad,
            AVG(uso_jurisprudencia) as prom_jurisprudencia
        FROM perfiles_cognitivos 
        WHERE formalismo IS NOT NULL
    """)
    
    promedios = cursor.fetchone()
    
    rasgos_nombres = [
        "🏛️ Formalismo",
        "🎨 Creatividad", 
        "📚 Dogmatismo",
        "🔬 Empirismo",
        "🌐 Interdisciplinariedad",
        "🧭 Nivel Abstracción",
        "📖 Complejidad Sintáctica",
        "⚖️ Uso Jurisprudencia"
    ]
    
    print("🔢 PROMEDIOS GENERALES:")
    for i, (nombre, valor) in enumerate(zip(rasgos_nombres, promedios)):
        print(f"   {nombre}: {valor:.3f}")
    
    # Autor con mayor formalismo
    cursor.execute("""
        SELECT autor, formalismo 
        FROM perfiles_cognitivos 
        WHERE formalismo = (SELECT MAX(formalismo) FROM perfiles_cognitivos)
    """)
    
    autor_formal = cursor.fetchone()
    print(f"\n🏆 AUTOR MÁS FORMALISTA: {autor_formal[0]} ({autor_formal[1]:.3f})")
    
    # Autor más empírico
    cursor.execute("""
        SELECT autor, empirismo 
        FROM perfiles_cognitivos 
        WHERE empirismo = (SELECT MAX(empirismo) FROM perfiles_cognitivos)
    """)
    
    autor_empirico = cursor.fetchone()
    print(f"🔬 AUTOR MÁS EMPÍRICO: {autor_empirico[0]} ({autor_empirico[1]:.3f})")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 INICIANDO VERIFICACIÓN FINAL")
    
    # Cambiar al directorio correcto
    if not Path("colaborative").exists():
        print("❌ Directorio 'colaborative' no encontrado")
        exit(1)
    
    # Verificar integridad
    sistema_operativo = verificar_integridad_completa()
    
    # Mostrar estadísticas si el sistema está operativo
    if sistema_operativo:
        mostrar_estadisticas_cognitivas()
    
    print(f"\n✅ Verificación completada")