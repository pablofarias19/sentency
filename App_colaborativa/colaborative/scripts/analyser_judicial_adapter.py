#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 ADAPTADOR: ANALYSER COGNITIVO → SISTEMA JUDICIAL
====================================================

Conecta el ANALYSER v2.0 (analyser_metodo_mejorado.py) con el sistema judicial.

FUNCIÓN:
- Toma el ANALYSER cognitivo existente (robusto y funcional)
- Lo adapta para trabajar con JUECES en lugar de AUTORES
- Guarda resultados en juez_centrico_arg.db en lugar de autor_centrico.db
- Mantiene TODA la funcionalidad de análisis cognitivo

INTEGRACIÓN:
- analyser_metodo_mejorado.py (motor cognitivo)
- juez_centrico_arg.db (base judicial)
- analizador_pensamiento_judicial_arg.py (análisis judicial)

AUTOR: Sistema Judicial Argentina
FECHA: 12 NOV 2025
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import asdict

# Importar ANALYSER cognitivo original
try:
    from analyser_metodo_mejorado import AnalyserMetodoMejorado
    ANALYSER_DISPONIBLE = True
except ImportError:
    print("⚠️ ANALYSER v2.0 no disponible")
    ANALYSER_DISPONIBLE = False

# Importar analizador judicial
from analizador_pensamiento_judicial_arg import AnalizadorPensamientoJudicialArg

# Configuración
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
BASES_RAG_DIR = BASE_DIR / "bases_rag" / "cognitiva"
DB_JUDICIAL = BASES_RAG_DIR / "juez_centrico_arg.db"


