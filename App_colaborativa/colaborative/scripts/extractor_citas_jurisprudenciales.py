#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 EXTRACTOR DE CITAS JURISPRUDENCIALES Y DOCTRINALES v1.0
==========================================================

Extrae citas a jurisprudencia y doctrina del texto de sentencias argentinas.

Detecta:
- Citas a CSJN (Fallos)
- Citas a Cámaras y Salas
- Citas a otros tribunales
- Citas a autores doctrinales
- Contexto textual de las citas

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import json

@dataclass
class CitaJurisprudencial:
    """Representa una cita jurisprudencial"""
    tipo: str  # 'csjn', 'camara', 'tribunal_superior', 'otro'
    tribunal: Optional[str]
    sala: Optional[str]
    autos: Optional[str]
    fallo_nro: Optional[str]
    extracto_textual: str
    posicion_inicio: int
    posicion_fin: int
    confianza: float  # 0-1

@dataclass
class CitaDoctri

nal:
    """Representa una cita doctrinal"""
    autor: str
    obra: Optional[str]
    extracto_textual: str
    posicion_inicio: int
    posicion_fin: int
    confianza: float


class ExtractorCitasJurisprudenciales:
    """
    Extrae citas jurisprudenciales y doctrinales de textos argentinos
    """

    def __init__(self):
        """Inicializa el extractor con patrones regex"""
        self._compilar_patrones()

    def _compilar_patrones(self):
        """Compila todos los patrones regex"""

        # ========================================
        # PATRONES PARA CSJN (Corte Suprema)
        # ========================================
        self.patrones_csjn = [
            # Fallos: 331:2499
            re.compile(
                r'Fallos:\s*(\d+):(\d+)',
                re.IGNORECASE
            ),
            # CSJN, Fallos: 331:2499
            re.compile(
                r'(?:CSJN|Corte Suprema).*?Fallos:\s*(\d+):(\d+)',
                re.IGNORECASE
            ),
            # Corte Suprema, autos "X c/ Y"
            re.compile(
                r'(?:CSJN|Corte Suprema).*?autos?\s*["\']([^"\']+)["\']',
                re.IGNORECASE
            ),
        ]

        # ========================================
        # PATRONES PARA CÁMARAS
        # ========================================
        self.patrones_camaras = [
            # Cámara Nacional del Trabajo, Sala X, autos "X c/ Y"
            re.compile(
                r'C[áa]mara\s+(?:Nacional\s+)?(?:de\s+)?([^,]+),\s*Sala\s+([IVX]+|[A-Z])',
                re.IGNORECASE
            ),
            # CNTrab, Sala X
            re.compile(
                r'(CN[A-Za-z]+),\s*Sala\s+([IVX]+|[A-Z])',
                re.IGNORECASE
            ),
            # Sala X, autos "..."
            re.compile(
                r'Sala\s+([IVX]+|[A-Z]).*?autos?\s*["\']([^"\']+)["\']',
                re.IGNORECASE
            ),
        ]

        # ========================================
        # PATRONES PARA AUTOS/CARÁTULAS
        # ========================================
        self.patron_autos = re.compile(
            r'autos?\s*["\']([^"\']+)["\']',
            re.IGNORECASE
        )

        # ========================================
        # PATRONES PARA AUTORES DOCTRINALES
        # ========================================
        self.patrones_autores = [
            # Como sostiene/enseña/opina AUTOR
            re.compile(
                r'(?:como|según|conforme)\s+(?:sostiene|enseña|opina|señala|expresa)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
                re.IGNORECASE
            ),
            # AUTOR sostiene/enseña/opina que
            re.compile(
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\s+(?:sostiene|enseña|opina|señala|expresa)\s+que',
                re.IGNORECASE
            ),
            # La doctrina de AUTOR
            re.compile(
                r'(?:la\s+)?doctrina\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
                re.IGNORECASE
            ),
            # Según AUTOR, "..."
            re.compile(
                r'seg[uú]n\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)[,:]',
                re.IGNORECASE
            ),
        ]

        # ========================================
        # PALABRAS A EXCLUIR (no son autores)
        # ========================================
        self.palabras_excluir_autor = {
            'actor', 'actora', 'demandado', 'demandada',
            'juez', 'jueza', 'magistrado', 'magistrada',
            'tribunal', 'corte', 'sala', 'cámara',
            'expte', 'expediente', 'autos', 'causa',
            'fiscal', 'defensor', 'perito', 'testigo'
        }

    def extraer_citas_csjn(self, texto: str) -> List[CitaJurisprudencial]:
        """
        Extrae citas a la Corte Suprema

        Returns:
            Lista de CitaJurisprudencial
        """
        citas = []

        for patron in self.patrones_csjn:
            for match in patron.finditer(texto):
                # Extraer contexto (±100 caracteres)
                inicio = max(0, match.start() - 100)
                fin = min(len(texto), match.end() + 100)
                extracto = texto[inicio:fin]

                # Extraer número de Fallos si está disponible
                if len(match.groups()) >= 2:
                    tomo = match.group(1)
                    pagina = match.group(2)
                    fallo_nro = f"Fallos: {tomo}:{pagina}"
                else:
                    fallo_nro = None

                # Buscar autos en el extracto
                autos_match = self.patron_autos.search(extracto)
                autos = autos_match.group(1) if autos_match else None

                cita = CitaJurisprudencial(
                    tipo='csjn',
                    tribunal='Corte Suprema de Justicia de la Nación',
                    sala=None,
                    autos=autos,
                    fallo_nro=fallo_nro,
                    extracto_textual=extracto.strip(),
                    posicion_inicio=match.start(),
                    posicion_fin=match.end(),
                    confianza=0.9
                )

                citas.append(cita)

        return citas

    def extraer_citas_camaras(self, texto: str) -> List[CitaJurisprudencial]:
        """
        Extrae citas a Cámaras y Salas

        Returns:
            Lista de CitaJurisprudencial
        """
        citas = []

        for patron in self.patrones_camaras:
            for match in patron.finditer(texto):
                # Extraer contexto
                inicio = max(0, match.start() - 100)
                fin = min(len(texto), match.end() + 100)
                extracto = texto[inicio:fin]

                # Extraer tribunal y sala
                grupos = match.groups()
                if len(grupos) >= 2:
                    tribunal = grupos[0]
                    sala = grupos[1]
                elif len(grupos) == 1:
                    # Solo sala mencionada
                    tribunal = "Cámara (no especificada)"
                    sala = grupos[0]
                else:
                    continue

                # Buscar autos
                autos_match = self.patron_autos.search(extracto)
                autos = autos_match.group(1) if autos_match else None

                cita = CitaJurisprudencial(
                    tipo='camara',
                    tribunal=tribunal.strip(),
                    sala=sala.strip(),
                    autos=autos,
                    fallo_nro=None,
                    extracto_textual=extracto.strip(),
                    posicion_inicio=match.start(),
                    posicion_fin=match.end(),
                    confianza=0.8
                )

                citas.append(cita)

        return citas

    def extraer_autores_doctrinales(self, texto: str) -> List[CitaDoctrial]:
        """
        Extrae citas a autores doctrinales

        Returns:
            Lista de CitaDoctrial
        """
        citas = []

        for patron in self.patrones_autores:
            for match in patron.finditer(texto):
                autor = match.group(1).strip()

                # Filtrar palabras que no son autores
                if autor.lower() in self.palabras_excluir_autor:
                    continue

                # Filtrar nombres muy cortos
                if len(autor) < 4:
                    continue

                # Extraer contexto
                inicio = max(0, match.start() - 50)
                fin = min(len(texto), match.end() + 150)
                extracto = texto[inicio:fin]

                cita = CitaDoctrial(
                    autor=autor,
                    obra=None,  # Podría mejorarse extrayendo títulos de obras
                    extracto_textual=extracto.strip(),
                    posicion_inicio=match.start(),
                    posicion_fin=match.end(),
                    confianza=0.7
                )

                citas.append(cita)

        return citas

    def extraer_todas_citas(self, texto: str) -> Dict[str, List]:
        """
        Extrae todas las citas de un texto

        Returns:
            Diccionario con citas jurisprudenciales y doctrinales
        """
        return {
            'citas_csjn': self.extraer_citas_csjn(texto),
            'citas_camaras': self.extraer_citas_camaras(texto),
            'citas_doctrinales': self.extraer_autores_doctrinales(texto)
        }

    def consolidar_citas(self, citas: Dict[str, List]) -> Dict:
        """
        Consolida y resume las citas extraídas

        Returns:
            Diccionario con resumen
        """
        # Contar citas por tipo
        total_csjn = len(citas['citas_csjn'])
        total_camaras = len(citas['citas_camaras'])
        total_doctrinales = len(citas['citas_doctrinales'])

        # Tribunales únicos
        tribunales_csjn = set()
        tribunales_camaras = set()

        for cita in citas['citas_csjn']:
            if cita.tribunal:
                tribunales_csjn.add(cita.tribunal)

        for cita in citas['citas_camaras']:
            if cita.tribunal:
                tribunales_camaras.add(cita.tribunal)
            if cita.sala:
                tribunales_camaras.add(f"{cita.tribunal} - Sala {cita.sala}")

        # Autores únicos
        autores = set()
        for cita in citas['citas_doctrinales']:
            autores.add(cita.autor)

        return {
            'total_citas_jurisprudenciales': total_csjn + total_camaras,
            'total_citas_csjn': total_csjn,
            'total_citas_camaras': total_camaras,
            'total_citas_doctrinales': total_doctrinales,
            'tribunales_csjn': list(tribunales_csjn),
            'tribunales_camaras': list(tribunales_camaras),
            'autores_citados': list(autores),
            'densidad_citas': (total_csjn + total_camaras + total_doctrinales)
        }

    def exportar_json(self, citas: Dict[str, List]) -> str:
        """Exporta las citas a JSON"""
        # Convertir dataclasses a diccionarios
        exportable = {
            'citas_csjn': [asdict(c) for c in citas['citas_csjn']],
            'citas_camaras': [asdict(c) for c in citas['citas_camaras']],
            'citas_doctrinales': [asdict(c) for c in citas['citas_doctrinales']]
        }

        return json.dumps(exportable, ensure_ascii=False, indent=2)

    def imprimir_resumen(self, citas: Dict[str, List]):
        """Imprime un resumen de las citas encontradas"""
        resumen = self.consolidar_citas(citas)

        print("\n" + "="*70)
        print("RESUMEN DE CITAS EXTRAÍDAS")
        print("="*70)

        print(f"\n📚 CITAS JURISPRUDENCIALES: {resumen['total_citas_jurisprudenciales']}")
        print(f"  • CSJN: {resumen['total_citas_csjn']}")
        print(f"  • Cámaras: {resumen['total_citas_camaras']}")

        if resumen['tribunales_camaras']:
            print("\n  Tribunales citados:")
            for trib in resumen['tribunales_camaras'][:5]:
                print(f"    - {trib}")

        print(f"\n👤 CITAS DOCTRINALES: {resumen['total_citas_doctrinales']}")

        if resumen['autores_citados']:
            print("\n  Autores citados:")
            for autor in resumen['autores_citados'][:10]:
                print(f"    - {autor}")

        print(f"\n📊 Densidad de citas: {resumen['densidad_citas']}")
        print("="*70 + "\n")


