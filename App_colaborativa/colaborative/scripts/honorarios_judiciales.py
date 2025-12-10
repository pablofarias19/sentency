#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULO DE HONORARIOS JUDICIALES - CORDOBA, ARGENTINA
=====================================================

Sistema para el analisis y calculo de honorarios profesionales
en el ambito judicial de Cordoba, Argentina.

REGLAS FUNDAMENTALES:
=====================

1. UNIDAD DE MEDIDA: Los honorarios SIEMPRE se determinan en JUS
   (unidad arancelaria del Poder Judicial de Cordoba).
   Si el monto esta en pesos, debe convertirse a JUS.

2. LIMITE DEL 30% MAXIMO:
   - SOLO aplica a sentencias que resuelven sobre REGULACION DE
     HONORARIOS DE LOS LETRADOS ACTORES o ABOGADOS que reclaman
     su regulacion de honorarios.
   - NO aplica a causas donde se cita a peritos para realizar
     labores periciales por otras razones.

3. FUENTE OFICIAL:
   Los valores JUS actualizados se obtienen de:
   https://www.justiciacordoba.gob.ar/justiciacordoba/Servicios/JUSyUnidadEconomica/1

AUTOR: Sistema Judicial v1.0
FECHA: 10 DIC 2025
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import date

# Importar el gestor de valores JUS
from valores_jus_cordoba import GestorValoresJUS, ValorJUS


class TipoCausaHonorarios(Enum):
    """
    Tipos de causas en relacion a honorarios

    IMPORTANTE:
    - REGULACION_HONORARIOS_LETRADOS: Causas donde el objeto ES la
      regulacion de honorarios de abogados/letrados. Aqui aplica el 30% max.
    - HONORARIOS_PERITOS_EN_CAUSA: Causas donde se designa peritos para
      realizar labores periciales. El objeto de la causa es OTRO (ej: danos,
      despido, etc.) y los honorarios periciales son accesorios.
    """
    REGULACION_HONORARIOS_LETRADOS = "regulacion_honorarios_letrados"
    HONORARIOS_PERITOS_EN_CAUSA = "honorarios_peritos_en_causa"
    OTRAS_CAUSAS = "otras_causas"


@dataclass
class HonorarioRegulado:
    """Representa un honorario regulado en una sentencia"""
    beneficiario: str  # Nombre del profesional
    tipo_profesional: str  # letrado, perito, mediador, etc.
    monto_jus: float  # Monto en JUS
    monto_pesos: Optional[float] = None  # Monto equivalente en pesos
    porcentaje_base: Optional[float] = None  # Porcentaje sobre la base regulatoria
    base_regulatoria_jus: Optional[float] = None  # Base sobre la que se calcula
    concepto: str = ""  # Labor realizada
    aplica_limite_30: bool = False  # Si aplica el limite del 30%
    observaciones: str = ""


@dataclass
class AnalisisHonorarios:
    """Resultado del analisis de honorarios de una sentencia"""
    tipo_causa: TipoCausaHonorarios
    es_regulacion_honorarios_letrados: bool
    aplica_limite_30_maximo: bool
    base_regulatoria_jus: Optional[float]
    base_regulatoria_pesos: Optional[float]
    honorarios_regulados: List[HonorarioRegulado]
    total_honorarios_jus: float
    porcentaje_total: Optional[float]  # Sobre la base regulatoria
    excede_limite_30: bool
    valor_jus_aplicado: float
    fecha_valor_jus: str
    observaciones: List[str]


