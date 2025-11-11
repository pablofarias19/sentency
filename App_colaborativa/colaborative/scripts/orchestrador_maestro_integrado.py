#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ ORCHESTRADOR MAESTRO INTEGRADO - Sistema de Pensamiento v6.0
==============================================================

IMPLEMENTA MEJORAS INTEGRALES:
- Integración del ANALYSER MÉTODO MEJORADO v2.0
- Comparador de Mentes para análisis de similaridad
- Esquema JSON unificado (perfil_autoral.json)
- Taxonomía expandida con 40+ dimensiones cognitivas
- Búsqueda por patrones de pensamiento específicos

NUEVA ARQUITECTURA:
1. Motor Principal: ANALYSER MÉTODO MEJORADO v2.0
2. Motor Cognitivo: Vectorizador con 20+ dimensiones
3. Motor Aristotélico: Modalidades y figuras silogísticas  
4. Motor Multi-Capa: 5 capas de análisis profundo
5. Motor Ingesta Pensamiento: Extracción pura de patrones cognitivos
6. NUEVO: Comparador de Mentes - Análisis de similaridad cognitiva

COMPATIBILIDAD: 100% con sistema existente + mejoras integrales
AUTOR: Sistema Cognitivo v6.0 - Mejoras Máximas
FECHA: 9 NOV 2025
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Tuple
import traceback

# Importar motores mejorados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analyser_metodo_mejorado import AnalyserMetodoMejorado
from comparador_mentes import ComparadorMentes, SimilitudMental

