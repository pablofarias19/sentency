#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 MOTOR DE INGESTA ORIENTADO AL PENSAMIENTO PURO
================================================

ENFOQUE REVOLUCIONARIO:
- 🎯 CÓMO PIENSA el autor > QUÉ dice el autor
- 🧬 Patrones cognitivos > Contenido semántico  
- 🔍 Metodología mental > Información textual
- 🧩 Arquitectura del razonamiento > Datos normativos

OBJETIVO: Descubrir la MENTE detrás del contenido

AUTOR: Sistema Cognitivo v5.0 - Ingesta del Pensamiento
FECHA: 9 NOV 2025
"""

import os
import sys
import re
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
import numpy as np
from collections import Counter, defaultdict

# Importar motores de análisis existentes
sys.path.append(os.path.dirname(__file__))
from detector_autor_y_metodo import analizar_metodologia_completa
from detector_razonamiento_aristotelico import detectar_modalidad_epistemica, analizar_estructura_silogistica
from analizador_multicapa_pensamiento import AnalizadorMultiCapa

class MotorIngestaPensamiento:
    """Motor especializado en extraer PATRONES DE PENSAMIENTO de documentos"""
    
    def __init__(self):
        self.analizador_multicapa = AnalizadorMultiCapa()
        
        # PROMPTS ESPECIALIZADOS EN PENSAMIENTO
        self.prompts_pensamiento = {
            "arquitectura_mental": self._prompt_arquitectura_mental(),
            "velocidad_cognitiva": self._prompt_velocidad_cognitiva(),
            "estilo_inferencial": self._prompt_estilo_inferencial(),
            "tolerancia_ambiguedad": self._prompt_tolerancia_ambiguedad(),
            "patrón_asociativo": self._prompt_patron_asociativo()
        }
        
        # PATRONES COGNITIVOS A DETECTAR
        self.patrones_cognitivos = {
            "lineal_vs_holístico": self._detectar_procesamiento(),
            "convergente_vs_divergente": self._detectar_creatividad_cognitiva(),
            "analítico_vs_intuitivo": self._detectar_estilo_cognitivo(),
            "sistemático_vs_exploratorio": self._detectar_aproximación(),
            "certeza_vs_incertidumbre": self._detectar_tolerancia_epistemica()
        }
    
    def _prompt_arquitectura_mental(self) -> str:
        """Prompt para detectar cómo organiza mentalmente los conceptos"""
        return '''
        🧩 ANALIZA LA ARQUITECTURA MENTAL DEL AUTOR:
        
        1. ORGANIZACIÓN CONCEPTUAL:
           - ¿Construye desde lo particular a lo general? (inductivo mental)
           - ¿Deduce desde principios generales? (deductivo mental)  
           - ¿Usa redes de conceptos interconectados? (sistémico mental)
           - ¿Procede por analogías y similitudes? (analógico mental)
        
        2. ESTRUCTURA DEL RAZONAMIENTO:
           - ¿Lineal y secuencial? → paso a paso ordenado
           - ¿Holístico y circular? → ve el todo primero
           - ¿En capas? → construye niveles de abstracción
           - ¿En redes? → conecta múltiples elementos simultáneamente
        
        3. GESTIÓN DE LA COMPLEJIDAD:
           - ¿Reduce complejidad a elementos simples? (reducionista)
           - ¿Mantiene la complejidad integrada? (sistémico)
           - ¿Navega cómodamente la complejidad? (tolerancia alta)
           - ¿Prefiere simplificar antes de analizar? (tolerancia baja)
        
        RESPONDE SOLO SOBRE CÓMO PIENSA, NO SOBRE QUÉ DICE.
        '''
    
    def _prompt_velocidad_cognitiva(self) -> str:
        """Prompt para detectar velocidad de procesamiento mental"""
        return '''
        ⚡ ANALIZA LA VELOCIDAD COGNITIVA DEL AUTOR:
        
        1. VELOCIDAD DE INFERENCIA:
           - ¿Conecta ideas rápidamente? (inferencia rápida)
           - ¿Toma tiempo para elaborar conexiones? (inferencia deliberada)
           - ¿Salta directamente a conclusiones? (procesamiento ágil)
           - ¿Construye gradualmente el argumento? (procesamiento pausado)
        
        2. RITMO DE EXPLORACIÓN:
           - ¿Explora múltiples opciones simultáneamente? (paralelo)
           - ¿Examina una opción completamente antes de pasar a otra? (serial)
           - ¿Cambia frecuentemente de perspectiva? (cognitivamente ágil)
           - ¿Mantiene una perspectiva consistente? (cognitivamente estable)
        
        3. PATRÓN TEMPORAL:
           - ¿Su razonamiento acelera hacia la conclusión? (convergente)
           - ¿Mantiene ritmo constante de análisis? (lineal)
           - ¿Decelera para explorar matices? (profundizador)
           - ¿Oscila entre velocidades? (variable)
        
        DETECTA EL TEMPO MENTAL, NO EL CONTENIDO.
        '''
    
    def _prompt_estilo_inferencial(self) -> str:
        """Prompt para detectar cómo hace inferencias"""
        return '''
        🔍 ANALIZA EL ESTILO INFERENCIAL DEL AUTOR:
        
        1. TIPO DE SALTOS LÓGICOS:
           - ¿Hace inferencias conservadoras? (bajo riesgo cognitivo)
           - ¿Se aventura con inferencias audaces? (alto riesgo cognitivo)
           - ¿Prefiere inferencias evidentes? (obvias)
           - ¿Busca inferencias sofisticadas? (elaboradas)
        
        2. GESTIÓN DE PREMISES:
           - ¿Explicita todas las premisas? (exhaustivo)
           - ¿Asume premisas implícitas? (sintético)
           - ¿Cuestiona sus propias premisas? (auto-reflexivo)
           - ¿Toma premisas como dadas? (asumptivo)
        
        3. CONEXIÓN LÓGICA:
           - ¿Sus conexiones son evidentes para todos? (transparente)
           - ¿Requieren expertise para seguirlas? (especializado)
           - ¿Son intuitivamente obvias? (intuitivo)
           - ¿Son lógicamente rigurosas? (formal)
        
        ENFÓCATE EN EL PROCESO DE INFERENCIA, NO EN LAS CONCLUSIONES.
        '''
    
    def _prompt_tolerancia_ambiguedad(self) -> str:
        """Prompt para detectar cómo maneja la incertidumbre"""
        return '''
        🌫️ ANALIZA LA TOLERANCIA A LA AMBIGÜEDAD DEL AUTOR:
        
        1. GESTIÓN DE INCERTIDUMBRE:
           - ¿Se siente cómodo con respuestas parciales? (tolerante)
           - ¿Busca siempre respuestas definitivas? (intolerante)
           - ¿Explora territorios inciertos? (explorador)
           - ¿Prefiere terreno conocido? (conservador)
        
        2. REACCIÓN A CONTRADICCIONES:
           - ¿Mantiene tensiones sin resolver? (dialéctico)
           - ¿Resuelve rápidamente las tensiones? (sintético)
           - ¿Se energiza con las paradojas? (paradójico)
           - ¿Se incomoda con inconsistencias? (coherentista)
        
        3. APERTURA EPISTÉMICA:
           - ¿Admite límites de su conocimiento? (humilde)
           - ¿Proyecta certeza incluso con dudas? (seguro)
           - ¿Disfruta explorar lo desconocido? (aventurero)
           - ¿Prefiere consolidar lo conocido? (consolidador)
        
        MIDE SU COMODIDAD CON LA INCERTIDUMBRE INTELECTUAL.
        '''
    
    def _prompt_patron_asociativo(self) -> str:
        """Prompt para detectar cómo asocia ideas"""
        return '''
        🕸️ ANALIZA LOS PATRONES ASOCIATIVOS DEL AUTOR:
        
        1. TIPO DE ASOCIACIONES:
           - ¿Por similitud conceptual? (analógico)
           - ¿Por contigüidad lógica? (secuencial)
           - ¿Por contraste u oposición? (dialéctico)
           - ¿Por jerarquía o niveles? (sistemático)
        
        2. DENSIDAD ASOCIATIVA:
           - ¿Pocas asociaciones pero profundas? (concentrado)
           - ¿Muchas asociaciones diversas? (expansivo)
           - ¿Asociaciones predecibles? (estructurado)
           - ¿Asociaciones sorprendentes? (creativo)
        
        3. RADIO ASOCIATIVO:
           - ¿Se mantiene en su dominio? (especializado)
           - ¿Conecta con otros dominios? (interdisciplinario)
           - ¿Asociaciones locales y próximas? (conservador)
           - ¿Asociaciones remotas y distantes? (innovador)
        
        DETECTA CÓMO SU MENTE CONECTA IDEAS ENTRE SÍ.
        '''
    
    def _detectar_procesamiento(self, texto: str) -> Dict[str, float]:
        """Detecta si el procesamiento es lineal u holístico"""
        
        # INDICADORES DE PROCESAMIENTO LINEAL
        indicadores_lineal = [
            r"\b(primero|segundo|tercero|finalmente)\b",
            r"\b(paso a paso|gradualmente|secuencialmente)\b",
            r"\b(en primer lugar|en segundo lugar|por último)\b",
            r"\b(inicialmente|posteriormente|a continuación)\b"
        ]
        
        # INDICADORES DE PROCESAMIENTO HOLÍSTICO  
        indicadores_holistico = [
            r"\b(en conjunto|globalmente|integralmente)\b",
            r"\b(considerando el todo|en su totalidad|holísticamente)\b",
            r"\b(simultaneamente|al mismo tiempo|conjuntamente)\b",
            r"\b(interconectado|interdependiente|sistémico)\b"
        ]
        
        score_lineal = self._contar_patrones(texto, indicadores_lineal)
        score_holistico = self._contar_patrones(texto, indicadores_holistico)
        
        return {
            "lineal": min(score_lineal / 10.0, 1.0),
            "holístico": min(score_holistico / 10.0, 1.0),
            "híbrido": 1.0 - abs(score_lineal - score_holistico) / max(score_lineal + score_holistico, 1)
        }
    
    def _detectar_creatividad_cognitiva(self, texto: str) -> Dict[str, float]:
        """Detecta si el pensamiento es convergente o divergente"""
        
        # INDICADORES CONVERGENTES (hacia UNA solución)
        indicadores_convergente = [
            r"\b(la solución|la respuesta|la conclusión única)\b",
            r"\b(necesariamente|inevitablemente|forzosamente)\b",
            r"\b(se deduce que|se sigue que|por tanto)\b",
            r"\b(única opción|única alternativa|no hay otra)\b"
        ]
        
        # INDICADORES DIVERGENTES (múltiples posibilidades)
        indicadores_divergente = [
            r"\b(múltiples opciones|diversas alternativas|varios enfoques)\b",
            r"\b(por otro lado|también podría|otra perspectiva)\b",
            r"\b(exploremos|consideremos|qué pasaría si)\b",
            r"\b(perspectivas diversas|enfoques variados|múltiples caminos)\b"
        ]
        
        score_convergente = self._contar_patrones(texto, indicadores_convergente)
        score_divergente = self._contar_patrones(texto, indicadores_divergente)
        
        return {
            "convergente": min(score_convergente / 8.0, 1.0),
            "divergente": min(score_divergente / 8.0, 1.0),
            "equilibrado": 1.0 - abs(score_convergente - score_divergente) / max(score_convergente + score_divergente, 1)
        }
    
    def _detectar_estilo_cognitivo(self, texto: str) -> Dict[str, float]:
        """Detecta si es analítico o intuitivo"""
        
        # INDICADORES ANALÍTICOS
        indicadores_analitico = [
            r"\b(analicemos|examinemos|descomponiendo|disectando)\b",
            r"\b(elemento por elemento|parte por parte|sistemáticamente)\b",
            r"\b(datos|evidencia|pruebas|métricas)\b",
            r"\b(lógicamente|racionalmente|metódicamente)\b"
        ]
        
        # INDICADORES INTUITIVOS
        indicadores_intuitivo = [
            r"\b(intuitivamente|se siente que|parece que)\b",
            r"\b(globalmente|en general|a primera vista)\b", 
            r"\b(experiencia sugiere|sentido común|sabiduría)\b",
            r"\b(percepción|impresión|sensación)\b"
        ]
        
        score_analitico = self._contar_patrones(texto, indicadores_analitico)
        score_intuitivo = self._contar_patrones(texto, indicadores_intuitivo)
        
        return {
            "analítico": min(score_analitico / 8.0, 1.0),
            "intuitivo": min(score_intuitivo / 8.0, 1.0),
            "integrado": 1.0 - abs(score_analitico - score_intuitivo) / max(score_analitico + score_intuitivo, 1)
        }
    
    def _detectar_aproximación(self, texto: str) -> Dict[str, float]:
        """Detecta si la aproximación es sistemática o exploratoria"""
        
        # INDICADORES SISTEMÁTICOS
        indicadores_sistematico = [
            r"\b(método|metodología|sistema|protocolo)\b",
            r"\b(ordenadamente|estructuradamente|organizadamente)\b",
            r"\b(según el marco|conforme al modelo|bajo el esquema)\b",
            r"\b(planificado|estructurado|organizado)\b"
        ]
        
        # INDICADORES EXPLORATORIOS
        indicadores_exploratorio = [
            r"\b(exploremos|investiguemos|descubramos|experimentemos)\b",
            r"\b(qué tal si|que pasaría|podríamos intentar)\b",
            r"\b(aventurándonos|arriesgando|probando)\b",
            r"\b(nueva perspectiva|enfoque fresco|ángulo diferente)\b"
        ]
        
        score_sistematico = self._contar_patrones(texto, indicadores_sistematico)
        score_exploratorio = self._contar_patrones(texto, indicadores_exploratorio)
        
        return {
            "sistemático": min(score_sistematico / 8.0, 1.0),
            "exploratorio": min(score_exploratorio / 8.0, 1.0),
            "adaptativo": 1.0 - abs(score_sistematico - score_exploratorio) / max(score_sistematico + score_exploratorio, 1)
        }
    
    def _detectar_tolerancia_epistemica(self, texto: str) -> Dict[str, float]:
        """Detecta tolerancia a la certeza vs incertidumbre"""
        
        # INDICADORES DE BÚSQUEDA DE CERTEZA
        indicadores_certeza = [
            r"\b(ciertamente|definitivamente|indudablemente|claramente)\b",
            r"\b(es evidente|es obvio|es claro|sin duda)\b",
            r"\b(categóricamente|taxativamente|rotundamente)\b",
            r"\b(no cabe duda|está claro|es incuestionable)\b"
        ]
        
        # INDICADORES DE TOLERANCIA A INCERTIDUMBRE
        indicadores_incertidumbre = [
            r"\b(quizás|tal vez|posiblemente|probablemente)\b",
            r"\b(parece que|podría ser|es posible que)\b",
            r"\b(en cierta medida|hasta cierto punto|relativamente)\b",
            r"\b(complejidad|ambigüedad|incertidumbre|matices)\b"
        ]
        
        score_certeza = self._contar_patrones(texto, indicadores_certeza)
        score_incertidumbre = self._contar_patrones(texto, indicadores_incertidumbre)
        
        return {
            "busca_certeza": min(score_certeza / 8.0, 1.0),
            "tolera_incertidumbre": min(score_incertidumbre / 8.0, 1.0),
            "equilibrio_epistémico": 1.0 - abs(score_certeza - score_incertidumbre) / max(score_certeza + score_incertidumbre, 1)
        }
    
    def _contar_patrones(self, texto: str, patrones: List[str]) -> int:
        """Cuenta ocurrencias de patrones en el texto"""
        contador = 0
        texto_lower = texto.lower()
        
        for patron in patrones:
            matches = re.findall(patron, texto_lower, re.IGNORECASE)
            contador += len(matches)
        
        return contador
    
    def extraer_pensamiento_puro(self, texto: str, autor: str = None) -> Dict[str, Any]:
        """Extrae patrones de pensamiento puro del texto"""
        
        print(f"🧠 Extrayendo patrones de pensamiento para: {autor}")
        
        # 1. ANÁLISIS COGNITIVO MULTIDIMENSIONAL
        patrones_cognitivos = {}
        for nombre, detector in self.patrones_cognitivos.items():
            patrones_cognitivos[nombre] = detector(texto)
        
        # 2. ANÁLISIS DE ARQUITECTURA MENTAL
        arquitectura_mental = self._analizar_arquitectura_mental(texto)
        
        # 3. ANÁLISIS DE VELOCIDAD COGNITIVA
        velocidad_cognitiva = self._analizar_velocidad_cognitiva(texto)
        
        # 4. ANÁLISIS DE ESTILO INFERENCIAL
        estilo_inferencial = self._analizar_estilo_inferencial(texto)
        
        # 5. PERFIL COGNITIVO INTEGRADO
        perfil_pensamiento = {
            "autor": autor,
            "timestamp": datetime.now().isoformat(),
            "patrones_cognitivos": patrones_cognitivos,
            "arquitectura_mental": arquitectura_mental,
            "velocidad_cognitiva": velocidad_cognitiva,
            "estilo_inferencial": estilo_inferencial,
            "meta_analisis": self._generar_meta_analisis(patrones_cognitivos, arquitectura_mental, velocidad_cognitiva)
        }
        
        return perfil_pensamiento
    
    def _analizar_arquitectura_mental(self, texto: str) -> Dict[str, Any]:
        """Analiza cómo está organizada mentalmente la información"""
        
        # DETECTAR ESTRUCTURA ORGANIZACIONAL
        estructura_secuencial = len(re.findall(r'\b(primero|segundo|tercero|luego|finalmente)\b', texto, re.IGNORECASE))
        estructura_jerarquica = len(re.findall(r'\b(principalmente|secundariamente|subordinado|superior|inferior)\b', texto, re.IGNORECASE))
        estructura_reticular = len(re.findall(r'\b(conecta|relaciona|vincula|interconecta|articula)\b', texto, re.IGNORECASE))
        
        total_indicadores = estructura_secuencial + estructura_jerarquica + estructura_reticular + 1
        
        return {
            "secuencial": estructura_secuencial / total_indicadores,
            "jerárquico": estructura_jerarquica / total_indicadores,
            "reticular": estructura_reticular / total_indicadores,
            "organización_dominante": max([
                ("secuencial", estructura_secuencial),
                ("jerárquico", estructura_jerarquica), 
                ("reticular", estructura_reticular)
            ], key=lambda x: x[1])[0]
        }
    
    def _analizar_velocidad_cognitiva(self, texto: str) -> Dict[str, Any]:
        """Analiza la velocidad del procesamiento mental"""
        
        # INDICADORES DE VELOCIDAD
        indicadores_rapida = len(re.findall(r'\b(inmediatamente|rápidamente|de inmediato|sin demora)\b', texto, re.IGNORECASE))
        indicadores_pausada = len(re.findall(r'\b(reflexionemos|consideremos|examinemos|analicemos)\b', texto, re.IGNORECASE))
        indicadores_variable = len(re.findall(r'\b(a veces|en ocasiones|dependiendo|según el caso)\b', texto, re.IGNORECASE))
        
        total = indicadores_rapida + indicadores_pausada + indicadores_variable + 1
        
        return {
            "velocidad_rápida": indicadores_rapida / total,
            "velocidad_pausada": indicadores_pausada / total,
            "velocidad_variable": indicadores_variable / total,
            "tempo_dominante": max([
                ("rápida", indicadores_rapida),
                ("pausada", indicadores_pausada),
                ("variable", indicadores_variable)
            ], key=lambda x: x[1])[0]
        }
    
    def _analizar_estilo_inferencial(self, texto: str) -> Dict[str, Any]:
        """Analiza cómo hace las inferencias"""
        
        # TIPOS DE INFERENCIA
        inferencia_deductiva = len(re.findall(r'\b(por tanto|en consecuencia|se sigue|se deduce)\b', texto, re.IGNORECASE))
        inferencia_inductiva = len(re.findall(r'\b(en general|habitualmente|frecuentemente|por lo común)\b', texto, re.IGNORECASE))
        inferencia_abductiva = len(re.findall(r'\b(probablemente|posiblemente|la mejor explicación|lo más probable)\b', texto, re.IGNORECASE))
        
        total = inferencia_deductiva + inferencia_inductiva + inferencia_abductiva + 1
        
        return {
            "deductiva": inferencia_deductiva / total,
            "inductiva": inferencia_inductiva / total,
            "abductiva": inferencia_abductiva / total,
            "estilo_dominante": max([
                ("deductiva", inferencia_deductiva),
                ("inductiva", inferencia_inductiva),
                ("abductiva", inferencia_abductiva)
            ], key=lambda x: x[1])[0]
        }
    
    def _generar_meta_analisis(self, patrones, arquitectura, velocidad) -> Dict[str, Any]:
        """Genera un meta-análisis del perfil cognitivo"""
        
        # CLASIFICACIÓN COGNITIVA GENERAL
        if arquitectura["organización_dominante"] == "secuencial" and velocidad["tempo_dominante"] == "pausada":
            tipo_mente = "Metódica-Sistemática"
        elif arquitectura["organización_dominante"] == "reticular" and velocidad["tempo_dominante"] == "rápida":
            tipo_mente = "Integrativa-Ágil"
        elif arquitectura["organización_dominante"] == "jerárquico":
            tipo_mente = "Estructural-Ordenada"
        else:
            tipo_mente = "Adaptativa-Flexible"
        
        return {
            "tipo_mente": tipo_mente,
            "complejidad_cognitiva": np.mean([
                sum([v for v in patrones.values() if isinstance(v, dict) and 'híbrido' in v]),
                arquitectura.get('reticular', 0),
                velocidad.get('velocidad_variable', 0)
            ]),
            "eficiencia_cognitiva": np.mean([
                velocidad.get('velocidad_rápida', 0),
                arquitectura.get('secuencial', 0)
            ]),
            "creatividad_cognitiva": np.mean([
                patrones.get('convergente_vs_divergente', {}).get('divergente', 0),
                arquitectura.get('reticular', 0)
            ])
        }
    
    def procesar_documento_completo(self, ruta_documento: str) -> Dict[str, Any]:
        """Procesa un documento completo extrayendo solo patrones de pensamiento"""
        
        print(f"📄 Procesando documento para análisis de pensamiento: {ruta_documento}")
        
        # LEER DOCUMENTO (implementar según formato)
        texto = self._leer_documento(ruta_documento)
        
        # DETECTAR AUTOR
        autor = self._detectar_autor(texto, ruta_documento)
        
        # EXTRAER PENSAMIENTO PURO
        perfil_pensamiento = self.extraer_pensamiento_puro(texto, autor)
        
        # ANÁLISIS COMPLEMENTARIOS
        perfil_pensamiento.update({
            "metodologia_juridica": analizar_metodologia_completa(texto),
            "modalidad_epistemica": detectar_modalidad_epistemica(texto),
            "estructura_silogistica": analizar_estructura_silogistica(texto),
            "analisis_multicapa": self.analizador_multicapa.analizar_autor_completo(autor, [texto])
        })
        
        return perfil_pensamiento
    
    def _leer_documento(self, ruta: str) -> str:
        """Lee documento según su formato"""
        # Implementar lectura de PDF, DOCX, TXT
        # Por simplicidad, asumo que ya está implementado
        pass
    
    def _detectar_autor(self, texto: str, ruta: str) -> str:
        """Detecta el autor del documento"""
        # Usar detector existente
        pass

def main():
    """Función principal para probar el motor"""
    
    motor = MotorIngestaPensamiento()
    
    # EJEMPLO DE USO
    texto_ejemplo = """
    En primer lugar, debemos analizar sistemáticamente los elementos que configuran 
    esta figura jurídica. La doctrina establece claramente que no puede haber 
    ambigüedad en la interpretación. Por tanto, se sigue necesariamente que 
    la única opción viable es aplicar el criterio restrictivo.
    """
    
    perfil = motor.extraer_pensamiento_puro(texto_ejemplo, "Autor de Prueba")
    
    print("🧠 PERFIL DE PENSAMIENTO EXTRAÍDO:")
    print(json.dumps(perfil, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()