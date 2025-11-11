#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
🔍 DIAGNÓSTICO SISTEMA PCA - Perfiles Cognitivo-Autorales
===========================================================
Analiza y corrige problemas en la detección de autores,
marcos y estrategias en el sistema PCA.
===========================================================
"""

import os
import sys
import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Rutas
BASE_PATH = Path(__file__).parent
SCRIPTS_DIR = BASE_PATH / "colaborative" / "scripts"
sys.path.append(str(SCRIPTS_DIR))

# Base de datos PCA
DB_COGNITIVA = BASE_PATH / "colaborative" / "bases_rag" / "cognitiva" / "metadatos.db"
PDFS_DIR = BASE_PATH / "colaborative" / "data" / "pdfs" / "general"

def print_header(titulo: str):
    """Imprime header formateado."""
    print("\n" + "=" * 70)
    print(f"🔍 {titulo}")
    print("=" * 70)

def diagnosticar_autores():
    """Diagnóstica problemas en detección de autores."""
    print_header("DIAGNÓSTICO DE DETECCIÓN DE AUTORES")
    
    if not DB_COGNITIVA.exists():
        print("❌ Base de datos PCA no encontrada")
        return
    
    try:
        with sqlite3.connect(str(DB_COGNITIVA)) as conn:
            cursor = conn.cursor()
            
            # Obtener todos los perfiles
            cursor.execute("""
                SELECT archivo, autor, marco_referencia, estrategia_intelectual, fecha_analisis 
                FROM perfiles_cognitivos 
                ORDER BY fecha_analisis DESC
            """)
            perfiles = cursor.fetchall()
            
            print(f"📊 Total perfiles analizados: {len(perfiles)}")
            print("\n🔍 ANÁLISIS DE PROBLEMAS:")
            
            problemas = {
                "autores_no_identificados": 0,
                "marcos_incorrectos": 0,
                "estrategias_repetitivas": 0,
                "caracteres_corruptos": 0
            }
            
            for archivo, autor, marco, estrategia, fecha in perfiles:
                # Problema 1: Autores no identificados
                if not autor or "no identificado" in autor.lower():
                    problemas["autores_no_identificados"] += 1
                    print(f"   ❌ {archivo}: Autor no detectado")
                
                # Problema 2: Caracteres corruptos
                if re.search(r'[•~]|[^\w\s\-.,áéíóúñüÁÉÍÓÚÑÜ]', autor or ""):
                    problemas["caracteres_corruptos"] += 1
                    print(f"   🔤 {archivo}: Caracteres corruptos en autor: '{autor}'")
                
                # Problema 3: Marcos incorrectos para documentos jurídicos
                if marco and ("Económico" in marco or "Liberal" in marco):
                    # Verificar si es documento jurídico
                    archivo_lower = archivo.lower()
                    if any(word in archivo_lower for word in ["amparo", "tutela", "derecho", "jurisprudencia", "codigo"]):
                        problemas["marcos_incorrectos"] += 1
                        print(f"   ⚖️ {archivo}: Marco incorrecto '{marco}' para documento jurídico")
                
                # Problema 4: Estrategias repetitivas
                if estrategia == "Comparativa":
                    problemas["estrategias_repetitivas"] += 1
            
            print(f"\n📈 RESUMEN DE PROBLEMAS:")
            print(f"   👤 Autores no identificados: {problemas['autores_no_identificados']}")
            print(f"   🔤 Caracteres corruptos: {problemas['caracteres_corruptos']}")
            print(f"   ⚖️ Marcos incorrectos: {problemas['marcos_incorrectos']}")
            print(f"   🔄 Estrategias repetitivas: {problemas['estrategias_repetitivas']}")
            
            return problemas
            
    except Exception as e:
        print(f"❌ Error diagnosticando: {e}")
        return {}

def analizar_pdfs_originales():
    """Analiza los PDFs originales para detectar autores reales."""
    print_header("ANÁLISIS DE PDFs ORIGINALES")
    
    if not PDFS_DIR.exists():
        print("❌ Directorio de PDFs no encontrado")
        return
    
    pdfs = list(PDFS_DIR.glob("*.pdf"))
    print(f"📄 PDFs encontrados: {len(pdfs)}")
    
    try:
        import fitz  # PyMuPDF
        
        for pdf_path in pdfs:
            print(f"\n📖 Analizando: {pdf_path.name}")
            
            try:
                doc = fitz.open(str(pdf_path))
                
                # Metadatos
                meta = doc.metadata
                if meta.get("author"):
                    print(f"   👤 Autor en metadatos: {meta['author']}")
                
                # Primera página
                primera_pagina = doc.load_page(0).get_text("text")
                
                # Buscar patrones de autor
                patrones_autor = [
                    r"(?i)(?:por|autor(?:a)?)\s*:?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})",
                    r"(?i)dr\.?\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,2})",
                    r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,2})(?=\s*\n.*(?:2018|2019|2020|2021|2022|2023|2024|2025))"
                ]
                
                autores_detectados = []
                for patron in patrones_autor:
                    matches = re.findall(patron, primera_pagina)
                    autores_detectados.extend(matches)
                
                if autores_detectados:
                    print(f"   ✅ Autores detectados: {', '.join(set(autores_detectados))}")
                else:
                    print("   ❌ No se detectaron autores en portada")
                    # Mostrar primeras líneas para análisis manual
                    lineas = primera_pagina.split('\n')[:10]
                    print("   📝 Primeras líneas:")
                    for i, linea in enumerate(lineas):
                        if linea.strip():
                            print(f"      {i+1}: {linea.strip()}")
                
                doc.close()
                
            except Exception as e:
                print(f"   ❌ Error procesando PDF: {e}")
                
    except ImportError:
        print("❌ PyMuPDF no disponible. Instala con: pip install PyMuPDF")

def proponer_correcciones():
    """Propone correcciones específicas para los problemas detectados."""
    print_header("PROPUESTAS DE CORRECCIÓN")
    
    print("""
