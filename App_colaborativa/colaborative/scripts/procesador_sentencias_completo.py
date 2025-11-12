#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 PROCESADOR COMPLETO DE SENTENCIAS v1.0
==========================================

Procesa sentencias completas aplicando:
1. Análisis cognitivo (ANALYSER v2.0)
2. Análisis judicial argentino
3. Guardado en base de datos
4. Actualización de perfiles de jueces

INTEGRA:
- analyser_metodo_mejorado.py (análisis cognitivo)
- analizador_pensamiento_judicial_arg.py (análisis judicial)
- Base de datos judicial argentina

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple

# Imports locales
from analizador_pensamiento_judicial_arg import AnalizadorPensamientoJudicialArg, AnalisisJudicial
from dataclasses import asdict

# Intentar importar ANALYSER v2.0
try:
    from analyser_metodo_mejorado import AnalyserMetodoMejorado
    ANALYSER_DISPONIBLE = True
except ImportError:
    print("⚠️ Advertencia: ANALYSER v2.0 no disponible. Solo se usará análisis judicial.")
    ANALYSER_DISPONIBLE = False

# Configuración
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
BASES_RAG_DIR = BASE_DIR / "bases_rag" / "cognitiva"
DB_FILE = BASES_RAG_DIR / "juez_centrico_arg.db"

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


