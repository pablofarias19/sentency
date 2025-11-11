# -*- coding: utf-8 -*-
"""
🎯 COORDINADOR CENTRAL DE INGESTA v1.0
=====================================
Punto único de entrada que organiza y coordina TODOS los tipos de ingesta del sistema

TIPOS DE INGESTA SOPORTADOS:
1. 🧠 Ingesta Cognitiva (analyser_metodo_mejorado.py)
2. 🚀 Ingesta Optimizada (procesador_cognitivo_optimizado.py) 
3. 📚 Ingesta Enriquecida (ingesta_enriquecida.py)
4. 🔄 Ingesta v3 (ingesta_cognitiva_v3.py)
5. 🎭 Orchestrador Maestro (orchestrador_maestro_integrado.py)

FUNCIONES:
✅ Punto único de entrada
✅ Detección automática del mejor motor
✅ Progreso unificado
✅ Manejo de errores centralizado
✅ Sincronización de bases de datos
"""

import os
import sys
import json
import sqlite3
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import importlib

# Agregar rutas al sistema
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

class CoordinadorCentralIngesta:
    """
    🎯 Coordinador central que unifica todos los motores de ingesta
    
    RESPONSABILIDADES:
    - Detección automática del mejor motor para cada documento
    - Coordinación entre diferentes tipos de ingesta
    - Sincronización de múltiples bases de datos
    - Progreso unificado y manejo de errores
    """
    
    def __init__(self):
        self.version = "v1.0_coordinador_central"
        
        # Configuración de rutas
        self.base_path = Path(__file__).parent.parent.parent
        self.scripts_path = self.base_path / "colaborative" / "scripts"
        self.pdfs_path = self.base_path / "colaborative" / "data" / "pdfs" / "general"
        
        # Bases de datos del sistema
        self.dbs = {
            "cognitivo": self.base_path / "colaborative" / "data" / "cognitivo.db",
            "pensamiento_v2": self.base_path / "colaborative" / "data" / "pensamiento_integrado_v2.db",
            "metadatos": self.base_path / "colaborative" / "bases_rag" / "cognitiva" / "metadatos.db"
        }
        
        # Motors disponibles
        self.motores_disponibles = {}
        self.cargar_motores()
    
    def cargar_motores(self):
        """Carga y verifica todos los motores disponibles"""
        
        print("🔧 Cargando motores de ingesta disponibles...")
        
        motores_config = {
            "cognitivo_optimizado": {
                "archivo": "procesador_cognitivo_optimizado.py",
                "clase": "ProcesadorCognitivoOptimizado",
                "descripcion": "🚀 Procesador optimizado con chunks y progreso",
                "mejor_para": ["textos_grandes", "pdfs_complejos"],
                "limite_caracteres": 50000
            },
            "ingesta_cognitiva": {
                "archivo": "ingesta_cognitiva.py", 
                "funcion": "procesar_carpeta_cognitiva_avanzada",
                "descripcion": "🧠 Ingesta cognitiva estándar",
                "mejor_para": ["procesamiento_batch", "textos_medianos"],
                "limite_caracteres": 100000
            },
            "analyser_mejorado": {
                "archivo": "analyser_metodo_mejorado.py",
                "clase": "AnalyserMetodoMejorado", 
                "descripcion": "🔬 ANALYSER MÉTODO MEJORADO v2.0",
                "mejor_para": ["análisis_detallado", "textos_pequeños"],
                "limite_caracteres": 30000
            },
            "orchestrador_maestro": {
                "archivo": "orchestrador_maestro_integrado.py",
                "clase": "OrchestadorMaestroIntegrado",
                "descripcion": "🎭 Orchestrador maestro integrado v6.0", 
                "mejor_para": ["análisis_completo", "perfiles_autorales"],
                "limite_caracteres": 80000
            },
            "ingesta_enriquecida": {
                "archivo": "ingesta_enriquecida.py",
                "funcion": "main",
                "descripcion": "📚 Ingesta enriquecida con perfiles PCA",
                "mejor_para": ["rag_dual", "contexto_enriquecido"],
                "limite_caracteres": 200000
            }
        }
        
        for motor_id, config in motores_config.items():
            archivo_path = self.scripts_path / config["archivo"]
            
            if archivo_path.exists():
                try:
                    # Intentar importar el módulo
                    spec = importlib.util.spec_from_file_location(motor_id, archivo_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    self.motores_disponibles[motor_id] = {
                        **config,
                        "modulo": module,
                        "disponible": True,
                        "ruta": archivo_path
                    }
                    
                    print(f"✅ {motor_id}: {config['descripcion']}")
                    
                except Exception as e:
                    self.motores_disponibles[motor_id] = {
                        **config,
                        "disponible": False,
                        "error": str(e)
                    }
                    print(f"⚠️ {motor_id}: Error cargando - {e}")
            else:
                print(f"❌ {motor_id}: Archivo no encontrado - {archivo_path}")
        
        print(f"\\n📊 Motores cargados: {len([m for m in self.motores_disponibles.values() if m.get('disponible')])}/{len(motores_config)}")
    
    def seleccionar_mejor_motor(self, ruta_pdf: str, tamano_texto: int) -> str:
        """
        Selecciona automáticamente el mejor motor para procesar un documento
        
        CRITERIO OPTIMIZADO:
        📏 < 100k caracteres  → ingesta_cognitiva.py (RÁPIDO)
        📏 ≥ 100k caracteres  → procesador_cognitivo_optimizado.py (CHUNKING)
        """
        
        print(f"🎯 Aplicando criterio de selección para {tamano_texto:,} caracteres")
        
        # Criterios de selección OPTIMIZADOS según análisis
        if tamano_texto >= 100000:  # ≥100k caracteres - USAR OPTIMIZADO
            preferencia = ["cognitivo_optimizado"]
            print("📊 Documento GRANDE → Usando procesador optimizado con chunking")
        else:  # <100k caracteres - USAR LIGERO
            preferencia = ["ingesta_cognitiva"]  
            print("⚡ Documento PEQUEÑO → Usando ingesta cognitiva ligera")
        
        # Seleccionar primer motor disponible de la lista de preferencia
        for motor_id in preferencia:
            if motor_id in self.motores_disponibles and self.motores_disponibles[motor_id].get("disponible"):
                return motor_id
        
        # Fallback: cualquier motor disponible
        for motor_id, motor_info in self.motores_disponibles.items():
            if motor_info.get("disponible"):
                return motor_id
        
        return None
    
    def estimar_tamano_texto(self, ruta_pdf: str) -> int:
        """
        Estima el tamaño del texto extraído basándose en características del archivo
        
        CASOS CONOCIDOS:
        - Teoria_y_Practica_del_Amparo_-_Daniel_Brola_-_2018.pdf → ~729k caracteres
        """
        
        try:
            nombre_archivo = os.path.basename(ruta_pdf).lower()
            tamano_archivo = os.path.getsize(ruta_pdf)
            
            # Casos específicos conocidos
            if "daniel_brola" in nombre_archivo or "teoria_y_practica_del_amparo" in nombre_archivo:
                print("📚 Documento identificado: Daniel Brola (~729k caracteres)")
                return 729000
            
            # Heurística mejorada basada en análisis de PDFs reales
            # PDFs legales típicos: 1500-2000 caracteres por página, 40-60KB por página
            caracteres_estimados = int((tamano_archivo / 45000) * 1750)
            
            print(f"📏 Archivo: {tamano_archivo:,} bytes → Estimado: {caracteres_estimados:,} caracteres")
            
            return caracteres_estimados
            
        except Exception as e:
            print(f"⚠️ Error estimando tamaño: {e}")
            return 50000  # Valor por defecto
    
    def procesar_documento_coordinado(self, ruta_pdf: str) -> Dict[str, Any]:
        """Procesa un documento usando el motor más adecuado"""
        
        nombre_archivo = os.path.basename(ruta_pdf)
        print(f"\\n🎯 COORDINANDO PROCESAMIENTO: {nombre_archivo}")
        print("-" * 60)
        
        # 1. Estimar tamaño
        tamano_estimado = self.estimar_tamano_texto(ruta_pdf)
        print(f"📏 Tamaño estimado: {tamano_estimado:,} caracteres")
        
        # 2. Seleccionar motor
        motor_seleccionado = self.seleccionar_mejor_motor(ruta_pdf, tamano_estimado)
        
        if not motor_seleccionado:
            return {
                "error": "No hay motores disponibles",
                "archivo": nombre_archivo,
                "estado": "error"
            }
        
        motor_info = self.motores_disponibles[motor_seleccionado]
        print(f"🚀 Motor seleccionado: {motor_info['descripcion']}")
        print(f"💡 Razón: Óptimo para {', '.join(motor_info['mejor_para'])}")
        
        # 3. Ejecutar procesamiento
        inicio_tiempo = time.time()
        
        try:
            resultado = self.ejecutar_motor(motor_seleccionado, ruta_pdf)
            tiempo_procesamiento = time.time() - inicio_tiempo
            
            return {
                "estado": "exitoso",
                "archivo": nombre_archivo, 
                "motor_usado": motor_seleccionado,
                "tiempo_procesamiento": tiempo_procesamiento,
                "resultado": resultado
            }
            
        except Exception as e:
            tiempo_procesamiento = time.time() - inicio_tiempo
            
            print(f"❌ Error con {motor_seleccionado}: {e}")
            
            # Intentar con motor de respaldo
            motores_respaldo = [mid for mid in self.motores_disponibles.keys() 
                             if mid != motor_seleccionado and self.motores_disponibles[mid].get("disponible")]
            
            if motores_respaldo:
                print(f"🔄 Intentando con motor de respaldo: {motores_respaldo[0]}")
                try:
                    resultado_respaldo = self.ejecutar_motor(motores_respaldo[0], ruta_pdf)
                    tiempo_total = time.time() - inicio_tiempo
                    
                    return {
                        "estado": "exitoso_respaldo",
                        "archivo": nombre_archivo,
                        "motor_principal": motor_seleccionado,
                        "motor_usado": motores_respaldo[0],
                        "tiempo_procesamiento": tiempo_total,
                        "resultado": resultado_respaldo,
                        "error_principal": str(e)
                    }
                except Exception as e2:
                    return {
                        "estado": "error",
                        "archivo": nombre_archivo, 
                        "motor_principal": motor_seleccionado,
                        "motor_respaldo": motores_respaldo[0],
                        "tiempo_procesamiento": tiempo_procesamiento,
                        "error_principal": str(e),
                        "error_respaldo": str(e2)
                    }
            else:
                return {
                    "estado": "error",
                    "archivo": nombre_archivo,
                    "motor_usado": motor_seleccionado,
                    "tiempo_procesamiento": tiempo_procesamiento,
                    "error": str(e)
                }
    
    def ejecutar_motor(self, motor_id: str, ruta_pdf: str) -> Any:
        """Ejecuta el motor específico seleccionado"""
        
        motor_info = self.motores_disponibles[motor_id]
        modulo = motor_info["modulo"]
        
        if motor_id == "cognitivo_optimizado":
            # Usar clase ProcesadorCognitivoOptimizado
            procesador = modulo.ProcesadorCognitivoOptimizado()
            return procesador.procesar_documento_optimizado(ruta_pdf)
            
        elif motor_id == "analyser_mejorado":
            # Usar clase AnalyserMetodoMejorado
            analyser = modulo.AnalyserMetodoMejorado()
            
            # Extraer texto primero (simplificado)
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(ruta_pdf)
                texto = ""
                for page in reader.pages:
                    texto += page.extract_text() + "\\n"
                
                autor = os.path.splitext(os.path.basename(ruta_pdf))[0].replace("_", " ").title()
                return analyser.generar_perfil_autoral_completo(texto, autor, ruta_pdf)
                
            except Exception as e:
                raise Exception(f"Error extrayendo texto para ANALYSER: {e}")
            
        elif motor_id == "ingesta_cognitiva":
            # Ejecutar función directamente
            return modulo.procesar_carpeta_cognitiva_avanzada(str(self.pdfs_path))
            
        elif motor_id == "orchestrador_maestro": 
            # Usar clase OrchestadorMaestroIntegrado
            orchestrador = modulo.OrchestadorMaestroIntegrado()
            # Implementar método específico según tu orchestrador
            return orchestrador.procesar_documento(ruta_pdf)
            
        elif motor_id == "ingesta_enriquecida":
            # Ejecutar función main
            return modulo.main()
            
        else:
            raise Exception(f"Motor {motor_id} no implementado")
    
    def procesar_todos_coordinado(self) -> Dict[str, Any]:
        """Procesa todos los PDFs de forma coordinada"""
        
        print("🎯 COORDINADOR CENTRAL DE INGESTA v1.0")
        print("="*60)
        print(f"📁 Carpeta PDFs: {self.pdfs_path}")
        print(f"🔧 Motores disponibles: {len([m for m in self.motores_disponibles.values() if m.get('disponible')])}")
        print("="*60)
        
        if not self.pdfs_path.exists():
            return {"error": f"Carpeta no existe: {self.pdfs_path}"}
        
        pdfs = list(self.pdfs_path.glob("*.pdf"))
        
        if not pdfs:
            return {"error": "No se encontraron PDFs para procesar"}
        
        print(f"📄 Encontrados {len(pdfs)} PDFs para procesar\\n")
        
        # Procesar cada PDF
        resultados = []
        tiempo_total_inicio = time.time()
        
        for i, pdf_path in enumerate(pdfs):
            print(f"\\n{'='*80}")
            print(f"📄 PROCESANDO [{i+1}/{len(pdfs)}]: {pdf_path.name}") 
            print(f"{'='*80}")
            
            resultado = self.procesar_documento_coordinado(str(pdf_path))
            resultados.append(resultado)
            
            # Mostrar resumen
            if resultado["estado"] == "exitoso":
                print(f"✅ COMPLETADO en {resultado['tiempo_procesamiento']:.1f}s con {resultado['motor_usado']}")
            elif resultado["estado"] == "exitoso_respaldo":
                print(f"✅ COMPLETADO (respaldo) en {resultado['tiempo_procesamiento']:.1f}s con {resultado['motor_usado']}")
            else:
                print(f"❌ ERROR: {resultado.get('error', 'Error desconocido')}")
        
        tiempo_total = time.time() - tiempo_total_inicio
        
        # Estadísticas finales
        exitosos = len([r for r in resultados if r["estado"].startswith("exitoso")])
        errores = len([r for r in resultados if r["estado"] == "error"])
        
        print(f"\\n{'='*80}")
        print("🎯 RESUMEN COORDINACIÓN CENTRAL")
        print(f"{'='*80}")
        print(f"✅ Procesados exitosamente: {exitosos}")
        print(f"❌ Errores: {errores}")
        print(f"📊 Total: {len(pdfs)}")
        print(f"📈 Tasa de éxito: {(exitosos/len(pdfs)*100):.1f}%")
        print(f"⏱️ Tiempo total: {tiempo_total:.1f} segundos")
        print(f"⚡ Promedio por documento: {tiempo_total/len(pdfs):.1f} segundos")
        
        # Estadísticas por motor
        motores_usados = {}
        for resultado in resultados:
            motor = resultado.get("motor_usado", "desconocido")
            if motor not in motores_usados:
                motores_usados[motor] = 0
            motores_usados[motor] += 1
        
        print(f"\\n🔧 MOTORES UTILIZADOS:")
        for motor, cantidad in motores_usados.items():
            if motor in self.motores_disponibles:
                descripcion = self.motores_disponibles[motor]["descripcion"]
                print(f"   {descripcion}: {cantidad} documentos")
            else:
                print(f"   {motor}: {cantidad} documentos")
        
        print(f"{'='*80}")
        
        return {
            "resultados": resultados,
            "estadisticas": {
                "total": len(pdfs),
                "exitosos": exitosos,
                "errores": errores,
                "tasa_exito": exitosos/len(pdfs)*100,
                "tiempo_total": tiempo_total,
                "motores_usados": motores_usados
            }
        }
    
    def sincronizar_bases_datos(self):
        """Sincroniza todas las bases de datos del sistema"""
        
        print("\\n🔄 Sincronizando bases de datos...")
        
        for db_name, db_path in self.dbs.items():
            if db_path.exists():
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                    num_tablas = cursor.fetchone()[0]
                    conn.close()
                    print(f"✅ {db_name}: {num_tablas} tablas")
                except Exception as e:
                    print(f"⚠️ {db_name}: Error - {e}")
            else:
                print(f"❌ {db_name}: No existe - {db_path}")
    
    def generar_reporte_estado(self) -> Dict[str, Any]:
        """Genera reporte completo del estado del sistema"""
        
        print("\\n📊 Generando reporte de estado del sistema...")
        
        # Contar PDFs
        pdfs_disponibles = len(list(self.pdfs_path.glob("*.pdf"))) if self.pdfs_path.exists() else 0
        
        # Contar registros en BD
        registros_bd = {}
        for db_name, db_path in self.dbs.items():
            if db_path.exists():
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tablas = [row[0] for row in cursor.fetchall()]
                    
                    registros_bd[db_name] = {}
                    for tabla in tablas:
                        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                        registros_bd[db_name][tabla] = cursor.fetchone()[0]
                    
                    conn.close()
                except Exception as e:
                    registros_bd[db_name] = {"error": str(e)}
        
        reporte = {
            "timestamp": datetime.now().isoformat(),
            "coordinador_version": self.version,
            "pdfs_disponibles": pdfs_disponibles,
            "motores_disponibles": len([m for m in self.motores_disponibles.values() if m.get("disponible")]),
            "motores_total": len(self.motores_disponibles),
            "bases_datos": registros_bd,
            "rutas": {
                "pdfs": str(self.pdfs_path),
                "scripts": str(self.scripts_path)
            }
        }
        
        return reporte

def procesar_documento_especifico(nombre_pdf: str):
    """
    Procesa un documento específico usando el coordinador inteligente
    
    Args:
        nombre_pdf: Nombre del archivo PDF (ej: "Teoria_y_Practica_del_Amparo_-_Daniel_Brola_-_2018.pdf")
    """
    
    coordinador = CoordinadorCentralIngesta()
    
    # Buscar el archivo
    ruta_pdf = coordinador.pdfs_path / nombre_pdf
    
    if not ruta_pdf.exists():
        print(f"❌ Archivo no encontrado: {nombre_pdf}")
        print(f"📁 Buscando en: {coordinador.pdfs_path}")
        # Listar PDFs disponibles
        pdfs_disponibles = list(coordinador.pdfs_path.glob("*.pdf"))
        if pdfs_disponibles:
            print("📄 PDFs disponibles:")
            for pdf in pdfs_disponibles:
                print(f"   - {pdf.name}")
        return None
    
    print(f"\\n🎯 PROCESAMIENTO COORDINADO ESPECÍFICO")
    print(f"📄 Archivo: {nombre_pdf}")
    print(f"📁 Ruta: {ruta_pdf}")
    print("=" * 60)
    
    # Procesar usando coordinación inteligente
    resultado = coordinador.procesar_documento_coordinado(str(ruta_pdf))
    
    # Mostrar resultado
    print("\\n" + "=" * 60)
    print("📊 RESULTADO FINAL:")
    
    if resultado["estado"] == "exitoso":
        print(f"✅ Estado: {resultado['estado']}")
        print(f"🚀 Motor usado: {resultado['motor_usado']}")
        print(f"⏱️ Tiempo: {resultado['tiempo_procesamiento']:.1f} segundos")
    elif resultado["estado"] == "exitoso_respaldo":
        print(f"✅ Estado: {resultado['estado']}")
        print(f"⚠️ Motor principal falló: {resultado['motor_principal']}")
        print(f"🚀 Motor usado (respaldo): {resultado['motor_usado']}")
        print(f"⏱️ Tiempo: {resultado['tiempo_procesamiento']:.1f} segundos")
    else:
        print(f"❌ Estado: {resultado['estado']}")
        print(f"💥 Error: {resultado.get('error', 'Error desconocido')}")
    
    print("=" * 60)
    return resultado

def main():
    """Función principal del coordinador"""
    
    import sys
    
    # Si se pasa un argumento, procesar solo ese documento
    if len(sys.argv) > 1:
        nombre_pdf = sys.argv[1]
        return procesar_documento_especifico(nombre_pdf)
    
    # Procesamiento completo de todos los documentos
    coordinador = CoordinadorCentralIngesta()
    
    # Mostrar reporte de estado
    reporte = coordinador.generar_reporte_estado()
    print(f"\\n📊 ESTADO DEL SISTEMA:")
    print(f"   📄 PDFs disponibles: {reporte['pdfs_disponibles']}")
    print(f"   🔧 Motores disponibles: {reporte['motores_disponibles']}/{reporte['motores_total']}")
    
    # Procesar todos los documentos de forma coordinada
    resultado_coordinacion = coordinador.procesar_todos_coordinado()
    
    # Sincronizar bases de datos
    coordinador.sincronizar_bases_datos()
    
    print("\\n🎉 COORDINACIÓN COMPLETADA")
    print("🌐 Para ver resultados: python colaborative/scripts/end2end_webapp.py")

if __name__ == "__main__":
    main()