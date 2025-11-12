#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
❓ SISTEMA DE PREGUNTAS JUDICIALES v1.0
========================================

Catálogo de 140+ preguntas predeterminadas sobre jueces argentinos.

Categorías:
A. Perfil e Identidad Judicial (20 preguntas)
B. Metodología Interpretativa (20 preguntas)
C. Protección de Derechos (20 preguntas)
D. Líneas Jurisprudenciales (20 preguntas)
E. Red de Influencias (15 preguntas)
F. Análisis Predictivo (15 preguntas)
G. Sesgos y Tendencias (15 preguntas)
H. Casos Específicos (15 preguntas)

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

from typing import Dict, List
from dataclasses import dataclass, asdict
import json

@dataclass
class Pregunta:
    """Representa una pregunta del sistema"""
    id: str
    categoria: str
    pregunta: str
    tipo_respuesta: str  # 'texto', 'numero', 'score', 'lista', 'boolean'
    requiere_bd: bool
    campos_necesarios: List[str]

    def to_dict(self):
        return asdict(self)


class SistemaPreguntasJudiciales:
    """
    Catálogo completo de preguntas sobre jueces argentinos
    """

    def __init__(self):
        """Inicializa el sistema con todas las preguntas"""
        self.preguntas = self._definir_preguntas()

    def _definir_preguntas(self) -> Dict[str, List[Pregunta]]:
        """Define todas las preguntas del sistema"""

        preguntas = {}

        # =====================================================================
        # CATEGORÍA A: PERFIL E IDENTIDAD JUDICIAL (20 preguntas)
        # =====================================================================
        preguntas['A'] = [
            Pregunta(
                id='A01',
                categoria='Perfil e Identidad',
                pregunta='¿Cuál es el perfil judicial general de este juez?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['tendencia_activismo', 'nivel_formalismo', 'interpretacion_dominante']
            ),
            Pregunta(
                id='A02',
                categoria='Perfil e Identidad',
                pregunta='¿Es un juez activista o restrictivo?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['tendencia_activismo']
            ),
            Pregunta(
                id='A03',
                categoria='Perfil e Identidad',
                pregunta='¿Cuál es su nivel de formalismo?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['nivel_formalismo']
            ),
            Pregunta(
                id='A04',
                categoria='Perfil e Identidad',
                pregunta='¿En qué fuero se desempeña principalmente?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['fuero']
            ),
            Pregunta(
                id='A05',
                categoria='Perfil e Identidad',
                pregunta='¿En qué jurisdicción actúa (federal/provincial)?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['jurisdiccion']
            ),
            Pregunta(
                id='A06',
                categoria='Perfil e Identidad',
                pregunta='¿A qué tribunal pertenece?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['tribunal']
            ),
            Pregunta(
                id='A07',
                categoria='Perfil e Identidad',
                pregunta='¿Cuántas sentencias se han analizado?',
                tipo_respuesta='numero',
                requiere_bd=True,
                campos_necesarios=['total_sentencias']
            ),
            Pregunta(
                id='A08',
                categoria='Perfil e Identidad',
                pregunta='¿Cuál es el nivel de confianza del análisis?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['confianza_analisis']
            ),
            Pregunta(
                id='A09',
                categoria='Perfil e Identidad',
                pregunta='¿Es un juez individual o una sala colegiada?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['tipo_entidad']
            ),
            Pregunta(
                id='A10',
                categoria='Perfil e Identidad',
                pregunta='¿Cuál es su frecuencia de control de constitucionalidad?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['frecuencia_control_constitucionalidad']
            ),
            Pregunta(
                id='A11',
                categoria='Perfil e Identidad',
                pregunta='¿Aplica interpretación conforme a tratados internacionales?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['uso_tratados_internacionales']
            ),
            Pregunta(
                id='A12',
                categoria='Perfil e Identidad',
                pregunta='¿Cuál es su nivel de innovación jurisprudencial?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['nivel_innovacion_jurisprudencial']
            ),
            Pregunta(
                id='A13',
                categoria='Perfil e Identidad',
                pregunta='¿Cuál es su nivel de deferencia institucional?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['deferencia_institucional']
            ),
            Pregunta(
                id='A14',
                categoria='Perfil e Identidad',
                pregunta='¿Cómo se compara con otros jueces de su fuero?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['fuero', 'tendencia_activismo']
            ),
            Pregunta(
                id='A15',
                categoria='Perfil e Identidad',
                pregunta='¿Cuáles son sus principales características distintivas?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['tendencia_activismo', 'nivel_formalismo', 'interpretacion_dominante']
            ),
            Pregunta(
                id='A16',
                categoria='Perfil e Identidad',
                pregunta='¿En qué materias se especializa?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['total_sentencias']
            ),
            Pregunta(
                id='A17',
                categoria='Perfil e Identidad',
                pregunta='¿Tiene un perfil garantista o restrictivo?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['sesgo_garantista']
            ),
            Pregunta(
                id='A18',
                categoria='Perfil e Identidad',
                pregunta='¿Cuál es su balance entre sustancia y forma?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['nivel_formalismo']
            ),
            Pregunta(
                id='A19',
                categoria='Perfil e Identidad',
                pregunta='¿Se considera un juez predecible?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['confianza_analisis']
            ),
            Pregunta(
                id='A20',
                categoria='Perfil e Identidad',
                pregunta='¿Cuál es su perfil completo en una síntesis?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['tendencia_activismo', 'nivel_formalismo', 'interpretacion_dominante', 'fuero']
            ),
        ]

        # =====================================================================
        # CATEGORÍA B: METODOLOGÍA INTERPRETATIVA (20 preguntas)
        # =====================================================================
        preguntas['B'] = [
            Pregunta(
                id='B01',
                categoria='Metodología Interpretativa',
                pregunta='¿Cuál es su método interpretativo dominante?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['interpretacion_dominante']
            ),
            Pregunta(
                id='B02',
                categoria='Metodología Interpretativa',
                pregunta='¿Con qué frecuencia usa interpretación literal?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['frecuencia_interpretacion_literal']
            ),
            Pregunta(
                id='B03',
                categoria='Metodología Interpretativa',
                pregunta='¿Con qué frecuencia usa interpretación sistemática?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['frecuencia_interpretacion_sistematica']
            ),
            Pregunta(
                id='B04',
                categoria='Metodología Interpretativa',
                pregunta='¿Con qué frecuencia usa interpretación teleológica?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['frecuencia_interpretacion_teleologica']
            ),
            Pregunta(
                id='B05',
                categoria='Metodología Interpretativa',
                pregunta='¿Usa interpretación histórica?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['frecuencia_interpretacion_historica']
            ),
            Pregunta(
                id='B06',
                categoria='Metodología Interpretativa',
                pregunta='¿Aplica el test de proporcionalidad?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['usa_test_proporcionalidad']
            ),
            Pregunta(
                id='B07',
                categoria='Metodología Interpretativa',
                pregunta='¿Aplica el test de razonabilidad?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['usa_test_razonabilidad']
            ),
            Pregunta(
                id='B08',
                categoria='Metodología Interpretativa',
                pregunta='¿Usa el principio in dubio pro operario?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['usa_in_dubio_pro_operario']
            ),
            Pregunta(
                id='B09',
                categoria='Metodología Interpretativa',
                pregunta='¿Usa el principio in dubio pro consumidor?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['usa_in_dubio_pro_consumidor']
            ),
            Pregunta(
                id='B10',
                categoria='Metodología Interpretativa',
                pregunta='¿Aplica el test de escrutinio estricto?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['usa_escrutinio_estricto']
            ),
            Pregunta(
                id='B11',
                categoria='Metodología Interpretativa',
                pregunta='¿Cuál es su estándar probatorio dominante?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['estandar_probatorio_dominante']
            ),
            Pregunta(
                id='B12',
                categoria='Metodología Interpretativa',
                pregunta='¿Usa sana crítica en la valoración probatoria?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['frecuencia_sana_critica']
            ),
            Pregunta(
                id='B13',
                categoria='Metodología Interpretativa',
                pregunta='¿Con qué frecuencia cita legislación?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['densidad_citas_legislacion']
            ),
            Pregunta(
                id='B14',
                categoria='Metodología Interpretativa',
                pregunta='¿Con qué frecuencia cita jurisprudencia?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['densidad_citas_jurisprudencia']
            ),
            Pregunta(
                id='B15',
                categoria='Metodología Interpretativa',
                pregunta='¿Con qué frecuencia cita doctrina?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['densidad_citas_doctrina']
            ),
            Pregunta(
                id='B16',
                categoria='Metodología Interpretativa',
                pregunta='¿Qué tests o doctrinas aplica más frecuentemente?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['usa_test_proporcionalidad', 'usa_test_razonabilidad', 'usa_in_dubio_pro_operario']
            ),
            Pregunta(
                id='B17',
                categoria='Metodología Interpretativa',
                pregunta='¿Realiza balancing de derechos en casos de colisión?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['frecuencia_balancing_derechos']
            ),
            Pregunta(
                id='B18',
                categoria='Metodología Interpretativa',
                pregunta='¿Cómo interpreta normas ambiguas?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['interpretacion_dominante']
            ),
            Pregunta(
                id='B19',
                categoria='Metodología Interpretativa',
                pregunta='¿Es originalista o no originalista en interpretación constitucional?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['frecuencia_interpretacion_historica', 'frecuencia_interpretacion_teleologica']
            ),
            Pregunta(
                id='B20',
                categoria='Metodología Interpretativa',
                pregunta='¿Cuál es su enfoque metodológico general?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['interpretacion_dominante', 'nivel_formalismo']
            ),
        ]

        # =====================================================================
        # CATEGORÍA C: PROTECCIÓN DE DERECHOS (20 preguntas)
        # =====================================================================
        preguntas['C'] = [
            Pregunta(
                id='C01',
                categoria='Protección de Derechos',
                pregunta='¿Cuál es su nivel de protección de derechos laborales?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['proteccion_trabajo']
            ),
            Pregunta(
                id='C02',
                categoria='Protección de Derechos',
                pregunta='¿Cuál es su nivel de protección del derecho a la igualdad?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['proteccion_igualdad']
            ),
            Pregunta(
                id='C03',
                categoria='Protección de Derechos',
                pregunta='¿Cuál es su nivel de protección de la libertad de expresión?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['proteccion_libertad_expresion']
            ),
            Pregunta(
                id='C04',
                categoria='Protección de Derechos',
                pregunta='¿Cuál es su nivel de protección de la privacidad?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['proteccion_privacidad']
            ),
            Pregunta(
                id='C05',
                categoria='Protección de Derechos',
                pregunta='¿Cuál es su nivel de protección del derecho de propiedad?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['proteccion_propiedad']
            ),
            Pregunta(
                id='C06',
                categoria='Protección de Derechos',
                pregunta='¿Cuál es su nivel de protección de derechos del consumidor?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['proteccion_consumidor']
            ),
            Pregunta(
                id='C07',
                categoria='Protección de Derechos',
                pregunta='¿Protege derechos sociales expansivamente?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['proteccion_trabajo', 'proteccion_consumidor']
            ),
            Pregunta(
                id='C08',
                categoria='Protección de Derechos',
                pregunta='¿Protege derechos civiles expansivamente?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['proteccion_libertad_expresion', 'proteccion_privacidad']
            ),
            Pregunta(
                id='C09',
                categoria='Protección de Derechos',
                pregunta='¿Qué derechos protege con mayor intensidad?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['proteccion_trabajo', 'proteccion_igualdad', 'proteccion_libertad_expresion', 'proteccion_privacidad', 'proteccion_propiedad', 'proteccion_consumidor']
            ),
            Pregunta(
                id='C10',
                categoria='Protección de Derechos',
                pregunta='¿Qué derechos protege con menor intensidad?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['proteccion_trabajo', 'proteccion_igualdad', 'proteccion_libertad_expresion', 'proteccion_privacidad', 'proteccion_propiedad', 'proteccion_consumidor']
            ),
            Pregunta(
                id='C11',
                categoria='Protección de Derechos',
                pregunta='¿Cómo resuelve colisiones entre derechos laborales y empresariales?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['proteccion_trabajo', 'sesgo_pro_trabajador']
            ),
            Pregunta(
                id='C12',
                categoria='Protección de Derechos',
                pregunta='¿Cómo resuelve colisiones entre libertad de expresión y derecho al honor?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['proteccion_libertad_expresion', 'frecuencia_balancing_derechos']
            ),
            Pregunta(
                id='C13',
                categoria='Protección de Derechos',
                pregunta='¿Aplica estándares especiales de protección en casos de discriminación?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['proteccion_igualdad', 'usa_escrutinio_estricto']
            ),
            Pregunta(
                id='C14',
                categoria='Protección de Derechos',
                pregunta='¿Protege derechos económicos de forma robusta?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['proteccion_propiedad']
            ),
            Pregunta(
                id='C15',
                categoria='Protección de Derechos',
                pregunta='¿Tiene un enfoque protectorio o restrictivo en derechos fundamentales?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['tendencia_activismo']
            ),
            Pregunta(
                id='C16',
                categoria='Protección de Derechos',
                pregunta='¿Reconoce derechos implícitos o no enumerados?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['reconocimiento_derechos_implicitos']
            ),
            Pregunta(
                id='C17',
                categoria='Protección de Derechos',
                pregunta='¿Aplica el principio pro homine?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['uso_tratados_internacionales']
            ),
            Pregunta(
                id='C18',
                categoria='Protección de Derechos',
                pregunta='¿Cuál es su balance general de protección de derechos?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['proteccion_trabajo', 'proteccion_igualdad', 'proteccion_libertad_expresion']
            ),
            Pregunta(
                id='C19',
                categoria='Protección de Derechos',
                pregunta='¿Expande o restringe el alcance de derechos constitucionales?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['tendencia_activismo']
            ),
            Pregunta(
                id='C20',
                categoria='Protección de Derechos',
                pregunta='¿Cómo se compara su protección de derechos con el promedio judicial?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['proteccion_trabajo', 'proteccion_igualdad']
            ),
        ]

        # =====================================================================
        # CATEGORÍA D: LÍNEAS JURISPRUDENCIALES (20 preguntas)
        # =====================================================================
        preguntas['D'] = [
            Pregunta(
                id='D01',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Cuáles son las principales líneas jurisprudenciales del juez?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D02',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿En qué temas tiene líneas más consolidadas?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D03',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Cuál es su nivel de consistencia en materia laboral?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D04',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Cuál es su nivel de consistencia en materia civil?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D05',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Tiene líneas contradictorias en algún tema?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D06',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Cuáles son sus casos paradigmáticos más importantes?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D07',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Ha modificado sustancialmente alguna línea a lo largo del tiempo?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D08',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Cuál es su criterio dominante en casos de despido?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D09',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Cuál es su criterio dominante en casos de discriminación?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D10',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Cuál es su criterio dominante en casos de daños y perjuicios?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D11',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Tiene líneas consolidadas en materia de derechos del consumidor?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D12',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Cuántas sentencias componen cada línea jurisprudencial?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D13',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Qué líneas tienen mayor confianza estadística?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D14',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Hay excepciones significativas a sus líneas principales?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D15',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Se puede predecir su decisión basándose en líneas anteriores?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales', 'confianza_analisis']
            ),
            Pregunta(
                id='D16',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Qué factores determinan sus líneas jurisprudenciales?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales', 'factores_predictivos']
            ),
            Pregunta(
                id='D17',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Es un juez consistente o variable en sus criterios?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D18',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Cuál es su línea más sólida y predecible?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D19',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Cuál es su línea más variable o inconsistente?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='D20',
                categoria='Líneas Jurisprudenciales',
                pregunta='¿Resumen ejecutivo de todas sus líneas jurisprudenciales?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
        ]

        # =====================================================================
        # CATEGORÍA E: RED DE INFLUENCIAS (15 preguntas)
        # =====================================================================
        preguntas['E'] = [
            Pregunta(
                id='E01',
                categoria='Red de Influencias',
                pregunta='¿Qué tribunales superiores cita más frecuentemente?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial']
            ),
            Pregunta(
                id='E02',
                categoria='Red de Influencias',
                pregunta='¿Con qué frecuencia cita a la CSJN?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial']
            ),
            Pregunta(
                id='E03',
                categoria='Red de Influencias',
                pregunta='¿Qué autores doctrinales cita más frecuentemente?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial']
            ),
            Pregunta(
                id='E04',
                categoria='Red de Influencias',
                pregunta='¿Cuál es su intensidad de citas doctrinales?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['densidad_citas_doctrina']
            ),
            Pregunta(
                id='E05',
                categoria='Red de Influencias',
                pregunta='¿Cuál es su intensidad de citas jurisprudenciales?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['densidad_citas_jurisprudencia']
            ),
            Pregunta(
                id='E06',
                categoria='Red de Influencias',
                pregunta='¿Qué salas de cámaras cita más frecuentemente?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial']
            ),
            Pregunta(
                id='E07',
                categoria='Red de Influencias',
                pregunta='¿Tiene influencias internacionales (tribunales extranjeros, CIDH)?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['uso_tratados_internacionales', 'redes_influencia_judicial']
            ),
            Pregunta(
                id='E08',
                categoria='Red de Influencias',
                pregunta='¿Cuáles son sus top 5 fuentes de influencia?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial']
            ),
            Pregunta(
                id='E09',
                categoria='Red de Influencias',
                pregunta='¿Cita autores laboralistas específicos?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial', 'fuero']
            ),
            Pregunta(
                id='E10',
                categoria='Red de Influencias',
                pregunta='¿Cita constitucionalistas específicos?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial']
            ),
            Pregunta(
                id='E11',
                categoria='Red de Influencias',
                pregunta='¿Cuál es su red de influencia completa?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial']
            ),
            Pregunta(
                id='E12',
                categoria='Red de Influencias',
                pregunta='¿Depende fuertemente de la CSJN o es más independiente?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial']
            ),
            Pregunta(
                id='E13',
                categoria='Red de Influencias',
                pregunta='¿Es más jurisprudencial o más doctrinal en sus fundamentos?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['densidad_citas_jurisprudencia', 'densidad_citas_doctrina']
            ),
            Pregunta(
                id='E14',
                categoria='Red de Influencias',
                pregunta='¿Cuál es la intensidad promedio de sus influencias?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial']
            ),
            Pregunta(
                id='E15',
                categoria='Red de Influencias',
                pregunta='¿Tiene un patrón distintivo en su red de influencias?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial']
            ),
        ]

        # =====================================================================
        # CATEGORÍA F: ANÁLISIS PREDICTIVO (15 preguntas)
        # =====================================================================
        preguntas['F'] = [
            Pregunta(
                id='F01',
                categoria='Análisis Predictivo',
                pregunta='¿Hay un modelo predictivo disponible para este juez?',
                tipo_respuesta='boolean',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F02',
                categoria='Análisis Predictivo',
                pregunta='¿Cuál es la precisión (accuracy) del modelo predictivo?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F03',
                categoria='Análisis Predictivo',
                pregunta='¿Cuáles son los factores más determinantes en sus decisiones?',
                tipo_respuesta='lista',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F04',
                categoria='Análisis Predictivo',
                pregunta='¿Qué factor tiene mayor peso predictivo?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F05',
                categoria='Análisis Predictivo',
                pregunta='¿La materia del caso es un factor determinante?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F06',
                categoria='Análisis Predictivo',
                pregunta='¿El tipo de actor (empresa/persona) influye en sus decisiones?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F07',
                categoria='Análisis Predictivo',
                pregunta='¿El tipo de demandado influye en sus decisiones?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F08',
                categoria='Análisis Predictivo',
                pregunta='¿Aplicar test de proporcionalidad predice el resultado?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F09',
                categoria='Análisis Predictivo',
                pregunta='¿Aplicar in dubio pro operario predice el resultado?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F10',
                categoria='Análisis Predictivo',
                pregunta='¿La protección de derechos laborales predice el resultado?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F11',
                categoria='Análisis Predictivo',
                pregunta='¿Qué probabilidad hay de que haga lugar a un reclamo laboral?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos', 'lineas_jurisprudenciales']
            ),
            Pregunta(
                id='F12',
                categoria='Análisis Predictivo',
                pregunta='¿Qué probabilidad hay de que haga lugar a un reclamo de consumidor?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos', 'lineas_jurisprudenciales']
            ),
            Pregunta(
                id='F13',
                categoria='Análisis Predictivo',
                pregunta='¿Es un juez predecible o impredecible según el modelo?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F14',
                categoria='Análisis Predictivo',
                pregunta='¿Cuántas sentencias se usaron para entrenar el modelo?',
                tipo_respuesta='numero',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='F15',
                categoria='Análisis Predictivo',
                pregunta='¿Cuál es la confianza del modelo predictivo?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
        ]

        # =====================================================================
        # CATEGORÍA G: SESGOS Y TENDENCIAS (15 preguntas)
        # =====================================================================
        preguntas['G'] = [
            Pregunta(
                id='G01',
                categoria='Sesgos y Tendencias',
                pregunta='¿Tiene sesgo pro-trabajador?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_trabajador']
            ),
            Pregunta(
                id='G02',
                categoria='Sesgos y Tendencias',
                pregunta='¿Tiene sesgo pro-empresa?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_empresa']
            ),
            Pregunta(
                id='G03',
                categoria='Sesgos y Tendencias',
                pregunta='¿Es garantista en materia penal?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['sesgo_garantista']
            ),
            Pregunta(
                id='G04',
                categoria='Sesgos y Tendencias',
                pregunta='¿Es punitivista en materia penal?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['sesgo_punitivista']
            ),
            Pregunta(
                id='G05',
                categoria='Sesgos y Tendencias',
                pregunta='¿Tiene sesgo pro-consumidor?',
                tipo_respuesta='score',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_consumidor']
            ),
            Pregunta(
                id='G06',
                categoria='Sesgos y Tendencias',
                pregunta='¿Cuál es su sesgo dominante?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_trabajador', 'sesgo_pro_empresa', 'sesgo_garantista', 'sesgo_punitivista', 'sesgo_pro_consumidor']
            ),
            Pregunta(
                id='G07',
                categoria='Sesgos y Tendencias',
                pregunta='¿Favorece sistemáticamente a algún tipo de parte?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_trabajador', 'sesgo_pro_empresa']
            ),
            Pregunta(
                id='G08',
                categoria='Sesgos y Tendencias',
                pregunta='¿Es neutral o tiene sesgos marcados?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_trabajador', 'sesgo_pro_empresa', 'sesgo_garantista']
            ),
            Pregunta(
                id='G09',
                categoria='Sesgos y Tendencias',
                pregunta='¿Cómo se comparan sus sesgos con el promedio de su fuero?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_trabajador', 'fuero']
            ),
            Pregunta(
                id='G10',
                categoria='Sesgos y Tendencias',
                pregunta='¿Tiene sesgo de confirmación en sus líneas jurisprudenciales?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales']
            ),
            Pregunta(
                id='G11',
                categoria='Sesgos y Tendencias',
                pregunta='¿Varía su criterio según la cuantía del reclamo?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['factores_predictivos']
            ),
            Pregunta(
                id='G12',
                categoria='Sesgos y Tendencias',
                pregunta='¿Tiene preferencia por algún tipo interpretativo?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['interpretacion_dominante']
            ),
            Pregunta(
                id='G13',
                categoria='Sesgos y Tendencias',
                pregunta='¿Es más favorable a actores individuales o colectivos?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_trabajador']
            ),
            Pregunta(
                id='G14',
                categoria='Sesgos y Tendencias',
                pregunta='¿Todos sus sesgos en una síntesis?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_trabajador', 'sesgo_pro_empresa', 'sesgo_garantista', 'sesgo_punitivista', 'sesgo_pro_consumidor']
            ),
            Pregunta(
                id='G15',
                categoria='Sesgos y Tendencias',
                pregunta='¿Son sus sesgos conscientes (doctrinarios) o inconscientes?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_trabajador', 'densidad_citas_doctrina']
            ),
        ]

        # =====================================================================
        # CATEGORÍA H: CASOS ESPECÍFICOS (15 preguntas)
        # =====================================================================
        preguntas['H'] = [
            Pregunta(
                id='H01',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un despido discriminatorio con prueba indiciaria?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales', 'factores_predictivos']
            ),
            Pregunta(
                id='H02',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un despido sin causa con alta antigüedad?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales', 'sesgo_pro_trabajador']
            ),
            Pregunta(
                id='H03',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un accidente laboral con responsabilidad compartida?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales', 'factores_predictivos']
            ),
            Pregunta(
                id='H04',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un reclamo de consumidor por producto defectuoso?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_consumidor', 'lineas_jurisprudenciales']
            ),
            Pregunta(
                id='H05',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería una colisión entre libertad de expresión y honor?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['proteccion_libertad_expresion', 'frecuencia_balancing_derechos']
            ),
            Pregunta(
                id='H06',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un planteo de inconstitucionalidad de ley laboral?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['tendencia_activismo', 'proteccion_trabajo']
            ),
            Pregunta(
                id='H07',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un caso de discriminación por género en el trabajo?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['proteccion_igualdad', 'usa_escrutinio_estricto']
            ),
            Pregunta(
                id='H08',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un caso de daños y perjuicios por mala praxis?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['lineas_jurisprudenciales', 'estandar_probatorio_dominante']
            ),
            Pregunta(
                id='H09',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un recurso de amparo por demora administrativa?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['tendencia_activismo', 'nivel_formalismo']
            ),
            Pregunta(
                id='H10',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un caso con prueba contradictoria?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['estandar_probatorio_dominante', 'frecuencia_sana_critica']
            ),
            Pregunta(
                id='H11',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un caso donde colisionan normas de diferente jerarquía?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['frecuencia_control_constitucionalidad', 'interpretacion_dominante']
            ),
            Pregunta(
                id='H12',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería una norma ambigua en derecho laboral?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['interpretacion_dominante', 'usa_in_dubio_pro_operario']
            ),
            Pregunta(
                id='H13',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un caso sin jurisprudencia clara aplicable?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['nivel_innovacion_jurisprudencial', 'densidad_citas_doctrina']
            ),
            Pregunta(
                id='H14',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un caso con precedente de CSJN contrario?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['redes_influencia_judicial', 'deferencia_institucional']
            ),
            Pregunta(
                id='H15',
                categoria='Casos Específicos',
                pregunta='¿Cómo resolvería un caso donde las partes tienen poder económico desigual?',
                tipo_respuesta='texto',
                requiere_bd=True,
                campos_necesarios=['sesgo_pro_trabajador', 'sesgo_pro_consumidor']
            ),
        ]

        return preguntas

    # =========================================================================
    # MÉTODOS DE CONSULTA
    # =========================================================================

    def obtener_todas_preguntas(self) -> List[Pregunta]:
        """Obtiene todas las preguntas del sistema"""
        todas = []
        for categoria in self.preguntas.values():
            todas.extend(categoria)
        return todas

    def obtener_preguntas_por_categoria(self, categoria: str) -> List[Pregunta]:
        """Obtiene preguntas de una categoría específica"""
        return self.preguntas.get(categoria, [])

    def obtener_pregunta_por_id(self, pregunta_id: str) -> Optional[Pregunta]:
        """Obtiene una pregunta por su ID"""
        for categoria in self.preguntas.values():
            for pregunta in categoria:
                if pregunta.id == pregunta_id:
                    return pregunta
        return None

    def buscar_preguntas(self, termino: str) -> List[Pregunta]:
        """Busca preguntas que contengan un término"""
        resultados = []
        termino_lower = termino.lower()

        for categoria in self.preguntas.values():
            for pregunta in categoria:
                if termino_lower in pregunta.pregunta.lower():
                    resultados.append(pregunta)

        return resultados

    def obtener_categorias(self) -> List[str]:
        """Obtiene lista de categorías disponibles"""
        categorias = {
            'A': 'Perfil e Identidad Judicial',
            'B': 'Metodología Interpretativa',
            'C': 'Protección de Derechos',
            'D': 'Líneas Jurisprudenciales',
            'E': 'Red de Influencias',
            'F': 'Análisis Predictivo',
            'G': 'Sesgos y Tendencias',
            'H': 'Casos Específicos'
        }
        return categorias

    def exportar_json(self, archivo: str = None):
        """Exporta todas las preguntas a JSON"""
        data = {
            'total_preguntas': len(self.obtener_todas_preguntas()),
            'categorias': self.obtener_categorias(),
            'preguntas': {
                cat: [p.to_dict() for p in pregs]
                for cat, pregs in self.preguntas.items()
            }
        }

        if archivo:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            return json.dumps(data, ensure_ascii=False, indent=2)

    def listar_preguntas(self, categoria: str = None):
        """Lista preguntas en formato legible"""
        if categoria:
            preguntas = self.obtener_preguntas_por_categoria(categoria)
            print(f"\n{'='*80}")
            print(f"CATEGORÍA {categoria}: {self.obtener_categorias()[categoria]}")
            print(f"{'='*80}\n")
        else:
            preguntas = self.obtener_todas_preguntas()
            print(f"\n{'='*80}")
            print(f"TODAS LAS PREGUNTAS ({len(preguntas)} total)")
            print(f"{'='*80}\n")

        for pregunta in preguntas:
            print(f"{pregunta.id}. {pregunta.pregunta}")
            print(f"    Tipo: {pregunta.tipo_respuesta}")
            if pregunta.campos_necesarios:
                print(f"    Campos BD: {', '.join(pregunta.campos_necesarios[:3])}...")
            print()


