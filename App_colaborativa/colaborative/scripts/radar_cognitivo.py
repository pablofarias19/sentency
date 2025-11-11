"""
===========================================================
 MÓDULO DE VISUALIZACIÓN – RADAR COGNITIVO JURÍDICO
===========================================================

Función:
    Representar gráficamente los rasgos cognitivos de un perfil
    jurídico (formalismo, creatividad, dogmatismo, empirismo,
    interdisciplinariedad) mediante un gráfico tipo radar.

Dependencias:
    pip install plotly pandas sqlite3
===========================================================
"""

import os
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

# ----------------------------------------------------------
# CONFIGURACIÓN DE RUTAS
# ----------------------------------------------------------
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"

# ----------------------------------------------------------
# FUNCIÓN PRINCIPAL
# ----------------------------------------------------------
def mostrar_radar_cognitivo(autor: str, return_html=False):
    """Genera y muestra un radar cognitivo para un autor determinado."""
    
    # Verificar que existe la base de datos
    if not DB_PATH.exists():
        print(f"⚠️ Base de datos no encontrada: {DB_PATH}")
        return None
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Obtener el último perfil del autor
    cursor.execute("""
        SELECT formalismo, creatividad, dogmatismo, empirismo, interdisciplinariedad,
               tipo_pensamiento, fecha_analisis
        FROM perfiles_cognitivos
        WHERE autor LIKE ?
        ORDER BY fecha_analisis DESC
        LIMIT 1
    """, (f"%{autor}%",))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print(f"⚠️ No se encontró perfil cognitivo para '{autor}'.")
        return None

    formalismo, creatividad, dogmatismo, empirismo, interdisciplinariedad, tipo, fecha = row

    # Crear DataFrame
    df = pd.DataFrame(dict(
        r=[formalismo, creatividad, dogmatismo, empirismo, interdisciplinariedad, formalismo],
        theta=["Formalismo", "Creatividad", "Dogmatismo", "Empirismo", "Interdisciplinariedad", "Formalismo"]
    ))

    # Crear gráfico radar
    fig = go.Figure(
        data=go.Scatterpolar(
            r=df["r"],
            theta=df["theta"],
            fill='toself',
            line_color='royalblue',
            fillcolor='rgba(65, 105, 225, 0.2)',
            name=autor,
            line_width=3
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 1], 
                tickfont_size=10,
                gridcolor='lightgray',
                gridwidth=1
            ),
            angularaxis=dict(
                tickfont_size=11,
                rotation=90,
                direction='clockwise'
            )
        ),
        title=dict(
            text=f"🧠 Perfil Cognitivo Jurídico: {autor}<br><sup>{tipo} | {fecha[:10] if fecha else 'N/A'}</sup>",
            x=0.5, y=0.95,
            font=dict(size=18, color='#2c3e50')
        ),
        showlegend=False,
        margin=dict(l=50, r=50, t=100, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    if return_html:
        return pio.to_html(fig, include_plotlyjs='cdn', div_id="radar-cognitivo")
    else:
        fig.show()
        return fig


def comparar_radares(autores: list, return_html=False):
    """Compara múltiples perfiles cognitivos en un solo radar."""
    
    if not DB_PATH.exists():
        print(f"⚠️ Base de datos no encontrada: {DB_PATH}")
        return None
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    fig = go.Figure()
    
    colores = ['royalblue', 'crimson', 'forestgreen', 'orange', 'purple', 'brown']
    
    for i, autor in enumerate(autores):
        cursor.execute("""
            SELECT formalismo, creatividad, dogmatismo, empirismo, interdisciplinariedad,
                   tipo_pensamiento
            FROM perfiles_cognitivos 
            WHERE autor LIKE ? 
            ORDER BY fecha_analisis DESC 
            LIMIT 1
        """, (f"%{autor}%",))
        
        row = cursor.fetchone()
        if row:
            valores = list(row[:5]) + [row[0]]  # cerrar el círculo
            color = colores[i % len(colores)]
            
            fig.add_trace(go.Scatterpolar(
                r=valores, 
                theta=["Formalismo", "Creatividad", "Dogmatismo", "Empirismo", "Interdisciplinariedad", "Formalismo"], 
                fill='toself', 
                name=f"{autor} ({row[5]})",
                line_color=color,
                fillcolor=f"rgba{tuple(list(pio.colors.hex_to_rgb(color)) + [0.1])}",
                line_width=2
            ))
    
    conn.close()

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 1],
                tickfont_size=10,
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                tickfont_size=11,
                rotation=90,
                direction='clockwise'
            )
        ),
        title=dict(
            text="🧠 Comparación de Perfiles Cognitivos Jurídicos",
            x=0.5, y=0.95,
            font=dict(size=18, color='#2c3e50')
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=50, r=50, t=100, b=100),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    if return_html:
        return pio.to_html(fig, include_plotlyjs='cdn', div_id="radar-comparacion")
    else:
        fig.show()
        return fig


