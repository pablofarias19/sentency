#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💡 GENERADOR DE EXPLICACIONES COGNITIVAS INTELIGENTES
==================================================

FUNCIONES:
1. Genera explicaciones claras para cada análisis cognitivo
2. Traduce métricas técnicas a lenguaje comprensible  
3. Crea recomendaciones prácticas basadas en perfiles
4. Proporciona contexto histórico y comparativo
5. Identifica patrones únicos y excepcionales

OBJETIVO: Hacer los análisis cognitivos comprensibles y útiles
AUTOR: Sistema Cognitivo Avanzado v6.0
FECHA: 9 NOV 2025
"""

import json
import sqlite3
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

class GeneradorExplicacionesCognitivas:
    """Sistema inteligente para generar explicaciones comprensibles"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.db_path = self.base_path / "data" / "pensamiento_integrado_v2.db"
        
        # Rangos de interpretación para métricas
        self.rangos_interpretacion = {
            "muy_bajo": (0.0, 0.2),
            "bajo": (0.2, 0.4), 
            "moderado": (0.4, 0.6),
            "alto": (0.6, 0.8),
            "muy_alto": (0.8, 1.0)
        }
        
        # Descripciones interpretativas
        self.descripciones_metricas = {
            "deductivo": {
                "muy_alto": "Pensamiento extremadamente lógico y estructurado. Construye argumentos paso a paso desde principios generales.",
                "alto": "Fuerte tendencia al razonamiento lógico formal. Prefiere conclusiones que se siguen necesariamente de las premisas.",
                "moderado": "Equilibra razonamiento deductivo con otros enfoques. Flexible pero mantiene estructura lógica.",
                "bajo": "Ocasionalmente usa lógica deductiva, pero prefiere otros métodos de razonamiento.",
                "muy_bajo": "Raramente construye argumentos deductivos formales. Prefiere enfoques más intuitivos o empíricos."
            },
            "creatividad": {
                "muy_alto": "Pensador altamente innovador. Genera conceptos originales y enfoques revolucionarios.",
                "alto": "Demuestra creatividad notable. Encuentra soluciones únicas a problemas complejos.",
                "moderado": "Equilibra creatividad con convención. Innova dentro de marcos establecidos.",
                "bajo": "Creatividad limitada. Se adhiere principalmente a enfoques tradicionales.",
                "muy_bajo": "Pensamiento muy convencional. Sigue estrictamente patrones establecidos."
            },
            "formalismo": {
                "muy_alto": "Extremadamente riguroso en el uso de formas legales. Prioriza la estructura por encima del contenido.",
                "alto": "Altamente formalista. Respeta estrictamente las formas y procedimientos jurídicos.",
                "moderado": "Equilibra formalismo con flexibilidad práctica. Respeta formas pero las adapta al contexto.",
                "bajo": "Flexible con las formas legales. Prioriza sustancia sobre estructura.",
                "muy_bajo": "Altamente informal. Minimiza la importancia de las formas legales tradicionales."
            }
        }
    
    def interpretar_valor(self, valor: float, metrica: str) -> Tuple[str, str]:
        """Interpreta un valor numérico y devuelve nivel y descripción"""
        # Determinar nivel
        for nivel, (min_val, max_val) in self.rangos_interpretacion.items():
            if min_val <= valor < max_val:
                nivel_detectado = nivel
                break
        else:
            nivel_detectado = "muy_alto" if valor >= 0.8 else "muy_bajo"
        
        # Obtener descripción
        descripcion = self.descripciones_metricas.get(metrica, {}).get(
            nivel_detectado, 
            f"Valor {nivel_detectado} ({valor:.1%}) para {metrica}"
        )
        
        return nivel_detectado, descripcion
    
    def generar_explicacion_razonamiento(self, perfil: Dict) -> str:
        """Genera explicación detallada del patrón de razonamiento"""
        razonamiento = perfil.get('cognicion', {}).get('razonamiento_formal', {})
        
        # Identificar patrón dominante
        patrones = {
            'deductivo': razonamiento.get('deductivo', 0),
            'inductivo': razonamiento.get('inductivo', 0), 
            'analogico': razonamiento.get('analogico', 0),
            'teleologico': razonamiento.get('teleologico', 0),
            'sistemico': razonamiento.get('sistemico', 0)
        }
        
        patron_dominante = max(patrones.items(), key=lambda x: x[1])
        patron_secundario = sorted(patrones.items(), key=lambda x: x[1], reverse=True)[1]
        
        nivel_dominante, desc_dominante = self.interpretar_valor(patron_dominante[1], patron_dominante[0])
        
        explicacion = f"""
🧠 **ANÁLISIS DEL PATRÓN DE RAZONAMIENTO**

📊 **Patrón Dominante:** {patron_dominante[0].upper()} ({patron_dominante[1]:.1%})
{desc_dominante}

📈 **Patrón Secundario:** {patron_secundario[0].upper()} ({patron_secundario[1]:.1%})

🎯 **Significado Práctico:**
Este autor construye principalmente sus argumentos mediante razonamiento {patron_dominante[0]}, 
lo que significa que {"parte de principios generales para llegar a conclusiones específicas" if patron_dominante[0] == "deductivo" 
else "observa casos particulares para formular reglas generales" if patron_dominante[0] == "inductivo"
else "establece similitudes entre situaciones para transferir soluciones" if patron_dominante[0] == "analogico" 
else "se enfoca en los fines y propósitos de las normas" if patron_dominante[0] == "teleologico"
else "integra elementos en sistemas coherentes"}.

💡 **Recomendación para Aplicación:**
Para comprender mejor este autor, {"siga la lógica paso a paso desde sus premisas" if patron_dominante[0] == "deductivo"
else "observe cómo generaliza desde ejemplos específicos" if patron_dominante[0] == "inductivo" 
else "identifique las analogías que establece" if patron_dominante[0] == "analogico"
else "analice qué objetivos persigue con cada argumento" if patron_dominante[0] == "teleologico"
else "vea cómo conecta diferentes elementos en un todo coherente"}.
"""
        return explicacion
    
    def generar_explicacion_estilo(self, perfil: Dict) -> str:
        """Genera explicación del estilo intelectual del autor"""
        estilo = perfil.get('estilo', {})
        
        formalismo = estilo.get('formalismo_juridico', 0)
        creatividad = perfil.get('cognicion', {}).get('creatividad', {}).get('originalidad_conceptual', 0)
        complejidad = estilo.get('complejidad_conceptual', 0)
        
        nivel_form, desc_form = self.interpretar_valor(formalismo, 'formalismo')
        nivel_creat, desc_creat = self.interpretar_valor(creatividad, 'creatividad')
        
        # Determinar arquetipo intelectual
        if formalismo > 0.7 and creatividad < 0.4:
            arquetipo = "JURISTA TRADICIONALISTA"
            descripcion_arquetipo = "Privilegia la ortodoxia jurídica y la aplicación rigurosa de formas establecidas."
        elif creatividad > 0.7 and formalismo < 0.4:
            arquetipo = "INNOVADOR JURÍDICO" 
            descripcion_arquetipo = "Busca constantemente nuevas formas de entender y aplicar el derecho."
        elif formalismo > 0.6 and creatividad > 0.6:
            arquetipo = "ARQUITECTO LEGAL"
            descripcion_arquetipo = "Combina rigor formal con innovación creativa para construir sistemas coherentes."
        elif formalismo < 0.4 and creatividad < 0.4:
            arquetipo = "PRAGMÁTICO JURÍDICO"
            descripcion_arquetipo = "Se enfoca en soluciones prácticas más que en formas o innovaciones."
        else:
            arquetipo = "JURISTA EQUILIBRADO"
            descripcion_arquetipo = "Mantiene un balance entre tradición e innovación jurídica."
        
        explicacion = f"""
🎭 **ANÁLISIS DEL ESTILO INTELECTUAL**

🏛️ **Arquetipo Detectado:** {arquetipo}
{descripcion_arquetipo}

📊 **Características Principales:**
• **Formalismo Jurídico:** {formalismo:.1%} - {desc_form}
• **Creatividad Conceptual:** {creatividad:.1%} - {desc_creat}
• **Complejidad del Pensamiento:** {complejidad:.1%}

🔍 **Implicaciones Prácticas:**
{"Este autor requiere atención especial a las formas y procedimientos legales" if formalismo > 0.6 
else "Este autor es flexible con las formas, priorizando la sustancia" if formalismo < 0.4
else "Este autor equilibra forma y sustancia"}.

{"Espere enfoques originales e ideas innovadoras" if creatividad > 0.6
else "Espere análisis convencionales y bien establecidos" if creatividad < 0.4  
else "Espere un equilibrio entre tradición e innovación"}.

💼 **Aplicación en la Práctica:**
Este perfil es especialmente útil para {"casos que requieren análisis formal riguroso" if formalismo > 0.6
else "situaciones que demandan soluciones creativas" if creatividad > 0.6
else "casos que necesitan equilibrio entre rigor y flexibilidad"}.
"""
        return explicacion
    
    def generar_explicacion_metodologica(self, perfil: Dict) -> str:
        """Genera explicación de la metodología jurídica empleada"""
        metodologia = perfil.get('metodologia', {})
        
        precedentes = metodologia.get('uso_precedentes', 0)
        flexibilidad = metodologia.get('flexibilidad_interpretativa', 0)
        empirismo = metodologia.get('orientacion_empirica', 0)
        
        explicacion = f"""
⚖️ **ANÁLISIS METODOLÓGICO JURÍDICO**

📚 **Uso de Precedentes:** {precedentes:.1%}
{"Confía fuertemente en jurisprudencia establecida" if precedentes > 0.7
else "Usa precedentes selectivamente" if precedentes > 0.4  
else "Raramente se apoya en precedentes"}

🔄 **Flexibilidad Interpretativa:** {flexibilidad:.1%}
{"Adaptación creativa de normas al contexto" if flexibilidad > 0.7
else "Interpretación equilibrada entre texto y contexto" if flexibilidad > 0.4
else "Interpretación literal y estricta"}

🔬 **Orientación Empírica:** {empirismo:.1%}
{"Fuerte énfasis en datos y evidencia empírica" if empirismo > 0.7  
else "Equilibra teoría y evidencia práctica" if empirismo > 0.4
else "Enfoque principalmente teórico"}

🎯 **Metodología Dominante:**
{"EMPÍRICO-PRAGMÁTICA: Basada en evidencia y resultados prácticos" if empirismo > 0.6
else "DOCTRINAL-SISTEMÁTICA: Basada en principios teóricos y coherencia conceptual" if precedentes > 0.6 and flexibilidad < 0.4
else "INTERPRETATIVA-FLEXIBLE: Adaptación contextual de principios jurídicos" if flexibilidad > 0.6
else "MIXTA-EQUILIBRADA: Combina diferentes enfoques metodológicos"}

💡 **Valor para la Práctica:**
Este enfoque metodológico es especialmente valioso cuando se necesita 
{"análisis basado en datos concretos y resultados medibles" if empirismo > 0.6
else "aplicación rigurosa de principios jurídicos establecidos" if precedentes > 0.6 and flexibilidad < 0.4  
else "interpretación adaptada a circunstancias especiales" if flexibilidad > 0.6
else "análisis integral que considere múltiples perspectivas"}.
"""
        return explicacion
    
    def generar_explicacion_comparativa(self, perfil: Dict, otros_autores: List[Dict] = None) -> str:
        """Genera explicación comparativa con otros autores"""
        if not otros_autores:
            otros_autores = self._obtener_otros_perfiles()
        
        if not otros_autores:
            return "📊 **ANÁLISIS COMPARATIVO:** No hay otros autores disponibles para comparación."
        
        # Calcular posición relativa
        autor_actual = perfil.get('cognicion', {}).get('razonamiento_formal', {}).get('deductivo', 0)
        creatividad_actual = perfil.get('cognicion', {}).get('creatividad', {}).get('originalidad_conceptual', 0)
        
        deductivos_otros = [p.get('cognicion', {}).get('razonamiento_formal', {}).get('deductivo', 0) for p in otros_autores]
        creativos_otros = [p.get('cognicion', {}).get('creatividad', {}).get('originalidad_conceptual', 0) for p in otros_autores]
        
        percentil_deductivo = sum(1 for x in deductivos_otros if x < autor_actual) / len(deductivos_otros) * 100
        percentil_creatividad = sum(1 for x in creativos_otros if x < creatividad_actual) / len(creativos_otros) * 100
        
        explicacion = f"""
📊 **ANÁLISIS COMPARATIVO CON OTROS AUTORES**

📈 **Posición Relativa:**
• **Razonamiento Deductivo:** Percentil {percentil_deductivo:.0f} 
  {"(Entre los más lógicos y estructurados)" if percentil_deductivo > 80
  else "(Por encima del promedio)" if percentil_deductivo > 60
  else "(Nivel promedio)" if percentil_deductivo > 40
  else "(Por debajo del promedio)"}

• **Creatividad Jurídica:** Percentil {percentil_creatividad:.0f}
  {"(Entre los más innovadores)" if percentil_creatividad > 80
  else "(Más creativo que la mayoría)" if percentil_creatividad > 60  
  else "(Creatividad promedio)" if percentil_creatividad > 40
  else "(Enfoque más tradicional)"}

🎯 **Características Distintivas:**
{"Este autor destaca por su excepcional rigor lógico" if percentil_deductivo > 90
else "Este autor destaca por su creatividad extraordinaria" if percentil_creatividad > 90
else "Este autor muestra un perfil equilibrado" if 40 < percentil_deductivo < 60 and 40 < percentil_creatividad < 60
else "Este autor tiene un perfil único en la combinación de características"}

💼 **Recomendación de Uso:**
{"Consulte este autor para análisis que requieran máximo rigor lógico" if percentil_deductivo > 80
else "Consulte este autor para casos que necesiten enfoques innovadores" if percentil_creatividad > 80  
else "Este autor ofrece un enfoque balanceado para diversos tipos de casos"}
"""
        return explicacion
    
    def _obtener_otros_perfiles(self) -> List[Dict]:
        """Obtiene otros perfiles de la base de datos para comparación"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT perfil_json FROM perfiles_autorales LIMIT 10")
            resultados = cursor.fetchall()
            
            perfiles = []
            for resultado in resultados:
                try:
                    perfil = json.loads(resultado[0])
                    perfiles.append(perfil)
                except json.JSONDecodeError:
                    continue
            
            conn.close()
            return perfiles
            
        except Exception as e:
            print(f"⚠️ Error obteniendo perfiles para comparación: {e}")
            return []
    
    def generar_explicacion_completa(self, perfil: Dict, autor: str) -> Dict[str, str]:
        """Genera explicación completa de un perfil autoral"""
        print(f"💡 Generando explicaciones para: {autor}")
        
        explicaciones = {
            "razonamiento": self.generar_explicacion_razonamiento(perfil),
            "estilo": self.generar_explicacion_estilo(perfil), 
            "metodologia": self.generar_explicacion_metodologica(perfil),
            "comparativa": self.generar_explicacion_comparativa(perfil)
        }
        
        # Resumen ejecutivo
        explicaciones["resumen"] = f"""
