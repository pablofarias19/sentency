"""
🔬 CHUNKER INTELIGENTE - Fragmentación Semántica Avanzada
=========================================================
Mejora el RAG fragmentando por temas coherentes en lugar de tamaño fijo.
"""

import re
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np

class ChunkerInteligente:
    """
    Fragmenta texto respetando coherencia semántica y estructura argumentativa.
    """
    
    def __init__(self, modelo_embeddings='all-mpnet-base-v2'):
        self.model = SentenceTransformer(modelo_embeddings)
        self.umbral_similitud = 0.75  # Umbral para considerar párrafos del mismo tema
        
    def fragmentar_por_coherencia(self, texto: str, 
                                  max_tokens: int = 512,
                                  overlap: int = 50) -> List[Dict]:
        """
        Fragmenta texto manteniendo coherencia semántica.
        
        Returns:
            Lista de chunks con metadatos: {
                'texto': str,
                'inicio': int,
                'fin': int,
                'tema_principal': str,
                'coherencia_interna': float,
                'tipo_contenido': str  # 'introduccion', 'desarrollo', 'conclusion'
            }
        """
        # 1. DIVIDIR EN PÁRRAFOS LÓGICOS
        parrafos = self._extraer_parrafos_estructurales(texto)
        
        # 2. CALCULAR EMBEDDINGS DE CADA PÁRRAFO
        embeddings = self.model.encode([p['texto'] for p in parrafos])
        
        # 3. AGRUPAR POR SIMILITUD SEMÁNTICA
        grupos = self._agrupar_por_similitud(parrafos, embeddings, max_tokens)
        
        # 4. AÑADIR METADATOS ENRIQUECIDOS
        chunks_enriquecidos = []
        for i, grupo in enumerate(grupos):
            chunk = {
                'id': i,
                'texto': grupo['texto_completo'],
                'inicio': grupo['inicio'],
                'fin': grupo['fin'],
                'tema_principal': self._extraer_tema_principal(grupo['texto_completo']),
                'coherencia_interna': grupo['similitud_promedio'],
                'tipo_contenido': self._clasificar_tipo_contenido(grupo['texto_completo'], i, len(grupos)),
                'palabras_clave': self._extraer_palabras_clave(grupo['texto_completo']),
                'entidades_juridicas': self._detectar_entidades_juridicas(grupo['texto_completo']),
                'nivel_tecnico': self._calcular_nivel_tecnico(grupo['texto_completo'])
            }
            chunks_enriquecidos.append(chunk)
            
        return chunks_enriquecidos
    
    def _extraer_parrafos_estructurales(self, texto: str) -> List[Dict]:
        """Identifica párrafos respetando estructura argumentativa."""
        parrafos = []
        
        # Detectar títulos, subtítulos, listas, etc.
        lineas = texto.split('\n')
        parrafo_actual = []
        tipo_actual = 'texto'
        
        for i, linea in enumerate(lineas):
            linea_limpia = linea.strip()
            
            if not linea_limpia:
                if parrafo_actual:
                    parrafos.append({
                        'texto': ' '.join(parrafo_actual),
                        'tipo': tipo_actual,
                        'posicion': i
                    })
                    parrafo_actual = []
                continue
            
            # Detectar tipo de contenido
            if self._es_titulo(linea_limpia):
                tipo_actual = 'titulo'
            elif self._es_lista(linea_limpia):
                tipo_actual = 'lista'
            elif self._es_cita(linea_limpia):
                tipo_actual = 'cita'
            else:
                tipo_actual = 'texto'
            
            parrafo_actual.append(linea_limpia)
        
        if parrafo_actual:
            parrafos.append({
                'texto': ' '.join(parrafo_actual),
                'tipo': tipo_actual,
                'posicion': len(lineas)
            })
        
        return parrafos
    
    def _agrupar_por_similitud(self, parrafos: List[Dict], 
                               embeddings: np.ndarray,
                               max_tokens: int) -> List[Dict]:
        """Agrupa párrafos semánticamente similares."""
        grupos = []
        grupo_actual = []
        embedding_grupo = []
        tokens_acumulados = 0
        
        for i, parrafo in enumerate(parrafos):
            palabras = len(parrafo['texto'].split())
            
            # Verificar si agregar este párrafo mantiene coherencia
            if grupo_actual:
                similitud = self._calcular_similitud(
                    np.mean(embedding_grupo, axis=0),
                    embeddings[i]
                )
                
                # Si supera tokens O no es coherente, crear nuevo grupo
                if tokens_acumulados + palabras > max_tokens or similitud < self.umbral_similitud:
                    # Guardar grupo actual
                    grupos.append({
                        'texto_completo': ' '.join([p['texto'] for p in grupo_actual]),
                        'inicio': grupo_actual[0]['posicion'],
                        'fin': grupo_actual[-1]['posicion'],
                        'similitud_promedio': np.mean([
                            self._calcular_similitud(embedding_grupo[j], embedding_grupo[k])
                            for j in range(len(embedding_grupo))
                            for k in range(j+1, len(embedding_grupo))
                        ]) if len(embedding_grupo) > 1 else 1.0
                    })
                    
                    # Iniciar nuevo grupo
                    grupo_actual = []
                    embedding_grupo = []
                    tokens_acumulados = 0
            
            grupo_actual.append(parrafo)
            embedding_grupo.append(embeddings[i])
            tokens_acumulados += palabras
        
        # Añadir último grupo
        if grupo_actual:
            grupos.append({
                'texto_completo': ' '.join([p['texto'] for p in grupo_actual]),
                'inicio': grupo_actual[0]['posicion'],
                'fin': grupo_actual[-1]['posicion'],
                'similitud_promedio': np.mean([
                    self._calcular_similitud(embedding_grupo[j], embedding_grupo[k])
                    for j in range(len(embedding_grupo))
                    for k in range(j+1, len(embedding_grupo))
                ]) if len(embedding_grupo) > 1 else 1.0
            })
        
        return grupos
    
    def _calcular_similitud(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Similitud coseno entre dos embeddings."""
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    
    def _es_titulo(self, linea: str) -> bool:
        """Detecta si la línea es un título."""
        return (
            linea.isupper() or 
            (len(linea) < 100 and re.match(r'^[IVX]+\.', linea)) or
            re.match(r'^\d+\.', linea)
        )
    
    def _es_lista(self, linea: str) -> bool:
        """Detecta si la línea es item de lista."""
        return bool(re.match(r'^[-•▪\*]\s', linea) or re.match(r'^[a-z]\)', linea))
    
    def _es_cita(self, linea: str) -> bool:
        """Detecta si la línea es una cita."""
        return '"' in linea or linea.startswith('»')
    
    def _extraer_tema_principal(self, texto: str) -> str:
        """Extrae el tema principal del chunk."""
        # Implementación simplificada - puede mejorarse con NLP
        palabras = texto.lower().split()
        frecuencias = {}
        for palabra in palabras:
            if len(palabra) > 5 and palabra.isalpha():
                frecuencias[palabra] = frecuencias.get(palabra, 0) + 1
        
        if frecuencias:
            return max(frecuencias, key=frecuencias.get)
        return "general"
    
    def _clasificar_tipo_contenido(self, texto: str, posicion: int, total: int) -> str:
        """Clasifica el tipo de contenido del chunk."""
        ratio = posicion / total
        
        if ratio < 0.15:
            return "introduccion"
        elif ratio > 0.85:
            return "conclusion"
        else:
            return "desarrollo"
    
    def _extraer_palabras_clave(self, texto: str, top_n: int = 5) -> List[str]:
        """Extrae palabras clave más relevantes."""
        # Términos jurídicos comunes
        stopwords = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'por', 'con'}
        
        palabras = [p.lower() for p in re.findall(r'\b[a-záéíóúñ]{4,}\b', texto)]
        frecuencias = {}
        for palabra in palabras:
            if palabra not in stopwords:
                frecuencias[palabra] = frecuencias.get(palabra, 0) + 1
        
        return sorted(frecuencias, key=frecuencias.get, reverse=True)[:top_n]
    
    def _detectar_entidades_juridicas(self, texto: str) -> List[str]:
        """Detecta entidades jurídicas específicas."""
        entidades = []
        
        # Artículos legales
        entidades.extend(re.findall(r'art(?:ículo)?\.?\s*\d+', texto, re.IGNORECASE))
        
        # Leyes
        entidades.extend(re.findall(r'ley\s+n[°º]?\s*\d+[\./]\d+', texto, re.IGNORECASE))
        
        # Jurisprudencia
        entidades.extend(re.findall(r'(?:CSJN|CNFed|SCBA|TFN)', texto))
        
        return list(set(entidades))
    
    def _calcular_nivel_tecnico(self, texto: str) -> float:
        """Calcula nivel técnico del fragmento (0.0 a 1.0)."""
        # Latinismos
        latinismos = len(re.findall(r'\b(?:iure|facto|ipso|erga|ultra|sine)\b', texto, re.IGNORECASE))
        
        # Términos técnicos
        tecnicos = len(re.findall(r'\b(?:jurisdiccional|hermenéutica|exegesis|teleológica)\b', texto, re.IGNORECASE))
        
        # Citas normativas
        citas = len(re.findall(r'art\.|ley|decreto', texto, re.IGNORECASE))
        
        palabras_total = len(texto.split())
        if palabras_total == 0:
            return 0.0
        
        densidad = (latinismos * 3 + tecnicos * 2 + citas) / palabras_total
        return min(1.0, densidad * 100)  # Normalizar


# ==========================================================
# EJEMPLO DE USO
# ==========================================================
if __name__ == "__main__":
    chunker = ChunkerInteligente()
    
    texto_ejemplo = """
    Introducción al Amparo Constitucional
    
    El amparo es una acción judicial expedita y rápida de garantía constitucional, 
    que tiene por objeto la protección inmediata de los derechos fundamentales.
    
    Según el art. 43 de la Constitución Nacional, toda persona puede interponer 
    acción expedita y rápida de amparo siempre que no exista otro medio judicial 
    más idóneo contra todo acto u omisión de autoridades públicas o de particulares.
    
    La CSJN ha establecido en diversos fallos que el amparo procede cuando se 
    configura una amenaza cierta e inminente, arbitraria o ilegal, que lesione 
    derechos o garantías constitucionales.
    """
    
    chunks = chunker.fragmentar_por_coherencia(texto_ejemplo)
    
    print("📊 CHUNKS GENERADOS:")
    for chunk in chunks:
        print(f"\n🔹 Chunk #{chunk['id']}")
        print(f"   Tema: {chunk['tema_principal']}")
        print(f"   Tipo: {chunk['tipo_contenido']}")
        print(f"   Coherencia: {chunk['coherencia_interna']:.2f}")
        print(f"   Palabras clave: {', '.join(chunk['palabras_clave'])}")
        print(f"   Nivel técnico: {chunk['nivel_tecnico']:.2f}")
        print(f"   Entidades: {', '.join(chunk['entidades_juridicas']) if chunk['entidades_juridicas'] else 'N/A'}")
        print(f"   Texto: {chunk['texto'][:100]}...")
