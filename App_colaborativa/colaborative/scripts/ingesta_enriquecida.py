# -*- coding: utf-8 -*-
"""
Ingesta Enriquecida con Perfil Cognitivo-Autoral
Procesa documentos con análisis estructural + perfiles cognitivos → FAISS_A + FAISS_B
"""

import os
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import List, Dict, Any

# Asegurar imports del proyecto
sys.path.append(os.path.dirname(__file__))

# Imports locales
try:
    from extractor_pdf_enriquecido import extract_from_pdf_enriquecido
    from profiles_rag import ProfilesStore, build_firma
    from autoaprendizaje import guardar_autoevaluacion
    print("✅ Imports locales cargados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos locales: {e}")
    print("Asegúrate de que están en el directorio correcto")
    raise

# Import del sistema RAG existente (ajustar según tu estructura)
try:
    # Buscar el módulo RAG en el proyecto
    possible_paths = [
        "rag_build",
        "ai_engine", 
        "pipeline_resumen_doctrinario"
    ]
    
    rag_module = None
    for module_name in possible_paths:
        try:
            rag_module = __import__(module_name)
            if hasattr(rag_module, 'ingest_documents') or hasattr(rag_module, 'process_document'):
                print(f"✅ Módulo RAG encontrado: {module_name}")
                break
        except ImportError:
            continue
    
    if not rag_module:
        print("⚠️ No se encontró módulo RAG específico, usando modo básico")
        
except Exception as e:
    print(f"⚠️ Error cargando sistema RAG: {e}")
    rag_module = None

# ==========================================================
# 🔹 FUNCIONES AUXILIARES
# ==========================================================
def detectar_metodologia_predominante(doc_data: Dict) -> str:
    """Detecta la metodología más común en el documento"""
    if not doc_data.get("chunks"):
        return "No especificada"
    
    metodologias = []
    for chunk in doc_data["chunks"]:
        labels = chunk.get("labels", {})
        if "metodologia" in labels:
            metodologias.append(labels["metodologia"])
    
    if metodologias:
        return Counter(metodologias).most_common(1)[0][0]
    return "No especificada"

def detectar_marco_predominante(doc_data: Dict) -> str:
    """Detecta el marco de referencia más común"""
    if not doc_data.get("chunks"):
        return "No identificado"
    
    marcos = []
    for chunk in doc_data["chunks"]:
        labels = chunk.get("labels", {})
        if "marco_referencia" in labels and labels["marco_referencia"] != "No identificado":
            marcos.append(labels["marco_referencia"])
    
    if marcos:
        return Counter(marcos).most_common(1)[0][0]
    return "No identificado"

def preparar_para_rag_tradicional(doc_data: Dict) -> List[Dict]:
    """
    Convierte datos enriquecidos al formato esperado por el RAG tradicional.
    Mantiene compatibilidad con el sistema existente.
    """
    documentos = []
    
    for chunk in doc_data["chunks"]:
        # Formato básico para RAG
        doc_tradicional = {
            "content": chunk["texto"],
            "source": chunk["metadata"]["fuente"],
            "title": chunk["metadata"].get("titulo", "Sin título"),
            "author": chunk["metadata"].get("autor", "Sin autor"),
            "section": chunk["metadata"].get("seccion", 1),
            # Mantener metadatos enriquecidos como extra
            "enriched_metadata": chunk["metadata"],
            "enriched_labels": chunk["labels"]
        }
        documentos.append(doc_tradicional)
    
    return documentos

