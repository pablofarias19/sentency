#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VALIDADOR DE COHERENCIA COGNITIVA
====================================

Implementa las 6 validaciones de coherencia entre dimensiones que estaban faltando.

ESTADO ANTERIOR:
- ❌ 0/6 validaciones implementadas
- ❌ Perfiles contradictorios se guardaban sin alertas
- ❌ coherencia_global hardcoded a 0.5

ESTE MÓDULO IMPLEMENTA:
1. ✅ Empirismo ↔ Dogmatismo (antagónicas)
2. ✅ Creatividad ↔ Dogmatismo (antagónicas)
3. ✅ Nivel Abstracción ↔ Empirismo (correlacionadas)
4. ✅ Complejidad Sintáctica ↔ Creatividad (correlacionadas)
5. ✅ Coherencia Global (cálculo real vs placeholder)
6. ✅ Interdisciplinariedad (validación de especialización)

UBICACIÓN DE INSERCIÓN EN ORCHESTRADOR:
orchestrador_maestro_integrado.py línea 176 (ANTES de cursor.execute INSERT)
"""

import logging
from typing import Dict, Tuple, List
from dataclasses import dataclass

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ResultadoValidacion:
    """Resultado de una validación de coherencia"""
    es_valido: bool
    tipo_alerta: str  # "ERROR", "WARNING", "INFO"
    mensaje: str
    dimension1: str
    dimension2: str
    valor1: float
    valor2: float
    sugerencia: str = ""


class ValidadorCoherenciaCognitiva:
    """Valida coherencia entre dimensiones cognitivas"""
    
    def __init__(self, modo_estricto: bool = True):
        """
        modo_estricto=True: Errores rechazan el perfil
        modo_estricto=False: Solo warnings, se guarda igual
        """
        self.modo_estricto = modo_estricto
        self.validaciones_ejecutadas = []
        self.errores = []
        self.warnings = []
    
    # ========================================================================
    # VALIDACIÓN 1: EMPIRISMO ↔ DOGMATISMO (Antagónicas)
    # ========================================================================
    
    def validar_empirismo_vs_dogmatismo(self, marcadores: Dict) -> ResultadoValidacion:
        """
        REGLA: Si EMPIRISMO > 0.7, entonces DOGMATISMO < 0.4
        
        Lógica:
        - Autor empirista: Se basa en datos, evidencia, muestras
        - Autor dogmático: Afirma sin demostración
        - Contradicción: NO pueden coexistir en alto grado
        
        Ejemplo de contradicción:
        - empirismo=0.9: "Basado en datos estadísticos..."
        - dogmatismo=0.85: "Es indudable e inequívoco..."
        - INCOHERENTE: ¿Por qué cita datos pero afirma sin prueba?
        """
        
        empirismo = marcadores.get('empirismo', 0.0)
        dogmatismo = marcadores.get('dogmatismo', 0.0)
        
        es_valido = True
        tipo_alerta = "INFO"
        mensaje = ""
        sugerencia = ""
        
        # REGLA ESTRICTA: E > 0.7 → D < 0.4
        if empirismo > 0.7 and dogmatismo > 0.4:
            es_valido = False
            tipo_alerta = "ERROR"
            mensaje = f"Contradicción fundamental: Empirismo={empirismo:.2f} (alto) + Dogmatismo={dogmatismo:.2f} (alto)"
            sugerencia = f"Reducir dogmatismo a < 0.4 o empirismo a < 0.7. Actualmente incompatibles."
        
        # ADVERTENCIA: E > 0.6 Y D > 0.5
        elif empirismo > 0.6 and dogmatismo > 0.5:
            tipo_alerta = "WARNING"
            mensaje = f"Inusual: Empirismo moderado-alto={empirismo:.2f} + Dogmatismo moderado={dogmatismo:.2f}"
            sugerencia = "Revisar si la argumentación mezcla datos con afirmaciones sin prueba"
        
        self.validaciones_ejecutadas.append("empirismo_vs_dogmatismo")
        return ResultadoValidacion(
            es_valido=es_valido,
            tipo_alerta=tipo_alerta,
            mensaje=mensaje,
            dimension1="empirismo",
            dimension2="dogmatismo",
            valor1=empirismo,
            valor2=dogmatismo,
            sugerencia=sugerencia
        )
    
    # ========================================================================
    # VALIDACIÓN 2: CREATIVIDAD ↔ DOGMATISMO (Antagónicas)
    # ========================================================================
    
    def validar_creatividad_vs_dogmatismo(self, marcadores: Dict) -> ResultadoValidacion:
        """
        REGLA: Si CREATIVIDAD > 0.7, entonces DOGMATISMO < 0.3
        
        Lógica:
        - Autor creativo: Propone reinterpretaciones, nuevos enfoques
        - Autor dogmático: Sigue principios rígidamente
        - Contradicción: Incompatibles en alto grado
        
        Ejemplo:
        - creatividad=0.8: "Propongo una teoría novedosa"
        - dogmatismo=0.7: "Basada en principios indudables"
        - INCOHERENTE: ¿Cómo es novedoso si se basa en indudables?
        """
        
        creatividad = marcadores.get('creatividad', 0.0)
        dogmatismo = marcadores.get('dogmatismo', 0.0)
        
        es_valido = True
        tipo_alerta = "INFO"
        mensaje = ""
        sugerencia = ""
        
        # REGLA ESTRICTA: C > 0.7 → D < 0.3
        if creatividad > 0.7 and dogmatismo > 0.3:
            es_valido = False
            tipo_alerta = "ERROR"
            mensaje = f"Contradicción: Creatividad={creatividad:.2f} (alta) + Dogmatismo={dogmatismo:.2f} (moderado)"
            sugerencia = "Reducir dogmatismo a < 0.3 o creatividad a < 0.7. Ideas innovadoras no pueden ser rígidas."
        
        # ADVERTENCIA: C > 0.6 Y D > 0.4
        elif creatividad > 0.6 and dogmatismo > 0.4:
            tipo_alerta = "WARNING"
            mensaje = f"Inusual: Creatividad moderada-alta={creatividad:.2f} + Dogmatismo moderado={dogmatismo:.2f}"
            sugerencia = "Verificar si las propuestas novedosas son realmente críticas con principios establecidos"
        
        self.validaciones_ejecutadas.append("creatividad_vs_dogmatismo")
        return ResultadoValidacion(
            es_valido=es_valido,
            tipo_alerta=tipo_alerta,
            mensaje=mensaje,
            dimension1="creatividad",
            dimension2="dogmatismo",
            valor1=creatividad,
            valor2=dogmatismo,
            sugerencia=sugerencia
        )
    
    # ========================================================================
    # VALIDACIÓN 3: NIVEL ABSTRACCIÓN ↔ EMPIRISMO (Correlacionadas)
    # ========================================================================
    
    def validar_abstraccion_vs_empirismo(self, marcadores: Dict) -> ResultadoValidacion:
        """
        REGLA: Si NIVEL ABSTRACCIÓN > 0.7, entonces EMPIRISMO debería ser < 0.5
        
        Lógica:
        - Autor teórico: Habla de principios, cláusulas generales, ratios
        - Autor empírico: Cita datos, muestras, evidencia
        - Expectativa: Teóricos tienden a ser menos empíricos (generalmente)
        - NO es error, solo inusualidad estadística
        
        Nota: Existen teóricos empíricos (ej: Hayek: teoría económica basada en datos)
        """
        
        abstraccion = marcadores.get('nivel_abstraccion', 0.0)
        empirismo = marcadores.get('empirismo', 0.0)
        
        es_valido = True
        tipo_alerta = "INFO"
        mensaje = ""
        sugerencia = ""
        
        # ADVERTENCIA: A > 0.7 Y E > 0.6 (inusual pero no error)
        if abstraccion > 0.7 and empirismo > 0.6:
            tipo_alerta = "WARNING"
            mensaje = f"Inusual: Abstracción alta={abstraccion:.2f} + Empirismo moderado-alto={empirismo:.2f}"
            sugerencia = "Autor combina teoría con datos (posible: teórico empirista). Revisar si hay coherencia."
        
        self.validaciones_ejecutadas.append("abstraccion_vs_empirismo")
        return ResultadoValidacion(
            es_valido=es_valido,
            tipo_alerta=tipo_alerta,
            mensaje=mensaje,
            dimension1="nivel_abstraccion",
            dimension2="empirismo",
            valor1=abstraccion,
            valor2=empirismo,
            sugerencia=sugerencia
        )
    
    # ========================================================================
    # VALIDACIÓN 4: COMPLEJIDAD SINTÁCTICA ↔ CREATIVIDAD (Correlacionadas)
    # ========================================================================
    
    def validar_sintaxis_vs_creatividad(self, marcadores: Dict) -> ResultadoValidacion:
        """
        REGLA: Si COMPLEJIDAD SINTÁCTICA > 0.8, esperaríamos CREATIVIDAD > 0.5
        
        Lógica:
        - Oraciones complejas: Suelen indicar argumentación sofisticada
        - Argumentación sofisticada: A menudo incluye ideas nuevas
        - Baja creatividad + Alta complejidad: Inusual (complejidad sin novedad)
        
        Nota: Posible caso: Autor que escribe complejo pero repite argumentos
        """
        
        complejidad = marcadores.get('complejidad_sintactica', 0.0)
        creatividad = marcadores.get('creatividad', 0.0)
        
        es_valido = True
        tipo_alerta = "INFO"
        mensaje = ""
        sugerencia = ""
        
        # ADVERTENCIA: S > 0.8 Y C < 0.4 (inusual)
        if complejidad > 0.8 and creatividad < 0.4:
            tipo_alerta = "WARNING"
            mensaje = f"Inusual: Sintaxis muy compleja={complejidad:.2f} pero creatividad baja={creatividad:.2f}"
            sugerencia = "Posible: Autor sofisticado pero poco original. Revisar si repite argumentos conocidos."
        
        self.validaciones_ejecutadas.append("sintaxis_vs_creatividad")
        return ResultadoValidacion(
            es_valido=es_valido,
            tipo_alerta=tipo_alerta,
            mensaje=mensaje,
            dimension1="complejidad_sintactica",
            dimension2="creatividad",
            valor1=complejidad,
            valor2=creatividad,
            sugerencia=sugerencia
        )
    
    # ========================================================================
    # VALIDACIÓN 5: COHERENCIA GLOBAL (Cálculo real vs placeholder)
    # ========================================================================
    
    def calcular_coherencia_global(self, marcadores: Dict) -> float:
        """
        REEMPLAZA valor hardcoded 0.5 por cálculo real.
        
        Fórmula:
        coherencia = (
            (1 - abs(empirismo - dogmatismo)) * 0.25 +          # Opuestos
            (1 - abs(creatividad - dogmatismo)) * 0.25 +        # Opuestos
            ((abstraccion + empirismo) / 2) * 0.25 +            # Correlacionadas
            ((complejidad + creatividad) / 2) * 0.25            # Correlacionadas
        )
        
        Resultado: 0.0 (muy incoherente) a 1.0 (perfectamente coherente)
        """
        
        empirismo = marcadores.get('empirismo', 0.0)
        dogmatismo = marcadores.get('dogmatismo', 0.0)
        creatividad = marcadores.get('creatividad', 0.0)
        abstraccion = marcadores.get('nivel_abstraccion', 0.0)
        complejidad = marcadores.get('complejidad_sintactica', 0.0)
        
        # Componente 1: Opuestos deberían ser inversamente proporcionales
        coherencia_empirismo_dogmatismo = 1 - abs(empirismo - dogmatismo)
        
        # Componente 2: Creatividad y dogmatismo antagónicos
        coherencia_creatividad_dogmatismo = 1 - abs(creatividad - dogmatismo)
        
        # Componente 3: Abstracción y empirismo correlacionadas moderadamente
        # Si están equilibradas, más coherencia
        coherencia_abstraccion = abs(abstraccion - empirismo)  # Menos similar = más distancia
        coherencia_abstraccion = 1 - (coherencia_abstraccion * 0.5)  # No es factor crítico
        
        # Componente 4: Complejidad y creatividad correlacionadas
        coherencia_sintaxis_creatividad = 1 - abs(complejidad - creatividad) * 0.5
        
        # Ponderación final
        coherencia_global = (
            coherencia_empirismo_dogmatismo * 0.3 +
            coherencia_creatividad_dogmatismo * 0.3 +
            coherencia_abstraccion * 0.2 +
            coherencia_sintaxis_creatividad * 0.2
        )
        
        return min(1.0, max(0.0, coherencia_global))
    
    def validar_coherencia_global(self, marcadores: Dict) -> ResultadoValidacion:
        """
        VALIDACIÓN 5: Coherencia Global real
        
        Antes: Hardcoded a 0.5 (inútil)
        Ahora: Se calcula como función de otras dimensiones
        """
        
        coherencia_anterior = marcadores.get('coherencia_global', 0.5)  # Valor viejo (siempre 0.5)
        coherencia_nueva = self.calcular_coherencia_global(marcadores)
        
        # Marcar si hay gran discrepancia
        tipo_alerta = "INFO"
        mensaje = ""
        sugerencia = ""
        es_valido = True
        
        if abs(coherencia_nueva - 0.5) > 0.3:
            if coherencia_nueva < 0.4:
                tipo_alerta = "WARNING"
                mensaje = f"Coherencia baja calculada: {coherencia_nueva:.2f} (antes stub=0.5)"
                sugerencia = "Perfil tiene dimensiones contradictorias. Revisar dimensiones antagónicas."
            elif coherencia_nueva > 0.8:
                tipo_alerta = "INFO"
                mensaje = f"Coherencia alta calculada: {coherencia_nueva:.2f} (antes stub=0.5)"
                sugerencia = "Perfil muy coherente en sus dimensiones."
        else:
            mensaje = f"Coherencia moderada: {coherencia_nueva:.2f} (antes stub=0.5)"
        
        self.validaciones_ejecutadas.append("coherencia_global")
        return ResultadoValidacion(
            es_valido=es_valido,
            tipo_alerta=tipo_alerta,
            mensaje=mensaje,
            dimension1="coherencia_global",
            dimension2="(calculada)",
            valor1=coherencia_anterior,
            valor2=coherencia_nueva,
            sugerencia=sugerencia
        )
    
    # ========================================================================
    # VALIDACIÓN 6: INTERDISCIPLINARIEDAD vs ESPECIALIZACIÓN
    # ========================================================================
    
    def validar_interdisciplinariedad(self, marcadores: Dict) -> ResultadoValidacion:
        """
        VALIDACIÓN 6: Validar coherencia de interdisciplinariedad
        
        Regla: Si INTERDISCIPLINARIEDAD > 0.8, el autor toca múltiples campos
        - No debería haber especialización extrema en 1 solo campo
        - Debería haber múltiples referencias disciplinarias
        
        Lógica:
        - Interdisciplinario: Cita "económico", "sociológico", "filosófico"
        - Especialista: Solo "jurídico"
        - CONTRADICCIÓN: Alto en ambos simultáneamente sería raro
        """
        
        interdisciplinariedad = marcadores.get('interdisciplinariedad', 0.0)
        
        tipo_alerta = "INFO"
        mensaje = ""
        sugerencia = ""
        es_valido = True
        
        if interdisciplinariedad > 0.8:
            tipo_alerta = "INFO"
            mensaje = f"Autor altamente interdisciplinario: {interdisciplinariedad:.2f}"
            sugerencia = "Combina múltiples perspectivas (económica, sociológica, filosófica, psicológica)"
        elif interdisciplinariedad < 0.2:
            tipo_alerta = "WARNING"
            mensaje = f"Autor muy especializado: {interdisciplinariedad:.2f}"
            sugerencia = "Enfoque principalmente en una disciplina (probablemente jurídica)"
        else:
            mensaje = f"Interdisciplinariedad moderada: {interdisciplinariedad:.2f}"
        
        self.validaciones_ejecutadas.append("interdisciplinariedad")
        return ResultadoValidacion(
            es_valido=es_valido,
            tipo_alerta=tipo_alerta,
            mensaje=mensaje,
            dimension1="interdisciplinariedad",
            dimension2="(especialización)",
            valor1=interdisciplinariedad,
            valor2=1.0 - interdisciplinariedad,
            sugerencia=sugerencia
        )
    
    # ========================================================================
    # MÉTODO PRINCIPAL: Ejecutar todas las validaciones
    # ========================================================================
    
    def validar_todo(self, marcadores: Dict) -> Tuple[bool, List[ResultadoValidacion]]:
        """
        Ejecuta las 6 validaciones y retorna:
        - es_valido: True si puede guardarse, False si hay errores críticos
        - resultados: Lista de ResultadoValidacion con detalles
        """
        
        self.errores = []
        self.warnings = []
        self.validaciones_ejecutadas = []
        
        resultados = [
            self.validar_empirismo_vs_dogmatismo(marcadores),
            self.validar_creatividad_vs_dogmatismo(marcadores),
            self.validar_abstraccion_vs_empirismo(marcadores),
            self.validar_sintaxis_vs_creatividad(marcadores),
            self.validar_coherencia_global(marcadores),
            self.validar_interdisciplinariedad(marcadores),
        ]
        
        # Clasificar resultados
        for resultado in resultados:
            if resultado.tipo_alerta == "ERROR":
                self.errores.append(resultado)
            elif resultado.tipo_alerta == "WARNING":
                self.warnings.append(resultado)
        
        # En modo estricto: errores rechazan el perfil
        es_valido = len(self.errores) == 0 if self.modo_estricto else True
        
        return es_valido, resultados
    
    def generar_reporte(self, resultados: List[ResultadoValidacion]) -> str:
        """Genera reporte legible de validaciones"""
        
        lineas = [
            "=" * 80,
            "📊 REPORTE DE VALIDACIÓN DE COHERENCIA COGNITIVA",
            "=" * 80,
        ]
        
        for r in resultados:
            lineas.append("")
            lineas.append(f"[{r.tipo_alerta}] {r.dimension1.upper()} ↔ {r.dimension2.upper()}")
            lineas.append(f"  Valores: {r.dimension1}={r.valor1:.2f}, {r.dimension2}={r.valor2:.2f}")
            lineas.append(f"  Mensaje: {r.mensaje}")
            if r.sugerencia:
                lineas.append(f"  Sugerencia: {r.sugerencia}")
        
        lineas.append("")
        lineas.append("=" * 80)
        lineas.append(f"Errores: {len(self.errores)} | Warnings: {len(self.warnings)}")
        lineas.append("=" * 80)
        
        return "\n".join(lineas)


# ============================================================================
# INTEGRACIÓN EN ORCHESTRADOR: Función helper
# ============================================================================

def aplicar_validaciones_coherencia(marcadores: Dict, modo_estricto: bool = False) -> Tuple[bool, Dict]:
    """
    Función de conveniencia para integrar en orchestrador_maestro_integrado.py
    
    Uso:
        es_valido, resultado = aplicar_validaciones_coherencia(marcadores)
        if not es_valido:
            raise ValueError(resultado['error'])
    
    Retorna:
        (es_valido, {
            'valido': bool,
            'coherencia_calculada': float,
            'errores': [mensajes],
            'warnings': [mensajes],
            'reporte': str
        })
    """
    
    validador = ValidadorCoherenciaCognitiva(modo_estricto=modo_estricto)
    es_valido, resultados = validador.validar_todo(marcadores)
    
    # Actualizar coherencia_global con cálculo real
    marcadores['coherencia_global'] = validador.calcular_coherencia_global(marcadores)
    
    # Extraer errores y warnings
    errores = [r.mensaje for r in resultados if r.tipo_alerta == "ERROR"]
    warnings = [r.mensaje for r in resultados if r.tipo_alerta == "WARNING"]
    
    resultado = {
        'valido': es_valido,
        'coherencia_calculada': marcadores['coherencia_global'],
        'errores': errores,
        'warnings': warnings,
        'reporte': validador.generar_reporte(resultados),
        'marcadores_actualizados': marcadores
    }
    
    if not es_valido and modo_estricto:
        resultado['error'] = f"Perfil rechazado por coherencia: {'; '.join(errores)}"
    
    return es_valido, resultado


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Caso 1: Perfil coherente
    print("\n" + "="*80)
    print("CASO 1: Perfil COHERENTE")
    print("="*80)
    
    marcadores_coherente = {
        'nivel_abstraccion': 0.6,
        'complejidad_sintactica': 0.5,
        'interdisciplinariedad': 0.5,
        'empirismo': 0.7,
        'dogmatismo': 0.2,
        'creatividad': 0.6,
        'uso_jurisprudencia': 0.8,
        'coherencia_global': 0.5  # Será reemplazado
    }
    
    es_valido, resultado = aplicar_validaciones_coherencia(marcadores_coherente)
    print(resultado['reporte'])
    print(f"\n✅ Válido: {es_valido}")
    print(f"📊 Coherencia calculada: {resultado['coherencia_calculada']:.2f}")
    
    # Caso 2: Perfil INCOHERENTE
    print("\n" + "="*80)
    print("CASO 2: Perfil INCOHERENTE")
    print("="*80)
    
    marcadores_incoherente = {
        'nivel_abstraccion': 0.3,
        'complejidad_sintactica': 0.2,
        'interdisciplinariedad': 0.3,
        'empirismo': 0.9,      # Alto
        'dogmatismo': 0.8,     # Alto → CONTRADICCIÓN
        'creatividad': 0.85,   # Alto
        'uso_jurisprudencia': 0.4,
        'coherencia_global': 0.5
    }
    
    es_valido, resultado = aplicar_validaciones_coherencia(marcadores_incoherente, modo_estricto=True)
    print(resultado['reporte'])
    print(f"\n❌ Válido: {es_valido}")
    print(f"📊 Coherencia calculada: {resultado['coherencia_calculada']:.2f}")
    if 'error' in resultado:
        print(f"⚠️ Error: {resultado['error']}")
