#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           CREADOR AUTOMÁTICO DE ESTRUCTURA DE DIRECTORIOS                    ║
║                    Sistema Sentency - Análisis Judicial                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Este script crea automáticamente toda la estructura de directorios necesaria
para el correcto funcionamiento de la aplicación Sentency.

USO:
    python crear_estructura_directorios.py [ruta_base]

    Si no se especifica ruta_base, se usa el directorio padre de 'scripts/'

EJEMPLO:
    python crear_estructura_directorios.py
    python crear_estructura_directorios.py /ruta/a/mi/proyecto
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# DEFINICIÓN DE LA ESTRUCTURA DE DIRECTORIOS
# ══════════════════════════════════════════════════════════════════════════════

ESTRUCTURA_DIRECTORIOS = {
    "bases_rag": {
        "cognitiva": {
            "faiss_index": {},
        }
    },
    "data": {
        "pdfs": {
            "general": {},
            "sentencias_pdf": {},
            "sentencias_texto": {},
        },
        "chunks": {
            "general": {},
        },
        "index": {
            "general": {},
        },
        "cache_informes": {},
        "logs": {},
        "resultados": {},
        "exports": {},
        "backups": {},
    },
    "models": {
        "embeddings": {},
        "ner": {},
        "generator": {},
    },
    "scripts": {},
    "templates": {},
    "static": {
        "css": {},
        "js": {},
        "images": {},
    },
    "config": {},
    "tests": {},
}

# ══════════════════════════════════════════════════════════════════════════════
# ARCHIVOS README A CREAR
# ══════════════════════════════════════════════════════════════════════════════