class ProcesadorSentenciasCompleto:
    """
    Procesador completo que integra análisis cognitivo y judicial
    """

    def __init__(self, db_path: Path = DB_FILE):
        """Inicializa el procesador"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None

        # Inicializar analizadores
        self.analizador_judicial = AnalizadorPensamientoJudicialArg()

        if ANALYSER_DISPONIBLE:
            self.analyser_cognitivo = AnalyserMetodoMejorado()
            print_success("ANALYSER v2.0 cargado")
        else:
            self.analyser_cognitivo = None

        # Conectar a BD
        self.conectar_bd()

    def conectar_bd(self):
        """Conecta a la base de datos"""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Base de datos no encontrada: {self.db_path}")

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print_success(f"Conectado a: {self.db_path}")

    def cerrar_bd(self):
        """Cierra la conexión"""
        if self.conn:
            self.conn.close()

    def obtener_sentencia(self, sentencia_id: str) -> Optional[Tuple[str, str, str]]:
        """
        Obtiene una sentencia de la BD

        Returns:
            Tupla (texto_completo, juez, materia) o None
        """
        self.cursor.execute("""
        SELECT texto_completo, juez, materia
        FROM sentencias_por_juez_arg
        WHERE sentencia_id = ?
        """, (sentencia_id,))

        resultado = self.cursor.fetchone()
        return resultado if resultado else None

    def analizar_sentencia(self, texto: str) -> Dict:
        """
        Análisis completo de una sentencia

        Args:
            texto: Texto completo

        Returns:
            Diccionario con análisis completo
        """
        resultado = {
            'timestamp': datetime.now().isoformat(),
            'version_analyser': self.analizador_judicial.version
        }

        # 1. Análisis judicial argentino
        print_info("Ejecutando análisis judicial argentino...")
        try:
            analisis_judicial = self.analizador_judicial.analizar(texto)
            resultado['analisis_judicial'] = asdict(analisis_judicial)
            print_success("Análisis judicial completado")
        except Exception as e:
            print_error(f"Error en análisis judicial: {e}")
            resultado['analisis_judicial'] = None

        # 2. Análisis cognitivo (si está disponible)
        if self.analyser_cognitivo:
            print_info("Ejecutando análisis cognitivo (ANALYSER v2.0)...")
            try:
                analisis_cognitivo = self.analyser_cognitivo.analizar_documento(texto, "sentencia")
                resultado['analisis_cognitivo'] = analisis_cognitivo
                print_success("Análisis cognitivo completado")
            except Exception as e:
                print_error(f"Error en análisis cognitivo: {e}")
                resultado['analisis_cognitivo'] = None
        else:
            resultado['analisis_cognitivo'] = None

        return resultado

    def guardar_analisis_sentencia(self, sentencia_id: str, analisis: Dict) -> bool:
        """
        Guarda el análisis de una sentencia en la BD

        Args:
            sentencia_id: ID de la sentencia
            analisis: Diccionario con el análisis completo

        Returns:
            True si se guardó exitosamente
        """
        try:
            # Convertir análisis a JSON
            analisis_json = json.dumps(analisis, ensure_ascii=False)

            # Extraer campos específicos para columnas individuales
            judicial = analisis.get('analisis_judicial', {})

            # Razonamientos identificados
            razonamientos = []
            if analisis.get('analisis_cognitivo'):
                cog = analisis['analisis_cognitivo']
                if isinstance(cog, dict) and 'cognicion' in cog:
                    razonamientos = list(cog['cognicion'].get('razonamiento_formal', {}).keys())

            # Tests aplicados
            tests_aplicados = []
            if judicial:
                tests_aplicados = [k for k, v in judicial.get('tests_aplicados', {}).items() if v > 0.2]

            # Actualizar sentencia
            self.cursor.execute("""
            UPDATE sentencias_por_juez_arg
            SET
                perfil_cognitivo = ?,
                razonamientos_identificados = ?,
                tests_aplicados = ?,
                fecha_procesamiento = ?
            WHERE sentencia_id = ?
            """, (
                analisis_json,
                json.dumps(razonamientos, ensure_ascii=False),
                json.dumps(tests_aplicados, ensure_ascii=False),
                datetime.now().isoformat(),
                sentencia_id
            ))

            self.conn.commit()
            print_success(f"Análisis guardado para: {sentencia_id}")
            return True

        except sqlite3.Error as e:
            print_error(f"Error al guardar análisis: {e}")
            self.conn.rollback()
            return False

    def procesar_sentencia_completa(self, sentencia_id: str) -> bool:
        """
        Procesa una sentencia completa: análisis + guardado + actualización de perfil

        Args:
            sentencia_id: ID de la sentencia

        Returns:
            True si se procesó exitosamente
        """
        print(f"\n{Colors.BOLD}{'='*70}")
        print(f"PROCESANDO SENTENCIA: {sentencia_id}")
        print(f"{'='*70}{Colors.ENDC}\n")

        # 1. Obtener sentencia
        print_info("Obteniendo sentencia de la BD...")
        sentencia = self.obtener_sentencia(sentencia_id)

        if not sentencia:
            print_error(f"Sentencia no encontrada: {sentencia_id}")
            return False

        texto, juez, materia = sentencia
        print_success(f"Sentencia obtenida - Juez: {juez}, Materia: {materia}")

        # 2. Analizar
        print_info(f"Analizando sentencia ({len(texto)} caracteres)...")
        analisis = self.analizar_sentencia(texto)

        # 3. Guardar análisis
        print_info("Guardando análisis en BD...")
        if not self.guardar_analisis_sentencia(sentencia_id, analisis):
            return False

        # 4. Actualizar perfil del juez (llamar al agregador)
        print_info(f"Actualizando perfil del juez: {juez}")
        self.actualizar_perfil_juez_basico(juez, analisis)

        print(f"\n{Colors.OKGREEN}✓ SENTENCIA PROCESADA EXITOSAMENTE{Colors.ENDC}\n")
        return True

    def actualizar_perfil_juez_basico(self, juez: str, analisis: Dict):
        """
        Actualización básica del perfil del juez con datos del último análisis

        Args:
            juez: Nombre del juez
            analisis: Análisis de la sentencia
        """
        try:
            judicial = analisis.get('analisis_judicial', {})

            if not judicial:
                return

            # Actualizar campos básicos (sin agregación por ahora)
            self.cursor.execute("""
            UPDATE perfiles_judiciales_argentinos
            SET
                ultima_actualizacion = ?,
                version_analyser = ?
            WHERE juez = ?
            """, (
                datetime.now().isoformat(),
                analisis.get('version_analyser', '1.0'),
                juez
            ))

            self.conn.commit()
            print_success(f"Perfil actualizado para: {juez}")

        except sqlite3.Error as e:
            print_error(f"Error al actualizar perfil: {e}")

    def procesar_sentencias_pendientes(self, limite: int = None) -> Dict:
        """
        Procesa todas las sentencias que aún no han sido analizadas

        Args:
            limite: Límite de sentencias a procesar (None = todas)

        Returns:
            Diccionario con estadísticas
        """
        print(f"\n{Colors.BOLD}{'='*70}")
        print("PROCESAMIENTO BATCH DE SENTENCIAS")
        print(f"{'='*70}{Colors.ENDC}\n")

        # Obtener sentencias pendientes
        query = """
        SELECT sentencia_id
        FROM sentencias_por_juez_arg
        WHERE perfil_cognitivo IS NULL
        """

        if limite:
            query += f" LIMIT {limite}"

        self.cursor.execute(query)
        pendientes = [row[0] for row in self.cursor.fetchall()]

        if not pendientes:
            print_warning("No hay sentencias pendientes de procesar")
            return {'total': 0, 'exitosas': 0, 'fallidas': 0}

        print_info(f"Sentencias pendientes: {len(pendientes)}")

        # Procesar
        exitosas = 0
        fallidas = 0

        for sentencia_id in pendientes:
            try:
                if self.procesar_sentencia_completa(sentencia_id):
                    exitosas += 1
                else:
                    fallidas += 1
            except Exception as e:
                print_error(f"Error inesperado procesando {sentencia_id}: {e}")
                fallidas += 1

        # Resumen
        print(f"\n{Colors.BOLD}{'='*70}")
        print("RESUMEN DEL PROCESAMIENTO")
        print(f"{'='*70}{Colors.ENDC}")
        print(f"Total: {len(pendientes)}")
        print(f"{Colors.OKGREEN}Exitosas: {exitosas}{Colors.ENDC}")
        print(f"{Colors.FAIL}Fallidas: {fallidas}{Colors.ENDC}\n")

        return {
            'total': len(pendientes),
            'exitosas': exitosas,
            'fallidas': fallidas
        }


def main():
    """Función principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Procesador completo de sentencias (análisis cognitivo + judicial)'
    )
    parser.add_argument(
        'sentencia_id',
        nargs='?',
        help='ID de sentencia específica a procesar'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Procesar todas las sentencias pendientes'
    )
    parser.add_argument(
        '--limite',
        type=int,
        default=None,
        help='Límite de sentencias en modo batch'
    )

    args = parser.parse_args()

    # Crear procesador
    try:
        procesador = ProcesadorSentenciasCompleto()
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)

    try:
        if args.batch:
            # Modo batch
            stats = procesador.procesar_sentencias_pendientes(args.limite)
            sys.exit(0 if stats['fallidas'] == 0 else 1)

        elif args.sentencia_id:
            # Procesar una sentencia específica
            if procesador.procesar_sentencia_completa(args.sentencia_id):
                sys.exit(0)
            else:
                sys.exit(1)

        else:
            # Sin argumentos, mostrar ayuda
            parser.print_help()
            sys.exit(1)

    finally:
        procesador.cerrar_bd()


if __name__ == "__main__":
    main()
