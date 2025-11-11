#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 PROCESADOR DE INGESTA COGNITIVA - Sistema Completo
==================================================

FUNCIONES PRINCIPALES:
1. Procesa PDFs → Extrae texto
2. Aplica ANALYSER MÉTODO MEJORADO v2.0
3. Genera perfiles cognitivos completos  
4. Crea explicaciones detalladas con IA
5. Almacena en pensamiento_integrado_v2.db
6. Habilita COMPARADOR DE MENTES

AUTOR: Sistema Cognitivo Avanzado
FECHA: 9 NOV 2025
"""

import os
import sys
import json
import sqlite3
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

# Agregar rutas al sistema
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

# Importar módulos del sistema
try:
    from analyser_metodo_mejorado import AnalyserMetodoMejorado
    from comparador_mentes import ComparadorMentes
    MOTORES_DISPONIBLES = True
    print("✅ Motores cognitivos cargados correctamente")
except ImportError as e:
    print(f"❌ Error cargando motores: {e}")
    MOTORES_DISPONIBLES = False

# Para procesamiento de PDFs
try:
    from PyPDF2 import PdfReader
    import fitz  # pymupdf como alternativa
    PDF_DISPONIBLE = True
except ImportError:
    print("⚠️ PyPDF2 o PyMuPDF no disponible")
    PDF_DISPONIBLE = False

# Para IA de explicaciones
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    IA_DISPONIBLE = True
except ImportError:
    print("⚠️ Transformers no disponible para IA")
    IA_DISPONIBLE = False

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('colaborative/logs/ingesta_cognitiva.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProcesadorIngestaCognitiva:
    """Sistema completo de procesamiento e ingesta cognitiva"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.pdfs_path = self.base_path / "data" / "pdfs"
        self.db_path = self.base_path / "data" / "pensamiento_integrado_v2.db"
        
        # Inicializar motores
        if MOTORES_DISPONIBLES:
            self.analyser = AnalyserMetodoMejorado()
            self.comparador = ComparadorMentes()
        
        # Inicializar IA para explicaciones
        self.generador_explicaciones = None
        if IA_DISPONIBLE:
            try:
                self.generador_explicaciones = pipeline(
                    "text2text-generation",
                    model="google/flan-t5-base",
                    max_length=512
                )
                print("✅ IA para explicaciones cargada")
            except Exception as e:
                print(f"⚠️ Error cargando IA: {e}")
    
    def inicializar_base_datos(self):
        """Crea las tablas necesarias en la base de datos"""
        print("🗄️ Inicializando base de datos cognitiva...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla principal de perfiles autorales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS perfiles_autorales (
                id TEXT PRIMARY KEY,
                autor TEXT NOT NULL,
                obra TEXT NOT NULL,
                fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                perfil_json TEXT NOT NULL,
                explicacion_metodologia TEXT,
                explicacion_creatividad TEXT,
                explicacion_formalismo TEXT,
                explicacion_comparativa TEXT
            )
        ''')
        
        # Tabla de documentos procesados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documentos_procesados (
                id TEXT PRIMARY KEY,
                ruta_archivo TEXT NOT NULL,
                autor_detectado TEXT,
                fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                chunks_procesados INTEGER,
                estado TEXT DEFAULT 'procesado'
            )
        ''')
        
        # Tabla de explicaciones detalladas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS explicaciones_ia (
                id TEXT PRIMARY KEY,
                perfil_id TEXT NOT NULL,
                tipo_explicacion TEXT NOT NULL,
                contenido_explicacion TEXT NOT NULL,
                confianza REAL,
                fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (perfil_id) REFERENCES perfiles_autorales (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Base de datos inicializada")
    
    def extraer_texto_pdf(self, ruta_pdf: str) -> str:
        """Extrae texto de un PDF usando múltiples métodos"""
        print(f"📄 Extrayendo texto de: {os.path.basename(ruta_pdf)}")
        
        texto_completo = ""
        
        try:
            # Método 1: PyPDF2
            if PDF_DISPONIBLE:
                reader = PdfReader(ruta_pdf)
                for page in reader.pages:
                    texto_completo += page.extract_text() + "\n"
                print(f"✅ Extraído con PyPDF2: {len(texto_completo)} caracteres")
        except Exception as e:
            print(f"⚠️ Error con PyPDF2: {e}")
            
            # Método 2: PyMuPDF como fallback
            try:
                doc = fitz.open(ruta_pdf)
                for page in doc:
                    texto_completo += page.get_text() + "\n"
                doc.close()
                print(f"✅ Extraído con PyMuPDF: {len(texto_completo)} caracteres")
            except Exception as e2:
                print(f"❌ Error también con PyMuPDF: {e2}")
        
        return texto_completo.strip()
    
    def detectar_autor_por_contenido(self, texto: str, nombre_archivo: str) -> str:
        """Detecta el autor basándose en el contenido y nombre del archivo"""
        # Extraer autor del nombre del archivo
        nombre_base = os.path.splitext(os.path.basename(nombre_archivo))[0]
        
        # Buscar patrones de autor en el texto
        patrones_autor = [
            r"Por\s+([A-Z][a-záéíóúñ]+(?:\s+[A-Z][a-záéíóúñ]+)*)",
            r"Autor:\s*([A-Z][a-záéíóúñ]+(?:\s+[A-Z][a-záéíóúñ]+)*)",
            r"Dr\.\s+([A-Z][a-záéíóúñ]+(?:\s+[A-Z][a-záéíóúñ]+)*)"
        ]
        
        import re
        for patron in patrones_autor:
            match = re.search(patron, texto[:2000])  # Buscar en los primeros 2000 caracteres
            if match:
                return match.group(1)
        
        # Si no se encuentra, usar nombre del archivo procesado
        autor_procesado = nombre_base.replace("_", " ").replace("-", " ")
        if "teoria" in autor_procesado.lower() and "practica" in autor_procesado.lower():
            return "Daniel Brola"  # Caso específico conocido
        
        return autor_procesado.title()
    
    def generar_explicacion_con_ia(self, perfil: Dict, tipo_explicacion: str) -> str:
        """Genera explicación detallada usando IA"""
        if not self.generador_explicaciones:
            return self._generar_explicacion_manual(perfil, tipo_explicacion)
        
        prompts = {
            "metodologia": f"""
Explica en detalle la metodología jurídica de este autor basándote en estos datos:
- Razonamiento deductivo: {perfil.get('cognicion', {}).get('razonamiento_formal', {}).get('deductivo', 0):.2f}
- Formalismo jurídico: {perfil.get('estilo', {}).get('formalismo_juridico', 0):.2f}
- Uso de precedentes: {perfil.get('metodologia', {}).get('uso_precedentes', 0):.2f}

Proporciona una explicación clara y práctica de cómo este autor construye sus argumentos legales.
""",
            "creatividad": f"""
Analiza la creatividad intelectual de este autor considerando:
- Originalidad conceptual: {perfil.get('cognicion', {}).get('creatividad', {}).get('originalidad_conceptual', 0):.2f}
- Flexibilidad interpretativa: {perfil.get('metodologia', {}).get('flexibilidad_interpretativa', 0):.2f}
- Innovación argumentativa: {perfil.get('estilo', {}).get('innovacion_argumentativa', 0):.2f}

Explica qué hace único el enfoque de este autor y cómo innova en el campo jurídico.
""",
        }
        
        if tipo_explicacion not in prompts:
            return "Explicación no disponible para este tipo."
        
        try:
            resultado = self.generador_explicaciones(
                prompts[tipo_explicacion],
                max_length=300,
                do_sample=True,
                temperature=0.7
            )
            return resultado[0]['generated_text']
        except Exception as e:
            print(f"⚠️ Error generando explicación IA: {e}")
            return self._generar_explicacion_manual(perfil, tipo_explicacion)
    
    def _generar_explicacion_manual(self, perfil: Dict, tipo_explicacion: str) -> str:
        """Genera explicaciones manuales cuando la IA no está disponible"""
        explicaciones = {
            "metodologia": f"""
📚 METODOLOGÍA JURÍDICA DETECTADA:

🧠 Patrón de Razonamiento Dominante:
- Deductivo: {perfil.get('cognicion', {}).get('razonamiento_formal', {}).get('deductivo', 0):.1%}
- Inductivo: {perfil.get('cognicion', {}).get('razonamiento_formal', {}).get('inductivo', 0):.1%}
- Analógico: {perfil.get('cognicion', {}).get('razonamiento_formal', {}).get('analogico', 0):.1%}

⚖️ Enfoque Jurídico:
- Formalismo: {perfil.get('estilo', {}).get('formalismo_juridico', 0):.1%}
- Flexibilidad Interpretativa: {perfil.get('metodologia', {}).get('flexibilidad_interpretativa', 0):.1%}
- Uso de Precedentes: {perfil.get('metodologia', {}).get('uso_precedentes', 0):.1%}

Este autor construye sus argumentos mediante un enfoque {"altamente formalista" if perfil.get('estilo', {}).get('formalismo_juridico', 0) > 0.7 else "equilibrado entre formalismo y flexibilidad"}.
""",
            "creatividad": f"""
🎨 ANÁLISIS DE CREATIVIDAD INTELECTUAL:

💡 Originalidad y Innovación:
- Originalidad Conceptual: {perfil.get('cognicion', {}).get('creatividad', {}).get('originalidad_conceptual', 0):.1%}
- Innovación Argumentativa: {perfil.get('estilo', {}).get('innovacion_argumentativa', 0):.1%}
- Pensamiento Lateral: {perfil.get('cognicion', {}).get('creatividad', {}).get('pensamiento_lateral', 0):.1%}

🔬 Enfoque Intelectual:
Este autor demuestra un nivel {"alto" if perfil.get('cognicion', {}).get('creatividad', {}).get('originalidad_conceptual', 0) > 0.6 else "moderado"} de creatividad jurídica, 
{"desarrollando enfoques novedosos" if perfil.get('stilo', {}).get('innovacion_argumentativa', 0) > 0.6 else "manteniendo un equilibrio entre innovación y tradición"} 
en sus argumentaciones legales.
""",
        }
        
        return explicaciones.get(tipo_explicacion, "Explicación no disponible.")
    
    def procesar_documento(self, ruta_pdf: str) -> Optional[str]:
        """Procesa un documento PDF completo"""
        print(f"\n🔄 PROCESANDO: {os.path.basename(ruta_pdf)}")
        
        # 1. Extraer texto
        texto = self.extraer_texto_pdf(ruta_pdf)
        if len(texto) < 100:
            print("❌ Texto insuficiente extraído")
            return None
        
        # 2. Detectar autor
        autor = self.detectar_autor_por_contenido(texto, ruta_pdf)
        print(f"👤 Autor detectado: {autor}")
        
        # 3. Procesar con ANALYSER MÉTODO MEJORADO
        if not MOTORES_DISPONIBLES:
            print("❌ Motores cognitivos no disponibles")
            return None
        
        print("🧠 Aplicando análisis cognitivo...")
        perfil = self.analyser.generar_perfil_autoral_completo(texto, autor, ruta_pdf)
        
        # 4. Generar explicaciones detalladas
        print("📝 Generando explicaciones...")
        explicacion_metodologia = self.generar_explicacion_con_ia(perfil, "metodologia")
        explicacion_creatividad = self.generar_explicacion_con_ia(perfil, "creatividad")
        
        # 5. Guardar en base de datos
        doc_id = str(uuid.uuid4())
        perfil_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Guardar documento procesado
        cursor.execute('''
            INSERT INTO documentos_procesados 
            (id, ruta_archivo, autor_detectado, chunks_procesados)
            VALUES (?, ?, ?, ?)
        ''', (doc_id, ruta_pdf, autor, 1))
        
        # Guardar perfil autoral
        cursor.execute('''
            INSERT INTO perfiles_autorales 
            (id, autor, obra, perfil_json, explicacion_metodologia, explicacion_creatividad)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            perfil_id, 
            autor, 
            os.path.basename(ruta_pdf),
            json.dumps(perfil, ensure_ascii=False, indent=2),
            explicacion_metodologia,
            explicacion_creatividad
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Documento procesado y almacenado: {perfil_id}")
        return perfil_id
    
    def procesar_todos_los_pdfs(self):
        """Procesa todos los PDFs en las carpetas configuradas"""
        print("\n🚀 INICIANDO PROCESAMIENTO COMPLETO DE PDFs")
        
        # Inicializar BD
        self.inicializar_base_datos()
        
        documentos_procesados = 0
        errores = 0
        
        # Procesar PDFs en ambas carpetas
        for subcarpeta in ["general", "civil"]:
            carpeta_pdfs = self.pdfs_path / subcarpeta
            
            if not carpeta_pdfs.exists():
                print(f"⚠️ Carpeta no existe: {carpeta_pdfs}")
                continue
            
            print(f"\n📁 Procesando carpeta: {subcarpeta}")
            
            for archivo_pdf in carpeta_pdfs.glob("*.pdf"):
                try:
                    resultado = self.procesar_documento(str(archivo_pdf))
                    if resultado:
                        documentos_procesados += 1
                    else:
                        errores += 1
                except Exception as e:
                    print(f"❌ Error procesando {archivo_pdf}: {e}")
                    errores += 1
        
        print(f"\n📊 RESUMEN DE PROCESAMIENTO:")
        print(f"✅ Documentos procesados exitosamente: {documentos_procesados}")
        print(f"❌ Errores encontrados: {errores}")
        
        # Probar el comparador
        if documentos_procesados > 0:
            print("\n🧮 Probando COMPARADOR DE MENTES...")
            try:
                resultados = self.comparador.buscar_por_patron("teleologico-ensayistico")
                print(f"🔍 Encontrados {len(resultados)} autores con patrón similar")
                
                if resultados:
                    for resultado in resultados[:3]:  # Mostrar top 3
                        print(f"👤 {resultado.autor_b}: {resultado.cosine_similarity:.2%} similaridad")
            except Exception as e:
                print(f"⚠️ Error probando comparador: {e}")

def main():
    """Función principal"""
    print("🧠 PROCESADOR DE INGESTA COGNITIVA v1.0")
    print("="*50)
    
    procesador = ProcesadorIngestaCognitiva()
    procesador.procesar_todos_los_pdfs()
    
    print("\n🎉 PROCESAMIENTO COMPLETADO")
    print("\nPara usar el sistema:")
    print("1. python colaborative/scripts/sistema_referencias_autores.py")
    print("2. python colaborative/scripts/comparador_mentes.py")

if __name__ == "__main__":
    main()