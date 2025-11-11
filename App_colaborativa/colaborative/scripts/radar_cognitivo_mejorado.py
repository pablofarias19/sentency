#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 RADAR COGNITIVO MEJORADO CON EXPLICACIONES DETALLADAS
========================================================

Versión mejorada que incluye:
- Visualización radar tradicional
- Explicaciones textuales detalladas
- Interpretaciones por dimensión
- Recomendaciones basadas en el perfil
- Informes completos por escrito

AUTOR: Sistema Cognitivo v5.0 - Radar Mejorado
FECHA: 9 NOV 2025
"""

import os
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path
from datetime import datetime

# ----------------------------------------------------------
# CONFIGURACIÓN DE RUTAS
# ----------------------------------------------------------
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "data" / "perfiles.db"

def interpretar_dimension(dimension: str, valor: float) -> dict:
    """Interpreta una dimensión cognitiva específica"""
    
    interpretaciones = {
        "formalismo": {
            "bajo": (0.0, 0.3, "Enfoque flexible y contextual. Prefiere adaptarse a las circunstancias específicas antes que seguir reglas rígidas."),
            "medio": (0.3, 0.7, "Balance entre estructura y flexibilidad. Aplica principios formales cuando es necesario, pero se adapta al contexto."),
            "alto": (0.7, 1.0, "Enfoque altamente estructurado. Prefiere marcos conceptuales claros, definiciones precisas y razonamiento sistemático.")
        },
        "creatividad": {
            "bajo": (0.0, 0.3, "Enfoque conservador y tradicional. Prefiere soluciones probadas y enfoques establecidos."),
            "medio": (0.3, 0.7, "Creatividad moderada. Combina enfoques tradicionales con ideas innovadoras cuando es apropiado."),
            "alto": (0.7, 1.0, "Altamente creativo e innovador. Busca constantemente nuevas perspectivas y enfoques originales.")
        },
        "dogmatismo": {
            "bajo": (0.0, 0.3, "Mente abierta y flexible. Dispuesto a considerar múltiples perspectivas y cambiar de opinión."),
            "medio": (0.3, 0.7, "Firmeza moderada en las convicciones. Mantiene principios core pero está abierto al diálogo."),
            "alto": (0.7, 1.0, "Convicciones muy firmes. Tiende a mantener posiciones establecidas y resistir cambios de perspectiva.")
        },
        "empirismo": {
            "bajo": (0.0, 0.3, "Enfoque más teórico y conceptual. Prefiere razonamiento abstracto sobre evidencia empírica."),
            "medio": (0.3, 0.7, "Balance entre teoría y práctica. Usa tanto conceptos teóricos como evidencia empírica."),
            "alto": (0.7, 1.0, "Fuertemente orientado a la evidencia. Prefiere datos concretos y experiencia práctica.")
        },
        "interdisciplinariedad": {
            "bajo": (0.0, 0.3, "Enfoque especializado. Se concentra profundamente en su área de expertise."),
            "medio": (0.3, 0.7, "Integración moderada. Conecta su área con otras disciplinas cuando es relevante."),
            "alto": (0.7, 1.0, "Altamente interdisciplinario. Integra constantemente perspectivas de múltiples campos.")
        },
        "nivel_abstraccion": {
            "bajo": (0.0, 0.3, "Enfoque concreto y práctico. Prefiere ejemplos específicos y aplicaciones directas."),
            "medio": (0.3, 0.7, "Balance entre abstracto y concreto. Maneja tanto conceptos teóricos como aplicaciones prácticas."),
            "alto": (0.7, 1.0, "Altamente abstracto. Prefiere conceptos teóricos generales y principios universales.")
        },
        "complejidad_sintactica": {
            "bajo": (0.0, 0.3, "Estilo directo y claro. Utiliza estructuras sintácticas simples y comunicación directa."),
            "medio": (0.3, 0.7, "Complejidad moderada. Combina claridad con precisión técnica cuando es necesario."),
            "alto": (0.7, 1.0, "Estilo complejo y elaborado. Utiliza estructuras sintácticas sofisticadas y matices lingüísticos.")
        },
        "uso_jurisprudencia": {
            "bajo": (0.0, 0.3, "Enfoque principalmente teórico o doctrinal. Menor referencia a casos específicos."),
            "medio": (0.3, 0.7, "Uso equilibrado. Combina doctrina con referencias jurisprudenciales relevantes."),
            "alto": (0.7, 1.0, "Fuertemente basado en precedentes. Usa extensivamente casos jurisprudenciales y ejemplos prácticos.")
        }
    }
    
    if dimension not in interpretaciones:
        return {"nivel": "desconocido", "descripcion": "Dimensión no reconocida"}
    
    niveles = interpretaciones[dimension]
    for nivel, (min_val, max_val, desc) in niveles.items():
        if min_val <= valor < max_val:
            return {"nivel": nivel, "descripcion": desc, "valor": valor}
    
    # Para valor 1.0 exacto
    return {"nivel": "alto", "descripcion": niveles["alto"][2], "valor": valor}

def generar_perfil_completo(autor: str) -> dict:
    """Genera un análisis completo del perfil cognitivo de un autor"""
    
    if not DB_PATH.exists():
        return {"error": f"Base de datos no encontrada: {DB_PATH}"}
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Obtener perfil completo del autor
    cursor.execute("""
        SELECT autor_detectado, formalismo, creatividad, dogmatismo, empirismo, 
               interdisciplinariedad, nivel_abstraccion, complejidad_sintactica, 
               uso_jurisprudencia, tono, ethos, pathos, logos, doc_titulo,
               total_palabras, archivo_fuente
        FROM perfiles_cognitivos
        WHERE autor_detectado LIKE ? AND autor_detectado IS NOT NULL
        ORDER BY fecha_registro DESC
        LIMIT 1
    """, (f"%{autor}%",))
    
    resultado = cursor.fetchone()
    conn.close()
    
    if not resultado:
        return {"error": f"No se encontró perfil para el autor: {autor}"}
    
    # Desempaquetar datos
    (autor_real, formalismo, creatividad, dogmatismo, empirismo, 
     interdisciplinariedad, nivel_abstraccion, complejidad_sintactica,
     uso_jurisprudencia, tono, ethos, pathos, logos, doc_titulo,
     total_palabras, archivo_fuente) = resultado
    
    # Interpretar cada dimensión
    dimensiones = {
        "formalismo": formalismo or 0,
        "creatividad": creatividad or 0,
        "dogmatismo": dogmatismo or 0,
        "empirismo": empirismo or 0,
        "interdisciplinariedad": interdisciplinariedad or 0,
        "nivel_abstraccion": nivel_abstraccion or 0,
        "complejidad_sintactica": complejidad_sintactica or 0,
        "uso_jurisprudencia": uso_jurisprudencia or 0
    }
    
    interpretaciones = {}
    for dim, valor in dimensiones.items():
        interpretaciones[dim] = interpretar_dimension(dim, valor)
    
    # Análisis retórico
    retorica = {
        "ethos": float(ethos or 0),
        "pathos": float(pathos or 0), 
        "logos": float(logos or 0)
    }
    
    # Determinar estilo dominante
    max_retorica = max(retorica.items(), key=lambda x: x[1])
    estilo_dominante = {
        "ethos": "Basado en credibilidad y autoridad",
        "pathos": "Orientado a la conexión emocional",
        "logos": "Centrado en la lógica y la razón"
    }[max_retorica[0]]
    
    return {
        "autor": autor_real,
        "documento": doc_titulo,
        "archivo": archivo_fuente,
        "total_palabras": total_palabras,
        "dimensiones": dimensiones,
        "interpretaciones": interpretaciones,
        "retorica": retorica,
        "estilo_dominante": estilo_dominante,
        "tono": tono
    }

def generar_recomendaciones(perfil: dict) -> list:
    """Genera recomendaciones basadas en el perfil cognitivo"""
    
    recomendaciones = []
    interpretaciones = perfil.get("interpretaciones", {})
    
    # Recomendaciones basadas en formalismo
    formalismo = interpretaciones.get("formalismo", {})
    if formalismo.get("nivel") == "alto":
        recomendaciones.append("💼 Excelente para trabajos que requieren estructura y precisión técnica")
        recomendaciones.append("📚 Ideal para análisis doctrinarios y construcción de marcos teóricos")
    elif formalismo.get("nivel") == "bajo":
        recomendaciones.append("🔄 Valioso para enfoques adaptativos y soluciones creativas")
        recomendaciones.append("🤝 Apropiado para mediación y resolución flexible de conflictos")
    
    # Recomendaciones basadas en creatividad
    creatividad = interpretaciones.get("creatividad", {})
    if creatividad.get("nivel") == "alto":
        recomendaciones.append("💡 Excelente para innovación jurídica y nuevos enfoques")
        recomendaciones.append("🎨 Valioso para redacción creativa y argumentación original")
    
    # Recomendaciones basadas en empirismo
    empirismo = interpretaciones.get("empirismo", {})
    if empirismo.get("nivel") == "alto":
        recomendaciones.append("📊 Ideal para investigación empírica y análisis de datos")
        recomendaciones.append("⚖️ Excelente para casos que requieren evidencia sólida")
    
    # Recomendaciones basadas en interdisciplinariedad
    interdisciplinariedad = interpretaciones.get("interdisciplinariedad", {})
    if interdisciplinariedad.get("nivel") == "alto":
        recomendaciones.append("🌐 Valioso para casos complejos que requieren múltiples perspectivas")
        recomendaciones.append("🔗 Ideal para colaboración interdisciplinaria")
    
    return recomendaciones

def generar_radar_html_mejorado(autor: str) -> str:
    """Genera HTML completo con radar y explicaciones detalladas"""
    
    perfil = generar_perfil_completo(autor)
    
    if "error" in perfil:
        return f"""
        <div style="background: #fff; padding: 30px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
            <h2 style="color: #e74c3c; text-align: center;">⚠️ Error</h2>
            <p style="text-align: center; color: #7f8c8d;">{perfil['error']}</p>
        </div>
        """
    
    # Generar gráfico radar
    dimensiones = perfil["dimensiones"]
    labels = list(dimensiones.keys())
    values = list(dimensiones.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name=perfil["autor"],
        line_color='#3498db',
        fillcolor='rgba(52, 152, 219, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showticklabels=True,
                ticks="outside",
                tick0=0,
                dtick=0.2
            )
        ),
        showlegend=True,
        title={
            'text': f"Radar Cognitivo: {perfil['autor']}",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        height=500,
        margin=dict(t=80, b=20, l=20, r=20)
    )
    
    radar_html = fig.to_html(include_plotlyjs='cdn', div_id="radar-cognitivo")
    
    # Generar explicaciones detalladas
    interpretaciones = perfil["interpretaciones"]
    explicaciones_html = ""
    
    for dim, interp in interpretaciones.items():
        nivel_color = {
            "bajo": "#95a5a6",
            "medio": "#f39c12", 
            "alto": "#27ae60"
        }.get(interp["nivel"], "#7f8c8d")
        
        explicaciones_html += f"""
        <div style="margin: 15px 0; padding: 15px; border-left: 4px solid {nivel_color}; background: #f8f9fa;">
            <h4 style="margin: 0 0 8px 0; color: #2c3e50; text-transform: capitalize;">
                {dim.replace('_', ' ')}: 
                <span style="color: {nivel_color}; font-weight: bold;">
                    {interp['nivel'].upper()} ({interp['valor']:.2f})
                </span>
            </h4>
            <p style="margin: 0; color: #34495e; line-height: 1.5;">
                {interp['descripcion']}
            </p>
        </div>
        """
    
    # Generar análisis retórico
    retorica = perfil["retorica"]
    retorica_html = f"""
    <div style="background: #ecf0f1; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: #2c3e50; margin-bottom: 15px;">🎭 Análisis Retórico</h3>
        <div style="display: flex; justify-content: space-around;">
            <div style="text-align: center;">
                <h4 style="color: #e74c3c; margin: 5px 0;">Ethos</h4>
                <div style="font-size: 24px; font-weight: bold;">{retorica['ethos']:.2f}</div>
                <small>Credibilidad</small>
            </div>
            <div style="text-align: center;">
                <h4 style="color: #f39c12; margin: 5px 0;">Pathos</h4>
                <div style="font-size: 24px; font-weight: bold;">{retorica['pathos']:.2f}</div>
                <small>Emoción</small>
            </div>
            <div style="text-align: center;">
                <h4 style="color: #3498db; margin: 5px 0;">Logos</h4>
                <div style="font-size: 24px; font-weight: bold;">{retorica['logos']:.2f}</div>
                <small>Lógica</small>
            </div>
        </div>
        <p style="text-align: center; margin-top: 15px; font-style: italic; color: #7f8c8d;">
            <strong>Estilo dominante:</strong> {perfil['estilo_dominante']}
        </p>
    </div>
    """
    
    # Generar recomendaciones
    recomendaciones = generar_recomendaciones(perfil)
    recomendaciones_html = """
    <div style="background: #e8f8f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: #27ae60; margin-bottom: 15px;">💡 Recomendaciones y Aplicaciones</h3>
        <ul style="list-style: none; padding: 0;">
    """
    for rec in recomendaciones:
        recomendaciones_html += f"<li style='margin: 8px 0; padding: 5px 0; border-bottom: 1px dotted #bdc3c7;'>{rec}</li>"
    
    recomendaciones_html += "</ul></div>"
    
    # Información del documento
    total_palabras = perfil['total_palabras'] or 0
    documento_titulo = perfil['documento'] or "Sin título"
    archivo_fuente = perfil['archivo'] or "Sin archivo"
    tono_predominante = perfil['tono'] or "No detectado"
    
    documento_html = f"""
    <div style="background: #fdf2e9; padding: 15px; border-radius: 8px; margin: 20px 0; font-size: 14px;">
        <h4 style="color: #d35400; margin-bottom: 10px;">📄 Información del Análisis</h4>
        <ul style="margin: 0; padding-left: 20px;">
            <li><strong>Documento:</strong> {documento_titulo}</li>
            <li><strong>Archivo:</strong> {archivo_fuente}</li>
            <li><strong>Total palabras:</strong> {total_palabras:,}</li>
            <li><strong>Tono predominante:</strong> {tono_predominante}</li>
        </ul>
    </div>
    """
    
    # HTML completo
    html_completo = f"""
    <div style="background: #fff; padding: 30px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); max-width: 1200px; margin: 0 auto;">
        
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2c3e50; margin-bottom: 10px;">🧠 Análisis Cognitivo Completo</h1>
            <h2 style="color: #3498db; margin: 0;">{perfil['autor']}</h2>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px;">
            <div>
                {radar_html}
            </div>
            <div>
                {retorica_html}
                {documento_html}
            </div>
        </div>
        
        <div style="margin-top: 30px;">
            <h3 style="color: #2c3e50; margin-bottom: 20px;">📋 Análisis Detallado por Dimensión</h3>
            {explicaciones_html}
        </div>
        
        {recomendaciones_html}
        
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #ecf0f1; color: #7f8c8d; font-size: 12px;">
            <p>Generado por Sistema Cognitivo v5.0 • {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
    </div>
    """
    
    return html_completo

# Función de compatibilidad con el sistema existente
def generar_radar_html_completo(autor=None, autores_comparar=None):
    """Función de compatibilidad para integración con webapp existente"""
    
    if autor:
        return generar_radar_html_mejorado(autor)
    else:
        return """
        <div style="background: #fff; padding: 30px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); text-align: center;">
            <h2 style="color: #2c3e50;">🧠 Radar Cognitivo Mejorado</h2>
            <p style="color: #7f8c8d;">Selecciona un autor para ver su análisis cognitivo completo con explicaciones detalladas.</p>
            <p style="color: #3498db; font-weight: bold;">Autores disponibles: Noelia Malvina Cofré, Citlalli, Daniel Esteban Brola, Carlos Pandiella Molina</p>
        </div>
        """

def obtener_estadisticas_radar():
    """Obtiene estadísticas de los autores disponibles"""
    
    if not DB_PATH.exists():
        return None
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT autor_detectado, COUNT(*) as docs, 
               AVG(formalismo) as avg_formalismo,
               AVG(creatividad) as avg_creatividad,
               AVG(empirismo) as avg_empirismo
        FROM perfiles_cognitivos 
        WHERE autor_detectado IS NOT NULL
        GROUP BY autor_detectado
    """)
    
    resultados = cursor.fetchall()
    conn.close()
    
    return resultados

if __name__ == "__main__":
    # Prueba del sistema
    autores = ["Noelia Malvina Cofré", "Citlalli", "Daniel Esteban Brola", "Carlos Pandiella Molina"]
    
    for autor in autores:
        print(f"\n🧠 Analizando: {autor}")
        html = generar_radar_html_mejorado(autor)
        
        # Guardar HTML para prueba
        with open(f"radar_{autor.replace(' ', '_')}.html", 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Análisis guardado en: radar_{autor.replace(' ', '_')}.html")