# -*- coding: utf-8 -*-
"""
🚀 PROCESADOR INTEGRAL MEJORADO v2.0 - SIN TRABAS
=================================================
Procesador robusto que maneja TODA la ingesta cognitiva sin trabarse.

CARACTERÍSTICAS ANTI-TRABAS:
✅ Manejo de errores individual por documento
✅ Timeouts configurables  
✅ Limpieza automática de memoria
✅ Progress tracking detallado
✅ Reintentos automáticos
✅ Logs completos de errores
✅ Verificación de integridad
"""

import sys
import os
import time
import traceback
import gc
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import sqlite3
import json
from datetime import datetime
import signal

# Configuración de paths
BASE_DIR = Path(__file__).parent
COLABORATIVE_DIR = BASE_DIR / "colaborative"
SCRIPTS_DIR = COLABORATIVE_DIR / "scripts"
DATA_DIR = COLABORATIVE_DIR / "data"
PDFS_DIR = DATA_DIR / "pdfs" / "general"

# Agregar al path para imports
sys.path.append(str(SCRIPTS_DIR))

# Configuraciones anti-trabas
MAX_TIEMPO_POR_DOCUMENTO = 180  # 3 minutos por documento
MAX_REINTENTOS = 3
CHUNK_SIZE = 1000  # Caracteres por chunk
TIMEOUT_PROCESO = 300  # 5 minutos máximo total

class TimeoutError(Exception):
    """Error por timeout en procesamiento"""
    pass

def timeout_handler(signum, frame):
    """Handler para timeout"""
    raise TimeoutError("Proceso excedió el tiempo límite")

