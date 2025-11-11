#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 MOTOR MEJORADO ANALYSER MÉTODO v2.0
=====================================

IMPLEMENTA MEJORAS INTEGRALES:
- Esquema JSON unificado (perfil_autoral.json)
- Taxonomía ampliada (14 tipos de razonamiento)
- Patrones regex avanzados
- Detección de estructuras argumentativas
- Análisis de dogmas, valores y sesgos
- Compatible con sistema existente

AUTOR: Sistema Cognitivo v5.0 - Mejoras Integrales
FECHA: 9 NOV 2025
"""

import os
import re
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import math
from validador_contexto_retorica import ValidadorContextoRetorica

# PATRONES EXPANDIDOS PARA ANÁLISIS PROFUNDO
RAZONAMIENTO_PATTERNS = {
    "deductivo": r"\b(por tanto|en consecuencia|se concluye|se sigue|de( ahí| allí) que)\b",
    "inductivo": r"\b(en general|por lo común|habitualmente|frecuentemente|muestras|patrones)\b",
    "abductivo": r"\b(la mejor explicación|explicaría|hipótesis plausible|inferencia a la mejor explicación)\b",
    "analogico": r"\b(similar|semejante|como|análogamente|por analogía)\b",
    "teleologico": r"\b(finalidad|propósito|objetivo|fin|meta)\b",
    "sistemico": r"\b(coherente|articulado|integrado|sistemático|holístico|subsistemas)\b",
    "autoritativo": r"\b(doctrina (establece|dice)|jurisprudencia|precedente|fallos:?)\b",
    "a_contrario": r"\b(a contrario|por el contrario|inversamente|contrario sensu)\b",
    "consecuencialista": r"\b(consecuencias|efectos|resultados|impacto|externalidades)\b",
    "dialectico": r"\b(tesis|antítesis|síntesis|contraargumento|réplica|objección)\b",
    "hermeneutico": r"\b(interpretación|sentido|contexto|hermen[eé]utica|telos|ratio)\b",
    "historico": r"\b(históricamente|evolución|contexto histórico|precedentes cronológicos)\b",
    "economico_analitico": r"\b(costos?|beneficios?|eficiencia|incentivos|trade-?off|óptimo)\b",
    "reduccion_al_absurdo": r"\b(suponiendo que|si se admitiera que.*(absurdo|contradicción))\b"
}

MODALIDAD_EPISTEMICA_PATTERNS = {
    "apodictico": r"\b(indudable|inequívoco|concluyente|necesario|demostrable)\b",
    "dialectico": r"\b(probable|verosímil|opinable|controvertido|discutible)\b",
    "retorico": r"\b(persuasión|audiencia|verosimilitud|credibilidad|convincente)\b",
    "sofistico": r"\b(aparentemente|truco argumental|equivocación|falacia)\b",
    "certeza": r"\b(indudable|inequívoco|concluyente|necesario|cierto)\b",
    "incertidumbre_explorada": r"\b(incertidumbre|ambigüedad|no concluyente|limitado)\b",
    "hedging": r"\b(probablemente|posiblemente|podría|parece|sugiere|eventual)\b"
}

RETORICA_PATTERNS = {
    "ethos": r"\b(según|conforme|establece la doctrina|jurisprudencia|autoridades? en la materia)\b",
    "pathos": r"\b(injusto|grave|alarmante|indignante|necesario|urgente|desproporcionado)\b",
    "logos": r"\b(porque|dado que|puesto que|en virtud de|la razón|por razones)\b"
}

ESTILOS_LITERARIOS = {
    "tecnico_juridico": [r"\b(art\.?|arts\.?|ley\s?\d+|decreto|fallos:|fs\.)\b", r"\b(v.gr\.|cfr\.)\b"],
    "ensayistico": [r"\b(pienso|considero|propongo|ensayo)\b", r"[;:—]\s"],
    "narrativo": [r"\b(primero|luego|entonces|finalmente)\b", r"\b(relata|narra)\b"],
    "barroco": [r"(,){3,}", r"\((?:[^()]+|\([^()]*\))*\)"],  # oraciones muy anidadas
    "minimalista": [r"\.\s+[A-ZÁÉÍÓÚÑ]"],  # frases cortas repetidas
    "aforistico": [r"\"[^\"]{5,120}\"", r"\b(aforismo|máxima)\b"],
    "impersonal_burocratico": [r"\b(se|queda|hágase|cítese|notifíquese)\b", r"\b(que se provea|tómese razón)\b"],
    "dialectico_critico": [r"\b(crítica|antinomia|paradoja|aporía)\b"]
}

FALACIAS_HINTS = {
    "ad_hominem": r"\b(ignorante|incompetente|malicioso)\b",
    "ad_populum": r"\b(todo el mundo|es sabido que|la mayoría)\b",
    "petitio_principii": r"\b(como es evidente que|resulta obvio que)\b",
    "falsa_analogia": r"\b(como.*también.*entonces)\b",
    "falso_dilema": r"\b(o bien.*|no hay alternativa)\b",
    "slippery_slope": r"\b(inevitablemente|irremediablemente)\b"
}

AXIOMAS = {
    "principio_protectorio": r"\b(protectorio|pro operario|in dubio pro operario)\b",
    "autonomia_voluntad_limitada": r"\b(límites|orden público|buenas costumbres|abuso del derecho)\b",
    "razonabilidad": r"\b(razonable|proporcionalidad|idoneidad|necesidad)\b",
    "seguridad_juridica": r"\b(seguridad jur[ií]dica|previsibilidad|confianza)\b"
}

SESGOS_VALORATIVOS = {
    "pro_trabajador": r"\b(trabajador|asalariado|protección laboral)\b",
    "pro_empresario": r"\b(competitividad|inversión|productividad|eficiencia)\b",
    "pro_consumidor": r"\b(consumidor|hipervulnerable|relación de consumo)\b",
    "garantista": r"\b(garantías|debido proceso|tutela judicial efectiva)\b",
    "punitivista": r"\b(sanción ejemplar|multas severas|tolerancia cero)\b",
    "liberal": r"\b(libertad contractual|minima intervención estatal)\b",
    "utilitarista": r"\b(bienestar general|eficiencia social|maximización del beneficio)\b"
}

FUENTES = {
    "jurisprudencia": r"\b(Fallos:|CSJN|SCBA|TSJ|Cámara|Sala|Expte\.?)\b",
    "doctrina": r"\b(opina|sostiene|doctrina|tratadista|autor)\b",
    "ley": r"\b(ley\s?\d+|art(?:s?)\.?\s?\d+)\b",
    "principios": r"\b(principio|proporcionalidad|razonabilidad|equidad)\b",
    "politicas_publicas": r"\b(política pública|impacto regulatorio|análisis económico)\b",
    "evidencia_empirica": r"\b(estadístic|datos|encuesta|muestra|regresión|dataset)\b"
}

class AnalyserMetodoMejorado:
    """Motor ANALYSER MÉTODO mejorado con taxonomía expandida"""
    
    def __init__(self):
        self.version = "v2.0_mejorado"
        
    def score_pattern(self, text: str, pattern: str) -> float:
        """Scoring rápido por conteos normalizados"""
        matches = re.findall(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        return min(1.0, len(matches) / max(1, len(text) // 800))
    
    def score_group(self, text: str, patterns_dict: Dict[str, str]) -> Dict[str, float]:
        """Score múltiples patrones"""
        return {k: self.score_pattern(text, p) for k, p in patterns_dict.items()}
    
    def score_style_group(self, text: str, patterns_list: List[str]) -> float:
        """Score grupo de estilos (lista de subpatrones)"""
        total_score = 0.0
        for pattern in patterns_list:
            total_score += self.score_pattern(text, pattern)
        return min(1.0, total_score / max(1, len(patterns_list)))
    
    def detectar_estructuras_argumentativas(self, text: str) -> Dict[str, float]:
        """Detección de estructuras argumentativas heurística"""
        estructuras = {}
        
        # IRAC (Issue, Rule, Application, Conclusion)
        estructuras["IRAC"] = 1.0 if re.search(
            r"(issue|cuestión).*(regla|norma).*(aplicación|análisis).*(conclusión)", 
            text, re.I | re.S
        ) else 0.0
        
        # Toulmin (Claim, Warrant, Backing)
        estructuras["Toulmin"] = 1.0 if re.search(
            r"(reclamo|pretensión).*(fundamento|garantía).*(respaldo|backing)", 
            text, re.I | re.S
        ) else 0.0
        
        # Issue Tree
        estructuras["Issue_Tree"] = 1.0 if re.search(
            r"(subproblema|subcuestión|desglose)", text, re.I
        ) else 0.0
        
        # Defeasible reasoning
        estructuras["Defeasible"] = 1.0 if re.search(
            r"(salvo|a menos que|excepto si)", text, re.I
        ) else 0.0
        
        # Burden Shift
        estructuras["Burden_Shift"] = 1.0 if re.search(
            r"(carga de la prueba|onus probandi|corresponde demostrar)", text, re.I
        ) else 0.0
        
        # Silogístico Formal
        estructuras["Silogistico_Formal"] = 1.0 if re.search(
            r"\b(Todo .* es .*)\b.*\b(Todo .* es .*)\b.*\b(Por tanto|Luego)\b.*", 
            text, re.I | re.S
        ) else 0.0
        
        return estructuras
    
    def detectar_falacias(self, text: str) -> List[str]:
        """Detecta falacias probables"""
        falacias_detectadas = []
        
        for falacia, pattern in FALACIAS_HINTS.items():
            if self.score_pattern(text, pattern) > 0.1:
                falacias_detectadas.append(falacia)
        
        return falacias_detectadas
    
    def extraer_dogmas_y_valores(self, text: str) -> Dict[str, Any]:
        """Extrae axiomas del autor, creencias y sesgos valorativos"""
        
        # Axiomas detectados
        axiomas_detectados = []
        for axioma, pattern in AXIOMAS.items():
            if self.score_pattern(text, pattern) > 0.1:
                axiomas_detectados.append(axioma)
        
        # Creencias explícitas (heurística)
        creencias = []
        matches_creencias = re.findall(
            r"\b(creo que|considero que|estoy convencido que|es evidente que) ([^.]{10,100})\.", 
            text, re.I
        )
        creencias = [match[1].strip() for match in matches_creencias[:3]]
        
        # Sesgos valorativos
        sesgos = self.score_group(text, SESGOS_VALORATIVOS)
        
        return {
            "axiomas_autor": axiomas_detectados,
            "creencias_explicitas": creencias,
            "sesgos_valorativos": sesgos
        }
    
    def extraer_puntos_apoyo(self, text: str) -> Dict[str, Any]:
        """Extrae fuentes y puntos de apoyo del argumento"""
        
        intensidades = self.score_group(text, FUENTES)
        fuentes_principales = [k for k, v in intensidades.items() if v > 0.1]
        
        return {
            "fuentes": fuentes_principales,
            "intensidad_fuentes": intensidades
        }
    
    def extraer_dilemas_y_limites(self, text: str) -> Dict[str, Any]:
        """Extrae dilemas explicitados y limitaciones reconocidas"""
        
        # Dilemas (patrón A vs B)
        dilemas = re.findall(r"\b(\w+)\s+vs\.?\s+(\w+)\b", text, re.I)
        dilemas_str = [f"{a}_vs_{b}" for a, b in dilemas]
        
        # Limitaciones reconocidas
        limitaciones_matches = re.findall(
            r"\b(limitación|límite|sesgo|parcialidad|datos incompletos|no concluyente) ([^.]{5,80})\.", 
            text, re.I
        )
        limitaciones = [match[1].strip() for match in limitaciones_matches[:3]]
        
        # Áreas de ambigüedad
        ambiguedad_matches = re.findall(
            r"\b(ambigüedad|imprecisión|zona gris|territorio inexplorado) ([^.]{5,80})\.", 
            text, re.I
        )
        ambiguedades = [match[1].strip() for match in ambiguedad_matches[:3]]
        
        return {
            "dilemas_explicitados": dilemas_str,
            "limitaciones_reconocidas": limitaciones,
            "areas_de_ambiguedad": ambiguedades
        }
    
    def calcular_marcadores_cognitivos(self, text: str) -> Dict[str, float]:
        """Calcula marcadores cognitivos expandidos"""
        
        return {
            "nivel_abstraccion": min(1.0, len(re.findall(r"\b(principio|cláusula general|ratio)\b", text, re.I)) / 5),
            "complejidad_sintactica": min(1.0, sum(1 for _ in re.finditer(r",", text)) / max(1, len(text) // 500)),
            "interdisciplinariedad": self.score_pattern(text, r"\b(económico|sociológico|filosófico|psicológico)\b"),
            "empirismo": self.score_pattern(text, r"\b(datos|muestra|estadístic|evidencia)\b"),
            "dogmatismo": self.score_pattern(text, r"\b(indudable|inequívoco|sin lugar a dudas)\b"),
            "creatividad": self.score_pattern(text, r"\b(propongo|novedoso|innovador|reinterpretación)\b"),
            "uso_jurisprudencia": self.score_pattern(text, r"(Fallos:|Cám\.|TSJ|SCBA|CSJN|Expte\.?)"),
            "coherencia_global": 0.5  # placeholder - se puede mejorar con análisis de conectores
        }
    
    def generar_perfil_autoral_completo(self, texto: str, autor: str = None, fuente: str = None) -> Dict[str, Any]:
        """Genera perfil autoral completo según esquema JSON unificado"""
        
        print(f"🧠 Generando perfil autoral completo para: {autor or 'Autor desconocido'}")
        
        # Análisis de estilos literarios
        estilos_scores = {}
        for estilo, patterns in ESTILOS_LITERARIOS.items():
            estilos_scores[estilo] = self.score_style_group(texto, patterns)
        
        # Perfil completo según esquema unificado
        perfil_autoral = {
            "meta": {
                "autor_probable": autor,
                "fuente": fuente or "texto_directo",
                "timestamp": datetime.now().isoformat(),
                "version_analyser": self.version
            },
            "cognicion": {
                "razonamiento_formal": self.score_group(texto, RAZONAMIENTO_PATTERNS),
                "modalidad_epistemica": self.score_group(texto, MODALIDAD_EPISTEMICA_PATTERNS),
                "retorica": {
                    **self.score_group(texto, RETORICA_PATTERNS),
                    "falacias_probables": self.detectar_falacias(texto)
                },
                "estilo_literario": estilos_scores,
                "estructuras_argumentativas": self.detectar_estructuras_argumentativas(texto)
            },
            "dogmas_y_valores": self.extraer_dogmas_y_valores(texto),
            "puntos_de_apoyo": self.extraer_puntos_apoyo(texto),
            "dilemas_y_limites": self.extraer_dilemas_y_limites(texto),
            "marcadores_cognitivos": self.calcular_marcadores_cognitivos(texto)
        }
        
        return perfil_autoral
    
    def generar_prompt_mejorado(self, chunk: str) -> str:
        """Genera prompt enriquecido para LLM externo"""
        
        return f"""
