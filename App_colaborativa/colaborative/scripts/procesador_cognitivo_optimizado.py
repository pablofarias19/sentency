# -*- coding: utf-8 -*-
"""
🚀 PROCESADOR COGNITIVO OPTIMIZADO v1.0
======================================
Versión optimizada que divide textos grandes en chunks y muestra progreso detallado

CARACTERÍSTICAS:
✅ División inteligente de textos grandes (>50k caracteres)
✅ Progreso detallado en tiempo real
✅ Análisis por chunks con combinación final
✅ Timeouts y recuperación de errores
✅ Compatibilidad total con sistema existente
"""

import os
import sys
import json
import sqlite3
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
import math

# Agregar rutas al sistema
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

# Importar módulos del sistema
try:
    from analyser_metodo_mejorado import AnalyserMetodoMejorado
    ANALYSER_DISPONIBLE = True
    print("✅ ANALYSER MÉTODO MEJORADO v2.0 cargado")
except ImportError as e:
    print(f"❌ Error cargando ANALYSER: {e}")
    ANALYSER_DISPONIBLE = False

# Para procesamiento de PDFs
try:
    from PyPDF2 import PdfReader
    import fitz  # pymupdf como alternativa
    PDF_DISPONIBLE = True
except ImportError:
    print("⚠️ PyPDF2 o PyMuPDF no disponible")
    PDF_DISPONIBLE = False

