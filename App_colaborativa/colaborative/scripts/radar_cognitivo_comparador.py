"""
===========================================================
 MÓDULO DE COMPARACIÓN DE PERFILES COGNITIVOS JURÍDICOS
===========================================================

Función:
    Permite comparar gráficamente los perfiles cognitivos de
    varios autores o documentos simultáneamente, mostrando
    sus diferencias en un radar interactivo.

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

def hex_to_rgb(hex_color):
    """Convierte color hexadecimal a tupla RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# ----------------------------------------------------------
# CONFIGURACIÓN DE RUTAS
# ----------------------------------------------------------
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"

# ----------------------------------------------------------
# FUNCIÓN PRINCIPAL
# ----------------------------------------------------------
def comparar_perfiles_cognitivos(autores: list, return_html=False):
    """
    Compara varios perfiles cognitivos simultáneamente.
    Cada autor se representa como un polígono distinto.
    """
    
    if not DB_PATH.exists():
        print(f"⚠️ Base de datos no encontrada: {DB_PATH}")
        return None
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    fig = go.Figure()
    categorias = ["Formalismo", "Creatividad", "Dogmatismo", "Empirismo", "Interdisciplinariedad"]

    colores = [
        "royalblue", "firebrick", "seagreen", "darkorange",
        "purple", "teal", "goldenrod", "slategray", "crimson", "forestgreen"
    ]
    
    perfiles_encontrados = []
    
    for i, autor in enumerate(autores):
        cursor.execute("""
            SELECT formalismo, creatividad, dogmatismo, empirismo, interdisciplinariedad, 
                   tipo_pensamiento, fecha_analisis
            FROM perfiles_cognitivos
            WHERE autor LIKE ?
            ORDER BY fecha_analisis DESC
            LIMIT 1
        """, (f"%{autor}%",))
        
        row = cursor.fetchone()
        if row:
            valores = list(row[:5]) + [row[0]]  # cerrar el círculo
            tipo = row[5] or "No clasificado"
            fecha = row[6][:10] if row[6] else "N/A"
            
            # Agregar transparencia al color de relleno
            color_fill = colores[i % len(colores)]
            
            # Colores con transparencia predefinidos
            colores_rgba = {
                "royalblue": "rgba(65, 105, 225, 0.15)",
                "firebrick": "rgba(178, 34, 34, 0.15)",
                "seagreen": "rgba(46, 139, 87, 0.15)",
                "darkorange": "rgba(255, 140, 0, 0.15)",
                "purple": "rgba(128, 0, 128, 0.15)",
                "teal": "rgba(0, 128, 128, 0.15)",
                "goldenrod": "rgba(218, 165, 32, 0.15)",
                "slategray": "rgba(112, 128, 144, 0.15)",
                "crimson": "rgba(220, 20, 60, 0.15)",
                "forestgreen": "rgba(34, 139, 34, 0.15)"
            }
            
            fig.add_trace(go.Scatterpolar(
                r=valores,
                theta=categorias + ["Formalismo"],
                fill='toself',
                name=f"{autor[:20]} ({tipo})",
                line=dict(color=color_fill, width=3),
                fillcolor=colores_rgba.get(color_fill, "rgba(65, 105, 225, 0.15)"),
                hovertemplate=f"<b>{autor}</b><br>" +
                             f"Tipo: {tipo}<br>" +
                             f"Fecha: {fecha}<br>" +
                             f"%{{theta}}: %{{r:.3f}}<extra></extra>"
            ))
            
            perfiles_encontrados.append({
                'autor': autor,
                'tipo': tipo,
                'fecha': fecha,
                'valores': row[:5]
            })
        else:
            print(f"⚠️ No se encontró perfil cognitivo para '{autor}'.")

    conn.close()

    if not fig.data:
        print("⚠️ No se generó ningún radar. Verifica los nombres de autores.")
        return None

    fig.update_layout(
        title=dict(
            text=f"⚖️ Comparación de Perfiles Cognitivos Jurídicos<br><sup>Comparando {len(perfiles_encontrados)} perfiles</sup>",
            x=0.5, y=0.95, 
            font=dict(size=18, color='#2c3e50')
        ),
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
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=12)
        ),
        margin=dict(l=50, r=200, t=100, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white',
        width=900,
        height=600
    )

    if return_html:
        return pio.to_html(fig, include_plotlyjs='cdn', div_id="radar-comparacion")
    else:
        fig.show()
        return fig, perfiles_encontrados


def obtener_estadisticas_comparacion(perfiles):
    """Genera estadísticas de la comparación realizada."""
    
    if not perfiles:
        return {}
    
    # Calcular promedios por rasgo
    rasgos = ['formalismo', 'creatividad', 'dogmatismo', 'empirismo', 'interdisciplinariedad']
    estadisticas = {}
    
    for i, rasgo in enumerate(rasgos):
        valores = [p['valores'][i] for p in perfiles]
        estadisticas[rasgo] = {
            'promedio': sum(valores) / len(valores),
            'maximo': max(valores),
            'minimo': min(valores),
            'autor_max': max(perfiles, key=lambda p: p['valores'][i])['autor'],
            'autor_min': min(perfiles, key=lambda p: p['valores'][i])['autor']
        }
    
    # Tipos de pensamiento
    tipos = [p['tipo'] for p in perfiles]
    tipos_count = {}
    for tipo in tipos:
        tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
    
    estadisticas['tipos_pensamiento'] = tipos_count
    estadisticas['total_perfiles'] = len(perfiles)
    
    return estadisticas


