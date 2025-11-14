#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 MOTOR DE RESPUESTAS JUDICIALES v1.0
=======================================

Motor que responde automáticamente las 140+ preguntas predeterminadas
sobre jueces argentinos, consultando la base de datos y modelos.

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

import sqlite3
import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from sistema_preguntas_judiciales import SistemaPreguntasJudiciales, Pregunta

# Configuración
# Importar configuración centralizada
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DATABASE_PATH as DB_FILE, BASES_RAG_DIR

SCRIPT_DIR = Path(__file__).parent
MODELOS_DIR = BASES_RAG_DIR / "modelos_predictivos"

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

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")


class MotorRespuestasJudiciales:
    """
    Motor inteligente que responde preguntas sobre jueces
    """

    def __init__(self, db_path: Path = DB_FILE):
        """Inicializa el motor"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.sistema_preguntas = SistemaPreguntasJudiciales()
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
        """Obtiene perfil completo del juez"""
        self.cursor.execute("SELECT * FROM perfiles_judiciales_argentinos WHERE juez = ?", (juez,))
        row = self.cursor.fetchone()

        if not row:
            return None

        columnas = [desc[0] for desc in self.cursor.description]
        return dict(zip(columnas, row))

    def obtener_lineas_jurisprudenciales(self, juez: str) -> List[Dict]:
        """Obtiene líneas jurisprudenciales"""
        self.cursor.execute("""
        SELECT tema, cantidad_sentencias, consistencia_score, criterio_dominante, casos_tipo, excepciones, confianza
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
        """Obtiene red de influencias"""
        self.cursor.execute("""
        SELECT juez_destino, tipo_destino, intensidad, cantidad_citas
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
                'intensidad': row[2],
                'citas': row[3]
            }

            if row[1] == 'csjn':
                csjn.append(dato)
            elif row[1] == 'tribunal_superior':
                tribunales.append(dato)
            elif row[1] == 'autor_doctrinal':
                autores.append(dato)

        return {'csjn': csjn, 'tribunales': tribunales, 'autores': autores}

    def obtener_factores_predictivos(self, juez: str) -> List[Dict]:
        """Obtiene factores predictivos"""
        self.cursor.execute("""
        SELECT factor, peso, confianza
        FROM factores_predictivos
        WHERE juez = ?
        ORDER BY peso DESC
        """, (juez,))

        return [{'factor': r[0], 'peso': r[1], 'confianza': r[2]} for r in self.cursor.fetchall()]

    def cargar_modelo_predictivo(self, juez: str) -> Optional[Dict]:
        """Carga modelo predictivo"""
        nombre_archivo = juez.replace(" ", "_").replace(".", "_")
        modelo_path = MODELOS_DIR / f"modelo_{nombre_archivo}.pkl"

        if not modelo_path.exists():
            return None

        try:
            with open(modelo_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None

    # =========================================================================
    # RESPUESTAS POR TIPO
    # =========================================================================

    def responder_score(self, juez: str, campo: str, perfil: Dict) -> str:
        """Responde pregunta tipo score (0-1)"""
        valor = perfil.get(campo)

        if valor is None:
            return "No disponible (insuficientes datos)"

        # Formatear
        return f"{valor:.2f} ({self._interpretar_score(valor, campo)})"

    def responder_numero(self, juez: str, campo: str, perfil: Dict) -> str:
        """Responde pregunta tipo número"""
        valor = perfil.get(campo)

        if valor is None:
            return "No disponible"

        return str(int(valor))

    def responder_boolean(self, juez: str, campo: str, perfil: Dict) -> str:
        """Responde pregunta tipo booleano"""
        if campo == 'factores_predictivos':
            factores = self.obtener_factores_predictivos(juez)
            return "SÍ" if factores else "NO"

        valor = perfil.get(campo)
        if valor is None:
            return "No disponible"

        return "SÍ" if valor else "NO"

    def responder_texto_simple(self, juez: str, campo: str, perfil: Dict) -> str:
        """Responde pregunta texto simple"""
        valor = perfil.get(campo)

        if valor is None:
            return "No disponible"

        return str(valor)

    # =========================================================================
    # RESPUESTAS COMPLEJAS
    # =========================================================================

    def responder_A01(self, juez: str, perfil: Dict) -> str:
        """A01: Perfil judicial general"""
        activismo = perfil.get('tendencia_activismo', 0)
        formalismo = perfil.get('nivel_formalismo', 0)
        interpretacion = perfil.get('interpretacion_dominante', 'N/D')
        fuero = perfil.get('fuero', 'N/D')

        return f"""Juez de fuero {fuero} con perfil {self._interpretar_activismo(activismo).lower()}, \
nivel de formalismo {self._interpretar_formalismo(formalismo).lower()}, \
y método interpretativo dominante {interpretacion}. \
Analizado con base en {perfil.get('total_sentencias', 0)} sentencias \
(confianza: {perfil.get('confianza_analisis', 0):.2f})."""

    def responder_A20(self, juez: str, perfil: Dict) -> str:
        """A20: Síntesis completa del perfil"""
        activismo = perfil.get('tendencia_activismo', 0)
        formalismo = perfil.get('nivel_formalismo', 0)
        interpretacion = perfil.get('interpretacion_dominante', 'N/D')
        fuero = perfil.get('fuero', 'N/D')
        trabajo = perfil.get('proteccion_trabajo', 0)
        garantista = perfil.get('sesgo_garantista', 0)

        return f"""SÍNTESIS: Juez de {fuero}, {self._interpretar_activismo(activismo).lower()}, \
{self._interpretar_formalismo(formalismo).lower()}. Interpretación {interpretacion}. \
Protección laboral: {trabajo:.2f}. Perfil {'garantista' if garantista > 0.5 else 'equilibrado'}. \
Base: {perfil.get('total_sentencias', 0)} sentencias."""

    def responder_C09(self, juez: str, perfil: Dict) -> str:
        """C09: Derechos protegidos con mayor intensidad"""
        derechos = {
            'trabajo': perfil.get('proteccion_trabajo', 0),
            'igualdad': perfil.get('proteccion_igualdad', 0),
            'libertad_expresion': perfil.get('proteccion_libertad_expresion', 0),
            'privacidad': perfil.get('proteccion_privacidad', 0),
            'propiedad': perfil.get('proteccion_propiedad', 0),
            'consumidor': perfil.get('proteccion_consumidor', 0)
        }

        # Ordenar por valor
        ordenados = sorted(derechos.items(), key=lambda x: x[1], reverse=True)

        # Top 3
        top = ordenados[:3]
        return ", ".join([f"{d.replace('_', ' ').title()} ({v:.2f})" for d, v in top])

    def responder_C10(self, juez: str, perfil: Dict) -> str:
        """C10: Derechos protegidos con menor intensidad"""
        derechos = {
            'trabajo': perfil.get('proteccion_trabajo', 0),
            'igualdad': perfil.get('proteccion_igualdad', 0),
            'libertad_expresion': perfil.get('proteccion_libertad_expresion', 0),
            'privacidad': perfil.get('proteccion_privacidad', 0),
            'propiedad': perfil.get('proteccion_propiedad', 0),
            'consumidor': perfil.get('proteccion_consumidor', 0)
        }

        ordenados = sorted(derechos.items(), key=lambda x: x[1])
        bottom = ordenados[:3]
        return ", ".join([f"{d.replace('_', ' ').title()} ({v:.2f})" for d, v in bottom])

    def responder_D01(self, juez: str, perfil: Dict) -> str:
        """D01: Principales líneas jurisprudenciales"""
        lineas = self.obtener_lineas_jurisprudenciales(juez)

        if not lineas:
            return "No hay líneas consolidadas (insuficientes sentencias por tema)"

        # Top 5 líneas
        resultado = []
        for linea in lineas[:5]:
            resultado.append(f"{linea['tema']} ({linea['cantidad']} sentencias, consistencia {linea['consistencia']:.2f})")

        return "; ".join(resultado)

    def responder_E01(self, juez: str, perfil: Dict) -> str:
        """E01: Tribunales más citados"""
        red = self.obtener_red_influencias(juez)

        if not red['csjn'] and not red['tribunales']:
            return "No se detectaron citas a tribunales superiores"

        resultado = []

        # CSJN
        if red['csjn']:
            resultado.append(f"CSJN ({red['csjn'][0]['citas']} citas)")

        # Otros tribunales
        for trib in red['tribunales'][:3]:
            resultado.append(f"{trib['destino']} ({trib['citas']} citas)")

        return ", ".join(resultado)

    def responder_E03(self, juez: str, perfil: Dict) -> str:
        """E03: Autores doctrinales más citados"""
        red = self.obtener_red_influencias(juez)

        if not red['autores']:
            return "No se detectaron citas doctrinales"

        # Top 5 autores
        resultado = []
        for autor in red['autores'][:5]:
            resultado.append(f"{autor['destino']} ({autor['citas']} citas)")

        return ", ".join(resultado)

    def responder_F03(self, juez: str, perfil: Dict) -> str:
        """F03: Factores más determinantes"""
        factores = self.obtener_factores_predictivos(juez)

        if not factores:
            return "Modelo predictivo no disponible"

        # Top 5 factores
        top = factores[:5]
        resultado = []
        for f in top:
            resultado.append(f"{f['factor']} (peso: {f['peso']:.3f})")

        return "; ".join(resultado)

    def responder_G06(self, juez: str, perfil: Dict) -> str:
        """G06: Sesgo dominante"""
        sesgos = {
            'pro-trabajador': perfil.get('sesgo_pro_trabajador', 0),
            'pro-empresa': perfil.get('sesgo_pro_empresa', 0),
            'garantista': perfil.get('sesgo_garantista', 0),
            'punitivista': perfil.get('sesgo_punitivista', 0),
            'pro-consumidor': perfil.get('sesgo_pro_consumidor', 0)
        }

        # Encontrar el máximo
        max_sesgo = max(sesgos.items(), key=lambda x: abs(x[1]))

        if abs(max_sesgo[1]) < 0.3:
            return "Neutral (no se detectan sesgos marcados)"

        return f"{max_sesgo[0].title()} ({max_sesgo[1]:.2f})"

    # =========================================================================
    # MOTOR PRINCIPAL
    # =========================================================================

    def responder_pregunta(self, juez: str, pregunta_id: str) -> Dict:
        """
        Responde una pregunta específica

        Returns:
            Dict con pregunta, respuesta, metadatos
        """
        # Obtener pregunta
        pregunta = self.sistema_preguntas.obtener_pregunta_por_id(pregunta_id)

        if not pregunta:
            return {
                'pregunta_id': pregunta_id,
                'error': 'Pregunta no encontrada'
            }

        # Obtener datos necesarios
        perfil = self.obtener_perfil_juez(juez)

        if not perfil:
            return {
                'pregunta_id': pregunta_id,
                'pregunta': pregunta.pregunta,
                'respuesta': f"No se encontró perfil para {juez}",
                'disponible': False
            }

        # Responder según tipo
        try:
            # Respuestas especializadas
            if hasattr(self, f'responder_{pregunta_id}'):
                metodo = getattr(self, f'responder_{pregunta_id}')
                respuesta = metodo(juez, perfil)
            # Respuestas genéricas por tipo
            elif pregunta.tipo_respuesta == 'score':
                campo = pregunta.campos_necesarios[0]
                respuesta = self.responder_score(juez, campo, perfil)
            elif pregunta.tipo_respuesta == 'numero':
                campo = pregunta.campos_necesarios[0]
                respuesta = self.responder_numero(juez, campo, perfil)
            elif pregunta.tipo_respuesta == 'boolean':
                campo = pregunta.campos_necesarios[0]
                respuesta = self.responder_boolean(juez, campo, perfil)
            elif pregunta.tipo_respuesta == 'texto':
                campo = pregunta.campos_necesarios[0]
                respuesta = self.responder_texto_simple(juez, campo, perfil)
            else:
                respuesta = "Tipo de respuesta no implementado"

            return {
                'pregunta_id': pregunta_id,
                'categoria': pregunta.categoria,
                'pregunta': pregunta.pregunta,
                'respuesta': respuesta,
                'tipo': pregunta.tipo_respuesta,
                'disponible': True
            }

        except Exception as e:
            return {
                'pregunta_id': pregunta_id,
                'pregunta': pregunta.pregunta,
                'respuesta': f"Error: {str(e)}",
                'disponible': False
            }

    def responder_categoria(self, juez: str, categoria: str) -> List[Dict]:
        """Responde todas las preguntas de una categoría"""
        preguntas = self.sistema_preguntas.obtener_preguntas_por_categoria(categoria)

        respuestas = []
        for pregunta in preguntas:
            respuesta = self.responder_pregunta(juez, pregunta.id)
            respuestas.append(respuesta)

        return respuestas

    def responder_todas(self, juez: str) -> Dict:
        """Responde las 140+ preguntas"""
        print(f"\n{Colors.BOLD}RESPONDIENDO 140+ PREGUNTAS: {juez}{Colors.ENDC}\n")

        todas_respuestas = {}

        for categoria in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            print_info(f"Procesando categoría {categoria}...")
            respuestas = self.responder_categoria(juez, categoria)
            todas_respuestas[categoria] = respuestas

        total = sum(len(r) for r in todas_respuestas.values())
        disponibles = sum(1 for cat in todas_respuestas.values() for r in cat if r.get('disponible'))

        print_success(f"Completado: {disponibles}/{total} respuestas disponibles")

        return {
            'juez': juez,
            'fecha': datetime.now().isoformat(),
            'total_preguntas': total,
            'respuestas_disponibles': disponibles,
            'respuestas': todas_respuestas
        }

    def generar_informe_preguntas(self, juez: str, formato: str = 'txt') -> str:
        """Genera informe con todas las respuestas"""
        respuestas_data = self.responder_todas(juez)

        if formato == 'json':
            return self._exportar_json(juez, respuestas_data)
        else:
            return self._exportar_txt(juez, respuestas_data)

    def _exportar_txt(self, juez: str, data: Dict) -> str:
        """Exporta respuestas a TXT"""
        lineas = []

        lineas.append("=" * 80)
        lineas.append(f"INFORME DE PREGUNTAS: {juez}".center(80))
        lineas.append("=" * 80)
        lineas.append(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        lineas.append(f"Total preguntas: {data['total_preguntas']}")
        lineas.append(f"Respuestas disponibles: {data['respuestas_disponibles']}")
        lineas.append("=" * 80)
        lineas.append("")

        categorias_nombres = self.sistema_preguntas.obtener_categorias()

        for categoria, respuestas in data['respuestas'].items():
            lineas.append(f"\n{categoria}. {categorias_nombres[categoria].upper()}")
            lineas.append("-" * 80)

            for resp in respuestas:
                lineas.append(f"\n{resp['pregunta_id']}. {resp['pregunta']}")
                lineas.append(f"R: {resp['respuesta']}")

        lineas.append("\n" + "=" * 80)
        lineas.append("FIN DEL INFORME")
        lineas.append("=" * 80)

        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo = BASE_DIR / "informes_generados" / f"preguntas_{juez.replace(' ', '_')}_{timestamp}.txt"
        archivo.parent.mkdir(parents=True, exist_ok=True)

        with open(archivo, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lineas))

        print_success(f"Informe guardado: {archivo}")
        return str(archivo)

    def _exportar_json(self, juez: str, data: Dict) -> str:
        """Exporta respuestas a JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo = BASE_DIR / "informes_generados" / f"preguntas_{juez.replace(' ', '_')}_{timestamp}.json"
        archivo.parent.mkdir(parents=True, exist_ok=True)

        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print_success(f"Informe JSON guardado: {archivo}")
        return str(archivo)

    # =========================================================================
    # UTILIDADES DE INTERPRETACIÓN
    # =========================================================================

    def _interpretar_score(self, valor: float, campo: str) -> str:
        """Interpreta un score según el campo"""
        if 'activismo' in campo:
            return self._interpretar_activismo(valor)
        elif 'formalismo' in campo:
            return self._interpretar_formalismo(valor)
        elif valor > 0.7:
            return "alto"
        elif valor > 0.4:
            return "moderado"
        else:
            return "bajo"

    def _interpretar_activismo(self, score: float) -> str:
        """Interpreta activismo"""
        if score > 0.6:
            return "marcadamente activista"
        elif score > 0.3:
            return "moderadamente activista"
        elif score > -0.3:
            return "equilibrado"
        elif score > -0.6:
            return "moderadamente restrictivo"
        else:
            return "muy restrictivo"

    def _interpretar_formalismo(self, score: float) -> str:
        """Interpreta formalismo"""
        if score > 0.6:
            return "alto formalismo"
        elif score > 0.3:
            return "formalismo moderado"
        else:
            return "bajo formalismo"


def main():
    """Función principal"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Motor de respuestas judiciales'
    )
    parser.add_argument(
        'juez',
        help='Nombre del juez'
    )
    parser.add_argument(
        '--pregunta',
        help='ID de pregunta específica (ej: A01)'
    )
    parser.add_argument(
        '--categoria',
        choices=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        help='Responder toda una categoría'
    )
    parser.add_argument(
        '--todas',
        action='store_true',
        help='Responder las 140+ preguntas'
    )
    parser.add_argument(
        '--formato',
        choices=['txt', 'json'],
        default='txt',
        help='Formato de salida'
    )

    args = parser.parse_args()

    # Crear motor
    try:
        motor = MotorRespuestasJudiciales()
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)

    try:
        if args.pregunta:
            # Responder pregunta específica
            respuesta = motor.responder_pregunta(args.juez, args.pregunta)
            print(f"\n{respuesta['pregunta']}")
            print(f"R: {respuesta['respuesta']}\n")

        elif args.categoria:
            # Responder categoría
            respuestas = motor.responder_categoria(args.juez, args.categoria)
            print(f"\n{Colors.BOLD}Categoría {args.categoria}{Colors.ENDC}\n")
            for resp in respuestas:
                print(f"{resp['pregunta_id']}. {resp['pregunta']}")
                print(f"R: {resp['respuesta']}\n")

        elif args.todas:
            # Responder todas y generar informe
            archivo = motor.generar_informe_preguntas(args.juez, args.formato)
            print(f"\n{Colors.OKGREEN}✓ Informe completo generado{Colors.ENDC}")
            print(f"  Archivo: {archivo}\n")

        else:
            parser.print_help()

    finally:
        motor.cerrar_bd()


if __name__ == "__main__":
    main()
