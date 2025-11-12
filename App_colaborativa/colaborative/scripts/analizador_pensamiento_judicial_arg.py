#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ ANALIZADOR DE PENSAMIENTO JUDICIAL ARGENTINO v1.0
====================================================

Análisis específico del razonamiento judicial argentino:
- Activismo vs restricción judicial
- Interpretación constitucional y normativa
- Protección de derechos específicos
- Tests y doctrinas del derecho argentino
- Estándares probatorios
- Sesgos característicos del sistema argentino
- Deferencia institucional

INTEGRA CON: analyser_metodo_mejorado.py (análisis cognitivo general)

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

# ========================================
# PATRONES PARA ACTIVISMO JUDICIAL
# ========================================
ACTIVISMO_PATTERNS = {
    "control_constitucionalidad": r"\b(inconstitucionalidad|control de constitucionalidad|declarar inconstitucional|inv[aá]lid[ao])\b",
    "interpretacion_expansiva": r"\b(interpretación extensiva|espíritu de la ley|finalidad de la norma|ratio legis)\b",
    "creacion_precedente": r"\b(sentamos precedente|establecemos criterio|innovamos)\b",
    "supervicion_politicas": r"\b(políticas? públicas?|estado de cosas inconstitucional|supervisión judicial)\b",
    "tutela_activa": r"\b(tutela judicial efectiva|protección reforzada|activismo judicial)\b"
}

RESTRICCION_PATTERNS = {
    "deferencia_legislador": r"\b(potestad del legislador|voluntad del legislador|discrecionalidad legislativa)\b",
    "interpretacion_literal": r"\b(interpretación literal|tenor literal|clara letra de la ley)\b",
    "autorestriction": r"\b(cuestiones no justiciables|separación de poderes|prudencia judicial)\b",
    "precedente_estricto": r"\b(stare decisis|vinculación al precedente|seguimos jurisprudencia)\b"
}

# ========================================
# PATRONES INTERPRETACIÓN NORMATIVA
# ========================================
INTERPRETACION_PATTERNS = {
    "literal": r"\b(texto expreso|letra de la ley|sentido literal|interpretación gramatical)\b",
    "sistematica": r"\b(interpretación sistemática|conjunto normativo|armonización normativa)\b",
    "teleologica": r"\b(finalidad|propósito|objeto de la norma|telos|ratio legis)\b",
    "historica": r"\b(voluntad del constituyente|antecedentes parlamentarios|evolución histórica)\b",
    "evolutiva": r"\b(interpretación dinámica|constitución viviente|evolución social|contexto actual)\b",
    "conforme": r"\b(interpretación conforme|conformidad constitucional)\b"
}

# ========================================
# TESTS JUDICIALES ARGENTINOS
# ========================================
TESTS_DOCTRINAS_PATTERNS = {
    "test_proporcionalidad": r"\b(test de proporcionalidad|proporcionalidad|idoneidad|necesidad y proporcionalidad en sentido estricto)\b",
    "test_razonabilidad": r"\b(test de razonabilidad|razonabilidad|art\.?\s*28|arbitrariedad)\b",
    "escrutinio_estricto": r"\b(escrutinio estricto|strict scrutiny|examen riguroso)\b",
    "escrutinio_intermedio": r"\b(escrutinio intermedio|examen intermedio)\b",
    "control_convencionalidad": r"\b(control de convencionalidad|tratados internacionales|jerarquía constitucional)\b",
    "doctrina_arbitrariedad": r"\b(arbitrariedad|capricho|irrazonabilidad manifiesta)\b",
    "gravedad_institucional": r"\b(gravedad institucional|excepcional gravedad)\b",
    "caso_federal": r"\b(caso federal|cuestión federal|sentencia arbitraria)\b"
}

# ========================================
# PRINCIPIOS IN DUBIO PRO
# ========================================
IN_DUBIO_PRO_PATTERNS = {
    "pro_operario": r"\b(in dubio pro operario|principio protectorio|favor del trabajador)\b",
    "pro_reo": r"\b(in dubio pro reo|favor del imputado|favor libertatis)\b",
    "pro_consumidor": r"\b(in dubio pro consumidor|favor del consumidor|hipervulnerabilidad)\b",
    "pro_homine": r"\b(pro homine|pro persona|favor de la persona)\b",
    "pro_actione": r"\b(pro actione|favor del acceso a la justicia)\b",
    "pro_natura": r"\b(in dubio pro natura|favor del ambiente)\b"
}

