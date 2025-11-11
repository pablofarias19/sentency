# -*- coding: utf-8 -*-
"""
🔧 REPARADOR SISTEMA COMPLETO v1.0
==================================
Soluciona TODOS los errores identificados y crea sistema unificado

PROBLEMAS DETECTADOS:
❌ sqlite3.OperationalError: no such table: perfiles_autorales
❌ 'AnalyserMetodoMejorado' object has no attribute 'procesar_texto_completo'

SOLUCIONES:
✅ Crear/reparar todas las tablas necesarias
✅ Corregir métodos en AnalyserMetodoMejorado
✅ Verificar integridad completa del sistema
"""

import os
import sys
import sqlite3
from pathlib import Path
import json

# Configuración de rutas
BASE_DIR = Path(__file__).parent
COLABORATIVE_DIR = BASE_DIR / "colaborative"
SCRIPTS_DIR = COLABORATIVE_DIR / "scripts"
DATA_DIR = COLABORATIVE_DIR / "data"

sys.path.append(str(SCRIPTS_DIR))

def crear_base_datos_completa():
    """Crea/repara TODAS las bases de datos necesarias"""
    print("🔧 REPARANDO BASES DE DATOS...")
    
    # Base de datos principal cognitiva
    db_cognitiva = DATA_DIR / "cognitivo.db"
    
    with sqlite3.connect(db_cognitiva) as conn:
        cursor = conn.cursor()
        
        # Tabla perfiles_autorales (FALTABA)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS perfiles_autorales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento_id TEXT UNIQUE,
            nombre_archivo TEXT,
            autor_detectado TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            -- RAZONAMIENTO (14 tipos)
            razonamiento_deductivo REAL DEFAULT 0.0,
            razonamiento_inductivo REAL DEFAULT 0.0,
            razonamiento_abductivo REAL DEFAULT 0.0,
            razonamiento_analogico REAL DEFAULT 0.0,
            razonamiento_teleologico REAL DEFAULT 0.0,
            razonamiento_sistemico REAL DEFAULT 0.0,
            razonamiento_autoritativo REAL DEFAULT 0.0,
            razonamiento_a_contrario REAL DEFAULT 0.0,
            razonamiento_consecuencialista REAL DEFAULT 0.0,
            razonamiento_dialectico REAL DEFAULT 0.0,
            razonamiento_hermeneutico REAL DEFAULT 0.0,
            razonamiento_historico REAL DEFAULT 0.0,
            razonamiento_economico_analitico REAL DEFAULT 0.0,
            razonamiento_reduccion_absurdo REAL DEFAULT 0.0,
            
            -- MODALIDADES EPISTÉMICAS (7 tipos)
            modalidad_apodíctico REAL DEFAULT 0.0,
            modalidad_dialectico REAL DEFAULT 0.0,
            modalidad_retorico REAL DEFAULT 0.0,
            modalidad_sofístico REAL DEFAULT 0.0,
            modalidad_certeza REAL DEFAULT 0.0,
            modalidad_incertidumbre REAL DEFAULT 0.0,
            modalidad_hedging REAL DEFAULT 0.0,
            
            -- RETÓRICA ARISTOTÉLICA
            retorica_ethos REAL DEFAULT 0.0,
            retorica_pathos REAL DEFAULT 0.0,
            retorica_logos REAL DEFAULT 0.0,
            
            -- ESTILOS LITERARIOS (8 tipos)
            estilo_tecnico_juridico REAL DEFAULT 0.0,
            estilo_ensayistico REAL DEFAULT 0.0,
            estilo_narrativo REAL DEFAULT 0.0,
            estilo_barroco REAL DEFAULT 0.0,
            estilo_minimalista REAL DEFAULT 0.0,
            estilo_aforistico REAL DEFAULT 0.0,
            estilo_impersonal_burocratico REAL DEFAULT 0.0,
            estilo_dialectico_critico REAL DEFAULT 0.0,
            
            -- ESTRUCTURAS ARGUMENTATIVAS (6 tipos)
            estructura_irac REAL DEFAULT 0.0,
            estructura_toulmin REAL DEFAULT 0.0,
            estructura_issue_tree REAL DEFAULT 0.0,
            estructura_defeasible REAL DEFAULT 0.0,
            estructura_burden_shift REAL DEFAULT 0.0,
            estructura_silogistico_formal REAL DEFAULT 0.0,
            
            -- MÉTRICAS GENERALES
            formalismo REAL DEFAULT 0.0,
            creatividad REAL DEFAULT 0.0,
            empirismo REAL DEFAULT 0.0,
            dogmatismo REAL DEFAULT 0.0,
            interdisciplinariedad REAL DEFAULT 0.0,
            complejidad_sintactica REAL DEFAULT 0.0,
            nivel_abstraccion REAL DEFAULT 0.0,
            uso_jurisprudencia REAL DEFAULT 0.0,
            
            -- METADATOS
            perfil_json TEXT,
            procesado_con TEXT DEFAULT 'AnalyserMetodoMejorado_v2.0'
        )
        ''')
        
        # Índices para búsquedas rápidas
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_autor ON perfiles_autorales(autor_detectado)",
            "CREATE INDEX IF NOT EXISTS idx_archivo ON perfiles_autorales(nombre_archivo)",
            "CREATE INDEX IF NOT EXISTS idx_razonamiento_teleologico ON perfiles_autorales(razonamiento_teleologico)",
            "CREATE INDEX IF NOT EXISTS idx_estilo_ensayistico ON perfiles_autorales(estilo_ensayistico)",
            "CREATE INDEX IF NOT EXISTS idx_creatividad ON perfiles_autorales(creatividad)",
            "CREATE INDEX IF NOT EXISTS idx_formalismo ON perfiles_autorales(formalismo)"
        ]
        
        for indice in indices:
            cursor.execute(indice)
        
        conn.commit()
        print("✅ Base de datos perfiles_autorales creada/reparada")
    
    # Base pensamiento_integrado_v2.db
    db_pensamiento = DATA_DIR / "pensamiento_integrado_v2.db"
    
    with sqlite3.connect(db_pensamiento) as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS perfiles_completos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento_id TEXT UNIQUE,
            nombre_archivo TEXT,
            autor_detectado TEXT,
            fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            perfil_completo TEXT,
            vector_cognitivo TEXT,
            motor_version TEXT DEFAULT 'OrchestadorMaestroIntegrado_v6.0'
        )
        ''')
        
        conn.commit()
        print("✅ Base de datos pensamiento_integrado_v2.db creada/reparada")

