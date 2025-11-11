# -*- coding: utf-8 -*-
"""
Ejemplo de Uso del Sistema RAG Enriquecido con PCA
Demuestra el flujo completo desde la ingesta hasta las consultas
"""

import os
import sys
from pathlib import Path
import tempfile

print("🎯 EJEMPLO DE USO - SISTEMA RAG ENRIQUECIDO CON PCA")
print("=" * 60)

# Asegurar que podemos importar los módulos
scripts_dir = Path("colaborative/scripts") 
sys.path.append(str(scripts_dir))

def crear_pdf_ejemplo():
    """Crea un PDF de ejemplo para demostrar el sistema"""
    print("\n📄 Creando PDF de ejemplo...")
    
    try:
        from reportlab.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Crear directorio si no existe
        pdf_dir = Path("colaborative/data/pdfs/general")
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo de destino
        pdf_path = pdf_dir / "ejemplo_teoria_derecho.pdf"
        
        if pdf_path.exists():
            print(f"  ✅ PDF ya existe: {pdf_path}")
            return str(pdf_path)
        
        # Crear documento
        doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Contenido del documento
        story.append(Paragraph("TEORÍA PURA DEL DERECHO", styles['Title']))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("Autor: Hans Kelsen", styles['Normal']))
        story.append(Paragraph("Año: 1960", styles['Normal']))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("I. INTRODUCCIÓN", styles['Heading2']))
        story.append(Paragraph(
            "La teoría pura del derecho constituye una metodología jurídica que busca "
            "eliminar de la ciencia jurídica todos los elementos que le son extraños. "
            "Kelsen propone un análisis estrictamente normativo del fenómeno jurídico, "
            "diferenciándose de las corrientes sociológicas y iusnaturalistas.",
            styles['Normal']
        ))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("II. CRÍTICA A HART", styles['Heading2']))
        story.append(Paragraph(
            "El problema central radica en la determinación de la validez jurídica. "
            "Hart sostiene una posición que el autor critica por su insuficiencia "
            "metodológica. La cuestión fundamental es establecer los criterios "
            "objetivos para determinar la pertenencia de una norma al ordenamiento.",
            styles['Normal']
        ))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("III. MARCO JURÍDICO-GARANTISTA", styles['Heading2']))
        story.append(Paragraph(
            "Siguiendo los lineamientos de Dworkin y Alexy, se propone una estrategia "
            "analítica que examine las condiciones de validez desde una perspectiva "
            "principialista. Los autores mencionados incluyen a Ferrajoli, Ross y "
            "otros teóricos del garantismo constitucional.",
            styles['Normal']
        ))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("IV. METODOLOGÍA COMPARATIVA", styles['Heading2']))
        story.append(Paragraph(
            "El análisis contrasta diferentes enfoques metodológicos en la teoría "
            "jurídica. Se comparan las posiciones de Weber, Luhmann y Habermas "
            "respecto a la fundamentación sociológica del derecho, estableciendo "
            "diferencias sustanciales con la propuesta kelseniana.",
            styles['Normal']
        ))
        
        # Construir PDF
        doc.build(story)
        
        print(f"  ✅ PDF creado: {pdf_path}")
        return str(pdf_path)
        
    except ImportError:
        print("  ⚠️ ReportLab no disponible, saltando creación de PDF")
        return None
    except Exception as e:
        print(f"  ❌ Error creando PDF: {e}")
        return None

