#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 AGREGADOR DE PERFILES DE JUECES v1.0
========================================

Agrega análisis de múltiples sentencias para crear un perfil consolidado del juez.

Funcionalidades:
- Promedia métricas de análisis judicial
- Identifica patrones consistentes
- Detecta temas recurrentes
- Calcula scores agregados
- Actualiza perfil en BD

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import Counter
import statistics

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

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")


class AgregadorPerfilesJueces:
    """
    Agrega análisis de múltiples sentencias para consolidar perfiles de jueces
    """

    def __init__(self, db_path: Path = DB_FILE):
        """Inicializa el agregador"""
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
        Obtiene todas las sentencias analizadas de un juez

        Returns:
            Lista de diccionarios con análisis
        """
        self.cursor.execute("""
        SELECT sentencia_id, perfil_cognitivo, materia, fecha_sentencia
        FROM sentencias_por_juez_arg
        WHERE juez = ? AND perfil_cognitivo IS NOT NULL
        """, (juez,))

        sentencias = []
        for row in self.cursor.fetchall():
            sent_id, perfil_json, materia, fecha = row
            try:
                perfil = json.loads(perfil_json)
                sentencias.append({
                    'sentencia_id': sent_id,
                    'perfil': perfil,
                    'materia': materia,
                    'fecha': fecha
                })
            except json.JSONDecodeError:
                continue

        return sentencias

    def promediar_diccionario(self, valores_list: List[Dict]) -> Dict[str, float]:
        """
        Promedia valores de múltiples diccionarios

        Args:
            valores_list: Lista de diccionarios con valores numéricos

        Returns:
            Diccionario con promedios
        """
        if not valores_list:
            return {}

        # Obtener todas las claves
        todas_claves = set()
        for d in valores_list:
            todas_claves.update(d.keys())

        # Calcular promedios
        promedios = {}
        for clave in todas_claves:
            valores = [d.get(clave, 0.0) for d in valores_list if clave in d]
            if valores:
                promedios[clave] = round(statistics.mean(valores), 3)

        return promedios

    def moda_con_conteos(self, valores: List) -> tuple:
        """
        Calcula la moda y su frecuencia

        Returns:
            Tupla (valor_moda, frecuencia)
        """
        if not valores:
            return (None, 0)

        counter = Counter(valores)
        moda = counter.most_common(1)[0]
        return moda

    def agregar_perfil_judicial(self, sentencias: List[Dict]) -> Dict:
        """
        Agrega análisis judicial de múltiples sentencias

        Returns:
            Diccionario con métricas agregadas
        """
        if not sentencias:
            return {}

        perfiles_judiciales = []
        for sent in sentencias:
            perfil = sent.get('perfil', {})
            judicial = perfil.get('analisis_judicial', {})
            if judicial:
                perfiles_judiciales.append(judicial)

        if not perfiles_judiciales:
            return {}

        # Promediar métricas numéricas
        agregado = {}

        # Activismo
        activismos = [p.get('tendencia_activismo', 0.0) for p in perfiles_judiciales]
        if activismos:
            agregado['tendencia_activismo'] = round(statistics.mean(activismos), 3)

        # Formalismo
        formalismos = [p.get('formalismo_vs_sustancialismo', 0.0) for p in perfiles_judiciales]
        if formalismos:
            agregado['formalismo_vs_sustancialismo'] = round(statistics.mean(formalismos), 3)

        # Protección general de derechos
        protecciones = [p.get('proteccion_general', 0.0) for p in perfiles_judiciales]
        if protecciones:
            agregado['proteccion_derechos_fundamentales'] = round(statistics.mean(protecciones), 3)

        # Deferencia
        def_leg = [p.get('deferencia_legislativo', 0.0) for p in perfiles_judiciales]
        if def_leg:
            agregado['deferencia_legislativo'] = round(statistics.mean(def_leg), 3)

        def_ej = [p.get('deferencia_ejecutivo', 0.0) for p in perfiles_judiciales]
        if def_ej:
            agregado['deferencia_ejecutivo'] = round(statistics.mean(def_ej), 3)

        # Derechos específicos (promediar todos)
        derechos_por_sentencia = [p.get('derechos_protegidos', {}) for p in perfiles_judiciales]
        agregado['derechos_protegidos'] = self.promediar_diccionario(derechos_por_sentencia)

        # Tests aplicados (promediar)
        tests_por_sentencia = [p.get('tests_aplicados', {}) for p in perfiles_judiciales]
        agregado['tests_aplicados'] = self.promediar_diccionario(tests_por_sentencia)

        # In dubio pro (promediar)
        indubio_por_sentencia = [p.get('in_dubio_pro_aplicado', {}) for p in perfiles_judiciales]
        agregado['in_dubio_pro'] = self.promediar_diccionario(indubio_por_sentencia)

        # Sesgos (promediar)
        sesgos_por_sentencia = [p.get('sesgos_detectados', {}) for p in perfiles_judiciales]
        agregado['sesgos'] = self.promediar_diccionario(sesgos_por_sentencia)

        # Interpretación normativa (moda)
        interpretaciones = [p.get('interpretacion_normativa') for p in perfiles_judiciales if p.get('interpretacion_normativa')]
        if interpretaciones:
            interp_dominante, _ = self.moda_con_conteos(interpretaciones)
            agregado['interpretacion_normativa'] = interp_dominante

        # Estándar probatorio (moda)
        estandares = [p.get('estandar_prueba') for p in perfiles_judiciales if p.get('estandar_prueba')]
        if estandares:
            estandar_dominante, _ = self.moda_con_conteos(estandares)
            agregado['estandar_prueba_preferido'] = estandar_dominante

        # Sesgo dominante (moda)
        sesgos_dom = [p.get('sesgo_dominante') for p in perfiles_judiciales if p.get('sesgo_dominante')]
        if sesgos_dom:
            sesgo_moda, _ = self.moda_con_conteos(sesgos_dom)
            agregado['sesgo_dominante'] = sesgo_moda

        # Fuentes citadas (promediar)
        fuentes_por_sentencia = [p.get('fuentes_citadas', {}) for p in perfiles_judiciales]
        agregado['fuentes'] = self.promediar_diccionario(fuentes_por_sentencia)

        return agregado

    def agregar_perfil_cognitivo(self, sentencias: List[Dict]) -> Dict:
        """
        Agrega análisis cognitivo de múltiples sentencias

        Returns:
            Diccionario con métricas agregadas
        """
        perfiles_cognitivos = []
        for sent in sentencias:
            perfil = sent.get('perfil', {})
            cognitivo = perfil.get('analisis_cognitivo')
            if cognitivo:
                perfiles_cognitivos.append(cognitivo)

        if not perfiles_cognitivos:
            return {}

        # Este análisis depende de la estructura del ANALYSER v2.0
        # Por ahora, retornar estructura básica
        return {
            'cantidad_analisis': len(perfiles_cognitivos)
        }

    def identificar_temas_recurrentes(self, sentencias: List[Dict], top_n: int = 10) -> List[str]:
        """
        Identifica los temas más recurrentes en las sentencias del juez

        Returns:
            Lista de temas ordenados por frecuencia
        """
        materias = [s.get('materia') for s in sentencias if s.get('materia')]

        if not materias:
            return []

        counter = Counter(materias)
        return [tema for tema, _ in counter.most_common(top_n)]

    def calcular_confianza_perfil(self, n_sentencias: int) -> float:
        """
        Calcula un score de confianza del perfil basado en cantidad de sentencias

        Returns:
            Float entre 0 y 1
        """
        if n_sentencias == 0:
            return 0.0
        elif n_sentencias == 1:
            return 0.3
        elif n_sentencias < 5:
            return 0.5
        elif n_sentencias < 10:
            return 0.7
        elif n_sentencias < 20:
            return 0.85
        else:
            return 1.0

    def actualizar_perfil_juez(self, juez: str) -> bool:
        """
        Actualiza el perfil completo de un juez en la BD

        Args:
            juez: Nombre del juez

        Returns:
            True si se actualizó exitosamente
        """
        print(f"\n{Colors.BOLD}Agregando perfil para: {juez}{Colors.ENDC}")

        # 1. Obtener todas las sentencias
        print_info("Obteniendo sentencias...")
        sentencias = self.obtener_sentencias_juez(juez)

        if not sentencias:
            print_error("No hay sentencias analizadas para este juez")
            return False

        print_success(f"Sentencias encontradas: {len(sentencias)}")

        # 2. Agregar perfiles
        print_info("Agregando análisis judicial...")
        perfil_judicial_agregado = self.agregar_perfil_judicial(sentencias)

        print_info("Agregando análisis cognitivo...")
        perfil_cognitivo_agregado = self.agregar_perfil_cognitivo(sentencias)

        # 3. Temas recurrentes
        temas = self.identificar_temas_recurrentes(sentencias)

        # 4. Confianza
        confianza = self.calcular_confianza_perfil(len(sentencias))

        # 5. Actualizar BD
        print_info("Actualizando base de datos...")
        try:
            # Extraer valores del perfil judicial agregado
            valores = perfil_judicial_agregado

            self.cursor.execute("""
            UPDATE perfiles_judiciales_argentinos
            SET
                total_sentencias_analizadas = ?,
                tendencia_activismo = ?,
                interpretacion_normativa = ?,
                formalismo_vs_sustancialismo = ?,
                proteccion_derechos_fundamentales = ?,
                deferencia_legislativo = ?,
                deferencia_ejecutivo = ?,
                estandar_prueba_preferido = ?,
                temas_recurrentes = ?,
                confianza_perfil = ?,
                ultima_actualizacion = ?,
                version_analyser = ?
            WHERE juez = ?
            """, (
                len(sentencias),
                valores.get('tendencia_activismo'),
                valores.get('interpretacion_normativa'),
                valores.get('formalismo_vs_sustancialismo'),
                valores.get('proteccion_derechos_fundamentales'),
                valores.get('deferencia_legislativo'),
                valores.get('deferencia_ejecutivo'),
                valores.get('estandar_prueba_preferido'),
                json.dumps(temas, ensure_ascii=False),
                confianza,
                datetime.now().isoformat(),
                '1.0-agregado',
                juez
            ))

            self.conn.commit()
            print_success(f"Perfil actualizado exitosamente")
            print_info(f"  - Sentencias: {len(sentencias)}")
            print_info(f"  - Confianza: {confianza:.2f}")
            print_info(f"  - Temas: {', '.join(temas[:3]) if temas else 'N/A'}")

            return True

        except sqlite3.Error as e:
            print_error(f"Error al actualizar perfil: {e}")
            self.conn.rollback()
            return False

    def agregar_todos_los_jueces(self) -> Dict:
        """
        Agrega perfiles de todos los jueces que tienen sentencias

        Returns:
            Estadísticas del procesamiento
        """
        print(f"\n{Colors.BOLD}{'='*70}")
        print("AGREGACIÓN DE PERFILES - TODOS LOS JUECES")
        print(f"{'='*70}{Colors.ENDC}\n")

        # Obtener todos los jueces con sentencias analizadas
        self.cursor.execute("""
        SELECT DISTINCT juez
        FROM sentencias_por_juez_arg
        WHERE perfil_cognitivo IS NOT NULL
        """)

        jueces = [row[0] for row in self.cursor.fetchall()]

        if not jueces:
            print_error("No hay jueces con sentencias analizadas")
            return {'total': 0, 'exitosos': 0, 'fallidos': 0}

        print_info(f"Jueces a procesar: {len(jueces)}")

        # Procesar cada juez
        exitosos = 0
        fallidos = 0

        for juez in jueces:
            try:
                if self.actualizar_perfil_juez(juez):
                    exitosos += 1
                else:
                    fallidos += 1
            except Exception as e:
                print_error(f"Error procesando {juez}: {e}")
                fallidos += 1

        # Resumen
        print(f"\n{Colors.BOLD}{'='*70}")
        print("RESUMEN")
        print(f"{'='*70}{Colors.ENDC}")
        print(f"Total: {len(jueces)}")
        print(f"{Colors.OKGREEN}Exitosos: {exitosos}{Colors.ENDC}")
        print(f"{Colors.FAIL}Fallidos: {fallidos}{Colors.ENDC}\n")

        return {
            'total': len(jueces),
            'exitosos': exitosos,
            'fallidos': fallidos
        }


def main():
    """Función principal"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Agregador de perfiles de jueces'
    )
    parser.add_argument(
        'juez',
        nargs='?',
        help='Nombre del juez a procesar'
    )
    parser.add_argument(
        '--todos',
        action='store_true',
        help='Agregar perfiles de todos los jueces'
    )

    args = parser.parse_args()

    # Crear agregador
    try:
        agregador = AgregadorPerfilesJueces()
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)

    try:
        if args.todos:
            # Procesar todos
            stats = agregador.agregar_todos_los_jueces()
            sys.exit(0 if stats['fallidos'] == 0 else 1)

        elif args.juez:
            # Procesar un juez
            if agregador.actualizar_perfil_juez(args.juez):
                sys.exit(0)
            else:
                sys.exit(1)

        else:
            # Sin argumentos
            parser.print_help()
            sys.exit(1)

    finally:
        agregador.cerrar_bd()


if __name__ == "__main__":
    main()
