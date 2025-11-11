"""
🕸️ GRAFO DE CONOCIMIENTO JURÍDICO - NETWORKX
============================================

Construye un grafo de conocimiento con:
- Nodos: Autores, Conceptos, Normas, Casos, Doctrinas
- Relaciones: cita_a, desarrolla, aplica, contradice, fundamenta_con

Permite consultas como:
- "¿Qué autores citan a Kelsen?"
- "¿Qué casos aplican el art. 43 CN?"
- "Cadena de influencia: Kelsen → Hart → Dworkin"
- "¿Qué argumentos contradicen la teoría de X?"

Autor: Sistema V7.8
Fecha: 11 Nov 2025
"""

import networkx as nx
import re
import json
import sqlite3
from typing import List, Dict, Set, Tuple, Optional
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np


class GrafoConocimientoJuridico:
    """
    Grafo de conocimiento para análisis de relaciones jurídicas.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Inicializa el grafo de conocimiento.
        
        Args:
            db_path: Ruta a metadatos.db para cargar datos existentes
        """
        # Crear grafo dirigido
        self.grafo = nx.DiGraph()
        
        # Contadores
        self.n_nodos = 0
        self.n_relaciones = 0
        
        # Base de datos
        self.db_path = db_path
        
        # Patrones de extracción
        self._compilar_patrones()
        
        print("✅ GrafoConocimientoJuridico inicializado")
    
    def _compilar_patrones(self):
        """
        Compila expresiones regulares para extracción de entidades.
        """
        # Artículos y leyes
        self.patron_articulo = re.compile(
            r'\b(art(?:ículo|iculo)?\.?\s*\d+(?:\s*(?:bis|ter|quater))?(?:\s*inc\.?\s*[a-z0-9]+)?)\b',
            re.IGNORECASE
        )
        
        self.patron_ley = re.compile(
            r'\bLey\s+(?:N[°º]?\s*)?(\d{1,6}(?:[/-]\d{2,4})?)\b',
            re.IGNORECASE
        )
        
        # Casos judiciales
        self.patron_caso = re.compile(
            r'\b([A-ZÁÉÍÓÚ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚ][a-záéíóúñ]+)*)\s+(?:c/|vs?\.?|contra)\s+([A-ZÁÉÍÓÚ][a-záéíóúñ]+)',
            re.IGNORECASE
        )
        
        self.patron_csjn = re.compile(
            r'\bCSJN\b|\bCorte Suprema\b',
            re.IGNORECASE
        )
        
        # Autores (nombres propios seguidos de año)
        self.patron_cita_autor = re.compile(
            r'\b([A-ZÁÉÍÓÚ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚ][a-záéíóúñ]+)*)\s*\((\d{4})\)',
            re.IGNORECASE
        )
        
        # Conceptos jurídicos (uppercase + contexto)
        self.patron_concepto = re.compile(
            r'\b(derecho\s+\w+|principio\s+de\s+\w+|teoría\s+de\s+\w+|doctrina\s+de\s+\w+)\b',
            re.IGNORECASE
        )
        
        # Latinismos
        self.patron_latinismo = re.compile(
            r'\b(pacta sunt servanda|nullum crimen sine lege|in dubio pro reo|res judicata|'
            r'habeas corpus|habeas data|erga omnes|ultra vires|mutatis mutandis|'
            r'ratio decidendi|obiter dicta|stare decisis)\b',
            re.IGNORECASE
        )
        
        # Verbos relacionales
        self.patrones_relaciones = {
            'cita_a': re.compile(r'\bcita(?:ndo)?\s+a\s+(\w+)|\b(?:según|conforme a|como sostiene)\s+(\w+)', re.IGNORECASE),
            'desarrolla': re.compile(r'\bdesarrolla(?:ndo)?\s+(?:el|la)\s+(\w+)|\belabora\s+(?:el|la)\s+(\w+)', re.IGNORECASE),
            'aplica': re.compile(r'\baplica(?:ndo)?\s+(?:el|la|los|las)\s+(\w+)', re.IGNORECASE),
            'contradice': re.compile(r'\bcontradice\s+a\s+(\w+)|\bse opone a\s+(\w+)', re.IGNORECASE),
            'fundamenta_con': re.compile(r'\bfundamenta(?:ndo)?\s+(?:con|en)\s+(\w+)', re.IGNORECASE)
        }
    
    def agregar_nodo(
        self, 
        nombre: str, 
        tipo: str, 
        atributos: Optional[Dict] = None
    ):
        """
        Agrega un nodo al grafo.
        
        Args:
            nombre: Nombre del nodo
            tipo: 'autor', 'concepto', 'norma', 'caso', 'doctrina'
            atributos: Diccionario con atributos adicionales
        """
        if not self.grafo.has_node(nombre):
            attrs = atributos or {}
            attrs['tipo'] = tipo
            self.grafo.add_node(nombre, **attrs)
            self.n_nodos += 1
    
    def agregar_relacion(
        self, 
        origen: str, 
        destino: str, 
        tipo_relacion: str,
        atributos: Optional[Dict] = None
    ):
        """
        Agrega una relación (arista) al grafo.
        
        Args:
            origen: Nodo origen
            destino: Nodo destino
            tipo_relacion: 'cita_a', 'desarrolla', 'aplica', 'contradice', 'fundamenta_con'
            atributos: Diccionario con atributos (ej: peso, año, contexto)
        """
        if not self.grafo.has_edge(origen, destino):
            attrs = atributos or {}
            attrs['tipo'] = tipo_relacion
            attrs['peso'] = attrs.get('peso', 1.0)
            self.grafo.add_edge(origen, destino, **attrs)
            self.n_relaciones += 1
        else:
            # Incrementar peso si ya existe
            self.grafo[origen][destino]['peso'] += 1
    
    def extraer_entidades_texto(self, texto: str) -> Dict[str, List[str]]:
        """
        Extrae entidades jurídicas de un texto.
        
        Args:
            texto: Texto a analizar
            
        Returns:
            Diccionario con listas de entidades por tipo
        """
        entidades = {
            'articulos': [],
            'leyes': [],
            'casos': [],
            'autores': [],
            'conceptos': [],
            'latinismos': []
        }
        
        # Artículos
        for match in self.patron_articulo.finditer(texto):
            art = match.group(1).strip()
            entidades['articulos'].append(art)
        
        # Leyes
        for match in self.patron_ley.finditer(texto):
            ley = f"Ley {match.group(1)}"
            entidades['leyes'].append(ley)
        
        # Casos
        for match in self.patron_caso.finditer(texto):
            caso = f"{match.group(1)} c/ {match.group(2)}"
            if len(caso) < 100:  # Filtrar falsos positivos
                entidades['casos'].append(caso)
        
        # Autores citados
        for match in self.patron_cita_autor.finditer(texto):
            autor = match.group(1).strip()
            if len(autor.split()) <= 3:  # Filtrar nombres demasiado largos
                entidades['autores'].append(autor)
        
        # Conceptos
        for match in self.patron_concepto.finditer(texto):
            concepto = match.group(1).strip().lower()
            entidades['conceptos'].append(concepto)
        
        # Latinismos
        for match in self.patron_latinismo.finditer(texto):
            latinismo = match.group(1).strip().lower()
            entidades['latinismos'].append(latinismo)
        
        # Eliminar duplicados manteniendo orden
        for key in entidades:
            entidades[key] = list(dict.fromkeys(entidades[key]))
        
        return entidades
    
    def construir_grafo_documento(
        self, 
        autor: str,
        texto: str,
        titulo: Optional[str] = None
    ):
        """
        Construye subgrafo para un documento específico.
        
        Args:
            autor: Autor del documento
            texto: Contenido del documento
            titulo: Título del documento (opcional)
        """
        # Agregar nodo del autor
        self.agregar_nodo(
            autor, 
            'autor',
            {'documentos': [titulo] if titulo else []}
        )
        
        # Extraer entidades
        entidades = self.extraer_entidades_texto(texto)
        
        # Agregar artículos como nodos
        for art in entidades['articulos']:
            self.agregar_nodo(art, 'norma', {'tipo_norma': 'articulo'})
            self.agregar_relacion(autor, art, 'cita_a', {'documento': titulo})
        
        # Agregar leyes
        for ley in entidades['leyes']:
            self.agregar_nodo(ley, 'norma', {'tipo_norma': 'ley'})
            self.agregar_relacion(autor, ley, 'cita_a', {'documento': titulo})
        
        # Agregar casos
        for caso in entidades['casos']:
            self.agregar_nodo(caso, 'caso', {})
            self.agregar_relacion(autor, caso, 'aplica', {'documento': titulo})
        
        # Agregar autores citados
        for autor_citado in entidades['autores']:
            if autor_citado.lower() != autor.lower():
                self.agregar_nodo(autor_citado, 'autor', {})
                self.agregar_relacion(autor, autor_citado, 'cita_a', {'documento': titulo})
        
        # Agregar conceptos
        for concepto in entidades['conceptos']:
            self.agregar_nodo(concepto, 'concepto', {})
            self.agregar_relacion(autor, concepto, 'desarrolla', {'documento': titulo})
        
        # Agregar latinismos
        for latinismo in entidades['latinismos']:
            self.agregar_nodo(latinismo, 'doctrina', {'tipo': 'latinismo'})
            self.agregar_relacion(autor, latinismo, 'fundamenta_con', {'documento': titulo})
    
    def cargar_desde_bd(self, limite: Optional[int] = None):
        """
        Carga documentos desde metadatos.db y construye el grafo.
        
        Args:
            limite: Número máximo de documentos a cargar (None = todos)
        """
        if not self.db_path or not Path(self.db_path).exists():
            print(f"⚠️  Base de datos no encontrada: {self.db_path}")
            return
        
        print(f"\n🔄 Cargando documentos desde {self.db_path}...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Cargar documentos
        query = "SELECT autor, texto_completo, titulo FROM perfiles_cognitivos"
        if limite:
            query += f" LIMIT {limite}"
        
        cursor.execute(query)
        documentos = cursor.fetchall()
        
        print(f"📚 Encontrados {len(documentos)} documentos")
        
        for i, (autor, texto, titulo) in enumerate(documentos, 1):
            if texto and autor:
                self.construir_grafo_documento(autor, texto, titulo)
                if i % 10 == 0:
                    print(f"   Procesados: {i}/{len(documentos)}")
        
        conn.close()
        
        print(f"\n✅ Grafo construido:")
        print(f"   🔵 Nodos: {self.n_nodos}")
        print(f"   🔗 Relaciones: {self.n_relaciones}")
    
    def consultar_relaciones(
        self, 
        nodo: str, 
        tipo_relacion: Optional[str] = None,
        direccion: str = 'saliente'
    ) -> List[Tuple[str, Dict]]:
        """
        Consulta relaciones de un nodo.
        
        Args:
            nodo: Nodo a consultar
            tipo_relacion: Filtrar por tipo ('cita_a', 'desarrolla', etc.)
            direccion: 'saliente' (desde nodo), 'entrante' (hacia nodo), 'ambas'
            
        Returns:
            Lista de tuplas (nodo_relacionado, atributos_relacion)
        """
        if not self.grafo.has_node(nodo):
            return []
        
        resultados = []
        
        # Relaciones salientes
        if direccion in ['saliente', 'ambas']:
            for destino in self.grafo.successors(nodo):
                attrs = self.grafo[nodo][destino]
                if tipo_relacion is None or attrs.get('tipo') == tipo_relacion:
                    resultados.append((destino, attrs))
        
        # Relaciones entrantes
        if direccion in ['entrante', 'ambas']:
            for origen in self.grafo.predecessors(nodo):
                attrs = self.grafo[origen][nodo]
                if tipo_relacion is None or attrs.get('tipo') == tipo_relacion:
                    resultados.append((origen, attrs))
        
        return resultados
    
    def quien_cita_a(self, nombre: str) -> List[str]:
        """
        ¿Quién cita a este autor/concepto/norma?
        
        Args:
            nombre: Nombre del nodo
            
        Returns:
            Lista de autores que lo citan
        """
        relaciones = self.consultar_relaciones(nombre, 'cita_a', 'entrante')
        return [r[0] for r in relaciones]
    
    def que_cita(self, autor: str) -> Dict[str, List[str]]:
        """
        ¿Qué cita este autor?
        
        Args:
            autor: Nombre del autor
            
        Returns:
            Diccionario con listas por tipo de entidad
        """
        relaciones = self.consultar_relaciones(autor, 'cita_a', 'saliente')
        
        resultado = {
            'autores': [],
            'normas': [],
            'casos': [],
            'conceptos': []
        }
        
        for nodo, _ in relaciones:
            if self.grafo.has_node(nodo):
                tipo = self.grafo.nodes[nodo].get('tipo', 'desconocido')
                if tipo == 'autor':
                    resultado['autores'].append(nodo)
                elif tipo == 'norma':
                    resultado['normas'].append(nodo)
                elif tipo == 'caso':
                    resultado['casos'].append(nodo)
                elif tipo == 'concepto':
                    resultado['conceptos'].append(nodo)
        
        return resultado
    
    def cadena_influencia(
        self, 
        origen: str, 
        destino: str,
        max_profundidad: int = 5
    ) -> List[List[str]]:
        """
        Encuentra cadenas de influencia entre dos autores.
        
        Args:
            origen: Autor origen
            destino: Autor destino
            max_profundidad: Profundidad máxima de búsqueda
            
        Returns:
            Lista de caminos (cada camino es una lista de nodos)
        """
        if not self.grafo.has_node(origen) or not self.grafo.has_node(destino):
            return []
        
        try:
            # Encontrar todos los caminos simples
            caminos = list(nx.all_simple_paths(
                self.grafo,
                origen,
                destino,
                cutoff=max_profundidad
            ))
            return caminos
        except nx.NetworkXNoPath:
            return []
    
    def autores_mas_citados(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Ranking de autores más citados.
        
        Args:
            top_n: Número de autores a retornar
            
        Returns:
            Lista de tuplas (autor, cantidad_citas)
        """
        citas_por_autor = defaultdict(int)
        
        for nodo in self.grafo.nodes():
            tipo = self.grafo.nodes[nodo].get('tipo')
            if tipo == 'autor':
                # Contar citas entrantes
                citas = len([
                    p for p in self.grafo.predecessors(nodo)
                    if self.grafo[p][nodo].get('tipo') == 'cita_a'
                ])
                if citas > 0:
                    citas_por_autor[nodo] = citas
        
        # Ordenar por cantidad de citas
        ranking = sorted(citas_por_autor.items(), key=lambda x: x[1], reverse=True)
        return ranking[:top_n]
    
    def normas_mas_aplicadas(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Ranking de normas más aplicadas/citadas.
        
        Args:
            top_n: Número de normas a retornar
            
        Returns:
            Lista de tuplas (norma, cantidad_aplicaciones)
        """
        aplicaciones = defaultdict(int)
        
        for nodo in self.grafo.nodes():
            tipo = self.grafo.nodes[nodo].get('tipo')
            if tipo == 'norma':
                # Contar aplicaciones/citas entrantes
                apps = len(list(self.grafo.predecessors(nodo)))
                if apps > 0:
                    aplicaciones[nodo] = apps
        
        ranking = sorted(aplicaciones.items(), key=lambda x: x[1], reverse=True)
        return ranking[:top_n]
    
    def exportar_gephi(self, archivo_salida: str):
        """
        Exporta el grafo en formato GEXF para visualización en Gephi.
        
        Args:
            archivo_salida: Ruta del archivo .gexf de salida
        """
        nx.write_gexf(self.grafo, archivo_salida)
        print(f"✅ Grafo exportado a {archivo_salida}")
    
    def exportar_json(self, archivo_salida: str):
        """
        Exporta el grafo en formato JSON.
        
        Args:
            archivo_salida: Ruta del archivo .json de salida
        """
        data = nx.node_link_data(self.grafo)
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Grafo exportado a {archivo_salida}")
    
    def estadisticas(self) -> Dict:
        """
        Genera estadísticas del grafo.
        
        Returns:
            Diccionario con estadísticas
        """
        stats = {
            'n_nodos': self.grafo.number_of_nodes(),
            'n_relaciones': self.grafo.number_of_edges(),
            'densidad': nx.density(self.grafo),
            'n_componentes': nx.number_weakly_connected_components(self.grafo),
            'nodos_por_tipo': Counter([
                self.grafo.nodes[n].get('tipo', 'desconocido')
                for n in self.grafo.nodes()
            ]),
            'relaciones_por_tipo': Counter([
                self.grafo[u][v].get('tipo', 'desconocida')
                for u, v in self.grafo.edges()
            ])
        }
        
        return stats


def demo_grafo_conocimiento():
    """
    Demostración del grafo de conocimiento.
    """
    print("="*70)
    print("🕸️  DEMO: GRAFO DE CONOCIMIENTO JURÍDICO")
    print("="*70)
    
    # Crear grafo
    db_path = Path("colaborative/bases_rag/cognitiva/metadatos.db")
    grafo = GrafoConocimientoJuridico(str(db_path))
    
    # Cargar documentos
    grafo.cargar_desde_bd(limite=20)
    
    # Estadísticas
    print("\n" + "="*70)
    print("📊 ESTADÍSTICAS DEL GRAFO")
    print("="*70)
    
    stats = grafo.estadisticas()
    print(f"\n🔵 Nodos totales: {stats['n_nodos']}")
    print(f"🔗 Relaciones totales: {stats['n_relaciones']}")
    print(f"📊 Densidad: {stats['densidad']:.4f}")
    print(f"🔀 Componentes conexas: {stats['n_componentes']}")
    
    print("\n📋 Nodos por tipo:")
    for tipo, cantidad in stats['nodos_por_tipo'].items():
        print(f"   {tipo:15s}: {cantidad:4d}")
    
    print("\n🔗 Relaciones por tipo:")
    for tipo, cantidad in stats['relaciones_por_tipo'].items():
        print(f"   {tipo:15s}: {cantidad:4d}")
    
    # Autores más citados
    print("\n" + "="*70)
    print("🏆 TOP AUTORES MÁS CITADOS")
    print("="*70)
    
    top_autores = grafo.autores_mas_citados(top_n=5)
    for i, (autor, citas) in enumerate(top_autores, 1):
        print(f"{i}. {autor:30s} ({citas} citas)")
    
    # Normas más aplicadas
    print("\n" + "="*70)
    print("📜 TOP NORMAS MÁS CITADAS")
    print("="*70)
    
    top_normas = grafo.normas_mas_aplicadas(top_n=5)
    for i, (norma, apps) in enumerate(top_normas, 1):
        print(f"{i}. {norma:30s} ({apps} aplicaciones)")
    
    # Exportar
    print("\n" + "="*70)
    print("💾 EXPORTANDO GRAFO")
    print("="*70)
    
    grafo.exportar_json("colaborative/bases_rag/cognitiva/grafo_conocimiento.json")
    grafo.exportar_gephi("colaborative/bases_rag/cognitiva/grafo_conocimiento.gexf")
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETADA")
    print("="*70)


if __name__ == "__main__":
    demo_grafo_conocimiento()