class OrchestadorMaestroIntegrado:
    """Orchestrador maestro con mejoras integrales v6.0"""
    
    def __init__(self):
        self.version = "v6.0_integrado_mejorado"
        self.db_integrada = "colaborative/bases_rag/cognitiva/pensamiento_integrado_v2.db"
        
        # Inicializar motores mejorados
        self.analyser_mejorado = AnalyserMetodoMejorado()
        self.comparador_mentes = ComparadorMentes()
        
        # Configurar base de datos integrada
        self._configurar_db_integrada()
        
        print(f"🚀 ORCHESTRADOR MAESTRO INTEGRADO {self.version} INICIADO")
        print("🔧 Motores disponibles:")
        print("   1. ANALYSER MÉTODO MEJORADO v2.0 (40+ dimensiones)")
        print("   2. COMPARADOR DE MENTES v1.0")
        print("   3. Sistema de Búsqueda por Patrones Cognitivos")
        print("   4. Análisis de Similaridad Mental")
    
    def _configurar_db_integrada(self):
        """Configura base de datos integrada con nuevas mejoras"""
        
        os.makedirs(os.path.dirname(self.db_integrada), exist_ok=True)
        
        conn = sqlite3.connect(self.db_integrada)
        cursor = conn.cursor()
        
        # Tabla principal de perfiles integrados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS perfiles_integrados_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT NOT NULL,
                fuente TEXT,
                perfil_completo TEXT,  -- JSON del esquema unificado
                vector_cognitivo TEXT,  -- Vector para comparaciones
                
                -- Índices de búsqueda rápida
                razonamiento_dominante TEXT,
                modalidad_dominante TEXT,
                estilo_dominante TEXT,
                
                -- Métricas clave para filtrado
                nivel_abstraccion REAL,
                creatividad REAL,
                empirismo REAL,
                sistematizacion REAL,
                
                -- Metadatos
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                version_orchestrador TEXT,
                
                UNIQUE(autor, fuente)
            )
        ''')
        
        # Tabla de comparaciones entre autores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comparaciones_mentales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor_a TEXT,
                autor_b TEXT,
                similaridad_coseno REAL,
                distancia_mental REAL,
                dimensiones_clave TEXT,  -- JSON
                diferencias_principales TEXT,  -- JSON
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                UNIQUE(autor_a, autor_b)
            )
        ''')
        
        # Tabla de patrones de búsqueda
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patrones_busqueda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_patron TEXT,
                patron_json TEXT,  -- Definición del patrón
                autores_coincidentes TEXT,  -- JSON con autores y scores
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabla para análisis lógico temático
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analisis_logico_tematico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT,
                expediente TEXT,
                temas TEXT,
                cuestiones_introductorias TEXT,
                formas_razonamiento TEXT,
                tautologias TEXT,
                falacias TEXT,
                fecha_sentencia TEXT
            )
        ''')

        # Tabla para metadatos judiciales enriquecidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadatos_judiciales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT,
                tribunal TEXT,
                jurisdiccion TEXT,
                caratula TEXT,
                numero_expediente TEXT,
                materia TEXT,
                fecha_sentencia TEXT,
                citaciones_doctrina TEXT,
                citaciones_jurisprudencia TEXT,
                calculos TEXT,
                ponderacion TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"💾 Base de datos integrada configurada: {self.db_integrada}")
    
    def analizar_documento_completo(self, texto: str, autor: str = None, fuente: str = None) -> Dict[str, Any]:
        """Análisis completo usando todos los motores mejorados"""
        
        print(f"\n🧠 INICIANDO ANÁLISIS COMPLETO INTEGRADO")
        print(f"📄 Fuente: {fuente or 'Texto directo'}")
        print(f"👤 Autor: {autor or 'Desconocido'}")
        print(f"📊 Longitud: {len(texto)} caracteres")
        
        try:
            # 1. Análisis principal con ANALYSER MEJORADO
            print("\n🎯 1. Ejecutando ANALYSER MÉTODO MEJORADO v2.0...")
            perfil_principal = self.analyser_mejorado.generar_perfil_autoral_completo(texto, autor, fuente)
            
            # 2. Vectorización para comparaciones
            print("🧮 2. Generando vector cognitivo...")
            vector_cognitivo = self.comparador_mentes.vectorizar_perfil(perfil_principal)
            
            # 3. Guardar en base de datos integrada
            print("💾 3. Guardando en base de datos integrada...")
            self._guardar_perfil_integrado(perfil_principal, vector_cognitivo)
            
            # 4. Buscar autores similares si ya existen perfiles
            print("🔍 4. Buscando autores con patrones similares...")
            autores_similares = self._buscar_autores_similares(perfil_principal)
            
            # 5. Compilar resultado integrado
            resultado_integrado = {
                "perfil_autoral": perfil_principal,
                "vector_cognitivo": vector_cognitivo,
                "autores_similares": autores_similares,
                "meta_analysis": {
                    "motor_principal": "ANALYSER_MEJORADO_v2.0",
                    "dimensiones_analizadas": len(self.comparador_mentes.FEATURE_KEYS),
                    "timestamp_analysis": datetime.now().isoformat(),
                    "version_orchestrador": self.version
                }
            }
            
            print("\n✅ ANÁLISIS COMPLETO FINALIZADO")
            return resultado_integrado
            
        except Exception as e:
            print(f"❌ Error en análisis integrado: {e}")
            traceback.print_exc()
            return {"error": str(e)}
    
    def _guardar_perfil_integrado(self, perfil: Dict[str, Any], vector: List[float]):
        """Guarda perfil en base de datos integrada"""
        
        conn = sqlite3.connect(self.db_integrada)
        cursor = conn.cursor()
        
        try:
            # Extraer métricas clave para indexación
            marcadores = perfil.get('marcadores_cognitivos', {})
            razonamiento_scores = perfil.get('cognicion', {}).get('razonamiento_formal', {})
            modalidad_scores = perfil.get('cognicion', {}).get('modalidad_epistemica', {})
            estilo_scores = perfil.get('cognicion', {}).get('estilo_literario', {})
            
            # Validar perfil antes de guardar
            perfil = self._validar_perfil(perfil)
            
            razonamiento_dominante = max(razonamiento_scores.items(), key=lambda x: x[1])[0] if razonamiento_scores else "desconocido"
            modalidad_dominante = max(modalidad_scores.items(), key=lambda x: x[1])[0] if modalidad_scores else "desconocido"
            estilo_dominante = max(estilo_scores.items(), key=lambda x: x[1])[0] if estilo_scores else "desconocido"
            
            # Insertar o actualizar
            cursor.execute('''
                INSERT OR REPLACE INTO perfiles_integrados_v2 
                (autor, fuente, perfil_completo, vector_cognitivo, 
                 razonamiento_dominante, modalidad_dominante, estilo_dominante,
                 nivel_abstraccion, creatividad, empirismo, sistematizacion, version_orchestrador)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                perfil['meta']['autor_probable'],
                perfil['meta']['fuente'],
                json.dumps(perfil, ensure_ascii=False),
                json.dumps(vector),
                razonamiento_dominante,
                modalidad_dominante,
                estilo_dominante,
                marcadores.get('nivel_abstraccion', 0.0),
                marcadores.get('creatividad', 0.0),
                marcadores.get('empirismo', 0.0),
                razonamiento_scores.get('sistemico', 0.0),
                self.version
            ))
            
            # Guardar metadatos judiciales si existen
            if "metadatos_judiciales" in perfil:
                md = perfil["metadatos_judiciales"]
                cursor.execute('''
                    INSERT INTO metadatos_judiciales (
                        autor, tribunal, jurisdiccion, caratula, numero_expediente,
                        materia, fecha_sentencia, citaciones_doctrina,
                        citaciones_jurisprudencia, calculos, ponderacion
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    md.get("autor"), md.get("tribunal"), md.get("jurisdiccion"),
                    md.get("caratula"), md.get("numero_expediente"), md.get("materia"),
                    md.get("fecha_sentencia"),
                    json.dumps(md.get("citaciones", {}).get("doctrina", [])),
                    json.dumps(md.get("citaciones", {}).get("jurisprudencia", [])),
                    json.dumps(md.get("calculos", {})),
                    json.dumps(md.get("ponderacion", {}))
                ))
            
            conn.commit()
            print(f"💾 Perfil integrado guardado: {perfil['meta']['autor_probable']}")
            
        except Exception as e:
            print(f"❌ Error guardando perfil integrado: {e}")
        finally:
            conn.close()
    
    def _buscar_autores_similares(self, perfil_nuevo: Dict[str, Any], limite: int = 5) -> List[Dict[str, Any]]:
        """Busca autores con patrones cognitivos similares"""
        
        conn = sqlite3.connect(self.db_integrada)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT autor, perfil_completo FROM perfiles_integrados_v2 WHERE autor != ?", 
                          (perfil_nuevo['meta']['autor_probable'],))
            rows = cursor.fetchall()
            
            similitudes = []
            
            for autor, perfil_json in rows:
                try:
                    perfil_existente = json.loads(perfil_json)
                    comparacion = self.comparador_mentes.comparar_mentes(perfil_nuevo, perfil_existente)
                    
                    similitudes.append({
                        "autor": autor,
                        "similaridad": comparacion.cosine_similarity,
                        "distancia": comparacion.distance,
                        "dimensiones_clave": comparacion.dimensiones_clave,
                        "diferencias_principales": comparacion.diferencias_principales[:3]
                    })
                    
                except json.JSONDecodeError:
                    continue
            
            # Ordenar por similaridad descendente
            similitudes.sort(key=lambda x: x['similaridad'], reverse=True)
            
            conn.close()
            return similitudes[:limite]
            
        except Exception as e:
            print(f"❌ Error buscando similitudes: {e}")
            conn.close()
            return []
    
    def buscar_por_patron_cognitivo(self, nombre_patron: str, patron: Dict[str, float], umbral: float = 0.7) -> List[Dict[str, Any]]:
        """Busca autores que coincidan con un patrón cognitivo específico"""
        
        print(f"\n🔍 BÚSQUEDA POR PATRÓN COGNITIVO: {nombre_patron}")
        print(f"📊 Patrón: {patron}")
        print(f"🎯 Umbral: {umbral}")
        
        coincidencias = self.comparador_mentes.buscar_por_patron_pensamiento(patron, umbral)
        
        # Guardar patrón de búsqueda
        self._guardar_patron_busqueda(nombre_patron, patron, coincidencias)
        
        resultado = []
        for autor, similaridad in coincidencias:
            resultado.append({
                "autor": autor,
                "coincidencia": similaridad,
                "patron_aplicado": patron
            })
        
        print(f"✅ Encontradas {len(resultado)} coincidencias")
        return resultado
    
    def _guardar_patron_busqueda(self, nombre: str, patron: Dict[str, float], coincidencias: List[Tuple[str, float]]):
        """Guarda patrón de búsqueda para auditoría"""
        
        conn = sqlite3.connect(self.db_integrada)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO patrones_busqueda 
                (nombre_patron, patron_json, autores_coincidentes)
                VALUES (?, ?, ?)
            ''', (
                nombre,
                json.dumps(patron, ensure_ascii=False),
                json.dumps(coincidencias, ensure_ascii=False)
            ))
            
            conn.commit()
            print(f"💾 Patrón guardado: {nombre}")
            
        except Exception as e:
            print(f"❌ Error guardando patrón: {e}")
        finally:
            conn.close()
    
    def generar_reporte_comparativo_completo(self, autor_a: str, autor_b: str) -> str:
        """Genera reporte comparativo detallado usando el comparador de mentes"""
        
        print(f"\n📊 GENERANDO REPORTE COMPARATIVO")
        print(f"👤 {autor_a} vs {autor_b}")
        
        reporte_basico = self.comparador_mentes.generar_reporte_comparativo(autor_a, autor_b)
        
        # Agregar información adicional del análisis integrado
        conn = sqlite3.connect(self.db_integrada)
        cursor = conn.cursor()
        
        try:
            # Obtener información adicional de ambos autores
            cursor.execute('''
                SELECT razonamiento_dominante, modalidad_dominante, estilo_dominante,
                       nivel_abstraccion, creatividad, empirismo
                FROM perfiles_integrados_v2 
                WHERE autor = ?
            ''', (autor_a,))
            info_a = cursor.fetchone()
            
            cursor.execute('''
                SELECT razonamiento_dominante, modalidad_dominante, estilo_dominante,
                       nivel_abstraccion, creatividad, empirismo
                FROM perfiles_integrados_v2 
                WHERE autor = ?
            ''', (autor_b,))
            info_b = cursor.fetchone()
            
            if info_a and info_b:
                reporte_extendido = reporte_basico + f"""

🎯 PERFILES COGNITIVOS DOMINANTES:

📈 {autor_a}:
  • Razonamiento: {info_a[0].title()}
  • Modalidad: {info_a[1].title()}  
  • Estilo: {info_a[2].title()}
  • Abstracción: {info_a[3]:.2f}
  • Creatividad: {info_a[4]:.2f}
  • Empirismo: {info_a[5]:.2f}

📉 {autor_b}:
  • Razonamiento: {info_b[0].title()}
  • Modalidad: {info_b[1].title()}
  • Estilo: {info_b[2].title()}
  • Abstracción: {info_b[3]:.2f}
  • Creatividad: {info_b[4]:.2f}
  • Empirismo: {info_b[5]:.2f}

🧠 ANÁLISIS INTEGRADO v{self.version}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                conn.close()
                return reporte_extendido
            
        except Exception as e:
            print(f"❌ Error generando reporte extendido: {e}")
        finally:
            conn.close()
        
        return reporte_basico
    
    def listar_autores_disponibles(self) -> List[Dict[str, Any]]:
        """Lista todos los autores disponibles con sus características principales"""
        
        conn = sqlite3.connect(self.db_integrada)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT autor, razonamiento_dominante, modalidad_dominante, estilo_dominante,
                       nivel_abstraccion, creatividad, empirismo, timestamp
                FROM perfiles_integrados_v2
                ORDER BY timestamp DESC
            ''')
            rows = cursor.fetchall()
            
            autores = []
            for row in rows:
                autores.append({
                    "autor": row[0],
                    "razonamiento_dominante": row[1],
                    "modalidad_dominante": row[2],
                    "estilo_dominante": row[3],
                    "nivel_abstraccion": row[4],
                    "creatividad": row[5],
                    "empirismo": row[6],
                    "timestamp": row[7]
                })
            
            conn.close()
            return autores
            
        except Exception as e:
            print(f"❌ Error listando autores: {e}")
            conn.close()
            return []
    
    def exportar_datos_completos(self, output_dir: str = "exports_orchestrador_integrado"):
        """Exporta todos los datos del análisis integrado"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Exportar perfiles completos
        autores = self.listar_autores_disponibles()
        with open(f"{output_dir}/autores_disponibles.json", 'w', encoding='utf-8') as f:
            json.dump(autores, f, indent=2, ensure_ascii=False)
        
        # Exportar matriz de similitudes
        matriz_path = f"{output_dir}/matriz_similitudes_completa.json"
        self.comparador_mentes.exportar_matriz_similitudes(matriz_path)
        
        print(f"📁 Datos exportados a: {output_dir}")
        return output_dir

    def _validar_perfil(self, perfil):
        """Valida y corrige rangos del perfil cognitivo"""
        for clave in ["empirismo", "dogmatismo", "razonamiento", "coherencia"]:
            if clave in perfil and not (0 <= perfil[clave] <= 1):
                perfil[clave] = max(0, min(perfil[clave], 1))
        
        # Validar marcadores cognitivos
        marcadores = perfil.get('marcadores_cognitivos', {})
        for clave in ["empirismo", "creatividad", "nivel_abstraccion"]:
            if clave in marcadores and not (0 <= marcadores[clave] <= 1):
                marcadores[clave] = max(0, min(marcadores[clave], 1))
        
        if "coherencia" in perfil and perfil["coherencia"] < 0.2:
            print(f"⚠️  Baja coherencia detectada en {perfil.get('meta', {}).get('autor_probable','(sin autor)')}")
        
        return perfil