ARCHIVOS_README = {
    "data/pdfs/sentencias_pdf/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: SENTENCIAS EN PDF                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar sentencias judiciales en formato PDF.

FORMATOS ACEPTADOS:
    - .pdf (Adobe PDF)

NOMENCLATURA RECOMENDADA:
    [Tribunal]_[Año]_[Tema]_[Expediente].pdf

    Ejemplos:
    - CSJN_2024_Responsabilidad_Civil_FRO123456.pdf
    - SCBA_2023_Laboral_Despido_LP45678.pdf
    - TSJ_Cordoba_2024_Daños_Punitivos_C789012.pdf

PROCESAMIENTO:
    Los archivos en este directorio serán procesados por:
    - ingesta_sentencias_judicial.py
    - extractor_metadata_argentina.py

NOTAS:
    - Preferir archivos con texto extraíble (no escaneados)
    - Si es posible, usar formato TXT en sentencias_texto/
""",

    "data/pdfs/sentencias_texto/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: SENTENCIAS EN TEXTO                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar sentencias judiciales en formato texto plano.
    Este formato es el RECOMENDADO para mejor procesamiento.

FORMATOS ACEPTADOS:
    - .txt (Texto plano UTF-8)

NOMENCLATURA RECOMENDADA:
    [Tribunal]_[Año]_[Tema]_[Expediente].txt

    Ejemplos:
    - CSJN_2024_Responsabilidad_Civil_FRO123456.txt
    - SCBA_2023_Laboral_Despido_LP45678.txt
    - TSJ_Cordoba_2024_Daños_Punitivos_C789012.txt

PROCESAMIENTO:
    Los archivos en este directorio serán procesados por:
    - ingesta_sentencias_judicial.py
    - extractor_metadata_argentina.py

VENTAJAS DEL FORMATO TXT:
    ✓ Procesamiento más rápido
    ✓ Menor uso de memoria
    ✓ Sin dependencias de librerías PDF
    ✓ Mejor extracción de metadata
""",

    "data/pdfs/general/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: DOCUMENTOS GENERALES                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar documentos de referencia general:
    - Doctrina legal
    - Artículos académicos
    - Normativa
    - Material de consulta

FORMATOS ACEPTADOS:
    - .pdf
    - .txt
    - .docx
""",

    "data/chunks/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: CHUNKS PROCESADOS                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar los fragmentos (chunks) de texto procesados.
    Estos archivos son generados automáticamente por el sistema.

CONTENIDO:
    - Archivos JSON con chunks de documentos
    - Formato: {documento_id}_chunks.json

CONFIGURACIÓN ACTUAL:
    - Tamaño de chunk: 800 tokens
    - Overlap: 100 tokens

IMPORTANTE:
    No modificar estos archivos manualmente.
    Son regenerados en cada procesamiento de documentos.
""",

    "data/cache_informes/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: CACHÉ DE INFORMES                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar informes generados en caché para acceso rápido.

CONTENIDO:
    - Informes de perfil judicial
    - Análisis de sentencias
    - Predicciones generadas

LIMPIEZA:
    Puede eliminar archivos antiguos para liberar espacio.
    El sistema regenerará los informes cuando se soliciten.
""",

    "data/logs/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: LOGS DEL SISTEMA                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar registros de ejecución del sistema.

CONTENIDO:
    - Logs de procesamiento de sentencias
    - Errores de extracción
    - Estadísticas de análisis
    - Registros de actividad web

MANTENIMIENTO:
    Revise periódicamente para identificar problemas.
    Puede archivar o eliminar logs antiguos.
""",

    "data/resultados/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: RESULTADOS DE ANÁLISIS                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar los resultados finales de análisis:
    - Perfiles de jueces exportados
    - Estadísticas agregadas
    - Reportes de líneas jurisprudenciales

FORMATOS DE SALIDA:
    - .json (datos estructurados)
    - .txt (informes de texto)
    - .md (Markdown)
    - .pdf (informes formateados)
""",

    "data/exports/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: EXPORTACIONES                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar archivos exportados del sistema:
    - Exportaciones de base de datos
    - Informes generados para clientes
    - Datos en formato intercambiable
""",

    "data/backups/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: BACKUPS                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar copias de seguridad automáticas:
    - Respaldos de bases de datos
    - Snapshots de configuración
    - Versiones anteriores de datos

POLÍTICA DE RETENCIÓN:
    Configure según sus necesidades de almacenamiento.
""",

    "bases_rag/cognitiva/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: BASE RAG COGNITIVA                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Base de datos principal del sistema Sentency.

CONTENIDO:
    - juez_centrico_arg.db    : Base principal con perfiles judiciales
    - metadatos.db            : Metadata de sentencias procesadas
    - faiss_index/            : Índices vectoriales FAISS

TABLAS PRINCIPALES:
    1. perfiles_judiciales_argentinos (80+ campos)
    2. sentencias_por_juez_arg
    3. lineas_jurisprudenciales
    4. redes_influencia_judicial
    5. factores_predictivos

IMPORTANTE:
    ¡No eliminar estos archivos! Contienen todos los análisis procesados.
    Hacer backups regulares a data/backups/
""",

    "models/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: MODELOS DE ML                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar modelos de Machine Learning descargados.

SUBDIRECTORIOS:
    - embeddings/  : Modelos de sentence-transformers
    - ner/         : Modelos de Named Entity Recognition (BERT)
    - generator/   : Modelos generativos (FLAN-T5)

MODELOS UTILIZADOS:
    - sentence-transformers/all-MiniLM-L6-v2
    - mrm8488/bert-spanish-cased-finetuned-ner
    - google/flan-t5-base

NOTA:
    Los modelos se descargan automáticamente la primera vez.
    Puede pre-descargarlos para uso offline.
""",

    "config/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: CONFIGURACIÓN                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar archivos de configuración del sistema.

ARCHIVOS:
    - config.json : Configuración de modelos y parámetros
    - .env        : Variables de entorno (API keys, etc.)

CONFIGURACIÓN PRINCIPAL (config.json):
    {
        "models": {
            "embedding": "sentence-transformers/all-MiniLM-L6-v2",
            "generator_local": "google/flan-t5-base",
            "ner": "mrm8488/bert-spanish-cased-finetuned-ner"
        },
        "parameters": {
            "chunk_size": 800,
            "chunk_overlap": 100
        }
    }
""",

    "tests/README.txt": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DIRECTORIO: TESTS                                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROPÓSITO:
    Almacenar tests unitarios y de integración.

EJECUCIÓN:
    pytest tests/
    python -m pytest tests/ -v
"""
}

# ══════════════════════════════════════════════════════════════════════════════
# ARCHIVO .gitkeep para directorios vacíos
# ══════════════════════════════════════════════════════════════════════════════

GITKEEP_CONTENT = "# Este archivo mantiene el directorio en git\n"


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES PRINCIPALES
# ══════════════════════════════════════════════════════════════════════════════

def imprimir_banner():
    """Imprime el banner del script."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ███████╗███████╗███╗   ██╗████████╗███████╗███╗   ██╗ ██████╗██╗   ██╗   ║
║     ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██╔════╝████╗  ██║██╔════╝╚██╗ ██╔╝   ║
║     ███████╗█████╗  ██╔██╗ ██║   ██║   █████╗  ██╔██╗ ██║██║      ╚████╔╝    ║
║     ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ██║╚██╗██║██║       ╚██╔╝     ║
║     ███████║███████╗██║ ╚████║   ██║   ███████╗██║ ╚████║╚██████╗   ██║      ║
║     ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝ ╚═════╝   ╚═╝      ║
║                                                                              ║
║           CREADOR AUTOMÁTICO DE ESTRUCTURA DE DIRECTORIOS                    ║
║                    Sistema de Análisis Judicial Argentino                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def obtener_ruta_base():
    """Determina la ruta base del proyecto."""
    if len(sys.argv) > 1:
        ruta = Path(sys.argv[1]).resolve()
    else:
        # Subir desde scripts/ a colaborative/
        ruta = Path(__file__).parent.parent.resolve()

    return ruta


def crear_directorios_recursivo(base_path: Path, estructura: dict, nivel: int = 0):
    """
    Crea directorios recursivamente según la estructura definida.

    Args:
        base_path: Ruta base donde crear
        estructura: Diccionario con la estructura
        nivel: Nivel de profundidad (para indentación)

    Returns:
        Tupla (creados, existentes)
    """
    creados = 0
    existentes = 0
    indent = "  " * nivel

    for nombre, subestructura in estructura.items():
        ruta_completa = base_path / nombre

        if ruta_completa.exists():
            print(f"{indent}✓ Ya existe: {ruta_completa.relative_to(base_path.parent)}")
            existentes += 1
        else:
            ruta_completa.mkdir(parents=True, exist_ok=True)
            print(f"{indent}✚ Creado:    {ruta_completa.relative_to(base_path.parent)}")
            creados += 1

        # Recursión para subdirectorios
        if subestructura:
            sub_creados, sub_existentes = crear_directorios_recursivo(
                ruta_completa, subestructura, nivel + 1
            )
            creados += sub_creados
            existentes += sub_existentes

    return creados, existentes


def crear_archivos_readme(base_path: Path):
    """Crea los archivos README en los directorios correspondientes."""
    print("\n" + "="*70)
    print("  CREANDO ARCHIVOS README")
    print("="*70 + "\n")

    creados = 0
    existentes = 0

    for ruta_relativa, contenido in ARCHIVOS_README.items():
        ruta_completa = base_path / ruta_relativa

        # Asegurar que el directorio padre existe
        ruta_completa.parent.mkdir(parents=True, exist_ok=True)

        if ruta_completa.exists():
            print(f"  ✓ Ya existe: {ruta_relativa}")
            existentes += 1
        else:
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                f.write(contenido.strip() + "\n")
            print(f"  ✚ Creado:    {ruta_relativa}")
            creados += 1

    return creados, existentes


def crear_gitkeep(base_path: Path):
    """Crea archivos .gitkeep en directorios que podrían quedar vacíos."""
    print("\n" + "="*70)
    print("  CREANDO ARCHIVOS .gitkeep")
    print("="*70 + "\n")

    # Directorios que necesitan .gitkeep
    dirs_gitkeep = [
        "data/pdfs/general",
        "data/pdfs/sentencias_pdf",
        "data/pdfs/sentencias_texto",
        "data/chunks/general",
        "data/index/general",
        "data/cache_informes",
        "data/logs",
        "data/resultados",
        "data/exports",
        "data/backups",
        "bases_rag/cognitiva/faiss_index",
        "models/embeddings",
        "models/ner",
        "models/generator",
        "static/css",
        "static/js",
        "static/images",
        "config",
        "tests",
    ]

    creados = 0

    for dir_rel in dirs_gitkeep:
        ruta_gitkeep = base_path / dir_rel / ".gitkeep"

        if not ruta_gitkeep.exists():
            ruta_gitkeep.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta_gitkeep, 'w') as f:
                f.write(GITKEEP_CONTENT)
            print(f"  ✚ Creado: {dir_rel}/.gitkeep")
            creados += 1

    if creados == 0:
        print("  ✓ Todos los .gitkeep ya existen")

    return creados


