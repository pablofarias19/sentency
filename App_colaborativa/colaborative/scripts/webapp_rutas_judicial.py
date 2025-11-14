#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 RUTAS WEBAPP PARA SISTEMA JUDICIAL
======================================

Rutas Flask para el sistema judicial que REEMPLAZAN las rutas de autores.

INTEGRACIÓN con end2end_webapp.py:
- Importar este módulo
- Registrar las rutas en la app Flask
- Reemplaza /autores, /pensamiento, /comparar por rutas judiciales

RUTAS:
- / → Búsqueda general (RAG adaptado a sentencias)
- /jueces → Listado de jueces
- /juez/<nombre> → Perfil completo del juez
- /lineas/<juez> → Líneas jurisprudenciales
- /red/<juez> → Red de influencias
- /prediccion/<juez> → Análisis predictivo
- /informes → Generador de informes
- /preguntas/<juez> → Sistema de 140 preguntas
- /cognitivo/<juez> → Análisis cognitivo (ANALYSER)

AUTOR: Sistema Judicial Argentina
FECHA: 12 NOV 2025
"""

from flask import render_template_string, request, jsonify, send_file
from pathlib import Path
import json
import sqlite3
from datetime import datetime

# Importar adaptador
from analyser_judicial_adapter import AnalyserJudicialAdapter, BibliotecaJudicial

# Importar sistema de informes
from generador_informes_judicial import GeneradorInformesJudicial

# Importar sistema de preguntas
from motor_respuestas_judiciales import MotorRespuestasJudiciales

# Importar analizadores
from analizador_lineas_jurisprudenciales import AnalizadorLineasJurisprudenciales
from analizador_redes_influencia import AnalizadorRedesInfluencia
from motor_predictivo_judicial import MotorPredictivoJudicial

# Importar configuración centralizada
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DATABASE_PATH as DB_JUDICIAL, BASE_DIR, BASES_RAG_DIR

# Instancias globales
biblioteca_judicial = None
generador_informes = None
motor_preguntas = None


def init_sistema_judicial():
    """Inicializa el sistema judicial"""
    global biblioteca_judicial, generador_informes, motor_preguntas

    biblioteca_judicial = BibliotecaJudicial()
    generador_informes = GeneradorInformesJudicial()
    motor_preguntas = MotorRespuestasJudiciales()

    print("✅ Sistema Judicial inicializado")


def registrar_rutas_judicial(app):
    """
    Registra las rutas judiciales en la app Flask

    Uso en end2end_webapp.py:
        from webapp_rutas_judicial import registrar_rutas_judicial
        registrar_rutas_judicial(app)
    """

    # =========================================================================
    # RUTA PRINCIPAL: BÚSQUEDA DE SENTENCIAS
    # =========================================================================

    @app.route('/judicial')
    @app.route('/judicial/buscar')
    def judicial_buscar():
        """Búsqueda de sentencias con RAG"""
        return render_template_string(TEMPLATE_BUSCAR_SENTENCIAS)

    @app.route('/judicial/buscar/query', methods=['POST'])
    def judicial_buscar_query():
        """API: Búsqueda semántica de sentencias"""
        data = request.get_json()
        query = data.get('query', '')
        fuero = data.get('fuero', None)
        juez = data.get('juez', None)

        # TODO: Implementar búsqueda RAG adaptada
        # Por ahora devolver placeholder
        resultados = {
            'query': query,
            'resultados': [],
            'mensaje': 'Búsqueda RAG en desarrollo'
        }

        return jsonify(resultados)

    # =========================================================================
    # LISTADO DE JUECES
    # =========================================================================

    @app.route('/jueces')
    def lista_jueces():
        """Listado de todos los jueces"""
        try:
            jueces = biblioteca_judicial.listar_jueces()

            return render_template_string(
                TEMPLATE_LISTA_JUECES,
                jueces=jueces,
                total=len(jueces)
            )
        except Exception as e:
            return f"Error: {e}", 500

    # =========================================================================
    # PERFIL COMPLETO DEL JUEZ
    # =========================================================================

    @app.route('/juez/<nombre>')
    def perfil_juez(nombre):
        """Perfil completo del juez"""
        try:
            perfil = biblioteca_judicial.obtener_perfil_completo(nombre)

            if not perfil:
                return f"Juez '{nombre}' no encontrado", 404

            return render_template_string(
                TEMPLATE_PERFIL_JUEZ,
                juez=nombre,
                perfil=perfil
            )
        except Exception as e:
            return f"Error: {e}", 500

    # =========================================================================
    # ANÁLISIS COGNITIVO DEL JUEZ
    # =========================================================================

    @app.route('/cognitivo/<juez>')
    def analisis_cognitivo(juez):
        """Análisis cognitivo completo del juez (ANALYSER)"""
        try:
            perfil = biblioteca_judicial.obtener_perfil_completo(juez)

            if not perfil:
                return f"Juez '{juez}' no encontrado", 404

            # Extraer métricas cognitivas
            cognitivo = {
                'razonamiento': perfil.get('razonamiento_dominante'),
                'modalidad': perfil.get('modalidad_epistemica'),
                'ethos': perfil.get('uso_ethos', 0),
                'pathos': perfil.get('uso_pathos', 0),
                'logos': perfil.get('uso_logos', 0),
                'estilo': perfil.get('estilo_literario'),
                'legislacion': perfil.get('densidad_citas_legislacion', 0),
                'jurisprudencia': perfil.get('densidad_citas_jurisprudencia', 0),
                'doctrina': perfil.get('densidad_citas_doctrina', 0)
            }

            return render_template_string(
                TEMPLATE_COGNITIVO,
                juez=juez,
                cognitivo=cognitivo,
                perfil=perfil
            )
        except Exception as e:
            return f"Error: {e}", 500

    # =========================================================================
    # LÍNEAS JURISPRUDENCIALES
    # =========================================================================

    @app.route('/lineas/<juez>')
    def lineas_juez(juez):
        """Líneas jurisprudenciales del juez"""
        try:
            conn = sqlite3.connect(DB_JUDICIAL)
            cursor = conn.cursor()

            cursor.execute("""
            SELECT tema, cantidad_sentencias, consistencia_score,
                   criterio_dominante, confianza
            FROM lineas_jurisprudenciales
            WHERE juez = ?
            ORDER BY cantidad_sentencias DESC
            """, (juez,))

            lineas = []
            for row in cursor.fetchall():
                lineas.append({
                    'tema': row[0],
                    'cantidad': row[1],
                    'consistencia': row[2],
                    'criterio': row[3],
                    'confianza': row[4]
                })

            conn.close()

            return render_template_string(
                TEMPLATE_LINEAS,
                juez=juez,
                lineas=lineas
            )
        except Exception as e:
            return f"Error: {e}", 500

    # =========================================================================
    # RED DE INFLUENCIAS
    # =========================================================================

    @app.route('/red/<juez>')
    def red_influencias(juez):
        """Red de influencias del juez"""
        try:
            conn = sqlite3.connect(DB_JUDICIAL)
            cursor = conn.cursor()

            # CSJN
            cursor.execute("""
            SELECT juez_destino, intensidad, cantidad_citas
            FROM redes_influencia_judicial
            WHERE juez_origen = ? AND tipo_destino = 'csjn'
            ORDER BY cantidad_citas DESC
            LIMIT 10
            """, (juez,))
            csjn = [{'destino': r[0], 'intensidad': r[1], 'citas': r[2]} for r in cursor.fetchall()]

            # Tribunales
            cursor.execute("""
            SELECT juez_destino, intensidad, cantidad_citas
            FROM redes_influencia_judicial
            WHERE juez_origen = ? AND tipo_destino = 'tribunal_superior'
            ORDER BY cantidad_citas DESC
            LIMIT 10
            """, (juez,))
            tribunales = [{'destino': r[0], 'intensidad': r[1], 'citas': r[2]} for r in cursor.fetchall()]

            # Autores
            cursor.execute("""
            SELECT juez_destino, intensidad, cantidad_citas
            FROM redes_influencia_judicial
            WHERE juez_origen = ? AND tipo_destino = 'autor_doctrinal'
            ORDER BY cantidad_citas DESC
            LIMIT 15
            """, (juez,))
            autores = [{'destino': r[0], 'intensidad': r[1], 'citas': r[2]} for r in cursor.fetchall()]

            conn.close()

            return render_template_string(
                TEMPLATE_RED,
                juez=juez,
                csjn=csjn,
                tribunales=tribunales,
                autores=autores
            )
        except Exception as e:
            return f"Error: {e}", 500

    # =========================================================================
    # ANÁLISIS PREDICTIVO
    # =========================================================================

    @app.route('/prediccion/<juez>')
    def prediccion_juez(juez):
        """Análisis predictivo del juez"""
        try:
            conn = sqlite3.connect(DB_JUDICIAL)
            cursor = conn.cursor()

            cursor.execute("""
            SELECT factor, peso, confianza
            FROM factores_predictivos
            WHERE juez = ?
            ORDER BY peso DESC
            LIMIT 15
            """, (juez,))

            factores = []
            for row in cursor.fetchall():
                factores.append({
                    'factor': row[0],
                    'peso': row[1],
                    'confianza': row[2]
                })

            conn.close()

            return render_template_string(
                TEMPLATE_PREDICCION,
                juez=juez,
                factores=factores
            )
        except Exception as e:
            return f"Error: {e}", 500

    # =========================================================================
    # GENERADOR DE INFORMES
    # =========================================================================

    @app.route('/informes')
    def generador_informes_view():
        """Interfaz para generar informes"""
        return render_template_string(TEMPLATE_INFORMES)

    @app.route('/informes/generar', methods=['POST'])
    def generar_informe():
        """API: Genera informe"""
        data = request.get_json()
        juez = data.get('juez')
        tipo = data.get('tipo', 'completo')
        formato = data.get('formato', 'txt')

        try:
            if tipo == 'completo':
                ruta = generador_informes.generar_informe_completo(juez, formato)
            # TODO: Otros tipos de informes

            return jsonify({'success': True, 'ruta': ruta})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    # =========================================================================
    # SISTEMA DE PREGUNTAS
    # =========================================================================

    @app.route('/preguntas/<juez>')
    def preguntas_juez(juez):
        """Sistema de 140 preguntas del juez"""
        return render_template_string(
            TEMPLATE_PREGUNTAS,
            juez=juez
        )

    @app.route('/preguntas/<juez>/responder', methods=['POST'])
    def responder_pregunta(juez):
        """API: Responde pregunta específica"""
        data = request.get_json()
        pregunta_id = data.get('pregunta_id')

        try:
            respuesta = motor_preguntas.responder_pregunta(juez, pregunta_id)
            return jsonify(respuesta)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/preguntas/<juez>/todas')
    def todas_preguntas(juez):
        """API: Responde todas las 140 preguntas"""
        try:
            respuestas = motor_preguntas.responder_todas(juez)
            return jsonify(respuestas)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    print("✅ Rutas judiciales registradas")


# =============================================================================
# TEMPLATES HTML
# =============================================================================

TEMPLATE_LISTA_JUECES = """
<!DOCTYPE html>
<html>
<head>
    <title>Jueces - Sistema Judicial</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        .stats { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { background: #34495e; color: white; padding: 12px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f8f9fa; }
        a { color: #3498db; text-decoration: none; font-weight: bold; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚖️ Sistema Judicial - Listado de Jueces</h1>

        <div class="stats">
            <strong>Total de jueces analizados:</strong> {{ total }}
        </div>

        <table>
            <tr>
                <th>Juez</th>
                <th>Tipo</th>
                <th>Fuero</th>
                <th>Jurisdicción</th>
                <th>Sentencias</th>
                <th>Confianza</th>
                <th>Acciones</th>
            </tr>
            {% for juez in jueces %}
            <tr>
                <td><a href="/juez/{{ juez.nombre }}">{{ juez.nombre }}</a></td>
                <td>{{ juez.tipo }}</td>
                <td>{{ juez.fuero }}</td>
                <td>{{ juez.jurisdiccion }}</td>
                <td>{{ juez.sentencias }}</td>
                <td>{{ "%.2f"|format(juez.confianza) }}</td>
                <td>
                    <a href="/cognitivo/{{ juez.nombre }}">Cognitivo</a> |
                    <a href="/lineas/{{ juez.nombre }}">Líneas</a> |
                    <a href="/red/{{ juez.nombre }}">Red</a>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

TEMPLATE_PERFIL_JUEZ = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ juez }} - Perfil Judicial</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 30px; }
        .metric { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .metric strong { color: #2c3e50; }
        .score { display: inline-block; background: #3498db; color: white; padding: 5px 10px; border-radius: 3px; margin-left: 10px; }
        .nav { margin-bottom: 20px; }
        .nav a { background: #3498db; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin-right: 10px; display: inline-block; }
        .nav a:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/jueces">← Volver</a>
            <a href="/cognitivo/{{ juez }}">Análisis Cognitivo</a>
            <a href="/lineas/{{ juez }}">Líneas Jurisprudenciales</a>
            <a href="/red/{{ juez }}">Red de Influencias</a>
            <a href="/prediccion/{{ juez }}">Análisis Predictivo</a>
            <a href="/preguntas/{{ juez }}">140 Preguntas</a>
        </div>

        <h1>⚖️ {{ juez }}</h1>

        <h2>📋 Información Básica</h2>
        <div class="metric"><strong>Tipo:</strong> {{ perfil.tipo_entidad }}</div>
        <div class="metric"><strong>Fuero:</strong> {{ perfil.fuero or 'N/D' }}</div>
        <div class="metric"><strong>Jurisdicción:</strong> {{ perfil.jurisdiccion or 'N/D' }}</div>
        <div class="metric"><strong>Tribunal:</strong> {{ perfil.tribunal or 'N/D' }}</div>
        <div class="metric"><strong>Sentencias analizadas:</strong> {{ perfil.total_sentencias or 0 }}</div>

        <h2>⚖️ Perfil Judicial</h2>
        <div class="metric">
            <strong>Activismo:</strong>
            <span class="score">{{ "%.2f"|format(perfil.tendencia_activismo or 0) }}</span>
        </div>
        <div class="metric">
            <strong>Formalismo:</strong>
            <span class="score">{{ "%.2f"|format(perfil.nivel_formalismo or 0) }}</span>
        </div>
        <div class="metric"><strong>Interpretación dominante:</strong> {{ perfil.interpretacion_dominante or 'N/D' }}</div>

        <h2>🛡️ Protección de Derechos</h2>
        <div class="metric"><strong>Trabajo:</strong> <span class="score">{{ "%.2f"|format(perfil.proteccion_trabajo or 0) }}</span></div>
        <div class="metric"><strong>Igualdad:</strong> <span class="score">{{ "%.2f"|format(perfil.proteccion_igualdad or 0) }}</span></div>
        <div class="metric"><strong>Consumidor:</strong> <span class="score">{{ "%.2f"|format(perfil.proteccion_consumidor or 0) }}</span></div>

        <h2>📊 Sesgos y Tendencias</h2>
        <div class="metric"><strong>Pro-trabajador:</strong> <span class="score">{{ "%.2f"|format(perfil.sesgo_pro_trabajador or 0) }}</span></div>
        <div class="metric"><strong>Garantista:</strong> <span class="score">{{ "%.2f"|format(perfil.sesgo_garantista or 0) }}</span></div>
        <div class="metric"><strong>Pro-consumidor:</strong> <span class="score">{{ "%.2f"|format(perfil.sesgo_pro_consumidor or 0) }}</span></div>
    </div>
</body>
</html>
"""

TEMPLATE_COGNITIVO = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ juez }} - Análisis Cognitivo</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1, h2 { color: #2c3e50; }
        .metric { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .score { display: inline-block; background: #9b59b6; color: white; padding: 5px 10px; border-radius: 3px; margin-left: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Análisis Cognitivo: {{ juez }}</h1>

        <h2>💭 Razonamiento</h2>
        <div class="metric"><strong>Tipo dominante:</strong> {{ cognitivo.razonamiento or 'N/D' }}</div>

        <h2>🎭 Retórica</h2>
        <div class="metric"><strong>Ethos (autoridad):</strong> <span class="score">{{ "%.2f"|format(cognitivo.ethos) }}</span></div>
        <div class="metric"><strong>Pathos (emoción):</strong> <span class="score">{{ "%.2f"|format(cognitivo.pathos) }}</span></div>
        <div class="metric"><strong>Logos (lógica):</strong> <span class="score">{{ "%.2f"|format(cognitivo.logos) }}</span></div>

        <h2>📚 Fuentes</h2>
        <div class="metric"><strong>Legislación:</strong> <span class="score">{{ "%.2f"|format(cognitivo.legislacion) }}</span></div>
        <div class="metric"><strong>Jurisprudencia:</strong> <span class="score">{{ "%.2f"|format(cognitivo.jurisprudencia) }}</span></div>
        <div class="metric"><strong>Doctrina:</strong> <span class="score">{{ "%.2f"|format(cognitivo.doctrina) }}</span></div>

        <h2>✍️ Estilo</h2>
        <div class="metric"><strong>Estilo literario:</strong> {{ cognitivo.estilo or 'N/D' }}</div>
    </div>
</body>
</html>
"""

TEMPLATE_LINEAS = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ juez }} - Líneas Jurisprudenciales</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .linea { background: #ecf0f1; padding: 20px; margin: 15px 0; border-radius: 5px; border-left: 5px solid #3498db; }
        .linea h3 { margin-top: 0; color: #2c3e50; }
        .badge { background: #3498db; color: white; padding: 3px 8px; border-radius: 3px; font-size: 0.9em; margin-right: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📜 Líneas Jurisprudenciales: {{ juez }}</h1>

        {% for linea in lineas %}
        <div class="linea">
            <h3>{{ linea.tema }}</h3>
            <p>
                <span class="badge">{{ linea.cantidad }} sentencias</span>
                <span class="badge">Consistencia: {{ "%.2f"|format(linea.consistencia) }}</span>
                <span class="badge">Confianza: {{ "%.2f"|format(linea.confianza) }}</span>
            </p>
            <p><strong>Criterio dominante:</strong> {{ linea.criterio }}</p>
        </div>
        {% endfor %}

        {% if not lineas %}
        <p>No hay líneas jurisprudenciales consolidadas para este juez.</p>
        {% endif %}
    </div>
</body>
</html>
"""

TEMPLATE_RED = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ juez }} - Red de Influencias</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; }
        .cita { background: #ecf0f1; padding: 10px; margin: 5px 0; border-radius: 3px; }
        .intensidad { float: right; background: #3498db; color: white; padding: 3px 8px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 Red de Influencias: {{ juez }}</h1>

        <h2>🏛️ CSJN</h2>
        {% for c in csjn %}
        <div class="cita">
            <span class="intensidad">{{ c.citas }} citas</span>
            <strong>{{ c.destino }}</strong>
        </div>
        {% endfor %}

        <h2>⚖️ Tribunales Superiores</h2>
        {% for t in tribunales %}
        <div class="cita">
            <span class="intensidad">{{ t.citas }} citas</span>
            <strong>{{ t.destino }}</strong>
        </div>
        {% endfor %}

        <h2>📚 Autores Doctrinales</h2>
        {% for a in autores %}
        <div class="cita">
            <span class="intensidad">{{ a.citas }} citas</span>
            <strong>{{ a.destino }}</strong>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

TEMPLATE_PREDICCION = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ juez }} - Análisis Predictivo</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .factor { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .peso { float: right; background: #e74c3c; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔮 Análisis Predictivo: {{ juez }}</h1>

        <h2>Top Factores Determinantes</h2>
        {% for f in factores %}
        <div class="factor">
            <span class="peso">{{ "%.3f"|format(f.peso) }}</span>
            <strong>{{ f.factor }}</strong>
        </div>
        {% endfor %}

        {% if not factores %}
        <p>Modelo predictivo no disponible (requiere mínimo 5 sentencias).</p>
        {% endif %}
    </div>
</body>
</html>
"""

TEMPLATE_PREGUNTAS = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ juez }} - 140 Preguntas</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        button { background: #3498db; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #2980b9; }
        #respuestas { margin-top: 20px; }
        .pregunta { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>❓ Sistema de 140 Preguntas: {{ juez }}</h1>

        <button onclick="responderTodas()">Responder las 140 Preguntas</button>

        <div id="respuestas"></div>
    </div>

    <script>
        function responderTodas() {
            document.getElementById('respuestas').innerHTML = '<p>Procesando 140 preguntas...</p>';

            fetch('/preguntas/{{ juez }}/todas')
                .then(r => r.json())
                .then(data => {
                    let html = '<h2>Respuestas (' + data.respuestas_disponibles + '/' + data.total_preguntas + ')</h2>';

                    for (let cat in data.respuestas) {
                        html += '<h3>Categoría ' + cat + '</h3>';

                        data.respuestas[cat].forEach(r => {
                            html += '<div class="pregunta">';
                            html += '<strong>' + r.pregunta_id + '. ' + r.pregunta + '</strong><br>';
                            html += 'R: ' + r.respuesta;
                            html += '</div>';
                        });
                    }

                    document.getElementById('respuestas').innerHTML = html;
                });
        }
    </script>
</body>
</html>
"""

TEMPLATE_INFORMES = """
<!DOCTYPE html>
<html>
<head>
    <title>Generador de Informes Judiciales</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        input, select { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #27ae60; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background: #229954; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Generador de Informes Judiciales</h1>

        <label>Nombre del Juez:</label>
        <input type="text" id="juez" placeholder="Dr. Juan Pérez">

        <label>Tipo de Informe:</label>
        <select id="tipo">
            <option value="completo">Informe Completo</option>
            <option value="linea">Línea Jurisprudencial</option>
            <option value="red">Red de Influencias</option>
            <option value="predictivo">Análisis Predictivo</option>
        </select>

        <label>Formato:</label>
        <select id="formato">
            <option value="txt">Texto (.txt)</option>
            <option value="json">JSON (.json)</option>
            <option value="md">Markdown (.md)</option>
        </select>

        <button onclick="generar()">Generar Informe</button>

        <div id="resultado" style="margin-top: 20px;"></div>
    </div>

    <script>
        function generar() {
            const juez = document.getElementById('juez').value;
            const tipo = document.getElementById('tipo').value;
            const formato = document.getElementById('formato').value;

            document.getElementById('resultado').innerHTML = '<p>Generando informe...</p>';

            fetch('/informes/generar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({juez, tipo, formato})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('resultado').innerHTML =
                        '<p style="color: green;">✓ Informe generado: ' + data.ruta + '</p>';
                } else {
                    document.getElementById('resultado').innerHTML =
                        '<p style="color: red;">✗ Error: ' + data.error + '</p>';
                }
            });
        }
    </script>
</body>
</html>
"""

TEMPLATE_BUSCAR_SENTENCIAS = """
<!DOCTYPE html>
<html>
<head>
    <title>Búsqueda de Sentencias - Sistema Judicial</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #2c3e50; }
        input, select { padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Búsqueda de Sentencias (RAG)</h1>
        <p>Búsqueda semántica en sentencias judiciales argentinas</p>

        <input type="text" id="query" placeholder="Ej: despido discriminatorio por embarazo" style="width: 70%;">
        <button onclick="buscar()">Buscar</button>

        <div id="resultados" style="margin-top: 20px;"></div>
    </div>

    <script>
        function buscar() {
            const query = document.getElementById('query').value;
            document.getElementById('resultados').innerHTML = '<p>Buscando...</p>';

            fetch('/judicial/buscar/query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query})
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('resultados').innerHTML =
                    '<p>' + data.mensaje + '</p>';
            });
        }
    </script>
</body>
</html>
"""


if __name__ == "__main__":
    # Para testing standalone
    from flask import Flask
    app = Flask(__name__)
    app.secret_key = "test"

    init_sistema_judicial()
    registrar_rutas_judicial(app)

    print("🚀 Servidor de prueba en http://localhost:5001")
    app.run(debug=True, port=5001)