def test_extractor():
    """Función de testing"""
    texto_ejemplo = """
    En los autos "Pérez, Juan c/ Empresa XYZ S.A. s/ despido", esta Sala ha sostenido
    en reiteradas oportunidades que el principio protectorio del derecho del trabajo
    impone una interpretación favorable al trabajador.

    Como bien lo ha establecido la Corte Suprema de Justicia de la Nación en Fallos: 331:2499,
    "Vizzoti, Carlos c/ AMSA S.A.", el principio de irrenunciabilidad constituye una
    limitación a la autonomía de la voluntad.

    En igual sentido, la Cámara Nacional del Trabajo, Sala VII, en autos "González, María
    c/ La Estrella S.A.", del 15/03/2020, ha expresado que corresponde aplicar el in dubio
    pro operario cuando existan dudas sobre el alcance de las normas.

    Como sostiene Grisolía en su obra "Derecho del Trabajo y de la Seguridad Social",
    el trabajador es la parte débil en la relación laboral. En similar sentido, Ackerman
    señala que la protección del trabajador es un principio rector del ordenamiento laboral.

    También la doctrina de Bidart Campos nos enseña que los derechos sociales tienen
    jerarquía constitucional.
    """

    extractor = ExtractorCitasJurisprudenciales()
    citas = extractor.extraer_todas_citas(texto_ejemplo)

    print("\n🔍 CITAS A CSJN:")
    for i, cita in enumerate(citas['citas_csjn'], 1):
        print(f"\n  {i}. {cita.fallo_nro or 'Sin número'}")
        if cita.autos:
            print(f"     Autos: {cita.autos}")
        print(f"     Extracto: ...{cita.extracto_textual[:100]}...")

    print("\n🔍 CITAS A CÁMARAS:")
    for i, cita in enumerate(citas['citas_camaras'], 1):
        print(f"\n  {i}. {cita.tribunal}, Sala {cita.sala}")
        if cita.autos:
            print(f"     Autos: {cita.autos}")

    print("\n🔍 CITAS DOCTRINALES:")
    for i, cita in enumerate(citas['citas_doctrinales'], 1):
        print(f"\n  {i}. Autor: {cita.autor}")
        print(f"     Contexto: ...{cita.extracto_textual[:100]}...")

    # Resumen
    extractor.imprimir_resumen(citas)


if __name__ == "__main__":
    test_extractor()
