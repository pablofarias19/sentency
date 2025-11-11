#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 BIBLIOTECA COGNITIVA MEJORADA v2.0
===========================================
- Selector de autores disponibles
- Análisis Multi-Capa del Pensamiento
- Visualización de variables/dimensiones analizadas
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import json

# Configuración de rutas
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"

class BibliotecaCognitivaMejorada:
    def __init__(self):
        self.db_path = DB_PATH
        
    def obtener_autores_completos(self):
        """Obtiene información completa de todos los autores"""
        
        if not self.db_path.exists():
            print(f"❌ DB no encontrada en: {self.db_path}")
            return []
        
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
                COALESCE(SUM(total_palabras), 0) as total_palabras,
                GROUP_CONCAT(DISTINCT tipo_pensamiento) as tipos_pensamiento,
                MAX(fecha_analisis) as ultima_actualizacion,
                AVG(ethos) as avg_ethos,
                AVG(pathos) as avg_pathos,
                AVG(logos) as avg_logos,
                AVG(nivel_tecnico) as avg_nivel_tecnico
            FROM perfiles_cognitivos 
            WHERE autor IS NOT NULL AND autor != 'Autor no identificado' AND autor != 'Desconocido'
            GROUP BY autor
            ORDER BY total_palabras DESC
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
                'ultima_actualizacion': row[14],
                'ethos': row[15] or 0,
                'pathos': row[16] or 0,
                'logos': row[17] or 0,
                'nivel_tecnico': row[18] or 0
            }
            autores.append(autor)
        
        return autores
    
    def generar_pagina_principal_html(self):
        """Genera HTML de la página principal mejorada con selector de autores"""
        
        autores = self.obtener_autores_completos()
        
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
    <title>📚 Biblioteca Cognitiva de Autores v2.0</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.8em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            background: #ecf0f1;
            padding: 30px 40px;
            margin: 0;
        }}
        
        .stat {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .stat .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 10px;
        }}
        
        .stat .label {{
            color: #7f8c8d;
            font-size: 0.95em;
            font-weight: 500;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 30px;
            padding: 40px;
        }}
        
        .sidebar {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            border: 2px solid #e9ecef;
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .sidebar h3 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.3em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .autor-item {{
            background: white;
            padding: 15px;
            margin-bottom: 12px;
            border-radius: 8px;
            cursor: pointer;
            border-left: 4px solid #3498db;
            transition: all 0.3s ease;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .autor-item:hover {{
            transform: translateX(5px);
            box-shadow: 0 3px 12px rgba(0,0,0,0.15);
            border-left-color: #e74c3c;
        }}
        
        .autor-item.active {{
            background: #3498db;
            color: white;
            border-left-color: #2980b9;
        }}
        
        .autor-nombre {{
            font-weight: 600;
            font-size: 0.95em;
        }}
        
        .autor-palabras {{
            font-size: 0.8em;
            opacity: 0.7;
            margin-top: 4px;
        }}
        
        .autor-item.active .autor-palabras {{
            opacity: 0.9;
        }}
        
        .badge {{
            background: rgba(255,255,255,0.3);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 500;
        }}
        
        .autor-item.active .badge {{
            background: rgba(0,0,0,0.2);
        }}
        
        .main-content {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .perfil-card {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            border: 2px solid #e9ecef;
        }}
        
        .perfil-card h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .metricas-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .metrica-box {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        
        .metrica-label {{
            font-size: 0.85em;
            color: #7f8c8d;
            margin-bottom: 8px;
            font-weight: 500;
        }}
        
        .metrica-valor {{
            font-size: 1.8em;
            font-weight: bold;
            color: #3498db;
        }}
        
        .metrica-valor.high {{
            color: #27ae60;
        }}
        
        .metrica-valor.medium {{
            color: #f39c12;
        }}
        
        .metrica-valor.low {{
            color: #e74c3c;
        }}
        
        .seccion {{
            margin-top: 20px;
        }}
        
        .seccion h3 {{
            color: #2c3e50;
            font-size: 1.2em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .variables-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }}
        
        .variable-item {{
            background: white;
            padding: 12px;
            border-radius: 6px;
            border-left: 3px solid #3498db;
            font-size: 0.9em;
        }}
        
        .variable-label {{
            color: #7f8c8d;
            font-size: 0.85em;
            margin-bottom: 5px;
        }}
        
        .variable-valor {{
            color: #2c3e50;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        .info-box {{
            background: #ecf0f1;
            border-left: 4px solid #3498db;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
        }}
        
        .info-box p {{
            color: #555;
            line-height: 1.6;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
        }}
        
        .empty-state p {{
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        
        .dimensiones-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        .dimensiones-table th,
        .dimensiones-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .dimensiones-table th {{
            background: #ecf0f1;
            font-weight: 600;
            color: #2c3e50;
        }}
        
        .dimensiones-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #3498db, #2980b9);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.75em;
            font-weight: bold;
        }}
        
        @media (max-width: 1200px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
            
            .sidebar {{
                max-height: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 BIBLIOTECA COGNITIVA DE AUTORES v2.0</h1>
            <p>Sistema integral de análisis del pensamiento autoral</p>
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
            <div class="sidebar">
                <h3>👥 Autores Disponibles</h3>
                <div id="autores-list">
"""
        
        # Generar lista de autores
        for i, autor in enumerate(autores):
            active_class = 'active' if i == 0 else ''
            html += f"""
                    <div class="autor-item {active_class}" onclick="seleccionarAutor('{autor['nombre']}', {i})">
                        <div>
                            <div class="autor-nombre">{autor['nombre']}</div>
                            <div class="autor-palabras">📝 {autor['total_palabras']:,} palabras</div>
                        </div>
                        <div class="badge">{autor['total_obras']} obra{'s' if autor['total_obras'] > 1 else ''}</div>
                    </div>
"""
        
        html += """
                </div>
            </div>
            
            <div class="main-content" id="main-content">
"""
        
        # Generar perfiles para cada autor (inicialmente ocultos)
        for i, autor in enumerate(autores):
            display_style = 'display: block;' if i == 0 else 'display: none;'
            
            # Determinar intensidad de colores basado en valores
            def get_intensity_class(value):
                if value >= 0.7:
                    return 'high'
                elif value >= 0.4:
                    return 'medium'
                else:
                    return 'low'
            
            html += f"""
                <div class="perfil-card" id="perfil-{i}" style="{display_style}">
                    <h2>👤 {autor['nombre']}</h2>
                    
                    <div class="info-box">
                        <p><strong>📚 Obras:</strong> {autor['total_obras']}</p>
                        <p><strong>📝 Total de palabras analizadas:</strong> {autor['total_palabras']:,}</p>
                        <p><strong>🧠 Tipo de pensamiento:</strong> {autor['tipo_pensamiento']}</p>
                        <p><strong>📅 Última actualización:</strong> {str(autor['ultima_actualizacion'])[:10]}</p>
                    </div>
                    
                    <h3>📊 LAS 8 DIMENSIONES COGNITIVAS ANALIZADAS</h3>
                    <table class="dimensiones-table">
                        <thead>
                            <tr>
                                <th>Dimensión</th>
                                <th>Descripción</th>
                                <th>Valor</th>
                                <th>Visualización</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>📏 Formalismo Jurídico</td>
                                <td>Uso de citas legales formales</td>
                                <td class="metrica-valor {get_intensity_class(autor['formalismo'])}">{autor['formalismo']:.3f}</td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {autor['formalismo']*100}%;">
                                            {int(autor['formalismo']*100)}%
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>🎨 Creatividad Conceptual</td>
                                <td>Originalidad en argumentación</td>
                                <td class="metrica-valor {get_intensity_class(autor['creatividad'])}">{autor['creatividad']:.3f}</td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {autor['creatividad']*100}%;">
                                            {int(autor['creatividad']*100)}%
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>🔒 Dogmatismo</td>
                                <td>Rigidez vs flexibilidad doctrinal</td>
                                <td class="metrica-valor {get_intensity_class(autor['dogmatismo'])}">{autor['dogmatismo']:.3f}</td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {autor['dogmatismo']*100}%;">
                                            {int(autor['dogmatismo']*100)}%
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>🔬 Empirismo Evidencial</td>
                                <td>Uso de datos y casos concretos</td>
                                <td class="metrica-valor {get_intensity_class(autor['empirismo'])}">{autor['empirismo']:.3f}</td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {autor['empirismo']*100}%;">
                                            {int(autor['empirismo']*100)}%
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>🌐 Interdisciplinariedad</td>
                                <td>Integración de otras disciplinas</td>
                                <td class="metrica-valor {get_intensity_class(autor['interdisciplinariedad'])}">{autor['interdisciplinariedad']:.3f}</td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {autor['interdisciplinariedad']*100}%;">
                                            {int(autor['interdisciplinariedad']*100)}%
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>🧩 Nivel de Abstracción</td>
                                <td>Complejidad conceptual</td>
                                <td class="metrica-valor {get_intensity_class(autor['nivel_abstraccion'])}">{autor['nivel_abstraccion']:.3f}</td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {autor['nivel_abstraccion']*100}%;">
                                            {int(autor['nivel_abstraccion']*100)}%
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>📝 Complejidad Sintáctica</td>
                                <td>Estructura del lenguaje</td>
                                <td class="metrica-valor {get_intensity_class(autor['complejidad_sintactica'])}">{autor['complejidad_sintactica']:.3f}</td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {autor['complejidad_sintactica']*100}%;">
                                            {int(autor['complejidad_sintactica']*100)}%
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>⚖️ Uso de Jurisprudencia</td>
                                <td>Referencias a precedentes</td>
                                <td class="metrica-valor {get_intensity_class(autor['uso_jurisprudencia'])}">{autor['uso_jurisprudencia']:.3f}</td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {autor['uso_jurisprudencia']*100}%;">
                                            {int(autor['uso_jurisprudencia']*100)}%
                                        </div>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <div class="seccion">
                        <h3>🎭 DIMENSIONES RETÓRICAS ARISTOTÉLICAS</h3>
                        <div class="metricas-grid">
                            <div class="metrica-box">
                                <div class="metrica-label">🎭 Ethos (Autoridad)</div>
                                <div class="metrica-valor">{autor['ethos']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['ethos']*100}%; background: linear-gradient(90deg, #9b59b6, #8e44ad);">
                                        {int(autor['ethos']*100)}%
                                    </div>
                                </div>
                            </div>
                            <div class="metrica-box">
                                <div class="metrica-label">❤️ Pathos (Emocional)</div>
                                <div class="metrica-valor">{autor['pathos']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['pathos']*100}%; background: linear-gradient(90deg, #e74c3c, #c0392b);">
                                        {int(autor['pathos']*100)}%
                                    </div>
                                </div>
                            </div>
                            <div class="metrica-box">
                                <div class="metrica-label">🧠 Logos (Lógica)</div>
                                <div class="metrica-valor">{autor['logos']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['logos']*100}%; background: linear-gradient(90deg, #27ae60, #229954);">
                                        {int(autor['logos']*100)}%
                                    </div>
                                </div>
                            </div>
                            <div class="metrica-box">
                                <div class="metrica-label">🏛️ Nivel Técnico</div>
                                <div class="metrica-valor">{autor['nivel_tecnico']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['nivel_tecnico']*100}%; background: linear-gradient(90deg, #f39c12, #d68910);">
                                        {int(autor['nivel_tecnico']*100)}%
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
    </div>
    
    <script>
        function seleccionarAutor(nombre, indice) {
            // Actualizar items
            document.querySelectorAll('.autor-item').forEach((item, idx) => {
                if (idx === indice) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });
            
            // Actualizar perfiles
            document.querySelectorAll('.perfil-card').forEach((card, idx) => {
                if (idx === indice) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        // Seleccionar primer autor por defecto
        document.addEventListener('DOMContentLoaded', function() {
            seleccionarAutor(document.querySelector('.autor-item').textContent, 0);
        });
    </script>
</body>
</html>
"""
        
        return html

if __name__ == "__main__":
    # Generar y guardar la página
    biblioteca = BibliotecaCognitivaMejorada()
    html = biblioteca.generar_pagina_principal_html()
    
    with open("biblioteca_mejorada.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ Página mejorada generada: biblioteca_mejorada.html")