class AnalyserJudicialAdapter:
    """
    Adaptador que conecta ANALYSER cognitivo con sistema judicial

    MANTIENE: Todo el análisis cognitivo del ANALYSER original
    ADAPTA: Referencias de autores → jueces, textos → sentencias
    INTEGRA: Análisis judicial específico argentino
    """

    def __init__(self, db_path: Path = DB_JUDICIAL):
        """Inicializa adaptador"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None

        # Motor cognitivo (el original, sin modificar)
        if ANALYSER_DISPONIBLE:
            self.analyser_cognitivo = AnalyserMetodoMejorado()
        else:
            self.analyser_cognitivo = None

        # Analizador judicial argentino
        self.analizador_judicial = AnalizadorPensamientoJudicialArg()

        # Conectar BD
        self.conectar_bd()

    def conectar_bd(self):
        """Conecta a BD judicial"""
        if not self.db_path.exists():
            raise FileNotFoundError(f"BD judicial no encontrada: {self.db_path}")

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def analizar_sentencia(self, texto: str, metadata: Dict = None) -> Dict:
        """
        Analiza una sentencia con ambos motores

        Args:
            texto: Texto completo de la sentencia
            metadata: Metadata de la sentencia (juez, expediente, etc.)

        Returns:
            Dict con análisis cognitivo + judicial
        """
        resultado = {
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }

        # 1. ANÁLISIS COGNITIVO (ANALYSER v2.0)
        if self.analyser_cognitivo:
            try:
                # El ANALYSER funciona igual, solo cambiamos cómo guardamos
                analisis_cog = self.analyser_cognitivo.analizar_documento(
                    texto=texto,
                    tipo_documento='sentencia'  # En lugar de 'ensayo' o 'artículo'
                )
                resultado['analisis_cognitivo'] = analisis_cog
            except Exception as e:
                print(f"⚠️ Error en análisis cognitivo: {e}")
                resultado['analisis_cognitivo'] = None

        # 2. ANÁLISIS JUDICIAL ARGENTINO (específico)
        try:
            analisis_jud = self.analizador_judicial.analizar(texto)
            resultado['analisis_judicial'] = asdict(analisis_jud)
        except Exception as e:
            print(f"⚠️ Error en análisis judicial: {e}")
            resultado['analisis_judicial'] = None

        return resultado

    def guardar_analisis_en_perfil(self, juez: str, analisis: Dict) -> bool:
        """
        Guarda análisis en el perfil del juez

        ADAPTA: En lugar de guardar en tabla de autores,
                guarda en perfiles_judiciales_argentinos
        """
        try:
            # Extraer métricas del análisis cognitivo
            cog = analisis.get('analisis_cognitivo', {})
            jud = analisis.get('analisis_judicial', {})

            # Preparar campos a actualizar
            campos_actualizar = {}

            # Del análisis cognitivo
            if cog:
                # Razonamiento
                if 'razonamiento' in cog:
                    campos_actualizar['razonamiento_dominante'] = cog['razonamiento'].get('tipo_dominante')
                    campos_actualizar['densidad_razonamiento'] = cog['razonamiento'].get('densidad_total', 0)

                # Modalidad epistémica
                if 'modalidad_epistemica' in cog:
                    campos_actualizar['modalidad_epistemica'] = cog['modalidad_epistemica'].get('dominante')

                # Retórica
                if 'retorica' in cog:
                    ret = cog['retorica']
                    campos_actualizar['uso_ethos'] = ret.get('ethos', 0)
                    campos_actualizar['uso_pathos'] = ret.get('pathos', 0)
                    campos_actualizar['uso_logos'] = ret.get('logos', 0)

                # Estilo
                if 'estilo' in cog:
                    campos_actualizar['estilo_literario'] = cog['estilo'].get('dominante')

                # Fuentes
                if 'fuentes' in cog:
                    fu = cog['fuentes']
                    campos_actualizar['densidad_citas_legislacion'] = fu.get('legislacion', 0)
                    campos_actualizar['densidad_citas_jurisprudencia'] = fu.get('jurisprudencia', 0)
                    campos_actualizar['densidad_citas_doctrina'] = fu.get('doctrina', 0)

            # Del análisis judicial
            if jud:
                campos_actualizar['tendencia_activismo'] = jud.get('activismo_score', 0)
                campos_actualizar['nivel_formalismo'] = jud.get('formalismo_score', 0)
                campos_actualizar['interpretacion_dominante'] = jud.get('interpretacion_dominante', 'N/D')
                campos_actualizar['estandar_probatorio_dominante'] = jud.get('estandar_dominante', 'N/D')

                # Protección de derechos
                derechos = jud.get('proteccion_derechos', {})
                campos_actualizar['proteccion_trabajo'] = derechos.get('trabajo', 0)
                campos_actualizar['proteccion_igualdad'] = derechos.get('igualdad', 0)
                campos_actualizar['proteccion_libertad_expresion'] = derechos.get('libertad_expresion', 0)
                campos_actualizar['proteccion_privacidad'] = derechos.get('privacidad', 0)
                campos_actualizar['proteccion_propiedad'] = derechos.get('propiedad', 0)
                campos_actualizar['proteccion_consumidor'] = derechos.get('consumidor', 0)

                # Tests y doctrinas
                tests = jud.get('tests_doctrinas', {})
                campos_actualizar['usa_test_proporcionalidad'] = tests.get('test_proporcionalidad', 0)
                campos_actualizar['usa_test_razonabilidad'] = tests.get('test_razonabilidad', 0)
                campos_actualizar['usa_in_dubio_pro_operario'] = tests.get('in_dubio_pro_operario', 0)
                campos_actualizar['usa_in_dubio_pro_consumidor'] = tests.get('in_dubio_pro_consumidor', 0)

                # Sesgos
                sesgos = jud.get('sesgos', {})
                campos_actualizar['sesgo_pro_trabajador'] = sesgos.get('pro_trabajador', 0)
                campos_actualizar['sesgo_pro_empresa'] = sesgos.get('pro_empresa', 0)
                campos_actualizar['sesgo_garantista'] = sesgos.get('garantista', 0)
                campos_actualizar['sesgo_punitivista'] = sesgos.get('punitivista', 0)
                campos_actualizar['sesgo_pro_consumidor'] = sesgos.get('pro_consumidor', 0)

            # Construir query de actualización
            if campos_actualizar:
                set_clause = ", ".join([f"{k} = ?" for k in campos_actualizar.keys()])
                valores = list(campos_actualizar.values()) + [juez]

                query = f"""
                UPDATE perfiles_judiciales_argentinos
                SET {set_clause},
                    fecha_ultima_actualizacion = CURRENT_TIMESTAMP
                WHERE juez = ?
                """

                self.cursor.execute(query, valores)
                self.conn.commit()

                return True

            return False

        except Exception as e:
            print(f"❌ Error guardando análisis: {e}")
            return False

    def procesar_juez(self, juez: str, sentencias_ids: List[str] = None) -> Dict:
        """
        Procesa todas las sentencias de un juez

        Args:
            juez: Nombre del juez
            sentencias_ids: Lista de IDs de sentencias a procesar (None = todas)

        Returns:
            Dict con estadísticas del procesamiento
        """
        # Obtener sentencias del juez
        if sentencias_ids:
            placeholders = ",".join(["?"] * len(sentencias_ids))
            query = f"""
            SELECT sentencia_id, texto_completo, metadata
            FROM sentencias_por_juez_arg
            WHERE juez = ? AND sentencia_id IN ({placeholders})
            """
            self.cursor.execute(query, [juez] + sentencias_ids)
        else:
            query = """
            SELECT sentencia_id, texto_completo, metadata
            FROM sentencias_por_juez_arg
            WHERE juez = ?
            """
            self.cursor.execute(query, (juez,))

        sentencias = self.cursor.fetchall()

        stats = {
            'juez': juez,
            'total_sentencias': len(sentencias),
            'procesadas': 0,
            'errores': 0
        }

        # Procesar cada sentencia
        for sent_id, texto, metadata_json in sentencias:
            try:
                metadata = json.loads(metadata_json) if metadata_json else {}

                # Analizar
                analisis = self.analizar_sentencia(texto, metadata)

                # Guardar en perfil
                self.guardar_analisis_en_perfil(juez, analisis)

                stats['procesadas'] += 1

            except Exception as e:
                print(f"❌ Error procesando {sent_id}: {e}")
                stats['errores'] += 1

        return stats

    def obtener_perfil_completo(self, juez: str) -> Optional[Dict]:
        """
        Obtiene perfil completo del juez

        Devuelve mismo formato que el sistema de autores,
        pero para jueces
        """
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

    def listar_jueces(self) -> List[Dict]:
        """
        Lista todos los jueces en el sistema

        Equivalente a listar_autores() del sistema antiguo
        """
        self.cursor.execute("""
        SELECT
            juez,
            tipo_entidad,
            fuero,
            jurisdiccion,
            tribunal,
            total_sentencias,
            confianza_analisis
        FROM perfiles_judiciales_argentinos
        ORDER BY total_sentencias DESC
        """)

        jueces = []
        for row in self.cursor.fetchall():
            jueces.append({
                'nombre': row[0],
                'tipo': row[1],
                'fuero': row[2],
                'jurisdiccion': row[3],
                'tribunal': row[4],
                'sentencias': row[5],
                'confianza': row[6]
            })

        return jueces

    def buscar_jueces(self, termino: str, fuero: str = None) -> List[Dict]:
        """
        Busca jueces por nombre o fuero

        Equivalente a buscar_autores() del sistema antiguo
        """
        query = """
        SELECT juez, tipo_entidad, fuero, total_sentencias
        FROM perfiles_judiciales_argentinos
        WHERE juez LIKE ?
        """
        params = [f"%{termino}%"]

        if fuero:
            query += " AND fuero = ?"
            params.append(fuero)

        query += " ORDER BY total_sentencias DESC LIMIT 20"

        self.cursor.execute(query, params)

        resultados = []
        for row in self.cursor.fetchall():
            resultados.append({
                'nombre': row[0],
                'tipo': row[1],
                'fuero': row[2],
                'sentencias': row[3]
            })

        return resultados

    def cerrar(self):
        """Cierra conexión a BD"""
        if self.conn:
            self.conn.close()


# ============================================================================
# API DE COMPATIBILIDAD CON SISTEMA ANTIGUO
# ============================================================================

class BibliotecaJudicial(AnalyserJudicialAdapter):
    """
    Alias compatible con BibliotecaCognitiva del sistema antiguo

    Permite que el código existente funcione sin cambios:
    - BibliotecaCognitiva() → BibliotecaJudicial()
    - autor → juez
    - texto → sentencia
    """

    def analizar_autor(self, nombre: str):
        """Compatibilidad: analizar_autor → procesar_juez"""
        return self.procesar_juez(nombre)

    def obtener_perfil_autor(self, nombre: str):
        """Compatibilidad: obtener_perfil_autor → obtener_perfil_completo"""
        return self.obtener_perfil_completo(nombre)

    def listar_autores(self):
        """Compatibilidad: listar_autores → listar_jueces"""
        return self.listar_jueces()


def main():
    """Ejemplo de uso"""
    import sys

    if len(sys.argv) < 2:
        print("Uso: python analyser_judicial_adapter.py <nombre_juez>")
        sys.exit(1)

    juez = sys.argv[1]

    # Crear adaptador
    adaptador = AnalyserJudicialAdapter()

    # Procesar juez
    print(f"\n🔄 Procesando juez: {juez}")
    stats = adaptador.procesar_juez(juez)

    print(f"\n✅ Resultados:")
    print(f"   Sentencias procesadas: {stats['procesadas']}/{stats['total_sentencias']}")
    print(f"   Errores: {stats['errores']}")

    # Mostrar perfil
    perfil = adaptador.obtener_perfil_completo(juez)
    if perfil:
        print(f"\n📊 Perfil del juez:")
        print(f"   Activismo: {perfil.get('tendencia_activismo', 'N/D')}")
        print(f"   Formalismo: {perfil.get('nivel_formalismo', 'N/D')}")
        print(f"   Interpretación: {perfil.get('interpretacion_dominante', 'N/D')}")

    adaptador.cerrar()


if __name__ == "__main__":
    main()