🔧 CORRECCIONES RECOMENDADAS:

1️⃣ DETECCIÓN DE AUTORES MEJORADA:
   • Usar más patrones de extracción de portada
   • Aplicar limpieza de caracteres Unicode
   • Combinar metadatos PDF + análisis de layout
   • Implementar validación de nombres comunes

2️⃣ CLASIFICACIÓN DE MARCOS:
   • Forzar clasificación "Jurídico" para documentos legales
   • Usar keywords del contenido para determinar marco
   • Evitar clasificaciones económicas en textos jurídicos

3️⃣ DIVERSIFICACIÓN DE ESTRATEGIAS:
   • Analizar estructura argumentativa real
   • Detectar tipos de razonamiento (deductivo, inductivo, etc.)
   • Clasificar según metodología jurídica utilizada

4️⃣ LIMPIEZA DE DATOS:
   • Normalizar encoding UTF-8
   • Filtrar caracteres especiales problemáticos
   • Aplicar corrección automática de texto
    """)

def ejecutar_diagnostico_completo():
    """Ejecuta diagnóstico completo del sistema PCA."""
    print("🔍 DIAGNÓSTICO SISTEMA PCA - PERFILES COGNITIVO-AUTORALES")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Diagnosticar problemas en BD
    problemas = diagnosticar_autores()
    
    # 2. Analizar PDFs originales
    analizar_pdfs_originales()
    
    # 3. Proponer correcciones
    proponer_correcciones()
    
    print("\n" + "=" * 70)
    print("🎯 DIAGNÓSTICO COMPLETADO")
    print("=" * 70)
    
    if problemas:
        total_problemas = sum(problemas.values())
        print(f"📊 Total problemas detectados: {total_problemas}")
        print("\n💡 SIGUIENTE PASO: Ejecutar corrector automático")
        print("   python corregir_sistema_pca.py")
    else:
        print("✅ No se detectaron problemas mayores")

if __name__ == "__main__":
    ejecutar_diagnostico_completo()