# ========================================
# PROTECCIÓN DE DERECHOS
# ========================================
DERECHOS_PATTERNS = {
    "libertad_expresion": r"\b(libertad de expresión|libertad de prensa|censura previa)\b",
    "igualdad": r"\b(igualdad|no discriminación|trato igualitario|diferenciación arbitraria)\b",
    "debido_proceso": r"\b(debido proceso|derecho de defensa|tutela judicial efectiva)\b",
    "intimidad": r"\b(intimidad|privacidad|datos personales|habeas data)\b",
    "propiedad": r"\b(derecho de propiedad|expropiación|confiscación)\b",
    "trabajo": r"\b(derecho al trabajo|estabilidad laboral|salario mínimo)\b",
    "salud": r"\b(derecho a la salud|prestaciones médicas|cobertura)\b",
    "ambiente": r"\b(derecho al ambiente|desarrollo sustentable|daño ambiental)\b",
    "vivienda": r"\b(derecho a la vivienda|vivienda digna)\b",
    "educacion": r"\b(derecho a la educación|acceso educativo)\b",
    "ninez": r"\b(interés superior del niño|derechos del niño)\b"
}

# ========================================
# ESTÁNDARES PROBATORIOS
# ========================================
ESTANDARES_PRUEBA = {
    "sana_critica": r"\b(sana crítica|reglas de la sana crítica)\b",
    "prueba_tasada": r"\b(prueba legal|prueba tasada|valor predeterminado)\b",
    "libre_conviccion": r"\b(libre convicción|íntima convicción)\b",
    "certeza_positiva": r"\b(certeza positiva|prueba indubitada)\b",
    "mas_alla_duda": r"\b(más allá de toda duda razonable|duda razonable)\b",
    "verosimilitud": r"\b(verosimilitud|prima facie|presunción)\b"
}

# ========================================
# FUENTES DEL DERECHO
# ========================================
FUENTES_PATTERNS = {
    "csjn": r"\b(Fallos:|CSJN|Corte Suprema de Justicia de la Nación)\b",
    "camaras": r"\b(Cámara|Sala|C[ÁA]mara Nacional)\b",
    "codigo_civil": r"\b(CCyC|Código Civil|Código Civil y Comercial|art\.?\s*\d+\s*CCyC)\b",
    "constitucion": r"\b(Constitución Nacional|art\.?\s*\d+\s*CN|art\.?\s*\d+\s*Const\.)\b",
    "ley_contrato_trabajo": r"\b(LCT|Ley de Contrato de Trabajo|ley 20\.744)\b",
    "ley_defensa_consumidor": r"\b(Ley de Defensa del Consumidor|ley 24\.240)\b",
    "tratados_ddhh": r"\b(CADH|Convención Americana|Pacto de San José|PIDCP|jerarquía constitucional)\b",
    "doctrina": r"\b(doctrina|autor|tratadista|sostiene|opina)\b"
}

# ========================================
# SESGOS ARGENTINOS ESPECÍFICOS
# ========================================
SESGOS_ARGENTINOS = {
    "pro_trabajador": [
        r"\b(trabajador|asalariado|dependiente|relación desigual)\b",
        r"\b(principio protectorio|in dubio pro operario)\b",
        r"\b(vulnerabilidad del trabajador)\b"
    ],
    "pro_consumidor": [
        r"\b(consumidor|usuario|vulnerabilidad del consumidor|hipervulnerabilidad)\b",
        r"\b(trato digno|relación de consumo)\b"
    ],
    "pro_estado": [
        r"\b(prerrogativas del Estado|potestades públicas|interés público)\b",
        r"\b(presunción de legitimidad)\b"
    ],
    "garantista": [
        r"\b(garantías constitucionales|tutela judicial efectiva|debido proceso)\b",
        r"\b(in dubio pro reo|favor libertatis)\b",
        r"\b(interpretación restrictiva de normas penales)\b"
    ],
    "punitivista": [
        r"\b(sanción ejemplar|reproche|punición)\b",
        r"\b(tolerancia cero|mano dura)\b"
    ]
}

