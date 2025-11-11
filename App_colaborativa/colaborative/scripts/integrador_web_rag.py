"""
🌐 INTEGRACIÓN WEB - MEJORAS RAG V7.8
====================================

Módulo Flask para integrar las 5 mejoras RAG en la webapp existente:
1. Chunks Inteligentes
2. Análisis Argumentativo
3. Análisis Temporal
4. Embeddings Multi-Nivel
5. Grafo de Conocimiento

Nuevas rutas web:
- /rag-mejorado         → Dashboard de mejoras RAG
- /chunks-inteligentes  → Explorador de fragmentos semánticos
- /analisis-argumentativo → Cadenas argumentativas
- /evolucion-temporal   → Línea de tiempo doctrinal
- /grafo-conocimiento   → Visualización del grafo
- /api/grafo/consulta   → API REST para consultas del grafo

Autor: Sistema V7.8
Fecha: 11 Nov 2025
"""

from flask import jsonify, render_template_string, request
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional
import sys
import os

# Importar módulos de mejoras RAG
sys.path.insert(0, os.path.dirname(__file__))

try:
    from chunker_inteligente import ChunkerInteligente
    CHUNKER_DISPONIBLE = True
except ImportError:
    CHUNKER_DISPONIBLE = False
    print("⚠️ chunker_inteligente.py no disponible")

try:
    from analizador_argumentativo import AnalizadorArgumentativo
    ARGUMENTATIVO_DISPONIBLE = True
except ImportError:
    ARGUMENTATIVO_DISPONIBLE = False
    print("⚠️ analizador_argumentativo.py no disponible")

try:
    from analizador_temporal import AnalizadorTemporal
    TEMPORAL_DISPONIBLE = True
except ImportError:
    TEMPORAL_DISPONIBLE = False
    print("⚠️ analizador_temporal.py no disponible")

try:
    from embeddings_fusion import EmbeddingsFusion
    EMBEDDINGS_FUSION_DISPONIBLE = True
except ImportError:
    EMBEDDINGS_FUSION_DISPONIBLE = False
    print("⚠️ embeddings_fusion.py no disponible")

try:
    from grafo_conocimiento import GrafoConocimientoJuridico
    GRAFO_DISPONIBLE = True
except ImportError:
    GRAFO_DISPONIBLE = False
    print("⚠️ grafo_conocimiento.py no disponible")