def main():
    """Función principal para probar el orchestrador integrado"""
    
    print("🚀 INICIANDO ORCHESTRADOR MAESTRO INTEGRADO v6.0")
    
    orchestrador = OrchestadorMaestroIntegrado()
    
    # Texto de ejemplo expandido para prueba completa
    texto_ejemplo = """
    El presente análisis sistemático busca establecer una metodología integral 
    para la interpretación de las normas laborales en el contexto contemporáneo.
    
    En primer lugar, debemos considerar que la doctrina establece claramente 
    el principio protectorio como eje fundamental. Por tanto, se sigue necesariamente
    que cualquier interpretación debe privilegiar la posición del trabajador
    cuando existe ambigüedad normativa.
    
    Sin embargo, reconozco que los datos empíricos disponibles son limitados
    y que existe una zona gris en la aplicación práctica. La evidencia estadística
    sugiere que aproximadamente el 60% de los casos presentan esta problemática.
    
    Como sostiene la jurisprudencia de la Corte Suprema en Fallos 341:234,
    la finalidad social debe guiar la hermenéutica jurídica. No obstante,
    considero que debemos ser creativos en la búsqueda de soluciones,
    integrando perspectivas económicas y sociológicas.
    
    La estructura argumentativa IRAC nos permite abordar sistemáticamente:
    el issue (¿cómo interpretar?), la rule (principio protectorio), 
    la application (casos concretos) y la conclusion (criterio flexible).
    """
    
    # Realizar análisis completo
    resultado = orchestrador.analizar_documento_completo(
        texto_ejemplo, 
        "Autor de Prueba Integrado",
        "test_integrado.txt"
    )
    
    if "error" not in resultado:
        print("\n📊 RESULTADO DEL ANÁLISIS INTEGRADO:")
        print(f"✅ Perfil autoral generado con {len(resultado['vector_cognitivo'])} dimensiones")
        print(f"✅ Autores similares encontrados: {len(resultado['autores_similares'])}")
        
        # Probar búsqueda por patrón
        patron_ejemplo = {
            "sistémico": 0.7,
            "creatividad": 0.6,
            "empirismo": 0.5
        }
        
        coincidencias = orchestrador.buscar_por_patron_cognitivo(
            "Patrón Sistémico-Creativo", 
            patron_ejemplo
        )
        
        print(f"✅ Búsqueda por patrón: {len(coincidencias)} coincidencias")
        
        # Listar autores disponibles
        autores_disponibles = orchestrador.listar_autores_disponibles()
        print(f"✅ Autores en base de datos: {len(autores_disponibles)}")
        
        # Exportar datos
        output_dir = orchestrador.exportar_datos_completos()
        print(f"✅ Datos exportados a: {output_dir}")
    
    print("\n🎯 ORCHESTRADOR MAESTRO INTEGRADO v6.0 - PRUEBA COMPLETADA")

if __name__ == "__main__":
    main()