def ejemplo_extraccion_enriquecida(pdf_path):
    """Demuestra la extracción enriquecida con PCA"""
    print(f"\n🔍 EJEMPLO: Extracción enriquecida de {Path(pdf_path).name}")
    
    try:
        from extractor_pdf_enriquecido import extract_from_pdf_enriquecido
        
        # Extraer con análisis PCA
        doc_data = extract_from_pdf_enriquecido(pdf_path)
        
        print("  📊 RESULTADOS DE EXTRACCIÓN:")
        print(f"    📖 Título: {doc_data['meta']['titulo']}")
        print(f"    👤 Autor: {doc_data['meta']['autor']}")
        print(f"    📅 Año: {doc_data['meta']['anio']}")
        print(f"    🔗 Hash: {doc_data['meta']['hash']}")
        print(f"    📄 Chunks: {len(doc_data['chunks'])}")
        
        print("\n  🧠 ANÁLISIS COGNITIVO-AUTORAL:")
        
        # Mostrar estadísticas
        stats = doc_data.get('stats', {})
        if 'metodologias' in stats:
            print(f"    🎯 Metodologías: {dict(stats['metodologias'])}")
        if 'marcos_referencia' in stats:
            print(f"    🏛️ Marcos: {dict(stats['marcos_referencia'])}")
        if 'estrategias' in stats:
            print(f"    ⚡ Estrategias: {dict(stats['estrategias'])}")
        
        # Mostrar ejemplo de chunk procesado
        if doc_data['chunks']:
            chunk_ejemplo = doc_data['chunks'][0]
            labels = chunk_ejemplo.get('labels', {})
            
            print(f"\n  📋 EJEMPLO DE CHUNK PROCESADO:")
            print(f"    🏷️ Metodología: {labels.get('metodologia', 'N/A')}")
            print(f"    🧠 Marco: {labels.get('marco_referencia', 'N/A')}")
            print(f"    ⚡ Estrategia: {labels.get('estrategia', 'N/A')}")
            print(f"    👥 Autores: {labels.get('autores_mencionados', [])}")
            print(f"    🎯 Tema: {labels.get('tema_especifico', 'N/A')}")
        
        return doc_data
        
    except Exception as e:
        print(f"  ❌ Error en extracción: {e}")
        return None

def ejemplo_perfiles_cognitivos(doc_data):
    """Demuestra el sistema de perfiles cognitivos"""
    print(f"\n🎭 EJEMPLO: Sistema de perfiles cognitivos")
    
    try:
        from profiles_rag import ProfilesStore, build_firma
        
        # Crear instancia del almacén
        store = ProfilesStore()
        stats_inicial = store.get_stats()
        
        print(f"  📊 Estado inicial del almacén:")
        print(f"    🗃️ Perfiles existentes: {stats_inicial.get('total_perfiles', 0)}")
        print(f"    📐 Dimensión: {stats_inicial.get('dimension', 'N/A')}")
        
        # Construir perfiles del documento
        rows_perfiles = []
        meta = doc_data['meta']
        
        for chunk in doc_data['chunks'][:3]:  # Solo primeros 3 chunks para ejemplo
            labels = chunk.get('labels', {})
            
            perfil = {
                "marco_referencia": labels.get("marco_referencia"),
                "critica_a": labels.get("critica_a", []),
                "motivo_intelectual": labels.get("motivo_intelectual"),
                "estrategia": labels.get("estrategia"),
                "autores_mencionados": labels.get("autores_mencionados", [])
            }
            
            firma = build_firma(
                perfil=perfil,
                meta_doc=meta,
                titulo_seccion=labels.get("tema_especifico", "Sin título"),
                palabras_clave=labels.get("palabras_clave", [])
            )
            
            row_perfil = {
                "doc_hash": meta["hash"],
                "doc_titulo": meta["titulo"],
                "autor_detectado": meta.get("autor", "No identificado"),
                "nivel": "seccion",
                "perfil_json": perfil,
                "firma": firma
            }
            rows_perfiles.append(row_perfil)
        
        print(f"\n  🔗 FIRMAS COGNITIVAS GENERADAS:")
        for i, row in enumerate(rows_perfiles, 1):
            print(f"    {i}. {row['firma'][:100]}...")
        
        # Añadir perfiles al almacén
        store.add_profiles(rows_perfiles)
        stats_final = store.get_stats()
        
        print(f"\n  ✅ Perfiles añadidos al almacén:")
        print(f"    📈 Total ahora: {stats_final.get('total_perfiles', 0)}")
        
        return store
        
    except Exception as e:
        print(f"  ❌ Error en perfiles: {e}")
        return None