def generar_comparacion_html_completo(autores_lista):
    """Genera HTML completo con comparación de perfiles."""
    
    if not autores_lista or len(autores_lista) < 2:
        return """
        <div style="text-align: center; padding: 40px; color: #7f8c8d;">
            <h3>⚠️ Comparación Requiere Múltiples Autores</h3>
            <p>Ingresa al menos 2 autores para generar una comparación.</p>
            <p><strong>Formato:</strong> Separa los nombres con comas</p>
        </div>
        """
    
    resultado = comparar_perfiles_cognitivos(autores_lista, return_html=True)
    
    if not resultado:
        return """
        <div style="text-align: center; padding: 40px; color: #7f8c8d;">
            <h3>⚠️ No se Pudieron Comparar los Perfiles</h3>
            <p>Verifica que los autores existan en la base de datos cognitiva.</p>
            <p><strong>Autores solicitados:</strong> {}</p>
        </div>
        """.format(", ".join(autores_lista))
    
    # Obtener estadísticas si hay perfiles
    perfiles_data = []
    if isinstance(resultado, tuple):
        radar_html, perfiles_data = resultado
        stats = obtener_estadisticas_comparacion(perfiles_data)
    else:
        radar_html = resultado
        stats = {}
    
    html_content = f"""
    <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; color: #2c3e50; margin-bottom: 20px;">
            ⚖️ Comparación de Perfiles Cognitivos
        </h2>
        
        {radar_html if isinstance(resultado, str) else (radar_html if isinstance(resultado, tuple) else resultado)}
        
        <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <h3 style="color: #495057;">📊 Análisis Comparativo</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0;">
    """
    
    # Agregar estadísticas si están disponibles
    if stats:
        for rasgo, data in stats.items():
            if rasgo != 'tipos_pensamiento' and rasgo != 'total_perfiles':
                html_content += f"""
                <div style="background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #007bff;">
                    <h4 style="margin: 0 0 10px 0; color: #2c3e50; text-transform: capitalize;">{rasgo.replace('_', ' ')}</h4>
                    <p style="margin: 5px 0; font-size: 0.9em;"><strong>Promedio:</strong> {data['promedio']:.3f}</p>
                    <p style="margin: 5px 0; font-size: 0.9em;"><strong>Máximo:</strong> {data['autor_max'][:15]} ({data['maximo']:.3f})</p>
                    <p style="margin: 5px 0; font-size: 0.9em;"><strong>Mínimo:</strong> {data['autor_min'][:15]} ({data['minimo']:.3f})</p>
                </div>
                """
    
    html_content += """
            </div>
        </div>
        
        <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 6px;">
            <h4 style="color: #1976d2;">💡 Interpretación del Radar Comparativo:</h4>
            <ul style="margin: 10px 0; padding-left: 20px; color: #424242;">
                <li><strong>Formalismo:</strong> Apego al texto legal, citas formales</li>
                <li><strong>Creatividad:</strong> Capacidad de reinterpretar normas</li>
                <li><strong>Dogmatismo:</strong> Adhesión a doctrina tradicional</li>
                <li><strong>Empirismo:</strong> Uso de casos concretos y experiencia</li>
                <li><strong>Interdisciplinariedad:</strong> Integración de conceptos extrajurídicos</li>
            </ul>
            <p style="font-style: italic; color: #666; margin-top: 10px;">
                💡 Cuanto más se acerca el polígono a 1.0, mayor es el peso de esa característica.
            </p>
        </div>
    </div>
    """
    
    return html_content


# ----------------------------------------------------------
# FUNCIÓN DE AUTORES DISPONIBLES
# ----------------------------------------------------------
def listar_autores_disponibles(limit=20):
    """Lista autores disponibles para comparación."""
    
    if not DB_PATH.exists():
        return []
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT autor, COUNT(*) as docs, tipo_pensamiento,
               AVG(formalismo) as avg_formalismo,
               AVG(creatividad) as avg_creatividad
        FROM perfiles_cognitivos 
        WHERE autor IS NOT NULL AND autor != '' 
        GROUP BY autor 
        ORDER BY docs DESC, autor
        LIMIT ?
    """, (limit,))
    
    resultados = cursor.fetchall()
    conn.close()
    
    return [
        {
            'autor': row[0],
            'documentos': row[1],
            'tipo': row[2],
            'formalismo': round(row[3], 3),
            'creatividad': round(row[4], 3)
        }
        for row in resultados
    ]


# ----------------------------------------------------------
# USO DIRECTO
# ----------------------------------------------------------
if __name__ == "__main__":
    print("📊 Comparando perfiles cognitivos de ejemplo...\n")
    
    # Obtener autores disponibles
    autores_disponibles = listar_autores_disponibles(5)
    
    if len(autores_disponibles) >= 2:
        autores_ejemplo = [a['autor'] for a in autores_disponibles[:3]]
        print(f"Comparando: {', '.join(autores_ejemplo)}")
        resultado = comparar_perfiles_cognitivos(autores_ejemplo)
        if resultado:
            print("✅ Comparación generada exitosamente")
    else:
        print("⚠️ Se necesitan al menos 2 perfiles para hacer comparación.")
        print("Ejecuta primero: python ingesta_cognitiva.py")