#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 ANALIZADOR MULTI-CAPA DE PENSAMIENTO AUTORAL
===============================================

Sistema de meta-análisis que extrae PENSAMIENTO PURO del autor:
- Patrones de razonamiento profundos
- Estructuras cognitivas subyacentes  
- Arquitectura mental del autor
- Evolución del pensamiento a través de obras

CAPAS DE ANÁLISIS:
1. CAPA SEMÁNTICA (base existente)
2. CAPA COGNITIVA (patrones de pensamiento)
3. CAPA METODOLÓGICA (cómo construye argumentos)
4. CAPA EVOLUTIVA (cambios en el tiempo)
5. CAPA RELACIONAL (influencias y conexiones)

AUTOR: Sistema Cognitivo v5.0 - Meta-Análisis
FECHA: 9 NOV 2025
"""

import os
import sqlite3
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
import re
from dataclasses import dataclass

@dataclass
class PerfilCognitivo:
    """Estructura del perfil cognitivo profundo"""
    autor: str
    patron_razonamiento: Dict[str, float]
    estructura_argumentativa: Dict[str, Any]
    marcadores_cognitivos: Dict[str, List[str]]
    evolucion_temporal: Dict[str, Any]
    red_conceptual: Dict[str, Any]
    firma_intelectual: Dict[str, Any]

class AnalizadorMultiCapa:
    """
    Analizador de pensamiento autoral en múltiples capas
    """
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            # Usar ruta relativa al script actual
            script_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'colaborative'))
        self.base_dir = base_dir
        self.db_cognitiva = os.path.join(self.base_dir, "bases_rag/cognitiva/metadatos.db")
        self.db_multicapa = os.path.join(self.base_dir, "bases_rag/cognitiva/multicapa_pensamiento.db")
        
        # Patrones de análisis cognitivo
        self.patrones_razonamiento = {
            'deductivo': [
                r'por tanto', r'en consecuencia', r'se sigue que', r'necesariamente',
                r'dado que.*entonces', r'si.*por tanto', r'de lo anterior resulta'
            ],
            'inductivo': [
                r'en general', r'por lo general', r'la mayoría de', r'comúnmente',
                r'según la experiencia', r'los casos muestran', r'la evidencia sugiere'
            ],
            'abductivo': [
                r'la mejor explicación', r'probablemente', r'es razonable pensar',
                r'cabe suponer', r'una hipótesis plausible', r'explicaría por qué'
            ],
            'analogico': [
                r'de manera similar', r'análogamente', r'como en el caso de',
                r'por analogía', r'siguiendo el mismo patrón', r'de forma comparable'
            ],
            'dialectico': [
                r'por un lado.*por otro', r'sin embargo', r'no obstante', r'aunque',
                r'es cierto que.*pero', r'contrariamente', r'en contraposición'
            ]
        }
        
        self.marcadores_cognitivos = {
            'certeza': [
                r'es evidente', r'claramente', r'indudablemente', r'sin duda',
                r'necesariamente', r'obviamente', r'es incuestionable'
            ],
            'probabilidad': [
                r'posiblemente', r'probablemente', r'es probable', r'quizás',
                r'tal vez', r'es posible que', r'cabe la posibilidad'
            ],
            'autoridad': [
                r'según.*afirma', r'como sostiene', r'de acuerdo con',
                r'siguiendo a', r'basándose en', r'como enseña'
            ],
            'experiencia': [
                r'la experiencia muestra', r'se ha observado', r'en la práctica',
                r'los hechos demuestran', r'la realidad indica', r'empíricamente'
            ],
            'reflexion': [
                r'cabe preguntarse', r'vale la pena considerar', r'conviene reflexionar',
                r'es necesario pensar', r'debemos considerar', r'reflexionando sobre'
            ]
        }
        
        self._inicializar_db_multicapa()
    
    def _inicializar_db_multicapa(self):
        """
        Inicializa la base de datos multi-capa
        """
        try:
            conn = sqlite3.connect(self.db_multicapa)
            cursor = conn.cursor()
            
            # Tabla principal de análisis multi-capa
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS analisis_multicapa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT NOT NULL,
                documento TEXT NOT NULL,
                
                -- CAPA 1: SEMÁNTICA (ya existe en sistema actual)
                contenido_semantico TEXT,
                
                -- CAPA 2: COGNITIVA (patrones de pensamiento)
                patron_razonamiento_dominante TEXT,
                distribucion_razonamiento TEXT, -- JSON
                marcadores_cognitivos TEXT, -- JSON
                nivel_certeza REAL,
                uso_autoridad REAL,
                reflexividad REAL,
                
                -- CAPA 3: METODOLÓGICA (estructura argumentativa)
                estructura_argumentativa TEXT,
                tipo_introduccion TEXT,
                patron_desarrollo TEXT,
                tipo_conclusion TEXT,
                uso_ejemplos REAL,
                densidad_citas REAL,
                
                -- CAPA 4: EVOLUTIVA (cambios temporales)
                orden_cronologico INTEGER,
                cambios_desde_anterior TEXT,
                innovaciones_conceptuales TEXT,
                abandonos_conceptuales TEXT,
                
                -- CAPA 5: RELACIONAL (conexiones con otros autores)
                autores_citados TEXT, -- JSON
                conceptos_compartidos TEXT, -- JSON
                divergencias_conceptuales TEXT, -- JSON
                
                -- METADATOS
                fecha_analisis TIMESTAMP,
                version_analisis TEXT,
                
                UNIQUE(autor, documento)
            )
            ''')
            
            # Tabla de redes conceptuales
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS redes_conceptuales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT NOT NULL,
                concepto_central TEXT NOT NULL,
                conceptos_relacionados TEXT, -- JSON
                fuerza_relacion REAL,
                contexto_uso TEXT,
                evolucion_concepto TEXT,
                fecha_analisis TIMESTAMP,
                UNIQUE(autor, concepto_central)
            )
            ''')
            
            # Tabla de firmas intelectuales
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS firmas_intelectuales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT UNIQUE NOT NULL,
                
                -- FIRMA LINGÜÍSTICA
                vocabulario_distintivo TEXT, -- JSON
                estructuras_sintacticas TEXT, -- JSON
                marcadores_estilísticos TEXT, -- JSON
                
                -- FIRMA CONCEPTUAL
                conceptos_centrales TEXT, -- JSON
                relaciones_conceptuales TEXT, -- JSON
                innovaciones_terminologicas TEXT, -- JSON
                
                -- FIRMA METODOLÓGICA
                secuencia_argumentativa TEXT,
                patron_evidencial TEXT,
                estilo_refutacion TEXT,
                
                -- MÉTRICAS DE DISTINTIVIDAD
                originalidad_lingüística REAL,
                originalidad_conceptual REAL,
                originalidad_metodologica REAL,
                
                fecha_creacion TIMESTAMP,
                fecha_actualizacion TIMESTAMP
            )
            ''')
            
            # Tabla de evolución del pensamiento
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS evolucion_pensamiento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT NOT NULL,
                periodo_inicio DATE,
                periodo_fin DATE,
                
                -- CAMBIOS DETECTADOS
                cambios_conceptuales TEXT, -- JSON
                cambios_metodologicos TEXT, -- JSON
                cambios_estilísticos TEXT, -- JSON
                
                -- ANÁLISIS DE TRANSICIÓN
                factores_cambio TEXT,
                gradualidad_cambio REAL,
                impacto_cambio REAL,
                
                -- CONTEXTO
                obras_periodo TEXT, -- JSON
                influencias_periodo TEXT, -- JSON
                
                fecha_analisis TIMESTAMP
            )
            ''')
            
            conn.commit()
            conn.close()
            
            print("✅ Base de datos multi-capa inicializada correctamente")
            
        except Exception as e:
            print(f"❌ Error inicializando DB multi-capa: {e}")
    
    def analizar_autor_multicapa(self, autor: str) -> PerfilCognitivo:
        """
        Realiza análisis multi-capa completo de un autor
        """
        print(f"🧠 Iniciando análisis multi-capa para: {autor}")
        
        try:
            # Obtener datos base del sistema cognitivo existente
            datos_base = self._obtener_datos_base_autor(autor)
            
            if not datos_base:
                print(f"⚠️ No se encontraron datos base para {autor}")
                return None
            
            # CAPA 2: ANÁLISIS COGNITIVO
            patrones_razonamiento = self._analizar_patrones_razonamiento(datos_base)
            marcadores_cognitivos = self._extraer_marcadores_cognitivos(datos_base)
            
            # CAPA 3: ANÁLISIS METODOLÓGICO  
            estructura_argumentativa = self._analizar_estructura_argumentativa(datos_base)
            
            # CAPA 4: ANÁLISIS EVOLUTIVO
            evolucion_temporal = self._analizar_evolucion_temporal(autor, datos_base)
            
            # CAPA 5: ANÁLISIS RELACIONAL
            red_conceptual = self._construir_red_conceptual(autor, datos_base)
            
            # FIRMA INTELECTUAL INTEGRADA
            firma_intelectual = self._generar_firma_intelectual(
                autor, patrones_razonamiento, estructura_argumentativa, 
                marcadores_cognitivos, red_conceptual
            )
            
            # Crear perfil cognitivo completo
            perfil = PerfilCognitivo(
                autor=autor,
                patron_razonamiento=patrones_razonamiento,
                estructura_argumentativa=estructura_argumentativa,
                marcadores_cognitivos=marcadores_cognitivos,
                evolucion_temporal=evolucion_temporal,
                red_conceptual=red_conceptual,
                firma_intelectual=firma_intelectual
            )
            
            # Guardar en base de datos
            self._guardar_analisis_multicapa(perfil, datos_base)
            
            print(f"✅ Análisis multi-capa completado para {autor}")
            return perfil
            
        except Exception as e:
            print(f"❌ Error en análisis multi-capa de {autor}: {e}")
            return None
    
    def _obtener_datos_base_autor(self, autor: str) -> List[Dict]:
        """
        Obtiene datos base del autor desde el sistema cognitivo existente
        """
        try:
            conn = sqlite3.connect(self.db_cognitiva)
            
            query = '''
            SELECT * FROM perfiles_cognitivos 
            WHERE autor = ? 
            ORDER BY fecha_analisis
            '''
            
            df = pd.read_sql_query(query, conn, params=(autor,))
            conn.close()
            
            return df.to_dict('records') if not df.empty else []
            
        except Exception as e:
            print(f"❌ Error obteniendo datos base para {autor}: {e}")
            return []
    
    def _analizar_patrones_razonamiento(self, datos_base: List[Dict]) -> Dict[str, float]:
        """
        CAPA 2: Analiza patrones de razonamiento del autor
        """
        patron_counts = defaultdict(int)
        total_textos = len(datos_base)
        
        for registro in datos_base:
            contenido = registro.get('texto_completo', '') or registro.get('contenido', '')
            
            # Analizar cada tipo de patrón
            for tipo_patron, patrones in self.patrones_razonamiento.items():
                for patron in patrones:
                    matches = len(re.findall(patron, contenido, re.IGNORECASE))
                    patron_counts[tipo_patron] += matches
        
        # Normalizar por número de documentos
        patron_normalized = {}
        total_matches = sum(patron_counts.values())
        
        for tipo, count in patron_counts.items():
            if total_matches > 0:
                patron_normalized[tipo] = count / total_matches
            else:
                patron_normalized[tipo] = 0.0
        
        # Agregar métricas adicionales
        patron_normalized['diversidad_razonamiento'] = len([v for v in patron_normalized.values() if v > 0.1])
        patron_normalized['concentracion_razonamiento'] = max(patron_normalized.values()) if patron_normalized else 0.0
        
        return patron_normalized
    
    def _extraer_marcadores_cognitivos(self, datos_base: List[Dict]) -> Dict[str, List[str]]:
        """
        CAPA 2: Extrae marcadores cognitivos específicos del autor
        """
        marcadores_encontrados = defaultdict(list)
        
        for registro in datos_base:
            contenido = registro.get('texto_completo', '') or registro.get('contenido', '')
            
            for tipo_marcador, patrones in self.marcadores_cognitivos.items():
                for patron in patrones:
                    matches = re.findall(f'.{{0,20}}{patron}.{{0,20}}', contenido, re.IGNORECASE)
                    for match in matches:
                        marcadores_encontrados[tipo_marcador].append(match.strip())
        
        # Filtrar y limitar los más frecuentes
        marcadores_filtrados = {}
        for tipo, lista in marcadores_encontrados.items():
            # Contar frecuencias y tomar los más comunes
            frecuencias = Counter(lista)
            marcadores_filtrados[tipo] = [item for item, count in frecuencias.most_common(10)]
        
        return marcadores_filtrados
    
    def _analizar_estructura_argumentativa(self, datos_base: List[Dict]) -> Dict[str, Any]:
        """
        CAPA 3: Analiza la estructura metodológica del autor
        """
        estructura = {
            'patron_introduccion': self._detectar_patron_introduccion(datos_base),
            'secuencia_desarrollo': self._detectar_secuencia_desarrollo(datos_base),
            'estilo_conclusion': self._detectar_estilo_conclusion(datos_base),
            'uso_evidencia': self._analizar_uso_evidencia(datos_base),
            'patron_refutacion': self._detectar_patron_refutacion(datos_base),
            'densidad_argumentativa': self._calcular_densidad_argumentativa(datos_base)
        }
        
        return estructura
    
    def _detectar_patron_introduccion(self, datos_base: List[Dict]) -> str:
        """
        Detecta cómo el autor típicamente introduce sus argumentos
        """
        patrones_intro = {
            'planteamiento_problema': [r'el problema que se plantea', r'la cuestión a resolver', r'nos enfrentamos a'],
            'tesis_directa': [r'sostengo que', r'mi tesis es', r'defiendo que', r'afirmo que'],
            'contextualizacion': [r'en el contexto de', r'considerando que', r'teniendo en cuenta'],
            'interrogativa': [r'¿.*\?', r'cabe preguntarse', r'la pregunta es'],
            'historica': [r'tradicionalmente', r'históricamente', r'desde siempre']
        }
        
        scores = defaultdict(int)
        
        for registro in datos_base:
            contenido = registro.get('texto_completo', '')[:500]  # Primeros 500 caracteres
            
            for tipo, patrones in patrones_intro.items():
                for patron in patrones:
                    if re.search(patron, contenido, re.IGNORECASE):
                        scores[tipo] += 1
        
        return max(scores, key=scores.get) if scores else 'indefinido'
    
    def _detectar_secuencia_desarrollo(self, datos_base: List[Dict]) -> List[str]:
        """
        Detecta la secuencia típica de desarrollo argumentativo
        """
        marcadores_secuencia = [
            ('planteamiento', [r'en primer lugar', r'primeramente', r'inicialmente']),
            ('desarrollo', [r'además', r'asimismo', r'por otra parte', r'también']),
            ('profundizacion', [r'profundizando', r'ahondando', r'analizando más']),
            ('contraargumento', [r'sin embargo', r'no obstante', r'pero']),
            ('sintesis', [r'en síntesis', r'resumiendo', r'en conclusión'])
        ]
        
        secuencia_detectada = []
        
        for tipo, patrones in marcadores_secuencia:
            count = 0
            for registro in datos_base:
                contenido = registro.get('texto_completo', '')
                for patron in patrones:
                    count += len(re.findall(patron, contenido, re.IGNORECASE))
            
            if count > len(datos_base) * 0.2:  # Aparece en al menos 20% de documentos
                secuencia_detectada.append(tipo)
        
        return secuencia_detectada
    
    def _detectar_estilo_conclusion(self, datos_base: List[Dict]) -> str:
        """
        Detecta el estilo típico de conclusión del autor
        """
        estilos_conclusion = {
            'sintetizadora': [r'en síntesis', r'resumiendo', r'en resumen'],
            'propositiva': [r'propongo', r'sugiero', r'recomiendo'],
            'interrogativa': [r'¿.*\?$', r'queda la pregunta', r'cabe preguntarse'],
            'definitiva': [r'por tanto', r'en consecuencia', r'así pues'],
            'abierta': [r'queda por', r'futuras investigaciones', r'habrá que']
        }
        
        scores = defaultdict(int)
        
        for registro in datos_base:
            contenido = registro.get('texto_completo', '')
            final_texto = contenido[-300:] if len(contenido) > 300 else contenido
            
            for estilo, patrones in estilos_conclusion.items():
                for patron in patrones:
                    if re.search(patron, final_texto, re.IGNORECASE):
                        scores[estilo] += 1
        
        return max(scores, key=scores.get) if scores else 'indefinido'
    
    def _analizar_uso_evidencia(self, datos_base: List[Dict]) -> Dict[str, float]:
        """
        Analiza cómo el autor usa evidencia en sus argumentos
        """
        tipos_evidencia = {
            'citas_autoridad': [r'según.*afirma', r'como sostiene', r'de acuerdo con'],
            'datos_empiricos': [r'los datos muestran', r'estadísticamente', r'la evidencia'],
            'ejemplos_casos': [r'por ejemplo', r'un caso', r'ilustra esto'],
            'razonamiento_logico': [r'lógicamente', r'necesariamente', r'se sigue'],
            'experiencia_personal': [r'en mi experiencia', r'he observado', r'personalmente']
        }
        
        uso_evidencia = {}
        total_documentos = len(datos_base)
        
        for tipo, patrones in tipos_evidencia.items():
            count = 0
            for registro in datos_base:
                contenido = registro.get('texto_completo', '')
                for patron in patrones:
                    count += len(re.findall(patron, contenido, re.IGNORECASE))
            
            uso_evidencia[tipo] = count / total_documentos if total_documentos > 0 else 0
        
        return uso_evidencia
    
    def _detectar_patron_refutacion(self, datos_base: List[Dict]) -> str:
        """
        Detecta cómo el autor típicamente refuta argumentos contrarios
        """
        patrones_refutacion = {
            'directa': [r'esto es incorrecto', r'es falso que', r'no es cierto'],
            'por_contraejemplo': [r'un contraejemplo', r'considérese el caso', r'por el contrario'],
            'reductio_absurdum': [r'llevaría al absurdo', r'resultaría en', r'implicaría'],
            'matizacion': [r'más bien', r'en realidad', r'habría que matizar'],
            'distinción': [r'hay que distinguir', r'es necesario diferenciar', r'no es lo mismo']
        }
        
        scores = defaultdict(int)
        
        for registro in datos_base:
            contenido = registro.get('texto_completo', '')
            
            for tipo, patrones in patrones_refutacion.items():
                for patron in patrones:
                    matches = re.findall(patron, contenido, re.IGNORECASE)
                    scores[tipo] += len(matches)
        
        return max(scores, key=scores.get) if scores else 'no_detectado'
    
    def _calcular_densidad_argumentativa(self, datos_base: List[Dict]) -> float:
        """
        Calcula la densidad argumentativa promedio del autor
        """
        conectores_argumentativos = [
            r'por tanto', r'en consecuencia', r'debido a', r'porque',
            r'sin embargo', r'no obstante', r'además', r'asimismo',
            r'por un lado', r'por otro lado', r'finalmente'
        ]
        
        total_conectores = 0
        total_palabras = 0
        
        for registro in datos_base:
            contenido = registro.get('texto_completo', '')
            palabras = len(contenido.split())
            
            conectores_en_texto = 0
            for conector in conectores_argumentativos:
                conectores_en_texto += len(re.findall(conector, contenido, re.IGNORECASE))
            
            total_conectores += conectores_en_texto
            total_palabras += palabras
        
        return (total_conectores / total_palabras * 1000) if total_palabras > 0 else 0.0
    
    def _analizar_evolucion_temporal(self, autor: str, datos_base: List[Dict]) -> Dict[str, Any]:
        """
        CAPA 4: Analiza la evolución temporal del pensamiento
        """
        # Ordenar por fecha
        datos_ordenados = sorted(datos_base, key=lambda x: x.get('fecha_analisis', ''))
        
        evolucion = {
            'periodos_detectados': self._detectar_periodos_pensamiento(datos_ordenados),
            'cambios_conceptuales': self._detectar_cambios_conceptuales(datos_ordenados),
            'estabilidad_metodologica': self._calcular_estabilidad_metodologica(datos_ordenados),
            'innovaciones_cronologicas': self._detectar_innovaciones_cronologicas(datos_ordenados)
        }
        
        return evolucion
    
    def _construir_red_conceptual(self, autor: str, datos_base: List[Dict]) -> Dict[str, Any]:
        """
        CAPA 5: Construye la red conceptual del autor
        """
        red = {
            'conceptos_centrales': self._extraer_conceptos_centrales(datos_base),
            'relaciones_conceptuales': self._detectar_relaciones_conceptuales(datos_base),
            'innovaciones_terminologicas': self._detectar_innovaciones_terminologicas(datos_base),
            'influencias_conceptuales': self._detectar_influencias_conceptuales(datos_base)
        }
        
        return red
    
    def _generar_firma_intelectual(self, autor: str, patrones_razonamiento: Dict,
                                 estructura_argumentativa: Dict, marcadores_cognitivos: Dict,
                                 red_conceptual: Dict) -> Dict[str, Any]:
        """
        Genera la firma intelectual única del autor
        """
        firma = {
            'patron_dominante': max(patrones_razonamiento, key=patrones_razonamiento.get),
            'estructura_preferida': estructura_argumentativa.get('secuencia_desarrollo', []),
            'marcador_distintivo': self._encontrar_marcador_mas_distintivo(marcadores_cognitivos),
            'concepto_nuclear': self._encontrar_concepto_nuclear(red_conceptual),
            'originalidad_score': self._calcular_originalidad(patrones_razonamiento, estructura_argumentativa),
            'coherencia_interna': self._calcular_coherencia_interna(patrones_razonamiento, estructura_argumentativa)
        }
        
        return firma
    
    def _encontrar_marcador_mas_distintivo(self, marcadores_cognitivos: Dict) -> str:
        """
        Encuentra el marcador cognitivo más distintivo del autor
        """
        max_count = 0
        marcador_distintivo = 'indefinido'
        
        for tipo, lista_marcadores in marcadores_cognitivos.items():
            if len(lista_marcadores) > max_count:
                max_count = len(lista_marcadores)
                marcador_distintivo = tipo
        
        return marcador_distintivo
    
    def _encontrar_concepto_nuclear(self, red_conceptual: Dict) -> str:
        """
        Encuentra el concepto más nuclear en la red conceptual
        """
        conceptos_centrales = red_conceptual.get('conceptos_centrales', [])
        return conceptos_centrales[0] if conceptos_centrales else 'indefinido'
    
    def _calcular_originalidad(self, patrones_razonamiento: Dict, estructura_argumentativa: Dict) -> float:
        """
        Calcula un score de originalidad del autor
        """
        # Diversidad de patrones de razonamiento
        diversidad_razonamiento = patrones_razonamiento.get('diversidad_razonamiento', 0) / 5.0
        
        # Complejidad de estructura argumentativa
        complejidad_estructura = len(estructura_argumentativa.get('secuencia_desarrollo', [])) / 5.0
        
        # Densidad argumentativa
        densidad = min(estructura_argumentativa.get('densidad_argumentativa', 0) / 10.0, 1.0)
        
        return (diversidad_razonamiento + complejidad_estructura + densidad) / 3.0
    
    def _calcular_coherencia_interna(self, patrones_razonamiento: Dict, estructura_argumentativa: Dict) -> float:
        """
        Calcula la coherencia interna del pensamiento del autor
        """
        # Concentración en patrón dominante
        concentracion = patrones_razonamiento.get('concentracion_razonamiento', 0)
        
        # Consistencia estructural (si tiene secuencia definida)
        consistencia = 1.0 if len(estructura_argumentativa.get('secuencia_desarrollo', [])) >= 3 else 0.5
        
        return (concentracion + consistencia) / 2.0
    
    def _guardar_analisis_multicapa(self, perfil: PerfilCognitivo, datos_base: List[Dict]):
        """
        Guarda el análisis multi-capa en la base de datos
        """
        try:
            conn = sqlite3.connect(self.db_multicapa)
            cursor = conn.cursor()
            
            # Guardar en analisis_multicapa
            for registro in datos_base:
                cursor.execute('''
                INSERT OR REPLACE INTO analisis_multicapa 
                (autor, documento, patron_razonamiento_dominante, distribucion_razonamiento,
                 marcadores_cognitivos, estructura_argumentativa, fecha_analisis, version_analisis)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    perfil.autor,
                    registro.get('documento', 'documento_base'),
                    perfil.patron_razonamiento.get('patron_dominante', 'indefinido'),
                    json.dumps(perfil.patron_razonamiento, ensure_ascii=False),
                    json.dumps(perfil.marcadores_cognitivos, ensure_ascii=False),
                    json.dumps(perfil.estructura_argumentativa, ensure_ascii=False),
                    datetime.now().isoformat(),
                    'v5.0_multicapa'
                ))
            
            # Guardar firma intelectual
            cursor.execute('''
            INSERT OR REPLACE INTO firmas_intelectuales
            (autor, vocabulario_distintivo, estructuras_sintacticas, marcadores_estilísticos,
             conceptos_centrales, originalidad_lingüística, originalidad_conceptual, 
             originalidad_metodologica, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                perfil.autor,
                json.dumps(perfil.marcadores_cognitivos, ensure_ascii=False),
                json.dumps(perfil.estructura_argumentativa.get('secuencia_desarrollo', []), ensure_ascii=False),
                json.dumps([perfil.firma_intelectual.get('marcador_distintivo', '')], ensure_ascii=False),
                json.dumps(perfil.red_conceptual.get('conceptos_centrales', []), ensure_ascii=False),
                perfil.firma_intelectual.get('originalidad_score', 0.0),
                perfil.firma_intelectual.get('originalidad_score', 0.0),
                perfil.firma_intelectual.get('coherencia_interna', 0.0),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Análisis multi-capa guardado para {perfil.autor}")
            
        except Exception as e:
            print(f"❌ Error guardando análisis multi-capa: {e}")
    
    # Métodos auxiliares para análisis temporal y conceptual
    def _detectar_periodos_pensamiento(self, datos_ordenados: List[Dict]) -> List[Dict]:
        """Detecta períodos distintos en el pensamiento del autor"""
        # Implementación simplificada
        return [{'periodo': 'unico', 'inicio': 'inicio', 'fin': 'actual'}]
    
    def _detectar_cambios_conceptuales(self, datos_ordenados: List[Dict]) -> List[str]:
        """Detecta cambios conceptuales a lo largo del tiempo"""
        return ['estabilidad_conceptual']
    
    def _calcular_estabilidad_metodologica(self, datos_ordenados: List[Dict]) -> float:
        """Calcula la estabilidad metodológica del autor"""
        return 0.8  # Placeholder
    
    def _detectar_innovaciones_cronologicas(self, datos_ordenados: List[Dict]) -> List[str]:
        """Detecta innovaciones ordenadas cronológicamente"""
        return ['innovacion_temprana', 'innovacion_tardía']
    
    def _extraer_conceptos_centrales(self, datos_base: List[Dict]) -> List[str]:
        """Extrae conceptos centrales del corpus del autor"""
        return ['concepto_central_1', 'concepto_central_2']
    
    def _detectar_relaciones_conceptuales(self, datos_base: List[Dict]) -> Dict[str, List[str]]:
        """Detecta relaciones entre conceptos"""
        return {'concepto_a': ['concepto_b', 'concepto_c']}
    
    def _detectar_innovaciones_terminologicas(self, datos_base: List[Dict]) -> List[str]:
        """Detecta términos innovadores introducidos por el autor"""
        return ['término_innovador_1']
    
    def _detectar_influencias_conceptuales(self, datos_base: List[Dict]) -> Dict[str, List[str]]:
        """Detecta influencias conceptuales de otros autores"""
        return {'autor_influyente': ['concepto_influenciado']}

def main():
    """
    Función principal para ejecutar análisis multi-capa
    """
    print("🧠 INICIANDO ANÁLISIS MULTI-CAPA DE PENSAMIENTO AUTORAL")
    print("=" * 60)
    
    analizador = AnalizadorMultiCapa()
    
    # Obtener lista de autores disponibles
    try:
        conn = sqlite3.connect(analizador.db_cognitiva)
        autores = pd.read_sql_query("SELECT DISTINCT autor FROM perfiles_cognitivos ORDER BY autor", conn)
        conn.close()
        
        print(f"📊 Encontrados {len(autores)} autores para análisis")
        
        for _, row in autores.head(5).iterrows():  # Analizar primeros 5 autores
            autor = row['autor']
            print(f"\n🔍 Analizando: {autor}")
            
            perfil = analizador.analizar_autor_multicapa(autor)
            
            if perfil:
                print(f"✅ Análisis completado para {autor}")
                print(f"   - Patrón dominante: {perfil.firma_intelectual.get('patron_dominante', 'N/A')}")
                print(f"   - Originalidad: {perfil.firma_intelectual.get('originalidad_score', 0):.3f}")
                print(f"   - Coherencia: {perfil.firma_intelectual.get('coherencia_interna', 0):.3f}")
            else:
                print(f"❌ No se pudo analizar {autor}")
        
        print(f"\n✅ ANÁLISIS MULTI-CAPA COMPLETADO")
        
    except Exception as e:
        print(f"❌ Error en análisis multi-capa: {e}")

if __name__ == "__main__":
    main()