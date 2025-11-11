#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 ORCHESTRADOR MAESTRO DE ANÁLISIS DE PENSAMIENTO
==================================================

INTEGRA TODOS LOS MOTORES PARA ANÁLISIS COMPLETO DEL PENSAMIENTO:

1. 🎯 Motor Principal ANALYSER MÉTODO
2. 🏛️ Motor Aristotélico Avanzado  
3. 🔬 Motor Cognitivo Multi-Dimensional
4. 🧬 Motor Multi-Capa (5 capas)
5. 🚀 Motor de Ingesta Orientado al Pensamiento

OBJETIVO: ORQUESTAR todos los análisis para crear un PERFIL MENTAL COMPLETO

AUTOR: Sistema Cognitivo v5.0 - Orchestrador Maestro
FECHA: 9 NOV 2025
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
import numpy as np

# Importar todos los motores de análisis
sys.path.append(os.path.dirname(__file__))

try:
    from detector_autor_y_metodo import AnalyserMetodo
    print("✅ Motor ANALYSER MÉTODO cargado")
except ImportError as e:
    print(f"⚠️ Motor ANALYSER MÉTODO no disponible: {e}")

try:
    from detector_razonamiento_aristotelico import DetectorAristotelico
    print("✅ Motor ARISTOTÉLICO cargado")
except ImportError as e:
    print(f"⚠️ Motor ARISTOTÉLICO no disponible: {e}")

try:
    from vectorizador_cognitivo import VectorizadorCognitivo
    print("✅ Motor COGNITIVO MULTI-DIMENSIONAL cargado")
except ImportError as e:
    print(f"⚠️ Motor COGNITIVO no disponible: {e}")

try:
    from analizador_multicapa_pensamiento import AnalizadorMultiCapa
    print("✅ Motor MULTI-CAPA cargado")
except ImportError as e:
    print(f"⚠️ Motor MULTI-CAPA no disponible: {e}")

try:
    from motor_ingesta_pensamiento import MotorIngestaPensamiento
    print("✅ Motor INGESTA PENSAMIENTO cargado")
except ImportError as e:
    print(f"⚠️ Motor INGESTA PENSAMIENTO no disponible: {e}")