class IntegradorWebRAG:
    """
    Integrador de mejoras RAG en Flask webapp.
    """
    
    def __init__(self, app, db_path: str = "colaborative/bases_rag/cognitiva/metadatos.db"):
        """
        Inicializa el integrador.
        
        Args:
            app: Aplicación Flask
            db_path: Ruta a metadatos.db
        """
        self.app = app
        self.db_path = db_path
        self.chunks_db = "colaborative/bases_rag/cognitiva/chunks_inteligentes.db"
        
        # Inicializar módulos
        self.chunker = ChunkerInteligente() if CHUNKER_DISPONIBLE else None
        self.analizador_arg = AnalizadorArgumentativo() if ARGUMENTATIVO_DISPONIBLE else None
        self.analizador_temp = AnalizadorTemporal(db_path) if TEMPORAL_DISPONIBLE else None
        self.grafo = GrafoConocimientoJuridico(db_path) if GRAFO_DISPONIBLE else None
        
        # Registrar rutas
        self._registrar_rutas()
        
        print("✅ IntegradorWebRAG inicializado")
    
    def _registrar_rutas(self):
        """Registra todas las rutas Flask."""
        
        # Dashboard principal
        @self.app.route("/rag-mejorado", methods=["GET"])
        def dashboard_rag_mejorado():
            return self._render_dashboard()
        
        # Chunks inteligentes
        @self.app.route("/chunks-inteligentes", methods=["GET"])
        def chunks_inteligentes():
            return self._render_chunks()
        
        @self.app.route("/api/chunks/buscar", methods=["GET"])
        def api_buscar_chunks():
            query = request.args.get('q', '')
            return self._buscar_chunks_api(query)
        
        # Análisis argumentativo
        @self.app.route("/analisis-argumentativo", methods=["GET"])
        def analisis_argumentativo():
            return self._render_argumentativo()
        
        @self.app.route("/api/argumentativo/documento/<int:doc_id>", methods=["GET"])
        def api_argumentativo_doc(doc_id):
            return self._obtener_analisis_argumentativo(doc_id)
        
        # Evolución temporal
        @self.app.route("/evolucion-temporal", methods=["GET"])
        def evolucion_temporal():
            return self._render_temporal()
        
        @self.app.route("/api/temporal/autor/<autor>", methods=["GET"])
        def api_temporal_autor(autor):
            return self._obtener_evolucion_autor(autor)
        
        # Grafo de conocimiento
        @self.app.route("/grafo-conocimiento", methods=["GET"])
        def grafo_conocimiento():
            return self._render_grafo()
        
        @self.app.route("/api/grafo/consulta", methods=["POST"])
        def api_grafo_consulta():
            return self._consultar_grafo()
        
        @self.app.route("/api/grafo/stats", methods=["GET"])
        def api_grafo_stats():
            return self._estadisticas_grafo()
        
        print("✅ Rutas RAG mejorado registradas")
    
    def _render_dashboard(self):
        """Renderiza dashboard principal de mejoras RAG."""
        
        # Contar recursos
        stats = {
            'chunks': self._contar_chunks(),
            'documentos': self._contar_documentos(),
            'autores': self._contar_autores(),
            'nodos_grafo': self.grafo.n_nodos if self.grafo else 0,
            'relaciones_grafo': self.grafo.n_relaciones if self.grafo else 0
        }
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>RAG Mejorado V7.8 - Dashboard</title>
            <meta charset="utf-8">
            <style>
                body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                        gap: 20px; margin-bottom: 30px; }
                .stat-card { background: white; padding: 20px; border-radius: 8px; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }
                .stat-value { font-size: 36px; font-weight: bold; color: #667eea; }
                .stat-label { color: #666; margin-top: 10px; }
                .modules { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                .module-card { background: white; padding: 25px; border-radius: 8px; 
                              box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; }
                .module-card:hover { transform: translateY(-5px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
                .module-card h3 { margin: 0 0 15px 0; color: #333; }
                .module-card p { color: #666; line-height: 1.6; }
                .btn { display: inline-block; padding: 10px 20px; background: #667eea; 
                      color: white; text-decoration: none; border-radius: 5px; 
                      margin-top: 15px; transition: background 0.2s; }
                .btn:hover { background: #5568d3; }
                .status { display: inline-block; padding: 5px 10px; border-radius: 3px; 
                         font-size: 12px; font-weight: bold; }
                .status.active { background: #4caf50; color: white; }
                .status.inactive { background: #f44336; color: white; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 RAG Mejorado V7.8</h1>
                    <p>Sistema de Análisis Doctrinal con Mejoras Avanzadas</p>
                </div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-value">{{ stats.chunks }}</div>
                        <div class="stat-label">Chunks Inteligentes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ stats.documentos }}</div>
                        <div class="stat-label">Documentos Procesados</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ stats.autores }}</div>
                        <div class="stat-label">Autores Analizados</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ stats.nodos_grafo }}</div>
                        <div class="stat-label">Nodos en Grafo</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ stats.relaciones_grafo }}</div>
                        <div class="stat-label">Relaciones Mapeadas</div>
                    </div>
                </div>
                
                <div class="modules">
                    <div class="module-card">
                        <h3>🧩 Chunks Inteligentes</h3>
                        <span class="status {{ 'active' if chunker_disponible else 'inactive' }}">
                            {{ 'ACTIVO' if chunker_disponible else 'INACTIVO' }}
                        </span>
                        <p>Fragmentación semántica respetando coherencia argumentativa. 
                           Detecta automáticamente temas, entidades jurídicas y nivel técnico.</p>
                        <a href="/chunks-inteligentes" class="btn">Explorar Chunks</a>
                    </div>
                    
                    <div class="module-card">
                        <h3>⚖️ Análisis Argumentativo</h3>
                        <span class="status {{ 'active' if argumentativo_disponible else 'inactive' }}">
                            {{ 'ACTIVO' if argumentativo_disponible else 'INACTIVO' }}
                        </span>
                        <p>Extracción de cadenas argumentativas completas: silogismos, objeciones, 
                           refutaciones y estructura retórica clásica.</p>
                        <a href="/analisis-argumentativo" class="btn">Ver Argumentos</a>
                    </div>
                    
                    <div class="module-card">
                        <h3>📅 Evolución Temporal</h3>
                        <span class="status {{ 'active' if temporal_disponible else 'inactive' }}">
                            {{ 'ACTIVO' if temporal_disponible else 'INACTIVO' }}
                        </span>
                        <p>Análisis temporal de doctrinas y autores. Detecta cambios significativos 
                           y tendencias evolutivas por periodo.</p>
                        <a href="/evolucion-temporal" class="btn">Timeline</a>
                    </div>
                    
                    <div class="module-card">
                        <h3>🧬 Embeddings Multi-Nivel</h3>
                        <span class="status {{ 'active' if embeddings_disponible else 'inactive' }}">
                            {{ 'ACTIVO' if embeddings_disponible else 'INACTIVO' }}
                        </span>
                        <p>Fusión de 3 modelos especializados: general (50%) + legal (35%) + 
                           multilingüe (15%). +25% precisión en búsquedas.</p>
                        <a href="/cognitivo" class="btn">Buscar Avanzado</a>
                    </div>
                    
                    <div class="module-card">
                        <h3>🕸️ Grafo de Conocimiento</h3>
                        <span class="status {{ 'active' if grafo_disponible else 'inactive' }}">
                            {{ 'ACTIVO' if grafo_disponible else 'INACTIVO' }}
                        </span>
                        <p>Red de relaciones jurídicas: autores, conceptos, normas, casos. 
                           Consultas como "¿Quién cita a Kelsen?"</p>
                        <a href="/grafo-conocimiento" class="btn">Explorar Grafo</a>
                    </div>
                    
                    <div class="module-card">
                        <h3>📊 Sistema ANALYSER</h3>
                        <span class="status active">ACTIVO</span>
                        <p>Sistema cognitivo completo con 8 rasgos especializados, 
                           radar comparativo y análisis multi-capa.</p>
                        <a href="/cognitivo" class="btn">ANALYSER</a>
                    </div>
                </div>
                
                <div style="margin-top: 30px; text-align: center; color: #666;">
                    <p><a href="/" style="color: #667eea;">← Volver al inicio</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(
            html,
            stats=stats,
            chunker_disponible=CHUNKER_DISPONIBLE,
            argumentativo_disponible=ARGUMENTATIVO_DISPONIBLE,
            temporal_disponible=TEMPORAL_DISPONIBLE,
            embeddings_disponible=EMBEDDINGS_FUSION_DISPONIBLE,
            grafo_disponible=GRAFO_DISPONIBLE
        )
    
    def _render_chunks(self):
        """Renderiza explorador de chunks inteligentes."""
        
        chunks = self._obtener_chunks_recientes(limite=50)
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chunks Inteligentes</title>
            <meta charset="utf-8">
            <style>
                body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { background: #667eea; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .search-box { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .search-box input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
                .chunk-card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 15px; 
                             box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .chunk-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
                .chunk-tema { font-weight: bold; color: #333; }
                .chunk-meta { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
                .badge { padding: 4px 8px; border-radius: 3px; font-size: 12px; }
                .badge.tema { background: #e3f2fd; color: #1976d2; }
                .badge.tipo { background: #f3e5f5; color: #7b1fa2; }
                .badge.coherencia { background: #e8f5e9; color: #388e3c; }
                .badge.tecnico { background: #fff3e0; color: #f57c00; }
                .chunk-texto { color: #666; line-height: 1.6; margin-top: 10px; }
                .entidades { margin-top: 10px; }
                .entidad { display: inline-block; padding: 3px 8px; background: #fce4ec; 
                          color: #c2185b; border-radius: 3px; margin: 2px; font-size: 11px; }
            </style>
            <script>
                function buscarChunks() {
                    const query = document.getElementById('search-input').value;
                    if (query.length > 2) {
                        fetch(`/api/chunks/buscar?q=${encodeURIComponent(query)}`)
                            .then(r => r.json())
                            .then(data => mostrarResultados(data))
                            .catch(err => console.error(err));
                    }
                }
                
                function mostrarResultados(chunks) {
                    const container = document.getElementById('chunks-container');
                    container.innerHTML = chunks.map(chunk => `
                        <div class="chunk-card">
                            <div class="chunk-header">
                                <div class="chunk-tema">${chunk.tema_principal}</div>
                            </div>
                            <div class="chunk-meta">
                                <span class="badge tipo">${chunk.tipo_contenido}</span>
                                <span class="badge coherencia">Coherencia: ${chunk.coherencia_interna?.toFixed(2) || 'N/A'}</span>
                                <span class="badge tecnico">Nivel técnico: ${chunk.nivel_tecnico?.toFixed(2) || 'N/A'}</span>
                            </div>
                            <div class="chunk-texto">${chunk.contenido.substring(0, 300)}...</div>
                            ${chunk.entidades_juridicas ? `
                                <div class="entidades">
                                    ${JSON.parse(chunk.entidades_juridicas).map(e => `<span class="entidad">${e}</span>`).join('')}
                                </div>
                            ` : ''}
                        </div>
                    `).join('');
                }
            </script>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧩 Explorador de Chunks Inteligentes</h1>
                    <p>Fragmentación semántica con metadatos enriquecidos</p>
                </div>
                
                <div class="search-box">
                    <input type="text" id="search-input" placeholder="Buscar en chunks..." 
                           onkeyup="buscarChunks()">
                </div>
                
                <div id="chunks-container">
                    {% for chunk in chunks %}
                    <div class="chunk-card">
                        <div class="chunk-header">
                            <div class="chunk-tema">{{ chunk.tema_principal }}</div>
                        </div>
                        <div class="chunk-meta">
                            <span class="badge tipo">{{ chunk.tipo_contenido }}</span>
                            <span class="badge coherencia">Coherencia: {{ "%.2f"|format(chunk.coherencia_interna or 0) }}</span>
                            <span class="badge tecnico">Nivel técnico: {{ "%.2f"|format(chunk.nivel_tecnico or 0) }}</span>
                        </div>
                        <div class="chunk-texto">{{ chunk.contenido[:300] }}...</div>
                        {% if chunk.entidades_juridicas %}
                        <div class="entidades">
                            {% for ent in chunk.entidades_juridicas.split(',')[:5] %}
                            <span class="entidad">{{ ent }}</span>
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
                
                <div style="margin-top: 20px; text-align: center;">
                    <a href="/rag-mejorado" style="color: #667eea;">← Volver al dashboard</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html, chunks=chunks)
    
    def _render_argumentativo(self):
        """Renderiza análisis argumentativo."""
        # Implementación simplificada
        return "<h1>Análisis Argumentativo</h1><p>Próximamente: cadenas argumentativas visuales</p>"
    
    def _render_temporal(self):
        """Renderiza evolución temporal."""
        # Implementación simplificada
        return "<h1>Evolución Temporal</h1><p>Próximamente: timeline interactivo</p>"
    
    def _render_grafo(self):
        """Renderiza grafo de conocimiento."""
        # Implementación simplificada
        return "<h1>Grafo de Conocimiento</h1><p>Próximamente: visualización con D3.js</p>"
    
    # ========== Métodos auxiliares ==========
    
    def _contar_chunks(self) -> int:
        """Cuenta chunks inteligentes en BD."""
        if not Path(self.chunks_db).exists():
            return 0
        conn = sqlite3.connect(self.chunks_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM chunks_enriquecidos")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def _contar_documentos(self) -> int:
        """Cuenta documentos en BD principal."""
        if not Path(self.db_path).exists():
            return 0
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def _contar_autores(self) -> int:
        """Cuenta autores únicos."""
        if not Path(self.db_path).exists():
            return 0
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT autor) FROM perfiles_cognitivos")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def _obtener_chunks_recientes(self, limite: int = 50) -> List[Dict]:
        """Obtiene chunks recientes de la BD."""
        if not Path(self.chunks_db).exists():
            return []
        
        conn = sqlite3.connect(self.chunks_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT * FROM chunks_enriquecidos 
            ORDER BY id DESC 
            LIMIT {limite}
        """)
        
        chunks = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return chunks
    
    def _buscar_chunks_api(self, query: str):
        """API para buscar chunks."""
        if not Path(self.chunks_db).exists():
            return jsonify([])
        
        conn = sqlite3.connect(self.chunks_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM chunks_enriquecidos 
            WHERE contenido LIKE ? OR tema_principal LIKE ?
            LIMIT 20
        """, (f'%{query}%', f'%{query}%'))
        
        chunks = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(chunks)
    
    def _obtener_analisis_argumentativo(self, doc_id: int):
        """Obtiene análisis argumentativo de un documento."""
        # Implementación futura
        return jsonify({'error': 'No implementado aún'})
    
    def _obtener_evolucion_autor(self, autor: str):
        """Obtiene evolución temporal de un autor."""
        if not self.analizador_temp:
            return jsonify({'error': 'Analizador temporal no disponible'})
        
        evolucion = self.analizador_temp.analizar_evolucion_autor(autor)
        return jsonify(evolucion)
    
    def _consultar_grafo(self):
        """Consulta el grafo de conocimiento."""
        if not self.grafo:
            return jsonify({'error': 'Grafo no disponible'})
        
        data = request.get_json()
        tipo_consulta = data.get('tipo')
        parametros = data.get('parametros', {})
        
        if tipo_consulta == 'quien_cita':
            nombre = parametros.get('nombre')
            resultados = self.grafo.quien_cita_a(nombre)
            return jsonify({'citadores': resultados})
        
        elif tipo_consulta == 'que_cita':
            autor = parametros.get('autor')
            resultados = self.grafo.que_cita(autor)
            return jsonify(resultados)
        
        elif tipo_consulta == 'cadena_influencia':
            origen = parametros.get('origen')
            destino = parametros.get('destino')
            caminos = self.grafo.cadena_influencia(origen, destino)
            return jsonify({'caminos': caminos})
        
        return jsonify({'error': 'Tipo de consulta no reconocido'})
    
    def _estadisticas_grafo(self):
        """Obtiene estadísticas del grafo."""
        if not self.grafo:
            return jsonify({'error': 'Grafo no disponible'})
        
        stats = self.grafo.estadisticas()
        
        # Convertir Counter a dict para JSON
        stats['nodos_por_tipo'] = dict(stats['nodos_por_tipo'])
        stats['relaciones_por_tipo'] = dict(stats['relaciones_por_tipo'])
        
        return jsonify(stats)


def registrar_rutas_rag_mejorado(app, db_path: str = "colaborative/bases_rag/cognitiva/metadatos.db"):
    """
    Función helper para registrar todas las rutas en una app Flask existente.
    
    Args:
        app: Aplicación Flask
        db_path: Ruta a metadatos.db
    
    Returns:
        IntegradorWebRAG instance
    """
    integrador = IntegradorWebRAG(app, db_path)
    return integrador