class AnalizadorHonorarios:
    """
    Analizador de honorarios en sentencias judiciales

    REGLA CLAVE:
    El limite del 30% maximo SOLO aplica cuando la sentencia resuelve
    sobre regulacion de honorarios de letrados/abogados.
    NO aplica para honorarios de peritos designados en otras causas.
    """

    # Patrones para detectar tipo de causa
    PATRONES_REGULACION_HONORARIOS_LETRADOS = [
        r'regulaci[oó]n\s+de\s+honorarios?\s+(?:del?\s+)?(?:letrado|abogado|profesional)',
        r's/\s*regulaci[oó]n\s+(?:de\s+)?honorarios',
        r'reclamo?\s+(?:de\s+)?honorarios?\s+(?:profesionales?|del?\s+letrado)',
        r'incidente\s+(?:de\s+)?regulaci[oó]n\s+(?:de\s+)?honorarios',
        r'letrado\s+(?:actor|reclamante)\s+.*honorarios',
        r'abogado\s+(?:actor|reclamante)\s+.*honorarios',
        r'honorarios?\s+(?:del?\s+)?(?:letrado|abogado)\s+(?:actor|patrocinante)',
    ]

    # Patrones para detectar honorarios de peritos (no aplica 30%)
    PATRONES_HONORARIOS_PERITOS = [
        r'honorarios?\s+(?:del?\s+)?perito',
        r'perito\s+.*honorarios',
        r'pericia\s+.*honorarios',
        r'labor\s+pericial',
        r'dictamen\s+pericial',
    ]

    # Patrones para extraer montos en JUS
    PATRONES_MONTO_JUS = [
        r'(\d+(?:[.,]\d+)?)\s*(?:jus|JUS)',
        r'(?:jus|JUS)\s*(\d+(?:[.,]\d+)?)',
        r'(\d+(?:[.,]\d+)?)\s*unidades?\s*(?:jus|JUS|arancelarias?)',
    ]

    # Patrones para extraer porcentajes
    PATRONES_PORCENTAJE = [
        r'(\d+(?:[.,]\d+)?)\s*%',
        r'(\d+(?:[.,]\d+)?)\s*por\s+ciento',
    ]

    def __init__(self):
        self.gestor_jus = GestorValoresJUS()

    def determinar_tipo_causa(self, texto_sentencia: str,
                               materia: Optional[str] = None,
                               objeto: Optional[str] = None) -> TipoCausaHonorarios:
        """
        Determina el tipo de causa en relacion a honorarios

        IMPORTANTE: Distingue entre:
        - Causas cuyo OBJETO es la regulacion de honorarios de letrados
          (aqui aplica el limite del 30%)
        - Causas donde hay peritos pero el objeto es otro
          (NO aplica el limite del 30%)

        Args:
            texto_sentencia: Texto completo de la sentencia
            materia: Materia de la causa (si se conoce)
            objeto: Objeto del proceso (si se conoce)

        Returns:
            TipoCausaHonorarios indicando el tipo
        """
        texto_lower = texto_sentencia.lower()
        objeto_lower = (objeto or "").lower()
        materia_lower = (materia or "").lower()

        # Verificar si es causa de regulacion de honorarios de letrados
        es_regulacion_letrados = False

        # Buscar en el objeto del proceso (mas confiable)
        for patron in self.PATRONES_REGULACION_HONORARIOS_LETRADOS:
            if re.search(patron, objeto_lower, re.IGNORECASE):
                es_regulacion_letrados = True
                break

        # Si no se encontro en el objeto, buscar en el texto completo
        # pero ser mas estrictos (debe estar en caratula o parte dispositiva)
        if not es_regulacion_letrados:
            # Buscar en primeras 1000 caracteres (encabezado/caratula)
            texto_encabezado = texto_lower[:1000]
            for patron in self.PATRONES_REGULACION_HONORARIOS_LETRADOS:
                if re.search(patron, texto_encabezado, re.IGNORECASE):
                    es_regulacion_letrados = True
                    break

        if es_regulacion_letrados:
            return TipoCausaHonorarios.REGULACION_HONORARIOS_LETRADOS

        # Verificar si hay honorarios de peritos (no aplica 30%)
        for patron in self.PATRONES_HONORARIOS_PERITOS:
            if re.search(patron, texto_lower, re.IGNORECASE):
                return TipoCausaHonorarios.HONORARIOS_PERITOS_EN_CAUSA

        return TipoCausaHonorarios.OTRAS_CAUSAS

    def extraer_montos_jus(self, texto: str) -> List[Tuple[float, str]]:
        """
        Extrae todos los montos en JUS mencionados en el texto

        Returns:
            Lista de tuplas (monto, contexto)
        """
        resultados = []
        texto_lower = texto.lower()

        for patron in self.PATRONES_MONTO_JUS:
            for match in re.finditer(patron, texto_lower):
                try:
                    monto_str = match.group(1).replace(',', '.')
                    monto = float(monto_str)
                    # Obtener contexto (50 chars antes y despues)
                    inicio = max(0, match.start() - 50)
                    fin = min(len(texto), match.end() + 50)
                    contexto = texto[inicio:fin].strip()
                    resultados.append((monto, contexto))
                except (ValueError, IndexError):
                    continue

        return resultados

    def extraer_porcentajes(self, texto: str) -> List[Tuple[float, str]]:
        """
        Extrae todos los porcentajes mencionados en el texto

        Returns:
            Lista de tuplas (porcentaje, contexto)
        """
        resultados = []

        for patron in self.PATRONES_PORCENTAJE:
            for match in re.finditer(patron, texto, re.IGNORECASE):
                try:
                    porc_str = match.group(1).replace(',', '.')
                    porcentaje = float(porc_str)
                    # Obtener contexto
                    inicio = max(0, match.start() - 50)
                    fin = min(len(texto), match.end() + 50)
                    contexto = texto[inicio:fin].strip()
                    resultados.append((porcentaje, contexto))
                except (ValueError, IndexError):
                    continue

        return resultados

    def verificar_limite_30_porciento(self, tipo_causa: TipoCausaHonorarios,
                                       porcentaje_total: float) -> Dict:
        """
        Verifica si aplica y se cumple el limite del 30%

        REGLA:
        El 30% maximo SOLO aplica a sentencias que resuelven sobre
        regulacion de honorarios de letrados actores o abogados.
        NO aplica para peritos citados en otras causas.

        Args:
            tipo_causa: Tipo de causa determinado
            porcentaje_total: Porcentaje total de honorarios sobre la base

        Returns:
            Diccionario con el analisis
        """
        aplica_limite = tipo_causa == TipoCausaHonorarios.REGULACION_HONORARIOS_LETRADOS

        resultado = {
            "tipo_causa": tipo_causa.value,
            "aplica_limite_30_maximo": aplica_limite,
            "porcentaje_calculado": porcentaje_total,
            "excede_limite": False,
            "explicacion": ""
        }

        if aplica_limite:
            if porcentaje_total > 30.0:
                resultado["excede_limite"] = True
                resultado["explicacion"] = (
                    f"EXCEDE LIMITE: El porcentaje de {porcentaje_total:.2f}% excede "
                    f"el maximo del 30% establecido para regulacion de honorarios "
                    f"de letrados. El limite aplica porque la causa es de regulacion "
                    f"de honorarios de abogados/letrados actores."
                )
            else:
                resultado["explicacion"] = (
                    f"DENTRO DEL LIMITE: El porcentaje de {porcentaje_total:.2f}% "
                    f"esta dentro del maximo del 30% para regulacion de honorarios "
                    f"de letrados."
                )
        else:
            resultado["explicacion"] = (
                f"NO APLICA LIMITE 30%: Esta causa es de tipo "
                f"'{tipo_causa.value}'. El limite del 30% maximo solo aplica "
                f"a sentencias que resuelven sobre regulacion de honorarios de "
                f"letrados actores o abogados. En causas donde se cita peritos "
                f"para labores periciales por otras razones, no aplica este limite."
            )

        return resultado

    def analizar_sentencia(self, texto_sentencia: str,
                           materia: Optional[str] = None,
                           objeto: Optional[str] = None,
                           fecha: Optional[str] = None) -> AnalisisHonorarios:
        """
        Analiza los honorarios en una sentencia

        Args:
            texto_sentencia: Texto completo de la sentencia
            materia: Materia de la causa
            objeto: Objeto del proceso
            fecha: Fecha de la sentencia (para valor JUS)

        Returns:
            AnalisisHonorarios con el resultado completo
        """
        # Determinar tipo de causa
        tipo_causa = self.determinar_tipo_causa(texto_sentencia, materia, objeto)
        es_regulacion_letrados = tipo_causa == TipoCausaHonorarios.REGULACION_HONORARIOS_LETRADOS
        aplica_limite_30 = es_regulacion_letrados

        # Obtener valor JUS vigente
        valor_jus = self.gestor_jus.obtener_valor_jus_vigente(fecha)
        valor_jus_pesos = valor_jus.valor_pesos if valor_jus else 0.0
        fecha_valor = valor_jus.fecha_vigencia if valor_jus else "No disponible"

        # Extraer montos y porcentajes
        montos_jus = self.extraer_montos_jus(texto_sentencia)
        porcentajes = self.extraer_porcentajes(texto_sentencia)

        # Construir lista de honorarios regulados
        honorarios = []
        total_jus = 0.0

        for monto, contexto in montos_jus:
            # Determinar si es de letrado o perito basado en contexto
            es_perito = any(
                re.search(patron, contexto.lower())
                for patron in self.PATRONES_HONORARIOS_PERITOS
            )
            tipo_profesional = "perito" if es_perito else "letrado"

            honorario = HonorarioRegulado(
                beneficiario="Extraido de sentencia",
                tipo_profesional=tipo_profesional,
                monto_jus=monto,
                monto_pesos=monto * valor_jus_pesos if valor_jus_pesos > 0 else None,
                concepto=contexto[:100],
                aplica_limite_30=aplica_limite_30 and not es_perito
            )
            honorarios.append(honorario)
            total_jus += monto

        # Calcular porcentaje sobre base regulatoria (si se puede determinar)
        base_regulatoria_jus = None
        porcentaje_total = None
        excede_limite = False

        # Buscar base regulatoria mencionada
        patron_base = r'base\s+regulatoria\s+(?:de\s+)?(\d+(?:[.,]\d+)?)\s*(?:jus|JUS)?'
        match_base = re.search(patron_base, texto_sentencia, re.IGNORECASE)
        if match_base:
            try:
                base_regulatoria_jus = float(match_base.group(1).replace(',', '.'))
                if base_regulatoria_jus > 0:
                    porcentaje_total = (total_jus / base_regulatoria_jus) * 100
                    if aplica_limite_30 and porcentaje_total > 30.0:
                        excede_limite = True
            except ValueError:
                pass

        # Observaciones
        observaciones = []

        if tipo_causa == TipoCausaHonorarios.REGULACION_HONORARIOS_LETRADOS:
            observaciones.append(
                "Esta causa ES de regulacion de honorarios de letrados. "
                "Aplica el limite maximo del 30%."
            )
        elif tipo_causa == TipoCausaHonorarios.HONORARIOS_PERITOS_EN_CAUSA:
            observaciones.append(
                "Esta causa tiene honorarios de peritos pero NO es de "
                "regulacion de honorarios de letrados. NO aplica el limite del 30%."
            )

        if not valor_jus:
            observaciones.append(
                f"ATENCION: No se encontro valor JUS vigente. "
                f"Consulte: {self.gestor_jus.URL_OFICIAL_JUS}"
            )

        if excede_limite:
            observaciones.append(
                f"ALERTA: El porcentaje total ({porcentaje_total:.2f}%) "
                f"excede el limite del 30% para regulacion de honorarios de letrados."
            )

        return AnalisisHonorarios(
            tipo_causa=tipo_causa,
            es_regulacion_honorarios_letrados=es_regulacion_letrados,
            aplica_limite_30_maximo=aplica_limite_30,
            base_regulatoria_jus=base_regulatoria_jus,
            base_regulatoria_pesos=base_regulatoria_jus * valor_jus_pesos if base_regulatoria_jus and valor_jus_pesos else None,
            honorarios_regulados=honorarios,
            total_honorarios_jus=total_jus,
            porcentaje_total=porcentaje_total,
            excede_limite_30=excede_limite,
            valor_jus_aplicado=valor_jus_pesos,
            fecha_valor_jus=fecha_valor,
            observaciones=observaciones
        )

    def convertir_pesos_a_jus(self, monto_pesos: float,
                              fecha: Optional[str] = None) -> Dict:
        """
        Convierte un monto de pesos a JUS

        Los honorarios SIEMPRE se determinan en JUS.
        Si el valor esta en pesos, debe traducirse.

        Args:
            monto_pesos: Monto en pesos argentinos
            fecha: Fecha para el valor JUS

        Returns:
            Diccionario con la conversion
        """
        return self.gestor_jus.convertir_pesos_a_jus(monto_pesos, fecha)