# ==========================================================
# 🔹 FUNCIÓN PRINCIPAL: INGESTA ENRIQUECIDA
# ==========================================================
def ingestar_pdf_enriquecido(ruta_pdf: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Procesa un PDF con análisis cognitivo-autoral completo.
    
    Flujo:
    1. Extracción estructural + PCA
    2. Ingesta a FAISS_A (contenido tradicional)
    3. Construcción de perfiles → FAISS_B
    4. Registro en autoaprendizaje
    
    Args:
        ruta_pdf: Ruta al archivo PDF
        verbose: Mostrar información detallada
        
    Returns:
        Diccionario con estadísticas del procesamiento
    """
    if verbose:
        print(f"\n🔍 INGESTA ENRIQUECIDA: {Path(ruta_pdf).name}")
        print("=" * 60)
    
    try:
        # ==========================================
        # PASO 1: EXTRACCIÓN ENRIQUECIDA
        # ==========================================
        if verbose:
            print("📄 Extrayendo contenido con análisis PCA...")
        
        doc_data = extract_from_pdf_enriquecido(ruta_pdf)
        meta = doc_data["meta"]
        chunks = doc_data["chunks"]
        
        if verbose:
            print(f"✅ Extraído: {meta['titulo']}")
            print(f"📊 Chunks: {len(chunks)}")
            print(f"👤 Autor: {meta['autor']}")
            print(f"📅 Año: {meta['anio']}")
        
        # ==========================================
        # PASO 2: INGESTA RAG TRADICIONAL (FAISS_A)
        # ==========================================
        if verbose:
            print("\n🔗 Ingresando a sistema RAG tradicional...")
            
        # Convertir a formato compatible
        docs_tradicionales = preparar_para_rag_tradicional(doc_data)
        
        # Intentar ingesta con sistema existente
        try:
            if rag_module and hasattr(rag_module, 'ingest_documents'):
                rag_module.ingest_documents(docs_tradicionales)
                if verbose:
                    print("✅ Ingesta RAG tradicional completada")
            elif rag_module and hasattr(rag_module, 'process_document'):
                for doc in docs_tradicionales:
                    rag_module.process_document(doc)
                if verbose:
                    print("✅ Procesamiento RAG individual completado")
            else:
                if verbose:
                    print("⚠️ Sistema RAG no disponible, solo procesamiento PCA")
        except Exception as e:
            if verbose:
                print(f"⚠️ Error en ingesta RAG: {e}")
        
        # ==========================================
        # PASO 3: PERFILES COGNITIVOS (FAISS_B)
        # ==========================================
        if verbose:
            print("\n🧠 Construyendo perfiles cognitivos...")
        
        store = ProfilesStore()
        rows_perfiles = []
        
        # Procesar cada chunk para crear perfiles
        for chunk in chunks:
            labels = chunk.get("labels", {})
            metadata = chunk.get("metadata", {})
            
            # Construir perfil cognitivo
            perfil = {
                "marco_referencia": labels.get("marco_referencia"),
                "critica_a": labels.get("critica_a", []),
                "motivo_intelectual": labels.get("motivo_intelectual"),
                "estrategia": labels.get("estrategia"),
                "autores_mencionados": labels.get("autores_mencionados", [])
            }
            
            # Construir firma cognitiva
            firma = build_firma(
                perfil=perfil,
                meta_doc=meta,
                titulo_seccion=labels.get("tema_especifico", "Sin título"),
                palabras_clave=labels.get("palabras_clave", [])
            )
            
            # Preparar fila para almacén
            row_perfil = {
                "doc_hash": meta["hash"],
                "doc_titulo": meta["titulo"],
                "autor_detectado": meta.get("autor", "No identificado"),
                "nivel": "seccion",
                "perfil_json": perfil,
                "firma": firma
            }
            rows_perfiles.append(row_perfil)
        
        # Añadir perfiles al almacén vectorial
        if rows_perfiles:
            store.add_profiles(rows_perfiles)
            if verbose:
                print(f"✅ {len(rows_perfiles)} perfiles almacenados en FAISS_B")
        
        # ==========================================
        # PASO 4: REGISTRO EN AUTOAPRENDIZAJE
        # ==========================================
        if verbose:
            print("\n📝 Registrando en sistema de autoaprendizaje...")
        
        # Estadísticas del documento
        metodologia_dom = detectar_metodologia_predominante(doc_data)
        marco_dom = detectar_marco_predominante(doc_data)
        
        info_documento = (
            f"DOCUMENTO: {meta.get('titulo')} ({meta.get('anio')}) | "
            f"AUTOR: {meta.get('autor')} | "
            f"METODOLOGÍA: {metodologia_dom} | "
            f"MARCO: {marco_dom} | "
            f"CHUNKS: {len(chunks)} | "
            f"PERFILES: {len(rows_perfiles)}"
        )
        
        autoevaluacion_texto = (
            f"Ingesta enriquecida completada exitosamente. "
            f"Estructura documental analizada + perfiles cognitivos registrados. "
            f"Stats: {dict(doc_data.get('stats', {}).get('metodologias', {}))}"
        )
        
        # Guardar registro
        guardar_autoevaluacion(
            modelo="Ingesta Enriquecida PCA",
            pregunta="Carga documental estructural",
            concepto=info_documento,
            autoevaluacion=autoevaluacion_texto,
            puntaje=9.0,  # Alta confianza en proceso estructurado
            prompt_base="Extracción PDF + Análisis Cognitivo-Autoral + Doble RAG"
        )
        
        if verbose:
            print("✅ Registro de autoaprendizaje guardado")
        
        # ==========================================
        # RESUMEN FINAL
        # ==========================================
        resultado = {
            "status": "success",
            "documento": {
                "titulo": meta["titulo"],
                "autor": meta["autor"],
                "hash": meta["hash"],
                "chunks_procesados": len(chunks),
                "perfiles_creados": len(rows_perfiles)
            },
            "analisis": {
                "metodologia_predominante": metodologia_dom,
                "marco_predominante": marco_dom,
                "estadisticas": doc_data.get("stats", {})
            },
            "fecha_procesamiento": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if verbose:
            print(f"\n✅ INGESTA COMPLETADA: {meta['titulo']}")
            print(f"📊 Chunks: {len(chunks)} | Perfiles: {len(rows_perfiles)}")
            print("=" * 60)
        
        return resultado
        
    except Exception as e:
        error_msg = f"Error procesando {ruta_pdf}: {str(e)}"
        if verbose:
            print(f"\n❌ {error_msg}")
        
        # Registrar error en autoaprendizaje
        try:
            guardar_autoevaluacion(
                modelo="Ingesta Enriquecida PCA",
                pregunta="Error en carga documental",
                concepto=f"ARCHIVO: {ruta_pdf}",
                autoevaluacion=error_msg,
                puntaje=0.0,
                prompt_base="Error de procesamiento"
            )
        except:
            pass
        
        return {
            "status": "error",
            "error": error_msg,
            "archivo": ruta_pdf
        }

# ==========================================================
# 🔹 INGESTA MASIVA DE CARPETA
# ==========================================================
def ingestar_carpeta_enriquecida(carpeta_pdf: str = "colaborative/data/pdfs/general", 
                                patron: str = "*.pdf",
                                verbose: bool = True) -> Dict[str, Any]:
    """
    Procesa todos los PDFs de una carpeta con ingesta enriquecida.
    
    Args:
        carpeta_pdf: Ruta de la carpeta con PDFs
        patron: Patrón de archivos (default: "*.pdf")
        verbose: Mostrar progreso detallado
        
    Returns:
        Estadísticas del procesamiento masivo
    """
    carpeta = Path(carpeta_pdf)
    
    if not carpeta.exists():
        if verbose:
            print(f"📁 Creando carpeta: {carpeta}")
        carpeta.mkdir(parents=True, exist_ok=True)
    
    # Buscar PDFs
    pdfs = list(carpeta.glob(patron))
    
    if not pdfs:
        msg = f"No se encontraron archivos {patron} en {carpeta}"
        if verbose:
            print(f"⚠️ {msg}")
        return {"status": "no_files", "message": msg}
    
    if verbose:
        print(f"\n📚 INGESTA MASIVA: {len(pdfs)} archivos")
        print("=" * 60)
    
    # Estadísticas
    stats = {
        "total_archivos": len(pdfs),
        "procesados_ok": 0,
        "errores": 0,
        "resultados": [],
        "inicio": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Procesar cada PDF
    for i, pdf_path in enumerate(pdfs, 1):
        if verbose:
            print(f"\n[{i}/{len(pdfs)}] {pdf_path.name}")
        
        resultado = ingestar_pdf_enriquecido(str(pdf_path), verbose=verbose)
        stats["resultados"].append(resultado)
        
        if resultado["status"] == "success":
            stats["procesados_ok"] += 1
        else:
            stats["errores"] += 1
    
    # Resumen final
    stats["fin"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if verbose:
        print(f"\n🎯 RESUMEN FINAL:")
        print(f"✅ Procesados: {stats['procesados_ok']}")
        print(f"❌ Errores: {stats['errores']}")
        print(f"📊 Total: {stats['total_archivos']}")
        print("=" * 60)
    
    return stats

# ==========================================================
# 🔹 FUNCIÓN PRINCIPAL
# ==========================================================
if __name__ == "__main__":
    print("🚀 SISTEMA DE INGESTA ENRIQUECIDA CON PCA")
    print("Procesamiento: PDF → Análisis Estructural → RAG Dual (FAISS_A + FAISS_B)")
    print()
    
    # Configuración por defecto
    carpeta_pdfs = "colaborative/data/pdfs/general"
    
    # Crear carpeta si no existe
    Path(carpeta_pdfs).mkdir(parents=True, exist_ok=True)
    
    # Verificar si hay PDFs
    pdfs_disponibles = list(Path(carpeta_pdfs).glob("*.pdf"))
    
    if pdfs_disponibles:
        print(f"📚 Encontrados {len(pdfs_disponibles)} PDFs en {carpeta_pdfs}")
        print("Procesando...")
        
        # Procesar carpeta completa
        resultado = ingestar_carpeta_enriquecida(carpeta_pdfs, verbose=True)
        
        if resultado["status"] != "no_files":
            # Registrar estadísticas globales
            guardar_autoevaluacion(
                modelo="Ingesta Masiva PCA",
                pregunta="Procesamiento de corpus documental",
                concepto=f"Procesados: {resultado['procesados_ok']}/{resultado['total_archivos']} documentos",
                autoevaluacion=f"Ingesta masiva completada. Errores: {resultado['errores']}",
                puntaje=8.0 if resultado['errores'] == 0 else 6.0,
                prompt_base="Sistema de ingesta enriquecida con PCA"
            )
            
        print("\n✅ Proceso completado. Revisa logs en /autoevaluaciones")
        
    else:
        print(f"📁 No se encontraron PDFs en: {carpeta_pdfs}")
        print(f"💡 Coloca archivos PDF en esa carpeta y ejecuta nuevamente.")
        
        # Crear archivo de ayuda
        readme_path = Path(carpeta_pdfs) / "README.txt"
        readme_path.write_text(
            "INSTRUCCIONES:\n"
            "1. Coloca archivos PDF en esta carpeta\n"
            "2. Ejecuta: python ingesta_enriquecida.py\n"
            "3. Los documentos serán procesados con análisis PCA\n"
            "4. Consulta resultados en /autoevaluaciones\n",
            encoding="utf-8"
        )
        print(f"📄 Creado: {readme_path}")