def crear_config_default(base_path: Path):
    """Crea archivo de configuración por defecto si no existe."""
    config_path = base_path / "config.json"

    if not config_path.exists():
        config_default = {
            "models": {
                "embedding": "sentence-transformers/all-MiniLM-L6-v2",
                "generator_local": "google/flan-t5-base",
                "generator_cloud": "gemini-2.5-pro",
                "ner": "mrm8488/bert-spanish-cased-finetuned-ner"
            },
            "parameters": {
                "chunk_size": 800,
                "chunk_overlap": 100,
                "k_search_content": 5,
                "k_search_profiles": 6,
                "min_confidence": 0.7
            },
            "paths": {
                "pdfs": "data/pdfs",
                "chunks": "data/chunks",
                "index": "data/index",
                "cache": "data/cache_informes",
                "logs": "data/logs",
                "results": "data/resultados",
                "database": "bases_rag/cognitiva/juez_centrico_arg.db"
            },
            "web": {
                "host": "127.0.0.1",
                "port": 5002,
                "debug": False
            }
        }

        import json
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_default, f, indent=2, ensure_ascii=False)

        print(f"\n  ✚ Creado config.json por defecto")
        return True

    return False


def crear_env_template(base_path: Path):
    """Crea archivo .env.template si no existe."""
    env_template_path = base_path / ".env.template"

    if not env_template_path.exists():
        env_content = """# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE ENTORNO - SENTENCY
# ══════════════════════════════════════════════════════════════════════════════
# Copie este archivo como .env y configure sus valores

# API de Google/Gemini (opcional, para generación mejorada)
GOOGLE_API_KEY=su_api_key_aqui

# Usar Gemini para generación (True/False)
USE_GEMINI=False

# Modo debug de Flask
FLASK_DEBUG=False

# Puerto de la aplicación web
FLASK_PORT=5002

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN AVANZADA
# ══════════════════════════════════════════════════════════════════════════════

# Nivel de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Máximo de workers para procesamiento paralelo
MAX_WORKERS=4
"""
        with open(env_template_path, 'w', encoding='utf-8') as f:
            f.write(env_content)

        print(f"  ✚ Creado .env.template")
        return True

    return False


