#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚖️ ANALIZADOR ESTRUCTURAL DE SENTENCIAS - V7.6
==============================================

Módulo especializado para el análisis de la estructura tripartita
de sentencias judiciales argentinas: VISTO - CONSIDERANDO - RESUELVO

CARACTERÍSTICAS:
- Identificación automática de las tres secciones
- Extracción de contenido específico por sección
- Análisis diferenciado para medición de distancia doctrinal
- Reconocimiento de patrones jurídicos argentinos

AUTOR: Sistema Cognitivo v7.6
FECHA: 11 NOV 2025
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class SeccionSentencia:
    """Representa una sección de la sentencia"""
    tipo: str  # 'visto', 'considerando', 'resuelvo'
    inicio: int  # posición de inicio en el texto
    fin: int     # posición de fin en el texto
    contenido: str  # texto de la sección
    
class AnalizadorEstructuralSentencias:
    """
    🏛️ ANALIZADOR ESTRUCTURAL DE SENTENCIAS
    
    Reconoce y analiza la estructura tripartita obligatoria de las 
    sentencias judiciales argentinas según tu especificación:
    
    📋 VISTO: Sección inicial (demanda, partes, objeto del proceso)
    ⚖️ CONSIDERANDO: Núcleo argumentativo (hechos, razonamiento jurídico)  
    📋 RESUELVO: Parte dispositiva (decisiones, óptica del tribunal)
    """
    
    def __init__(self):
        # Patrones para identificar secciones principales
        self.patrones_visto = [
            r'\bVISTO\b:?\s*',
            r'\bV\s*I\s*S\s*T\s*O\b:?\s*',
            r'\bVISTA\b:?\s*'
        ]
        
        self.patrones_considerando = [
            r'\bCONSIDERANDO\b:?\s*',
            r'\bC\s*O\s*N\s*S\s*I\s*D\s*E\s*R\s*A\s*N\s*D\s*O\b:?\s*',
            r'\bCONSIDERANDOS?\b:?\s*',
            r'\bY\s+CONSIDERANDO\b:?\s*'
        ]
        
        self.patrones_resuelvo = [
            r'\bRESUELVO\b:?\s*',
            r'\bR\s*E\s*S\s*U\s*E\s*L\s*V\s*O\b:?\s*',
            r'\bPOR\s+ELLO\b[^.]*\bRESUELVO\b:?\s*',
            r'\bFALLO\b:?\s*',
            r'\bDECIDO\b:?\s*'
        ]
        
        # Patrones para análisis de contenido específico
        self.patrones_contenido = {
            'visto': {
                'demanda': r'demanda\s+interpuesta\s+por\s+([^.]+)',
                'partes': r'([A-Z][A-Za-z\s,]+)\s+c/\s+([A-Z][A-Za-z\s,]+)',
                'expediente': r'expediente\s+n[°º]?\s*([A-Z0-9\-/]+)',
                'caratula': r'autos:?\s*["\']([^"\']+)["\']',
                'objeto': r's/\s*([^"\']+?)(?:["\']|$)',
                'referencias': r'fs?\.\s*(\d+(?:/\d+)?)'
            },
            'considerando': {
                'hechos': r'que\s+surge\s+de\s+autos\s+que\s+([^.]+)',
                'doctrina': r'(?:doctrina|autor(?:es)?|tratadista)\s+([^.]+?)(?:establece|sostiene|considera)\s+que\s+([^.]+)',
                'jurisprudencia': r'(?:jurisprudencia|fallos?|precedente)\s+([^.]+)',
                'normativa': r'(?:art(?:ículo)?|inc(?:iso)?|ley)\s+([^.]+)',
                'razonamiento': r'este\s+(?:tribunal|juzgado|magistrado)\s+(?:considera|entiende)\s+que\s+([^.]+)',
                'prueba': r'(?:probado|acreditado|demostrado)\s+que\s+([^.]+)'
            },
            'resuelvo': {
                'decision_principal': r'(?:hacer\s+lugar|rechazar|admitir)\s+(?:a\s+)?la\s+([^.]+)',
                'condena': r'condenar?\s+a\s+([^.]+?)(?:\s+al?\s+pago\s+de\s+([^.]+))?',
                'costas': r'(?:imponer|costas)\s+([^.]+)',
                'recursos': r'(?:recursos?|apelación)\s+([^.]+)',
                'honorarios': r'honorarios?\s+([^.]+)'
            }
        }
    
    def identificar_secciones(self, texto: str) -> List[SeccionSentencia]:
        """
        🔍 Identifica las tres secciones principales de la sentencia
        
        Args:
            texto: Texto completo de la sentencia
            
        Returns:
            Lista de secciones identificadas con sus posiciones
        """
        secciones = []
        texto_upper = texto.upper()
        
        # Buscar VISTO
        visto_match = None
        for patron in self.patrones_visto:
            match = re.search(patron, texto_upper)
            if match:
                visto_match = match
                break
        
        # Buscar CONSIDERANDO
        considerando_match = None
        for patron in self.patrones_considerando:
            match = re.search(patron, texto_upper)
            if match:
                considerando_match = match
                break
        
        # Buscar RESUELVO
        resuelvo_match = None
        for patron in self.patrones_resuelvo:
            match = re.search(patron, texto_upper)
            if match:
                resuelvo_match = match
                break
        
        # Crear secciones con contenido
        if visto_match:
            fin_visto = considerando_match.start() if considerando_match else len(texto)
            secciones.append(SeccionSentencia(
                tipo='visto',
                inicio=visto_match.start(),
                fin=fin_visto,
                contenido=texto[visto_match.end():fin_visto].strip()
            ))
        
        if considerando_match:
            fin_considerando = resuelvo_match.start() if resuelvo_match else len(texto)
            secciones.append(SeccionSentencia(
                tipo='considerando', 
                inicio=considerando_match.start(),
                fin=fin_considerando,
                contenido=texto[considerando_match.end():fin_considerando].strip()
            ))
        
        if resuelvo_match:
            # Buscar final (firma del juez o final del documento)
            patron_firma = r'(?:Dr\.|Dra\.|Juez|Jueza|Magistrado)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*'
            firma_match = re.search(patron_firma, texto[resuelvo_match.end():])
            fin_resuelvo = resuelvo_match.end() + firma_match.start() if firma_match else len(texto)
            
            secciones.append(SeccionSentencia(
                tipo='resuelvo',
                inicio=resuelvo_match.start(),
                fin=fin_resuelvo,
                contenido=texto[resuelvo_match.end():fin_resuelvo].strip()
            ))
        
        return secciones
    
    def analizar_visto(self, contenido: str) -> Dict:
        """
        📋 Analiza la sección VISTO
        
        Extrae: demanda interpuesta, partes, objeto del proceso,
        referencias a actuaciones principales
        """
        resultados = {
            'demanda_interpuesta': None,
            'partes': {'actor': None, 'demandado': None},
            'expediente': None,
            'caratula': None,
            'objeto_proceso': None,
            'referencias_procesales': []
        }
        
        # Extraer información específica
        for clave, patron in self.patrones_contenido['visto'].items():
            matches = re.findall(patron, contenido, re.IGNORECASE)
            
            if clave == 'demanda' and matches:
                resultados['demanda_interpuesta'] = matches[0].strip()
            elif clave == 'partes' and matches:
                if matches[0]:  # tuple (actor, demandado)
                    resultados['partes']['actor'] = matches[0][0].strip()
                    resultados['partes']['demandado'] = matches[0][1].strip()
            elif clave == 'expediente' and matches:
                resultados['expediente'] = matches[0].strip()
            elif clave == 'caratula' and matches:
                resultados['caratula'] = matches[0].strip()
            elif clave == 'objeto' and matches:
                resultados['objeto_proceso'] = matches[0].strip()
            elif clave == 'referencias' and matches:
                resultados['referencias_procesales'] = matches
        
        return resultados
    
    def analizar_considerando(self, contenido: str) -> Dict:
        """
        ⚖️ Analiza la sección CONSIDERANDO
        
        Extrae: hechos probados, razonamiento jurídico, citas doctrinales,
        jurisprudencia, normativa aplicable
        
        IMPORTANTE: Aquí se mide principalmente la distancia doctrinal
        """
        resultados = {
            'hechos_probados': [],
            'doctrina_citada': [],
            'jurisprudencia_citada': [],
            'normativa_aplicada': [],
            'razonamiento_tribunal': [],
            'elementos_probatorios': []
        }
        
        # Extraer información específica del considerando
        for clave, patron in self.patrones_contenido['considerando'].items():
            matches = re.findall(patron, contenido, re.IGNORECASE | re.DOTALL)
            
            if clave == 'hechos' and matches:
                resultados['hechos_probados'].extend(match.strip() for match in matches)
            elif clave == 'doctrina' and matches:
                # matches es lista de tuplas (autor, posición)
                for match in matches:
                    if isinstance(match, tuple) and len(match) == 2:
                        resultados['doctrina_citada'].append({
                            'autor': match[0].strip(),
                            'posicion': match[1].strip()
                        })
            elif clave == 'jurisprudencia' and matches:
                resultados['jurisprudencia_citada'].extend(match.strip() for match in matches)
            elif clave == 'normativa' and matches:
                resultados['normativa_aplicada'].extend(match.strip() for match in matches)
            elif clave == 'razonamiento' and matches:
                resultados['razonamiento_tribunal'].extend(match.strip() for match in matches)
            elif clave == 'prueba' and matches:
                resultados['elementos_probatorios'].extend(match.strip() for match in matches)
        
        return resultados
    
    def analizar_resuelvo(self, contenido: str) -> Dict:
        """
        📋 Analiza la sección RESUELVO
        
        Extrae: decisiones finales, condenas, costas, recursos,
        todas las cuestiones desde la óptica del tribunal
        """
        resultados = {
            'decision_principal': None,
            'condenas': [],
            'costas': None,
            'recursos_admisibles': [],
            'honorarios': [],
            'mandatos_especificos': []
        }
        
        # Extraer información específica del resuelvo
        for clave, patron in self.patrones_contenido['resuelvo'].items():
            matches = re.findall(patron, contenido, re.IGNORECASE)
            
            if clave == 'decision_principal' and matches:
                resultados['decision_principal'] = matches[0].strip()
            elif clave == 'condena' and matches:
                for match in matches:
                    if isinstance(match, tuple):
                        condena = {
                            'sujeto': match[0].strip() if match[0] else None,
                            'monto': match[1].strip() if len(match) > 1 and match[1] else None
                        }
                        resultados['condenas'].append(condena)
            elif clave == 'costas' and matches:
                resultados['costas'] = matches[0].strip()
            elif clave == 'recursos' and matches:
                resultados['recursos_admisibles'].extend(match.strip() for match in matches)
            elif clave == 'honorarios' and matches:
                resultados['honorarios'].extend(match.strip() for match in matches)
        
        # Buscar mandatos numerados (1°), 2°), etc.)
        mandatos = re.findall(r'(\d+[°º]?\))\s*([^1-9]+?)(?=\d+[°º]?\)|$)', contenido, re.DOTALL)
        for numero, texto in mandatos:
            resultados['mandatos_especificos'].append({
                'numero': numero.strip(),
                'contenido': texto.strip()
            })
        
        return resultados
    
    def analizar_sentencia_completa(self, texto: str) -> Dict:
        """
        🏛️ Análisis completo de sentencia con estructura tripartita
        
        Returns:
            Diccionario con análisis completo de las tres secciones
        """
        secciones = self.identificar_secciones(texto)
        
        resultado = {
            'estructura_detectada': {
                'visto_encontrado': False,
                'considerando_encontrado': False, 
                'resuelvo_encontrado': False
            },
            'analisis_por_seccion': {},
            'metricas_estructurales': {}
        }
        
        for seccion in secciones:
            resultado['estructura_detectada'][f'{seccion.tipo}_encontrado'] = True
            
            if seccion.tipo == 'visto':
                resultado['analisis_por_seccion']['visto'] = self.analizar_visto(seccion.contenido)
            elif seccion.tipo == 'considerando':
                resultado['analisis_por_seccion']['considerando'] = self.analizar_considerando(seccion.contenido)
            elif seccion.tipo == 'resuelvo':
                resultado['analisis_por_seccion']['resuelvo'] = self.analizar_resuelvo(seccion.contenido)
        
        # Métricas estructurales
        total_secciones = sum(resultado['estructura_detectada'].values())
        resultado['metricas_estructurales'] = {
            'completitud_estructural': total_secciones / 3.0,  # 0.0 a 1.0
            'secciones_detectadas': total_secciones,
            'estructura_valida': total_secciones == 3
        }
        
        return resultado