def ejemplo_busqueda_gemelos(store):
    """Demuestra la búsqueda de gemelos cognitivos"""
    print(f"\n🔍 EJEMPLO: Búsqueda de gemelos cognitivos")
    
    try:
        from profiles_rag import enrich_prompt_with_profiles
        
        # Consultas de ejemplo
        consultas = [
            "¿Qué es la validez jurídica?",
            "Teoría pura del derecho Kelsen",
            "Críticas a Hart sobre normas"
        ]
        
        for i, consulta in enumerate(consultas, 1):
            print(f"\n  🎯 CONSULTA {i}: {consulta}")
            
            # Buscar gemelos cognitivos
            vecinos = store.search_profiles(f"CONSULTA:{consulta}", k=5)
            
            if vecinos:
                print(f"    🎭 Gemelos encontrados: {len(vecinos)}")
                for score, meta in vecinos[:3]:
                    autor = meta.get('autor_detectado', 'N/A')
                    titulo = meta.get('doc_titulo', 'N/A')[:40]
                    print(f"      • {score:.3f} - {autor} | {titulo}...")
            else:
                print(f"    ⚠️ No se encontraron gemelos cognitivos")
            
            # Generar contexto enriquecido
            contexto = enrich_prompt_with_profiles(consulta, "Teoría del Derecho", k=3)
            print(f"    💡 Contexto generado:")
            print(f"      {contexto[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en búsqueda: {e}")
        return False

def ejemplo_autoaprendizaje():
    """Demuestra el sistema de autoaprendizaje"""
    print(f"\n📚 EJEMPLO: Sistema de autoaprendizaje")
    
    try:
        from autoaprendizaje import guardar_autoevaluacion, generar_contexto_adaptativo
        
        # Simular una evaluación
        guardar_autoevaluacion(
            modelo="Ejemplo PCA",
            pregunta="¿Qué es la teoría pura del derecho?",
            concepto="La teoría pura del derecho es una metodología jurídica propuesta por Kelsen...",
            autoevaluacion="Respuesta técnicamente correcta con referencias apropiadas.",
            puntaje=8.5,
            prompt_base="Ejemplo de evaluación del sistema PCA"
        )
        
        print("  ✅ Evaluación de ejemplo guardada")
        
        # Generar contexto adaptativo
        contexto = generar_contexto_adaptativo()
        print(f"  💡 Contexto adaptativo:")
        print(f"    {contexto[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en autoaprendizaje: {e}")
        return False

def ejemplo_completo():
    """Ejecuta el ejemplo completo del sistema"""
    print("🚀 Iniciando ejemplo completo del sistema...\n")
    
    try:
        # 1. Crear PDF de ejemplo
        pdf_path = crear_pdf_ejemplo()
        if not pdf_path:
            print("⚠️ No se pudo crear PDF, usar uno existente si está disponible")
            return False
        
        # 2. Extracción enriquecida
        doc_data = ejemplo_extraccion_enriquecida(pdf_path)
        if not doc_data:
            print("❌ Falló la extracción enriquecida")
            return False
        
        # 3. Sistema de perfiles
        store = ejemplo_perfiles_cognitivos(doc_data)
        if not store:
            print("❌ Falló el sistema de perfiles")
            return False
        
        # 4. Búsqueda de gemelos
        if not ejemplo_busqueda_gemelos(store):
            print("❌ Falló la búsqueda de gemelos")
            return False
        
        # 5. Autoaprendizaje
        if not ejemplo_autoaprendizaje():
            print("❌ Falló el autoaprendizaje")
            return False
        
        # Resumen final
        print("\n" + "=" * 60)
        print("🎉 EJEMPLO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("\n✅ Funcionalidades demostradas:")
        print("  • Extracción PDF con análisis PCA")
        print("  • Construcción de perfiles cognitivos")
        print("  • Almacenamiento vectorial (FAISS_B)")
        print("  • Búsqueda de gemelos cognitivos")
        print("  • Enriquecimiento de prompts")
        print("  • Sistema de autoaprendizaje")
        
        print("\n📋 El sistema está listo para uso real:")
        print("  1. Coloca PDFs reales en: colaborative/data/pdfs/general/")
        print("  2. Ejecuta: python colaborative/scripts/ingesta_enriquecida.py")
        print("  3. Inicia webapp: python colaborative/scripts/end2end_webapp.py")
        print("  4. Consulta en: http://127.0.0.1:5002")
        print("  5. Audita en: http://127.0.0.1:5002/perfiles")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en ejemplo completo: {e}")
        return False

if __name__ == "__main__":
    try:
        success = ejemplo_completo()
        if not success:
            print("\n⚠️ El ejemplo no se completó correctamente.")
            print("Revisa los errores anteriores y asegúrate de que:")
            print("• Las dependencias estén instaladas (pip install -r requirements.txt)")
            print("• Los módulos del sistema estén en su lugar")
            print("• Los directorios tengan permisos adecuados")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Ejemplo cancelado por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)