def test_analizador_honorarios():
    """Test del analizador de honorarios"""
    print("=" * 70)
    print("TEST DEL ANALIZADOR DE HONORARIOS JUDICIALES")
    print("=" * 70)

    analizador = AnalizadorHonorarios()

    # Caso 1: Regulacion de honorarios de letrados (SI aplica 30%)
    print("\n" + "=" * 70)
    print("CASO 1: REGULACION DE HONORARIOS DE LETRADOS")
    print("=" * 70)

    texto_caso1 = """
    JUZGADO CIVIL - CORDOBA
    Autos: "PEREZ, JUAN c/ EMPRESA S.A. s/ REGULACION DE HONORARIOS DEL LETRADO"
    Expediente N 12345/2024

    VISTO: El incidente de regulacion de honorarios promovido por el
    Dr. Carlos Rodriguez, letrado actor en los autos principales...

    CONSIDERANDO: Que el letrado reclamante solicita la regulacion de sus
    honorarios profesionales por la labor desarrollada en el juicio principal.
    La base regulatoria asciende a 1000 JUS...

    RESUELVO: Regular los honorarios del Dr. Carlos Rodriguez, letrado actor,
    en la suma de 250 JUS, equivalente al 25% de la base regulatoria...

    Dr. MARTINEZ - Juez
    """

    resultado1 = analizador.analizar_sentencia(
        texto_caso1,
        materia="regulacion de honorarios",
        objeto="regulacion de honorarios del letrado actor"
    )

    print(f"Tipo de causa: {resultado1.tipo_causa.value}")
    print(f"Es regulacion de honorarios de letrados: {resultado1.es_regulacion_honorarios_letrados}")
    print(f"Aplica limite del 30%: {resultado1.aplica_limite_30_maximo}")
    print(f"Total honorarios JUS: {resultado1.total_honorarios_jus}")
    print(f"Excede limite: {resultado1.excede_limite_30}")
    print(f"Observaciones: {resultado1.observaciones}")

    # Caso 2: Causa de danos con perito (NO aplica 30%)
    print("\n" + "=" * 70)
    print("CASO 2: CAUSA DE DANOS CON PERITO (NO aplica 30%)")
    print("=" * 70)

    texto_caso2 = """
    JUZGADO CIVIL - CORDOBA
    Autos: "GARCIA, MARIA c/ CLINICA SA s/ DANOS Y PERJUICIOS"
    Expediente N 67890/2024

    VISTO: La demanda por danos y perjuicios promovida por Maria Garcia
    contra Clinica SA por mala praxis medica...

    CONSIDERANDO: Que de la pericia medica obrante a fs. 45/60, realizada
    por el perito medico Dr. Lopez, surge que existio negligencia...

    RESUELVO:
    1) HACER LUGAR a la demanda de danos y perjuicios.
    2) CONDENAR a Clinica SA al pago de 5000 JUS en concepto de indemnizacion.
    3) Regular los honorarios del perito medico Dr. Lopez en 500 JUS por
       la labor pericial realizada...

    Dr. FERNANDEZ - Juez
    """

    resultado2 = analizador.analizar_sentencia(
        texto_caso2,
        materia="danos y perjuicios",
        objeto="danos y perjuicios - mala praxis"
    )

    print(f"Tipo de causa: {resultado2.tipo_causa.value}")
    print(f"Es regulacion de honorarios de letrados: {resultado2.es_regulacion_honorarios_letrados}")
    print(f"Aplica limite del 30%: {resultado2.aplica_limite_30_maximo}")
    print(f"Total honorarios JUS: {resultado2.total_honorarios_jus}")
    print(f"Observaciones: {resultado2.observaciones}")

    # Test de verificacion de limite
    print("\n" + "=" * 70)
    print("TEST DE VERIFICACION DE LIMITE 30%")
    print("=" * 70)

    # Para causa de letrados con 35% (excede)
    verificacion1 = analizador.verificar_limite_30_porciento(
        TipoCausaHonorarios.REGULACION_HONORARIOS_LETRADOS, 35.0
    )
    print(f"\nCausa de letrados con 35%:")
    print(f"  {verificacion1['explicacion']}")

    # Para causa de peritos con 35% (no aplica limite)
    verificacion2 = analizador.verificar_limite_30_porciento(
        TipoCausaHonorarios.HONORARIOS_PERITOS_EN_CAUSA, 35.0
    )
    print(f"\nCausa con peritos con 35%:")
    print(f"  {verificacion2['explicacion']}")

    # Test de conversion pesos a JUS
    print("\n" + "=" * 70)
    print("TEST DE CONVERSION PESOS A JUS")
    print("=" * 70)

    conversion = analizador.convertir_pesos_a_jus(100000.00)
    print(json.dumps(conversion, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    test_analizador_honorarios()