def test_analizador():
    """🧪 Test del analizador estructural"""
    
    texto_ejemplo = """
    JUZGADO CIVIL Y COMERCIAL N° 5 - LA PLATA
    EXPEDIENTE N° 12345/2023
    AUTOS: "GARCÍA, JUAN c/ CLÍNICA MODELO S.A. s/ DAÑOS Y PERJUICIOS"
    
    VISTO: La demanda interpuesta por Juan García contra Clínica Modelo S.A. 
    reclamando daños y perjuicios por mala praxis médica, obrante a fs. 1/15, 
    la contestación de demanda de fs. 20/25, y las pruebas rendidas...
    
    CONSIDERANDO: I) Que surge de autos que el actor se sometió a una 
    intervención quirúrgica el día 10/01/2022 en el establecimiento demandado.
    La doctrina mayoritaria establece que en casos de mala praxis médica, 
    la carga probatoria recae sobre el paciente (conf. López, "Responsabilidad 
    Médica", p. 123). Sin embargo, este tribunal considera que se ha configurado 
    la responsabilidad del demandado según surge de la pericia médica de fs. 45.
    
    II) Que analizando la prueba rendida, se encuentra probado que hubo 
    negligencia en el tratamiento...
    
    POR ELLO, oído el Ministerio Público y RESUELVO: 
    1°) HACER LUGAR a la demanda interpuesta por Juan García.
    2°) CONDENAR a Clínica Modelo S.A. al pago de $500.000 por daños y perjuicios.
    3°) IMPONER las costas al demandado vencido.
    
                                    Dr. ROBERTO MARTINEZ
                                        Juez Titular
    """
    
    analizador = AnalizadorEstructuralSentencias()
    resultado = analizador.analizar_sentencia_completa(texto_ejemplo)
    
    print("🔍 RESULTADO DEL ANÁLISIS ESTRUCTURAL")
    print("=" * 50)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_analizador()