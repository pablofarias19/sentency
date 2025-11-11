"""
🎯 ANALIZADOR DE METADATOS ARGUMENTATIVOS
=========================================
Extrae cadenas argumentativas completas, contra-argumentos y estructura retórica.
"""

import re
from typing import List, Dict, Any, Tuple
from collections import defaultdict

class AnalizadorArgumentativo:
    """
    Analiza la estructura argumentativa profunda de textos jurídicos.
    """
    
    def __init__(self):
        # Conectores argumentativos por categoría
        self.conectores = {
            'causales': ['porque', 'ya que', 'puesto que', 'dado que', 'en virtud de'],
            'consecutivos': ['por tanto', 'por consiguiente', 'en consecuencia', 'así pues', 'de modo que'],
            'adversativos': ['pero', 'sin embargo', 'no obstante', 'ahora bien', 'con todo'],
            'concesivos': ['aunque', 'si bien', 'a pesar de', 'pese a', 'aun cuando'],
            'condicionales': ['si', 'en caso de', 'siempre que', 'con tal de que', 'a condición de'],
            'finales': ['para', 'a fin de', 'con el objeto de', 'con el propósito de'],
            'comparativos': ['así como', 'del mismo modo', 'igualmente', 'análogamente', 'similarmente']
        }
        
        # Patrones de silogismos
        self.patrones_silogismo = {
            'premisa_mayor': [
                r'(?:todo|toda|todos|todas)\s+([^.]+?)\s+(?:es|son|debe|deben|tiene|tienen)',
                r'(?:ningún|ninguna|ninguno)\s+([^.]+?)\s+(?:es|son|puede|pueden)',
                r'(?:cualquier|cada)\s+([^.]+?)\s+(?:que|requiere|implica)'
            ],
            'premisa_menor': [
                r'(?:el|la|los|las)\s+([^.]+?)\s+(?:es un|es una|son|constituye)',
                r'(?:este|esta|estos|estas)\s+([^.]+?)\s+(?:es|son|tiene|tienen)'
            ],
            'conclusion': [
                r'(?:por tanto|por consiguiente|en consecuencia|luego|entonces),?\s+([^.]+)',
                r'(?:se concluye que|se deduce que|se infiere que)\s+([^.]+)',
                r'(?:resulta que|de ello se sigue que)\s+([^.]+)'
            ]
        }
        
        # Patrones de objeciones anticipadas
        self.patrones_objeciones = [
            r'podría (?:objetarse|argumentarse|sostenerse) que\s+([^.]+)',
            r'(?:algunos|ciertos autores) (?:sostienen|afirman|consideran) que\s+([^.]+)',
            r'(?:se ha dicho|se dice) que\s+([^.]+)',
            r'(?:la crítica|una objeción) señala que\s+([^.]+)'
        ]
        
        # Patrones de refutaciones
        self.patrones_refutaciones = [
            r'sin embargo,?\s+([^.]+)',
            r'(?:no obstante|con todo),?\s+([^.]+)',
            r'(?:esta objeción|tal argumento) (?:no es válida|carece de fundamento|es infundada)',
            r'(?:debe rechazarse|cabe rechazar) (?:esta|tal) (?:postura|tesis)'
        ]
    
    def analizar_documento_completo(self, texto: str) -> Dict[str, Any]:
        """
        Análisis argumentativo completo del documento.
        
        Returns:
            Dict con: cadenas_argumentativas, objeciones, refutaciones,
                     estructura_retorica, mapa_fuerza_argumentativa
        """
        parrafos = self._extraer_parrafos(texto)
        
        resultado = {
            'cadenas_argumentativas': self._extraer_cadenas_argumentativas(parrafos),
            'objeciones_anticipadas': self._extraer_objeciones(texto),
            'refutaciones': self._extraer_refutaciones(texto),
            'estructura_retorica': self._analizar_estructura_retorica(parrafos),
            'mapa_fuerza': self._calcular_mapa_fuerza(parrafos),
            'conectores_por_tipo': self._analizar_conectores(texto),
            'nivel_dialectico': self._calcular_nivel_dialectico(texto)
        }
        
        return resultado
    
    def _extraer_parrafos(self, texto: str) -> List[Dict]:
        """Extrae párrafos con metadatos básicos."""
        parrafos = []
        bloques = texto.split('\n\n')
        
        for i, bloque in enumerate(bloques):
            if len(bloque.strip()) < 50:
                continue
            
            parrafos.append({
                'id': i,
                'texto': bloque.strip(),
                'posicion_relativa': i / len(bloques) if bloques else 0,
                'longitud': len(bloque.split())
            })
        
        return parrafos
    
    def _extraer_cadenas_argumentativas(self, parrafos: List[Dict]) -> List[Dict]:
        """
        Detecta cadenas completas de argumentación (premisa mayor → menor → conclusión).
        """
        cadenas = []
        
        for i, parrafo in enumerate(parrafos):
            texto = parrafo['texto'].lower()
            
            # Buscar premisa mayor
            premisa_mayor = None
            for patron in self.patrones_silogismo['premisa_mayor']:
                match = re.search(patron, texto, re.IGNORECASE)
                if match:
                    premisa_mayor = match.group(0)
                    break
            
            if not premisa_mayor:
                continue
            
            # Buscar premisa menor en el mismo párrafo o siguiente
            premisa_menor = None
            for patron in self.patrones_silogismo['premisa_menor']:
                match = re.search(patron, texto, re.IGNORECASE)
                if match:
                    premisa_menor = match.group(0)
                    break
            
            # Buscar conclusión
            conclusion = None
            for patron in self.patrones_silogismo['conclusion']:
                match = re.search(patron, texto, re.IGNORECASE)
                if match:
                    conclusion = match.group(0)
                    break
            
            # Si tenemos al menos premisa y conclusión, registrar
            if premisa_mayor and conclusion:
                tipo_silogismo = self._clasificar_silogismo(premisa_mayor, premisa_menor, conclusion)
                
                cadena = {
                    'id': len(cadenas),
                    'parrafo_origen': i,
                    'premisa_mayor': premisa_mayor,
                    'premisa_menor': premisa_menor,
                    'conclusion': conclusion,
                    'tipo_silogismo': tipo_silogismo,
                    'validez_logica': self._evaluar_validez_logica(premisa_mayor, premisa_menor, conclusion),
                    'fuerza_persuasiva': self._calcular_fuerza_persuasiva(texto)
                }
                cadenas.append(cadena)
        
        return cadenas
    
    def _clasificar_silogismo(self, premisa_mayor: str, premisa_menor: str, conclusion: str) -> str:
        """Clasifica el tipo de silogismo."""
        pm = premisa_mayor.lower() if premisa_mayor else ""
        
        if 'todo' in pm or 'toda' in pm:
            return 'Barbara (AAA-1)'  # Todos A son B, Todos B son C → Todos A son C
        elif 'ningún' in pm or 'ninguna' in pm:
            return 'Cesare (EAE-2)'  # Ningún A es B, Todo C es A → Ningún C es B
        elif 'algún' in pm or 'alguna' in pm:
            return 'Darii (AII-1)'  # Todo A es B, Algún C es A → Algún C es B
        else:
            return 'Forma mixta o no estándar'
    
    def _evaluar_validez_logica(self, premisa_mayor: str, premisa_menor: str, conclusion: str) -> float:
        """
        Evalúa validez lógica del argumento (0.0 a 1.0).
        Simplificado - en producción usar lógica formal.
        """
        score = 0.5  # Base neutral
        
        if premisa_mayor and premisa_menor and conclusion:
            score += 0.2  # Estructura completa
        
        # Detectar cuantificadores apropiados
        if any(q in (premisa_mayor or "").lower() for q in ['todo', 'toda', 'ningún', 'algún']):
            score += 0.2
        
        # Detectar conectores lógicos apropiados
        if any(c in (conclusion or "").lower() for c in ['por tanto', 'luego', 'entonces', 'en consecuencia']):
            score += 0.1
        
        return min(1.0, score)
    
    def _calcular_fuerza_persuasiva(self, texto: str) -> float:
        """Calcula fuerza persuasiva del argumento."""
        score = 0.0
        texto_lower = texto.lower()
        
        # Citas de autoridad
        if any(ind in texto_lower for ind in ['según', 'conforme', 'como sostiene', 'csjn', 'corte']):
            score += 0.2
        
        # Datos empíricos
        if re.search(r'\d+%|\d+ casos|\d+ sentencias', texto):
            score += 0.2
        
        # Latinismos (autoridad técnica)
        if re.search(r'\b(iure|facto|ipso|erga|ultra|sine)\b', texto):
            score += 0.1
        
        # Estructura clara
        if any(c in texto_lower for c in ['primero', 'segundo', 'finalmente', 'en resumen']):
            score += 0.15
        
        # Citas normativas
        if re.search(r'art\.?\s*\d+|ley\s+\d+', texto_lower):
            score += 0.15
        
        return min(1.0, score)
    
    def _extraer_objeciones(self, texto: str) -> List[Dict]:
        """Extrae objeciones anticipadas por el autor."""
        objeciones = []
        
        for patron in self.patrones_objeciones:
            for match in re.finditer(patron, texto, re.IGNORECASE):
                objeciones.append({
                    'texto': match.group(0),
                    'posicion': match.start(),
                    'tipo': 'objecion_anticipada'
                })
        
        return objeciones
    
    def _extraer_refutaciones(self, texto: str) -> List[Dict]:
        """Extrae refutaciones a objeciones."""
        refutaciones = []
        
        for patron in self.patrones_refutaciones:
            for match in re.finditer(patron, texto, re.IGNORECASE):
                refutaciones.append({
                    'texto': match.group(0),
                    'posicion': match.start(),
                    'tipo': 'refutacion'
                })
        
        return refutaciones
    
    def _analizar_estructura_retorica(self, parrafos: List[Dict]) -> Dict[str, Any]:
        """
        Analiza estructura retórica según modelo clásico.
        """
        total = len(parrafos)
        if total == 0:
            return {}
        
        # Divisiones aproximadas
        limite_exordio = int(total * 0.15)
        limite_narratio = int(total * 0.30)
        limite_confirmatio = int(total * 0.70)
        limite_refutatio = int(total * 0.85)
        
        estructura = {
            'exordio': {  # Introducción
                'parrafos': list(range(0, limite_exordio)),
                'funcion': 'Captación de atención, presentación del tema',
                'texto_muestra': parrafos[0]['texto'][:200] if parrafos else ''
            },
            'narratio': {  # Exposición de hechos
                'parrafos': list(range(limite_exordio, limite_narratio)),
                'funcion': 'Exposición de hechos y antecedentes',
                'longitud': limite_narratio - limite_exordio
            },
            'confirmatio': {  # Argumentos a favor
                'parrafos': list(range(limite_narratio, limite_confirmatio)),
                'funcion': 'Argumentación principal a favor de la tesis',
                'longitud': limite_confirmatio - limite_narratio
            },
            'refutatio': {  # Refutación de objeciones
                'parrafos': list(range(limite_confirmatio, limite_refutatio)),
                'funcion': 'Refutación de objeciones y contra-argumentos',
                'longitud': limite_refutatio - limite_confirmatio
            },
            'peroratio': {  # Conclusión
                'parrafos': list(range(limite_refutatio, total)),
                'funcion': 'Conclusión y cierre',
                'texto_muestra': parrafos[-1]['texto'][:200] if parrafos else ''
            }
        }
        
        return estructura
    
    def _calcular_mapa_fuerza(self, parrafos: List[Dict]) -> List[Dict]:
        """
        Calcula fuerza argumentativa por párrafo.
        """
        mapa = []
        
        for parrafo in parrafos:
            fuerza = self._calcular_fuerza_persuasiva(parrafo['texto'])
            tipo = self._clasificar_tipo_parrafo(parrafo['texto'])
            
            mapa.append({
                'parrafo': parrafo['id'],
                'fuerza': fuerza,
                'tipo': tipo,
                'longitud': parrafo['longitud']
            })
        
        return mapa
    
    def _clasificar_tipo_parrafo(self, texto: str) -> str:
        """Clasifica el tipo funcional del párrafo."""
        texto_lower = texto.lower()
        
        if any(ind in texto_lower for ind in ['según', 'como sostiene', 'conforme']):
            return 'cita_autoridad'
        elif re.search(r'\d+%|\d+ casos', texto):
            return 'evidencia_empirica'
        elif any(c in texto_lower for c in ['por tanto', 'en consecuencia', 'se concluye']):
            return 'conclusion'
        elif any(c in texto_lower for c in ['porque', 'ya que', 'dado que']):
            return 'fundamentacion'
        elif any(c in texto_lower for c in ['sin embargo', 'no obstante', 'pero']):
            return 'objecion_refutacion'
        else:
            return 'exposicion'
    
    def _analizar_conectores(self, texto: str) -> Dict[str, int]:
        """Analiza frecuencia de conectores por tipo."""
        frecuencias = {}
        texto_lower = texto.lower()
        
        for tipo, conectores in self.conectores.items():
            count = sum(texto_lower.count(c) for c in conectores)
            frecuencias[tipo] = count
        
        return frecuencias
    
    def _calcular_nivel_dialectico(self, texto: str) -> float:
        """
        Calcula nivel dialéctico (capacidad de anticipar y refutar objeciones).
        """
        objeciones = self._extraer_objeciones(texto)
        refutaciones = self._extraer_refutaciones(texto)
        
        if len(objeciones) == 0:
            return 0.0
        
        # Ratio objeciones/refutaciones
        ratio = len(refutaciones) / len(objeciones) if objeciones else 0
        
        # Normalizar a 0-1
        return min(1.0, ratio)