Eres METODÓLOGO JURÍDICO y ANALISTA COGNITIVO. Describe CÓMO PIENSA el autor (no qué dice).
Devuelve SOLO JSON con el esquema 'perfil_autoral.json'.

Evalúa:
1) Razonamiento formal (deductivo, inductivo, abductivo, analógico, teleológico, sistémico, autoritativo, a contrario, consecuencialista, dialéctico, hermenéutico, histórico, económico-analítico, reducción al absurdo).
2) Modalidad epistémica (apodíctico, dialéctico, retórico, sofístico, certeza, incertidumbre explorada, hedging).
3) Retórica (ethos, pathos, logos, falacias probables).
4) Estilo literario (técnico-jurídico, ensayístico, narrativo, barroco, minimalista, aforístico, impersonal-burocrático, dialéctico-crítico).
5) Estructuras argumentativas (IRAC, Toulmin, Issue Tree, Defeasible, Burden Shift, Silogístico Formal).
6) Dogmas y valores (axiomas, creencias, sesgos valorativos).
7) Puntos de apoyo (jurisprudencia, doctrina, ley, principios, políticas públicas, evidencia empírica).
8) Dilemas y límites (dilemas explicitados, limitaciones reconocidas, áreas de ambigüedad).
9) Marcadores cognitivos (nivel de abstracción, complejidad sintáctica, interdisciplinariedad, empirismo, dogmatismo, creatividad, uso de jurisprudencia, coherencia global).