@dataclass
class AnalisisJudicial:
    """Resultado del análisis judicial"""
    # Activismo
    tendencia_activismo: float  # -1 a 1
    indicadores_activismo: Dict[str, float]
    indicadores_restriccion: Dict[str, float]

    # Interpretación
    interpretacion_normativa: str  # literal, sistematica, teleologica, etc.
    interpretacion_scores: Dict[str, float]

    # Formalismo
    formalismo_vs_sustancialismo: float  # -1 a 1

    # Protección de derechos
    derechos_protegidos: Dict[str, float]
    proteccion_general: float

    # Tests y doctrinas
    tests_aplicados: Dict[str, float]
    in_dubio_pro_aplicado: Dict[str, float]

    # Estándares probatorios
    estandar_prueba: str
    estandares_scores: Dict[str, float]

    # Fuentes
    fuentes_citadas: Dict[str, float]
    peso_fuentes: Dict[str, str]  # 'alto', 'medio', 'bajo'

    # Sesgos
    sesgos_detectados: Dict[str, float]
    sesgo_dominante: str

    # Deferencia
    deferencia_legislativo: float
    deferencia_ejecutivo: float

class AnalizadorPensamientoJudicialArg:
    """
    Analizador de pensamiento judicial específico para Argentina
    """

    def __init__(self):
        self.version = "v1.0"

    def analizar(self, texto: str) -> AnalisisJudicial:
        """
        Análisis completo de una sentencia

        Args:
            texto: Texto completo de la sentencia

        Returns:
            AnalisisJudicial con todos los scores
        """
        return AnalisisJudicial(
            tendencia_activismo=self._calcular_activismo(texto),
            indicadores_activismo=self._score_patterns(texto, ACTIVISMO_PATTERNS),
            indicadores_restriccion=self._score_patterns(texto, RESTRICCION_PATTERNS),
            interpretacion_normativa=self._determinar_interpretacion(texto),
            interpretacion_scores=self._score_patterns(texto, INTERPRETACION_PATTERNS),
            formalismo_vs_sustancialismo=self._calcular_formalismo(texto),
            derechos_protegidos=self._score_patterns(texto, DERECHOS_PATTERNS),
            proteccion_general=self._calcular_proteccion_general(texto),
            tests_aplicados=self._score_patterns(texto, TESTS_DOCTRINAS_PATTERNS),
            in_dubio_pro_aplicado=self._score_patterns(texto, IN_DUBIO_PRO_PATTERNS),
            estandar_prueba=self._determinar_estandar_prueba(texto),
            estandares_scores=self._score_patterns(texto, ESTANDARES_PRUEBA),
            fuentes_citadas=self._score_patterns(texto, FUENTES_PATTERNS),
            peso_fuentes=self._clasificar_peso_fuentes(texto),
            sesgos_detectados=self._detectar_sesgos(texto),
            sesgo_dominante=self._determinar_sesgo_dominante(texto),
            deferencia_legislativo=self._calcular_deferencia_legislativo(texto),
            deferencia_ejecutivo=self._calcular_deferencia_ejecutivo(texto)
        )

    def _score_pattern(self, texto: str, pattern: str) -> float:
        """Score individual de un patrón"""
        matches = len(re.findall(pattern, texto, re.IGNORECASE | re.MULTILINE))
        # Normalizar por cada 1000 palabras
        palabras = len(texto.split())
        if palabras == 0:
            return 0.0
        normalized = (matches / (palabras / 1000.0))
        return min(1.0, normalized / 5.0)  # Cap en 1.0, ~5 menciones por 1000 palabras = score alto

    def _score_patterns(self, texto: str, patterns_dict: Dict[str, str]) -> Dict[str, float]:
        """Score múltiples patrones"""
        return {k: self._score_pattern(texto, p) for k, p in patterns_dict.items()}

    def _score_pattern_list(self, texto: str, patterns_list: List[str]) -> float:
        """Score de una lista de patrones (suma)"""
        total = sum(self._score_pattern(texto, p) for p in patterns_list)
        return min(1.0, total)

    def _calcular_activismo(self, texto: str) -> float:
        """
        Calcula tendencia activismo vs restricción

        Returns:
            -1 (restricción extrema) a +1 (activismo extremo)
        """
        score_activismo = sum(self._score_patterns(texto, ACTIVISMO_PATTERNS).values())
        score_restriccion = sum(self._score_patterns(texto, RESTRICCION_PATTERNS).values())

        if score_activismo == 0 and score_restriccion == 0:
            return 0.0

        # Normalizar a rango -1, 1
        total = score_activismo + score_restriccion
        if total == 0:
            return 0.0

        balance = (score_activismo - score_restriccion) / total
        return balance

    def _determinar_interpretacion(self, texto: str) -> str:
        """Determina el tipo de interpretación dominante"""
        scores = self._score_patterns(texto, INTERPRETACION_PATTERNS)
        if not scores:
            return "mixta"

        max_tipo = max(scores.items(), key=lambda x: x[1])

        if max_tipo[1] < 0.1:  # Umbral mínimo
            return "mixta"

        return max_tipo[0]

    def _calcular_formalismo(self, texto: str) -> float:
        """
        Calcula formalismo vs sustancialismo

        Returns:
            -1 (formalista) a +1 (sustancialista)
        """
        # Indicadores de formalismo
        formal_patterns = [
            r"\b(forma|requisito formal|procedimiento|rito)\b",
            r"\b(letra de la ley|texto expreso|norma clara)\b",
            r"\b(formalidad|cumplimiento estricto)\b"
        ]

        # Indicadores de sustancialismo
        sustancial_patterns = [
            r"\b(sustancia|fondo|espíritu de la norma|finalidad)\b",
            r"\b(realidad|situación concreta|contexto)\b",
            r"\b(justicia material|equidad)\b"
        ]

        score_formal = sum(self._score_pattern(texto, p) for p in formal_patterns)
        score_sustancial = sum(self._score_pattern(texto, p) for p in sustancial_patterns)

        total = score_formal + score_sustancial
        if total == 0:
            return 0.0

        balance = (score_sustancial - score_formal) / total
        return balance

    def _calcular_proteccion_general(self, texto: str) -> float:
        """Calcula score general de protección de derechos"""
        scores = self._score_patterns(texto, DERECHOS_PATTERNS)
        if not scores:
            return 0.0
        return min(1.0, sum(scores.values()) / len(scores))

    def _determinar_estandar_prueba(self, texto: str) -> str:
        """Determina el estándar probatorio aplicado"""
        scores = self._score_patterns(texto, ESTANDARES_PRUEBA)
        if not scores:
            return "sana_critica"  # Por defecto en Argentina

        max_std = max(scores.items(), key=lambda x: x[1])

        if max_std[1] < 0.1:
            return "sana_critica"

        return max_std[0]

    def _clasificar_peso_fuentes(self, texto: str) -> Dict[str, str]:
        """Clasifica el peso relativo de cada fuente"""
        scores = self._score_patterns(texto, FUENTES_PATTERNS)

        clasificacion = {}
        for fuente, score in scores.items():
            if score >= 0.5:
                clasificacion[fuente] = "alto"
            elif score >= 0.2:
                clasificacion[fuente] = "medio"
            elif score > 0:
                clasificacion[fuente] = "bajo"

        return clasificacion

    def _detectar_sesgos(self, texto: str) -> Dict[str, float]:
        """Detecta sesgos específicos argentinos"""
        sesgos = {}
        for sesgo, patterns_list in SESGOS_ARGENTINOS.items():
            sesgos[sesgo] = self._score_pattern_list(texto, patterns_list)
        return sesgos

    def _determinar_sesgo_dominante(self, texto: str) -> str:
        """Determina el sesgo dominante (si hay)"""
        sesgos = self._detectar_sesgos(texto)
        if not sesgos:
            return "neutral"

        max_sesgo = max(sesgos.items(), key=lambda x: x[1])

        if max_sesgo[1] < 0.3:  # Umbral para considerar sesgo significativo
            return "neutral"

        return max_sesgo[0]

    def _calcular_deferencia_legislativo(self, texto: str) -> float:
        """Calcula nivel de deferencia al poder legislativo"""
        deferencia_patterns = [
            r"\b(potestad del legislador|voluntad del legislador|decisión política)\b",
            r"\b(margen de apreciación del legislador)\b",
            r"\b(no corresponde al juez|excede la función judicial)\b"
        ]

        return self._score_pattern_list(texto, deferencia_patterns)

    def _calcular_deferencia_ejecutivo(self, texto: str) -> float:
        """Calcula nivel de deferencia al poder ejecutivo"""
        deferencia_patterns = [
            r"\b(zona de reserva de la administración|discrecionalidad administrativa)\b",
            r"\b(prerrogativas del poder ejecutivo)\b",
            r"\b(mérito u oportunidad|no revisable judicialmente)\b"
        ]

        return self._score_pattern_list(texto, deferencia_patterns)

    def exportar_json(self, analisis: AnalisisJudicial) -> str:
        """Exporta el análisis a JSON"""
        return json.dumps(asdict(analisis), ensure_ascii=False, indent=2)

    def imprimir_resumen(self, analisis: AnalisisJudicial):
        """Imprime un resumen legible del análisis"""
        print("\n" + "="*70)
        print("ANÁLISIS DE PENSAMIENTO JUDICIAL")
        print("="*70)

        print(f"\n📊 ACTIVISMO JUDICIAL")
        if analisis.tendencia_activismo > 0.3:
            print(f"  Tendencia: ACTIVISTA ({analisis.tendencia_activismo:+.2f})")
        elif analisis.tendencia_activismo < -0.3:
            print(f"  Tendencia: RESTRICTIVA ({analisis.tendencia_activismo:+.2f})")
        else:
            print(f"  Tendencia: MODERADA ({analisis.tendencia_activismo:+.2f})")

        print(f"\n📖 INTERPRETACIÓN NORMATIVA")
        print(f"  Tipo dominante: {analisis.interpretacion_normativa.upper()}")

        print(f"\n⚖️  FORMALISMO")
        if analisis.formalismo_vs_sustancialismo > 0.3:
            print(f"  Tendencia: SUSTANCIALISTA ({analisis.formalismo_vs_sustancialismo:+.2f})")
        elif analisis.formalismo_vs_sustancialismo < -0.3:
            print(f"  Tendencia: FORMALISTA ({analisis.formalismo_vs_sustancialismo:+.2f})")
        else:
            print(f"  Tendencia: EQUILIBRADA ({analisis.formalismo_vs_sustancialismo:+.2f})")

        print(f"\n🛡️  PROTECCIÓN DE DERECHOS")
        print(f"  Score general: {analisis.proteccion_general:.2f}")
        top_derechos = sorted(analisis.derechos_protegidos.items(),
                             key=lambda x: x[1], reverse=True)[:3]
        if top_derechos:
            print("  Derechos más protegidos:")
            for derecho, score in top_derechos:
                if score > 0:
                    print(f"    - {derecho}: {score:.2f}")

        print(f"\n🔬 TESTS Y DOCTRINAS")
        tests_aplicados = [k for k, v in analisis.tests_aplicados.items() if v > 0.2]
        if tests_aplicados:
            print(f"  Aplicados: {', '.join(tests_aplicados)}")
        else:
            print("  No se detectaron tests específicos")

        print(f"\n📚 FUENTES DEL DERECHO")
        for fuente, peso in analisis.peso_fuentes.items():
            print(f"  {fuente}: {peso}")

        print(f"\n⚠️  SESGOS DETECTADOS")
        print(f"  Sesgo dominante: {analisis.sesgo_dominante.upper()}")
        sesgos_significativos = {k: v for k, v in analisis.sesgos_detectados.items() if v > 0.3}
        if sesgos_significativos:
            for sesgo, score in sesgos_significativos.items():
                print(f"    - {sesgo}: {score:.2f}")

        print(f"\n🏛️  DEFERENCIA INSTITUCIONAL")
        print(f"  Legislativo: {analisis.deferencia_legislativo:.2f}")
        print(f"  Ejecutivo: {analisis.deferencia_ejecutivo:.2f}")

        print("="*70 + "\n")


def test_analizador():
    """Función de testing"""
    texto_ejemplo = """
    En autos "García, Juan c/ Empresa XYZ S.A. s/ despido", corresponde analizar
    si el despido del actor resulta discriminatorio según lo establece la doctrina
    de la Corte Suprema de Justicia de la Nación en Fallos 331:2499.

    Conforme el principio protectorio y el in dubio pro operario consagrado en el
    art. 9 de la LCT, corresponde interpretar las normas en favor del trabajador.

    Aplicando el test de razonabilidad del art. 28 de la Constitución Nacional,
    considero que la conducta del empleador resulta desproporcionada y vulnera
    el derecho al trabajo protegido constitucionalmente.

    Por estas razones, y en aplicación de los principios de justicia social,
    corresponde HACER LUGAR a la demanda.
    """

    analizador = AnalizadorPensamientoJudicialArg()
    analisis = analizador.analizar(texto_ejemplo)
    analizador.imprimir_resumen(analisis)

    # Exportar JSON
    json_output = analizador.exportar_json(analisis)
    print("\nJSON Output (primeros 500 caracteres):")
    print(json_output[:500])


if __name__ == "__main__":
    test_analizador()