# ==========================================================
# EJEMPLO DE USO
# ==========================================================
if __name__ == "__main__":
    analizador = AnalizadorArgumentativo()
    
    texto_ejemplo = """
    Todo derecho fundamental requiere tutela judicial efectiva. El acceso 
    a la justicia es un derecho fundamental reconocido constitucionalmente.
    Por tanto, el acceso a la justicia requiere tutela judicial efectiva.
    
    Podría objetarse que existen vías alternativas de resolución de conflictos.
    Sin embargo, esta objeción no es válida, puesto que la Corte ha sostenido
    que tales vías son complementarias, no sustitutivas.
    
    Según la CSJN en Fallos 330:3248, el amparo procede cuando se configura
    una amenaza cierta e inminente a derechos constitucionales.
    """
    
    resultado = analizador.analizar_documento_completo(texto_ejemplo)
    
    print("🎯 ANÁLISIS ARGUMENTATIVO COMPLETO")
    print("=" * 70)
    
    print(f"\n📊 Cadenas argumentativas detectadas: {len(resultado['cadenas_argumentativas'])}")
    for cadena in resultado['cadenas_argumentativas']:
        print(f"\n  🔹 Cadena #{cadena['id']}")
        print(f"     Tipo: {cadena['tipo_silogismo']}")
        print(f"     Validez lógica: {cadena['validez_logica']:.2f}")
        print(f"     Fuerza persuasiva: {cadena['fuerza_persuasiva']:.2f}")
        print(f"     Premisa mayor: {cadena['premisa_mayor'][:80]}...")
        if cadena['premisa_menor']:
            print(f"     Premisa menor: {cadena['premisa_menor'][:80]}...")
        print(f"     Conclusión: {cadena['conclusion'][:80]}...")
    
    print(f"\n⚠️ Objeciones anticipadas: {len(resultado['objeciones_anticipadas'])}")
    for obj in resultado['objeciones_anticipadas']:
        print(f"  • {obj['texto'][:100]}...")
    
    print(f"\n🛡️ Refutaciones: {len(resultado['refutaciones'])}")
    for ref in resultado['refutaciones']:
        print(f"  • {ref['texto'][:100]}...")
    
    print(f"\n📐 Nivel dialéctico: {resultado['nivel_dialectico']:.2f}")
    
    print(f"\n🎭 Conectores por tipo:")
    for tipo, count in resultado['conectores_por_tipo'].items():
        if count > 0:
            print(f"  • {tipo}: {count}")
