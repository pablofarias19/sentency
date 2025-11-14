#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 ANALIZADOR DE LÍNEAS JURISPRUDENCIALES v1.0
===============================================

Identifica y analiza líneas jurisprudenciales consistentes por juez y tema.

Funcionalidades:
- Agrupa sentencias por tema
- Identifica criterios consistentes
- Calcula consistencia (0-1)
- Extrae casos paradigmáticos
- Identifica excepciones al criterio
- Detecta factores predictivos
- Guarda en tabla lineas_jurisprudenciales

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict
import statistics

# Configuración
# Importar configuración centralizada
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DATABASE_PATH as DB_FILE, BASES_RAG_DIR

SCRIPT_DIR = Path(__file__).parent

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


class AnalizadorLineasJurisprudenciales:
    """
    Analiza líneas jurisprudenciales de un juez
    """

    def __init__(self, db_path: Path = DB_FILE):
        """Inicializa el analizador"""
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

    def obtener_sentencias_juez(self, juez: str) -> List[Dict]:
        """
        Obtiene todas las sentencias de un juez con análisis

        Returns:
            Lista de diccionarios con sentencia y análisis
        """
        self.cursor.execute("""
        SELECT
            sentencia_id,
            materia,
            fecha_sentencia,
            resultado,
            perfil_cognitivo,
            texto_completo,
            caratula
        FROM sentencias_por_juez_arg
        WHERE juez = ? AND perfil_cognitivo IS NOT NULL
        ORDER BY fecha_sentencia
        """, (juez,))

        sentencias = []
        for row in self.cursor.fetchall():
            sent_id, materia, fecha, resultado, perfil_json, texto, caratula = row

            perfil = {}
            if perfil_json:
                try:
                    perfil = json.loads(perfil_json)
                except json.JSONDecodeError:
                    pass

            sentencias.append({
                'sentencia_id': sent_id,
                'materia': materia,
                'fecha': fecha,
                'resultado': resultado,
                'perfil': perfil,
                'texto': texto,
                'caratula': caratula
            })

        return sentencias

    def agrupar_por_tema(self, sentencias: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Agrupa sentencias por tema (materia)

        Returns:
            Diccionario {tema: [sentencias]}
        """
        grupos = defaultdict(list)

        for sent in sentencias:
            tema = sent.get('materia') or 'sin_clasificar'
            # Normalizar tema
            tema = tema.lower().strip()
            grupos[tema].append(sent)

        return dict(grupos)

    def identificar_criterio_dominante(self, sentencias: List[Dict]) -> str:
        """
        Identifica el criterio dominante en un grupo de sentencias

        Returns:
            Descripción del criterio
        """
        # Analizar resultados
        resultados = [s.get('resultado') for s in sentencias if s.get('resultado')]
        resultado_moda = Counter(resultados).most_common(1)[0][0] if resultados else 'no_determinado'

        # Analizar interpretación normativa
        interpretaciones = []
        for s in sentencias:
            perfil = s.get('perfil', {})
            judicial = perfil.get('analisis_judicial', {})
            interp = judicial.get('interpretacion_normativa')
            if interp:
                interpretaciones.append(interp)

        interp_moda = Counter(interpretaciones).most_common(1)[0][0] if interpretaciones else 'no_determinado'

        # Analizar tests aplicados
        tests_counter = Counter()
        for s in sentencias:
            perfil = s.get('perfil', {})
            judicial = perfil.get('analisis_judicial', {})
            tests = judicial.get('tests_aplicados', {})
            for test, score in tests.items():
                if score > 0.3:  # Umbral
                    tests_counter[test] += 1

        tests_frecuentes = [t for t, _ in tests_counter.most_common(3)]

        # Construir descripción del criterio
        criterio = f"Tiende a {resultado_moda} los reclamos, "
        criterio += f"usando interpretación {interp_moda}"

        if tests_frecuentes:
            criterio += f". Aplica frecuentemente: {', '.join(tests_frecuentes)}"

        return criterio

    def calcular_consistencia(self, sentencias: List[Dict]) -> Tuple[float, int, int]:
        """
        Calcula la consistencia de una línea

        Returns:
            Tupla (consistencia_score, consistentes, inconsistentes)
        """
        if len(sentencias) < 2:
            return (1.0, len(sentencias), 0)

        # Analizar resultados
        resultados = [s.get('resultado') for s in sentencias if s.get('resultado')]
        if resultados:
            resultado_moda = Counter(resultados).most_common(1)[0]
            consistentes_resultado = resultado_moda[1]
            total = len(resultados)
        else:
            return (0.5, 0, 0)

        # Analizar interpretación
        interpretaciones = []
        for s in sentencias:
            perfil = s.get('perfil', {})
            judicial = perfil.get('analisis_judicial', {})
            interp = judicial.get('interpretacion_normativa')
            if interp:
                interpretaciones.append(interp)

        if interpretaciones:
            interp_moda = Counter(interpretaciones).most_common(1)[0]
            consistentes_interp = interp_moda[1]
            total_interp = len(interpretaciones)
        else:
            consistentes_interp = 0
            total_interp = 1

        # Score combinado
        score_resultado = consistentes_resultado / total if total > 0 else 0.5
        score_interp = consistentes_interp / total_interp if total_interp > 0 else 0.5

        consistencia = (score_resultado + score_interp) / 2.0

        consistentes = int(consistencia * len(sentencias))
        inconsistentes = len(sentencias) - consistentes

        return (round(consistencia, 3), consistentes, inconsistentes)

    def identificar_casos_paradigmaticos(self, sentencias: List[Dict], top_n: int = 3) -> List[str]:
        """
        Identifica los casos más representativos de la línea

        Returns:
            Lista de IDs de sentencias paradigmáticas
        """
        if not sentencias:
            return []

        # Criterio: sentencias más antiguas (establecen precedente)
        # y sentencias con análisis más completo
        scored = []

        for sent in sentencias:
            score = 0.0

            # Antigüedad (primeras sentencias establecen criterio)
            fecha = sent.get('fecha')
            if fecha:
                # Fechas más antiguas = mayor score
                try:
                    fecha_dt = datetime.fromisoformat(fecha)
                    # Score basado en antigüedad (más viejo = más score)
                    dias_desde_primera = (datetime.now() - fecha_dt).days
                    score += min(1.0, dias_desde_primera / 3650.0)  # Máximo 10 años
                except:
                    pass

            # Completitud del análisis
            perfil = sent.get('perfil', {})
            if perfil:
                score += 0.5

            # Tests aplicados (más tests = más representativo)
            judicial = perfil.get('analisis_judicial', {})
            tests = judicial.get('tests_aplicados', {})
            tests_count = sum(1 for v in tests.values() if v > 0.3)
            score += min(1.0, tests_count * 0.2)

            scored.append((sent['sentencia_id'], score))

        # Ordenar por score y tomar top N
        scored.sort(key=lambda x: x[1], reverse=True)
        return [sent_id for sent_id, _ in scored[:top_n]]

    def identificar_excepciones(self, sentencias: List[Dict], criterio_dominante: str) -> List[Dict]:
        """
        Identifica sentencias que se apartan del criterio

        Returns:
            Lista de diccionarios con excepciones
        """
        # Determinar resultado dominante
        resultados = [s.get('resultado') for s in sentencias if s.get('resultado')]
        if not resultados:
            return []

        resultado_moda = Counter(resultados).most_common(1)[0][0]

        # Identificar sentencias con resultado diferente
        excepciones = []
        for sent in sentencias:
            if sent.get('resultado') and sent['resultado'] != resultado_moda:
                excepciones.append({
                    'sentencia_id': sent['sentencia_id'],
                    'resultado': sent['resultado'],
                    'razon': f"Resultado diferente al dominante ({resultado_moda})"
                })

        return excepciones

    def extraer_factores_predictivos(self, sentencias: List[Dict]) -> List[Dict]:
        """
        Extrae factores que predicen la aplicación de esta línea

        Returns:
            Lista de factores con pesos
        """
        factores = []

        # Analizar materia
        materias = [s.get('materia') for s in sentencias if s.get('materia')]
        if materias:
            materia_moda = Counter(materias).most_common(1)[0]
            factores.append({
                'factor': f"materia={materia_moda[0]}",
                'peso': materia_moda[1] / len(materias)
            })

        # Analizar tests aplicados
        tests_counter = Counter()
        for s in sentencias:
            perfil = s.get('perfil', {})
            judicial = perfil.get('analisis_judicial', {})
            tests = judicial.get('tests_aplicados', {})
            for test, score in tests.items():
                if score > 0.3:
                    tests_counter[test] += 1

        for test, count in tests_counter.most_common(3):
            factores.append({
                'factor': f"test={test}",
                'peso': count / len(sentencias)
            })

        return factores

    def analizar_linea(self, juez: str, tema: str, sentencias: List[Dict]) -> Dict:
        """
        Análisis completo de una línea jurisprudencial

        Returns:
            Diccionario con análisis completo
        """
        if not sentencias:
            return {}

        print_info(f"Analizando línea: {tema} ({len(sentencias)} sentencias)")

        # Fechas
        fechas = [s.get('fecha') for s in sentencias if s.get('fecha')]
        fecha_primera = min(fechas) if fechas else None
        fecha_ultima = max(fechas) if fechas else None

        # Criterio dominante
        criterio = self.identificar_criterio_dominante(sentencias)

        # Consistencia
        consistencia, consistentes, inconsistentes = self.calcular_consistencia(sentencias)

        # Casos paradigmáticos
        paradigmaticos = self.identificar_casos_paradigmaticos(sentencias)

        # Excepciones
        excepciones = self.identificar_excepciones(sentencias, criterio)

        # Factores predictivos
        factores = self.extraer_factores_predictivos(sentencias)

        # Tests recurrentes
        tests_counter = Counter()
        for s in sentencias:
            perfil = s.get('perfil', {})
            judicial = perfil.get('analisis_judicial', {})
            tests = judicial.get('tests_aplicados', {})
            for test, score in tests.items():
                if score > 0.3:
                    tests_counter[test] += 1

        tests_recurrentes = [t for t, _ in tests_counter.most_common(5)]

        linea = {
            'juez': juez,
            'tema': tema,
            'cantidad_sentencias': len(sentencias),
            'fecha_primera': fecha_primera,
            'fecha_ultima': fecha_ultima,
            'sentencias_ids': [s['sentencia_id'] for s in sentencias],
            'criterio_dominante': criterio,
            'consistencia_score': consistencia,
            'consistentes': consistentes,
            'inconsistentes': inconsistentes,
            'casos_paradigmaticos': paradigmaticos,
            'excepciones': excepciones,
            'factores_predictivos': factores,
            'tests_recurrentes': tests_recurrentes,
            'confianza': min(1.0, len(sentencias) / 10.0)  # Más sentencias = más confianza
        }

        print_success(f"  Consistencia: {consistencia:.2f}, Casos paradigmáticos: {len(paradigmaticos)}")

        return linea

    def guardar_linea(self, linea: Dict) -> bool:
        """
        Guarda una línea jurisprudencial en la BD

        Returns:
            True si se guardó exitosamente
        """
        try:
            self.cursor.execute("""
            INSERT INTO lineas_jurisprudenciales (
                juez,
                tema,
                materia,
                sentencias_ids,
                cantidad_sentencias,
                fecha_primera_sentencia,
                fecha_ultima_sentencia,
                criterio_dominante,
                consistencia_score,
                sentencias_consistentes,
                sentencias_inconsistentes,
                tests_recurrentes,
                excepciones_identificadas,
                factores_predictivos,
                casos_tipo,
                fecha_analisis,
                confianza_linea
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                linea['juez'],
                linea['tema'],
                linea['tema'],  # Por ahora materia = tema
                json.dumps(linea['sentencias_ids'], ensure_ascii=False),
                linea['cantidad_sentencias'],
                linea['fecha_primera'],
                linea['fecha_ultima'],
                linea['criterio_dominante'],
                linea['consistencia_score'],
                linea['consistentes'],
                linea['inconsistentes'],
                json.dumps(linea['tests_recurrentes'], ensure_ascii=False),
                json.dumps(linea['excepciones'], ensure_ascii=False),
                json.dumps(linea['factores_predictivos'], ensure_ascii=False),
                json.dumps(linea['casos_paradigmaticos'], ensure_ascii=False),
                datetime.now().isoformat(),
                linea['confianza']
            ))

            self.conn.commit()
            return True

        except sqlite3.Error as e:
            print_error(f"Error al guardar línea: {e}")
            self.conn.rollback()
            return False

    def analizar_juez_completo(self, juez: str, min_sentencias: int = 2) -> Dict:
        """
        Analiza todas las líneas jurisprudenciales de un juez

        Args:
            juez: Nombre del juez
            min_sentencias: Mínimo de sentencias para considerar una línea

        Returns:
            Estadísticas del análisis
        """
        print(f"\n{Colors.BOLD}{'='*70}")
        print(f"ANÁLISIS DE LÍNEAS JURISPRUDENCIALES: {juez}")
        print(f"{'='*70}{Colors.ENDC}\n")

        # 1. Obtener sentencias
        print_info("Obteniendo sentencias...")
        sentencias = self.obtener_sentencias_juez(juez)

        if not sentencias:
            print_error("No hay sentencias analizadas para este juez")
            return {'total': 0, 'lineas_encontradas': 0, 'guardadas': 0}

        print_success(f"Sentencias encontradas: {len(sentencias)}")

        # 2. Agrupar por tema
        print_info("Agrupando por tema...")
        grupos = self.agrupar_por_tema(sentencias)
        print_success(f"Temas identificados: {len(grupos)}")

        # 3. Analizar cada línea
        lineas_analizadas = 0
        lineas_guardadas = 0

        # Limpiar líneas antiguas de este juez
        self.cursor.execute("DELETE FROM lineas_jurisprudenciales WHERE juez = ?", (juez,))
        self.conn.commit()

        for tema, sents in grupos.items():
            if len(sents) < min_sentencias:
                print_warning(f"  Tema '{tema}' tiene solo {len(sents)} sentencia(s), omitiendo")
                continue

            linea = self.analizar_linea(juez, tema, sents)
            lineas_analizadas += 1

            if self.guardar_linea(linea):
                lineas_guardadas += 1

        # 4. Actualizar perfil del juez con líneas consolidadas
        self.actualizar_perfil_juez_con_lineas(juez)

        # Resumen
        print(f"\n{Colors.BOLD}{'='*70}")
        print("RESUMEN")
        print(f"{'='*70}{Colors.ENDC}")
        print(f"Total sentencias: {len(sentencias)}")
        print(f"Temas identificados: {len(grupos)}")
        print(f"{Colors.OKGREEN}Líneas analizadas: {lineas_analizadas}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Líneas guardadas: {lineas_guardadas}{Colors.ENDC}\n")

        return {
            'total': len(sentencias),
            'temas': len(grupos),
            'lineas_encontradas': lineas_analizadas,
            'guardadas': lineas_guardadas
        }

    def actualizar_perfil_juez_con_lineas(self, juez: str):
        """Actualiza el perfil del juez con resumen de líneas"""
        try:
            # Obtener líneas del juez
            self.cursor.execute("""
            SELECT tema, consistencia_score
            FROM lineas_jurisprudenciales
            WHERE juez = ?
            ORDER BY cantidad_sentencias DESC
            """, (juez,))

            lineas = self.cursor.fetchall()

            if not lineas:
                return

            # Crear resumen
            lineas_consolidadas = {}
            lineas_inconsistentes = []

            for tema, consistencia in lineas:
                if consistencia >= 0.7:
                    lineas_consolidadas[tema] = consistencia
                elif consistencia < 0.5:
                    lineas_inconsistentes.append(tema)

            # Actualizar perfil
            self.cursor.execute("""
            UPDATE perfiles_judiciales_argentinos
            SET
                lineas_consolidadas = ?,
                lineas_inconsistentes = ?
            WHERE juez = ?
            """, (
                json.dumps(lineas_consolidadas, ensure_ascii=False),
                json.dumps(lineas_inconsistentes, ensure_ascii=False),
                juez
            ))

            self.conn.commit()
            print_success(f"Perfil actualizado con {len(lineas_consolidadas)} líneas consolidadas")

        except sqlite3.Error as e:
            print_error(f"Error al actualizar perfil: {e}")

    def analizar_todos_los_jueces(self, min_sentencias: int = 2) -> Dict:
        """
        Analiza líneas de todos los jueces

        Returns:
            Estadísticas totales
        """
        print(f"\n{Colors.BOLD}{'='*70}")
        print("ANÁLISIS DE LÍNEAS - TODOS LOS JUECES")
        print(f"{'='*70}{Colors.ENDC}\n")

        # Obtener todos los jueces con sentencias
        self.cursor.execute("""
        SELECT DISTINCT juez
        FROM sentencias_por_juez_arg
        WHERE perfil_cognitivo IS NOT NULL
        """)

        jueces = [row[0] for row in self.cursor.fetchall()]

        if not jueces:
            print_error("No hay jueces con sentencias analizadas")
            return {'total_jueces': 0, 'total_lineas': 0}

        print_info(f"Jueces a procesar: {len(jueces)}")

        # Procesar cada juez
        total_lineas = 0
        for juez in jueces:
            try:
                stats = self.analizar_juez_completo(juez, min_sentencias)
                total_lineas += stats['guardadas']
            except Exception as e:
                print_error(f"Error procesando {juez}: {e}")

        # Resumen final
        print(f"\n{Colors.BOLD}{'='*70}")
        print("RESUMEN FINAL")
        print(f"{'='*70}{Colors.ENDC}")
        print(f"Jueces procesados: {len(jueces)}")
        print(f"{Colors.OKGREEN}Total líneas identificadas: {total_lineas}{Colors.ENDC}\n")

        return {
            'total_jueces': len(jueces),
            'total_lineas': total_lineas
        }


def main():
    """Función principal"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Analizador de líneas jurisprudenciales'
    )
    parser.add_argument(
        'juez',
        nargs='?',
        help='Nombre del juez a analizar'
    )
    parser.add_argument(
        '--todos',
        action='store_true',
        help='Analizar todos los jueces'
    )
    parser.add_argument(
        '--min-sentencias',
        type=int,
        default=2,
        help='Mínimo de sentencias para considerar una línea (default: 2)'
    )

    args = parser.parse_args()

    # Crear analizador
    try:
        analizador = AnalizadorLineasJurisprudenciales()
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)

    try:
        if args.todos:
            stats = analizador.analizar_todos_los_jueces(args.min_sentencias)
            sys.exit(0)

        elif args.juez:
            stats = analizador.analizar_juez_completo(args.juez, args.min_sentencias)
            sys.exit(0)

        else:
            parser.print_help()
            sys.exit(1)

    finally:
        analizador.cerrar_bd()


if __name__ == "__main__":
    main()