Texto:
{chunk}
"""
    
    def guardar_perfil_en_db(self, perfil: Dict[str, Any], db_path: str = "colaborative/bases_rag/cognitiva/perfiles_autorales.db"):
        """Guarda perfil en base de datos"""
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS perfiles_autorales_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT,
                fuente TEXT,
                perfil_json TEXT,
                razonamiento_dominante TEXT,
                estilo_dominante TEXT,
                modalidad_dominante TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                version TEXT
            )
        ''')
        
        # Extraer elementos principales para indexación
        razonamiento_scores = perfil['cognicion']['razonamiento_formal']
        razonamiento_dominante = max(razonamiento_scores.items(), key=lambda x: x[1])[0]
        
        estilo_scores = perfil['cognicion']['estilo_literario']
        estilo_dominante = max(estilo_scores.items(), key=lambda x: x[1])[0]
        
        modalidad_scores = perfil['cognicion']['modalidad_epistemica']
        modalidad_dominante = max(modalidad_scores.items(), key=lambda x: x[1])[0]
        
        # Insertar perfil
        cursor.execute('''
            INSERT INTO perfiles_autorales_v2 
            (autor, fuente, perfil_json, razonamiento_dominante, estilo_dominante, modalidad_dominante, version)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            perfil['meta']['autor_probable'],
            perfil['meta']['fuente'],
            json.dumps(perfil, ensure_ascii=False),
            razonamiento_dominante,
            estilo_dominante,
            modalidad_dominante,
            perfil['meta']['version_analyser']
        ))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Perfil guardado: {perfil['meta']['autor_probable']} - {razonamiento_dominante}")


    def procesar_texto_completo(self, texto: str, metadatos: Dict = None) -> Dict:
        """
        ⭐ MÉTODO PRINCIPAL - Procesa texto completo y genera perfil autoral
        
        Args:
            texto: Texto a analizar
            metadatos: Información adicional del documento
            
        Returns:
            Dict: Perfil autoral completo con 40+ dimensiones
        """
        return self.generar_perfil_autoral_completo(texto, metadatos)

def main():
    """Función principal para probar el motor mejorado"""
    
    print("🚀 INICIANDO ANALYSER MÉTODO MEJORADO v2.0")
    
    analyser = AnalyserMetodoMejorado()
    
    # Texto de ejemplo para prueba
    texto_ejemplo = """
    En primer lugar, debemos analizar sistemáticamente los elementos que configuran 
    esta figura jurídica. La doctrina establece claramente que no puede haber 
    ambigüedad en la interpretación. Por tanto, se sigue necesariamente que 
    la única opción viable es aplicar el criterio restrictivo.
    
    Como sostiene la jurisprudencia de la Corte Suprema, el principio protectorio
    debe ser interpretado en función de la finalidad social que persigue. Sin embargo,
    reconozco que los datos disponibles son limitados y que existe una zona gris
    en la aplicación práctica de esta norma.
    """
    
    # Generar perfil completo
    perfil = analyser.generar_perfil_autoral_completo(texto_ejemplo, "Autor de Prueba")
    
    print("\n🧠 PERFIL AUTORAL GENERADO:")
    print(json.dumps(perfil, indent=2, ensure_ascii=False))
    
    # Guardar en base de datos
    analyser.guardar_perfil_en_db(perfil)
    
    print("\n✅ Prueba completada exitosamente")

def detectar_ethos_pathos_logos(texto: str) -> dict:
    """Detección contextual ponderada de ETHOS, PATHOS, LOGOS"""
    v = ValidadorContextoRetorica()
    ethos = v.analizar_ethos(texto)
    pathos = v.analizar_pathos(texto)
    logos = v.analizar_logos(texto)

    return {
        "ethos": len(ethos),
        "pathos": len(pathos),
        "logos": len(logos),
        "ponderacion_ethos": sum(e.confianza for e in ethos) / (len(ethos) or 1),
        "ponderacion_pathos": sum(p.confianza for p in pathos) / (len(pathos) or 1),
        "ponderacion_logos": sum(l.confianza for l in logos) / (len(logos) or 1),
    }

if __name__ == "__main__":
    main()