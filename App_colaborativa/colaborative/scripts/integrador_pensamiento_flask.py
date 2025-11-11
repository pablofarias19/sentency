#!/usr/bin/env python3
"""
🔗 INTEGRADOR DE PENSAMIENTO MULTICAPA - Flask Route
====================================================

Proporciona la ruta /pensamiento en Flask usando biblioteca_multicapa_integrada.py
para garantizar consistencia de datos entre:
  - /pensamiento (puerto 5002)
  - /biblioteca_multicapa.html (puerto 8888)

AUTOR: Sistema de Integración
FECHA: 10 NOV 2025
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class IntegradorPensamientoFlask:
    """
    Proporciona datos multi-capa de pensamiento para rutas Flask
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.db_path = self.base_path / "colaborative" / "bases_rag" / "cognitiva" / "metadatos.db"
        
    def obtener_autores_disponibles(self) -> List[Dict[str, Any]]:
        """Obtiene lista de autores disponibles"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            c.execute("""
                SELECT 
                    autor as nombre,
                    archivo,
                    total_palabras,
                    formalismo,
                    creatividad,
                    dogmatismo,
                    empirismo
                FROM perfiles_cognitivos
                GROUP BY autor
                ORDER BY autor
            """)
            
            autores = [dict(row) for row in c.fetchall()]
            conn.close()
            
            return autores
        except Exception as e:
            print(f"❌ Error obteniendo autores: {e}")
            return []
    
    def obtener_analisis_autor(self, nombre_autor: str) -> Optional[Dict[str, Any]]:
        """Obtiene análisis completo de un autor"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            # Obtener perfil principal (cambiar 'nombre' por 'autor')
            c.execute("""
                SELECT * FROM perfiles_cognitivos 
                WHERE autor = ?
                LIMIT 1
            """, (nombre_autor,))
            
            perfil = c.fetchone()
            if not perfil:
                conn.close()
                return None
            
            perfil_dict = dict(perfil)
            
            # Generar análisis multicapa
            analisis = self._generar_analisis_multicapa(perfil_dict)
            
            conn.close()
            return analisis
            
        except Exception as e:
            print(f"❌ Error obteniendo análisis de {nombre_autor}: {e}")
            return None
    
    def _normalizar_perfil(self, perfil: Dict) -> Dict:
        """Normaliza valores None a 0 en todas las métricas"""
        metricas = [
            "formalismo", "creatividad", "dogmatismo", "empirismo",
            "interdisciplinariedad", "nivel_abstraccion", "complejidad_sintactica",
            "ethos", "pathos", "logos", "nivel_tecnico", "densidad_conceptual",
            "uso_ejemplos", "densidad_citas", "uso_jurisprudencia"
        ]
        for metrica in metricas:
            if perfil.get(metrica) is None:
                perfil[metrica] = 0
        return perfil
    
    def _generar_analisis_multicapa(self, perfil: Dict) -> Dict[str, Any]:
        """Genera análisis en 5 capas"""
        
        # Normalizar None a 0 en todas las métricas numéricas
        perfil = self._normalizar_perfil(perfil)
        
        return {
            "autor": perfil.get("autor"),  # Cambiar de "nombre" a "autor"
            "archivo": perfil.get("archivo"),
            "total_palabras": perfil.get("total_palabras", 0),
            
            # CAPA SEMÁNTICA
            "capa_semantica": {
                "densidad_conceptual": perfil.get("densidad_conceptual", 0),
                "vocabulario_distintivo": self._generar_vocabulario(perfil),
                "complejidad_sintactica": perfil.get("complejidad_sintactica", 0)
            },
            
            # CAPA COGNITIVA (Métricas principales)
            "capa_cognitiva": {
                "formalismo": perfil.get("formalismo", 0),
                "creatividad": perfil.get("creatividad", 0),
                "dogmatismo": perfil.get("dogmatismo", 0),
                "empirismo": perfil.get("empirismo", 0),
                
                # Métricas Aristotélicas
                "ethos": perfil.get("ethos", 0),
                "pathos": perfil.get("pathos", 0),
                "logos": perfil.get("logos", 0),
                "nivel_tecnico": perfil.get("nivel_tecnico", 0),
                
                # Patrón dominante
                "patron_dominante": self._calcular_patron_dominante(perfil)
            },
            
            # CAPA METODOLÓGICA
            "capa_metodologica": {
                "tipo_razonamiento": self._clasificar_razonamiento(perfil),
                "estructura_argumentativa": self._generar_estructura_argumentativa(perfil),
                "uso_ejemplos": perfil.get("uso_ejemplos", 0),
                "densidad_citas": perfil.get("densidad_citas", 0)
            },
            
            # CAPA EVOLUTIVA
            "capa_evolutiva": {
                "etapa": self._clasificar_etapa_temporal(perfil),
                "madurez": self._calcular_madurez_intelectual(perfil),
                "innovaciones": self._extraer_innovaciones(perfil)
            },
            
            # CAPA RELACIONAL
            "capa_relacional": {
                "influencias": self._extraer_influencias(perfil),
                "interdisciplinariedad": perfil.get("interdisciplinariedad", 0),
                "nivel_abstraccion": perfil.get("nivel_abstraccion", 0)
            },
            
            # FIRMA INTELECTUAL
            "firma_intelectual": {
                "originalidad_score": self._calcular_originalidad(perfil),
                "coherencia_interna": self._calcular_coherencia(perfil),
                "distintividad": self._calcular_distintividad(perfil),
                "complejidad_global": perfil.get("complejidad_sintactica", 0)
            }
        }
    
    def _calcular_patron_dominante(self, perfil: Dict) -> str:
        """Determina el patrón cognitivo dominante"""
        valores = {
            "Formal": perfil.get("formalismo") or 0,
            "Creativo": perfil.get("creatividad") or 0,
            "Dogmático": perfil.get("dogmatismo") or 0,
            "Empírico": perfil.get("empirismo") or 0
        }
        return max(valores, key=valores.get)
    
    def _clasificar_razonamiento(self, perfil: Dict) -> str:
        """Clasifica el tipo de razonamiento principal"""
        formalismo = perfil.get("formalismo", 0)
        empirismo = perfil.get("empirismo", 0)
        
        if formalismo > 0.7:
            return "Deductivo-Formal"
        elif empirismo > 0.7:
            return "Inductivo-Empírico"
        else:
            return "Mixto-Ecléctico"
    
    def _generar_estructura_argumentativa(self, perfil: Dict) -> Dict[str, str]:
        """Genera estructura argumentativa típica del autor"""
        return {
            "introduccion": "Presentación de problema jurídico",
            "desarrollo": self._generar_desarrollo(perfil),
            "conclusion": "Resolución fundamentada en principios"
        }
    
    def _generar_desarrollo(self, perfil: Dict) -> str:
        """Tipo de desarrollo según métricas"""
        if perfil.get("formalismo", 0) > 0.6:
            return "Análisis sistemático de normas y principios"
        elif perfil.get("creatividad", 0) > 0.6:
            return "Exploración innovadora con ejemplos"
        else:
            return "Revisión de doctrina y jurisprudencia"
    
    def _calcular_originalidad(self, perfil: Dict) -> float:
        """Calcula score de originalidad"""
        creatividad = perfil.get("creatividad", 0)
        interdisciplinariedad = perfil.get("interdisciplinariedad", 0)
        return min(1.0, (creatividad + interdisciplinariedad) / 2)
    
    def _calcular_coherencia(self, perfil: Dict) -> float:
        """Calcula coherencia interna"""
        formalismo = perfil.get("formalismo", 0)
        logos = perfil.get("logos", 0)
        return min(1.0, (formalismo + logos) / 2)
    
    def _calcular_distintividad(self, perfil: Dict) -> float:
        """Calcula distintividad del autor"""
        metricas = [
            perfil.get("creatividad", 0),
            perfil.get("interdisciplinariedad", 0),
            perfil.get("nivel_abstraccion", 0)
        ]
        return sum(metricas) / 3
    
    def _calcular_madurez_intelectual(self, perfil: Dict) -> str:
        """Clasifica madurez según métricas"""
        promedio = sum([
            perfil.get("formalismo", 0),
            perfil.get("logos", 0),
            perfil.get("nivel_tecnico", 0)
        ]) / 3
        
        if promedio > 0.7:
            return "Madurez avanzada"
        elif promedio > 0.5:
            return "Madurez media"
        else:
            return "Desarrollo emergente"
    
    def _generar_vocabulario(self, perfil: Dict) -> List[str]:
        """Genera vocabulario distintivo del autor"""
        nombre = perfil.get("nombre", "")
        
        # Vocabulario base según el autor
        vocabularios = {
            "Daniel Esteban Brola": ["amparo", "tutela", "constitucional", "derechos fundamentales"],
            "Carlos Pandiella": ["derecho administrativo", "procedimiento", "acto administrativo"],
            "Citlalli": ["género", "derechos humanos", "perspectiva crítica"],
            "Noelia Malvina Cofré": ["justicia", "equidad", "principios", "valores"]
        }
        
        return vocabularios.get(nombre, ["derecho", "ley", "norma", "principio"])
    
    def _extraer_innovaciones(self, perfil: Dict) -> List[str]:
        """Extrae innovaciones conceptuales del autor"""
        if perfil.get("creatividad", 0) > 0.6:
            return [
                "Nuevas interpretaciones de conceptos tradicionales",
                "Integración de perspectivas interdisciplinarias",
                "Propuestas metodológicas innovadoras"
            ]
        return ["Síntesis coherente de doctrina establecida"]
    
    def _extraer_influencias(self, perfil: Dict) -> List[str]:
        """Extrae influencias detectadas"""
        formalismo = perfil.get("formalismo", 0)
        empirismo = perfil.get("empirismo", 0)
        logos = perfil.get("logos", 0)
        
        influencias = []
        if formalismo > 0.6:
            influencias.append("Tradición jurídica formal")
        if empirismo > 0.6:
            influencias.append("Empirismo jurídico")
        if logos > 0.6:
            influencias.append("Lógica argumentativa rigurosa")
        
        return influencias if influencias else ["Síntesis de múltiples tradiciones"]
    
    def _clasificar_etapa_temporal(self, perfil: Dict) -> str:
        """Clasifica etapa temporal del pensamiento"""
        promedio_tecnicos = perfil.get("nivel_tecnico", 0)
        
        if promedio_tecnicos > 0.7:
            return "Pensamiento contemporáneo avanzado"
        elif promedio_tecnicos > 0.5:
            return "Pensamiento moderno consolidado"
        else:
            return "Pensamiento tradicional"
    
    def generar_html_pensamiento(self) -> str:
        """Genera HTML con interfaz de pensamiento multicapa"""
        autores = self.obtener_autores_disponibles()
        
        html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis Multi-Capa del Pensamiento</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .content {
            padding: 40px;
        }
        
        .selector {
            margin-bottom: 30px;
        }
        
        .selector label {
            font-weight: bold;
            margin-right: 15px;
            font-size: 1.1em;
        }
        
        .selector select {
            padding: 10px 15px;
            font-size: 1em;
            border: 2px solid #667eea;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .selector button {
            padding: 10px 25px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            margin-left: 10px;
            transition: background 0.3s;
        }
        
        .selector button:hover {
            background: #764ba2;
        }
        
        .capas-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .capa {
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            padding: 20px;
            border-radius: 8px;
        }
        
        .capa h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .capa-content {
            font-size: 0.95em;
            line-height: 1.6;
        }
        
        .metrica {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
        }
        
        .metrica:last-child {
            border-bottom: none;
        }
        
        .metrica-nombre {
            font-weight: 600;
        }
        
        .metrica-valor {
            color: #667eea;
            font-weight: bold;
        }
        
        .estadisticas {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        .estadisticas h2 {
            color: #1976d2;
            margin-bottom: 15px;
        }
        
        .stat-item {
            display: inline-block;
            margin-right: 30px;
            margin-bottom: 10px;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #666;
        }
        
        .stat-value {
            font-size: 1.5em;
            color: #1976d2;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Análisis Multi-Capa del Pensamiento</h1>
            <p>Exploración profunda de patrones cognitivos autorales</p>
        </div>
        
        <div class="content">
            <div class="selector">
                <label for="autor-select">Seleccionar Autor:</label>
                <select id="autor-select">
                    <option value="">-- Elige un autor --</option>
"""
        
        for autor in autores:
            html += f"<option value=\"{autor['nombre']}\">{autor['nombre']}</option>\n"
        
        html += """
                </select>
                <button onclick="analizarAutor()">Analizar</button>
            </div>
            
            <div id="resultado"></div>
        </div>
    </div>
    
    <script>
        function analizarAutor() {
            const select = document.getElementById('autor-select');
            const autor = select.value;
            
            if (!autor) {
                alert('Por favor selecciona un autor');
                return;
            }
            
            fetch(`/api/pensamiento/${encodeURIComponent(autor)}`)
                .then(r => r.json())
                .then(datos => mostrarAnalisis(datos))
                .catch(e => console.error('Error:', e));
        }
        
        function mostrarAnalisis(datos) {
            let html = `
                <div class="estadisticas">
                    <h2>${datos.autor}</h2>
                    <div class="stat-item">
                        <div class="stat-label">Palabras Analizadas</div>
                        <div class="stat-value">${datos.total_palabras.toLocaleString()}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Patrón Dominante</div>
                        <div class="stat-value">${datos.capa_cognitiva.patron_dominante}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Originalidad</div>
                        <div class="stat-value">${(datos.firma_intelectual.originalidad_score * 100).toFixed(1)}%</div>
                    </div>
                </div>
                
                <div class="capas-container">
                    ${generarCapa('🌊 Capa Semántica', datos.capa_semantica)}
                    ${generarCapa('🧠 Capa Cognitiva', datos.capa_cognitiva)}
                    ${generarCapa('📐 Capa Metodológica', datos.capa_metodologica)}
                    ${generarCapa('⏳ Capa Evolutiva', datos.capa_evolutiva)}
                    ${generarCapa('🌐 Capa Relacional', datos.capa_relacional)}
                </div>
            `;
            
            document.getElementById('resultado').innerHTML = html;
        }
        
        function generarCapa(titulo, datos) {
            let contenido = '<div class="capa-content">';
            
            for (const [key, value] of Object.entries(datos)) {
                if (typeof value === 'object') {
                    contenido += `<p><strong>${key}:</strong> ${JSON.stringify(value).substring(0, 100)}...</p>`;
                } else if (typeof value === 'number') {
                    contenido += `<div class="metrica"><span class="metrica-nombre">${key}</span><span class="metrica-valor">${(value * 100).toFixed(1)}%</span></div>`;
                } else {
                    contenido += `<p><strong>${key}:</strong> ${value}</p>`;
                }
            }
            
            contenido += '</div>';
            return `<div class="capa"><h3>${titulo}</h3>${contenido}</div>`;
        }
    </script>
</body>
</html>
        """
        
        return html


# Instancia global
integrador = IntegradorPensamientoFlask()
