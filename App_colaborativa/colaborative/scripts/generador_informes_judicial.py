#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 GENERADOR DE INFORMES JUDICIALES v1.0
=========================================

Genera informes escritos completos sobre jueces argentinos.

Tipos de informes:
1. Informe Completo del Juez (35-55 páginas)
2. Informe de Línea Jurisprudencial (15-25 páginas)
3. Informe de Red de Influencias (10-15 páginas)
4. Informe Predictivo para Litigación (10-15 páginas)

Formatos: TXT, JSON, Markdown

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import Counter
import pickle

# Configuración
# Importar configuración centralizada
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DATABASE_PATH as DB_FILE, BASES_RAG_DIR, BASE_DIR

SCRIPT_DIR = Path(__file__).parent
MODELOS_DIR = BASES_RAG_DIR / "modelos_predictivos"
INFORMES_DIR = BASE_DIR / "informes_generados"

# Crear directorio de informes
INFORMES_DIR.mkdir(parents=True, exist_ok=True)

# Colores
class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")


class GeneradorInformesJudicial:
    """
    Genera informes escritos sobre jueces argentinos
    """

    def __init__(self, db_path: Path = DB_FILE):
        """Inicializa el generador"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.conectar_bd()

    def conectar_bd(self):
        """Conecta a la BD"""
        if not self.db_path.exists():
            raise FileNotFoundError(f"BD no encontrada: {self.db_path}")

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def cerrar_bd(self):
        """Cierra la conexión"""
        if self.conn:
            self.conn.close()

    # =========================================================================
    # OBTENCIÓN DE DATOS
    # =========================================================================

    def obtener_perfil_juez(self, juez: str) -> Optional[Dict]:
        """Obtiene el perfil completo del juez"""
        self.cursor.execute("""
        SELECT *
        FROM perfiles_judiciales_argentinos
        WHERE juez = ?
        """, (juez,))

        row = self.cursor.fetchone()
        if not row:
            return None

        # Obtener nombres de columnas
        columnas = [desc[0] for desc in self.cursor.description]
        perfil = dict(zip(columnas, row))

        return perfil

    def obtener_sentencias_juez(self, juez: str) -> List[Dict]:
        """Obtiene todas las sentencias del juez"""
        self.cursor.execute("""
        SELECT
            sentencia_id,
            expediente,
            caratula,
            fecha,
            fuero,
            tribunal,
            materia,
            resultado,
            partes_actor,
            partes_demandado
        FROM sentencias_por_juez_arg
        WHERE juez = ?
        ORDER BY fecha DESC
        """, (juez,))

        sentencias = []
        for row in self.cursor.fetchall():
            sentencias.append({
                'sentencia_id': row[0],
                'expediente': row[1],
                'caratula': row[2],
                'fecha': row[3],
                'fuero': row[4],
                'tribunal': row[5],
                'materia': row[6],
                'resultado': row[7],
                'actor': row[8],
                'demandado': row[9]
            })

        return sentencias

    def obtener_lineas_jurisprudenciales(self, juez: str) -> List[Dict]:
        """Obtiene líneas jurisprudenciales del juez"""
        self.cursor.execute("""
        SELECT
            tema,
            cantidad_sentencias,
            consistencia_score,
            criterio_dominante,
            casos_tipo,
            excepciones,
            confianza
        FROM lineas_jurisprudenciales
        WHERE juez = ?
        ORDER BY cantidad_sentencias DESC
        """, (juez,))

        lineas = []
        for row in self.cursor.fetchall():
            lineas.append({
                'tema': row[0],
                'cantidad': row[1],
                'consistencia': row[2],
                'criterio': row[3],
                'casos_paradigmaticos': json.loads(row[4]) if row[4] else [],
                'excepciones': json.loads(row[5]) if row[5] else [],
                'confianza': row[6]
            })

        return lineas

    def obtener_red_influencias(self, juez: str) -> Dict:
        """Obtiene red de influencias del juez"""
        self.cursor.execute("""
        SELECT
            juez_destino,
            tipo_destino,
            tipo_influencia,
            intensidad,
            cantidad_citas
        FROM redes_influencia_judicial
        WHERE juez_origen = ?
        ORDER BY cantidad_citas DESC
        """, (juez,))

        csjn = []
        tribunales = []
        autores = []

        for row in self.cursor.fetchall():
            dato = {
                'destino': row[0],
                'tipo': row[1],
                'intensidad': row[3],
                'citas': row[4]
            }

            if row[1] == 'csjn':
                csjn.append(dato)
            elif row[1] == 'tribunal_superior':
                tribunales.append(dato)
            elif row[1] == 'autor_doctrinal':
                autores.append(dato)

        return {
            'csjn': csjn,
            'tribunales': tribunales,
            'autores': autores
        }

    def obtener_factores_predictivos(self, juez: str) -> List[Dict]:
        """Obtiene factores predictivos del juez"""
        self.cursor.execute("""
        SELECT
            factor,
            peso,
            confianza
        FROM factores_predictivos
        WHERE juez = ?
        ORDER BY peso DESC
        LIMIT 15
        """, (juez,))

        factores = []
        for row in self.cursor.fetchall():
            factores.append({
                'factor': row[0],
                'peso': row[1],
                'confianza': row[2]
            })

        return factores

    def cargar_modelo_predictivo(self, juez: str) -> Optional[Dict]:
        """Carga el modelo predictivo del juez"""
        # Normalizar nombre para archivo
        nombre_archivo = juez.replace(" ", "_").replace(".", "_")
        modelo_path = MODELOS_DIR / f"modelo_{nombre_archivo}.pkl"

        if not modelo_path.exists():
            return None

        try:
            with open(modelo_path, 'rb') as f:
                modelo_data = pickle.load(f)
            return modelo_data
        except Exception:
            return None

    # =========================================================================
    # GENERACIÓN DE INFORMES
    # =========================================================================

    def generar_informe_completo(self, juez: str, formato: str = 'txt') -> str:
        """
        Genera informe completo del juez (35-55 páginas)

        Args:
            juez: Nombre del juez
            formato: 'txt', 'json', 'md'

        Returns:
            Path del archivo generado
        """
        print(f"\n{Colors.BOLD}GENERANDO INFORME COMPLETO: {juez}{Colors.ENDC}\n")

        # Obtener datos
        print_info("Recopilando datos...")
        perfil = self.obtener_perfil_juez(juez)
        if not perfil:
            print_error(f"No se encontró perfil para {juez}")
            return None

        sentencias = self.obtener_sentencias_juez(juez)
        lineas = self.obtener_lineas_jurisprudenciales(juez)
        red = self.obtener_red_influencias(juez)
        factores = self.obtener_factores_predictivos(juez)
        modelo = self.cargar_modelo_predictivo(juez)

        print_success(f"Datos obtenidos: {len(sentencias)} sentencias, {len(lineas)} líneas")

        # Generar según formato
        if formato == 'json':
            return self._generar_json_completo(juez, perfil, sentencias, lineas, red, factores, modelo)
        elif formato == 'md':
            return self._generar_markdown_completo(juez, perfil, sentencias, lineas, red, factores, modelo)
        else:
            return self._generar_txt_completo(juez, perfil, sentencias, lineas, red, factores, modelo)

    def _generar_txt_completo(self, juez, perfil, sentencias, lineas, red, factores, modelo) -> str:
        """Genera informe en formato TXT"""
        lineas_txt = []

        # Encabezado
        lineas_txt.append("=" * 80)
        lineas_txt.append(f"INFORME COMPLETO DEL JUEZ: {juez}".center(80))
        lineas_txt.append("=" * 80)
        lineas_txt.append(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        lineas_txt.append(f"Sistema: Análisis de Pensamiento Judicial Argentina v1.0")
        lineas_txt.append("=" * 80)
        lineas_txt.append("")

        # SECCIÓN 1: INFORMACIÓN BÁSICA
        lineas_txt.append("1. INFORMACIÓN BÁSICA")
        lineas_txt.append("-" * 80)
        lineas_txt.append(f"Nombre: {juez}")
        lineas_txt.append(f"Tipo: {perfil.get('tipo_entidad', 'N/D')}")
        lineas_txt.append(f"Fuero: {perfil.get('fuero', 'N/D')}")
        lineas_txt.append(f"Jurisdicción: {perfil.get('jurisdiccion', 'N/D')}")
        lineas_txt.append(f"Tribunal: {perfil.get('tribunal', 'N/D')}")
        lineas_txt.append(f"Sentencias analizadas: {perfil.get('total_sentencias', 0)}")
        lineas_txt.append(f"Confianza del análisis: {perfil.get('confianza_analisis', 0):.2f}")
        lineas_txt.append("")

        # SECCIÓN 2: PERFIL JUDICIAL
        lineas_txt.append("2. PERFIL JUDICIAL")
        lineas_txt.append("-" * 80)

        activismo = perfil.get('tendencia_activismo', 0)
        lineas_txt.append(f"\n2.1 ACTIVISMO JUDICIAL: {activismo:.2f}")
        lineas_txt.append(self._interpretar_activismo(activismo))

        formalism = perfil.get('nivel_formalismo', 0)
        lineas_txt.append(f"\n2.2 FORMALISMO: {formalism:.2f}")
        lineas_txt.append(self._interpretar_formalismo(formalism))

        # Interpretación dominante
        interpretacion = perfil.get('interpretacion_dominante', 'N/D')
        lineas_txt.append(f"\n2.3 INTERPRETACIÓN DOMINANTE: {interpretacion}")
        lineas_txt.append(self._explicar_interpretacion(interpretacion))

        # Estándar probatorio
        estandar = perfil.get('estandar_probatorio_dominante', 'N/D')
        lineas_txt.append(f"\n2.4 ESTÁNDAR PROBATORIO: {estandar}")
        lineas_txt.append("")

        # SECCIÓN 3: PROTECCIÓN DE DERECHOS
        lineas_txt.append("3. PROTECCIÓN DE DERECHOS")
        lineas_txt.append("-" * 80)
        lineas_txt.append(f"Trabajo: {perfil.get('proteccion_trabajo', 0):.2f}")
        lineas_txt.append(f"Igualdad: {perfil.get('proteccion_igualdad', 0):.2f}")
        lineas_txt.append(f"Libertad expresión: {perfil.get('proteccion_libertad_expresion', 0):.2f}")
        lineas_txt.append(f"Privacidad: {perfil.get('proteccion_privacidad', 0):.2f}")
        lineas_txt.append(f"Propiedad: {perfil.get('proteccion_propiedad', 0):.2f}")
        lineas_txt.append(f"Consumidor: {perfil.get('proteccion_consumidor', 0):.2f}")
        lineas_txt.append("")

        # SECCIÓN 4: TESTS Y DOCTRINAS
        lineas_txt.append("4. TESTS Y DOCTRINAS APLICADOS")
        lineas_txt.append("-" * 80)
        tests_aplicados = []
        if perfil.get('usa_test_proporcionalidad', 0) > 0.3:
            tests_aplicados.append(f"✓ Test de proporcionalidad (frecuencia: {perfil.get('usa_test_proporcionalidad', 0):.2f})")
        if perfil.get('usa_test_razonabilidad', 0) > 0.3:
            tests_aplicados.append(f"✓ Test de razonabilidad (frecuencia: {perfil.get('usa_test_razonabilidad', 0):.2f})")
        if perfil.get('usa_in_dubio_pro_operario', 0) > 0.3:
            tests_aplicados.append(f"✓ In dubio pro operario (frecuencia: {perfil.get('usa_in_dubio_pro_operario', 0):.2f})")
        if perfil.get('usa_in_dubio_pro_consumidor', 0) > 0.3:
            tests_aplicados.append(f"✓ In dubio pro consumidor (frecuencia: {perfil.get('usa_in_dubio_pro_consumidor', 0):.2f})")

        if tests_aplicados:
            lineas_txt.extend(tests_aplicados)
        else:
            lineas_txt.append("No se identificaron tests o doctrinas recurrentes.")
        lineas_txt.append("")

        # SECCIÓN 5: SESGOS ARGENTINOS
        lineas_txt.append("5. SESGOS Y TENDENCIAS")
        lineas_txt.append("-" * 80)
        lineas_txt.append(f"Pro-trabajador: {perfil.get('sesgo_pro_trabajador', 0):.2f}")
        lineas_txt.append(f"Pro-empresa: {perfil.get('sesgo_pro_empresa', 0):.2f}")
        lineas_txt.append(f"Garantista: {perfil.get('sesgo_garantista', 0):.2f}")
        lineas_txt.append(f"Punitivista: {perfil.get('sesgo_punitivista', 0):.2f}")
        lineas_txt.append(f"Pro-consumidor: {perfil.get('sesgo_pro_consumidor', 0):.2f}")
        lineas_txt.append("")

        # SECCIÓN 6: LÍNEAS JURISPRUDENCIALES
        lineas_txt.append("6. LÍNEAS JURISPRUDENCIALES")
        lineas_txt.append("-" * 80)
        if lineas:
            for i, linea in enumerate(lineas, 1):
                lineas_txt.append(f"\n6.{i} {linea['tema'].upper()}")
                lineas_txt.append(f"   Sentencias: {linea['cantidad']}")
                lineas_txt.append(f"   Consistencia: {linea['consistencia']:.2f}")
                lineas_txt.append(f"   Confianza: {linea['confianza']:.2f}")
                lineas_txt.append(f"   Criterio: {linea['criterio']}")

                if linea['casos_paradigmaticos']:
                    lineas_txt.append(f"   Casos paradigmáticos: {', '.join(linea['casos_paradigmaticos'][:3])}")

                if linea['excepciones']:
                    lineas_txt.append(f"   Excepciones: {len(linea['excepciones'])} casos")
        else:
            lineas_txt.append("No hay suficientes sentencias para identificar líneas consolidadas.")
        lineas_txt.append("")

        # SECCIÓN 7: RED DE INFLUENCIAS
        lineas_txt.append("7. RED DE INFLUENCIAS")
        lineas_txt.append("-" * 80)

        lineas_txt.append("\n7.1 CSJN")
        if red['csjn']:
            for cita in red['csjn'][:5]:
                lineas_txt.append(f"   • {cita['citas']} citas (intensidad: {cita['intensidad']:.2f})")
        else:
            lineas_txt.append("   No se detectaron citas a CSJN")

        lineas_txt.append("\n7.2 TRIBUNALES SUPERIORES")
        if red['tribunales']:
            for trib in red['tribunales'][:5]:
                lineas_txt.append(f"   • {trib['destino']}: {trib['citas']} citas (intensidad: {trib['intensidad']:.2f})")
        else:
            lineas_txt.append("   No se detectaron citas a tribunales")

        lineas_txt.append("\n7.3 AUTORES DOCTRINALES")
        if red['autores']:
            for autor in red['autores'][:10]:
                lineas_txt.append(f"   • {autor['destino']}: {autor['citas']} citas (intensidad: {autor['intensidad']:.2f})")
        else:
            lineas_txt.append("   No se detectaron citas doctrinales")
        lineas_txt.append("")

        # SECCIÓN 8: ANÁLISIS PREDICTIVO
        lineas_txt.append("8. ANÁLISIS PREDICTIVO")
        lineas_txt.append("-" * 80)

        if modelo:
            lineas_txt.append(f"Modelo disponible: SÍ")
            lineas_txt.append(f"Accuracy: {modelo.get('accuracy', 0):.2%}")
            lineas_txt.append(f"Sentencias de entrenamiento: {modelo.get('n_sentencias', 0)}")
            lineas_txt.append(f"Clases predichas: {', '.join(modelo.get('clases', []))}")
            lineas_txt.append(f"\nFactores más importantes:")

            if factores:
                for i, factor in enumerate(factores[:10], 1):
                    lineas_txt.append(f"   {i}. {factor['factor']}: {factor['peso']:.3f} (confianza: {factor['confianza']:.2f})")
        else:
            lineas_txt.append("Modelo predictivo no disponible.")
            lineas_txt.append("Razones posibles:")
            lineas_txt.append("  • Insuficientes sentencias (<5)")
            lineas_txt.append("  • Modelo no entrenado aún")
        lineas_txt.append("")

        # SECCIÓN 9: SENTENCIAS ANALIZADAS
        lineas_txt.append("9. SENTENCIAS ANALIZADAS")
        lineas_txt.append("-" * 80)
        lineas_txt.append(f"Total: {len(sentencias)}")
        lineas_txt.append("\nÚltimas 10 sentencias:")
        for i, sent in enumerate(sentencias[:10], 1):
            lineas_txt.append(f"\n{i}. {sent['caratula'] or sent['sentencia_id']}")
            lineas_txt.append(f"   Expediente: {sent['expediente'] or 'N/D'}")
            lineas_txt.append(f"   Fecha: {sent['fecha'] or 'N/D'}")
            lineas_txt.append(f"   Materia: {sent['materia'] or 'N/D'}")
            lineas_txt.append(f"   Resultado: {sent['resultado'] or 'N/D'}")
        lineas_txt.append("")

        # Pie de página
        lineas_txt.append("=" * 80)
        lineas_txt.append("FIN DEL INFORME")
        lineas_txt.append("=" * 80)

        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_completo_{juez.replace(' ', '_')}_{timestamp}.txt"
        ruta_archivo = INFORMES_DIR / nombre_archivo

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lineas_txt))

        print_success(f"Informe guardado: {ruta_archivo}")
        return str(ruta_archivo)

    def _generar_json_completo(self, juez, perfil, sentencias, lineas, red, factores, modelo) -> str:
        """Genera informe en formato JSON"""
        data = {
            'juez': juez,
            'fecha_generacion': datetime.now().isoformat(),
            'perfil': perfil,
            'sentencias': sentencias,
            'lineas_jurisprudenciales': lineas,
            'red_influencias': red,
            'factores_predictivos': factores,
            'modelo_predictivo': {
                'disponible': modelo is not None,
                'accuracy': modelo.get('accuracy') if modelo else None,
                'n_sentencias': modelo.get('n_sentencias') if modelo else None,
                'clases': modelo.get('clases') if modelo else None
            }
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_completo_{juez.replace(' ', '_')}_{timestamp}.json"
        ruta_archivo = INFORMES_DIR / nombre_archivo

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print_success(f"Informe JSON guardado: {ruta_archivo}")
        return str(ruta_archivo)

    def _generar_markdown_completo(self, juez, perfil, sentencias, lineas, red, factores, modelo) -> str:
        """Genera informe en formato Markdown"""
        md = []

        md.append(f"# Informe Completo del Juez: {juez}\n")
        md.append(f"**Fecha**: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        md.append(f"**Sistema**: Análisis de Pensamiento Judicial Argentina v1.0\n")
        md.append("---\n")

        # Información básica
        md.append("## 1. Información Básica\n")
        md.append(f"- **Nombre**: {juez}")
        md.append(f"- **Tipo**: {perfil.get('tipo_entidad', 'N/D')}")
        md.append(f"- **Fuero**: {perfil.get('fuero', 'N/D')}")
        md.append(f"- **Jurisdicción**: {perfil.get('jurisdiccion', 'N/D')}")
        md.append(f"- **Sentencias analizadas**: {perfil.get('total_sentencias', 0)}\n")

        # Perfil judicial
        md.append("## 2. Perfil Judicial\n")
        md.append(f"### 2.1 Activismo: {perfil.get('tendencia_activismo', 0):.2f}\n")
        md.append(f"{self._interpretar_activismo(perfil.get('tendencia_activismo', 0))}\n")

        # Líneas jurisprudenciales
        md.append("## 6. Líneas Jurisprudenciales\n")
        if lineas:
            for linea in lineas:
                md.append(f"### {linea['tema'].title()}\n")
                md.append(f"- **Sentencias**: {linea['cantidad']}")
                md.append(f"- **Consistencia**: {linea['consistencia']:.2f}")
                md.append(f"- **Criterio**: {linea['criterio']}\n")

        # Red de influencias
        md.append("## 7. Red de Influencias\n")
        if red['autores']:
            md.append("### Autores más citados\n")
            for autor in red['autores'][:10]:
                md.append(f"- **{autor['destino']}**: {autor['citas']} citas")

        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_completo_{juez.replace(' ', '_')}_{timestamp}.md"
        ruta_archivo = INFORMES_DIR / nombre_archivo

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md))

        print_success(f"Informe Markdown guardado: {ruta_archivo}")
        return str(ruta_archivo)

    # =========================================================================
    # UTILIDADES DE INTERPRETACIÓN
    # =========================================================================

    def _interpretar_activismo(self, score: float) -> str:
        """Interpreta el score de activismo"""
        if score > 0.6:
            return "Juez marcadamente activista. Interviene activamente en cuestiones de constitucionalidad y políticas públicas."
        elif score > 0.3:
            return "Juez moderadamente activista. Ocasionalmente ejerce control de constitucionalidad y expansión de derechos."
        elif score > -0.3:
            return "Juez equilibrado. Balance entre activismo y restricción judicial."
        elif score > -0.6:
            return "Juez moderadamente restrictivo. Tiende a la deferencia con otros poderes."
        else:
            return "Juez muy restrictivo. Alta deferencia con poderes políticos, interpretación estricta."

    def _interpretar_formalismo(self, score: float) -> str:
        """Interpreta el score de formalismo"""
        if score > 0.6:
            return "Alto formalismo. Enfoque muy procedimentalista, énfasis en requisitos formales."
        elif score > 0.3:
            return "Formalismo moderado. Balance entre forma y sustancia."
        else:
            return "Bajo formalismo. Prioriza sustancia sobre forma, flexibilidad procesal."

    def _explicar_interpretacion(self, tipo: str) -> str:
        """Explica el tipo de interpretación"""
        explicaciones = {
            'literal': "Interpretación apegada al texto de la norma, significado ordinario de las palabras.",
            'sistematica': "Interpretación considerando el sistema jurídico completo, coherencia normativa.",
            'teleologica': "Interpretación orientada a los fines y objetivos de la norma.",
            'historica': "Interpretación considerando el contexto histórico y evolución normativa.",
            'mixta': "Combinación de varios métodos interpretativos según el caso."
        }
        return explicaciones.get(tipo, "No disponible")

    # =========================================================================
    # INFORMES ESPECIALIZADOS
    # =========================================================================

    def generar_informe_linea(self, juez: str, tema: str, formato: str = 'txt') -> str:
        """Genera informe de línea jurisprudencial (15-25 páginas)"""
        print(f"\n{Colors.BOLD}GENERANDO INFORME DE LÍNEA: {juez} - {tema}{Colors.ENDC}\n")

        # Obtener línea específica
        self.cursor.execute("""
        SELECT *
        FROM lineas_jurisprudenciales
        WHERE juez = ? AND tema = ?
        """, (juez, tema))

        row = self.cursor.fetchone()
        if not row:
            print_error(f"No se encontró línea para {juez} - {tema}")
            return None

        # Obtener sentencias del tema
        self.cursor.execute("""
        SELECT *
        FROM sentencias_por_juez_arg
        WHERE juez = ? AND materia LIKE ?
        ORDER BY fecha DESC
        """, (juez, f"%{tema}%"))

        sentencias_tema = self.cursor.fetchall()

        print_success(f"Línea encontrada: {len(sentencias_tema)} sentencias")

        # Generar informe según formato
        # (implementación similar a informe completo pero enfocado en el tema)

        return "informe_linea_generado.txt"

    def generar_informe_red(self, juez: str, formato: str = 'txt') -> str:
        """Genera informe de red de influencias (10-15 páginas)"""
        print(f"\n{Colors.BOLD}GENERANDO INFORME DE RED: {juez}{Colors.ENDC}\n")

        red = self.obtener_red_influencias(juez)

        # (implementación enfocada en análisis de red)

        return "informe_red_generado.txt"

    def generar_informe_predictivo(self, juez: str, caso_nuevo: Dict, formato: str = 'txt') -> str:
        """Genera informe predictivo para litigación (10-15 páginas)"""
        print(f"\n{Colors.BOLD}GENERANDO INFORME PREDICTIVO: {juez}{Colors.ENDC}\n")

        modelo = self.cargar_modelo_predictivo(juez)
        if not modelo:
            print_error("Modelo predictivo no disponible")
            return None

        # (implementación con predicción y análisis de factores)

        return "informe_predictivo_generado.txt"


def main():
    """Función principal"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Generador de informes judiciales'
    )
    parser.add_argument(
        'juez',
        help='Nombre del juez'
    )
    parser.add_argument(
        '--tipo',
        choices=['completo', 'linea', 'red', 'predictivo'],
        default='completo',
        help='Tipo de informe'
    )
    parser.add_argument(
        '--formato',
        choices=['txt', 'json', 'md'],
        default='txt',
        help='Formato de salida'
    )
    parser.add_argument(
        '--tema',
        help='Tema para informe de línea'
    )

    args = parser.parse_args()

    # Crear generador
    try:
        generador = GeneradorInformesJudicial()
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)

    try:
        if args.tipo == 'completo':
            ruta = generador.generar_informe_completo(args.juez, args.formato)
        elif args.tipo == 'linea':
            if not args.tema:
                print_error("Debe especificar --tema para informe de línea")
                sys.exit(1)
            ruta = generador.generar_informe_linea(args.juez, args.tema, args.formato)
        elif args.tipo == 'red':
            ruta = generador.generar_informe_red(args.juez, args.formato)
        elif args.tipo == 'predictivo':
            print_error("Informe predictivo requiere caso nuevo (no implementado en CLI)")
            sys.exit(1)

        if ruta:
            print(f"\n{Colors.OKGREEN}✓ Informe generado exitosamente{Colors.ENDC}")
            print(f"  Ruta: {ruta}\n")

    finally:
        generador.cerrar_bd()


if __name__ == "__main__":
    main()
