#!/usr/bin/env python3
"""
Sistema de Análisis de Pensamiento Judicial - Argentina
Extractor de Metadata de Sentencias Argentinas

Versión: 1.0
Fecha: 2025-11-12

Este script extrae automáticamente metadata de sentencias argentinas
usando patrones regex específicos del formato judicial argentino.
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json

class ExtractorMetadataArgentina:
    """
    Extractor de metadata para sentencias judiciales argentinas
    """

    def __init__(self):
        """Inicializa el extractor con patrones regex"""
        self._compilar_patrones()

    def _compilar_patrones(self):
        """Compila todos los patrones regex para optimizar performance"""

        # Patrones para expediente
        self.patrones_expediente = [
            re.compile(r'Expediente\s*(?:N°|Nro|Nº|Número)?\s*[:\.]?\s*([A-Z0-9\-\/]+)', re.IGNORECASE),
            re.compile(r'Expte\.?\s*(?:N°|Nro|Nº)?\s*[:\.]?\s*([A-Z0-9\-\/]+)', re.IGNORECASE),
            re.compile(r'Causa\s*(?:N°|Nro|Nº)?\s*[:\.]?\s*([A-Z0-9\-\/]+)', re.IGNORECASE),
            re.compile(r'EXP[:\s\-]*([A-Z0-9\-\/]+)', re.IGNORECASE),
        ]

        # Patrones para carátula
        self.patrones_caratula = [
            re.compile(r'(?:Autos|Causa)\s*[:\.]?\s*["\']([^"\']+)["\']', re.IGNORECASE),
            re.compile(r'(?:en\s+autos\s*[:\.]?\s*)([A-ZÁÉÍÓÚÑ][^\.]+?)\s+s\/\s+', re.IGNORECASE),
            re.compile(r'Caratulados\s*[:\.]?\s*["\']?([^"\'\.]+)["\']?', re.IGNORECASE),
        ]

        # Patrones para fecha de sentencia
        self.patrones_fecha = [
            re.compile(r'Buenos\s+Aires,\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', re.IGNORECASE),
            re.compile(r'(?:fecha|dictada)\s*[:\.]?\s*(\d{1,2})/(\d{1,2})/(\d{4})', re.IGNORECASE),
            re.compile(r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', re.IGNORECASE),
        ]

        # Patrones para juez/jueces
        self.patrones_juez = [
            re.compile(r'Juez(?:a)?(?:\s+de\s+(?:primera\s+)?instancia)?\s*[:\.]?\s*(?:Dr\.|Dra\.)?\s*([A-ZÁÉÍÓÚÑ][^,\.\n]+)', re.IGNORECASE),
            re.compile(r'Vocal(?:es)?\s*[:\.]?\s*(?:Dr\.|Dra\.)?\s*([A-ZÁÉÍÓÚÑ][^,\.\n]+)', re.IGNORECASE),
            re.compile(r'Magistrad(?:o|a)(?:s)?\s*[:\.]?\s*(?:Dr\.|Dra\.)?\s*([A-ZÁÉÍÓÚÑ][^,\.\n]+)', re.IGNORECASE),
            re.compile(r'(?:Dr\.|Dra\.)\s+([A-ZÁÉÍÓÚÑ][^\n\.,]{10,50})\s*\(Juez', re.IGNORECASE),
        ]

        # Patrones para sala (tribunal colegiado)
        self.patrones_sala = [
            re.compile(r'Sala\s+([IVX]+|[A-Z])\s*(?:de\s+)?(?:la\s+)?Cámara', re.IGNORECASE),
            re.compile(r'Cámara\s+(?:Nacional\s+)?(?:de\s+Apelaciones\s+)?(?:en\s+lo\s+)?([A-Za-z\s]+)\s*(?:-|\,)?\s*Sala\s+([IVX]+|[A-Z])', re.IGNORECASE),
        ]

        # Patrones para fuero
        self.patrones_fuero = [
            re.compile(r'Juzgado\s+(?:Nacional\s+)?(?:de\s+)?(?:Primera\s+Instancia\s+)?(?:en\s+lo\s+)?([A-Za-z\s]+)', re.IGNORECASE),
            re.compile(r'Cámara\s+(?:Nacional\s+)?(?:de\s+Apelaciones\s+)?en\s+lo\s+([A-Za-z\s]+)', re.IGNORECASE),
            re.compile(r'Fuero\s*[:\.]?\s*([A-Za-z\s]+)', re.IGNORECASE),
        ]

        # Patrones para tipo de sentencia
        self.patrones_tipo_sentencia = [
            re.compile(r'Sentencia\s+(definitiva|interlocutoria|homologatoria)', re.IGNORECASE),
            re.compile(r'(Sentencia|Resolución|Auto)\s+(?:N°|Nro)', re.IGNORECASE),
        ]

        # Patrones para partes
        self.patrones_actor = [
            re.compile(r'Actor(?:es)?\s*[:\.]?\s*([A-ZÁÉÍÓÚÑ][^c\/\n]{5,80}?)(?:\s+c\/|\s+contra)', re.IGNORECASE),
            re.compile(r'([A-ZÁÉÍÓÚÑ][^c\/\n]{5,80}?)\s+c\/\s+', re.IGNORECASE),
        ]

        self.patrones_demandado = [
            re.compile(r'Demandad(?:o|a)(?:s)?\s*[:\.]?\s*([A-ZÁÉÍÓÚÑ][^\n\.]{5,80})', re.IGNORECASE),
            re.compile(r'c\/\s+([A-ZÁÉÍÓÚÑ][^\n\.]{5,80}?)\s+s\/', re.IGNORECASE),
            re.compile(r'contra\s+([A-ZÁÉÍÓÚÑ][^\n\.]{5,80})', re.IGNORECASE),
        ]

        # Patrones para materia
        self.patrones_materia = [
            re.compile(r's\/\s+([^\.]+)', re.IGNORECASE),
            re.compile(r'(?:sobre|por)\s+([^\.]{10,80})', re.IGNORECASE),
        ]

        # Patrones para resultado
        self.patrones_resultado = [
            re.compile(r'(?:SE\s+)?(?:RESUELVE|FALLA)[:\s]*(.*?)(?:HACER LUGAR|RECHAZAR|NO HACER LUGAR)', re.IGNORECASE | re.DOTALL),
            re.compile(r'(HACER LUGAR|NO HACER LUGAR|RECHAZAR)', re.IGNORECASE),
        ]

        # Meses en español
        self.meses_esp = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
            'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
            'septiembre': 9, 'setiembre': 9, 'octubre': 10,
            'noviembre': 11, 'diciembre': 12
        }

    def extraer_metadata(self, texto: str, archivo_nombre: str = None) -> Dict:
        """
        Extrae toda la metadata de una sentencia

        Args:
            texto: Texto completo de la sentencia
            archivo_nombre: Nombre del archivo original (opcional)

        Returns:
            Diccionario con toda la metadata extraída
        """
        metadata = {
            'archivo_original': archivo_nombre,
            'fecha_extraccion': datetime.now().isoformat(),
            'texto_procesado': True
        }

        # Extraer cada tipo de metadata
        metadata['expediente'] = self.extraer_expediente(texto)
        metadata['caratula'] = self.extraer_caratula(texto)
        metadata['fecha_sentencia'] = self.extraer_fecha(texto)
        metadata['juez'], metadata['tipo_entidad'] = self.extraer_juez(texto)
        metadata['sala'] = self.extraer_sala(texto)
        metadata['fuero'] = self.extraer_fuero(texto)
        metadata['tipo_sentencia'] = self.extraer_tipo_sentencia(texto)
        metadata['actor'] = self.extraer_actor(texto)
        metadata['demandado'] = self.extraer_demandado(texto)
        metadata['materia'] = self.extraer_materia(texto)
        metadata['resultado'] = self.extraer_resultado(texto)
        metadata['tribunal'] = self.inferir_tribunal(metadata)

        # Determinar jurisdicción
        metadata['jurisdiccion'] = self.inferir_jurisdiccion(metadata)

        # Calcular confianza de la extracción
        metadata['confianza_extraccion'] = self.calcular_confianza(metadata)

        return metadata

    def extraer_expediente(self, texto: str) -> Optional[str]:
        """Extrae el número de expediente"""
        texto_inicio = texto[:3000]  # Buscar en los primeros 3000 caracteres

        for patron in self.patrones_expediente:
            match = patron.search(texto_inicio)
            if match:
                return match.group(1).strip()

        return None

    def extraer_caratula(self, texto: str) -> Optional[str]:
        """Extrae la carátula del expediente"""
        texto_inicio = texto[:5000]

        for patron in self.patrones_caratula:
            match = patron.search(texto_inicio)
            if match:
                return match.group(1).strip()

        return None

    def extraer_fecha(self, texto: str) -> Optional[str]:
        """Extrae la fecha de la sentencia y la convierte a formato ISO"""
        texto_inicio = texto[:3000]

        for patron in self.patrones_fecha:
            match = patron.search(texto_inicio)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) == 3:
                        dia, mes, anio = groups

                        # Si el mes es texto, convertirlo a número
                        if mes.isalpha():
                            mes_num = self.meses_esp.get(mes.lower())
                            if mes_num:
                                fecha = datetime(int(anio), mes_num, int(dia))
                                return fecha.strftime('%Y-%m-%d')
                        else:
                            # Formato DD/MM/AAAA
                            fecha = datetime(int(anio), int(mes), int(dia))
                            return fecha.strftime('%Y-%m-%d')
                except:
                    continue

        return None

    def extraer_juez(self, texto: str) -> Tuple[Optional[str], str]:
        """
        Extrae el/los juez/ces

        Returns:
            Tupla (nombre_juez, tipo_entidad)
            tipo_entidad: 'individual' o 'sala'
        """
        texto_inicio = texto[:5000]

        # Primero verificar si es sala
        if self.extraer_sala(texto):
            # Es sala, extraer vocales
            vocales = []
            for patron in self.patrones_juez:
                matches = patron.finditer(texto_inicio)
                for match in matches:
                    nombre = match.group(1).strip()
                    if len(nombre) > 5 and nombre not in vocales:
                        vocales.append(nombre)

            if vocales:
                return ', '.join(vocales[:3]), 'sala'  # Máximo 3 vocales
            else:
                return 'Sala (vocales no identificados)', 'sala'

        # Si no es sala, es juez individual
        for patron in self.patrones_juez:
            match = patron.search(texto_inicio)
            if match:
                nombre = match.group(1).strip()
                if len(nombre) > 5:
                    return nombre, 'individual'

        return None, 'individual'

    def extraer_sala(self, texto: str) -> Optional[str]:
        """Extrae información de sala si es tribunal colegiado"""
        texto_inicio = texto[:3000]

        for patron in self.patrones_sala:
            match = patron.search(texto_inicio)
            if match:
                return match.group(0).strip()

        return None

    def extraer_fuero(self, texto: str) -> Optional[str]:
        """Extrae el fuero"""
        texto_inicio = texto[:3000]

        for patron in self.patrones_fuero:
            match = patron.search(texto_inicio)
            if match:
                fuero_raw = match.group(1).strip().lower()

                # Normalizar fueros comunes
                if 'laboral' in fuero_raw or 'trabajo' in fuero_raw:
                    return 'laboral'
                elif 'civil' in fuero_raw and 'comercial' in fuero_raw:
                    return 'civil_comercial'
                elif 'civil' in fuero_raw:
                    return 'civil'
                elif 'comercial' in fuero_raw:
                    return 'comercial'
                elif 'penal' in fuero_raw:
                    return 'penal'
                elif 'contencioso' in fuero_raw or 'administrativo' in fuero_raw:
                    return 'contencioso_administrativo'
                elif 'familia' in fuero_raw:
                    return 'familia'
                elif 'seguridad social' in fuero_raw:
                    return 'seguridad_social'
                else:
                    return fuero_raw

        return None

    def extraer_tipo_sentencia(self, texto: str) -> Optional[str]:
        """Extrae el tipo de sentencia"""
        texto_inicio = texto[:2000]

        for patron in self.patrones_tipo_sentencia:
            match = patron.search(texto_inicio)
            if match:
                tipo = match.group(1).strip().lower()
                return tipo

        return 'definitiva'  # Por defecto

    def extraer_actor(self, texto: str) -> Optional[str]:
        """Extrae el actor/demandante"""
        texto_inicio = texto[:5000]

        for patron in self.patrones_actor:
            match = patron.search(texto_inicio)
            if match:
                actor = match.group(1).strip()
                if len(actor) > 3:
                    return actor

        return None

    def extraer_demandado(self, texto: str) -> Optional[str]:
        """Extrae el demandado"""
        texto_inicio = texto[:5000]

        for patron in self.patrones_demandado:
            match = patron.search(texto_inicio)
            if match:
                demandado = match.group(1).strip()
                if len(demandado) > 3:
                    return demandado

        return None

    def extraer_materia(self, texto: str) -> Optional[str]:
        """Extrae la materia del caso"""
        # Primero intentar desde la carátula
        caratula = self.extraer_caratula(texto)
        if caratula:
            match = re.search(r's\/\s+([^\.]+)', caratula)
            if match:
                return match.group(1).strip().lower()

        # Sino, buscar en el texto
        texto_inicio = texto[:5000]
        for patron in self.patrones_materia:
            match = patron.search(texto_inicio)
            if match:
                materia = match.group(1).strip().lower()
                if len(materia) > 3:
                    return materia

        return None

    def extraer_resultado(self, texto: str) -> Optional[str]:
        """Extrae el resultado de la sentencia"""
        # Buscar en la parte dispositiva (generalmente al final)
        texto_dispositivo = texto[-5000:]

        for patron in self.patrones_resultado:
            match = patron.search(texto_dispositivo)
            if match:
                resultado_raw = match.group(0).lower()

                if 'hacer lugar' in resultado_raw and 'no hacer lugar' not in resultado_raw:
                    return 'hace_lugar'
                elif 'no hacer lugar' in resultado_raw or 'rechazar' in resultado_raw:
                    return 'rechaza'
                elif 'parcialmente' in resultado_raw:
                    return 'hace_lugar_parcial'

        return None

    def inferir_tribunal(self, metadata: Dict) -> str:
        """Infiere el nombre del tribunal basado en la metadata"""
        partes = []

        if metadata.get('sala'):
            partes.append(metadata['sala'])
        elif metadata.get('fuero'):
            if metadata['tipo_entidad'] == 'sala':
                partes.append(f"Cámara de Apelaciones en lo {metadata['fuero'].title()}")
            else:
                partes.append(f"Juzgado en lo {metadata['fuero'].title()}")

        return ' - '.join(partes) if partes else 'Tribunal no identificado'

    def inferir_jurisdiccion(self, metadata: Dict) -> str:
        """Infiere si es federal o provincial"""
        tribunal = metadata.get('tribunal', '').lower()
        sala = metadata.get('sala', '').lower() if metadata.get('sala') else ''

        if 'nacional' in tribunal or 'nacional' in sala:
            return 'federal'
        elif 'federal' in tribunal or 'federal' in sala:
            return 'federal'
        else:
            return 'provincial'

    def calcular_confianza(self, metadata: Dict) -> float:
        """
        Calcula un score de confianza de la extracción

        Returns:
            float entre 0 y 1
        """
        campos_importantes = [
            'expediente', 'fecha_sentencia', 'juez',
            'fuero', 'actor', 'demandado'
        ]

        campos_extraidos = sum(1 for campo in campos_importantes if metadata.get(campo))
        confianza = campos_extraidos / len(campos_importantes)

        return round(confianza, 2)

    def validar_metadata(self, metadata: Dict) -> Tuple[bool, List[str]]:
        """
        Valida que la metadata tenga los campos mínimos necesarios

        Returns:
            Tupla (es_valido, lista_errores)
        """
        errores = []

        # Campos obligatorios
        if not metadata.get('juez'):
            errores.append("Falta identificar el juez")

        if not metadata.get('expediente'):
            errores.append("Falta número de expediente")

        if not metadata.get('fecha_sentencia'):
            errores.append("Falta fecha de sentencia")

        # Advertencias (no bloquean)
        if not metadata.get('caratula'):
            errores.append("Advertencia: No se pudo extraer carátula")

        if not metadata.get('fuero'):
            errores.append("Advertencia: No se pudo identificar fuero")

        es_valido = len([e for e in errores if not e.startswith('Advertencia')]) == 0

        return es_valido, errores

    def exportar_json(self, metadata: Dict, ruta_salida: str):
        """Exporta la metadata a un archivo JSON"""
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

    def imprimir_metadata(self, metadata: Dict):
        """Imprime la metadata de forma legible"""
        print("\n" + "="*70)
        print("METADATA EXTRAÍDA")
        print("="*70)

        for clave, valor in metadata.items():
            if valor and clave != 'texto_procesado':
                print(f"{clave.replace('_', ' ').title()}: {valor}")

        print(f"\nConfianza de extracción: {metadata.get('confianza_extraccion', 0)*100:.0f}%")
        print("="*70 + "\n")


def test_extractor():
    """Función de testing"""
    texto_ejemplo = """
    JUZGADO NACIONAL DEL TRABAJO N° 45
    Expediente Nro. 12345/2023

    Autos: "PÉREZ, JUAN c/ EMPRESA ABC S.A. s/ DESPIDO"

    Buenos Aires, 15 de marzo de 2024

    VISTOS: estos autos caratulados "PÉREZ, JUAN c/ EMPRESA ABC S.A. s/ DESPIDO"

    Juez: Dr. Roberto González

    CONSIDERANDO:
    [... contenido de la sentencia ...]

    RESUELVO:
    HACER LUGAR a la demanda interpuesta...
    """

    extractor = ExtractorMetadataArgentina()
    metadata = extractor.extraer_metadata(texto_ejemplo, "sentencia_ejemplo.pdf")
    extractor.imprimir_metadata(metadata)

    # Validar
    es_valido, errores = extractor.validar_metadata(metadata)
    print(f"Metadata válida: {es_valido}")
    if errores:
        print("Errores/Advertencias:")
        for error in errores:
            print(f"  - {error}")


if __name__ == "__main__":
    test_extractor()
