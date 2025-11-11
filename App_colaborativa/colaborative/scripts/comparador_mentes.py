#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧮 COMPARADOR DE MENTES - Sistema de Análisis Cognitivo Comparativo
=================================================================

IMPLEMENTA:
- Vectorización de perfiles autorales
- Cálculo de similaridad coseno entre formas de pensar
- Ranking de autores por cercanía cognitiva
- Búsqueda por patrones de pensamiento específicos
- Análisis de distancias mentales

COMPATIBLE CON: perfil_autoral.json (esquema unificado)
AUTOR: Sistema Cognitivo v5.0 - Mejoras Integrales
FECHA: 9 NOV 2025
"""

import json
import sqlite3
import math
from typing import Dict, List, Tuple, Any
import os
from dataclasses import dataclass

@dataclass
class SimilitudMental:
    """Resultado de comparación entre dos mentes"""
    autor_a: str
    autor_b: str
    cosine_similarity: float
    distance: float
    dimensiones_clave: Dict[str, float]
    diferencias_principales: List[Tuple[str, float]]

class ComparadorMentes:
    """Sistema de comparación de patrones cognitivos entre autores"""
    
    # Claves de features para vectorización
    FEATURE_KEYS = [
        # Razonamiento formal (14 dimensiones)
        "cognicion.razonamiento_formal.deductivo",
        "cognicion.razonamiento_formal.inductivo",
        "cognicion.razonamiento_formal.abductivo",
        "cognicion.razonamiento_formal.analogico",
        "cognicion.razonamiento_formal.teleologico",
        "cognicion.razonamiento_formal.sistemico",
        "cognicion.razonamiento_formal.autoritativo",
        "cognicion.razonamiento_formal.a_contrario",
        "cognicion.razonamiento_formal.consecuencialista",
        "cognicion.razonamiento_formal.dialectico",
        "cognicion.razonamiento_formal.hermeneutico",
        "cognicion.razonamiento_formal.historico",
        "cognicion.razonamiento_formal.economico_analitico",
        "cognicion.razonamiento_formal.reduccion_al_absurdo",
        
        # Modalidad epistémica (7 dimensiones)
        "cognicion.modalidad_epistemica.apodictico",
        "cognicion.modalidad_epistemica.dialectico",
        "cognicion.modalidad_epistemica.retorico",
        "cognicion.modalidad_epistemica.sofistico",
        "cognicion.modalidad_epistemica.certeza",
        "cognicion.modalidad_epistemica.incertidumbre_explorada",
        "cognicion.modalidad_epistemica.hedging",
        
        # Retórica (3 dimensiones)
        "cognicion.retorica.ethos",
        "cognicion.retorica.pathos", 
        "cognicion.retorica.logos",
        
        # Estilos literarios (8 dimensiones)
        "cognicion.estilo_literario.tecnico_juridico",
        "cognicion.estilo_literario.ensayistico",
        "cognicion.estilo_literario.narrativo",
        "cognicion.estilo_literario.barroco",
        "cognicion.estilo_literario.minimalista",
        "cognicion.estilo_literario.aforistico",
        "cognicion.estilo_literario.impersonal_burocratico",
        "cognicion.estilo_literario.dialectico_critico",
        
        # Marcadores cognitivos (8 dimensiones)
        "marcadores_cognitivos.nivel_abstraccion",
        "marcadores_cognitivos.complejidad_sintactica", 
        "marcadores_cognitivos.interdisciplinariedad",
        "marcadores_cognitivos.empirismo",
        "marcadores_cognitivos.dogmatismo",
        "marcadores_cognitivos.creatividad",
        "marcadores_cognitivos.uso_jurisprudencia",
        "marcadores_cognitivos.coherencia_global"
    ]
    
    def __init__(self, db_path: str = "colaborative/bases_rag/cognitiva/perfiles_autorales.db"):
        self.db_path = db_path
        self.version = "v1.0_comparador_mentes"
        
    def _get_nested_value(self, data: Dict, path: str) -> float:
        """Extrae valor anidado usando notación de punto"""
        keys = path.split(".")
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return 0.0
        
        return float(current) if isinstance(current, (int, float)) else 0.0
    
    def vectorizar_perfil(self, perfil: Dict[str, Any]) -> List[float]:
        """Convierte perfil autoral en vector numérico"""
        return [self._get_nested_value(perfil, key) for key in self.FEATURE_KEYS]
    
    def calcular_coseno(self, vector_a: List[float], vector_b: List[float]) -> float:
        """Calcula similaridad coseno entre dos vectores"""
        if len(vector_a) != len(vector_b):
            raise ValueError("Vectores deben tener la misma dimensión")
            
        # Producto punto
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        
        # Magnitudes
        magnitude_a = math.sqrt(sum(a * a for a in vector_a))
        magnitude_b = math.sqrt(sum(b * b for b in vector_b))
        
        # Evitar división por cero
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0
            
        return dot_product / (magnitude_a * magnitude_b)
    
    def calcular_distancia(self, vector_a: List[float], vector_b: List[float]) -> float:
        """Calcula distancia como 1 - coseno"""
        return 1.0 - self.calcular_coseno(vector_a, vector_b)
    
    def analizar_diferencias_dimensionales(self, perfil_a: Dict, perfil_b: Dict) -> List[Tuple[str, float]]:
        """Identifica las mayores diferencias por dimensión"""
        diferencias = []
        
        for key in self.FEATURE_KEYS:
            val_a = self._get_nested_value(perfil_a, key)
            val_b = self._get_nested_value(perfil_b, key)
            diff = abs(val_a - val_b)
            diferencias.append((key.split('.')[-1], diff))
        
        # Ordenar por mayor diferencia
        diferencias.sort(key=lambda x: x[1], reverse=True)
        return diferencias[:5]  # Top 5 diferencias
    
    def comparar_mentes(self, perfil_a: Dict, perfil_b: Dict) -> SimilitudMental:
        """Compara dos perfiles autorales completos"""
        
        # Vectorizar perfiles
        vector_a = self.vectorizar_perfil(perfil_a)
        vector_b = self.vectorizar_perfil(perfil_b)
        
        # Calcular métricas
        cosine_sim = self.calcular_coseno(vector_a, vector_b)
        distance = self.calcular_distancia(vector_a, vector_b)
        
        # Análisis dimensional
        diferencias = self.analizar_diferencias_dimensionales(perfil_a, perfil_b)
        
        # Dimensiones clave (con mayor peso)
        dimensiones_clave = {
            "razonamiento": self.calcular_coseno(
                [self._get_nested_value(perfil_a, k) for k in self.FEATURE_KEYS[:14]],
                [self._get_nested_value(perfil_b, k) for k in self.FEATURE_KEYS[:14]]
            ),
            "modalidad_epistemica": self.calcular_coseno(
                [self._get_nested_value(perfil_a, k) for k in self.FEATURE_KEYS[14:21]],
                [self._get_nested_value(perfil_b, k) for k in self.FEATURE_KEYS[14:21]]
            ),
            "estilo_literario": self.calcular_coseno(
                [self._get_nested_value(perfil_a, k) for k in self.FEATURE_KEYS[24:32]],
                [self._get_nested_value(perfil_b, k) for k in self.FEATURE_KEYS[24:32]]
            )
        }
        
        return SimilitudMental(
            autor_a=perfil_a.get('meta', {}).get('autor_probable', 'Desconocido A'),
            autor_b=perfil_b.get('meta', {}).get('autor_probable', 'Desconocido B'),
            cosine_similarity=cosine_sim,
            distance=distance,
            dimensiones_clave=dimensiones_clave,
            diferencias_principales=diferencias
        )
    
    def cargar_perfiles_desde_db(self) -> List[Dict[str, Any]]:
        """Carga todos los perfiles desde la base de datos"""
        
        if not os.path.exists(self.db_path):
            print(f"⚠️  Base de datos no encontrada: {self.db_path}")
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT autor, perfil_json FROM perfiles_autorales_v2")
            rows = cursor.fetchall()
            
            perfiles = []
            for autor, perfil_json in rows:
                try:
                    perfil = json.loads(perfil_json)
                    perfiles.append(perfil)
                except json.JSONDecodeError:
                    print(f"⚠️  Error decodificando perfil de {autor}")
                    continue
            
            conn.close()
            return perfiles
            
        except sqlite3.OperationalError as e:
            print(f"⚠️  Error de base de datos: {e}")
            conn.close()
            return []
    
    def buscar_por_patron_pensamiento(self, patron: Dict[str, float], umbral: float = 0.7) -> List[Tuple[str, float]]:
        """Busca autores que coincidan con un patrón de pensamiento específico"""
        
        perfiles = self.cargar_perfiles_desde_db()
        coincidencias = []
        
        for perfil in perfiles:
            # Crear vector del patrón buscado
            vector_patron = []
            vector_perfil = []
            
            for key in self.FEATURE_KEYS:
                dimension = key.split('.')[-1]
                if dimension in patron:
                    vector_patron.append(patron[dimension])
                    vector_perfil.append(self._get_nested_value(perfil, key))
            
            if vector_patron:  # Si hay dimensiones que comparar
                similaridad = self.calcular_coseno(vector_patron, vector_perfil)
                if similaridad >= umbral:
                    autor = perfil.get('meta', {}).get('autor_probable', 'Desconocido')
                    coincidencias.append((autor, similaridad))
        
        # Ordenar por similaridad descendente
        coincidencias.sort(key=lambda x: x[1], reverse=True)
        return coincidencias
    
    def ranking_similitud_a_autor(self, autor_referencia: str) -> List[Tuple[str, float]]:
        """Crea ranking de autores similares a uno de referencia"""
        
        perfiles = self.cargar_perfiles_desde_db()
        
        # Encontrar perfil de referencia
        perfil_ref = None
        for perfil in perfiles:
            if perfil.get('meta', {}).get('autor_probable') == autor_referencia:
                perfil_ref = perfil
                break
        
        if not perfil_ref:
            print(f"⚠️  Autor de referencia '{autor_referencia}' no encontrado")
            return []
        
        # Calcular similaridades
        ranking = []
        for perfil in perfiles:
            autor = perfil.get('meta', {}).get('autor_probable', 'Desconocido')
            if autor != autor_referencia:  # Excluir el mismo autor
                similaridad = self.comparar_mentes(perfil_ref, perfil)
                ranking.append((autor, similaridad.cosine_similarity))
        
        # Ordenar por similaridad descendente
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking
    
    def generar_reporte_comparativo(self, autor_a: str, autor_b: str) -> str:
        """Genera reporte detallado de comparación entre dos autores"""
        
        perfiles = self.cargar_perfiles_desde_db()
        
        # Encontrar perfiles
        perfil_a = perfil_b = None
        for perfil in perfiles:
            autor = perfil.get('meta', {}).get('autor_probable')
            if autor == autor_a:
                perfil_a = perfil
            elif autor == autor_b:
                perfil_b = perfil
        
        if not perfil_a or not perfil_b:
            return f"⚠️  No se encontraron perfiles para {autor_a} y/o {autor_b}"
        
        # Comparar
        comparacion = self.comparar_mentes(perfil_a, perfil_b)
        
        reporte = f"""
