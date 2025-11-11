#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 BIBLIOTECA COGNITIVA - ANÁLISIS MULTI-CAPA INTEGRADO v4.0
===========================================================
Sistema completo que extrae:
- PENSAMIENTO PURO del autor
- Patrones cognitivos profundos
- Arquitectura mental
- Análisis comparativo de autores
- Interpretaciones contextualizadas con Gemini
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

# Configuración de rutas
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"
MULTICAPA_DB = BASE_PATH / "bases_rag" / "cognitiva" / "multicapa_pensamiento.db"

class BibliotecaIntegrada:
    def __init__(self):
        self.db_path = DB_PATH
        self.multicapa_db = MULTICAPA_DB
        self.gemini_model = None
        
        # Inicializar Gemini
        if GEMINI_DISPONIBLE:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        
    def verificar_bases_datos(self):
        """Verifica qué bases de datos están disponibles y con qué datos"""
        info = {
            'metadatos_db': {'existe': self.db_path.exists(), 'registros': 0},
            'multicapa_db': {'existe': self.multicapa_db.exists(), 'registros': 0}
        }
        
        # Verificar BD de metadatos
        if self.db_path.exists():
            try:
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
                info['metadatos_db']['registros'] = cursor.fetchone()[0]
                conn.close()
            except Exception as e:
                print(f"Error verificando metadatos.db: {e}")
        
        # Verificar BD multicapa
        if self.multicapa_db.exists():
            try:
                conn = sqlite3.connect(str(self.multicapa_db))
                cursor = conn.cursor()
                # Obtener tablas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    info['multicapa_db'][table[0]] = count
                conn.close()
            except Exception as e:
                print(f"Error verificando multicapa_db: {e}")
        
        return info
    
    def obtener_autores_con_datos_completos(self):
        """Obtiene autores con todos los datos cognitivos disponibles"""
        
        if not self.db_path.exists():
            return []
        
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Consulta que obtiene TODOS los datos disponibles
        cursor.execute("""
            SELECT 
                autor,
                COUNT(*) as total_obras,
                MAX(fecha_analisis) as fecha_analisis,
                AVG(formalismo) as formalismo,
                AVG(creatividad) as creatividad,
                AVG(dogmatismo) as dogmatismo,
                AVG(empirismo) as empirismo,
                AVG(interdisciplinariedad) as interdisciplinariedad,
                AVG(nivel_abstraccion) as nivel_abstraccion,
                AVG(complejidad_sintactica) as complejidad_sintactica,
                AVG(uso_jurisprudencia) as uso_jurisprudencia,
                SUM(total_palabras) as total_palabras,
                AVG(ethos) as ethos,
                AVG(pathos) as pathos,
                AVG(logos) as logos,
                AVG(nivel_tecnico) as nivel_tecnico,
                GROUP_CONCAT(DISTINCT razonamiento_dominante) as razonamiento_dominante,
                GROUP_CONCAT(DISTINCT modalidad_epistemica) as modalidad_epistemica,
                GROUP_CONCAT(DISTINCT estructura_silogistica) as estructura_silogistica,
                MAX(metadatos_json) as metadatos,
                GROUP_CONCAT(DISTINCT tipo_pensamiento) as tipo_pensamiento
            FROM perfiles_cognitivos
            WHERE autor IS NOT NULL 
                AND autor NOT IN ('Autor no identificado', 'Desconocido')
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
                'fecha_analisis': row['fecha_analisis'],
                'formalismo': row['formalismo'] or 0,
                'creatividad': row['creatividad'] or 0,
                'dogmatismo': row['dogmatismo'] or 0,
                'empirismo': row['empirismo'] or 0,
                'interdisciplinariedad': row['interdisciplinariedad'] or 0,
                'nivel_abstraccion': row['nivel_abstraccion'] or 0,
                'complejidad_sintactica': row['complejidad_sintactica'] or 0,
                'uso_jurisprudencia': row['uso_jurisprudencia'] or 0,
                'total_palabras': row['total_palabras'] or 0,
                'ethos': row['ethos'] or 0,
                'pathos': row['pathos'] or 0,
                'logos': row['logos'] or 0,
                'nivel_tecnico': row['nivel_tecnico'] or 0,
                'razonamiento_dominante': row['razonamiento_dominante'] or 'No clasificado',
                'modalidad_epistemica': row['modalidad_epistemica'] or 'No clasificada',
                'estructura_silogistica': row['estructura_silogistica'] or 'No detectada',
                'tipo_pensamiento': row['tipo_pensamiento'] or 'Jurídico-Aristotélico'
            }
            autores.append(autor)
        
        return autores
    
    def generar_analisis_multicapa(self, autor):
        """Genera análisis multi-capa del pensamiento del autor"""
        
        analisis = {
            'capa_semantica': self._analizar_capa_semantica(autor),
            'capa_cognitiva': self._analizar_capa_cognitiva(autor),
            'capa_metodologica': self._analizar_capa_metodologica(autor),
            'capa_evolutiva': self._analizar_capa_evolutiva(autor),
            'capa_relacional': self._analizar_capa_relacional(autor),
        }
        
        return analisis
    
    def _analizar_capa_semantica(self, autor):
        """Análisis de conceptos y vocabulario"""
        return f"Utiliza {autor['total_palabras']:,} palabras en su construcción argumentativa. Densidad conceptual y riqueza semántica."
    
    def _analizar_capa_cognitiva(self, autor):
        """Análisis de patrones de pensamiento"""
        patrones = []
        
        if autor['nivel_abstraccion'] > 0.7:
            patrones.append("Pensamiento altamente abstracto - genera teorías generales")
        if autor['empirismo'] > 0.7:
            patrones.append("Anclado en lo empírico - fundamenta en casos reales")
        if autor['creatividad'] > 0.6:
            patrones.append("Alto nivel creativo - propone nuevas perspectivas")
        if autor['complejidad_sintactica'] > 0.7:
            patrones.append("Estructura argumentativa compleja y sofisticada")
        
        return " | ".join(patrones) if patrones else "Patrón cognitivo mixto"
    
    def _analizar_capa_metodologica(self, autor):
        """Análisis de métodos de razonamiento"""
        metodos = []
        
        if autor['formalismo'] > 0.7:
            metodos.append("Método: Formalista (basado en normas)")
        elif autor['creatividad'] > 0.6:
            metodos.append("Método: Interpretativo (enfoque flexible)")
        else:
            metodos.append("Método: Ecléctico (mixto)")
        
        if autor['logos'] > 0.7:
            metodos.append("Retórica: Lógica rigurosa")
        if autor['ethos'] > 0.6:
            metodos.append("Estrategia: Construcción de autoridad")
        
        return " | ".join(metodos)
    
    def _analizar_capa_evolutiva(self, autor):
        """Análisis de cambios temporales"""
        return f"Evolución registrada desde {str(autor['fecha_analisis'])[:10]}. Constelación de {autor['total_obras']} obra(s) procesada(s)."
    
    def _analizar_capa_relacional(self, autor):
        """Análisis de relaciones e influencias"""
        influencias = []
        
        if autor['uso_jurisprudencia'] > 0.5:
            influencias.append("Influencias jurisprudenciales detectadas")
        if autor['interdisciplinariedad'] > 0.4:
            influencias.append("Diálogos interdisciplinarios presentes")
        
        return " | ".join(influencias) if influencias else "Red relacional identificada"
    
    def generar_html_completo(self):
        """Genera HTML con sistema Multi-Capa integrado"""
        
        # Verificar bases de datos
        info_db = self.verificar_bases_datos()
        autores = self.obtener_autores_con_datos_completos()
        
        # Estadísticas
        total_autores = len(autores)
        total_obras = sum(a['total_obras'] for a in autores)
        total_palabras = sum(a['total_palabras'] for a in autores)
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Biblioteca Cognitiva Multi-Capa</title>
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
            max-width: 1800px;
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
            font-weight: 500;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 30px;
            padding: 40px;
        }}
        
        .sidebar {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            border: 2px solid #e9ecef;
            height: fit-content;
        }}
        
        .sidebar h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.1em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .autor-item {{
            background: white;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
            cursor: pointer;
            border-left: 4px solid #3498db;
            transition: all 0.3s;
        }}
        
        .autor-item:hover {{
            transform: translateX(5px);
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }}
        
        .autor-item.active {{
            background: #3498db;
            color: white;
        }}
        
        .autor-nombre {{
            font-weight: 600;
            font-size: 0.9em;
        }}
        
        .main {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .perfil {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            border: 2px solid #e9ecef;
        }}
        
        .perfil h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .capa {{
            background: white;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 5px solid #9b59b6;
        }}
        
        .capa h4 {{
            color: #9b59b6;
            margin-bottom: 10px;
            font-size: 1em;
        }}
        
        .capa p {{
            color: #555;
            line-height: 1.6;
            font-size: 0.95em;
        }}
        
        .metricas {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 12px;
            margin-top: 15px;
        }}
        
        .metrica {{
            background: white;
            padding: 12px;
            border-radius: 6px;
            text-align: center;
            border-left: 3px solid #3498db;
        }}
        
        .metrica-label {{
            font-size: 0.8em;
            color: #7f8c8d;
            margin-bottom: 5px;
        }}
        
        .metrica-valor {{
            font-size: 1.5em;
            font-weight: bold;
            color: #3498db;
        }}
        
        .info-db {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 6px;
            font-size: 0.9em;
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
            <h1>🧠 BIBLIOTECA COGNITIVA - ANÁLISIS MULTI-CAPA</h1>
            <p>Análisis profundo del PENSAMIENTO PURO: patrones cognitivos, arquitectura mental y evolución intelectual</p>
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
                <h3>👥 Autores</h3>
                <div id="autores-list">
"""
        
        # Lista de autores
        for i, autor in enumerate(autores):
            active = 'active' if i == 0 else ''
            html += f"""
                    <div class="autor-item {active}" onclick="seleccionar({i})">
                        <div class="autor-nombre">👤 {autor['nombre']}</div>
                        <div style="font-size: 0.8em; opacity: 0.7; margin-top: 3px;">📝 {autor['total_palabras']:,}</div>
                    </div>
"""
        
        html += """
                </div>
            </div>
            
            <div class="main" id="main">
"""
        
        # Perfiles con análisis multi-capa
        for i, autor in enumerate(autores):
            display = 'block' if i == 0 else 'none'
            analisis = self.generar_analisis_multicapa(autor)
            
            html += f"""
                <div class="perfil" id="perfil-{i}" style="display: {display}">
                    <h2>👤 {autor['nombre']}</h2>
                    
                    <div class="info-db">
                        📊 <strong>Estadísticas:</strong> {autor['total_obras']} obra(s) | {autor['total_palabras']:,} palabras | Tipo: {autor['tipo_pensamiento']}
                    </div>
                    
                    <div class="capa">
                        <h4>🧬 CAPA SEMÁNTICA - Vocabulario y Conceptos</h4>
                        <p>{analisis['capa_semantica']}</p>
                    </div>
                    
                    <div class="capa">
                        <h4>🧠 CAPA COGNITIVA - Patrones de Pensamiento</h4>
                        <p>{analisis['capa_cognitiva']}</p>
                        <div class="metricas">
                            <div class="metrica">
                                <div class="metrica-label">Abstracción</div>
                                <div class="metrica-valor">{autor['nivel_abstraccion']:.2f}</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-label">Creatividad</div>
                                <div class="metrica-valor">{autor['creatividad']:.2f}</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-label">Empirismo</div>
                                <div class="metrica-valor">{autor['empirismo']:.2f}</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-label">Complejidad</div>
                                <div class="metrica-valor">{autor['complejidad_sintactica']:.2f}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="capa">
                        <h4>🔧 CAPA METODOLÓGICA - Estrategias de Razonamiento</h4>
                        <p>{analisis['capa_metodologica']}</p>
                        <div class="metricas">
                            <div class="metrica">
                                <div class="metrica-label">Formalismo</div>
                                <div class="metrica-valor">{autor['formalismo']:.2f}</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-label">Logos</div>
                                <div class="metrica-valor">{autor['logos']:.2f}</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-label">Ethos</div>
                                <div class="metrica-valor">{autor['ethos']:.2f}</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-label">Jurisprudencia</div>
                                <div class="metrica-valor">{autor['uso_jurisprudencia']:.2f}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="capa">
                        <h4>⏳ CAPA EVOLUTIVA - Desarrollo Temporal</h4>
                        <p>{analisis['capa_evolutiva']}</p>
                    </div>
                    
                    <div class="capa">
                        <h4>🔗 CAPA RELACIONAL - Redes de Influencia</h4>
                        <p>{analisis['capa_relacional']}</p>
                        <div class="metricas">
                            <div class="metrica">
                                <div class="metrica-label">Interdisciplinariedad</div>
                                <div class="metrica-valor">{autor['interdisciplinariedad']:.2f}</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-label">Pathos</div>
                                <div class="metrica-valor">{autor['pathos']:.2f}</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-label">Dogmatismo</div>
                                <div class="metrica-valor">{autor['dogmatismo']:.2f}</div>
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
        function seleccionar(i) {
            document.querySelectorAll('.autor-item').forEach((el, idx) => {
                el.classList.toggle('active', idx === i);
            });
            document.querySelectorAll('.perfil').forEach((el, idx) => {
                el.style.display = idx === i ? 'block' : 'none';
            });
        }
    </script>
</body>
</html>
"""
        
        return html

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧠 GENERANDO BIBLIOTECA MULTI-CAPA INTEGRADA")
    print("="*80 + "\n")
    
    biblioteca = BibliotecaIntegrada()
    
    # Verificar bases de datos
    print("📊 Verificando bases de datos...")
    info = biblioteca.verificar_bases_datos()
    print(f"   ✅ metadatos.db: {info['metadatos_db']['registros']} registros")
    print(f"   ✅ multicapa_db: existe = {info['multicapa_db']['existe']}\n")
    
    # Generar HTML
    html = biblioteca.generar_html_completo()
    
    output_path = Path(__file__).parent.parent / "biblioteca_multicapa.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Archivo generado: {output_path.name}")
    print(f"📊 Tamaño: {len(html):,} caracteres\n")
