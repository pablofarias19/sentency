#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 SISTEMA DE REFERENCIAS DE AUTORES INTERACTIVO
==============================================

PROPORCIONA:
- Listado completo de autores con sus obras
- Búsquedas avanzadas por metodología, razonamiento, creatividad
- Perfiles detallados con análisis cognitivo completo
- Vinculación con documentos ingestados
- Comparaciones entre autores
- Interfaz intuitiva y navegable

INTEGRA CON:
- Sistema de ingesta de documentos
- Perfiles autorales v2.0
- Comparador de mentes
- Orchestrador maestro integrado

AUTOR: Sistema Cognitivo v6.0 - Referencias Autorales
FECHA: 9 NOV 2025
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from flask import Flask, render_template, request, jsonify, redirect, url_for
import glob

class SistemaReferenciasAutores:
    """Sistema completo de referencias de autores con análisis cognitivo"""
    
    def __init__(self):
        self.version = "v1.0_referencias_autores"
        
        # Usar rutas absolutas basadas en el directorio del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
        
        self.db_path = os.path.join(base_dir, "colaborative", "bases_rag", "cognitiva", "pensamiento_integrado_v2.db")
        self.db_original = os.path.join(base_dir, "colaborative", "bases_rag", "cognitiva", "metadatos.db")
        
        # Configurar Flask
        self.app = Flask(__name__, 
                        template_folder='../templates',
                        static_folder='../static')
        
        self._configurar_rutas()
        print(f"📚 Sistema de Referencias de Autores {self.version} iniciado")
    
    def _configurar_rutas(self):
        """Configura todas las rutas de la aplicación"""
        
        @self.app.route('/autores')
        def lista_autores():
            """Página principal con listado de autores"""
            autores = self.obtener_todos_los_autores()
            estadisticas = self.calcular_estadisticas_generales()
            return render_template('autores_referencias.html', 
                                 autores=autores, 
                                 estadisticas=estadisticas,
                                 filtros=self.obtener_opciones_filtros())
        
        @self.app.route('/autor/<nombre>')
        def perfil_autor(nombre):
            """Perfil detallado de un autor específico"""
            perfil = self.obtener_perfil_completo_autor(nombre)
            if not perfil:
                return "Autor no encontrado", 404
            
            return render_template('perfil_autor_detallado.html', 
                                 autor=perfil,
                                 similares=self.obtener_autores_similares(nombre))
        
        @self.app.route('/api/autores/buscar')
        def buscar_autores():
            """API para búsqueda avanzada de autores"""
            filtros = request.args.to_dict()
            resultados = self.buscar_autores_avanzado(filtros)
            return jsonify(resultados)
        
        @self.app.route('/api/autores/comparar')
        def comparar_autores_api():
            """API para comparar dos autores"""
            autor_a = request.args.get('autor_a')
            autor_b = request.args.get('autor_b')
            
            if not autor_a or not autor_b:
                return jsonify({"error": "Se requieren ambos autores"}), 400
            
            comparacion = self.comparar_autores_detallado(autor_a, autor_b)
            return jsonify(comparacion)
        
        @self.app.route('/comparacion')
        def pagina_comparacion():
            """Página para comparar autores"""
            autores_disponibles = [a['nombre'] for a in self.obtener_todos_los_autores()]
            return render_template('comparacion_autores.html', 
                                 autores=autores_disponibles)
    
    def obtener_todos_los_autores(self) -> List[Dict[str, Any]]:
        """Obtiene listado completo de autores con información básica"""
        
        autores = []
        autores_nombres_set = set()  # Para evitar duplicados
        
        # Primero obtener de la base de datos original (metadatos.db con la información real)
        if os.path.exists(self.db_original):
            autores_db_original = self._obtener_autores_db_original()
            autores.extend(autores_db_original)
            autores_nombres_set.update([a['nombre'] for a in autores_db_original])
        
        # Luego, complementar con base de datos integrada (v2.0) si hay autores que no están
        if os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    SELECT autor, razonamiento_dominante, modalidad_dominante, estilo_dominante,
                           nivel_abstraccion, creatividad, empirismo, sistematizacion, timestamp
                    FROM perfiles_integrados_v2
                    ORDER BY timestamp DESC
                ''')
                
                for row in cursor.fetchall():
                    nombre = row[0]
                    # Solo agregar si no está ya en la lista
                    if nombre not in autores_nombres_set:
                        obras = self.obtener_obras_autor(nombre)
                        
                        autores.append({
                            "nombre": nombre,
                            "razonamiento_dominante": row[1].title(),
                            "modalidad_dominante": row[2].title(),
                            "estilo_dominante": row[3].title(),
                            "nivel_abstraccion": round(row[4], 2),
                            "creatividad": round(row[5], 2),
                            "empirismo": round(row[6], 2),
                            "sistematizacion": round(row[7], 2),
                            "timestamp": row[8],
                            "num_obras": len(obras),
                            "obras": obras[:3]  # Primeras 3 obras
                        })
                        autores_nombres_set.add(nombre)
                
            except sqlite3.OperationalError:
                pass
            finally:
                conn.close()
        
        return autores
    
    def _obtener_autores_db_original(self) -> List[Dict[str, Any]]:
        """Obtiene autores de la base de datos original como fallback"""
        
        conn = sqlite3.connect(self.db_original)
        cursor = conn.cursor()
        autores = []
        
        try:
            cursor.execute("SELECT DISTINCT autor FROM perfiles_cognitivos WHERE autor IS NOT NULL")
            nombres = cursor.fetchall()
            
            for (nombre,) in nombres:
                # Obtener último perfil del autor
                cursor.execute('''
                    SELECT creatividad, formalismo, empirismo, nivel_abstraccion, fecha_registro
                    FROM perfiles_cognitivos 
                    WHERE autor = ? 
                    ORDER BY fecha_registro DESC LIMIT 1
                ''', (nombre,))
                
                perfil = cursor.fetchone()
                obras = self.obtener_obras_autor(nombre)
                
                if perfil:
                    autores.append({
                        "nombre": nombre,
                        "razonamiento_dominante": "Clásico",
                        "modalidad_dominante": "Dialéctico",
                        "estilo_dominante": "Técnico-Jurídico",
                        "nivel_abstraccion": round(perfil[3], 2),
                        "creatividad": round(perfil[0], 2),
                        "empirismo": round(perfil[2], 2),
                        "sistematizacion": round(perfil[1], 2),
                        "timestamp": perfil[4] if perfil[4] else datetime.now().isoformat(),
                        "num_obras": len(obras),
                        "obras": obras[:3]
                    })
        
        except sqlite3.OperationalError as e:
            print(f"⚠️ Error accediendo DB original: {e}")
        finally:
            conn.close()
        
        return autores
    
    def obtener_obras_autor(self, autor: str) -> List[Dict[str, str]]:
        """Obtiene las obras/documentos asociados a un autor"""
        
        obras = []
        
        # Usar rutas absolutas
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
        
        # Buscar en directorio de PDFs
        pdf_dirs = [
            os.path.join(base_dir, "colaborative", "data", "pdfs", "general"),
            os.path.join(base_dir, "colaborative", "data", "pdfs", "civil")
        ]
        
        for pdf_dir in pdf_dirs:
            if os.path.exists(pdf_dir):
                for archivo in glob.glob(f"{pdf_dir}/*.pdf"):
                    nombre_archivo = os.path.basename(archivo)
                    
                    # Heurística simple: si el nombre del autor aparece en el archivo
                    if autor.lower().replace(" ", "_") in nombre_archivo.lower():
                        obras.append({
                            "titulo": nombre_archivo.replace(".pdf", "").replace("_", " ").title(),
                            "archivo": nombre_archivo,
                            "ruta": archivo,
                            "tipo": "PDF"
                        })
        
        # No intentar buscar en chunks para evitar errores
        # (la tabla probablemente no existe)
        
        return obras
    
    def _buscar_obras_en_chunks(self, autor: str) -> List[Dict[str, str]]:
        """Busca obras en la base de chunks/fragmentos - DEPRECATED"""
        return []
    
    def obtener_perfil_completo_autor(self, nombre: str) -> Optional[Dict[str, Any]]:
        """Obtiene perfil cognitivo completo de un autor"""
        
        # Primero intentar base de datos original (metadatos.db) - la fuente de verdad
        if os.path.exists(self.db_original):
            perfil = self._obtener_perfil_original(nombre)
            if perfil:
                return perfil
        
        # Fallback a base de datos v2.0 integrada si no está en original
        if os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    SELECT perfil_completo, vector_cognitivo
                    FROM perfiles_integrados_v2 
                    WHERE autor = ?
                ''', (nombre,))
                
                resultado = cursor.fetchone()
                if resultado:
                    perfil_json, vector_json = resultado
                    perfil = json.loads(perfil_json)
                    vector = json.loads(vector_json)
                    
                    # Enriquecer con información adicional
                    perfil['obras'] = self.obtener_obras_autor(nombre)
                    perfil['vector_cognitivo'] = vector
                    perfil['metodologia_explicacion'] = self._generar_explicacion_metodologia(perfil)
                    perfil['creatividad_valoracion'] = self._generar_valoracion_creatividad(perfil)
                    perfil['formalismo_analisis'] = self._generar_analisis_formalismo(perfil)
                    perfil['logica_intelectual'] = self._generar_analisis_logica_intelectual(perfil)
                    
                    conn.close()
                    return perfil
                    
            except (sqlite3.OperationalError, json.JSONDecodeError) as e:
                pass
            finally:
                conn.close()
        
        return None
    
    def _obtener_perfil_original(self, nombre: str) -> Optional[Dict[str, Any]]:
        """Obtiene perfil de la base de datos original (metadatos.db)"""
        
        print(f"[DEBUG] _obtener_perfil_original llamada para: {nombre}")
        
        try:
            print(f"[DEBUG] Conectando a: {self.db_original}")
            conn = sqlite3.connect(self.db_original)
            cursor = conn.cursor()
            print(f"[DEBUG] Conexión exitosa")
            
            # Obtener el registro más reciente del autor
            cursor.execute('''
                SELECT 
                    creatividad, formalismo, empirismo, nivel_abstraccion, dogmatismo, 
                    uso_jurisprudencia, modalidad_epistemica, estructura_silogistica, 
                    razonamiento_dominante, razonamiento_top3, fecha_registro, archivo,
                    ethos, pathos, logos, tipo_pensamiento, total_palabras, tono
                FROM perfiles_cognitivos 
                WHERE autor = ? 
                ORDER BY fecha_registro DESC LIMIT 1
            ''', (nombre,))
            
            resultado = cursor.fetchone()
            print(f"[DEBUG] Query result: {resultado is not None}")
            
            if not resultado:
                print(f"[DEBUG] No result, returning None")
                return None
            
            # Parsear resultado
            (creatividad, formalismo, empirismo, nivel_abstraccion, dogmatismo,
             uso_jurisprudencia, modalidad_epistemica, estructura_silogistica,
             razonamiento_dominante, razonamiento_top3, fecha_registro, archivo,
             ethos, pathos, logos, tipo_pensamiento, total_palabras, tono) = resultado
            
            print(f"[DEBUG] Unpacking successful")
            
            # Construir perfil completo
            perfil = {
                "nombre": nombre,
                "tipo_pensamiento": tipo_pensamiento or "No especificado",
                "fecha_registro": fecha_registro,
                "archivo": archivo,
                "total_palabras": total_palabras or 0,
                "meta": {
                    "confidencia": "Alta",
                    "fuente": "Análisis Cognitivo Integrado",
                    "version": "2.1"
                },
                "cognicion": {
                    "creatividad": round(creatividad, 3) if creatividad else 0,
                    "formalismo": round(formalismo, 3) if formalismo else 0,
                    "empirismo": round(empirismo, 3) if empirismo else 0,
                    "nivel_abstraccion": round(nivel_abstraccion, 3) if nivel_abstraccion else 0,
                    "dogmatismo": round(dogmatismo, 3) if dogmatismo else 0,
                    "uso_jurisprudencia": round(uso_jurisprudencia, 3) if uso_jurisprudencia else 0,
                    "modalidad_epistemica": modalidad_epistemica or "Desconocida",
                    "razonamiento_dominante": razonamiento_dominante or "No especificado"
                },
                "retorica": {
                    "ethos": round(ethos, 3) if ethos else 0,
                    "pathos": round(pathos, 3) if pathos else 0,
                    "logos": round(logos, 3) if logos else 0
                },
                "obras": self.obtener_obras_autor(nombre)
            }
            
            # Parsear estructura silogística si es JSON
            if estructura_silogistica:
                try:
                    if isinstance(estructura_silogistica, str):
                        estructura_silogistica = json.loads(estructura_silogistica)
                    perfil["cognicion"]["estructura_silogistica"] = estructura_silogistica
                except:
                    perfil["cognicion"]["estructura_silogistica"] = estructura_silogistica
            
            # Parsear razonamiento top3
            if razonamiento_top3:
                try:
                    if isinstance(razonamiento_top3, str):
                        razonamiento_top3 = json.loads(razonamiento_top3)
                    perfil["cognicion"]["razonamiento_top3"] = razonamiento_top3
                except:
                    perfil["cognicion"]["razonamiento_top3"] = razonamiento_top3
            
            conn.close()
            print(f"[DEBUG] Perfil construido exitosamente")
            return perfil
            
        except Exception as e:
            print(f"[ERROR] Error obteniendo perfil de {nombre}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _generar_explicacion_metodologia(self, perfil: Dict[str, Any]) -> str:
        """Genera explicación detallada de la metodología del autor"""
        
        razonamiento = perfil.get('cognicion', {}).get('razonamiento_formal', {})
        modalidad = perfil.get('cognicion', {}).get('modalidad_epistemica', {})
        
        # Encontrar patrones dominantes
        razon_top = max(razonamiento.items(), key=lambda x: x[1]) if razonamiento else ("desconocido", 0)
        modal_top = max(modalidad.items(), key=lambda x: x[1]) if modalidad else ("desconocido", 0)
        
        explicacion = f"""
        **METODOLOGÍA JURÍDICA APLICADA:**
        
        El autor demuestra un **razonamiento predominantemente {razon_top[0].replace('_', ' ')}** 
        (intensidad: {razon_top[1]:.2f}), lo que indica que construye sus argumentos mediante 
        {'deducciones lógicas rigurosas desde principios generales' if razon_top[0] == 'deductivo' else
         'generalizaciones basadas en casos particulares' if razon_top[0] == 'inductivo' else
         'analogías y comparaciones sistemáticas' if razon_top[0] == 'analogico' else
         'análisis orientado a fines y propósitos' if razon_top[0] == 'teleologico' else
         'estructuras coherentes y sistemáticas' if razon_top[0] == 'sistemico' else
         'apoyos en autoridades doctrinarias y jurisprudenciales' if razon_top[0] == 'autoritativo' else
         'contrastes y oposiciones argumentativas'}.
        
        Su **modalidad epistémica {modal_top[0]}** (intensidad: {modal_top[1]:.2f}) revela que 
        {'busca certezas demostrables y conocimiento necesario' if modal_top[0] == 'apodictico' else
         'explora probabilidades y opiniones razonables' if modal_top[0] == 'dialectico' else
         'enfatiza la persuasión y verosimilitud' if modal_top[0] == 'retorico' else
         'mantiene prudente incertidumbre exploratoria'}.
        """
        
        return explicacion.strip()
    
    def _generar_valoracion_creatividad(self, perfil: Dict[str, Any]) -> str:
        """Genera valoración sobre la creatividad del autor"""
        
        marcadores = perfil.get('marcadores_cognitivos', {})
        creatividad = marcadores.get('creatividad', 0)
        interdisciplina = marcadores.get('interdisciplinariedad', 0)
        abstraccion = marcadores.get('nivel_abstraccion', 0)
        
        nivel_creatividad = (
            "EXCEPCIONAL" if creatividad > 0.8 else
            "ALTA" if creatividad > 0.6 else
            "MODERADA" if creatividad > 0.4 else
            "CONSERVADORA" if creatividad > 0.2 else
            "TRADICIONAL"
        )
        
        valoracion = f"""
        **VALORACIÓN DE CREATIVIDAD: {nivel_creatividad}**
        
        **Innovación Conceptual:** {creatividad:.2f}/1.0
        - {'Propone enfoques novedosos y reinterpretaciones originales' if creatividad > 0.7 else
           'Desarrolla variaciones creativas sobre conceptos establecidos' if creatividad > 0.5 else
           'Aplica metodologías tradicionales con matices personales' if creatividad > 0.3 else
           'Se adhiere a enfoques doctrinarios consolidados'}
        
        **Interdisciplinariedad:** {interdisciplina:.2f}/1.0
        - {'Integra múltiples disciplinas de forma innovadora' if interdisciplina > 0.7 else
           'Incorpora perspectivas de otras áreas del conocimiento' if interdisciplina > 0.5 else
           'Ocasionalmente refiere a conceptos no-jurídicos' if interdisciplina > 0.3 else
           'Se mantiene dentro del ámbito jurídico tradicional'}
        
        **Complejidad Abstracta:** {abstraccion:.2f}/1.0
        - {'Maneja conceptos de alta abstracción teórica' if abstraccion > 0.7 else
           'Desarrolla principios generales y conceptos intermedios' if abstraccion > 0.5 else
           'Combina teoría y práctica de manera equilibrada' if abstraccion > 0.3 else
           'Enfoque predominantemente práctico y concreto'}
        """
        
        return valoracion.strip()
    
    def _generar_analisis_formalismo(self, perfil: Dict[str, Any]) -> str:
        """Genera análisis del nivel de formalismo"""
        
        estilo = perfil.get('cognicion', {}).get('estilo_literario', {})
        marcadores = perfil.get('marcadores_cognitivos', {})
        
        tecnico_juridico = estilo.get('tecnico_juridico', 0)
        burocratico = estilo.get('impersonal_burocratico', 0)
        jurisprudencia = marcadores.get('uso_jurisprudencia', 0)
        complejidad = marcadores.get('complejidad_sintactica', 0)
        
        nivel_formalismo = (tecnico_juridico + burocratico + jurisprudencia) / 3
        
        categoria_formalismo = (
            "ULTRA-FORMAL" if nivel_formalismo > 0.8 else
            "ALTAMENTE FORMAL" if nivel_formalismo > 0.6 else
            "MODERADAMENTE FORMAL" if nivel_formalismo > 0.4 else
            "INFORMAL-FLEXIBLE" if nivel_formalismo > 0.2 else
            "CONVERSACIONAL"
        )
        
        analisis = f"""
        **ANÁLISIS DE FORMALISMO: {categoria_formalismo}**
        
        **Técnica Jurídica:** {tecnico_juridico:.2f}/1.0
        - {'Empleo sistemático de terminología técnica y citas precisas' if tecnico_juridico > 0.7 else
           'Uso competente de lenguaje jurídico especializado' if tecnico_juridico > 0.5 else
           'Terminología jurídica estándar con claridad expositiva' if tecnico_juridico > 0.3 else
           'Lenguaje accesible con mínima tecnicidad'}
        
        **Rigor Estructural:** {complejidad:.2f}/1.0
        - {'Construcciones sintácticas complejas y precisas' if complejidad > 0.7 else
           'Estructura argumentativa sólida y organizada' if complejidad > 0.5 else
           'Exposición clara con estructura básica' if complejidad > 0.3 else
           'Estilo directo y sintaxis simple'}
        
        **Apoyatura Jurisprudencial:** {jurisprudencia:.2f}/1.0
        - {'Referencias exhaustivas a precedentes y fallos' if jurisprudencia > 0.7 else
           'Citas jurisprudenciales selectivas y pertinentes' if jurisprudencia > 0.5 else
           'Referencias ocasionales a jurisprudencia relevante' if jurisprudencia > 0.3 else
           'Mínimo uso de precedentes jurisprudenciales'}
        """
        
        return analisis.strip()
    
    def _generar_analisis_logica_intelectual(self, perfil: Dict[str, Any]) -> str:
        """Genera análisis de la lógica del trabajo intelectual"""
        
        razonamiento = perfil.get('cognicion', {}).get('razonamiento_formal', {})
        estructuras = perfil.get('cognicion', {}).get('estructuras_argumentativas', {})
        marcadores = perfil.get('marcadores_cognitivos', {})
        
        coherencia = marcadores.get('coherencia_global', 0)
        sistematizacion = razonamiento.get('sistemico', 0)
        
        # Identificar estructura argumentativa dominante
        estructura_dominante = max(estructuras.items(), key=lambda x: x[1]) if estructuras else ("libre", 0)
        
        analisis = f"""
        **LÓGICA DEL TRABAJO INTELECTUAL:**
        
        **Arquitectura Argumentativa:**
        - Emplea predominantemente estructura **{estructura_dominante[0].replace('_', ' ').upper()}** 
          (intensidad: {estructura_dominante[1]:.2f})
        - {'Sigue rigurosamente el patrón Issue-Rule-Application-Conclusion' if estructura_dominante[0] == 'IRAC' else
           'Desarrolla argumentos según el modelo Toulmin (claim-warrant-backing)' if estructura_dominante[0] == 'Toulmin' else
           'Estructura libre adaptada al contenido específico'}
        
        **Coherencia Sistémica:** {coherencia:.2f}/1.0
        - {'Demuestra una lógica interna impecable y conexiones sólidas entre ideas' if coherencia > 0.8 else
           'Mantiene coherencia general con buena articulación conceptual' if coherencia > 0.6 else
           'Coherencia básica con algunas inconsistencias menores' if coherencia > 0.4 else
           'Enfoque fragmentario con lógica situacional'}
        
        **Desarrollo de Tesis:**
        - **Sistematización:** {sistematizacion:.2f}/1.0
        - {'Construye sistemas teóricos comprehensivos e integrados' if sistematizacion > 0.7 else
           'Desarrolla marcos conceptuales coherentes y articulados' if sistematizacion > 0.5 else
           'Presenta ideas organizadas con estructura básica' if sistematizacion > 0.3 else
           'Aborda temas de manera puntual y específica'}
        
        **Proceso Decisorio Intelectual:**
        - {'Decisiones fundamentadas en análisis sistemático exhaustivo' if coherencia > 0.7 and sistematizacion > 0.7 else
           'Decisiones basadas en evaluación cuidadosa de alternativas' if coherencia > 0.5 else
           'Decisiones pragmáticas con justificación suficiente' if coherencia > 0.3 else
           'Decisiones intuitivas con validación posterior'}
        """
        
        return analisis.strip()
    
    def _obtener_perfil_original(self, nombre: str) -> Optional[Dict[str, Any]]:
        """Obtiene perfil de la base de datos original como fallback"""
        
        if not os.path.exists(self.db_original):
            return None
        
        conn = sqlite3.connect(self.db_original)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT creatividad, formalismo, empirismo, nivel_abstraccion, dogmatismo,
                       complejidad_sintactica, interdisciplinariedad, uso_jurisprudencia
                FROM perfiles_cognitivos 
                WHERE autor = ? 
                ORDER BY timestamp DESC LIMIT 1
            ''', (nombre,))
            
            resultado = cursor.fetchone()
            if resultado:
                perfil = {
                    "meta": {
                        "autor_probable": nombre,
                        "fuente": "sistema_original",
                        "timestamp": datetime.now().isoformat(),
                        "version_analyser": "original"
                    },
                    "marcadores_cognitivos": {
                        "creatividad": resultado[0],
                        "formalismo": resultado[1],
                        "empirismo": resultado[2],
                        "nivel_abstraccion": resultado[3],
                        "dogmatismo": resultado[4],
                        "complejidad_sintactica": resultado[5],
                        "interdisciplinariedad": resultado[6],
                        "uso_jurisprudencia": resultado[7],
                        "coherencia_global": 0.5
                    },
                    "obras": self.obtener_obras_autor(nombre)
                }
                
                # Generar análisis básicos
                perfil['metodologia_explicacion'] = "Análisis basado en sistema original - datos limitados"
                perfil['creatividad_valoracion'] = f"Creatividad: {resultado[0]:.2f}/1.0"
                perfil['formalismo_analisis'] = f"Formalismo: {resultado[1]:.2f}/1.0"
                perfil['logica_intelectual'] = "Análisis completo disponible con sistema v2.0"
                
                return perfil
        
        except sqlite3.OperationalError:
            pass
        finally:
            conn.close()
        
        return None
    
    def buscar_autores_avanzado(self, filtros: Dict[str, str]) -> List[Dict[str, Any]]:
        """Búsqueda avanzada de autores con múltiples criterios"""
        
        autores = self.obtener_todos_los_autores()
        
        # Aplicar filtros
        resultados = []
        
        for autor in autores:
            cumple_filtros = True
            
            # Filtro por razonamiento
            if filtros.get('razonamiento') and filtros['razonamiento'] != 'todos':
                if autor['razonamiento_dominante'].lower() != filtros['razonamiento'].lower():
                    cumple_filtros = False
            
            # Filtro por creatividad mínima
            if filtros.get('creatividad_min'):
                try:
                    min_creatividad = float(filtros['creatividad_min'])
                    if autor['creatividad'] < min_creatividad:
                        cumple_filtros = False
                except ValueError:
                    pass
            
            # Filtro por nivel de abstracción
            if filtros.get('abstraccion_min'):
                try:
                    min_abstraccion = float(filtros['abstraccion_min'])
                    if autor['nivel_abstraccion'] < min_abstraccion:
                        cumple_filtros = False
                except ValueError:
                    pass
            
            # Filtro por empirismo
            if filtros.get('empirismo_min'):
                try:
                    min_empirismo = float(filtros['empirismo_min'])
                    if autor['empirismo'] < min_empirismo:
                        cumple_filtros = False
                except ValueError:
                    pass
            
            # Filtro por número de obras
            if filtros.get('obras_min'):
                try:
                    min_obras = int(filtros['obras_min'])
                    if autor['num_obras'] < min_obras:
                        cumple_filtros = False
                except ValueError:
                    pass
            
            # Filtro por texto en nombre
            if filtros.get('nombre'):
                if filtros['nombre'].lower() not in autor['nombre'].lower():
                    cumple_filtros = False
            
            if cumple_filtros:
                resultados.append(autor)
        
        # Ordenar resultados
        orden = filtros.get('orden', 'nombre')
        reverse = filtros.get('direccion') == 'desc'
        
        if orden == 'creatividad':
            resultados.sort(key=lambda x: x['creatividad'], reverse=reverse)
        elif orden == 'abstraccion':
            resultados.sort(key=lambda x: x['nivel_abstraccion'], reverse=reverse)
        elif orden == 'obras':
            resultados.sort(key=lambda x: x['num_obras'], reverse=reverse)
        else:
            resultados.sort(key=lambda x: x['nombre'], reverse=reverse)
        
        return resultados
    
    def comparar_autores_detallado(self, autor_a: str, autor_b: str) -> Dict[str, Any]:
        """Comparación detallada entre dos autores"""
        
        perfil_a = self.obtener_perfil_completo_autor(autor_a)
        perfil_b = self.obtener_perfil_completo_autor(autor_b)
        
        if not perfil_a or not perfil_b:
            return {"error": "Uno o ambos autores no encontrados"}
        
        # Usar comparador de mentes si está disponible
        try:
            from comparador_mentes import ComparadorMentes
            comparador = ComparadorMentes()
            
            if 'vector_cognitivo' in perfil_a and 'vector_cognitivo' in perfil_b:
                comparacion = comparador.comparar_mentes(perfil_a, perfil_b)
                
                return {
                    "autor_a": autor_a,
                    "autor_b": autor_b,
                    "similaridad_general": comparacion.cosine_similarity,
                    "distancia_mental": comparacion.distance,
                    "dimensiones_clave": comparacion.dimensiones_clave,
                    "diferencias_principales": comparacion.diferencias_principales,
                    "perfil_a": perfil_a,
                    "perfil_b": perfil_b
                }
        except ImportError:
            pass
        
        # Comparación básica si no está disponible el comparador avanzado
        return self._comparacion_basica(perfil_a, perfil_b)
    
    def _comparacion_basica(self, perfil_a: Dict, perfil_b: Dict) -> Dict[str, Any]:
        """Comparación básica entre dos perfiles"""
        
        marcadores_a = perfil_a.get('marcadores_cognitivos', {})
        marcadores_b = perfil_b.get('marcadores_cognitivos', {})
        
        diferencias = {}
        for key in marcadores_a.keys():
            if key in marcadores_b:
                diferencias[key] = abs(marcadores_a[key] - marcadores_b[key])
        
        return {
            "autor_a": perfil_a['meta']['autor_probable'],
            "autor_b": perfil_b['meta']['autor_probable'],
            "diferencias": diferencias,
            "perfil_a": perfil_a,
            "perfil_b": perfil_b
        }
    
    def obtener_autores_similares(self, autor: str, limite: int = 5) -> List[Dict[str, Any]]:
        """Obtiene autores similares al autor especificado"""
        
        try:
            from comparador_mentes import ComparadorMentes
            comparador = ComparadorMentes()
            ranking = comparador.ranking_similitud_a_autor(autor)
            
            similares = []
            for nombre, similaridad in ranking[:limite]:
                perfil_basico = next((a for a in self.obtener_todos_los_autores() if a['nombre'] == nombre), None)
                if perfil_basico:
                    perfil_basico['similaridad'] = similaridad
                    similares.append(perfil_basico)
            
            return similares
            
        except ImportError:
            # Fallback: encontrar autores con características similares
            return self._buscar_similares_basico(autor, limite)
    
    def _buscar_similares_basico(self, autor: str, limite: int) -> List[Dict[str, Any]]:
        """Búsqueda básica de autores similares"""
        
        autor_ref = next((a for a in self.obtener_todos_los_autores() if a['nombre'] == autor), None)
        if not autor_ref:
            return []
        
        todos_autores = [a for a in self.obtener_todos_los_autores() if a['nombre'] != autor]
        
        # Calcular similaridad básica
        for a in todos_autores:
            similaridad = 1.0 - (
                abs(a['creatividad'] - autor_ref['creatividad']) +
                abs(a['nivel_abstraccion'] - autor_ref['nivel_abstraccion']) +
                abs(a['empirismo'] - autor_ref['empirismo'])
            ) / 3
            a['similaridad'] = max(0, similaridad)
        
        # Ordenar por similaridad y devolver top
        todos_autores.sort(key=lambda x: x['similaridad'], reverse=True)
        return todos_autores[:limite]
    
    def calcular_estadisticas_generales(self) -> Dict[str, Any]:
        """Calcula estadísticas generales del sistema"""
        
        autores = self.obtener_todos_los_autores()
        
        if not autores:
            return {}
        
        total_obras = sum(a['num_obras'] for a in autores)
        creatividad_promedio = sum(a['creatividad'] for a in autores) / len(autores)
        abstraccion_promedio = sum(a['nivel_abstraccion'] for a in autores) / len(autores)
        
        # Razonamiento más común
        razonamientos = [a['razonamiento_dominante'] for a in autores]
        razonamiento_comun = max(set(razonamientos), key=razonamientos.count)
        
        return {
            "total_autores": len(autores),
            "total_obras": total_obras,
            "obras_promedio": round(total_obras / len(autores), 1),
            "creatividad_promedio": round(creatividad_promedio, 2),
            "abstraccion_promedio": round(abstraccion_promedio, 2),
            "razonamiento_mas_comun": razonamiento_comun
        }
    
    def obtener_opciones_filtros(self) -> Dict[str, List[str]]:
        """Obtiene opciones disponibles para filtros"""
        
        autores = self.obtener_todos_los_autores()
        
        razonamientos = list(set(a['razonamiento_dominante'] for a in autores))
        modalidades = list(set(a['modalidad_dominante'] for a in autores))
        estilos = list(set(a['estilo_dominante'] for a in autores))
        
        return {
            "razonamientos": sorted(razonamientos),
            "modalidades": sorted(modalidades),
            "estilos": sorted(estilos)
        }

def main():
    """Función para probar el sistema"""
    print("📚 INICIANDO SISTEMA DE REFERENCIAS DE AUTORES")
    
    sistema = SistemaReferenciasAutores()
    
    # Probar funcionalidades
    autores = sistema.obtener_todos_los_autores()
    print(f"✅ Encontrados {len(autores)} autores")
    
    if autores:
        print(f"📊 Primer autor: {autores[0]['nombre']}")
        perfil = sistema.obtener_perfil_completo_autor(autores[0]['nombre'])
        if perfil:
            print("✅ Perfil completo obtenido")
    
    estadisticas = sistema.calcular_estadisticas_generales()
    print(f"📈 Estadísticas: {estadisticas}")
    
    print("🚀 Sistema listo para uso web")

if __name__ == "__main__":
    main()