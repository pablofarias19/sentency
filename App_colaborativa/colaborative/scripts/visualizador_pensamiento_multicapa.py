#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 VISUALIZADOR DE PENSAMIENTO AUTORAL MULTI-CAPA
=================================================

Visualizaciones especializadas en PENSAMIENTO PURO del autor:
- Mapas cognitivos de razonamiento
- Arquitectura argumentativa visual
- Evolución del pensamiento temporal
- Redes de influencia conceptual
- Firmas intelectuales comparativas

ENFOQUE: Mostrar CÓMO PIENSA el autor, no QUÉ dice.

AUTOR: Sistema Cognitivo v5.0 - Visualización Meta-Análisis
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
import math

class VisualizadorPensamientoMulticapa:
    """
    Visualizador especializado en pensamiento autoral multi-capa
    """
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            # Usar ruta relativa al script actual
            script_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'colaborative'))
        self.base_dir = base_dir
        self.db_multicapa = os.path.join(self.base_dir, "bases_rag/cognitiva/multicapa_pensamiento.db")
        
        # Colores para tipos de razonamiento
        self.colores_razonamiento = {
            'deductivo': '#1f77b4',      # Azul - Lógico
            'inductivo': '#ff7f0e',      # Naranja - Empírico
            'abductivo': '#2ca02c',      # Verde - Hipotético
            'analogico': '#d62728',      # Rojo - Comparativo
            'dialectico': '#9467bd'      # Morado - Sintético
        }
        
        # Colores para marcadores cognitivos
        self.colores_marcadores = {
            'certeza': '#e74c3c',
            'probabilidad': '#f39c12',
            'autoridad': '#8e44ad',
            'experiencia': '#27ae60',
            'reflexion': '#3498db'
        }
    
    def generar_mapa_cognitivo_razonamiento(self, autor: str) -> str:
        """
        Genera mapa cognitivo del patrón de razonamiento del autor
        """
        try:
            conn = sqlite3.connect(self.db_multicapa)
            
            query = '''
            SELECT distribucion_razonamiento, marcadores_cognitivos 
            FROM analisis_multicapa 
            WHERE autor = ?
            LIMIT 1
            '''
            
            result = pd.read_sql_query(query, conn, params=(autor,))
            conn.close()
            
            if result.empty:
                return f"<p>⚠️ No hay datos de razonamiento para {autor}</p>"
            
            # Parse JSON data
            distribucion = json.loads(result.iloc[0]['distribucion_razonamiento'])
            marcadores = json.loads(result.iloc[0]['marcadores_cognitivos'])
            
            # Crear subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[
                    'Mapa de Razonamiento Dominante', 'Patrones Cognitivos Detectados',
                    'Marcadores de Certeza vs Reflexión', 'Arquitectura Mental Global'
                ],
                specs=[[{"type": "polar"}, {"type": "bar"}],
                       [{"type": "scatter"}, {"type": "sunburst"}]]
            )
            
            # 1. Radar de razonamiento
            tipos = list(distribucion.keys())[:5]  # Top 5 tipos
            valores = [distribucion.get(tipo, 0) for tipo in tipos]
            
            fig.add_trace(go.Scatterpolar(
                r=valores,
                theta=tipos,
                fill='toself',
                name=f'Perfil {autor[:15]}',
                line_color='rgba(31, 119, 180, 0.8)',
                fillcolor='rgba(31, 119, 180, 0.3)'
            ), row=1, col=1)
            
            # 2. Barras de patrones cognitivos
            patron_counts = {k: len(v) for k, v in marcadores.items()}
            fig.add_trace(go.Bar(
                x=list(patron_counts.keys()),
                y=list(patron_counts.values()),
                marker_color=[self.colores_marcadores.get(k, '#666') for k in patron_counts.keys()],
                text=list(patron_counts.values()),
                textposition='auto',
                showlegend=False
            ), row=1, col=2)
            
            # 3. Scatter de certeza vs reflexión
            certeza_count = len(marcadores.get('certeza', []))
            reflexion_count = len(marcadores.get('reflexion', []))
            autoridad_count = len(marcadores.get('autoridad', []))
            
            fig.add_trace(go.Scatter(
                x=[certeza_count],
                y=[reflexion_count],
                mode='markers+text',
                text=[autor[:10]],
                textposition='top center',
                marker=dict(
                    size=autoridad_count * 5 + 20,
                    color='rgba(231, 76, 60, 0.7)',
                    line=dict(width=2, color='white')
                ),
                showlegend=False,
                hovertemplate=f"""
                <b>{autor}</b><br>
                Certeza: {certeza_count}<br>
                Reflexión: {reflexion_count}<br>
                Autoridad: {autoridad_count}<br>
                <extra></extra>
                """
            ), row=2, col=1)
            
            # 4. Sunburst de arquitectura mental
            sunburst_data = self._crear_datos_sunburst(distribucion, marcadores)
            
            fig.add_trace(go.Sunburst(
                labels=sunburst_data['labels'],
                parents=sunburst_data['parents'],
                values=sunburst_data['values'],
                branchvalues="total",
                hovertemplate='<b>%{label}</b><br>Valor: %{value}<extra></extra>',
                maxdepth=3
            ), row=2, col=2)
            
            fig.update_layout(
                title=f"🧠 Mapa Cognitivo Multi-Capa: {autor}",
                height=800,
                showlegend=True
            )
            
            return fig.to_html(include_plotlyjs='inline', div_id="mapa_cognitivo")
            
        except Exception as e:
            return f"<p>❌ Error generando mapa cognitivo: {e}</p>"
    
    def _crear_datos_sunburst(self, distribucion: Dict, marcadores: Dict) -> Dict[str, List]:
        """
        Crea datos para el gráfico sunburst de arquitectura mental
        """
        labels = ["Arquitectura Mental"]
        parents = [""]
        values = [1]
        
        # Nivel 1: Razonamiento y Marcadores
        labels.extend(["Razonamiento", "Marcadores Cognitivos"])
        parents.extend(["Arquitectura Mental", "Arquitectura Mental"])
        values.extend([0.6, 0.4])
        
        # Nivel 2: Tipos de razonamiento
        for tipo, valor in distribucion.items():
            if valor > 0.1:  # Solo mostrar valores significativos
                labels.append(tipo.title())
                parents.append("Razonamiento")
                values.append(valor * 0.6)
        
        # Nivel 2: Tipos de marcadores
        for tipo, lista in marcadores.items():
            if len(lista) > 0:
                labels.append(tipo.title())
                parents.append("Marcadores Cognitivos")
                values.append(len(lista) * 0.1)
        
        return {"labels": labels, "parents": parents, "values": values}
    
    def generar_arquitectura_argumentativa_visual(self, autor: str) -> str:
        """
        Visualiza la arquitectura argumentativa específica del autor
        """
        try:
            conn = sqlite3.connect(self.db_multicapa)
            
            query = '''
            SELECT estructura_argumentativa
            FROM analisis_multicapa 
            WHERE autor = ?
            LIMIT 1
            '''
            
            result = pd.read_sql_query(query, conn, params=(autor,))
            conn.close()
            
            if result.empty:
                return f"<p>⚠️ No hay datos de estructura argumentativa para {autor}</p>"
            
            estructura = json.loads(result.iloc[0]['estructura_argumentativa'])
            
            # Crear diagrama de flujo argumentativo
            fig = go.Figure()
            
            # Secuencia de desarrollo
            secuencia = estructura.get('secuencia_desarrollo', [])
            if secuencia:
                x_positions = list(range(len(secuencia)))
                y_position = [1] * len(secuencia)
                
                # Nodos de la secuencia
                fig.add_trace(go.Scatter(
                    x=x_positions,
                    y=y_position,
                    mode='markers+text',
                    text=secuencia,
                    textposition='top center',
                    marker=dict(
                        size=30,
                        color='rgba(52, 152, 219, 0.8)',
                        line=dict(width=2, color='white')
                    ),
                    name='Secuencia Argumentativa',
                    hovertemplate='<b>%{text}</b><br>Posición: %{x}<extra></extra>'
                ))
                
                # Conectores entre nodos
                for i in range(len(x_positions) - 1):
                    fig.add_shape(
                        type="line",
                        x0=x_positions[i], y0=y_position[i],
                        x1=x_positions[i+1], y1=y_position[i+1],
                        line=dict(color="rgba(52, 152, 219, 0.6)", width=3, dash="dash")
                    )
            
            # Agregar información de patrones
            patron_intro = estructura.get('patron_introduccion', 'indefinido')
            estilo_conclusion = estructura.get('estilo_conclusion', 'indefinido')
            
            # Nodo de introducción
            fig.add_trace(go.Scatter(
                x=[-1],
                y=[1],
                mode='markers+text',
                text=[f'Intro: {patron_intro}'],
                textposition='middle left',
                marker=dict(size=25, color='rgba(46, 204, 113, 0.8)'),
                name='Patrón Introducción',
                showlegend=False
            ))
            
            # Nodo de conclusión
            fig.add_trace(go.Scatter(
                x=[len(secuencia)],
                y=[1],
                mode='markers+text',
                text=[f'Concl: {estilo_conclusion}'],
                textposition='middle right',
                marker=dict(size=25, color='rgba(231, 76, 60, 0.8)'),
                name='Estilo Conclusión',
                showlegend=False
            ))
            
            # Información adicional
            densidad = estructura.get('densidad_argumentativa', 0)
            uso_evidencia = estructura.get('uso_evidencia', {})
            
            fig.add_annotation(
                x=len(secuencia)/2,
                y=1.5,
                text=f"Densidad Argumentativa: {densidad:.2f}",
                showarrow=False,
                font=dict(size=12, color="darkblue")
            )
            
            # Mostrar tipos de evidencia como barras laterales
            if uso_evidencia:
                evidencia_text = "<br>".join([f"{k}: {v:.2f}" for k, v in uso_evidencia.items()])
                fig.add_annotation(
                    x=len(secuencia)/2,
                    y=0.3,
                    text=f"Uso de Evidencia:<br>{evidencia_text}",
                    showarrow=False,
                    font=dict(size=10, color="darkgreen"),
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="green",
                    borderwidth=1
                )
            
            fig.update_layout(
                title=f"🏗️ Arquitectura Argumentativa: {autor}",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 2]),
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(248, 249, 250, 0.8)'
            )
            
            return fig.to_html(include_plotlyjs='inline', div_id="arquitectura_argumentativa")
            
        except Exception as e:
            return f"<p>❌ Error en arquitectura argumentativa: {e}</p>"
    
    def generar_comparativa_firmas_intelectuales(self, autor_a: str, autor_b: str) -> str:
        """
        Compara las firmas intelectuales de dos autores
        """
        try:
            conn = sqlite3.connect(self.db_multicapa)
            
            query = '''
            SELECT autor, originalidad_lingüística, originalidad_conceptual, 
                   originalidad_metodologica, conceptos_centrales, marcadores_estilísticos
            FROM firmas_intelectuales 
            WHERE autor IN (?, ?)
            '''
            
            df = pd.read_sql_query(query, conn, params=(autor_a, autor_b))
            conn.close()
            
            if len(df) != 2:
                return f"<p>⚠️ No se encontraron firmas completas para ambos autores</p>"
            
            # Crear comparativa visual
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[
                    'Originalidad Comparativa', 'Conceptos Centrales',
                    'Marcadores Estilísticos', 'Perfil Integrado'
                ],
                specs=[[{"type": "bar"}, {"type": "scatter"}],
                       [{"type": "bar"}, {"type": "polar"}]]
            )
            
            # 1. Barras de originalidad
            categorias = ['Lingüística', 'Conceptual', 'Metodológica']
            
            for i, autor_data in df.iterrows():
                valores = [
                    autor_data['originalidad_lingüística'],
                    autor_data['originalidad_conceptual'],
                    autor_data['originalidad_metodologica']
                ]
                
                fig.add_trace(go.Bar(
                    x=categorias,
                    y=valores,
                    name=autor_data['autor'][:15],
                    text=[f"{v:.3f}" for v in valores],
                    textposition='auto'
                ), row=1, col=1)
            
            # 2. Scatter de conceptos centrales
            for i, autor_data in df.iterrows():
                conceptos = json.loads(autor_data['conceptos_centrales'] or '[]')
                
                fig.add_trace(go.Scatter(
                    x=[i],
                    y=[len(conceptos)],
                    mode='markers+text',
                    text=[autor_data['autor'][:10]],
                    textposition='top center',
                    marker=dict(
                        size=len(conceptos) * 10 + 20,
                        opacity=0.7
                    ),
                    name=f"Conceptos {autor_data['autor'][:10]}",
                    showlegend=False,
                    hovertemplate=f"""
                    <b>{autor_data['autor']}</b><br>
                    Conceptos: {len(conceptos)}<br>
                    Lista: {', '.join(conceptos[:3])}...<br>
                    <extra></extra>
                    """
                ), row=1, col=2)
            
            # 3. Marcadores estilísticos
            for i, autor_data in df.iterrows():
                marcadores = json.loads(autor_data['marcadores_estilísticos'] or '[]')
                
                fig.add_trace(go.Bar(
                    x=[autor_data['autor'][:10]],
                    y=[len(marcadores)],
                    name=f"Marcadores {autor_data['autor'][:10]}",
                    text=len(marcadores),
                    textposition='auto',
                    showlegend=False
                ), row=2, col=1)
            
            # 4. Perfil polar integrado
            for i, autor_data in df.iterrows():
                valores_polares = [
                    autor_data['originalidad_lingüística'],
                    autor_data['originalidad_conceptual'],
                    autor_data['originalidad_metodologica'],
                    len(json.loads(autor_data['conceptos_centrales'] or '[]')) / 10.0,
                    len(json.loads(autor_data['marcadores_estilísticos'] or '[]')) / 10.0
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=valores_polares,
                    theta=['Lingüística', 'Conceptual', 'Metodológica', 'Conceptos', 'Marcadores'],
                    fill='toself',
                    name=autor_data['autor'][:15],
                    opacity=0.6
                ), row=2, col=2)
            
            fig.update_layout(
                title=f"🎭 Comparativa de Firmas Intelectuales: {autor_a[:15]} vs {autor_b[:15]}",
                height=800,
                showlegend=True
            )
            
            return fig.to_html(include_plotlyjs='inline', div_id="comparativa_firmas")
            
        except Exception as e:
            return f"<p>❌ Error en comparativa de firmas: {e}</p>"
    
    def generar_evolucion_pensamiento_temporal(self, autor: str) -> str:
        """
        Visualiza la evolución temporal del pensamiento del autor
        """
        try:
            conn = sqlite3.connect(self.db_multicapa)
            
            # Obtener datos temporales
            query = '''
            SELECT documento, fecha_analisis, distribucion_razonamiento,
                   patron_razonamiento_dominante
            FROM analisis_multicapa 
            WHERE autor = ?
            ORDER BY fecha_analisis
            '''
            
            df = pd.read_sql_query(query, conn, params=(autor,))
            conn.close()
            
            if df.empty:
                return f"<p>⚠️ No hay datos temporales para {autor}</p>"
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=[
                    'Evolución de Patrones de Razonamiento',
                    'Dominancia de Patrón a lo Largo del Tiempo'
                ],
                vertical_spacing=0.15
            )
            
            # 1. Línea temporal de evolución
            fechas = pd.to_datetime(df['fecha_analisis'])
            patrones_dominantes = df['patron_razonamiento_dominante']
            
            # Crear serie temporal
            patron_counts = {}
            for i, (fecha, patron) in enumerate(zip(fechas, patrones_dominantes)):
                if patron not in patron_counts:
                    patron_counts[patron] = []
                patron_counts[patron].append((fecha, i))
            
            for patron, puntos in patron_counts.items():
                fechas, indices = zip(*puntos)
                fig.add_trace(go.Scatter(
                    x=list(fechas),
                    y=list(indices),
                    mode='lines+markers',
                    name=patron.title(),
                    line=dict(color=self.colores_razonamiento.get(patron, '#666')),
                    marker=dict(size=8)
                ), row=1, col=1)
            
            # 2. Heatmap de distribución temporal
            distribuciones = []
            for dist_json in df['distribucion_razonamiento']:
                try:
                    dist = json.loads(dist_json)
                    distribuciones.append(dist)
                except:
                    distribuciones.append({})
            
            if distribuciones:
                # Crear matriz para heatmap
                todos_patrones = set()
                for dist in distribuciones:
                    todos_patrones.update(dist.keys())
                
                patrones_lista = sorted(list(todos_patrones))
                matriz = []
                
                for dist in distribuciones:
                    fila = [dist.get(patron, 0) for patron in patrones_lista]
                    matriz.append(fila)
                
                fig.add_trace(go.Heatmap(
                    z=matriz,
                    x=patrones_lista,
                    y=[f"Doc {i+1}" for i in range(len(matriz))],
                    colorscale='Viridis',
                    showscale=True
                ), row=2, col=1)
            
            fig.update_layout(
                title=f"⏰ Evolución Temporal del Pensamiento: {autor}",
                height=700,
                showlegend=True
            )
            
            return fig.to_html(include_plotlyjs='inline', div_id="evolucion_temporal")
            
        except Exception as e:
            return f"<p>❌ Error en evolución temporal: {e}</p>"
    
    def generar_red_influencia_conceptual(self, autor: str) -> str:
        """
        Genera red de influencias conceptuales del autor
        """
        try:
            conn = sqlite3.connect(self.db_multicapa)
            
            query = '''
            SELECT conceptos_centrales, autores_citados, conceptos_compartidos
            FROM analisis_multicapa 
            WHERE autor = ?
            LIMIT 1
            '''
            
            result = pd.read_sql_query(query, conn, params=(autor,))
            conn.close()
            
            if result.empty:
                return f"<p>⚠️ No hay datos de red conceptual para {autor}</p>"
            
            # Parse datos
            conceptos = json.loads(result.iloc[0]['conceptos_centrales'] or '[]')
            autores_citados = json.loads(result.iloc[0]['autores_citados'] or '[]')
            conceptos_compartidos = json.loads(result.iloc[0]['conceptos_compartidos'] or '{}')
            
            # Crear red con NetworkX
            G = nx.Graph()
            
            # Nodo central del autor
            G.add_node(autor, tipo='autor_central', size=50, color='red')
            
            # Agregar conceptos como nodos
            for concepto in conceptos[:10]:  # Limitar a 10 conceptos principales
                G.add_node(concepto, tipo='concepto', size=30, color='blue')
                G.add_edge(autor, concepto, weight=1.0, tipo='desarrolla')
            
            # Agregar autores citados
            for autor_citado in autores_citados[:5]:  # Limitar a 5 autores
                G.add_node(autor_citado, tipo='autor_citado', size=25, color='green')
                G.add_edge(autor, autor_citado, weight=0.7, tipo='cita')
            
            # Calcular posiciones
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            # Crear trazas de aristas
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
            
            # Crear traza de nodos
            node_trace = go.Scatter(
                x=[pos[node][0] for node in G.nodes()],
                y=[pos[node][1] for node in G.nodes()],
                mode='markers+text',
                text=[node[:15] + '...' if len(node) > 15 else node for node in G.nodes()],
                textposition="middle center",
                textfont=dict(size=8),
                marker=dict(
                    size=[G.nodes[node].get('size', 20) for node in G.nodes()],
                    color=[{
                        'autor_central': 'rgba(231, 76, 60, 0.8)',
                        'concepto': 'rgba(52, 152, 219, 0.8)',
                        'autor_citado': 'rgba(46, 204, 113, 0.8)'
                    }.get(G.nodes[node].get('tipo', ''), 'rgba(149, 165, 166, 0.8)') for node in G.nodes()],
                    line=dict(width=2, color='white'),
                    opacity=0.8
                ),
                hovertemplate="""
                <b>%{text}</b><br>
                Tipo: """ + str([G.nodes[node].get('tipo', 'indefinido') for node in G.nodes()]) + """<br>
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
                title=f"🕸️ Red de Influencia Conceptual: {autor}",
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=60),
                annotations=[
                    dict(
                        text="Rojo=Autor Central, Azul=Conceptos, Verde=Autores Citados",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002,
                        xanchor='left', yanchor='bottom',
                        font=dict(size=10, color='#666')
                    )
                ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=600,
                plot_bgcolor='rgba(245,245,245,0.8)'
            )
            
            return fig.to_html(include_plotlyjs='inline', div_id="red_conceptual")
            
        except Exception as e:
            return f"<p>❌ Error en red conceptual: {e}</p>"

def generar_dashboard_pensamiento_completo(autor: str) -> str:
    """
    Genera dashboard completo de análisis de pensamiento multi-capa
    """
    viz = VisualizadorPensamientoMulticapa()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧠 Análisis de Pensamiento Multi-Capa: {autor}</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
            .container {{ max-width: 1600px; margin: 0 auto; background: white; border-radius: 15px; 
                        padding: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 40px; background: linear-gradient(135deg, #3498db, #9b59b6); 
                      color: white; padding: 20px; border-radius: 10px; }}
            .visualization {{ margin: 30px 0; padding: 20px; border-radius: 10px; background: #f8f9fa; 
                            border-left: 5px solid #3498db; }}
            .description {{ background: #e8f4fd; padding: 15px; border-radius: 8px; margin-bottom: 20px; 
                          border: 1px solid #bee5eb; }}
            .meta-info {{ background: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0; 
                        border: 1px solid #ffeaa7; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Análisis Multi-Capa de Pensamiento Autoral</h1>
                <h2>{autor}</h2>
                <p>Visualización del PENSAMIENTO PURO: Cómo piensa, razona y construye argumentos</p>
                <div class="meta-info">
                    <strong>Enfoque:</strong> Meta-análisis cognitivo • <strong>Capas:</strong> 5 niveles • 
                    <strong>Generado:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </div>
            </div>
            
            <div class="visualization">
                <div class="description">
                    <h3>🧠 Mapa Cognitivo de Razonamiento Multi-Dimensional</h3>
                    <p><strong>CAPA 2:</strong> Patrones de razonamiento dominantes, marcadores cognitivos y arquitectura mental global.</p>
                </div>
                {viz.generar_mapa_cognitivo_razonamiento(autor)}
            </div>
            
            <div class="visualization">
                <div class="description">
                    <h3>🏗️ Arquitectura Argumentativa Visual</h3>
                    <p><strong>CAPA 3:</strong> Estructura metodológica: cómo introduce, desarrolla y concluye sus argumentos.</p>
                </div>
                {viz.generar_arquitectura_argumentativa_visual(autor)}
            </div>
            
            <div class="visualization">
                <div class="description">
                    <h3>⏰ Evolución Temporal del Pensamiento</h3>
                    <p><strong>CAPA 4:</strong> Cambios y evolución en patrones de razonamiento a través del tiempo.</p>
                </div>
                {viz.generar_evolucion_pensamiento_temporal(autor)}
            </div>
            
            <div class="visualization">
                <div class="description">
                    <h3>🕸️ Red de Influencia Conceptual</h3>
                    <p><strong>CAPA 5:</strong> Conexiones conceptuales, autores citados y red de influencias intelectuales.</p>
                </div>
                {viz.generar_red_influencia_conceptual(autor)}
            </div>
            
            <div style="text-align: center; margin: 40px 0; padding: 20px; background: #e8f5e8; border-radius: 10px;">
                <h3>🎯 Resumen del Análisis Multi-Capa</h3>
                <p>Este análisis se centra en el <strong>PENSAMIENTO PURO</strong> del autor, no en el contenido semántico.</p>
                <ul style="text-align: left; display: inline-block;">
                    <li><strong>CAPA 1:</strong> Base semántica (contenido existente)</li>
                    <li><strong>CAPA 2:</strong> Patrones cognitivos de razonamiento</li>
                    <li><strong>CAPA 3:</strong> Arquitectura metodológica argumentativa</li>
                    <li><strong>CAPA 4:</strong> Evolución temporal del pensamiento</li>
                    <li><strong>CAPA 5:</strong> Redes de influencia conceptual</li>
                </ul>
            </div>
            
        </div>
    </body>
    </html>
    """
    
    return html

if __name__ == "__main__":
    # Ejemplo de uso
    autor = "Carlos Pandiella Molina"
    html_dashboard = generar_dashboard_pensamiento_completo(autor)
    
    # Guardar archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"pensamiento_multicapa_{autor.replace(' ', '_')}_{timestamp}.html"
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(html_dashboard)
    
    print(f"✅ Dashboard de pensamiento multi-capa generado: {nombre_archivo}")