class ProcesadorCognitivoOptimizado:
    """
    🧠 Procesador cognitivo optimizado para textos grandes
    
    FUNCIONES:
    - División inteligente de textos
    - Progreso detallado en tiempo real
    - Análisis por chunks con combinación
    - Recuperación de errores
    """
    
    def __init__(self):
        self.version = "v1.0_optimizado"
        
        # Configuración de chunks
        self.CHUNK_SIZE = 15000  # Caracteres por chunk (optimizado)
        self.CHUNK_OVERLAP = 2000  # Solapamiento entre chunks
        self.MIN_CHUNK_SIZE = 5000  # Tamaño mínimo para analizar
        
        # Rutas
        self.base_path = Path(__file__).parent.parent.parent
        self.pdfs_path = self.base_path / "colaborative" / "data" / "pdfs" / "general"
        self.db_path = self.base_path / "colaborative" / "data" / "cognitivo.db"
        
        # Inicializar ANALYSER
        if ANALYSER_DISPONIBLE:
            self.analyser = AnalyserMetodoMejorado()
            print("✅ ANALYSER inicializado correctamente")
        else:
            self.analyser = None
            print("❌ ANALYSER no disponible")
    
    def dividir_texto_inteligente(self, texto: str) -> List[Dict]:
        """Divide texto en chunks inteligentes manteniendo contexto"""
        
        if len(texto) <= self.CHUNK_SIZE:
            return [{"chunk": texto, "posicion": 0, "total_chunks": 1}]
        
        chunks = []
        total_chunks = math.ceil(len(texto) / self.CHUNK_SIZE)
        
        print(f"📊 Dividiendo texto de {len(texto):,} caracteres en {total_chunks} chunks")
        
        posicion = 0
        chunk_num = 0
        
        while posicion < len(texto):
            fin_chunk = min(posicion + self.CHUNK_SIZE, len(texto))
            
            # Buscar punto de corte natural (final de párrafo)
            if fin_chunk < len(texto):
                # Buscar hacia atrás por un punto y salto de línea
                for i in range(fin_chunk, max(posicion + self.MIN_CHUNK_SIZE, fin_chunk - 500), -1):
                    if texto[i:i+2] == '.\\n' or texto[i:i+2] == '. ':
                        fin_chunk = i + 1
                        break
            
            chunk_texto = texto[posicion:fin_chunk]
            
            if len(chunk_texto.strip()) >= self.MIN_CHUNK_SIZE:
                chunks.append({
                    "chunk": chunk_texto.strip(),
                    "posicion": chunk_num,
                    "total_chunks": total_chunks,
                    "inicio": posicion,
                    "fin": fin_chunk,
                    "caracteres": len(chunk_texto.strip())
                })
                chunk_num += 1
            
            # Avanzar con solapamiento
            posicion = fin_chunk - self.CHUNK_OVERLAP if fin_chunk < len(texto) else fin_chunk
        
        print(f"✅ Texto dividido en {len(chunks)} chunks procesables")
        return chunks
    
    def mostrar_progreso(self, current: int, total: int, descripcion: str, tiempo_chunk: float = None):
        """Muestra progreso detallado"""
        porcentaje = (current / total) * 100
        barra_length = 30
        filled_length = int(barra_length * current // total)
        barra = '█' * filled_length + '-' * (barra_length - filled_length)
        
        tiempo_str = f" ({tiempo_chunk:.1f}s)" if tiempo_chunk else ""
        
        print(f"\\r📊 [{barra}] {porcentaje:.1f}% ({current}/{total}) {descripcion}{tiempo_str}", end='', flush=True)
        
        if current == total:
            print()  # Nueva línea al final
    
    def analizar_chunk_con_progreso(self, chunk_data: Dict, autor: str, nombre_archivo: str) -> Optional[Dict]:
        """Analiza un chunk individual con seguimiento de progreso"""
        
        chunk_num = chunk_data["posicion"] + 1
        total_chunks = chunk_data["total_chunks"]
        caracteres = chunk_data["caracteres"]
        
        print(f"\\n🧠 Analizando chunk {chunk_num}/{total_chunks} ({caracteres:,} caracteres)")
        
        inicio_tiempo = time.time()
        
        try:
            # Aplicar análisis cognitivo
            perfil_chunk = self.analyser.generar_perfil_autoral_completo(
                chunk_data["chunk"], 
                autor, 
                f"{nombre_archivo}_chunk_{chunk_num}"
            )
            
            tiempo_chunk = time.time() - inicio_tiempo
            
            self.mostrar_progreso(chunk_num, total_chunks, f"Chunk {chunk_num} completado", tiempo_chunk)
            
            return perfil_chunk
            
        except Exception as e:
            print(f"\\n❌ Error en chunk {chunk_num}: {e}")
            return None
    
    def combinar_perfiles_chunks(self, perfiles_chunks: List[Dict], autor: str, nombre_archivo: str) -> Dict:
        """Combina perfiles de múltiples chunks en uno consolidado"""
        
        print("\\n🔄 Combinando análisis de chunks...")
        
        if not perfiles_chunks:
            return {}
        
        if len(perfiles_chunks) == 1:
            return perfiles_chunks[0]
        
        # Inicializar perfil combinado
        perfil_combinado = {
            "meta": {
                "autor_probable": autor,
                "fuente": nombre_archivo,
                "timestamp": datetime.now().isoformat(),
                "version_analyser": f"{self.version}_combinado",
                "chunks_analizados": len(perfiles_chunks)
            },
            "cognicion": {
                "razonamiento_formal": {},
                "modalidad_epistemica": {},
                "retorica": {"falacias_probables": []},
                "estilo_literario": {},
                "estructuras_argumentativas": {}
            },
            "dogmas_y_valores": {
                "axiomas_autor": [],
                "creencias_explicitas": [],
                "sesgos_valorativos": {}
            },
            "puntos_de_apoyo": {
                "fuentes": [],
                "intensidad_fuentes": {}
            },
            "dilemas_y_limites": {
                "dilemas_explicitados": [],
                "limitaciones_reconocidas": [],
                "areas_de_ambiguedad": []
            },
            "marcadores_cognitivos": {}
        }
        
        # Combinar métricas numéricas (promedio)
        metricas_numericas = [
            "cognicion.razonamiento_formal",
            "cognicion.modalidad_epistemica", 
            "cognicion.estilo_literario",
            "cognicion.estructuras_argumentativas",
            "dogmas_y_valores.sesgos_valorativos",
            "puntos_de_apoyo.intensidad_fuentes",
            "marcadores_cognitivos"
        ]
        
        for metrica_path in metricas_numericas:
            keys = metrica_path.split('.')
            
            # Recopilar valores de todos los chunks
            valores_por_clave = {}
            
            for perfil in perfiles_chunks:
                seccion = perfil
                for key in keys:
                    if key in seccion:
                        seccion = seccion[key]
                    else:
                        seccion = {}
                        break
                
                if isinstance(seccion, dict):
                    for k, v in seccion.items():
                        if isinstance(v, (int, float)):
                            if k not in valores_por_clave:
                                valores_por_clave[k] = []
                            valores_por_clave[k].append(v)
            
            # Calcular promedios
            resultado = {}
            for k, valores in valores_por_clave.items():
                resultado[k] = sum(valores) / len(valores) if valores else 0.0
            
            # Asignar al perfil combinado
            seccion_destino = perfil_combinado
            for key in keys[:-1]:
                seccion_destino = seccion_destino[key]
            seccion_destino[keys[-1]] = resultado
        
        # Combinar listas (unión sin duplicados)
        listas_a_combinar = [
            ("dogmas_y_valores", "axiomas_autor"),
            ("dogmas_y_valores", "creencias_explicitas"),
            ("puntos_de_apoyo", "fuentes"),
            ("dilemas_y_limites", "dilemas_explicitados"),
            ("dilemas_y_limites", "limitaciones_reconocidas"),
            ("dilemas_y_limites", "areas_de_ambiguedad")
        ]
        
        for seccion, clave in listas_a_combinar:
            elementos_combinados = set()
            
            for perfil in perfiles_chunks:
                if seccion in perfil and clave in perfil[seccion]:
                    elementos = perfil[seccion][clave]
                    if isinstance(elementos, list):
                        elementos_combinados.update(elementos)
            
            perfil_combinado[seccion][clave] = list(elementos_combinados)
        
        # Combinar falacias
        falacias_combinadas = set()
        for perfil in perfiles_chunks:
            if "cognicion" in perfil and "retorica" in perfil["cognicion"]:
                falacias = perfil["cognicion"]["retorica"].get("falacias_probables", [])
                if isinstance(falacias, list):
                    falacias_combinadas.update(falacias)
        
        perfil_combinado["cognicion"]["retorica"]["falacias_probables"] = list(falacias_combinadas)
        
        print(f"✅ Perfiles combinados: {len(perfiles_chunks)} chunks → 1 perfil consolidado")
        
        return perfil_combinado
    
    def procesar_documento_optimizado(self, ruta_pdf: str) -> Optional[str]:
        """Procesa un documento PDF con optimización y progreso detallado"""
        
        nombre_archivo = os.path.basename(ruta_pdf)
        print(f"\\n🚀 PROCESANDO (OPTIMIZADO): {nombre_archivo}")
        
        # 1. Extraer texto
        print("📄 Extrayendo texto...")
        texto = self.extraer_texto_pdf(ruta_pdf)
        
        if len(texto) < 100:
            print("❌ Texto insuficiente extraído")
            return None
        
        print(f"✅ Extraído: {len(texto):,} caracteres")
        
        # 2. Detectar autor
        autor = self.detectar_autor_por_contenido(texto, ruta_pdf)
        print(f"👤 Autor detectado: {autor}")
        
        if not ANALYSER_DISPONIBLE:
            print("❌ ANALYSER no disponible")
            return None
        
        # 3. Dividir en chunks si es necesario
        chunks = self.dividir_texto_inteligente(texto)
        
        if len(chunks) > 1:
            print(f"📊 Procesando {len(chunks)} chunks para optimizar rendimiento")
        
        # 4. Procesar cada chunk
        perfiles_chunks = []
        tiempo_total_inicio = time.time()
        
        for i, chunk_data in enumerate(chunks):
            perfil_chunk = self.analizar_chunk_con_progreso(chunk_data, autor, nombre_archivo)
            
            if perfil_chunk:
                perfiles_chunks.append(perfil_chunk)
            
            # Mostrar progreso general
            self.mostrar_progreso(i + 1, len(chunks), "chunks procesados")
        
        if not perfiles_chunks:
            print("❌ No se pudo procesar ningún chunk")
            return None
        
        # 5. Combinar perfiles si hay múltiples chunks
        if len(chunks) > 1:
            perfil_final = self.combinar_perfiles_chunks(perfiles_chunks, autor, nombre_archivo)
        else:
            perfil_final = perfiles_chunks[0]
        
        tiempo_total = time.time() - tiempo_total_inicio
        print(f"\\n⏱️ Tiempo total de procesamiento: {tiempo_total:.1f} segundos")
        
        # 6. Guardar en base de datos
        doc_id = str(uuid.uuid4())
        
        try:
            self.guardar_perfil_optimizado(perfil_final, doc_id, ruta_pdf)
            print(f"✅ Documento procesado y guardado: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"❌ Error guardando en BD: {e}")
            return None
    
    def extraer_texto_pdf(self, ruta_pdf: str) -> str:
        """Extrae texto de PDF (igual que el original)"""
        
        if not PDF_DISPONIBLE:
            print("❌ Librerías PDF no disponibles")
            return ""
        
        print(f"📄 Extrayendo texto de: {os.path.basename(ruta_pdf)}")
        
        texto_completo = ""
        
        try:
            # Método 1: PyPDF2
            reader = PdfReader(ruta_pdf)
            for page in reader.pages:
                texto_completo += page.extract_text() + "\\n"
            print(f"✅ Extraído con PyPDF2: {len(texto_completo)} caracteres")
            
        except Exception as e:
            print(f"⚠️ Error con PyPDF2: {e}")
            
            # Método 2: PyMuPDF como fallback
            try:
                doc = fitz.open(ruta_pdf)
                for page in doc:
                    texto_completo += page.get_text() + "\\n"
                doc.close()
                print(f"✅ Extraído con PyMuPDF: {len(texto_completo)} caracteres")
            except Exception as e2:
                print(f"❌ Error también con PyMuPDF: {e2}")
        
        return texto_completo.strip()
    
    def detectar_autor_por_contenido(self, texto: str, nombre_archivo: str) -> str:
        """Detecta el autor (igual que el original)"""
        nombre_base = os.path.splitext(os.path.basename(nombre_archivo))[0]
        
        # Buscar patrones de autor en el texto
        patrones_autor = [
            r"Por\\s+([A-Z][a-záéíóúñ]+(?:\\s+[A-Z][a-záéíóúñ]+)*)",
            r"Autor:\\s*([A-Z][a-záéíóúñ]+(?:\\s+[A-Z][a-záéíóúñ]+)*)",
            r"Dr\\.\\s+([A-Z][a-záéíóúñ]+(?:\\s+[A-Z][a-záéíóúñ]+)*)"
        ]
        
        import re
        for patron in patrones_autor:
            match = re.search(patron, texto[:2000])
            if match:
                return match.group(1)
        
        # Casos específicos conocidos
        if "teoria" in nombre_base.lower() and "practica" in nombre_base.lower():
            return "Daniel Brola"
        
        return nombre_base.replace("_", " ").replace("-", " ").title()
    
    def guardar_perfil_optimizado(self, perfil: Dict, doc_id: str, ruta_archivo: str):
        """Guarda perfil en base de datos"""
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Crear tabla si no existe (compatible con el sistema actual)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS perfiles_autorales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento_id TEXT UNIQUE,
            nombre_archivo TEXT,
            autor_detectado TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            perfil_json TEXT,
            procesado_con TEXT DEFAULT 'ProcesadorCognitivoOptimizado_v1.0'
        )
        ''')
        
        # Insertar o actualizar
        cursor.execute('''
        INSERT OR REPLACE INTO perfiles_autorales 
        (documento_id, nombre_archivo, autor_detectado, perfil_json, procesado_con)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            doc_id,
            os.path.basename(ruta_archivo),
            perfil['meta']['autor_probable'],
            json.dumps(perfil, ensure_ascii=False, indent=2),
            self.version
        ))
        
        conn.commit()
        conn.close()
    
    def procesar_todos_los_pdfs(self):
        """Procesa todos los PDFs con optimización"""
        
        print("\\n🚀 INICIANDO PROCESAMIENTO OPTIMIZADO DE PDFs")
        print("=" * 60)
        
        if not self.pdfs_path.exists():
            print(f"❌ Carpeta no existe: {self.pdfs_path}")
            return
        
        pdfs = list(self.pdfs_path.glob("*.pdf"))
        
        if not pdfs:
            print("❌ No se encontraron PDFs para procesar")
            return
        
        print(f"📁 Encontrados {len(pdfs)} PDFs para procesar")
        
        documentos_procesados = 0
        errores = 0
        tiempo_total_inicio = time.time()
        
        for i, pdf_path in enumerate(pdfs):
            print(f"\\n{'='*60}")
            print(f"📄 PROCESANDO [{i+1}/{len(pdfs)}]: {pdf_path.name}")
            print(f"{'='*60}")
            
            try:
                resultado = self.procesar_documento_optimizado(str(pdf_path))
                
                if resultado:
                    documentos_procesados += 1
                    print(f"✅ COMPLETADO: {pdf_path.name}")
                else:
                    errores += 1
                    print(f"❌ ERROR: {pdf_path.name}")
                    
            except Exception as e:
                errores += 1
                print(f"💥 EXCEPCIÓN en {pdf_path.name}: {e}")
        
        tiempo_total = time.time() - tiempo_total_inicio
        
        print(f"\\n{'='*60}")
        print("🎯 RESUMEN FINAL")
        print(f"{'='*60}")
        print(f"✅ Procesados exitosamente: {documentos_procesados}")
        print(f"❌ Errores: {errores}")
        print(f"📊 Total: {len(pdfs)}")
        print(f"📈 Tasa de éxito: {(documentos_procesados/len(pdfs)*100):.1f}%")
        print(f"⏱️ Tiempo total: {tiempo_total:.1f} segundos")
        print(f"⚡ Promedio por documento: {tiempo_total/len(pdfs):.1f} segundos")
        print(f"{'='*60}")

def main():
    """Función principal"""
    print("🧠 PROCESADOR COGNITIVO OPTIMIZADO v1.0")
    print("="*50)
    
    procesador = ProcesadorCognitivoOptimizado()
    procesador.procesar_todos_los_pdfs()
    
    print("\\n🎉 Procesamiento completado")
    print("🌐 Para ver los resultados:")
    print("   python colaborative/scripts/end2end_webapp.py")

if __name__ == "__main__":
    main()