🧠 REPORTE COMPARATIVO DE MENTES
===============================

👤 AUTOR A: {comparacion.autor_a}
👤 AUTOR B: {comparacion.autor_b}

📊 MÉTRICAS GLOBALES:
• Similaridad Coseno: {comparacion.cosine_similarity:.3f}
• Distancia Mental: {comparacion.distance:.3f}
• Nivel de Afinidad: {'ALTA' if comparacion.cosine_similarity > 0.8 else 'MEDIA' if comparacion.cosine_similarity > 0.6 else 'BAJA'}

🎯 SIMILARIDADES POR DIMENSIÓN:
• Razonamiento: {comparacion.dimensiones_clave['razonamiento']:.3f}
• Modalidad Epistémica: {comparacion.dimensiones_clave['modalidad_epistemica']:.3f}
• Estilo Literario: {comparacion.dimensiones_clave['estilo_literario']:.3f}

⚡ MAYORES DIFERENCIAS:
"""
        
        for i, (dimension, diferencia) in enumerate(comparacion.diferencias_principales, 1):
            reporte += f"  {i}. {dimension.replace('_', ' ').title()}: {diferencia:.3f}\n"
        
        return reporte
    
    def exportar_matriz_similitudes(self, output_path: str = "matriz_similitudes_mentes.json"):
        """Exporta matriz completa de similitudes entre todos los autores"""
        
        perfiles = self.cargar_perfiles_desde_db()
        autores = [p.get('meta', {}).get('autor_probable', 'Desconocido') for p in perfiles]
        
        matriz = {}
        
        print(f"🔄 Calculando matriz de similitudes para {len(autores)} autores...")
        
        for i, autor_a in enumerate(autores):
            matriz[autor_a] = {}
            for j, autor_b in enumerate(autores):
                if i == j:
                    matriz[autor_a][autor_b] = 1.0  # Identidad
                elif autor_b in matriz and autor_a in matriz[autor_b]:
                    # Simetría: ya calculado
                    matriz[autor_a][autor_b] = matriz[autor_b][autor_a]
                else:
                    # Calcular similaridad
                    comparacion = self.comparar_mentes(perfiles[i], perfiles[j])
                    matriz[autor_a][autor_b] = comparacion.cosine_similarity
        
        # Exportar
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(matriz, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Matriz exportada a: {output_path}")
        return matriz

def main():
    """Función principal para probar el comparador"""
    
    print("🚀 INICIANDO COMPARADOR DE MENTES v1.0")
    
    comparador = ComparadorMentes()
    
    # Ejemplo de búsqueda por patrón
    patron_teleologico_ensayistico = {
        "teleologico": 0.8,
        "ensayistico": 0.7,
        "creatividad": 0.6
    }
    
    print("\n🔍 Buscando autores con patrón teleológico-ensayístico...")
    coincidencias = comparador.buscar_por_patron_pensamiento(patron_teleologico_ensayistico)
    
    if coincidencias:
        print("📋 AUTORES ENCONTRADOS:")
        for autor, similaridad in coincidencias:
            print(f"  • {autor}: {similaridad:.3f}")
    else:
        print("❌ No se encontraron coincidencias")
    
    # Cargar perfiles para otros ejemplos
    perfiles = comparador.cargar_perfiles_desde_db()
    
    if len(perfiles) >= 2:
        print(f"\n🧮 Comparando primeros dos perfiles disponibles...")
        comparacion = comparador.comparar_mentes(perfiles[0], perfiles[1])
        
        print(f"👤 {comparacion.autor_a} vs {comparacion.autor_b}")
        print(f"📊 Similaridad: {comparacion.cosine_similarity:.3f}")
        print(f"📏 Distancia: {comparacion.distance:.3f}")
    
    print("\n✅ Prueba completada")

if __name__ == "__main__":
    main()