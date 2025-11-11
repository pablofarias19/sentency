"""
===========================================================
 MATRIZ DE SIMILITUD COGNITIVA – ANALYSER METODO
===========================================================

Función:
    Calcula la distancia o similitud entre todos los perfiles
    cognitivos registrados y genera un heatmap interactivo
    que muestra convergencias o divergencias entre autores.

Dependencias:
    pip install numpy pandas plotly sqlite3
===========================================================
"""

import os
import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
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
def generar_matriz_cognitiva(return_html=False, max_autores=15):
    """
    Calcula las distancias entre los vectores cognitivos almacenados
    y genera una matriz de similitud (1 - distancia normalizada).
    """
    
    if not DB_PATH.exists():
        print(f"⚠️ Base de datos no encontrada: {DB_PATH}")
        return None
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Obtener perfiles con mejores métricas para matriz más legible
    cursor.execute("""
        SELECT autor, formalismo, creatividad, dogmatismo, empirismo, interdisciplinariedad,
               nivel_abstraccion, complejidad_sintactica, uso_jurisprudencia, tipo_pensamiento
        FROM perfiles_cognitivos
        WHERE autor IS NOT NULL AND autor != ''
        GROUP BY autor
        HAVING COUNT(*) >= 1
        ORDER BY COUNT(*) DESC
        LIMIT ?
    """, (max_autores,))
    
    registros = cursor.fetchall()
    conn.close()

    if len(registros) < 2:
        error_msg = "⚠️ Se necesitan al menos dos perfiles cognitivos para generar la matriz."
        if return_html:
            return f"""
            <div style="text-align: center; padding: 40px; color: #7f8c8d;">
                <h3>{error_msg}</h3>
                <p>Ejecuta <code>ingesta_cognitiva.py</code> para procesar más documentos.</p>
            </div>
            """
        print(error_msg)
        return None

    # Construir matriz de vectores cognitivos
    autores = []
    vectores = []
    tipos_pensamiento = []
    
    for registro in registros:
        autor = registro[0]
        # Usar 8 rasgos cognitivos como vector
        vector_cognitivo = np.array(registro[1:9], dtype=float)
        tipo = registro[9] or "No clasificado"
        
        autores.append(autor[:20])  # Limitar longitud del nombre
        vectores.append(vector_cognitivo)
        tipos_pensamiento.append(tipo)

    vectores = np.array(vectores)
    n = len(vectores)
    matriz_sim = np.zeros((n, n))

    # Calcular similitud cognitiva (combinando coseno y euclidiana)
    for i in range(n):
        for j in range(n):
            if i == j:
                matriz_sim[i, j] = 1.0
            else:
                v1, v2 = vectores[i], vectores[j]
                
                # Similitud coseno
                cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                
                # Distancia euclidiana normalizada
                dist_eucl = np.linalg.norm(v1 - v2)
                max_dist = np.sqrt(8)  # máxima distancia posible entre vectores 8D [0,1]
                sim_eucl = 1 - (dist_eucl / max_dist)
                
                # Combinación híbrida (60% coseno, 40% euclidiana)
                similitud_final = 0.6 * cos_sim + 0.4 * sim_eucl
                matriz_sim[i, j] = round(max(0, similitud_final), 3)

    # Crear DataFrame
    df = pd.DataFrame(matriz_sim, index=autores, columns=autores)

    # Crear heatmap con Plotly
    fig = px.imshow(
        df.values,
        x=autores,
        y=autores,
        color_continuous_scale="RdYlBu_r",  # Rojo-Amarillo-Azul invertido
        text_auto=True,
        labels=dict(x="Autor", y="Autor", color="Similitud Cognitiva"),
        title="🧠 Matriz de Similitud Cognitiva Jurídica",
        aspect="auto"
    )

    fig.update_layout(
        width=800, height=800,
        title=dict(
            text="🧠 Matriz de Similitud Cognitiva Jurídica<br><sup>Análisis de convergencias doctrinarias</sup>",
            x=0.5, y=0.95,
            font=dict(size=18, color='#2c3e50')
        ),
        margin=dict(l=100, r=100, t=120, b=100),
        xaxis=dict(
            side="top", 
            tickangle=45,
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=10)
        ),
        coloraxis_colorbar=dict(
            title=dict(text="Grado de Similitud", font=dict(size=12)),
            tickvals=[0, 0.25, 0.5, 0.75, 1.0],
            ticktext=["0.0<br>Divergente", "0.25<br>Poco Similar", "0.5<br>Moderado", "0.75<br>Similar", "1.0<br>Idéntico"]
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Agregar anotaciones para valores
    fig.update_traces(
        texttemplate="%{z:.2f}",
        textfont={"size": 9},
        hovertemplate="<b>%{y}</b> vs <b>%{x}</b><br>Similitud: %{z:.3f}<extra></extra>"
    )

    if return_html:
        html_chart = pio.to_html(fig, include_plotlyjs='cdn', div_id="matriz-cognitiva")
        
        # Generar análisis adicional
        analisis = generar_analisis_matriz(df, tipos_pensamiento, autores)
        
        html_completo = f"""
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="text-align: center; color: #2c3e50; margin-bottom: 20px;">
                🧭 Mapa de Similitud Cognitiva Jurídica
            </h2>
            
            {html_chart}
            
            {analisis}
        </div>
        """
        
        return html_completo
    else:
        fig.show()
        return df, fig


def generar_analisis_matriz(df, tipos, autores):
    """Genera análisis interpretativo de la matriz."""
    
    # Encontrar pares más similares y más diferentes
    np_matrix = df.values
    n = len(df)
    
    # Excluir diagonal (similitud consigo mismo)
    similarities = []
    for i in range(n):
        for j in range(i+1, n):
            similarities.append({
                'autor1': autores[i],
                'autor2': autores[j],
                'similitud': np_matrix[i, j],
                'tipo1': tipos[i] if i < len(tipos) else 'N/A',
                'tipo2': tipos[j] if j < len(tipos) else 'N/A'
            })
    
    # Ordenar por similitud
    similarities.sort(key=lambda x: x['similitud'], reverse=True)
    
    mas_similares = similarities[:3]
    mas_diferentes = similarities[-3:]
    
    # Promedio de similitud
    promedio_sim = np.mean([s['similitud'] for s in similarities])
    
    html_analisis = f"""
    <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
        <h3 style="color: #495057;">📊 Análisis de la Matriz Cognitiva</h3>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
            
            <div style="background: #d4edda; padding: 15px; border-radius: 6px; border-left: 4px solid #28a745;">
                <h4 style="color: #155724; margin-top: 0;">🤝 Perfiles Más Similares</h4>
    """
    
    for sim in mas_similares:
        html_analisis += f"""
                <p style="margin: 8px 0; font-size: 0.9em;">
                    <strong>{sim['autor1']}</strong> vs <strong>{sim['autor2']}</strong><br>
                    <span style="color: #28a745; font-weight: bold;">Similitud: {sim['similitud']:.3f}</span>
                    ({sim['tipo1']} vs {sim['tipo2']})
                </p>
        """
    
    html_analisis += f"""
            </div>
            
            <div style="background: #f8d7da; padding: 15px; border-radius: 6px; border-left: 4px solid #dc3545;">
                <h4 style="color: #721c24; margin-top: 0;">🔄 Perfiles Más Divergentes</h4>
    """
    
    for sim in mas_diferentes:
        html_analisis += f"""
                <p style="margin: 8px 0; font-size: 0.9em;">
                    <strong>{sim['autor1']}</strong> vs <strong>{sim['autor2']}</strong><br>
                    <span style="color: #dc3545; font-weight: bold;">Similitud: {sim['similitud']:.3f}</span>
                    ({sim['tipo1']} vs {sim['tipo2']})
                </p>
        """
    
    html_analisis += f"""
            </div>
        </div>
        
        <div style="background: #cce5ff; padding: 15px; border-radius: 6px; margin-top: 15px;">
            <h4 style="color: #004085;">🧮 Métricas Generales</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <strong>Similitud Promedio:</strong> {promedio_sim:.3f}<br>
                    <small>Cohesión general del corpus jurídico</small>
                </div>
                <div>
                    <strong>Total Comparaciones:</strong> {len(similarities)}<br>
                    <small>Pares únicos analizados</small>
                </div>
                <div>
                    <strong>Autores Analizados:</strong> {len(autores)}<br>
                    <small>Perfiles cognitivos incluidos</small>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 15px; padding: 15px; background: #e3f2fd; border-radius: 6px;">
            <h4 style="color: #1976d2;">💡 Interpretación de la Matriz:</h4>
            <ul style="margin: 10px 0; padding-left: 20px; color: #424242;">
                <li><strong>Azul intenso (0.8-1.0):</strong> Escuelas de pensamiento convergentes</li>
                <li><strong>Verde-Amarillo (0.5-0.8):</strong> Similitudes moderadas, posibles influencias</li>
                <li><strong>Naranja-Rojo (0.0-0.5):</strong> Enfoques divergentes, corrientes distintas</li>
            </ul>
            <p style="font-style: italic; color: #666; margin-top: 10px;">
                🧠 Esta matriz revela patrones de convergencia doctrinal y permite identificar clusters de pensamiento jurídico.
            </p>
        </div>
    </div>
    """
    
    return html_analisis


def exportar_matriz_csv(df, filename="matriz_cognitiva.csv"):
    """Exporta la matriz de similitud a CSV."""
    output_path = BASE_PATH / "data" / "resultados" / filename
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=True)
    print(f"✅ Matriz exportada a: {output_path}")
    return output_path


# ----------------------------------------------------------
# USO DIRECTO
# ----------------------------------------------------------
if __name__ == "__main__":
    print("📊 Generando matriz de similitud cognitiva...\n")
    resultado = generar_matriz_cognitiva()
    
    if resultado:
        if isinstance(resultado, tuple):
            df, fig = resultado
            print(f"✅ Matriz generada con {len(df)} autores")
            
            # Exportar a CSV
            exportar_matriz_csv(df)
        else:
            print("✅ Matriz generada exitosamente")
    else:
        print("❌ No se pudo generar la matriz")
        print("Ejecuta primero: python ingesta_cognitiva.py")