👤 **PERFIL COGNITIVO DE {autor.upper()}**

🎯 **En Síntesis:**
Este autor presenta un perfil intelectual caracterizado por 
{self._generar_resumen_ejecutivo(perfil)}.

🔍 **Aplicación Práctica:**
Consulte este autor cuando necesite 
{self._generar_recomendacion_uso(perfil)}.

📈 **Nivel de Confianza del Análisis:** 
{self._calcular_confianza(perfil):.1%}
"""
        
        return explicaciones
    
    def _generar_resumen_ejecutivo(self, perfil: Dict) -> str:
        """Genera resumen ejecutivo del perfil"""
        razonamiento = perfil.get('cognicion', {}).get('razonamiento_formal', {})
        patron_dominante = max(razonamiento.items(), key=lambda x: x[1])[0] if razonamiento else "equilibrado"
        
        formalismo = perfil.get('estilo', {}).get('formalismo_juridico', 0)
        creatividad = perfil.get('cognicion', {}).get('creatividad', {}).get('originalidad_conceptual', 0)
        
        if formalismo > 0.7:
            return f"razonamiento {patron_dominante} altamente formalista"
        elif creatividad > 0.7:
            return f"razonamiento {patron_dominante} altamente creativo"
        else:
            return f"razonamiento {patron_dominante} equilibrado"
    
    def _generar_recomendacion_uso(self, perfil: Dict) -> str:
        """Genera recomendación de cuándo usar este autor"""
        razonamiento = perfil.get('cognicion', {}).get('razonamiento_formal', {})
        patron_dominante = max(razonamiento.items(), key=lambda x: x[1])[0] if razonamiento else "equilibrado"
        
        recomendaciones = {
            "deductivo": "análisis lógicos rigurosos y construcción de argumentos estructurados",
            "inductivo": "generalización desde casos específicos y identificación de patrones",
            "analogico": "comparación entre situaciones similares y transferencia de soluciones",
            "teleologico": "análisis de propósitos normativos y interpretación finalista",
            "sistemico": "integración de elementos dispersos en marcos coherentes"
        }
        
        return recomendaciones.get(patron_dominante, "análisis jurídicos integrales")
    
    def _calcular_confianza(self, perfil: Dict) -> float:
        """Calcula nivel de confianza del análisis basado en datos disponibles"""
        # Verificar completitud del perfil
        campos_principales = [
            'cognicion.razonamiento_formal',
            'estilo.formalismo_juridico', 
            'metodologia.uso_precedentes'
        ]
        
        completitud = 0
        for campo in campos_principales:
            keys = campo.split('.')
            valor = perfil
            try:
                for key in keys:
                    valor = valor[key]
                if isinstance(valor, dict) and valor:
                    completitud += 1
                elif isinstance(valor, (int, float)) and valor > 0:
                    completitud += 1
            except (KeyError, TypeError):
                continue
        
        return completitud / len(campos_principales)

def main():
    """Función de prueba"""
    print("💡 GENERADOR DE EXPLICACIONES COGNITIVAS v1.0")
    
    generador = GeneradorExplicacionesCognitivas()
    
    # Perfil de prueba
    perfil_prueba = {
        "cognicion": {
            "razonamiento_formal": {
                "deductivo": 0.8,
                "inductivo": 0.3,
                "analogico": 0.6
            },
            "creatividad": {
                "originalidad_conceptual": 0.7
            }
        },
        "estilo": {
            "formalismo_juridico": 0.6,
            "complejidad_conceptual": 0.8
        },
        "metodologia": {
            "uso_precedentes": 0.9,
            "flexibilidad_interpretativa": 0.4
        }
    }
    
    explicaciones = generador.generar_explicacion_completa(perfil_prueba, "Autor de Prueba")
    
    for tipo, explicacion in explicaciones.items():
        print(f"\n{tipo.upper()}:")
        print(explicacion)

if __name__ == "__main__":
    main()