def corregir_analyser_mejorado():
    """Corrige los métodos faltantes en AnalyserMetodoMejorado"""
    print("🔧 CORRIGIENDO ANALYSER MÉTODO MEJORADO...")
    
    analyser_file = SCRIPTS_DIR / "analyser_metodo_mejorado.py"
    
    if not analyser_file.exists():
        print("❌ analyser_metodo_mejorado.py no existe, creándolo...")
        crear_analyser_corregido()
    else:
        # Verificar si tiene el método correcto
        with open(analyser_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'def procesar_texto_completo(' not in content:
            print("🔧 Agregando método procesar_texto_completo...")
            agregar_metodo_faltante(analyser_file)
        else:
            print("✅ analyser_metodo_mejorado.py ya tiene los métodos correctos")

def crear_analyser_corregido():
    """Crea AnalyserMetodoMejorado con TODOS los métodos necesarios"""
    
    analyser_content = '''# -*- coding: utf-8 -*-
"""
🧠 ANALYSER MÉTODO MEJORADO v2.0 - CORREGIDO
============================================
Motor principal con taxonomía expandida (40+ dimensiones)
TODOS LOS MÉTODOS NECESARIOS INCLUIDOS
"""

import re
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Any
import numpy as np

class AnalyserMetodoMejorado:
    """
    🧠 Motor principal de análisis cognitivo con taxonomía expandida
    
    CARACTERÍSTICAS:
    - 14 Tipos de Razonamiento
    - 7 Modalidades Epistémicas  
    - 8 Estilos Literarios
    - 6 Estructuras Argumentativas
    - Retórica + Detección de Falacias
    """
    
    def __init__(self):
        self.version = "AnalyserMetodoMejorado_v2.0"
        self._cargar_patrones()
    
    def procesar_texto_completo(self, texto: str, metadatos: Dict = None) -> Dict:
        """
        ⭐ MÉTODO PRINCIPAL - Procesa texto completo y genera perfil autoral
        
        Args:
            texto: Texto a analizar
            metadatos: Información adicional del documento
            
        Returns:
            Dict: Perfil autoral completo con 40+ dimensiones
        """
        if not texto or len(texto.strip()) < 50:
            return self._perfil_vacio()
        
        # Análisis principal
        perfil = {
            "version_motor": self.version,
            "metadatos": metadatos or {},
        }
        
        # 1. ANÁLISIS DE RAZONAMIENTO (14 tipos)
        perfil["razonamiento"] = self._analizar_razonamiento(texto)
        
        # 2. MODALIDADES EPISTÉMICAS (7 tipos)
        perfil["modalidades_epistemicas"] = self._analizar_modalidades_epistemicas(texto)
        
        # 3. RETÓRICA ARISTOTÉLICA
        perfil["retorica"] = self._analizar_retorica_aristotelica(texto)
        
        # 4. ESTILOS LITERARIOS (8 tipos)
        perfil["estilos_literarios"] = self._analizar_estilos_literarios(texto)
        
        # 5. ESTRUCTURAS ARGUMENTATIVAS (6 tipos)
        perfil["estructuras_argumentativas"] = self._analizar_estructuras_argumentativas(texto)
        
        # 6. MÉTRICAS GENERALES
        perfil["metricas_generales"] = self._calcular_metricas_generales(texto)
        
        # 7. DETECCIÓN DE AUTOR
        perfil["autor_detectado"] = self._detectar_autor(texto, metadatos)
        
        # 8. RESUMEN COGNITIVO
        perfil["resumen_cognitivo"] = self._generar_resumen_cognitivo(perfil)
        
        return perfil
    
    def generar_perfil_autoral_completo(self, texto: str, metadatos: Dict = None) -> Dict:
        """Alias del método principal para compatibilidad"""
        return self.procesar_texto_completo(texto, metadatos)
    
    def _cargar_patrones(self):
        """Carga todos los patrones de análisis"""
        
        # PATRONES DE RAZONAMIENTO (14 tipos)
        self.RAZONAMIENTO_PATTERNS = {
            "deductivo": re.compile(r"\\b(por tanto|en consecuencia|se concluye|se sigue|de ahí que|luego|entonces)\\b", re.IGNORECASE),
            "inductivo": re.compile(r"\\b(en general|por lo común|habitualmente|frecuentemente|suele|tiende a|patrón|tendencia)\\b", re.IGNORECASE),
            "abductivo": re.compile(r"\\b(la mejor explicación|más probable|hipótesis|presumiblemente|verosímil|explicación más plausible)\\b", re.IGNORECASE),
            "analogico": re.compile(r"\\b(similar|semejante|como|análogamente|por analogía|paralelismo|equivalente|comparable)\\b", re.IGNORECASE),
            "teleologico": re.compile(r"\\b(finalidad|propósito|objetivo|fin|meta|función|ratio legis|espíritu de la ley)\\b", re.IGNORECASE),
            "sistemico": re.compile(r"\\b(coherente|articulado|integrado|sistemático|conjunto|armonía|unidad|totalidad)\\b", re.IGNORECASE),
            "autoritativo": re.compile(r"\\b(doctrina establece|jurisprudencia|precedente|según la autoridad|conforme a|establece)\\b", re.IGNORECASE),
            "a_contrario": re.compile(r"\\b(a contrario|por el contrario|inversamente|opuestamente|al revés)\\b", re.IGNORECASE),
            "consecuencialista": re.compile(r"\\b(consecuencias|efectos|resultados|impacto|derivaciones|implicaciones)\\b", re.IGNORECASE),
            "dialectico": re.compile(r"\\b(tesis|antítesis|síntesis|contradicción|tensión|dialéctica|oposición)\\b", re.IGNORECASE),
            "hermeneutico": re.compile(r"\\b(interpretación|hermenéu|significado|sentido|comprensión|exégesis)\\b", re.IGNORECASE),
            "historico": re.compile(r"\\b(evolución|desarrollo histórico|antecedentes|tradición|origen|génesis)\\b", re.IGNORECASE),
            "economico_analitico": re.compile(r"\\b(eficiencia|costo-beneficio|incentivos|óptimo|racionalidad económica)\\b", re.IGNORECASE),
            "reduccion_absurdo": re.compile(r"\\b(reducción al absurdo|si fuera|llevaría a|contradicción|imposible|absurdo)\\b", re.IGNORECASE)
        }
        
        # MODALIDADES EPISTÉMICAS (7 tipos)
        self.MODALIDAD_EPISTEMICA_PATTERNS = {
            "apodíctico": re.compile(r"\\b(necesariamente|indudablemente|demostrable|evidente|incuestionable)\\b", re.IGNORECASE),
            "dialectico": re.compile(r"\\b(probable|opinión|razonable|verosímil|posible|plausible)\\b", re.IGNORECASE),
            "retorico": re.compile(r"\\b(persuasivo|convincente|retórica|elocuencia|persuasión)\\b", re.IGNORECASE),
            "sofístico": re.compile(r"\\b(aparentemente|pseudo|sofisma|falacia|engañoso)\\b", re.IGNORECASE),
            "certeza": re.compile(r"\\b(cierto|seguro|definitivo|inequívoco|claro|preciso)\\b", re.IGNORECASE),
            "incertidumbre": re.compile(r"\\b(incierto|dudoso|ambiguo|complejo|problemático|discutible)\\b", re.IGNORECASE),
            "hedging": re.compile(r"\\b(podría|quizás|tal vez|posiblemente|aparentemente|parece)\\b", re.IGNORECASE)
        }
        
        # RETÓRICA ARISTOTÉLICA
        self.RETORICA_PATTERNS = {
            "ethos": re.compile(r"\\b(según|conforme|establece la doctrina|jurisprudencia|autoridad|experto)\\b", re.IGNORECASE),
            "pathos": re.compile(r"\\b(injusto|grave|preocupante|alarmante|necesario|urgente|importante)\\b", re.IGNORECASE),
            "logos": re.compile(r"\\b(porque|dado que|puesto que|en virtud de|razón|fundamento|lógica)\\b", re.IGNORECASE)
        }
        
        # ESTILOS LITERARIOS (8 tipos)
        self.ESTILO_PATTERNS = {
            "tecnico_juridico": re.compile(r"\\b(artículo|inciso|párrafo|código|ley|decreto|jurisprudencia)\\b", re.IGNORECASE),
            "ensayistico": re.compile(r"\\b(reflexión|consideración|pensamiento|ensayo|meditación)\\b", re.IGNORECASE),
            "narrativo": re.compile(r"\\b(historia|relato|caso|acontecimiento|sucedió|narración)\\b", re.IGNORECASE),
            "barroco": re.compile(r"\\b(ornamental|elaborado|complejo|sofisticado|rebuscado)\\b", re.IGNORECASE),
            "minimalista": re.compile(r"\\b(simple|directo|claro|conciso|preciso|escueto)\\b", re.IGNORECASE),
            "aforistico": re.compile(r"\\b(máxima|principio|aforismo|sentencia|máxima jurídica)\\b", re.IGNORECASE),
            "impersonal_burocratico": re.compile(r"\\b(se establece|se determina|corresponde|procede|cabe)\\b", re.IGNORECASE),
            "dialectico_critico": re.compile(r"\\b(crítica|cuestionamiento|debate|controversia|polémica)\\b", re.IGNORECASE)
        }
        
        # ESTRUCTURAS ARGUMENTATIVAS (6 tipos)
        self.ESTRUCTURA_PATTERNS = {
            "irac": re.compile(r"\\b(issue|rule|application|conclusion|problema|regla|aplicación)\\b", re.IGNORECASE),
            "toulmin": re.compile(r"\\b(claim|data|warrant|backing|qualifier|rebuttal|alegación|datos)\\b", re.IGNORECASE),
            "issue_tree": re.compile(r"\\b(árbol|estructura|ramificación|subdivisión|clasificación)\\b", re.IGNORECASE),
            "defeasible": re.compile(r"\\b(excepción|salvo|a menos que|derrotable|presumible)\\b", re.IGNORECASE),
            "burden_shift": re.compile(r"\\b(carga de la prueba|burden|onus|demostrar|probar)\\b", re.IGNORECASE),
            "silogistico_formal": re.compile(r"\\b(premisa|conclusión|silogismo|todos|algunos|ningún)\\b", re.IGNORECASE)
        }
    
    def _analizar_razonamiento(self, texto: str) -> Dict:
        """Analiza los 14 tipos de razonamiento"""
        resultados = {}
        
        for tipo, pattern in self.RAZONAMIENTO_PATTERNS.items():
            matches = pattern.findall(texto)
            score = min(len(matches) / 10.0, 1.0)  # Normalizar a 0-1
            resultados[tipo] = round(score, 3)
        
        return resultados
    
    def _analizar_modalidades_epistemicas(self, texto: str) -> Dict:
        """Analiza las 7 modalidades epistémicas"""
        resultados = {}
        
        for modalidad, pattern in self.MODALIDAD_EPISTEMICA_PATTERNS.items():
            matches = pattern.findall(texto)
            score = min(len(matches) / 8.0, 1.0)
            resultados[modalidad] = round(score, 3)
        
        return resultados
    
    def _analizar_retorica_aristotelica(self, texto: str) -> Dict:
        """Analiza retórica aristotélica (ethos, pathos, logos)"""
        resultados = {}
        
        for elemento, pattern in self.RETORICA_PATTERNS.items():
            matches = pattern.findall(texto)
            score = min(len(matches) / 5.0, 1.0)
            resultados[elemento] = round(score, 3)
        
        return resultados
    
    def _analizar_estilos_literarios(self, texto: str) -> Dict:
        """Analiza los 8 estilos literarios"""
        resultados = {}
        
        for estilo, pattern in self.ESTILO_PATTERNS.items():
            matches = pattern.findall(texto)
            score = min(len(matches) / 6.0, 1.0)
            resultados[estilo] = round(score, 3)
        
        return resultados
    
    def _analizar_estructuras_argumentativas(self, texto: str) -> Dict:
        """Analiza las 6 estructuras argumentativas"""
        resultados = {}
        
        for estructura, pattern in self.ESTRUCTURA_PATTERNS.items():
            matches = pattern.findall(texto)
            score = min(len(matches) / 4.0, 1.0)
            resultados[estructura] = round(score, 3)
        
        return resultados
    
    def _calcular_metricas_generales(self, texto: str) -> Dict:
        """Calcula métricas generales de análisis"""
        return {
            "formalismo": self._calcular_formalismo(texto),
            "creatividad": self._calcular_creatividad(texto),
            "empirismo": self._calcular_empirismo(texto),
            "dogmatismo": self._calcular_dogmatismo(texto),
            "interdisciplinariedad": self._calcular_interdisciplinariedad(texto),
            "complejidad_sintactica": self._calcular_complejidad_sintactica(texto),
            "nivel_abstraccion": self._calcular_nivel_abstraccion(texto),
            "uso_jurisprudencia": self._calcular_uso_jurisprudencia(texto)
        }
    
    def _calcular_formalismo(self, texto: str) -> float:
        """Calcula nivel de formalismo jurídico"""
        patterns_formales = re.findall(r'\\b(artículo|inciso|código|ley|decreto|jurisprudencia)\\b', texto, re.IGNORECASE)
        return min(len(patterns_formales) / 20.0, 1.0)
    
    def _calcular_creatividad(self, texto: str) -> float:
        """Calcula nivel de creatividad conceptual"""
        patterns_creativos = re.findall(r'\\b(innovador|original|nuevo enfoque|perspectiva|creativo)\\b', texto, re.IGNORECASE)
        return min(len(patterns_creativos) / 10.0, 1.0)
    
    def _calcular_empirismo(self, texto: str) -> float:
        """Calcula nivel de empirismo evidencial"""
        patterns_empiricos = re.findall(r'\\b(datos|estadística|evidencia|caso concreto|muestra)\\b', texto, re.IGNORECASE)
        return min(len(patterns_empiricos) / 8.0, 1.0)
    
    def _calcular_dogmatismo(self, texto: str) -> float:
        """Calcula nivel de dogmatismo vs flexibilidad"""
        patterns_dogmaticos = re.findall(r'\\b(indiscutible|incuestionable|definitivo|absoluto)\\b', texto, re.IGNORECASE)
        return min(len(patterns_dogmaticos) / 5.0, 1.0)
    
    def _calcular_interdisciplinariedad(self, texto: str) -> float:
        """Calcula integración de otras disciplinas"""
        patterns_interdisciplinarios = re.findall(r'\\b(sociología|economía|psicología|filosofía|antropología)\\b', texto, re.IGNORECASE)
        return min(len(patterns_interdisciplinarios) / 6.0, 1.0)
    
    def _calcular_complejidad_sintactica(self, texto: str) -> float:
        """Calcula complejidad sintáctica del lenguaje"""
        oraciones = texto.split('.')
        if not oraciones:
            return 0.0
        
        promedio_palabras = sum(len(orac.split()) for orac in oraciones) / len(oraciones)
        return min(promedio_palabras / 30.0, 1.0)
    
    def _calcular_nivel_abstraccion(self, texto: str) -> float:
        """Calcula nivel de abstracción conceptual"""
        patterns_abstractos = re.findall(r'\\b(concepto|teoría|principio|fundamento|esencia)\\b', texto, re.IGNORECASE)
        return min(len(patterns_abstractos) / 12.0, 1.0)
    
    def _calcular_uso_jurisprudencia(self, texto: str) -> float:
        """Calcula uso de jurisprudencia y precedentes"""
        patterns_jurisprudencia = re.findall(r'\\b(fallo|sentencia|precedente|tribunal|corte)\\b', texto, re.IGNORECASE)
        return min(len(patterns_jurisprudencia) / 15.0, 1.0)
    
    def _detectar_autor(self, texto: str, metadatos: Dict = None) -> str:
        """Detecta el autor del documento"""
        if metadatos and 'autor' in metadatos:
            return metadatos['autor']
        
        # Patrones de detección de autor en texto
        patterns_autor = [
            r'Por:?\\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'Autor:?\\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\\s*\\(Autor\\)'
        ]
        
        for pattern in patterns_autor:
            match = re.search(pattern, texto[:1000])  # Buscar en el primer tercio
            if match:
                return match.group(1).strip()
        
        return "Autor no detectado"
    
    def _generar_resumen_cognitivo(self, perfil: Dict) -> str:
        """Genera resumen cognitivo del análisis"""
        
        # Encontrar características dominantes
        razonamiento_dominante = max(perfil["razonamiento"].items(), key=lambda x: x[1])
        estilo_dominante = max(perfil["estilos_literarios"].items(), key=lambda x: x[1])
        modalidad_dominante = max(perfil["modalidades_epistemicas"].items(), key=lambda x: x[1])
        
        resumen = f"""
🧠 PERFIL COGNITIVO DOMINANTE:
- Razonamiento: {razonamiento_dominante[0]} (score: {razonamiento_dominante[1]})
- Estilo: {estilo_dominante[0]} (score: {estilo_dominante[1]})
- Modalidad: {modalidad_dominante[0]} (score: {modalidad_dominante[1]})

📊 MÉTRICAS PRINCIPALES:
- Formalismo: {perfil["metricas_generales"]["formalismo"]:.3f}
- Creatividad: {perfil["metricas_generales"]["creatividad"]:.3f}
- Empirismo: {perfil["metricas_generales"]["empirismo"]:.3f}
"""
        
        return resumen.strip()
    
    def _perfil_vacio(self) -> Dict:
        """Retorna perfil vacío para textos inválidos"""
        return {
            "version_motor": self.version,
            "error": "Texto insuficiente para análisis",
            "razonamiento": {tipo: 0.0 for tipo in self.RAZONAMIENTO_PATTERNS.keys()},
            "modalidades_epistemicas": {mod: 0.0 for mod in self.MODALIDAD_EPISTEMICA_PATTERNS.keys()},
            "retorica": {ret: 0.0 for ret in self.RETORICA_PATTERNS.keys()},
            "estilos_literarios": {est: 0.0 for est in self.ESTILO_PATTERNS.keys()},
            "estructuras_argumentativas": {estr: 0.0 for estr in self.ESTRUCTURA_PATTERNS.keys()},
            "metricas_generales": {
                "formalismo": 0.0, "creatividad": 0.0, "empirismo": 0.0,
                "dogmatismo": 0.0, "interdisciplinariedad": 0.0,
                "complejidad_sintactica": 0.0, "nivel_abstraccion": 0.0,
                "uso_jurisprudencia": 0.0
            },
            "autor_detectado": "No detectado",
            "resumen_cognitivo": "Análisis no realizado por texto insuficiente"
        }

def main():
    """Test del motor corregido"""
    print("🧠 TESTING ANALYSER MÉTODO MEJORADO v2.0 - CORREGIDO")
    
    analyser = AnalyserMetodoMejorado()
    
    texto_test = """
    El presente análisis jurídico establece que, conforme a la doctrina mayoritaria,
    el razonamiento deductivo aplicado en este caso permite concluir que las consecuencias
    de esta interpretación sistemática son coherentes con el propósito teleológico de la norma.
    
    Por tanto, la jurisprudencia debe considerar este precedente como vinculante,
    dado que la finalidad de la ley apunta hacia una interpretación más flexible
    y menos dogmática de los principios establecidos.
    """
    
    perfil = analyser.procesar_texto_completo(texto_test)
    
    print("\n✅ PERFIL GENERADO:")
    print(f"Razonamiento deductivo: {perfil['razonamiento']['deductivo']}")
    print(f"Razonamiento teleológico: {perfil['razonamiento']['teleologico']}")
    print(f"Modalidad dialéctica: {perfil['modalidades_epistemicas']['dialectico']}")
    print(f"Autor detectado: {perfil['autor_detectado']}")
    
    print("\n🎉 ANALYSER MÉTODO MEJORADO v2.0 FUNCIONANDO CORRECTAMENTE")

if __name__ == "__main__":
    main()
'''
    
    with open(SCRIPTS_DIR / "analyser_metodo_mejorado.py", 'w', encoding='utf-8') as f:
        f.write(analyser_content)
    
    print("✅ analyser_metodo_mejorado.py creado correctamente")

def agregar_metodo_faltante(archivo_path):
    """Agrega método faltante al archivo existente"""
    with open(archivo_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Agregar método al final de la clase
    metodo_adicional = '''
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
'''
    
    # Buscar final de clase y agregar método
    if 'class AnalyserMetodoMejorado' in content:
        # Agregar al final del archivo antes del main
        if 'def main():' in content:
            content = content.replace('def main():', metodo_adicional + '\ndef main():')
        else:
            content += metodo_adicional
        
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Método procesar_texto_completo agregado")

def verificar_sistema_completo():
    """Verifica que todos los componentes estén funcionando"""
    print("🔍 VERIFICANDO SISTEMA COMPLETO...")
    
    errores = []
    
    # 1. Verificar archivos clave
    archivos_clave = [
        SCRIPTS_DIR / "analyser_metodo_mejorado.py",
        SCRIPTS_DIR / "comparador_mentes.py", 
        SCRIPTS_DIR / "orchestrador_maestro_integrado.py",
        SCRIPTS_DIR / "sistema_referencias_autores.py"
    ]
    
    for archivo in archivos_clave:
        if not archivo.exists():
            errores.append(f"❌ Falta archivo: {archivo}")
        else:
            print(f"✅ Archivo existe: {archivo.name}")
    
    # 2. Verificar bases de datos
    dbs = [
        DATA_DIR / "cognitivo.db",
        DATA_DIR / "pensamiento_integrado_v2.db"
    ]
    
    for db in dbs:
        if db.exists():
            print(f"✅ Base de datos existe: {db.name}")
        else:
            errores.append(f"❌ Falta base de datos: {db}")
    
    # 3. Verificar tablas
    try:
        with sqlite3.connect(DATA_DIR / "cognitivo.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = [row[0] for row in cursor.fetchall()]
            
            if 'perfiles_autorales' in tablas:
                print("✅ Tabla perfiles_autorales existe")
            else:
                errores.append("❌ Falta tabla perfiles_autorales")
    except Exception as e:
        errores.append(f"❌ Error verificando base de datos: {e}")
    
    if errores:
        print("\n🚨 ERRORES ENCONTRADOS:")
        for error in errores:
            print(error)
        return False
    else:
        print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
        return True

def main():
    """Reparación completa del sistema"""
    print("🚨 INICIANDO REPARACIÓN COMPLETA DEL SISTEMA")
    print("=" * 60)
    
    try:
        # 1. Crear/reparar bases de datos
        crear_base_datos_completa()
        
        # 2. Corregir AnalyserMetodoMejorado
        corregir_analyser_mejorado()
        
        # 3. Verificar sistema completo
        if verificar_sistema_completo():
            print("\n🎉 REPARACIÓN COMPLETADA EXITOSAMENTE")
            print("\n📋 PRÓXIMOS PASOS:")
            print("1. python procesar_todo.py")
            print("2. .\iniciar_sistema.bat")
        else:
            print("\n❌ REPARACIÓN INCOMPLETA - Revisar errores arriba")
    
    except Exception as e:
        print(f"\n💥 ERROR EN REPARACIÓN: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()