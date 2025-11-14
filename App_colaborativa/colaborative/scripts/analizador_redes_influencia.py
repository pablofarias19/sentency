#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 ANALIZADOR DE REDES DE INFLUENCIA JUDICIAL v1.0
==================================================

Construye y analiza redes de influencia entre jueces basándose en citas.

Funcionalidades:
- Extrae citas de todas las sentencias
- Construye relaciones juez→juez / juez→autor
- Calcula métricas de red
- Identifica jueces más influyentes
- Guarda en tabla redes_influencia_judicial

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import Counter, defaultdict

from extractor_citas_jurisprudenciales import ExtractorCitasJurisprudenciales

# Importar configuración centralizada
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DATABASE_PATH as DB_FILE, BASES_RAG_DIR

# Configuración
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


class AnalizadorRedesInfluencia:
    """
    Construye y analiza redes de influencia judicial
    """

    def __init__(self, db_path: Path = DB_FILE):
        """Inicializa el analizador"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.extractor_citas = ExtractorCitasJurisprudenciales()
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
        """Obtiene sentencias de un juez"""
        self.cursor.execute("""
        SELECT sentencia_id, texto_completo
        FROM sentencias_por_juez_arg
        WHERE juez = ? AND texto_completo IS NOT NULL
        """, (juez,))

        sentencias = []
        for row in self.cursor.fetchall():
            sentencias.append({
                'sentencia_id': row[0],
                'texto': row[1]
            })

        return sentencias

    def extraer_citas_juez(self, juez: str) -> Dict:
        """
        Extrae todas las citas de las sentencias de un juez

        Returns:
            Diccionario con citas consolidadas
        """
        print_info(f"Extrayendo citas de {juez}...")

        sentencias = self.obtener_sentencias_juez(juez)

        if not sentencias:
            print_warning(f"  No hay sentencias para {juez}")
            return {}

        # Consolidar citas de todas las sentencias
        citas_csjn_total = []
        citas_camaras_total = []
        citas_doctrinales_total = []

        for sent in sentencias:
            citas = self.extractor_citas.extraer_todas_citas(sent['texto'])
            citas_csjn_total.extend(citas['citas_csjn'])
            citas_camaras_total.extend(citas['citas_camaras'])
            citas_doctrinales_total.extend(citas['citas_doctrinales'])

        # Contar frecuencias
        tribunales_counter = Counter()
        autores_counter = Counter()

        for cita in citas_csjn_total:
            tribunales_counter['CSJN'] += 1

        for cita in citas_camaras_total:
            if cita.tribunal:
                key = f"{cita.tribunal} - Sala {cita.sala}" if cita.sala else cita.tribunal
                tribunales_counter[key] += 1

        for cita in citas_doctrinales_total:
            autores_counter[cita.autor] += 1

        print_success(f"  Citas encontradas: {len(citas_csjn_total)} CSJN, {len(citas_camaras_total)} Cámaras, {len(citas_doctrinales_total)} doctrinales")

        return {
            'juez': juez,
            'tribunales': dict(tribunales_counter),
            'autores': dict(autores_counter),
            'total_citas': len(citas_csjn_total) + len(citas_camaras_total) + len(citas_doctrinales_total)
        }

    def guardar_relaciones(self, juez_origen: str, citas_data: Dict) -> int:
        """
        Guarda las relaciones de influencia en la BD

        Returns:
            Cantidad de relaciones guardadas
        """
        guardadas = 0

        # Limpiar relaciones antiguas
        self.cursor.execute("DELETE FROM redes_influencia_judicial WHERE juez_origen = ?", (juez_origen,))

        # Guardar citas a tribunales
        for tribunal, cantidad in citas_data.get('tribunales', {}).items():
            tipo_destino = 'csjn' if tribunal == 'CSJN' else 'tribunal_superior'

            try:
                self.cursor.execute("""
                INSERT INTO redes_influencia_judicial (
                    juez_origen,
                    juez_destino,
                    tipo_destino,
                    tipo_influencia,
                    intensidad,
                    cantidad_citas,
                    fecha_primera_cita,
                    fecha_ultima_cita
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    juez_origen,
                    tribunal,
                    tipo_destino,
                    'cita_literal',
                    min(1.0, cantidad / 10.0),  # Normalizar intensidad
                    cantidad,
                    datetime.now().date().isoformat(),
                    datetime.now().date().isoformat()
                ))
                guardadas += 1
            except sqlite3.Error:
                pass

        # Guardar citas a autores
        for autor, cantidad in citas_data.get('autores', {}).items():
            try:
                self.cursor.execute("""
                INSERT INTO redes_influencia_judicial (
                    juez_origen,
                    juez_destino,
                    tipo_destino,
                    tipo_influencia,
                    intensidad,
                    cantidad_citas,
                    fecha_primera_cita,
                    fecha_ultima_cita
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    juez_origen,
                    autor,
                    'autor_doctrinal',
                    'cita_literal',
                    min(1.0, cantidad / 5.0),
                    cantidad,
                    datetime.now().date().isoformat(),
                    datetime.now().date().isoformat()
                ))
                guardadas += 1
            except sqlite3.Error:
                pass

        self.conn.commit()
        return guardadas

    def analizar_juez(self, juez: str) -> Dict:
        """
        Analiza la red de influencias de un juez

        Returns:
            Estadísticas
        """
        print(f"\n{Colors.BOLD}Analizando red de: {juez}{Colors.ENDC}")

        # Extraer citas
        citas_data = self.extraer_citas_juez(juez)

        if not citas_data:
            return {'juez': juez, 'relaciones': 0}

        # Guardar relaciones
        relaciones = self.guardar_relaciones(juez, citas_data)

        print_success(f"  Relaciones guardadas: {relaciones}")

        return {
            'juez': juez,
            'relaciones': relaciones,
            'total_citas': citas_data.get('total_citas', 0)
        }

    def analizar_todos_los_jueces(self) -> Dict:
        """Analiza la red de todos los jueces"""
        print(f"\n{Colors.BOLD}{'='*70}")
        print("ANÁLISIS DE REDES DE INFLUENCIA - TODOS LOS JUECES")
        print(f"{'='*70}{Colors.ENDC}\n")

        # Obtener todos los jueces
        self.cursor.execute("""
        SELECT DISTINCT juez
        FROM sentencias_por_juez_arg
        WHERE texto_completo IS NOT NULL
        """)

        jueces = [row[0] for row in self.cursor.fetchall()]

        if not jueces:
            print_error("No hay jueces con sentencias")
            return {'total': 0, 'relaciones': 0}

        print_info(f"Jueces a analizar: {len(jueces)}")

        # Analizar cada juez
        total_relaciones = 0
        for juez in jueces:
            try:
                stats = self.analizar_juez(juez)
                total_relaciones += stats.get('relaciones', 0)
            except Exception as e:
                print_error(f"Error procesando {juez}: {e}")

        # Resumen
        print(f"\n{Colors.BOLD}{'='*70}")
        print("RESUMEN")
        print(f"{'='*70}{Colors.ENDC}")
        print(f"Jueces analizados: {len(jueces)}")
        print(f"{Colors.OKGREEN}Total relaciones: {total_relaciones}{Colors.ENDC}\n")

        return {
            'total_jueces': len(jueces),
            'total_relaciones': total_relaciones
        }


def main():
    """Función principal"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Analizador de redes de influencia judicial'
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

    args = parser.parse_args()

    # Crear analizador
    try:
        analizador = AnalizadorRedesInfluencia()
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)

    try:
        if args.todos:
            stats = analizador.analizar_todos_los_jueces()
            sys.exit(0)

        elif args.juez:
            stats = analizador.analizar_juez(args.juez)
            sys.exit(0)

        else:
            parser.print_help()
            sys.exit(1)

    finally:
        analizador.cerrar_bd()


if __name__ == "__main__":
    main()