def obtener_estadisticas_radar():
    """Obtiene estadísticas para mostrar autores disponibles."""
    
    if not DB_PATH.exists():
        return []
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT autor, COUNT(*) as documentos, 
               AVG(formalismo) as avg_formalismo,
               AVG(creatividad) as avg_creatividad,
               AVG(empirismo) as avg_empirismo,
               tipo_pensamiento
        FROM perfiles_cognitivos 
        WHERE autor IS NOT NULL AND autor != '' 
        GROUP BY autor 
        ORDER BY documentos DESC, autor
        LIMIT 20
    """)
    
    resultados = cursor.fetchall()
    conn.close()
    
    return [
        {
            'autor': row[0],
            'documentos': row[1],
            'formalismo': round(row[2], 3),
            'creatividad': round(row[3], 3),
            'empirismo': round(row[4], 3),
            'tipo': row[5]
        }
        for row in resultados
    ]


def generar_radar_html_completo(autor=None, autores_comparar=None):
    """Genera HTML completo con radar cognitivo para embebido en webapp."""
    
    html_content = """
    <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; color: #2c3e50; margin-bottom: 20px;">
            🧠 Visualización Radar Cognitivo
        </h2>
    """
    
    if autor:
        radar_html = mostrar_radar_cognitivo(autor, return_html=True)
        if radar_html:
            html_content += radar_html
        else:
            html_content += f"""
            <div style="text-align: center; padding: 40px; color: #7f8c8d;">
                <h3>⚠️ No se encontró perfil para: {autor}</h3>
                <p>Asegúrate de que el autor tenga documentos procesados en el sistema cognitivo.</p>
            </div>
            """
    
    elif autores_comparar and len(autores_comparar) > 1:
        radar_html = comparar_radares(autores_comparar, return_html=True)
        if radar_html:
            html_content += radar_html
        else:
            html_content += """
            <div style="text-align: center; padding: 40px; color: #7f8c8d;">
                <h3>⚠️ No se pudieron comparar los perfiles</h3>
                <p>Verifica que los autores existan en la base de datos cognitiva.</p>
            </div>
            """
    
    else:
        # Mostrar estadísticas disponibles
        stats = obtener_estadisticas_radar()
        if stats:
            html_content += """
            <div style="margin: 20px 0;">
                <h3 style="color: #34495e;">📊 Autores Disponibles para Análisis:</h3>
                <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                    <tr style="background: #ecf0f1;">
                        <th style="padding: 10px; border: 1px solid #bdc3c7;">Autor</th>
                        <th style="padding: 10px; border: 1px solid #bdc3c7;">Docs</th>
                        <th style="padding: 10px; border: 1px solid #bdc3c7;">Formalismo</th>
                        <th style="padding: 10px; border: 1px solid #bdc3c7;">Creatividad</th>
                        <th style="padding: 10px; border: 1px solid #bdc3c7;">Empirismo</th>
                        <th style="padding: 10px; border: 1px solid #bdc3c7;">Tipo</th>
                    </tr>
            """
            
            for stat in stats[:10]:  # Top 10
                html_content += f"""
                    <tr>
                        <td style="padding: 8px; border: 1px solid #bdc3c7;"><strong>{stat['autor'][:30]}</strong></td>
                        <td style="padding: 8px; border: 1px solid #bdc3c7; text-align: center;">{stat['documentos']}</td>
                        <td style="padding: 8px; border: 1px solid #bdc3c7; text-align: center;">{stat['formalismo']}</td>
                        <td style="padding: 8px; border: 1px solid #bdc3c7; text-align: center;">{stat['creatividad']}</td>
                        <td style="padding: 8px; border: 1px solid #bdc3c7; text-align: center;">{stat['empirismo']}</td>
                        <td style="padding: 8px; border: 1px solid #bdc3c7;">{stat['tipo']}</td>
                    </tr>
                """
                
            html_content += """
                </table>
                <p style="color: #7f8c8d; font-style: italic;">
                    💡 Usa el formulario arriba para generar un radar específico o comparar autores.
                </p>
            </div>
            """
        else:
            html_content += """
            <div style="text-align: center; padding: 40px; color: #7f8c8d;">
                <h3>📊 Sistema Cognitivo Vacío</h3>
                <p>No hay perfiles cognitivos en la base de datos.</p>
                <p>Ejecuta <code>ingesta_cognitiva.py</code> para procesar documentos.</p>
            </div>
            """
    
    html_content += """
        </div>
    """
    
    return html_content


# ----------------------------------------------------------
# USO DIRECTO
# ----------------------------------------------------------
if __name__ == "__main__":
    print("📊 Generando radar cognitivo de ejemplo...\n")
    
    # Obtener primer autor disponible
    stats = obtener_estadisticas_radar()
    if stats:
        primer_autor = stats[0]['autor']
        print(f"Generando radar para: {primer_autor}")
        mostrar_radar_cognitivo(primer_autor)
    else:
        print("⚠️ No hay perfiles cognitivos disponibles.")
        print("Ejecuta primero: python ingesta_cognitiva.py")