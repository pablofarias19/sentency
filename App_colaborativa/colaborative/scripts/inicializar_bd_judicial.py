#!/usr/bin/env python3
"""
Sistema de Análisis de Pensamiento Judicial - Argentina
Inicializador de Base de Datos

Versión: 1.0
Fecha: 2025-11-12

Este script inicializa la base de datos SQLite con el esquema completo
para el análisis de pensamiento judicial argentino.
"""

import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime

# Configuración de rutas
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
BASES_RAG_DIR = BASE_DIR / "bases_rag" / "cognitiva"
SCHEMA_FILE = SCRIPT_DIR / "schema_juez_centrico_arg.sql"
DB_FILE = BASES_RAG_DIR / "juez_centrico_arg.db"

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Imprime un encabezado formateado"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}{Colors.ENDC}\n")

def print_success(text):
    """Imprime mensaje de éxito"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """Imprime mensaje de error"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    """Imprime mensaje de advertencia"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    """Imprime mensaje informativo"""
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def verificar_archivos():
    """Verifica que existan los archivos necesarios"""
    print_info("Verificando archivos necesarios...")

    if not SCHEMA_FILE.exists():
        print_error(f"No se encuentra el archivo de esquema: {SCHEMA_FILE}")
        return False

    print_success(f"Archivo de esquema encontrado: {SCHEMA_FILE}")
    return True

def crear_directorios():
    """Crea los directorios necesarios si no existen"""
    print_info("Verificando directorios...")

    if not BASES_RAG_DIR.exists():
        print_warning(f"Creando directorio: {BASES_RAG_DIR}")
        BASES_RAG_DIR.mkdir(parents=True, exist_ok=True)
        print_success("Directorio creado")
    else:
        print_success(f"Directorio existe: {BASES_RAG_DIR}")

    return True

def backup_database():
    """Hace backup de la base de datos si existe"""
    if DB_FILE.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = DB_FILE.parent / f"juez_centrico_arg_backup_{timestamp}.db"

        print_warning(f"La base de datos ya existe: {DB_FILE}")
        respuesta = input("¿Desea hacer un backup antes de recrearla? (s/n): ")

        if respuesta.lower() in ['s', 'si', 'sí', 'yes', 'y']:
            import shutil
            shutil.copy2(DB_FILE, backup_file)
            print_success(f"Backup creado: {backup_file}")
            return True
        elif respuesta.lower() in ['n', 'no']:
            print_warning("Se procederá sin hacer backup")
            return True
        else:
            print_error("Respuesta no válida. Abortando.")
            return False

    return True

def inicializar_base_datos(forzar=False):
    """
    Inicializa la base de datos ejecutando el esquema SQL

    Args:
        forzar: Si True, sobrescribe la BD sin preguntar
    """
    print_header("INICIALIZACIÓN DE BASE DE DATOS JUDICIAL ARGENTINA")

    # Verificar archivos
    if not verificar_archivos():
        return False

    # Crear directorios
    if not crear_directorios():
        return False

    # Backup si es necesario
    if not forzar and not backup_database():
        return False

    try:
        # Leer el esquema SQL
        print_info(f"Leyendo esquema desde: {SCHEMA_FILE}")
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        print_success(f"Esquema leído ({len(schema_sql)} caracteres)")

        # Conectar a la base de datos
        print_info(f"Conectando a: {DB_FILE}")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Ejecutar el esquema
        print_info("Ejecutando esquema SQL...")
        cursor.executescript(schema_sql)
        conn.commit()

        print_success("Esquema ejecutado exitosamente")

        # Verificar tablas creadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tablas = cursor.fetchall()

        print_info(f"\nTablas creadas ({len(tablas)}):")
        for tabla in tablas:
            print(f"  • {tabla[0]}")

        # Verificar vistas creadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")
        vistas = cursor.fetchall()

        if vistas:
            print_info(f"\nVistas creadas ({len(vistas)}):")
            for vista in vistas:
                print(f"  • {vista[0]}")

        # Verificar índices creados
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%' ORDER BY name")
        indices = cursor.fetchall()

        if indices:
            print_info(f"\nÍndices creados ({len(indices)}):")
            for indice in indices:
                print(f"  • {indice[0]}")

        conn.close()

        print_success("\n✓ Base de datos inicializada correctamente")
        print_info(f"Ubicación: {DB_FILE}")
        print_info(f"Tamaño: {DB_FILE.stat().st_size / 1024:.2f} KB")

        return True

    except sqlite3.Error as e:
        print_error(f"Error de SQLite: {e}")
        return False
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return False

def verificar_integridad():
    """Verifica la integridad de la base de datos"""
    print_header("VERIFICACIÓN DE INTEGRIDAD")

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # PRAGMA integrity_check
        cursor.execute("PRAGMA integrity_check")
        resultado = cursor.fetchone()[0]

        if resultado == "ok":
            print_success("Integridad de la base de datos: OK")
        else:
            print_error(f"Problemas de integridad: {resultado}")
            return False

        # Verificar foreign keys
        cursor.execute("PRAGMA foreign_key_check")
        fk_errors = cursor.fetchall()

        if not fk_errors:
            print_success("Integridad de claves foráneas: OK")
        else:
            print_error(f"Errores en claves foráneas: {len(fk_errors)}")
            return False

        conn.close()
        return True

    except Exception as e:
        print_error(f"Error en verificación: {e}")
        return False

def mostrar_estadisticas():
    """Muestra estadísticas de la base de datos"""
    print_header("ESTADÍSTICAS DE LA BASE DE DATOS")

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Contar registros en tablas principales
        tablas = [
            'perfiles_judiciales_argentinos',
            'sentencias_por_juez_arg',
            'lineas_jurisprudenciales',
            'redes_influencia_judicial',
            'factores_predictivos'
        ]

        print("\nRegistros por tabla:")
        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            print(f"  • {tabla}: {count}")

        conn.close()

    except Exception as e:
        print_error(f"Error al obtener estadísticas: {e}")

def insertar_datos_ejemplo():
    """Inserta datos de ejemplo para testing"""
    print_header("INSERCIÓN DE DATOS DE EJEMPLO")

    respuesta = input("¿Desea insertar datos de ejemplo para testing? (s/n): ")

    if respuesta.lower() not in ['s', 'si', 'sí', 'yes', 'y']:
        print_info("Omitiendo datos de ejemplo")
        return True

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Insertar un juez de ejemplo
        cursor.execute("""
        INSERT INTO perfiles_judiciales_argentinos (
            juez, tipo_entidad, fuero, instancia, jurisdiccion, tribunal,
            total_sentencias_analizadas, version_analyser
        ) VALUES (
            'Dr. Juan Pérez (EJEMPLO)',
            'individual',
            'laboral',
            'primera_instancia',
            'federal',
            'Juzgado Nacional del Trabajo N° 1',
            0,
            '1.0-testing'
        )
        """)

        print_success("Juez de ejemplo insertado: Dr. Juan Pérez (EJEMPLO)")

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print_error(f"Error al insertar datos de ejemplo: {e}")
        return False

def main():
    """Función principal"""
    # Parsear argumentos
    forzar = '--force' in sys.argv or '-f' in sys.argv
    solo_verificar = '--verify' in sys.argv or '-v' in sys.argv

    if solo_verificar:
        if DB_FILE.exists():
            verificar_integridad()
            mostrar_estadisticas()
        else:
            print_error(f"La base de datos no existe: {DB_FILE}")
        return

    # Inicializar
    if inicializar_base_datos(forzar):
        # Verificar
        if verificar_integridad():
            # Insertar datos de ejemplo
            insertar_datos_ejemplo()
            # Mostrar estadísticas
            mostrar_estadisticas()

            print_header("INICIALIZACIÓN COMPLETADA")
            print_success("El sistema está listo para procesar sentencias")
            print_info("\nPróximos pasos:")
            print("  1. Ejecutar el script de ingesta de sentencias")
            print("  2. Procesar sentencias con el analizador")
            print("  3. Generar informes")
        else:
            print_error("La base de datos tiene problemas de integridad")
    else:
        print_error("No se pudo inicializar la base de datos")
        sys.exit(1)

if __name__ == "__main__":
    main()