class OrchestadorMaestro:
    """Orchestrador que combina todos los motores de análisis del pensamiento"""
    
    def __init__(self):
        print("🧠 Inicializando Orchestrador Maestro de Análisis de Pensamiento")
        
        # Inicializar motores disponibles
        self.motores = {}
        
        # Motor 1: ANALYSER MÉTODO
        try:
            self.motores['analyser'] = AnalyserMetodo()
        except:
            print("⚠️ ANALYSER MÉTODO no inicializado")
        
        # Motor 2: ARISTOTÉLICO
        try:
            self.motores['aristotelico'] = DetectorAristotelico()
        except:
            print("⚠️ ARISTOTÉLICO no inicializado")
        
        # Motor 3: COGNITIVO MULTI-DIMENSIONAL
        try:
            self.motores['cognitivo'] = VectorizadorCognitivo()
        except:
            print("⚠️ COGNITIVO no inicializado")
        
        # Motor 4: MULTI-CAPA
        try:
            self.motores['multicapa'] = AnalizadorMultiCapa()
        except:
            print("⚠️ MULTI-CAPA no inicializado")
        
        # Motor 5: INGESTA PENSAMIENTO
        try:
            self.motores['ingesta_pensamiento'] = MotorIngestaPensamiento()
        except:
            print("⚠️ INGESTA PENSAMIENTO no inicializado")
        
        print(f"✅ Orchestrador inicializado con {len(self.motores)} motores")
        
        # Base de datos integrada
        self.db_path = "colaborative/bases_rag/cognitiva/pensamiento_integrado.db"
        self._inicializar_db_integrada()
    
    def _inicializar_db_integrada(self):
        """Inicializa base de datos para análisis integrado"""
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla principal de análisis integrado
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analisis_pensamiento_integrado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT NOT NULL,
                documento TEXT,
                
                -- ANÁLISIS ANALYSER MÉTODO
                metodologia_juridica TEXT,
                razonamiento_dominante TEXT,
                confianza_autor REAL,
                
                -- ANÁLISIS ARISTOTÉLICO
                modalidad_epistemica TEXT,
                estructura_silogistica TEXT,
                ethos REAL,
                pathos REAL, 
                logos REAL,
                
                -- ANÁLISIS COGNITIVO 8D
                formalismo REAL,
                creatividad REAL,
                dogmatismo REAL,
                empirismo REAL,
                interdisciplinariedad REAL,
                nivel_abstraccion REAL,
                complejidad_sintactica REAL,
                uso_jurisprudencia REAL,
                
                -- ANÁLISIS MULTI-CAPA
                patron_razonamiento_profundo TEXT,
                estructura_argumentativa_profunda TEXT,
                evolucion_temporal TEXT,
                conexiones_intelectuales TEXT,
                marcadores_cognitivos TEXT,
                
                -- ANÁLISIS INGESTA PENSAMIENTO
                arquitectura_mental TEXT,
                velocidad_cognitiva TEXT,
                estilo_inferencial TEXT,
                tolerancia_ambiguedad TEXT,
                patrones_asociativos TEXT,
                
                -- META-ANÁLISIS INTEGRADO
                tipo_mente_integrado TEXT,
                complejidad_cognitiva_total REAL,
                creatividad_cognitiva_total REAL,
                eficiencia_cognitiva_total REAL,
                
                -- METADATOS
                fecha_analisis DATETIME DEFAULT CURRENT_TIMESTAMP,
                version_orchestrador TEXT DEFAULT 'v5.0',
                motores_utilizados TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"✅ Base de datos integrada inicializada: {self.db_path}")
    
    def analizar_documento_completo(self, ruta_documento: str, autor: str = None) -> Dict[str, Any]:
        """Ejecuta análisis completo con todos los motores disponibles"""
        
        print(f"\n🎭 INICIANDO ANÁLISIS INTEGRADO COMPLETO")
        print(f"📄 Documento: {ruta_documento}")
        print(f"👤 Autor: {autor}")
        print("=" * 60)
        
        # Leer texto del documento
        texto = self._leer_documento(ruta_documento)
        
        # Contenedor para todos los análisis
        analisis_integrado = {
            "documento": ruta_documento,
            "autor": autor or "Desconocido",
            "timestamp": datetime.now().isoformat(),
            "texto_longitud": len(texto),
            "analisis": {},
            "meta_analisis": {}
        }
        
        # EJECUTAR TODOS LOS MOTORES
        print("🔄 Ejecutando motores de análisis...")
        
        # Motor 1: ANALYSER MÉTODO
        if 'analyser' in self.motores:
            try:
                print("  🎯 Ejecutando ANALYSER MÉTODO...")
                analisis_integrado["analisis"]["analyser"] = self.motores['analyser'].analizar_completo(texto)
                print("  ✅ ANALYSER MÉTODO completado")
            except Exception as e:
                print(f"  ❌ Error en ANALYSER MÉTODO: {e}")
                analisis_integrado["analisis"]["analyser"] = {"error": str(e)}
        
        # Motor 2: ARISTOTÉLICO
        if 'aristotelico' in self.motores:
            try:
                print("  🏛️ Ejecutando ARISTOTÉLICO...")
                analisis_integrado["analisis"]["aristotelico"] = self.motores['aristotelico'].analizar_completo(texto)
                print("  ✅ ARISTOTÉLICO completado")
            except Exception as e:
                print(f"  ❌ Error en ARISTOTÉLICO: {e}")
                analisis_integrado["analisis"]["aristotelico"] = {"error": str(e)}
        
        # Motor 3: COGNITIVO 8D
        if 'cognitivo' in self.motores:
            try:
                print("  🔬 Ejecutando COGNITIVO 8D...")
                analisis_integrado["analisis"]["cognitivo"] = self.motores['cognitivo'].extraer_perfil_completo(texto)
                print("  ✅ COGNITIVO 8D completado")
            except Exception as e:
                print(f"  ❌ Error en COGNITIVO 8D: {e}")
                analisis_integrado["analisis"]["cognitivo"] = {"error": str(e)}
        
        # Motor 4: MULTI-CAPA
        if 'multicapa' in self.motores:
            try:
                print("  🧬 Ejecutando MULTI-CAPA...")
                analisis_integrado["analisis"]["multicapa"] = self.motores['multicapa'].analizar_autor_completo(autor, [texto])
                print("  ✅ MULTI-CAPA completado")
            except Exception as e:
                print(f"  ❌ Error en MULTI-CAPA: {e}")
                analisis_integrado["analisis"]["multicapa"] = {"error": str(e)}
        
        # Motor 5: INGESTA PENSAMIENTO
        if 'ingesta_pensamiento' in self.motores:
            try:
                print("  🚀 Ejecutando INGESTA PENSAMIENTO...")
                analisis_integrado["analisis"]["ingesta_pensamiento"] = self.motores['ingesta_pensamiento'].extraer_pensamiento_puro(texto, autor)
                print("  ✅ INGESTA PENSAMIENTO completado")
            except Exception as e:
                print(f"  ❌ Error en INGESTA PENSAMIENTO: {e}")
                analisis_integrado["analisis"]["ingesta_pensamiento"] = {"error": str(e)}
        
        # GENERAR META-ANÁLISIS INTEGRADO
        print("🧠 Generando meta-análisis integrado...")
        analisis_integrado["meta_analisis"] = self._generar_meta_analisis_integrado(analisis_integrado["analisis"])
        
        # GUARDAR EN BASE DE DATOS
        self._guardar_analisis_integrado(analisis_integrado)
        
        print("✅ ANÁLISIS INTEGRADO COMPLETADO")
        return analisis_integrado
    
    def _generar_meta_analisis_integrado(self, analisis: Dict[str, Any]) -> Dict[str, Any]:
        """Genera meta-análisis integrando todos los motores"""
        
        meta_analisis = {
            "tipo_mente_integrado": self._determinar_tipo_mente_integrado(analisis),
            "perfil_cognitivo_consolidado": self._consolidar_perfil_cognitivo(analisis),
            "fortalezas_cognitivas": self._identificar_fortalezas_cognitivas(analisis),
            "estilo_pensamiento_dominante": self._determinar_estilo_dominante(analisis),
            "complejidad_intelectual": self._calcular_complejidad_intelectual(analisis),
            "recomendaciones_uso": self._generar_recomendaciones_uso(analisis)
        }
        
        return meta_analisis
    
    def _determinar_tipo_mente_integrado(self, analisis: Dict[str, Any]) -> str:
        """Determina el tipo de mente basado en todos los análisis"""
        
        tipos_detectados = []
        
        # Desde ANALYSER
        if 'analyser' in analisis and 'metodologia_juridica' in analisis['analyser']:
            metodologia = analisis['analyser']['metodologia_juridica']
            if 'formal' in metodologia.lower():
                tipos_detectados.append("Formal-Sistemática")
            elif 'empírico' in metodologia.lower():
                tipos_detectados.append("Empírico-Práctica")
        
        # Desde ARISTOTÉLICO
        if 'aristotelico' in analisis and 'modalidad_epistemica' in analisis['aristotelico']:
            modalidad = analisis['aristotelico']['modalidad_epistemica']
            if modalidad == 'apodíctico':
                tipos_detectados.append("Demostrativa-Rigurosa")
            elif modalidad == 'dialéctico':
                tipos_detectados.append("Dialógica-Reflexiva")
        
        # Desde COGNITIVO
        if 'cognitivo' in analisis:
            cog = analisis['cognitivo']
            if cog.get('creatividad', 0) > 0.7:
                tipos_detectados.append("Creativo-Innovadora")
            if cog.get('formalismo', 0) > 0.7:
                tipos_detectados.append("Estructurada-Ordenada")
        
        # Desde INGESTA PENSAMIENTO
        if 'ingesta_pensamiento' in analisis and 'meta_analisis' in analisis['ingesta_pensamiento']:
            meta = analisis['ingesta_pensamiento']['meta_analisis']
            tipos_detectados.append(meta.get('tipo_mente', 'Adaptativa'))
        
        # Consolidar tipo dominante
        if not tipos_detectados:
            return "Híbrida-Adaptativa"
        
        # Encontrar el tipo más común
        contador_tipos = {}
        for tipo in tipos_detectados:
            contador_tipos[tipo] = contador_tipos.get(tipo, 0) + 1
        
        tipo_dominante = max(contador_tipos.items(), key=lambda x: x[1])[0]
        return tipo_dominante
    
    def _consolidar_perfil_cognitivo(self, analisis: Dict[str, Any]) -> Dict[str, float]:
        """Consolida el perfil cognitivo desde todos los motores"""
        
        perfil_consolidado = {}
        dimensiones = ['formalismo', 'creatividad', 'empirismo', 'dogmatismo', 
                      'interdisciplinariedad', 'nivel_abstraccion', 'complejidad_sintactica']
        
        for dimension in dimensiones:
            valores = []
            
            # Desde COGNITIVO
            if 'cognitivo' in analisis and dimension in analisis['cognitivo']:
                valores.append(analisis['cognitivo'][dimension])
            
            # Desde otros motores (mapear cuando corresponda)
            # ... lógica de mapeo entre motores
            
            if valores:
                perfil_consolidado[dimension] = np.mean(valores)
            else:
                perfil_consolidado[dimension] = 0.5  # neutral
        
        return perfil_consolidado
    
    def _identificar_fortalezas_cognitivas(self, analisis: Dict[str, Any]) -> List[str]:
        """Identifica las fortalezas cognitivas principales"""
        
        fortalezas = []
        
        # Analizar cada motor
        for motor, resultados in analisis.items():
            if isinstance(resultados, dict) and 'error' not in resultados:
                # Lógica específica por motor
                if motor == 'cognitivo':
                    for dim, valor in resultados.items():
                        if isinstance(valor, (int, float)) and valor > 0.7:
                            fortalezas.append(f"Alto {dim}")
                
                elif motor == 'aristotelico':
                    if resultados.get('logos', 0) > 0.7:
                        fortalezas.append("Razonamiento lógico sólido")
                    if resultados.get('ethos', 0) > 0.7:
                        fortalezas.append("Alta credibilidad argumentativa")
        
        return fortalezas[:5]  # Top 5 fortalezas
    
    def _determinar_estilo_dominante(self, analisis: Dict[str, Any]) -> str:
        """Determina el estilo de pensamiento dominante"""
        
        estilos = []
        
        # Recopilar indicadores de estilo desde todos los motores
        if 'ingesta_pensamiento' in analisis:
            patrones = analisis['ingesta_pensamiento'].get('patrones_cognitivos', {})
            for patron, resultado in patrones.items():
                if isinstance(resultado, dict):
                    max_valor = max(resultado.values())
                    max_key = max(resultado.items(), key=lambda x: x[1])[0]
                    if max_valor > 0.6:
                        estilos.append(max_key)
        
        return estilos[0] if estilos else "Equilibrado"
    
    def _calcular_complejidad_intelectual(self, analisis: Dict[str, Any]) -> float:
        """Calcula la complejidad intelectual integrada"""
        
        complejidades = []
        
        # Desde diferentes motores
        if 'cognitivo' in analisis:
            comp_sint = analisis['cognitivo'].get('complejidad_sintactica', 0)
            nivel_abs = analisis['cognitivo'].get('nivel_abstraccion', 0)
            interdis = analisis['cognitivo'].get('interdisciplinariedad', 0)
            complejidades.append(np.mean([comp_sint, nivel_abs, interdis]))
        
        if 'ingesta_pensamiento' in analisis and 'meta_analisis' in analisis['ingesta_pensamiento']:
            meta = analisis['ingesta_pensamiento']['meta_analisis']
            complejidades.append(meta.get('complejidad_cognitiva', 0))
        
        return np.mean(complejidades) if complejidades else 0.5
    
    def _generar_recomendaciones_uso(self, analisis: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones de uso basadas en el perfil integrado"""
        
        recomendaciones = []
        
        # Basado en fortalezas identificadas
        fortalezas = self._identificar_fortalezas_cognitivas(analisis)
        
        for fortaleza in fortalezas:
            if 'formal' in fortaleza.lower():
                recomendaciones.append("💼 Ideal para trabajos que requieren estructura y precisión")
            elif 'creativ' in fortaleza.lower():
                recomendaciones.append("🎨 Excelente para innovación y enfoques originales")
            elif 'empiric' in fortaleza.lower():
                recomendaciones.append("📊 Valioso para investigación basada en evidencia")
            elif 'lógic' in fortaleza.lower():
                recomendaciones.append("🧠 Apropiado para razonamiento complejo y análisis riguroso")
        
        return recomendaciones[:3]  # Top 3 recomendaciones
    
    def _guardar_analisis_integrado(self, analisis: Dict[str, Any]):
        """Guarda el análisis integrado en la base de datos"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extraer valores para inserción
        autor = analisis.get('autor', 'Desconocido')
        documento = analisis.get('documento', '')
        
        # Preparar datos para inserción (simplificado)
        cursor.execute('''
            INSERT INTO analisis_pensamiento_integrado 
            (autor, documento, tipo_mente_integrado, motores_utilizados)
            VALUES (?, ?, ?, ?)
        ''', (
            autor,
            documento,
            analisis.get('meta_analisis', {}).get('tipo_mente_integrado', 'Desconocido'),
            json.dumps(list(analisis.get('analisis', {}).keys()))
        ))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Análisis integrado guardado para: {autor}")
    
    def _leer_documento(self, ruta: str) -> str:
        """Lee documento según su formato"""
        # Implementación simplificada
        try:
            if ruta.endswith('.txt'):
                with open(ruta, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return "Documento de ejemplo para pruebas del orchestrador."
        except Exception as e:
            print(f"⚠️ Error leyendo documento: {e}")
            return "Texto de prueba para análisis."
    
    def generar_reporte_integrado(self, autor: str) -> str:
        """Genera un reporte integrado para un autor"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM analisis_pensamiento_integrado 
            WHERE autor = ? 
            ORDER BY fecha_analisis DESC 
            LIMIT 1
        ''', (autor,))
        
        resultado = cursor.fetchone()
        conn.close()
        
        if not resultado:
            return f"❌ No se encontró análisis integrado para: {autor}"
        
        # Generar reporte HTML/texto
        reporte = f"""
        🧠 REPORTE INTEGRADO DE ANÁLISIS DE PENSAMIENTO
        ==============================================
        
        👤 AUTOR: {autor}
        📅 FECHA: {resultado[30]}  # fecha_analisis
        🎭 TIPO DE MENTE: {resultado[29]}  # tipo_mente_integrado
        
        🔧 MOTORES UTILIZADOS: {resultado[31]}  # motores_utilizados
        
        📊 PERFIL COGNITIVO INTEGRADO:
        [Detalles del perfil consolidado]
        
        💡 RECOMENDACIONES:
        [Recomendaciones específicas]
        
        ═══════════════════════════════════════════════
        Generado por Orchestrador Maestro v5.0
        """
        
        return reporte

def main():
    """Función principal para probar el orchestrador"""
    
    print("🚀 INICIANDO ORCHESTRADOR MAESTRO")
    
    orchestrador = OrchestadorMaestro()
    
    # Ejemplo de uso
    if len(orchestrador.motores) > 0:
        print("\n🧪 EJECUTANDO ANÁLISIS DE PRUEBA...")
        
        # Crear documento de prueba
        doc_prueba = "documento_prueba.txt"
        with open(doc_prueba, 'w', encoding='utf-8') as f:
            f.write("""
            En primer lugar, debemos analizar sistemáticamente los elementos que configuran 
            esta figura jurídica. La doctrina establece claramente que no puede haber 
            ambigüedad en la interpretación. Por tanto, se sigue necesariamente que 
            la única opción viable es aplicar el criterio restrictivo.
            """)
        
        # Ejecutar análisis completo
        resultado = orchestrador.analizar_documento_completo(doc_prueba, "Autor de Prueba")
        
        print("\n📋 RESULTADO DEL ANÁLISIS:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
        # Generar reporte
        reporte = orchestrador.generar_reporte_integrado("Autor de Prueba")
        print("\n📄 REPORTE INTEGRADO:")
        print(reporte)
        
        # Limpiar
        os.remove(doc_prueba)
    else:
        print("⚠️ No hay motores disponibles para análisis")

if __name__ == "__main__":
    main()