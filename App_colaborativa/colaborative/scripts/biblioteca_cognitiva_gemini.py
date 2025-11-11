#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 BIBLIOTECA COGNITIVA CON ANÁLISIS INTERPRETATIVO DE GEMINI v3.0
==================================================================
- Análisis numérico de las 8 dimensiones cognitivas
- Interpretación contextual por Gemini
- Explicación del pensamiento aplicado a las obras
- Lenguaje natural y propiedades del pensamiento autoral
"""

import sqlite3
from pathlib import Path
import json
import os

# Importar Gemini
try:
    import google.generativeai as genai
    GEMINI_DISPONIBLE = True
except ImportError:
    GEMINI_DISPONIBLE = False
    print("⚠️ Gemini no disponible - instala: pip install google-generativeai")

# Configuración de rutas
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"

class BibliotecaCognitivaGemini:
    def __init__(self):
        self.db_path = DB_PATH
        self.gemini_model = None
        
        # Inicializar Gemini si está disponible
        if GEMINI_DISPONIBLE:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
                print("✅ Gemini configurado correctamente")
            else:
                print("⚠️ GOOGLE_API_KEY no configurada")
        
    def obtener_autores_completos(self):
        """Obtiene información completa de todos los autores"""
        
        if not self.db_path.exists():
            print(f"❌ DB no encontrada en: {self.db_path}")
            return []
        
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
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
                AVG(nivel_tecnico) as avg_nivel_tecnico,
                MAX(texto_muestra) as muestra_texto
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
                'nombre': row['autor'],
                'total_obras': row['total_obras'],
                'obras': row['obras'] if row['obras'] else 'Sin título específico',
                'archivos': row['archivos'],
                'formalismo': row['avg_formalismo'] or 0,
                'creatividad': row['avg_creatividad'] or 0,
                'dogmatismo': row['avg_dogmatismo'] or 0,
                'empirismo': row['avg_empirismo'] or 0,
                'interdisciplinariedad': row['avg_interdisciplinariedad'] or 0,
                'nivel_abstraccion': row['avg_nivel_abstraccion'] or 0,
                'complejidad_sintactica': row['avg_complejidad_sintactica'] or 0,
                'uso_jurisprudencia': row['avg_uso_jurisprudencia'] or 0,
                'total_palabras': row['total_palabras'] or 0,
                'tipo_pensamiento': row['tipos_pensamiento'] or 'No clasificado',
                'ultima_actualizacion': row['ultima_actualizacion'],
                'ethos': row['avg_ethos'] or 0,
                'pathos': row['avg_pathos'] or 0,
                'logos': row['avg_logos'] or 0,
                'nivel_tecnico': row['avg_nivel_tecnico'] or 0,
                'muestra_texto': row['muestra_texto'] or ''
            }
            autores.append(autor)
        
        return autores
    
    def generar_interpretacion_gemini(self, autor):
        """Genera interpretación contextual usando Gemini"""
        
        if not self.gemini_model:
            return self._generar_interpretacion_default(autor)
        
        try:
            # Construir prompt especializado
            prompt = f"""
Analiza el perfil cognitivo del autor JURÍDICO {autor['nombre']} y proporciona una interpretación 
clara y contextualizada de su pensamiento. Los datos numéricos son:

DIMENSIONES COGNITIVAS:
- Formalismo Jurídico: {autor['formalismo']:.3f} (uso de citas legales formales)
- Creatividad Conceptual: {autor['creatividad']:.3f} (originalidad argumentativa)
- Dogmatismo: {autor['dogmatismo']:.3f} (rigidez doctrinal)
- Empirismo Evidencial: {autor['empirismo']:.3f} (uso de datos/casos)
- Interdisciplinariedad: {autor['interdisciplinariedad']:.3f} (integración de disciplinas)
- Nivel de Abstracción: {autor['nivel_abstraccion']:.3f} (complejidad conceptual)
- Complejidad Sintáctica: {autor['complejidad_sintactica']:.3f} (estructura del lenguaje)
- Uso de Jurisprudencia: {autor['uso_jurisprudencia']:.3f} (referencias a precedentes)

RETÓRICA ARISTOTÉLICA:
- Ethos (Autoridad): {autor['ethos']:.3f}
- Pathos (Emoción): {autor['pathos']:.3f}
- Logos (Lógica): {autor['logos']:.3f}
- Nivel Técnico: {autor['nivel_tecnico']:.3f}

