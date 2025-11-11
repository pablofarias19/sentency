#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 VISUALIZADOR AUTOR-CÉNTRICO AVANZADO
========================================

Genera visualizaciones centradas en perfiles autorales, metodologías,
redes de influencia y comparativas cognitivas.

ENFOQUE:
- Mapas de metodologías autorales
- Redes de influencia inter-autoral
- Comparativas cognitivas dinámicas
- Evolución metodológica temporal

AUTOR: Sistema Cognitivo v4.0
FECHA: 9 NOV 2025
"""

import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import sqlite3
import networkx as nx
from typing import Dict, List, Any, Optional, Tuple
import json
from datetime import datetime

class VisualizadorAutorCentrico:
    """
    Sistema de visualización centrado en perfiles autorales
    """
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            # Usar ruta relativa al script actual
            script_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'colaborative'))
        self.base_dir = base_dir
        self.db_autor_centrico = os.path.join(self.base_dir, "bases_rag/cognitiva/autor_centrico.db")
        self.colores_metodologia = {
            'Formalista-Positivista': '#1f77b4',
            'Innovadora-Propositiva': '#ff7f0e', 
            'Empírico-Casuística': '#2ca02c',
            'Dogmática-Tradicional': '#d62728',
            'Ecléctica-Balanceada': '#9467bd'
        }
    
    def generar_mapa_metodologico_interactivo(self) -> str:
        """
        Genera mapa interactivo de metodologías autorales
        """
        try:
            conn = sqlite3.connect(self.db_autor_centrico)
            
            # Obtener datos de perfiles
            query = '''
            SELECT autor, metodologia_principal, uso_ethos, uso_pathos, uso_logos,
                   total_documentos, originalidad_score, coherencia_interna
            FROM perfiles_autorales_expandidos
            '''
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if df.empty:
                return "<p>⚠️ No hay datos de perfiles autorales disponibles</p>"
            
            # Crear scatter plot 3D de metodologías
            fig = go.Figure()
            
            for metodologia in df['metodologia_principal'].unique():
                if pd.isna(metodologia):
                    continue
                    
                subset = df[df['metodologia_principal'] == metodologia]
                
                fig.add_trace(go.Scatter3d(
                    x=subset['uso_ethos'],
                    y=subset['uso_pathos'], 
                    z=subset['uso_logos'],
                    mode='markers+text',
                    text=subset['autor'].apply(lambda x: x[:15] + '...' if len(x) > 15 else x),
                    textposition="top center",
                    name=metodologia,
                    marker=dict(
                        size=subset['total_documentos'] * 2 + 5,
                        color=self.colores_metodologia.get(metodologia, '#666666'),
                        opacity=0.7,
                        line=dict(width=2, color='white')
                    ),
                    hovertemplate="""
                    <b>%{text}</b><br>
                    Metodología: """ + metodologia + """<br>
                    Ethos: %{x:.3f}<br>
                    Pathos: %{y:.3f}<br>
                    Logos: %{z:.3f}<br>
                    Documentos: """ + subset['total_documentos'].astype(str) + """<br>
                    <extra></extra>
                    """
                ))
            
            fig.update_layout(
                title=dict(
                    text="🧠 Mapa Metodológico Autor-Céntrico 3D<br><sub>Posición Aristotélica: Ethos, Pathos, Logos</sub>",
                    font=dict(size=16, color='#2c3e50')
                ),
                scene=dict(
                    xaxis_title="ETHOS (Autoridad/Credibilidad)",
                    yaxis_title="PATHOS (Componente Emocional)",
                    zaxis_title="LOGOS (Estructura Lógica)",
                    bgcolor='rgba(240,240,240,0.1)'
                ),
                height=600,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02
                )
            )
            
            return fig.to_html(include_plotlyjs='inline', div_id="mapa_metodologico")
            
        except Exception as e:
            return f"<p>❌ Error generando mapa metodológico: {e}</p>"
    
    def generar_red_influencias_interactiva(self) -> str:
        """
        Genera red interactiva de influencias entre autores
        """
        try:
            conn = sqlite3.connect(self.db_autor_centrico)
            
            # Obtener comparativas con alta similitud
            query = '''
            SELECT autor_a, autor_b, similitud_metodologica
            FROM comparativas_autorales 
            WHERE similitud_metodologica > 0.6
            ORDER BY similitud_metodologica DESC
            '''
            df_conexiones = pd.read_sql_query(query, conn)
            
            # Obtener datos de autores
            query_autores = '''
            SELECT autor, metodologia_principal, total_documentos, uso_ethos, uso_pathos, uso_logos
            FROM perfiles_autorales_expandidos
            '''
            df_autores = pd.read_sql_query(query_autores, conn)
            conn.close()
            
            if df_conexiones.empty or df_autores.empty:
                return "<p>⚠️ No hay suficientes datos para generar red de influencias</p>"
            
            # Crear grafo con NetworkX
            G = nx.Graph()
            
            # Añadir nodos (autores)
            for _, autor in df_autores.iterrows():
                G.add_node(autor['autor'], 
                          metodologia=autor['metodologia_principal'],
                          documentos=autor['total_documentos'],
                          ethos=autor['uso_ethos'],
                          pathos=autor['uso_pathos'],
                          logos=autor['uso_logos'])
            
            # Añadir aristas (similitudes)
            for _, conexion in df_conexiones.iterrows():
                G.add_edge(conexion['autor_a'], conexion['autor_b'],
                          weight=conexion['similitud_metodologica'])
            
            # Calcular posiciones con layout spring
            pos = nx.spring_layout(G, k=3, iterations=50)
            
            # Crear trazas para aristas
            edge_trace = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                weight = G[edge[0]][edge[1]]['weight']
                
                edge_trace.append(go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=weight*3, color=f'rgba(100,100,100,{weight})'),
                    hoverinfo='none',
                    showlegend=False
                ))
            
            # Crear traza para nodos
            node_trace = go.Scatter(
                x=[pos[node][0] for node in G.nodes()],
                y=[pos[node][1] for node in G.nodes()],
                mode='markers+text',
                text=[node[:12] + '...' if len(node) > 12 else node for node in G.nodes()],
                textposition="middle center",
                textfont=dict(size=10, color='white'),
                marker=dict(
                    size=[G.nodes[node]['documentos']*3 + 15 for node in G.nodes()],
                    color=[self.colores_metodologia.get(G.nodes[node]['metodologia'], '#666666') 
                           for node in G.nodes()],
                    line=dict(width=2, color='white'),
                    opacity=0.8
                ),
                hovertemplate="""
                <b>%{text}</b><br>
                Metodología: """ + str([G.nodes[node]['metodologia'] for node in G.nodes()]) + """<br>
                Documentos: """ + str([G.nodes[node]['documentos'] for node in G.nodes()]) + """<br>
                Conexiones: """ + str([G.degree(node) for node in G.nodes()]) + """<br>
                <extra></extra>
                """,
                showlegend=False
            )
            
            # Crear figura
            fig = go.Figure()
            
            # Añadir aristas
            for trace in edge_trace:
                fig.add_trace(trace)
            
            # Añadir nodos
            fig.add_trace(node_trace)
            
            fig.update_layout(
                title=dict(
                    text="🕸️ Red de Influencias Metodológicas<br><sub>Similitud > 60% - Tamaño = Documentos</sub>",
                    font=dict(size=16, color='#2c3e50')
                ),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=60),
                annotations=[ dict(
                    text="Grosor de línea = Similitud metodológica",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    xanchor='left', yanchor='bottom',
                    font=dict(size=12, color='#666')
                )],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=600,
                plot_bgcolor='rgba(245,245,245,0.8)'
            )
            
            return fig.to_html(include_plotlyjs='inline', div_id="red_influencias")
            
        except Exception as e:
            return f"<p>❌ Error generando red de influencias: {e}</p>"
    
    def generar_comparativa_metodologica_detallada(self, autor_a: str, autor_b: str) -> str:
        """
        Genera comparativa detallada entre dos autores específicos
        """
        try:
            conn = sqlite3.connect(self.db_autor_centrico)
            
            # Obtener datos de ambos autores
            query = '''
            SELECT * FROM perfiles_autorales_expandidos 
            WHERE autor IN (?, ?)
            '''
            df_autores = pd.read_sql_query(query, conn, params=(autor_a, autor_b))
            
            # Obtener comparativa si existe
            query_comp = '''
            SELECT * FROM comparativas_autorales 
            WHERE (autor_a = ? AND autor_b = ?) OR (autor_a = ? AND autor_b = ?)
            '''
            df_comp = pd.read_sql_query(query_comp, conn, params=(autor_a, autor_b, autor_b, autor_a))
            
            conn.close()
            
            if len(df_autores) != 2:
                return f"<p>⚠️ No se encontraron datos para ambos autores: {autor_a}, {autor_b}</p>"
            
            # Crear subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[
                    'Perfil Aristotélico', 'Características Metodológicas',
                    'Métricas Comparativas', 'Convergencias y Divergencias'
                ],
                specs=[[{"type": "polar"}, {"type": "bar"}],
                       [{"type": "scatter"}, {"type": "table"}]]
            )
            
            # 1. Perfil Aristotélico (Polar)
            categorias = ['Ethos', 'Pathos', 'Logos']
            
            for i, autor_data in df_autores.iterrows():
                valores = [
                    autor_data['uso_ethos'] or 0,
                    autor_data['uso_pathos'] or 0, 
                    autor_data['uso_logos'] or 0
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=valores,
                    theta=categorias,
                    fill='toself',
                    name=autor_data['autor'][:20],
                    opacity=0.6
                ), row=1, col=1)
            
            # 2. Características Metodológicas (Bar)
            metodologias = [df_autores.iloc[0]['metodologia_principal'], 
                          df_autores.iloc[1]['metodologia_principal']]
            autores_nombres = [df_autores.iloc[0]['autor'][:15], 
                             df_autores.iloc[1]['autor'][:15]]
            
            fig.add_trace(go.Bar(
                x=autores_nombres,
                y=[1, 1],  # Placeholder
                text=metodologias,
                textposition='inside',
                marker_color=[self.colores_metodologia.get(m, '#666') for m in metodologias],
                showlegend=False
            ), row=1, col=2)
            
            # 3. Métricas Comparativas (Scatter)
            metricas = ['total_documentos', 'originalidad_score', 'coherencia_interna']
            for i, metrica in enumerate(metricas):
                valores_a = [df_autores.iloc[0][metrica] or 0]
                valores_b = [df_autores.iloc[1][metrica] or 0]
                
                fig.add_trace(go.Scatter(
                    x=valores_a,
                    y=[i],
                    mode='markers',
                    name=f"{autor_a[:10]} - {metrica}",
                    marker_size=10,
                    showlegend=False
                ), row=2, col=1)
                
                fig.add_trace(go.Scatter(
                    x=valores_b,
                    y=[i],
                    mode='markers', 
                    name=f"{autor_b[:10]} - {metrica}",
                    marker_size=10,
                    showlegend=False
                ), row=2, col=1)
            
            # 4. Tabla de comparación
            if not df_comp.empty:
                similitud = df_comp.iloc[0]['similitud_metodologica']
                tabla_data = [
                    ['Similitud Metodológica', f"{similitud:.3f}"],
                    ['Compatibilidad', 'Alta' if similitud > 0.7 else 'Media' if similitud > 0.5 else 'Baja']
                ]
            else:
                tabla_data = [
                    ['Similitud Metodológica', 'No calculada'],
                    ['Estado', 'Pendiente de análisis']
                ]
            
            fig.add_trace(go.Table(
                header=dict(values=['Métrica', 'Valor']),
                cells=dict(values=list(zip(*tabla_data)))
            ), row=2, col=2)
            
            fig.update_layout(
                title=f"🔍 Comparativa Metodológica: {autor_a[:20]} vs {autor_b[:20]}",
                height=800,
                showlegend=True
            )
            
            return fig.to_html(include_plotlyjs='inline', div_id="comparativa_detallada")
            
        except Exception as e:
            return f"<p>❌ Error en comparativa detallada: {e}</p>"
    
    def generar_dashboard_metodologias(self) -> str:
        """
        Genera dashboard completo de metodologías autorales
        """
        try:
            conn = sqlite3.connect(self.db_autor_centrico)
            
            # Datos principales
            df_autores = pd.read_sql_query('''
                SELECT metodologia_principal, COUNT(*) as cantidad,
                       AVG(uso_ethos) as avg_ethos,
                       AVG(uso_pathos) as avg_pathos,
                       AVG(uso_logos) as avg_logos,
                       SUM(total_documentos) as total_docs
                FROM perfiles_autorales_expandidos
                GROUP BY metodologia_principal
            ''', conn)
            
            conn.close()
            
            if df_autores.empty:
                return "<p>⚠️ No hay datos de metodologías disponibles</p>"
            
            # Crear dashboard con múltiples visualizaciones
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[
                    'Distribución de Metodologías', 'Perfil Aristotélico por Metodología',
                    'Productividad por Metodología', 'Índice de Especialización'
                ],
                specs=[[{"type": "pie"}, {"type": "bar"}],
                       [{"type": "scatter"}, {"type": "bar"}]]
            )
            
            # 1. Distribución (Pie)
            fig.add_trace(go.Pie(
                labels=df_autores['metodologia_principal'],
                values=df_autores['cantidad'],
                hole=0.4,
                textinfo='label+percent',
                marker_colors=[self.colores_metodologia.get(m, '#666') 
                              for m in df_autores['metodologia_principal']]
            ), row=1, col=1)
            
            # 2. Perfil Aristotélico (Bar agrupado)
            fig.add_trace(go.Bar(
                x=df_autores['metodologia_principal'],
                y=df_autores['avg_ethos'],
                name='Ethos',
                marker_color='rgba(31, 119, 180, 0.7)'
            ), row=1, col=2)
            
            fig.add_trace(go.Bar(
                x=df_autores['metodologia_principal'],
                y=df_autores['avg_pathos'],
                name='Pathos',
                marker_color='rgba(255, 127, 14, 0.7)'
            ), row=1, col=2)
            
            fig.add_trace(go.Bar(
                x=df_autores['metodologia_principal'],
                y=df_autores['avg_logos'],
                name='Logos',
                marker_color='rgba(44, 160, 44, 0.7)'
            ), row=1, col=2)
            
            # 3. Productividad (Scatter)
            fig.add_trace(go.Scatter(
                x=df_autores['cantidad'],
                y=df_autores['total_docs'],
                mode='markers+text',
                text=df_autores['metodologia_principal'],
                textposition='top center',
                marker=dict(
                    size=df_autores['total_docs']/10 + 10,
                    color=[self.colores_metodologia.get(m, '#666') 
                           for m in df_autores['metodologia_principal']],
                    opacity=0.7
                ),
                showlegend=False
            ), row=2, col=1)
            
            # 4. Índice de especialización
            especializacion = df_autores['total_docs'] / df_autores['cantidad']
            fig.add_trace(go.Bar(
                x=df_autores['metodologia_principal'],
                y=especializacion,
                marker_color=[self.colores_metodologia.get(m, '#666') 
                             for m in df_autores['metodologia_principal']],
                showlegend=False
            ), row=2, col=2)
            
            fig.update_layout(
                title="📊 Dashboard Metodologías Autor-Céntricas",
                height=800,
                showlegend=True
            )
            
            return fig.to_html(include_plotlyjs='inline', div_id="dashboard_metodologias")
            
        except Exception as e:
            return f"<p>❌ Error en dashboard: {e}</p>"

def generar_visualizacion_completa() -> str:
    """
    Genera página HTML completa con todas las visualizaciones autor-céntricas
    """
    viz = VisualizadorAutorCentrico()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>📊 Sistema Autor-Céntrico - Visualizaciones</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
            .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .visualization {{ margin: 30px 0; padding: 20px; border-radius: 10px; background: #f8f9fa; }}
            .description {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Sistema Autor-Céntrico de Análisis Cognitivo</h1>
                <p>Enfoque en metodologías, perfiles autorales y redes de influencia</p>
                <p><small>Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}</small></p>
            </div>
            
            <div class="visualization">
                <div class="description">
                    <h3>📊 Dashboard General de Metodologías</h3>
                    <p>Vista general de la distribución metodológica, perfiles aristotélicos y productividad por enfoque.</p>
                </div>
                {viz.generar_dashboard_metodologias()}
            </div>
            
            <div class="visualization">
                <div class="description">
                    <h3>🧠 Mapa Metodológico 3D</h3>
                    <p>Posicionamiento espacial de autores según sus características aristotélicas (Ethos, Pathos, Logos).</p>
                </div>
                {viz.generar_mapa_metodologico_interactivo()}
            </div>
            
            <div class="visualization">
                <div class="description">
                    <h3>🕸️ Red de Influencias Metodológicas</h3>
                    <p>Conexiones entre autores basadas en similitud metodológica. Líneas más gruesas = mayor similitud.</p>
                </div>
                {viz.generar_red_influencias_interactiva()}
            </div>
            
        </div>
    </body>
    </html>
    """
    
    return html

if __name__ == "__main__":
    # Generar visualización completa
    html_completo = generar_visualizacion_completa()
    
    # Guardar archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"visualizacion_autor_centrica_{timestamp}.html"
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(html_completo)
    
    print(f"✅ Visualización autor-céntrica generada: {nombre_archivo}")