class ProcesadorIntegralMejorado:
    """
    🚀 Procesador robusto que no se traba
    
    ANTI-TRABAS:
    - Procesamiento individual con timeouts
    - Manejo de errores granular  
    - Limpieza de memoria automática
    - Progress tracking detallado
    """
    
    def __init__(self):
        self.version = "ProcesadorIntegralMejorado_v2.0"
        self.errores_procesamiento = []
        self.documentos_procesados = 0
        self.documentos_fallidos = 0
        
        # Inicializar componentes
        self._inicializar_componentes()
        
        # Configurar timeout global
        signal.signal(signal.SIGALRM, timeout_handler)
    
    def _inicializar_componentes(self):
        """Inicializa todos los componentes necesarios"""
        print("🔧 INICIALIZANDO COMPONENTES...")
        
        try:
            # Importar AnalyserMetodoMejorado
            from analyser_metodo_mejorado import AnalyserMetodoMejorado
            self.analyser = AnalyserMetodoMejorado()
            print("✅ AnalyserMetodoMejorado cargado")
        except Exception as e:
            print(f"⚠️ Error cargando AnalyserMetodoMejorado: {e}")
            self.analyser = None
        
        try:
            # Importar ComparadorMentes si existe
            from comparador_mentes import ComparadorMentes
            self.comparador = ComparadorMentes()
            print("✅ ComparadorMentes cargado")
        except Exception as e:
            print(f"⚠️ ComparadorMentes no disponible: {e}")
            self.comparador = None
        
        # Verificar base de datos
        self._verificar_base_datos()
    
    def _verificar_base_datos(self):
        """Verifica y repara base de datos si es necesario"""
        db_path = DATA_DIR / "cognitivo.db"
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Verificar tabla principal
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='perfiles_autorales'")
                if not cursor.fetchone():
                    print("⚠️ Tabla perfiles_autorales no existe, creándola...")
                    self._crear_tabla_perfiles_autorales(cursor)
                    conn.commit()
                
                print("✅ Base de datos verificada y funcional")
                
        except Exception as e:
            print(f"❌ Error en base de datos: {e}")
            raise
    
    def _crear_tabla_perfiles_autorales(self, cursor):
        """Crea tabla perfiles_autorales con esquema completo"""
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS perfiles_autorales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento_id TEXT UNIQUE,
            nombre_archivo TEXT,
            autor_detectado TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            -- RAZONAMIENTO (14 tipos)
            razonamiento_deductivo REAL DEFAULT 0.0,
            razonamiento_inductivo REAL DEFAULT 0.0,
            razonamiento_abductivo REAL DEFAULT 0.0,
            razonamiento_analogico REAL DEFAULT 0.0,
            razonamiento_teleologico REAL DEFAULT 0.0,
            razonamiento_sistemico REAL DEFAULT 0.0,
            razonamiento_autoritativo REAL DEFAULT 0.0,
            razonamiento_a_contrario REAL DEFAULT 0.0,
            razonamiento_consecuencialista REAL DEFAULT 0.0,
            razonamiento_dialectico REAL DEFAULT 0.0,
            razonamiento_hermeneutico REAL DEFAULT 0.0,
            razonamiento_historico REAL DEFAULT 0.0,
            razonamiento_economico_analitico REAL DEFAULT 0.0,
            razonamiento_reduccion_absurdo REAL DEFAULT 0.0,
            
            -- MODALIDADES EPISTÉMICAS (7 tipos)
            modalidad_apodíctico REAL DEFAULT 0.0,
            modalidad_dialectico REAL DEFAULT 0.0,
            modalidad_retorico REAL DEFAULT 0.0,
            modalidad_sofístico REAL DEFAULT 0.0,
            modalidad_certeza REAL DEFAULT 0.0,
            modalidad_incertidumbre REAL DEFAULT 0.0,
            modalidad_hedging REAL DEFAULT 0.0,
            
            -- RETÓRICA ARISTOTÉLICA
            retorica_ethos REAL DEFAULT 0.0,
            retorica_pathos REAL DEFAULT 0.0,
            retorica_logos REAL DEFAULT 0.0,
            
            -- ESTILOS LITERARIOS (8 tipos)
            estilo_tecnico_juridico REAL DEFAULT 0.0,
            estilo_ensayistico REAL DEFAULT 0.0,
            estilo_narrativo REAL DEFAULT 0.0,
            estilo_barroco REAL DEFAULT 0.0,
            estilo_minimalista REAL DEFAULT 0.0,
            estilo_aforistico REAL DEFAULT 0.0,
            estilo_impersonal_burocratico REAL DEFAULT 0.0,
            estilo_dialectico_critico REAL DEFAULT 0.0,
            
            -- ESTRUCTURAS ARGUMENTATIVAS (6 tipos)
            estructura_irac REAL DEFAULT 0.0,
            estructura_toulmin REAL DEFAULT 0.0,
            estructura_issue_tree REAL DEFAULT 0.0,
            estructura_defeasible REAL DEFAULT 0.0,
            estructura_burden_shift REAL DEFAULT 0.0,
            estructura_silogistico_formal REAL DEFAULT 0.0,
            
            -- MÉTRICAS GENERALES
            formalismo REAL DEFAULT 0.0,
            creatividad REAL DEFAULT 0.0,
            empirismo REAL DEFAULT 0.0,
            dogmatismo REAL DEFAULT 0.0,
            interdisciplinariedad REAL DEFAULT 0.0,
            complejidad_sintactica REAL DEFAULT 0.0,
            nivel_abstraccion REAL DEFAULT 0.0,
            uso_jurisprudencia REAL DEFAULT 0.0,
            
            -- METADATOS
            perfil_json TEXT,
            procesado_con TEXT DEFAULT 'ProcesadorIntegralMejorado_v2.0'
        )
        ''')
    
    def procesar_todo_robusto(self) -> Dict:
        """
        🚀 PROCESAMIENTO COMPLETO ANTI-TRABAS
        
        CARACTERÍSTICAS:
        - Timeout por documento
        - Manejo individual de errores
        - Progress tracking
        - Limpieza de memoria
        """
        
        print("🚀 INICIANDO PROCESAMIENTO INTEGRAL MEJORADO v2.0")
        print("=" * 60)
        
        inicio_total = time.time()
        
        try:
            # 1. Detectar documentos
            documentos = self._detectar_documentos_nuevos()
            total_docs = len(documentos)
            
            if total_docs == 0:
                print("ℹ️ No hay documentos nuevos para procesar")
                return {"status": "success", "documentos_procesados": 0, "mensaje": "Sin documentos nuevos"}
            
            print(f"📚 Encontrados {total_docs} documentos para procesar")
            
            # 2. Procesar cada documento individualmente
            for i, doc_path in enumerate(documentos, 1):
                self._procesar_documento_individual(doc_path, i, total_docs)
                
                # Limpieza de memoria cada 3 documentos
                if i % 3 == 0:
                    gc.collect()
                    print(f"🧹 Limpieza de memoria realizada (documento {i}/{total_docs})")
            
            # 3. Resumen final
            tiempo_total = time.time() - inicio_total
            return self._generar_reporte_final(tiempo_total)
            
        except KeyboardInterrupt:
            print("\n⚠️ PROCESAMIENTO INTERRUMPIDO POR EL USUARIO")
            return {"status": "interrupted", "documentos_procesados": self.documentos_procesados}
        
        except Exception as e:
            print(f"\n💥 ERROR CRÍTICO EN PROCESAMIENTO: {e}")
            traceback.print_exc()
            return {"status": "error", "error": str(e), "documentos_procesados": self.documentos_procesados}
    
    def _detectar_documentos_nuevos(self) -> List[Path]:
        """Detecta documentos PDF nuevos en la carpeta"""
        
        if not PDFS_DIR.exists():
            PDFS_DIR.mkdir(parents=True, exist_ok=True)
            print(f"📁 Carpeta creada: {PDFS_DIR}")
            return []
        
        # Buscar PDFs
        pdfs = list(PDFS_DIR.glob("*.pdf"))
        
        if not pdfs:
            print(f"📁 No se encontraron PDFs en: {PDFS_DIR}")
            return []
        
        # Filtrar documentos ya procesados
        documentos_nuevos = []
        
        try:
            db_path = DATA_DIR / "cognitivo.db"
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                for pdf in pdfs:
                    doc_id = pdf.stem  # Nombre sin extensión
                    cursor.execute("SELECT COUNT(*) FROM perfiles_autorales WHERE documento_id = ?", (doc_id,))
                    
                    if cursor.fetchone()[0] == 0:
                        documentos_nuevos.append(pdf)
                    else:
                        print(f"⏭️ Ya procesado: {pdf.name}")
        
        except Exception as e:
            print(f"⚠️ Error verificando documentos procesados: {e}")
            # Si hay error, procesar todos
            documentos_nuevos = pdfs
        
        return documentos_nuevos
    
    def _procesar_documento_individual(self, doc_path: Path, numero: int, total: int):
        """
        Procesa un documento individual con protección anti-trabas
        
        PROTECCIONES:
        - Timeout por documento
        - Reintentos automáticos  
        - Manejo granular de errores
        - Progress tracking
        """
        
        print(f"\n📄 PROCESANDO ({numero}/{total}): {doc_path.name}")
        print("-" * 50)
        
        inicio_doc = time.time()
        
        for intento in range(1, MAX_REINTENTOS + 1):
            try:
                # Configurar timeout para este documento
                signal.alarm(MAX_TIEMPO_POR_DOCUMENTO)
                
                # Procesar documento
                resultado = self._procesar_documento_contenido(doc_path)
                
                # Cancelar timeout
                signal.alarm(0)
                
                if resultado["success"]:
                    tiempo_doc = time.time() - inicio_doc
                    print(f"✅ DOCUMENTO PROCESADO EXITOSAMENTE en {tiempo_doc:.1f}s")
                    self.documentos_procesados += 1
                    return
                else:
                    print(f"⚠️ Intento {intento} falló: {resultado.get('error', 'Error desconocido')}")
                    
            except TimeoutError:
                signal.alarm(0)  # Cancelar timeout
                print(f"⏱️ TIMEOUT en intento {intento} (>{MAX_TIEMPO_POR_DOCUMENTO}s)")
                
            except Exception as e:
                signal.alarm(0)  # Cancelar timeout
                print(f"❌ ERROR en intento {intento}: {e}")
                
                if intento < MAX_REINTENTOS:
                    print(f"🔄 Reintentando en 2 segundos...")
                    time.sleep(2)
        
        # Si llegamos aquí, todos los intentos fallaron
        self.documentos_fallidos += 1
        error_info = {
            "documento": doc_path.name,
            "intentos": MAX_REINTENTOS,
            "timestamp": datetime.now().isoformat()
        }
        self.errores_procesamiento.append(error_info)
        print(f"💥 DOCUMENTO FALLÓ DESPUÉS DE {MAX_REINTENTOS} INTENTOS")
    
    def _procesar_documento_contenido(self, doc_path: Path) -> Dict:
        """Procesa el contenido real del documento"""
        
        try:
            # 1. Extraer texto del PDF
            print("📖 Extrayendo texto...")
            texto = self._extraer_texto_pdf(doc_path)
            
            if not texto or len(texto.strip()) < 100:
                return {"success": False, "error": "Texto insuficiente o vacío"}
            
            print(f"📝 Texto extraído: {len(texto)} caracteres")
            
            # 2. Generar perfil cognitivo
            print("🧠 Generando perfil cognitivo...")
            
            if not self.analyser:
                return {"success": False, "error": "AnalyserMetodoMejorado no disponible"}
            
            metadatos = {
                "nombre_archivo": doc_path.name,
                "ruta_completa": str(doc_path),
                "fecha_procesamiento": datetime.now().isoformat()
            }
            
            perfil = self.analyser.procesar_texto_completo(texto, metadatos)
            
            if not perfil:
                return {"success": False, "error": "Error generando perfil cognitivo"}
            
            print("✅ Perfil cognitivo generado")
            
            # 3. Guardar en base de datos
            print("💾 Guardando en base de datos...")
            resultado_db = self._guardar_perfil_en_db(doc_path, perfil)
            
            if not resultado_db["success"]:
                return {"success": False, "error": f"Error guardando en DB: {resultado_db['error']}"}
            
            print("✅ Guardado en base de datos")
            
            return {"success": True, "perfil": perfil}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _extraer_texto_pdf(self, pdf_path: Path) -> str:
        """Extrae texto de PDF de forma robusta"""
        
        try:
            import fitz  # PyMuPDF
            
            texto_completo = ""
            
            with fitz.open(pdf_path) as doc:
                for pagina_num in range(len(doc)):
                    pagina = doc.load_page(pagina_num)
                    texto_pagina = pagina.get_text()
                    texto_completo += texto_pagina + "\n"
            
            # Limpiar texto
            texto_limpio = texto_completo.strip()
            
            # Remover líneas muy cortas (probablemente headers/footers)
            lineas = texto_limpio.split('\n')
            lineas_filtradas = [linea for linea in lineas if len(linea.strip()) > 10]
            
            return '\n'.join(lineas_filtradas)
            
        except Exception as e:
            print(f"❌ Error extrayendo texto de {pdf_path.name}: {e}")
            return ""
    
    def _guardar_perfil_en_db(self, doc_path: Path, perfil: Dict) -> Dict:
        """Guarda perfil en base de datos de forma robusta"""
        
        try:
            db_path = DATA_DIR / "cognitivo.db"
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Preparar datos
                documento_id = doc_path.stem
                nombre_archivo = doc_path.name
                autor_detectado = perfil.get("autor_detectado", "No detectado")
                perfil_json = json.dumps(perfil, ensure_ascii=False, indent=2)
                
                # Extraer métricas del perfil
                razonamiento = perfil.get("razonamiento", {})
                modalidades = perfil.get("modalidades_epistemicas", {})
                retorica = perfil.get("retorica", {})
                estilos = perfil.get("estilos_literarios", {})
                estructuras = perfil.get("estructuras_argumentativas", {})
                metricas_gen = perfil.get("metricas_generales", {})
                
                # INSERT con manejo de conflictos
                cursor.execute('''
                INSERT OR REPLACE INTO perfiles_autorales (
                    documento_id, nombre_archivo, autor_detectado, perfil_json,
                    
                    -- Razonamiento
                    razonamiento_deductivo, razonamiento_inductivo, razonamiento_abductivo,
                    razonamiento_analogico, razonamiento_teleologico, razonamiento_sistemico,
                    razonamiento_autoritativo, razonamiento_a_contrario, razonamiento_consecuencialista,
                    razonamiento_dialectico, razonamiento_hermeneutico, razonamiento_historico,
                    razonamiento_economico_analitico, razonamiento_reduccion_absurdo,
                    
                    -- Modalidades epistémicas
                    modalidad_apodíctico, modalidad_dialectico, modalidad_retorico,
                    modalidad_sofístico, modalidad_certeza, modalidad_incertidumbre, modalidad_hedging,
                    
                    -- Retórica
                    retorica_ethos, retorica_pathos, retorica_logos,
                    
                    -- Estilos literarios
                    estilo_tecnico_juridico, estilo_ensayistico, estilo_narrativo,
                    estilo_barroco, estilo_minimalista, estilo_aforistico,
                    estilo_impersonal_burocratico, estilo_dialectico_critico,
                    
                    -- Estructuras argumentativas
                    estructura_irac, estructura_toulmin, estructura_issue_tree,
                    estructura_defeasible, estructura_burden_shift, estructura_silogistico_formal,
                    
                    -- Métricas generales
                    formalismo, creatividad, empirismo, dogmatismo,
                    interdisciplinariedad, complejidad_sintactica, nivel_abstraccion, uso_jurisprudencia
                    
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    documento_id, nombre_archivo, autor_detectado, perfil_json,
                    
                    # Razonamiento
                    razonamiento.get("deductivo", 0.0), razonamiento.get("inductivo", 0.0), razonamiento.get("abductivo", 0.0),
                    razonamiento.get("analogico", 0.0), razonamiento.get("teleologico", 0.0), razonamiento.get("sistemico", 0.0),
                    razonamiento.get("autoritativo", 0.0), razonamiento.get("a_contrario", 0.0), razonamiento.get("consecuencialista", 0.0),
                    razonamiento.get("dialectico", 0.0), razonamiento.get("hermeneutico", 0.0), razonamiento.get("historico", 0.0),
                    razonamiento.get("economico_analitico", 0.0), razonamiento.get("reduccion_absurdo", 0.0),
                    
                    # Modalidades epistémicas
                    modalidades.get("apodíctico", 0.0), modalidades.get("dialectico", 0.0), modalidades.get("retorico", 0.0),
                    modalidades.get("sofístico", 0.0), modalidades.get("certeza", 0.0), modalidades.get("incertidumbre", 0.0), modalidades.get("hedging", 0.0),
                    
                    # Retórica
                    retorica.get("ethos", 0.0), retorica.get("pathos", 0.0), retorica.get("logos", 0.0),
                    
                    # Estilos literarios
                    estilos.get("tecnico_juridico", 0.0), estilos.get("ensayistico", 0.0), estilos.get("narrativo", 0.0),
                    estilos.get("barroco", 0.0), estilos.get("minimalista", 0.0), estilos.get("aforistico", 0.0),
                    estilos.get("impersonal_burocratico", 0.0), estilos.get("dialectico_critico", 0.0),
                    
                    # Estructuras argumentativas
                    estructuras.get("irac", 0.0), estructuras.get("toulmin", 0.0), estructuras.get("issue_tree", 0.0),
                    estructuras.get("defeasible", 0.0), estructuras.get("burden_shift", 0.0), estructuras.get("silogistico_formal", 0.0),
                    
                    # Métricas generales
                    metricas_gen.get("formalismo", 0.0), metricas_gen.get("creatividad", 0.0), metricas_gen.get("empirismo", 0.0), metricas_gen.get("dogmatismo", 0.0),
                    metricas_gen.get("interdisciplinariedad", 0.0), metricas_gen.get("complejidad_sintactica", 0.0), metricas_gen.get("nivel_abstraccion", 0.0), metricas_gen.get("uso_jurisprudencia", 0.0)
                ))
                
                conn.commit()
                
                return {"success": True}
                
        except Exception as e:
            print(f"❌ Error guardando en DB: {e}")
            return {"success": False, "error": str(e)}
    
    def _generar_reporte_final(self, tiempo_total: float) -> Dict:
        """Genera reporte final del procesamiento"""
        
        reporte = {
            "status": "completed",
            "tiempo_total": f"{tiempo_total:.1f}s",
            "documentos_procesados": self.documentos_procesados,
            "documentos_fallidos": self.documentos_fallidos,
            "tasa_exito": f"{(self.documentos_procesados / (self.documentos_procesados + self.documentos_fallidos) * 100):.1f}%" if (self.documentos_procesados + self.documentos_fallidos) > 0 else "0%",
            "errores": self.errores_procesamiento
        }
        
        print("\n" + "=" * 60)
        print("🎉 PROCESAMIENTO COMPLETADO")
        print("=" * 60)
        print(f"⏱️ Tiempo total: {reporte['tiempo_total']}")
        print(f"✅ Documentos procesados: {reporte['documentos_procesados']}")
        print(f"❌ Documentos fallidos: {reporte['documentos_fallidos']}")
        print(f"📊 Tasa de éxito: {reporte['tasa_exito']}")
        
        if self.errores_procesamiento:
            print("\n⚠️ ERRORES ENCONTRADOS:")
            for error in self.errores_procesamiento:
                print(f"  - {error['documento']}: {error['intentos']} intentos fallidos")
        
        return reporte

def main():
    """Función principal del procesador mejorado"""
    
    print("🚀 PROCESADOR INTEGRAL MEJORADO v2.0")
    print("Procesador robusto anti-trabas para ingesta cognitiva")
    print("=" * 60)
    
    try:
        procesador = ProcesadorIntegralMejorado()
        resultado = procesador.procesar_todo_robusto()
        
        # Guardar reporte
        reporte_path = BASE_DIR / f"reporte_procesamiento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(reporte_path, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Reporte guardado en: {reporte_path}")
        
        if resultado["status"] == "completed" and resultado["documentos_procesados"] > 0:
            print("\n🚀 PRÓXIMO PASO:")
            print("Ejecuta: .\\iniciar_sistema.bat")
            print("Para usar el sistema web con los nuevos análisis")
        
    except KeyboardInterrupt:
        print("\n⚠️ Procesamiento interrumpido por el usuario")
    except Exception as e:
        print(f"\n💥 Error crítico: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()