def main():
    """Función principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Sistema de preguntas judiciales'
    )
    parser.add_argument(
        '--listar',
        action='store_true',
        help='Listar todas las preguntas'
    )
    parser.add_argument(
        '--categoria',
        choices=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        help='Listar preguntas de una categoría'
    )
    parser.add_argument(
        '--exportar',
        help='Exportar preguntas a JSON'
    )
    parser.add_argument(
        '--buscar',
        help='Buscar preguntas por término'
    )

    args = parser.parse_args()

    sistema = SistemaPreguntasJudiciales()

    if args.listar or args.categoria:
        sistema.listar_preguntas(args.categoria)
    elif args.exportar:
        sistema.exportar_json(args.exportar)
        print(f"✓ Preguntas exportadas a: {args.exportar}")
    elif args.buscar:
        resultados = sistema.buscar_preguntas(args.buscar)
        print(f"\n{'='*80}")
        print(f"RESULTADOS DE BÚSQUEDA: '{args.buscar}' ({len(resultados)} encontradas)")
        print(f"{'='*80}\n")
        for p in resultados:
            print(f"{p.id}. {p.pregunta}\n")
    else:
        # Mostrar resumen
        print(f"\n{'='*80}")
        print("SISTEMA DE PREGUNTAS JUDICIALES v1.0")
        print(f"{'='*80}\n")
        print(f"Total de preguntas: {len(sistema.obtener_todas_preguntas())}")
        print(f"\nCategorías:")
        for cat, nombre in sistema.obtener_categorias().items():
            n = len(sistema.obtener_preguntas_por_categoria(cat))
            print(f"  {cat}. {nombre} ({n} preguntas)")
        print()


if __name__ == "__main__":
    main()
