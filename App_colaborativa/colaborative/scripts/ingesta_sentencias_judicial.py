#!/usr/bin/env python3
"""
Sistema de Análisis de Pensamiento Judicial - Argentina
Ingesta de Sentencias

Versión: 1.0
Fecha: 2025-11-12

Este script procesa sentencias argentinas:
1. Extrae texto de PDF/TXT
2. Extrae metadata automáticamente
3. Realiza chunking del texto
4. Guarda en base de datos judicial
5. Prepara para análisis cognitivo posterior
"""

import sqlite3
import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
import uuid

# Importar extractor de metadata
from extractor_metadata_argentina import ExtractorMetadataArgentina

# Configuración
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
BASES_RAG_DIR = BASE_DIR / "bases_rag" / "cognitiva"
DB_FILE = BASES_RAG_DIR / "juez_centrico_arg.db"
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
TXT_DIR = DATA_DIR / "txt"
CHUNKS_DIR = DATA_DIR / "chunks"

# Parámetros de chunking
CHUNK_TOKENS = 1000
STEP_TOKENS = 300

# Colores para terminal
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


class IngestorSentenciasJudicial:
    """
    Ingestor de sentencias para el sistema judicial argentino
    """

    def __init__(self, db_path: Path = DB_FILE):
        """Inicializa el ingestor"""
        self.db_path = db_path
        self.extractor_metadata = ExtractorMetadataArgentina()
        self.conn = None
        self.cursor = None

        # Verificar que la BD existe
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Base de datos no encontrada: {self.db_path}\n"
                f"Ejecute primero: python inicializar_bd_judicial.py"
            )

        # Conectar a BD
        self.conectar_bd()

    def conectar_bd(self):
        """Conecta a la base de datos"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print_success(f"Conectado a: {self.db_path}")

    def cerrar_bd(self):
        """Cierra la conexión a la BD"""
        if self.conn:
            self.conn.close()

    def extraer_texto(self, archivo_path: Path) -> str:
        """
        Extrae texto de PDF o TXT

        Args:
            archivo_path: Ruta al archivo

        Returns:
            Texto extraído
        """
        if archivo_path.suffix.lower() == '.txt':
            # Leer TXT directamente
            return archivo_path.read_text(encoding='utf-8', errors='ignore')

        elif archivo_path.suffix.lower() == '.pdf':
            # Verificar si ya existe el TXT
            txt_path = TXT_DIR / (archivo_path.stem + '.txt')

            if txt_path.exists():
                print_info(f"Usando TXT existente: {txt_path.name}")
                return txt_path.read_text(encoding='utf-8', errors='ignore')

            # Si no existe, extraer de PDF
            print_info(f"Extrayendo texto de PDF: {archivo_path.name}")
            try:
                # Intentar importar utilidad existente
                from utils_text_extractor import pdf_to_txt
                pdf_to_txt(archivo_path, txt_path)
                return txt_path.read_text(encoding='utf-8', errors='ignore')
            except ImportError:
                # Si no existe, usar PyPDF2 básico
                return self._extraer_pdf_basico(archivo_path)
        else:
            raise ValueError(f"Formato no soportado: {archivo_path.suffix}")

    def _extraer_pdf_basico(self, pdf_path: Path) -> str:
        """Extracción básica de PDF sin dependencias"""
        try:
            import PyPDF2
            texto = []
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    texto.append(page.extract_text())
            return '\n'.join(texto)
        except:
            print_error(f"No se pudo extraer texto de: {pdf_path}")
            return ""

    def hacer_chunks(self, texto: str) -> List[str]:
        """
        Divide el texto en chunks con overlap

        Args:
            texto: Texto completo

        Returns:
            Lista de chunks
        """
        tokens = texto.split()
        chunks = []
        i = 0

        while i < len(tokens):
            j = min(i + CHUNK_TOKENS, len(tokens))
            chunk = ' '.join(tokens[i:j])
            chunks.append(chunk)

            if j == len(tokens):
                break

            i += (CHUNK_TOKENS - STEP_TOKENS)

        return chunks

    def generar_sentencia_id(self, expediente: str = None, archivo: str = None) -> str:
        """
        Genera un ID único para la sentencia

        Args:
            expediente: Número de expediente
            archivo: Nombre de archivo

        Returns:
            ID único
        """
        if expediente:
            # Normalizar expediente
            exp_norm = expediente.replace('/', '_').replace(' ', '_')
            return f"SENT_{exp_norm}"
        elif archivo:
            # Usar hash del nombre de archivo
            hash_archivo = hashlib.sha1(archivo.encode()).hexdigest()[:12]
            return f"SENT_{hash_archivo}"
        else:
            # UUID aleatorio
            return f"SENT_{uuid.uuid4().hex[:12]}"

    def juez_existe(self, nombre_juez: str) -> bool:
        """Verifica si un juez ya existe en la BD"""
        self.cursor.execute(
            "SELECT 1 FROM perfiles_judiciales_argentinos WHERE juez = ?",
            (nombre_juez,)
        )
        return self.cursor.fetchone() is not None

    def crear_perfil_juez_basico(self, metadata: Dict):
        """
        Crea un perfil básico de juez si no existe

        Args:
            metadata: Metadata extraída de la sentencia
        """
        nombre_juez = metadata['juez']

        if self.juez_existe(nombre_juez):
            return

        print_info(f"Creando perfil básico para: {nombre_juez}")

        self.cursor.execute("""
        INSERT INTO perfiles_judiciales_argentinos (
            juez, tipo_entidad, fuero, instancia, jurisdiccion, tribunal,
            total_sentencias_analizadas, version_analyser
        ) VALUES (?, ?, ?, ?, ?, ?, 0, '1.0-ingesta')
        """, (
            nombre_juez,
            metadata.get('tipo_entidad', 'individual'),
            metadata.get('fuero'),
            'primera_instancia',  # Por defecto
            metadata.get('jurisdiccion'),
            metadata.get('tribunal')
        ))

        self.conn.commit()
        print_success(f"Perfil creado para: {nombre_juez}")

    def guardar_sentencia(self, metadata: Dict, texto_completo: str, chunks: List[str]):
        """
        Guarda la sentencia en la BD

        Args:
            metadata: Metadata extraída
            texto_completo: Texto completo de la sentencia
            chunks: Chunks del texto
        """
        # Generar ID
        sentencia_id = self.generar_sentencia_id(
            metadata.get('expediente'),
            metadata.get('archivo_original')
        )

        # Verificar si ya existe
        self.cursor.execute(
            "SELECT 1 FROM sentencias_por_juez_arg WHERE sentencia_id = ?",
            (sentencia_id,)
        )

        if self.cursor.fetchone():
            print_warning(f"Sentencia ya existe: {sentencia_id}")
            return False

        # Guardar chunks como JSON
        chunks_json = json.dumps(chunks, ensure_ascii=False)

        # Guardar en ruta de chunks si es necesario
        chunks_file = CHUNKS_DIR / f"{sentencia_id}_chunks.json"
        chunks_file.parent.mkdir(parents=True, exist_ok=True)
        chunks_file.write_text(chunks_json, encoding='utf-8')

        # Insertar sentencia
        try:
            self.cursor.execute("""
            INSERT INTO sentencias_por_juez_arg (
                sentencia_id, juez, archivo_original,
                fecha_sentencia, expediente, caratula,
                fuero, instancia, jurisdiccion, tribunal,
                tipo_sentencia, materia, actor, demandado, resultado,
                texto_completo, ruta_chunks,
                fecha_procesamiento, extension_palabras
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sentencia_id,
                metadata['juez'],
                metadata.get('archivo_original'),
                metadata.get('fecha_sentencia'),
                metadata.get('expediente'),
                metadata.get('caratula'),
                metadata.get('fuero'),
                'primera_instancia',  # Por defecto
                metadata.get('jurisdiccion'),
                metadata.get('tribunal'),
                metadata.get('tipo_sentencia'),
                metadata.get('materia'),
                metadata.get('actor'),
                metadata.get('demandado'),
                metadata.get('resultado'),
                texto_completo,
                str(chunks_file),
                datetime.now().isoformat(),
                len(texto_completo.split())
            ))

            self.conn.commit()
            print_success(f"Sentencia guardada: {sentencia_id}")

            # Actualizar contador del juez
            self.cursor.execute("""
            UPDATE perfiles_judiciales_argentinos
            SET total_sentencias_analizadas = total_sentencias_analizadas + 1
            WHERE juez = ?
            """, (metadata['juez'],))
            self.conn.commit()

            return True

        except sqlite3.Error as e:
            print_error(f"Error al guardar sentencia: {e}")
            self.conn.rollback()
            return False

    def procesar_sentencia(self, archivo_path: Path) -> bool:
        """
        Procesa una sentencia completa

        Args:
            archivo_path: Ruta al archivo PDF o TXT

        Returns:
            True si se procesó exitosamente
        """
        print(f"\n{Colors.BOLD}Procesando: {archivo_path.name}{Colors.ENDC}")

        # 1. Extraer texto
        try:
            texto = self.extraer_texto(archivo_path)
            if not texto or len(texto) < 100:
                print_error("Texto vacío o muy corto")
                return False
            print_success(f"Texto extraído: {len(texto)} caracteres")
        except Exception as e:
            print_error(f"Error al extraer texto: {e}")
            return False

        # 2. Extraer metadata
        try:
            metadata = self.extractor_metadata.extraer_metadata(
                texto,
                archivo_path.name
            )
            print_success(f"Metadata extraída (confianza: {metadata['confianza_extraccion']*100:.0f}%)")

            # Validar metadata
            es_valido, errores = self.extractor_metadata.validar_metadata(metadata)
            if not es_valido:
                print_error("Metadata inválida:")
                for error in errores:
                    if not error.startswith('Advertencia'):
                        print(f"  - {error}")
                return False

            # Mostrar advertencias
            for error in errores:
                if error.startswith('Advertencia'):
                    print_warning(error)

        except Exception as e:
            print_error(f"Error al extraer metadata: {e}")
            return False

        # 3. Hacer chunks
        try:
            chunks = self.hacer_chunks(texto)
            print_success(f"Chunks creados: {len(chunks)}")
        except Exception as e:
            print_error(f"Error al hacer chunks: {e}")
            return False

        # 4. Crear perfil de juez si no existe
        try:
            self.crear_perfil_juez_basico(metadata)
        except Exception as e:
            print_error(f"Error al crear perfil de juez: {e}")
            return False

        # 5. Guardar sentencia
        try:
            resultado = self.guardar_sentencia(metadata, texto, chunks)
            return resultado
        except Exception as e:
            print_error(f"Error al guardar sentencia: {e}")
            return False

    def procesar_directorio(self, directorio: Path, extension: str = '.pdf'):
        """
        Procesa todas las sentencias de un directorio

        Args:
            directorio: Ruta al directorio
            extension: Extensión de archivos a procesar
        """
        archivos = list(directorio.glob(f'*{extension}'))

        if not archivos:
            print_warning(f"No se encontraron archivos {extension} en: {directorio}")
            return

        print(f"\n{Colors.BOLD}{'='*70}")
        print(f"PROCESANDO {len(archivos)} ARCHIVOS")
        print(f"{'='*70}{Colors.ENDC}\n")

        exitosos = 0
        fallidos = 0

        for archivo in archivos:
            try:
                if self.procesar_sentencia(archivo):
                    exitosos += 1
                else:
                    fallidos += 1
            except Exception as e:
                print_error(f"Error inesperado al procesar {archivo.name}: {e}")
                fallidos += 1

        # Resumen
        print(f"\n{Colors.BOLD}{'='*70}")
        print("RESUMEN")
        print(f"{'='*70}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Exitosos: {exitosos}{Colors.ENDC}")
        print(f"{Colors.FAIL}Fallidos: {fallidos}{Colors.ENDC}")
        print(f"{Colors.BOLD}Total: {exitosos + fallidos}{Colors.ENDC}\n")

    def mostrar_estadisticas(self):
        """Muestra estadísticas de la BD"""
        print(f"\n{Colors.BOLD}{'='*70}")
        print("ESTADÍSTICAS DE LA BASE DE DATOS")
        print(f"{'='*70}{Colors.ENDC}\n")

        # Total de jueces
        self.cursor.execute("SELECT COUNT(*) FROM perfiles_judiciales_argentinos")
        total_jueces = self.cursor.fetchone()[0]
        print(f"Total de jueces: {total_jueces}")

        # Total de sentencias
        self.cursor.execute("SELECT COUNT(*) FROM sentencias_por_juez_arg")
        total_sentencias = self.cursor.fetchone()[0]
        print(f"Total de sentencias: {total_sentencias}")

        # Por fuero
        self.cursor.execute("""
        SELECT fuero, COUNT(*) as cnt
        FROM sentencias_por_juez_arg
        WHERE fuero IS NOT NULL
        GROUP BY fuero
        ORDER BY cnt DESC
        """)
        fueros = self.cursor.fetchall()

        if fueros:
            print("\nSentencias por fuero:")
            for fuero, cnt in fueros:
                print(f"  • {fuero}: {cnt}")

        # Top jueces por cantidad de sentencias
        self.cursor.execute("""
        SELECT j.juez, j.total_sentencias_analizadas
        FROM perfiles_judiciales_argentinos j
        WHERE j.total_sentencias_analizadas > 0
        ORDER BY j.total_sentencias_analizadas DESC
        LIMIT 5
        """)
        top_jueces = self.cursor.fetchall()

        if top_jueces:
            print("\nTop 5 jueces por cantidad de sentencias:")
            for juez, cnt in top_jueces:
                print(f"  • {juez}: {cnt}")

        print()


def main():
    """Función principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Ingestor de sentencias judiciales argentinas'
    )
    parser.add_argument(
        'archivo_o_directorio',
        type=Path,
        help='Archivo o directorio con sentencias'
    )
    parser.add_argument(
        '--extension',
        type=str,
        default='.pdf',
        help='Extensión de archivos a procesar (default: .pdf)'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Mostrar estadísticas al final'
    )

    args = parser.parse_args()

    # Verificar que existe el archivo/directorio
    if not args.archivo_o_directorio.exists():
        print_error(f"No existe: {args.archivo_o_directorio}")
        sys.exit(1)

    # Crear ingestor
    try:
        ingestor = IngestorSentenciasJudicial()
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)

    # Procesar
    try:
        if args.archivo_o_directorio.is_file():
            # Procesar un solo archivo
            ingestor.procesar_sentencia(args.archivo_o_directorio)
        else:
            # Procesar directorio
            ingestor.procesar_directorio(args.archivo_o_directorio, args.extension)

        # Estadísticas
        if args.stats:
            ingestor.mostrar_estadisticas()

    finally:
        ingestor.cerrar_bd()


if __name__ == "__main__":
    main()