def imprimir_resumen(base_path: Path, dirs_creados: int, dirs_existentes: int,
                     readme_creados: int, readme_existentes: int, gitkeep_creados: int):
    """Imprime un resumen de las operaciones realizadas."""
    total_dirs = dirs_creados + dirs_existentes
    total_readme = readme_creados + readme_existentes

    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                              RESUMEN DE OPERACIÓN                            ║")
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    print(f"║  Ruta base: {str(base_path)[:55]:<55} ║")
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    print(f"║  Directorios:                                                                ║")
    print(f"║    - Creados:    {dirs_creados:3d}                                                       ║")
    print(f"║    - Existentes: {dirs_existentes:3d}                                                       ║")
    print(f"║    - Total:      {total_dirs:3d}                                                       ║")
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    print(f"║  Archivos README:                                                            ║")
    print(f"║    - Creados:    {readme_creados:3d}                                                       ║")
    print(f"║    - Existentes: {readme_existentes:3d}                                                       ║")
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    print(f"║  Archivos .gitkeep creados: {gitkeep_creados:3d}                                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")

    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                         ESTRUCTURA CREADA                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print(f"""
{base_path.name}/
├── bases_rag/
│   └── cognitiva/              ← Base de datos principal
│       └── faiss_index/        ← Índices vectoriales FAISS
│
├── data/
│   ├── pdfs/
│   │   ├── general/            ← Documentos generales
│   │   ├── sentencias_pdf/     ← Sentencias en PDF
│   │   └── sentencias_texto/   ← Sentencias en TXT (recomendado)
│   ├── chunks/                 ← Fragmentos procesados
│   ├── index/                  ← Índices de búsqueda
│   ├── cache_informes/         ← Caché de informes
│   ├── logs/                   ← Registros del sistema
│   ├── resultados/             ← Salidas de análisis
│   ├── exports/                ← Exportaciones
│   └── backups/                ← Copias de seguridad
│
├── models/
│   ├── embeddings/             ← Modelos de embeddings
│   ├── ner/                    ← Modelos NER
│   └── generator/              ← Modelos generativos
│
├── scripts/                    ← Scripts Python
├── templates/                  ← Templates HTML Flask
├── static/                     ← Archivos estáticos web
├── config/                     ← Archivos de configuración
└── tests/                      ← Tests unitarios
""")

    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                         PRÓXIMOS PASOS                                       ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print("""
  1. Copie .env.template a .env y configure sus API keys

  2. Coloque sus sentencias en:
     - data/pdfs/sentencias_texto/  (formato TXT recomendado)
     - data/pdfs/sentencias_pdf/    (formato PDF)

  3. Ejecute la ingesta:
     python ingesta_sentencias_judicial.py

  4. O use la interfaz web:
     python end2end_webapp.py
     Acceda a: http://127.0.0.1:5002
""")


def main():
    """Función principal."""
    imprimir_banner()

    # Obtener ruta base
    base_path = obtener_ruta_base()

    print(f"  Ruta base detectada: {base_path}")
    print(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Crear estructura de directorios
    print("\n" + "="*70)
    print("  CREANDO ESTRUCTURA DE DIRECTORIOS")
    print("="*70 + "\n")

    dirs_creados, dirs_existentes = crear_directorios_recursivo(base_path, ESTRUCTURA_DIRECTORIOS)

    # Crear archivos README
    readme_creados, readme_existentes = crear_archivos_readme(base_path)

    # Crear archivos .gitkeep
    gitkeep_creados = crear_gitkeep(base_path)

    # Crear config por defecto
    print("\n" + "="*70)
    print("  CREANDO ARCHIVOS DE CONFIGURACIÓN")
    print("="*70 + "\n")

    crear_config_default(base_path)
    crear_env_template(base_path)

    # Imprimir resumen
    imprimir_resumen(base_path, dirs_creados, dirs_existentes,
                     readme_creados, readme_existentes, gitkeep_creados)

    print("\n  ✅ Proceso completado exitosamente!\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
