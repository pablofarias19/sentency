#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
🔧 CORRECTOR SISTEMA PCA - Perfiles Cognitivo-Autorales
===========================================================
Corrige automáticamente los problemas detectados en:
- Detección de autores
- Clasificación de marcos
- Diversificación de estrategias
- Limpieza de datos
===========================================================
"""

import os
import sys
import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Rutas
BASE_PATH = Path(__file__).parent
SCRIPTS_DIR = BASE_PATH / "colaborative" / "scripts"
sys.path.append(str(SCRIPTS_DIR))

# Base de datos PCA
DB_COGNITIVA = BASE_PATH / "colaborative" / "bases_rag" / "cognitiva" / "metadatos.db"
PDFS_DIR = BASE_PATH / "colaborative" / "data" / "pdfs" / "general"

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    print("⚠️ PyMuPDF no disponible. Algunos análisis serán limitados.")
    PYMUPDF_AVAILABLE = False

def print_header(titulo: str):
    """Imprime header formateado."""
    print("\n" + "=" * 70)
    print(f"🔧 {titulo}")
    print("=" * 70)

def limpiar_texto_autor(texto: str) -> str:
    """Limpia caracteres problemáticos en nombres de autores."""
    if not texto:
        return texto
    
    # Reemplazar caracteres problemáticos
    texto = texto.replace('•', '.')
    texto = texto.replace('~', 'ñ')
    texto = re.sub(r'[^\w\s\-.,áéíóúñüÁÉÍÓÚÑÜ]', '', texto)
    
    # Normalizar espacios
    texto = ' '.join(texto.split())
    
    return texto.strip()

def detectar_autor_mejorado(archivo_pdf: str) -> Dict[str, Any]:
    """Detecta autor con algoritmo mejorado."""
    pdf_path = PDFS_DIR / archivo_pdf
    
    if not pdf_path.exists() or not PYMUPDF_AVAILABLE:
        return {"nombre": "Autor no identificado", "confianza": 0.0, "fuente": "archivo_no_encontrado"}
    
    try:
        doc = fitz.open(str(pdf_path))
        meta = doc.metadata
        primera_pagina = doc.load_page(0).get_text("text")
        doc.close()
        
        candidatos = []
        
        # 1️⃣ Metadatos PDF (alta confianza)
        if meta.get("author") and len(meta["author"].strip()) > 2:
            autor_limpio = limpiar_texto_autor(meta["author"])
            if autor_limpio and autor_limpio != "Autor no identificado":
                candidatos.append((autor_limpio, 0.8, "metadatos_pdf"))
        
        # 2️⃣ Patrones mejorados en portada
        patrones_autor = [
            # Especialista + Nombre
            r"(?i)esp\.?\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})",
            # Doctor + Nombre  
            r"(?i)dr\.?\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})",
            # Por/Autor
            r"(?i)(?:por|autor(?:a)?)\s*:?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})",
            # Nombre seguido de año
            r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})(?=\s*[-\n].*(?:201[8-9]|202[0-5]))",
            # Nombre al final de línea antes de título
            r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})(?=\s*\n\s*[A-Z][a-z].*(?:amparo|tutela|derecho))",
        ]
        
        for patron in patrones_autor:
            matches = re.findall(patron, primera_pagina)
            for match in matches:
                autor_limpio = limpiar_texto_autor(match)
                if len(autor_limpio) > 5:  # Filtrar nombres muy cortos
                    candidatos.append((autor_limpio, 0.7, "patron_portada"))
        
        # 3️⃣ Buscar en líneas específicas de la portada
        lineas = primera_pagina.split('\n')[:15]  # Primeras 15 líneas
        for i, linea in enumerate(lineas):
            linea = linea.strip()
            # Línea que contiene solo un nombre (posible autor)
            if re.match(r'^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3}$', linea):
                # Verificar que no sea parte del título
                if not any(word in linea.lower() for word in ['amparo', 'tutela', 'derecho', 'teoria', 'practica']):
                    autor_limpio = limpiar_texto_autor(linea)
                    candidatos.append((autor_limpio, 0.6, f"linea_{i+1}"))
        
        # Seleccionar mejor candidato
        if candidatos:
            # Filtrar duplicados similares
            candidatos_unicos = []
            for autor, conf, fuente in candidatos:
                # Verificar si ya existe similar
                es_duplicado = False
                for autor_existente, _, _ in candidatos_unicos:
                    if (autor.lower() in autor_existente.lower() or 
                        autor_existente.lower() in autor.lower()):
                        es_duplicado = True
                        break
                
                if not es_duplicado:
                    candidatos_unicos.append((autor, conf, fuente))
            
            # Tomar el de mayor confianza
            mejor_candidato = max(candidatos_unicos, key=lambda x: x[1])
            autor_final, confianza, fuente = mejor_candidato
            
            return {
                "nombre": autor_final,
                "confianza": round(confianza, 2),
                "fuente": fuente
            }
    
    except Exception as e:
        print(f"⚠️ Error procesando {archivo_pdf}: {e}")
    
    return {"nombre": "Autor no identificado", "confianza": 0.0, "fuente": "error_procesamiento"}

def clasificar_marco_mejorado(archivo: str, contenido: str = "") -> str:
    """Clasifica marco de referencia con lógica mejorada."""
    archivo_lower = archivo.lower()
    
    # Para documentos jurídicos, siempre clasificar como Jurídico
    keywords_juridicos = [
        'amparo', 'tutela', 'derecho', 'codigo', 'ley', 'jurisprudencia',
        'constitucion', 'civil', 'penal', 'procesal', 'recurso', 'incidente'
    ]
    
    if any(keyword in archivo_lower for keyword in keywords_juridicos):
        # Subcategorización jurídica
        if 'amparo' in archivo_lower or 'tutela' in archivo_lower:
            return "Jurídico / Constitucional"
        elif 'civil' in archivo_lower:
            return "Jurídico / Civil"
        elif 'penal' in archivo_lower:
            return "Jurídico / Penal"
        else:
            return "Jurídico / General"
    
    # Para otros casos, usar análisis de contenido
    if contenido:
        contenido_lower = contenido.lower()
        if any(keyword in contenido_lower for keyword in keywords_juridicos):
            return "Jurídico / Doctrinal"
    
    return "Sin clasificar"

def diversificar_estrategia(texto: str, autor: str) -> str:
    """Diversifica estrategias intelectuales basado en contenido real."""
    if not texto:
        return "No determinada"
    
    texto_lower = texto.lower()
    
    # Analizar patrones de razonamiento
    patrones_estrategia = {
        "Analítica": ["analizar", "examinar", "estudiar", "diseccionar", "desglosar"],
        "Crítica": ["criticar", "cuestionar", "objetar", "refutar", "controvertir"],
        "Propositiva": ["proponer", "sugerir", "recomendar", "plantear", "formular"],
        "Comparativa": ["comparar", "contrastar", "equiparar", "confrontar", "cotejar"],
        "Sistémica": ["sistema", "estructura", "organizar", "coordinar", "articular"],
        "Dogmática": ["doctrina", "principio", "dogma", "ortodoxia", "canónico"],
        "Pragmática": ["práctica", "aplicar", "implementar", "ejecutar", "operativo"],
        "Hermenéutica": ["interpretar", "hermenéutica", "exégesis", "significado", "sentido"]
    }
    
    puntuaciones = {}
    for estrategia, keywords in patrones_estrategia.items():
        puntuaciones[estrategia] = sum(1 for word in keywords if word in texto_lower)
    
    # Encontrar estrategia dominante
    if puntuaciones:
        estrategia_principal = max(puntuaciones, key=puntuaciones.get)
        if puntuaciones[estrategia_principal] > 0:
            return estrategia_principal
    
    return "Multimétodo"

def corregir_base_datos():
    """Corrige los datos en la base de datos PCA."""
    print_header("CORRECCIÓN DE BASE DE DATOS PCA")
    
    if not DB_COGNITIVA.exists():
        print("❌ Base de datos PCA no encontrada")
        return
    
    try:
        with sqlite3.connect(str(DB_COGNITIVA)) as conn:
            cursor = conn.cursor()
            
            # Obtener estructura actual de la tabla
            cursor.execute("PRAGMA table_info(perfiles_cognitivos)")
            columnas = [col[1] for col in cursor.fetchall()]
            print(f"📊 Columnas encontradas: {columnas}")
            
            # Obtener todos los registros
            cursor.execute("SELECT * FROM perfiles_cognitivos")
            registros = cursor.fetchall()
            
            print(f"📄 Registros a corregir: {len(registros)}")
            
            correcciones = 0
            
            for registro in registros:
                # Mapear campos (ajustar según estructura real)
                if len(registro) >= 4:
                    id_registro = registro[0]
                    archivo = registro[1] if len(registro) > 1 else ""
                    autor_actual = registro[2] if len(registro) > 2 else ""
                    
                    # Detectar autor mejorado
                    if not autor_actual or "no identificado" in autor_actual.lower():
                        nuevo_autor_info = detectar_autor_mejorado(archivo)
                        nuevo_autor = nuevo_autor_info["nombre"]
                        
                        if nuevo_autor != "Autor no identificado":
                            # Actualizar autor
                            cursor.execute("""
                                UPDATE perfiles_cognitivos 
                                SET autor = ? 
                                WHERE id = ?
                            """, (nuevo_autor, id_registro))
                            
                            print(f"   ✅ {archivo}: Autor corregido → {nuevo_autor}")
                            correcciones += 1
                    
                    # Limpiar caracteres problemáticos
                    elif autor_actual:
                        autor_limpio = limpiar_texto_autor(autor_actual)
                        if autor_limpio != autor_actual:
                            cursor.execute("""
                                UPDATE perfiles_cognitivos 
                                SET autor = ? 
                                WHERE id = ?
                            """, (autor_limpio, id_registro))
                            
                            print(f"   🔤 {archivo}: Caracteres limpiados → {autor_limpio}")
                            correcciones += 1
            
            conn.commit()
            print(f"\n✅ Correcciones aplicadas: {correcciones}")
            
    except Exception as e:
        print(f"❌ Error corrigiendo base de datos: {e}")

def reprocesar_perfiles_completo():
    """Reprocesa completamente los perfiles con algoritmos mejorados."""
    print_header("REPROCESAMIENTO COMPLETO DE PERFILES")
    
    # Importar módulo de ingesta cognitiva
    try:
        from ingesta_cognitiva import main as procesar_ingesta
        
        print("🔄 Reprocesando con algoritmos mejorados...")
        print("   Esto sobrescribirá los perfiles existentes con detección mejorada")
        
        respuesta = input("\n¿Continuar con reprocesamiento? (s/N): ")
        if respuesta.lower() == 's':
            procesar_ingesta()
            print("✅ Reprocesamiento completado")
        else:
            print("❌ Reprocesamiento cancelado")
            
    except ImportError:
        print("❌ No se pudo importar módulo de ingesta cognitiva")

def ejecutar_correcciones():
    """Ejecuta todas las correcciones del sistema PCA."""
    print("🔧 CORRECTOR SISTEMA PCA - PERFILES COGNITIVO-AUTORALES")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n🎯 OPCIONES DE CORRECCIÓN:")
    print("1. Corregir base de datos actual (rápido)")
    print("2. Reprocesar completamente (completo pero lento)")
    print("3. Solo diagnóstico (sin cambios)")
    
    opcion = input("\nSelecciona opción (1-3): ").strip()
    
    if opcion == "1":
        corregir_base_datos()
    elif opcion == "2":
        reprocesar_perfiles_completo()
    elif opcion == "3":
        print("ℹ️ Ejecuta: python diagnostico_pca.py")
    else:
        print("❌ Opción no válida")
    
    print("\n" + "=" * 70)
    print("🎯 CORRECCIÓN COMPLETADA")
    print("=" * 70)

if __name__ == "__main__":
    ejecutar_correcciones()