CONTEXTO:
- Total de palabras analizadas: {autor['total_palabras']:,}
- Número de obras procesadas: {autor['total_obras']}
- Tipo de pensamiento detectado: {autor['tipo_pensamiento']}

INSTRUCCIONES:
1. Proporciona un análisis interpretativo (NO solo números)
2. Explica qué tipo de pensamiento jurídico tiene este autor
3. Describe las características de su lenguaje y argumentación
4. Relaciona las métricas con propiedades reales del pensamiento
5. Menciona fortalezas y particularidades de su enfoque
6. Sé claro, profesional y accesible (no tecnicista)
7. Usa 2-3 párrafos máximo

Responde directamente sin prefijos ni explicaciones de lo que vas a hacer.
"""
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"⚠️ Error con Gemini: {e}")
            return self._generar_interpretacion_default(autor)
    
    def _generar_interpretacion_default(self, autor):
        """Interpretación fallback sin Gemini"""
        
        interpretaciones = []
        
        # Análisis de tendencias
        if autor['formalismo'] > 0.7:
            interpretaciones.append(f"El pensamiento de {autor['nombre']} es altamente formalista, basado en citas legales precisas y estructura jurídica rigurosa.")
        elif autor['formalismo'] > 0.4:
            interpretaciones.append(f"{autor['nombre']} emplea un enfoque semiformal, equilibrando citas legales con argumentación flexible.")
        else:
            interpretaciones.append(f"{autor['nombre']} adopta un enfoque poco formalista, enfatizando la interpretación sobre la literalidad normativa.")
        
        if autor['creatividad'] > 0.6:
            interpretaciones.append(f"Demuestra alta creatividad conceptual, proponiendo nuevas formas de entender los problemas jurídicos.")
        
        if autor['empirismo'] > 0.6:
            interpretaciones.append(f"Su pensamiento está fuertemente basado en casos concretos y evidencia empírica.")
        
        if autor['nivel_abstraccion'] > 0.7:
            interpretaciones.append(f"Trabaja en niveles altos de abstracción, desarrollando teorías generales.")
        
        if autor['complejidad_sintactica'] > 0.7:
            interpretaciones.append(f"Su lenguaje es complejo y estructurado, reflejando argumentación sofisticada.")
        
        if autor['logos'] > 0.7 and autor['pathos'] < 0.3:
            interpretaciones.append(f"Su retórica es primariamente lógica, sustentada en argumentos racionales rigurosos.")
        
        return "\n".join(interpretaciones) if interpretaciones else "Autor sin interpretación disponible."
    
    def generar_pagina_principal_html(self):
        """Genera HTML con análisis de Gemini integrado"""
        
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
    <title>📚 Biblioteca Cognitiva - Análisis Interpretativo</title>
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
        
        .seccion-interpretacion {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #9b59b6;
            margin-bottom: 20px;
            line-height: 1.8;
        }}
        
        .seccion-interpretacion h3 {{
            color: #9b59b6;
            font-size: 1.2em;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .seccion-interpretacion p {{
            color: #555;
            font-size: 0.95em;
            margin-bottom: 10px;
        }}
        
        .seccion-interpretacion p:last-child {{
            margin-bottom: 0;
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
        
        .metricas-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
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
        
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 8px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #3498db, #2980b9);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.7em;
            font-weight: bold;
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
            margin-bottom: 5px;
        }}
        
        .info-box p:last-child {{
            margin-bottom: 0;
        }}
        
        .gemini-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #9b59b6, #8e44ad);
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 500;
            margin-left: 10px;
        }}
        
        @media (max-width: 1200px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 BIBLIOTECA COGNITIVA DE AUTORES</h1>
            <p>Análisis Interpretativo del Pensamiento Jurídico con Gemini AI</p>
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
                    <div class="autor-item {active_class}" onclick="seleccionarAutor({i})">
                        <div class="autor-nombre">👤 {autor['nombre']}</div>
                        <div class="autor-palabras">📝 {autor['total_palabras']:,} palabras</div>
                    </div>
"""
        
        html += """
                </div>
            </div>
            
            <div class="main-content" id="main-content">
"""
        
        # Generar perfiles para cada autor
        for i, autor in enumerate(autores):
            display_style = 'display: block;' if i == 0 else 'display: none;'
            
            # Generar interpretación
            print(f"🧠 Generando interpretación para {autor['nombre']}...")
            interpretacion = self.generar_interpretacion_gemini(autor)
            
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
                        <p><strong>📝 Total de palabras:</strong> {autor['total_palabras']:,}</p>
                        <p><strong>🧠 Tipo de pensamiento:</strong> {autor['tipo_pensamiento']}</p>
                    </div>
                    
                    <div class="seccion-interpretacion">
                        <h3>🤖 INTERPRETACIÓN CON GEMINI {' ' if not self.gemini_model else ''}<span class="gemini-badge">GEMINI AI</span></h3>
                        <p>{interpretacion}</p>
                    </div>
                    
                    <div class="seccion">
                        <h3>📊 DIMENSIONES COGNITIVAS CUANTIFICADAS</h3>
                        <div class="metricas-grid">
                            <div class="metrica-box">
                                <div class="metrica-label">📏 Formalismo</div>
                                <div class="metrica-valor {get_intensity_class(autor['formalismo'])}">{autor['formalismo']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['formalismo']*100}%;">
                                        {int(autor['formalismo']*100)}%
                                    </div>
                                </div>
                            </div>
                            <div class="metrica-box">
                                <div class="metrica-label">🎨 Creatividad</div>
                                <div class="metrica-valor {get_intensity_class(autor['creatividad'])}">{autor['creatividad']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['creatividad']*100}%;">
                                        {int(autor['creatividad']*100)}%
                                    </div>
                                </div>
                            </div>
                            <div class="metrica-box">
                                <div class="metrica-label">🔒 Dogmatismo</div>
                                <div class="metrica-valor {get_intensity_class(autor['dogmatismo'])}">{autor['dogmatismo']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['dogmatismo']*100}%;">
                                        {int(autor['dogmatismo']*100)}%
                                    </div>
                                </div>
                            </div>
                            <div class="metrica-box">
                                <div class="metrica-label">🔬 Empirismo</div>
                                <div class="metrica-valor {get_intensity_class(autor['empirismo'])}">{autor['empirismo']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['empirismo']*100}%;">
                                        {int(autor['empirismo']*100)}%
                                    </div>
                                </div>
                            </div>
                            <div class="metrica-box">
                                <div class="metrica-label">🌐 Interdisciplinariedad</div>
                                <div class="metrica-valor {get_intensity_class(autor['interdisciplinariedad'])}">{autor['interdisciplinariedad']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['interdisciplinariedad']*100}%;">
                                        {int(autor['interdisciplinariedad']*100)}%
                                    </div>
                                </div>
                            </div>
                            <div class="metrica-box">
                                <div class="metrica-label">🧩 Abstracción</div>
                                <div class="metrica-valor {get_intensity_class(autor['nivel_abstraccion'])}">{autor['nivel_abstraccion']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['nivel_abstraccion']*100}%;">
                                        {int(autor['nivel_abstraccion']*100)}%
                                    </div>
                                </div>
                            </div>
                            <div class="metrica-box">
                                <div class="metrica-label">📝 Complejidad Sintáctica</div>
                                <div class="metrica-valor {get_intensity_class(autor['complejidad_sintactica'])}">{autor['complejidad_sintactica']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['complejidad_sintactica']*100}%;">
                                        {int(autor['complejidad_sintactica']*100)}%
                                    </div>
                                </div>
                            </div>
                            <div class="metrica-box">
                                <div class="metrica-label">⚖️ Jurisprudencia</div>
                                <div class="metrica-valor {get_intensity_class(autor['uso_jurisprudencia'])}">{autor['uso_jurisprudencia']:.3f}</div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {autor['uso_jurisprudencia']*100}%;">
                                        {int(autor['uso_jurisprudencia']*100)}%
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="seccion">
                        <h3>🎭 RETÓRICA ARISTOTÉLICA</h3>
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
        function seleccionarAutor(indice) {
            document.querySelectorAll('.autor-item').forEach((item, idx) => {
                if (idx === indice) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });
            
            document.querySelectorAll('.perfil-card').forEach((card, idx) => {
                if (idx === indice) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""
        
        return html

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 GENERANDO BIBLIOTECA CON ANÁLISIS INTERPRETATIVO DE GEMINI")
    print("="*80 + "\n")
    
    biblioteca = BibliotecaCognitivaGemini()
    html = biblioteca.generar_pagina_principal_html()
    
    output_path = Path(__file__).parent.parent / "biblioteca_con_gemini.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ Archivo generado: {output_path.name}")
    print(f"📊 Tamaño: {len(html):,} caracteres\n")
