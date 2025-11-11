#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 BIBLIOTECA COGNITIVA DE AUTORES - PÁGINA PRINCIPAL MEJORADA
=============================================================

Sistema que expone claramente:
- Autores disponibles
- Sus obras procesadas  
- Características del pensamiento
- Relaciones entre autores
- Análisis detallados
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime
import json

# Configuración de rutas - usar ruta relativa al archivo actual
BASE_PATH = Path(__file__).resolve().parent
DB_PATH = BASE_PATH / "colaborative" / "bases_rag" / "cognitiva" / "metadatos.db"

class BibliotecaCognitiva:
    def __init__(self):
        self.db_path = DB_PATH
        
    def obtener_autores_completos(self):
        """Obtiene información completa de todos los autores"""
        
        print(f"🔍 Buscando DB en: {self.db_path}")
        if not self.db_path.exists():
            print(f"❌ DB no encontrada en: {self.db_path}")
            return []
        print(f"✅ DB encontrada en: {self.db_path}")
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Consulta completa con todas las métricas
        cursor.execute("""
            SELECT 
                autor,
                COUNT(*) as total_obras,
                GROUP_CONCAT(DISTINCT fuente) as obras,
                GROUP_CONCAT(DISTINCT archivo) as archivos,
                AVG(formalismo) as avg_formalismo,
                AVG(creatividad) as avg_creatividad,
                AVG(dogmatismo) as avg_dogmatismo,
                AVG(empirismo) as avg_empirismo,
                AVG(interdisciplinariedad) as avg_interdisciplinariedad,
                AVG(nivel_abstraccion) as avg_nivel_abstraccion,
                AVG(complejidad_sintactica) as avg_complejidad_sintactica,
                AVG(uso_jurisprudencia) as avg_uso_jurisprudencia,
                COALESCE(SUM(total_palabras), 1000) as total_palabras,
                GROUP_CONCAT(DISTINCT tipo_pensamiento) as tipos_pensamiento,
                MAX(fecha_analisis) as ultima_actualizacion
            FROM perfiles_cognitivos 
            WHERE autor IS NOT NULL AND autor != 'Autor no identificado' AND autor != 'Desconocido'
            GROUP BY autor
            ORDER BY autor
        """)
        
        resultados = cursor.fetchall()
        conn.close()
        
        autores = []
        for row in resultados:
            autor = {
                'nombre': row[0],
                'total_obras': row[1],
                'obras': row[2] if row[2] else 'Sin título específico',
                'archivos': row[3],
                'formalismo': row[4] or 0,
                'creatividad': row[5] or 0,
                'dogmatismo': row[6] or 0,
                'empirismo': row[7] or 0,
                'interdisciplinariedad': row[8] or 0,
                'nivel_abstraccion': row[9] or 0,
                'complejidad_sintactica': row[10] or 0,
                'uso_jurisprudencia': row[11] or 0,
                'total_palabras': row[12] or 0,
                'tipo_pensamiento': row[13] or 'No clasificado',
                'ultima_actualizacion': row[14]
            }
            autores.append(autor)
        
        return autores
    
    def calcular_relaciones_autores(self, autores):
        """Calcula relaciones y similitudes entre autores"""
        relaciones = {}
        
        for i, autor1 in enumerate(autores):
            relaciones[autor1['nombre']] = []
            
            for j, autor2 in enumerate(autores):
                if i != j:
                    # Calcular similitud cognitiva
                    dimensiones = {
                        'formalismo': autor1['formalismo'],
                        'creatividad': autor1['creatividad'],
                        'empirismo': autor1['empirismo'],
                        'nivel_abstraccion': autor1['nivel_abstraccion']
                    }
                    
                    similitud = self._calcular_similitud_cognitiva(autor1, autor2)
                    if similitud > 0.7:  # Umbral de similitud
                        afines = self._obtener_dimensiones_afines(autor1, autor2)
                        relaciones[autor1['nombre']].append({
                            'nombre': autor2['nombre'],
                            'similitud': similitud,
                            'dimensiones_afines': afines
                        })
        
        return relaciones
    
    def _calcular_similitud_cognitiva(self, autor1, autor2):
        """Calcula similitud entre dos perfiles cognitivos"""
        dimensiones = ['formalismo', 'creatividad', 'empirismo', 'nivel_abstraccion']
        
        diferencias = []
        for dim in dimensiones:
            diff = abs(autor1[dim] - autor2[dim])
            diferencias.append(1 - diff)  # Convertir diferencia en similitud
        
        return sum(diferencias) / len(diferencias)
    
    def _obtener_dimensiones_afines(self, autor1, autor2):
        """Encuentra las dimensiones más afines entre dos autores"""
        dimensiones = {
            'formalismo': 'Formalismo jurídico',
            'creatividad': 'Creatividad argumentativa',
            'empirismo': 'Enfoque empírico',
            'nivel_abstraccion': 'Nivel de abstracción'
        }
        
        afines = []
        for dim_key, dim_nombre in dimensiones.items():
            diferencia = abs(autor1[dim_key] - autor2[dim_key])
            if diferencia < 0.2:  # Muy similares
                promedio = (autor1[dim_key] + autor2[dim_key]) / 2
                afines.append(f"{dim_nombre} ({promedio:.2f})")
        
        return afines[:3]  # Top 3 más afines
    
    def generar_pagina_principal_html(self):
        """Genera HTML de la página principal mejorada"""
        
        autores = self.obtener_autores_completos()
        relaciones = self.calcular_relaciones_autores(autores)
        
        # Estadísticas generales
        total_autores = len(autores)
        total_obras = sum(autor["total_obras"] for autor in autores)
        total_palabras = sum(autor["total_palabras"] for autor in autores)
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 Biblioteca Cognitiva de Autores</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0; padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1400px; margin: 0 auto;
            background: white; border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white; padding: 30px; text-align: center;
        }}
        .header h1 {{ margin: 0; font-size: 2.5em; }}
        .stats {{
            display: flex; justify-content: space-around;
            background: #ecf0f1; padding: 20px; margin: 0;
        }}
        .stat {{
            text-align: center; padding: 10px;
        }}
        .stat .number {{
            font-size: 2em; font-weight: bold; color: #2c3e50;
        }}
        .stat .label {{
            color: #7f8c8d; font-size: 0.9em;
        }}
        .content {{
            display: grid; grid-template-columns: 2fr 1fr;
            gap: 30px; padding: 30px;
        }}
        .autores-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        .autor-card {{
            background: #f8f9fa; border-radius: 12px; padding: 20px;
            border-left: 5px solid #3498db;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .autor-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        .autor-nombre {{
            font-size: 1.3em; font-weight: bold; color: #2c3e50;
            margin-bottom: 10px;
        }}
        .autor-obras {{
            color: #7f8c8d; font-size: 0.9em; margin-bottom: 15px;
            display: -webkit-box; -webkit-line-clamp: 2;
            -webkit-box-orient: vertical; overflow: hidden;
        }}
        .metricas {{
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 8px; margin-bottom: 15px;
        }}
        .metrica {{
            background: white; padding: 8px; border-radius: 6px;
            text-align: center; font-size: 0.8em;
        }}
        .metrica .valor {{
            font-weight: bold; color: #3498db;
        }}
        .tipo-pensamiento {{
            background: #3498db; color: white;
            padding: 5px 10px; border-radius: 15px;
            font-size: 0.8em; display: inline-block;
        }}
        .relaciones {{
            background: #f1f2f6; border-radius: 12px; padding: 20px;
        }}
        .relaciones h3 {{
            color: #2c3e50; margin-top: 0;
        }}
        .relacion {{
            background: white; padding: 15px; border-radius: 8px;
            margin-bottom: 10px; border-left: 3px solid #e74c3c;
        }}
        .navegacion {{
            background: #34495e; padding: 15px; text-align: center;
        }}
        .navegacion a {{
            color: white; text-decoration: none; margin: 0 15px;
            padding: 8px 15px; border-radius: 5px;
            background: rgba(255,255,255,0.2);
            transition: background 0.3s;
        }}
        .navegacion a:hover {{
            background: rgba(255,255,255,0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 BIBLIOTECA COGNITIVA DE AUTORES</h1>
            <p>Sistema de análisis cognitivo y relacional de pensamiento jurídico</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="number">{total_autores}</div>
                <div class="label">Autores Analizados</div>
            </div>
            <div class="stat">
                <div class="number">{total_obras}</div>
                <div class="label">Obras Procesadas</div>
            </div>
            <div class="stat">
                <div class="number">{total_palabras:,}</div>
                <div class="label">Palabras Analizadas</div>
            </div>
        </div>
        
        <div class="content">
            <div class="autores-section">
                <h2>👥 Autores Disponibles</h2>
                <div class="autores-grid">
"""
        
        # Generar cards de autores
        for autor in autores:
            relacionados = relaciones.get(autor['nombre'], [])
            relaciones_str = ""
            if relacionados:
                relaciones_str = f"<br><small>🔗 Relacionado con: {', '.join([r['nombre'] for r in relacionados[:2]])}</small>"
            
            html += f"""
                    <div class="autor-card">
                        <div class="autor-nombre">👤 {autor['nombre']}</div>
                        <div class="autor-obras">📚 {autor['obras']}</div>
                        
                        <div class="metricas">
                            <div class="metrica">
                                <div class="valor">{autor['formalismo']:.2f}</div>
                                <div>Formalismo</div>
                            </div>
                            <div class="metrica">
                                <div class="valor">{autor['creatividad']:.2f}</div>
                                <div>Creatividad</div>
                            </div>
                            <div class="metrica">
                                <div class="valor">{autor['empirismo']:.2f}</div>
                                <div>Empirismo</div>
                            </div>
                            <div class="metrica">
                                <div class="valor">{autor['nivel_abstraccion']:.2f}</div>
                                <div>Abstracción</div>
                            </div>
                        </div>
                        
                        <div class="tipo-pensamiento">{autor['tipo_pensamiento']}</div>
                        <small style="color: #7f8c8d;">
                            📝 {autor['total_palabras']:,} palabras | 📅 {autor['ultima_actualizacion'][:10]}
                            {relaciones_str}
                        </small>
                    </div>
"""
        
        html += """
                </div>
            </div>
            
            <div class="relaciones">
                <h3>🔗 Relaciones Cognitivas</h3>
                <p style="color: #7f8c8d; font-size: 0.9em;">
                    Autores con perfiles cognitivos similares basados en análisis multidimensional
                </p>
"""
        
        # Generar sección de relaciones
        for autor_nombre, autor_relaciones in list(relaciones.items())[:5]:  # Top 5
            if autor_relaciones:
                html += f"""
                <div class="relacion">
                    <strong>{autor_nombre}</strong>
                    <br>
"""
                for rel in autor_relaciones[:2]:  # Top 2 relaciones por autor
                    html += f"""
                    <small>↔️ <strong>{rel['nombre']}</strong> ({rel['similitud']:.1%} similitud)</small><br>
                    <small style="color: #7f8c8d;">Dimensiones afines: {', '.join(rel['dimensiones_afines'][:2])}</small><br>
"""
                html += "</div>"
        
        html += """
            </div>
        </div>
        
        <div class="navegacion">
            <a href="/">🏠 Inicio</a>
            <a href="/cognitivo">🧠 Análisis Cognitivo</a>
            <a href="/radar">📊 Radar Cognitivo</a>
            <a href="/perfiles">👥 Perfiles</a>
        </div>
    </div>
    
    <script>
        // Hacer clickeable cada autor
        document.querySelectorAll('.autor-card').forEach(card => {
            card.addEventListener('click', function(e) {
                if (e.target.tagName !== 'A') {
                    const nombre = this.querySelector('.autor-nombre').textContent.replace('👤 ', '');
                    window.location.href = `/autor/${encodeURIComponent(nombre)}`;
                }
            });
        });
    </script>
</body>
</html>
"""
        
        return html

if __name__ == "__main__":
    # Generar y guardar la página
    biblioteca = BibliotecaCognitiva()
    html = biblioteca.generar_pagina_principal_html()
    
    with open("biblioteca_cognitiva.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ Página principal generada: biblioteca_cognitiva.html")
    print("🌐 Para integrar al sistema, copia este código a end2end_webapp.py")