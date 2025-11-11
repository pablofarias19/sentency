# -*- coding: utf-8 -*-
"""
Configuración del Sistema RAG Enriquecido con PCA
Define rutas, parámetros y configuraciones globales
"""

import os
from pathlib import Path

# ==========================================================
# 🔹 CONFIGURACIÓN DE DIRECTORIOS
# ==========================================================
BASE_DIR = Path("colaborative")
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Directorios de datos
PDFS_DIR = DATA_DIR / "pdfs"
PDFS_GENERAL = PDFS_DIR / "general"
PDFS_CIVIL = PDFS_DIR / "civil"
INDEX_DIR = DATA_DIR / "index"
LOGS_DIR = DATA_DIR / "logs"
CHUNKS_DIR = DATA_DIR / "chunks"

# Crear directorios si no existen
for directory in [DATA_DIR, PDFS_GENERAL, PDFS_CIVIL, INDEX_DIR, LOGS_DIR, CHUNKS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ==========================================================
# 🔹 CONFIGURACIÓN DE BASES DE DATOS
# ==========================================================
# Base de datos tradicional de autoaprendizaje
DB_AUTOAPRENDIZAJE = DATA_DIR / "autoaprendizaje.db"

# Base de datos de perfiles cognitivos (PCA)
DB_PERFILES = DATA_DIR / "perfiles.db"

# Índices FAISS
FAISS_A_INDEX = INDEX_DIR / "vector_index.faiss"  # Contenido tradicional
FAISS_B_INDEX = DATA_DIR / "faiss_profiles.index"  # Perfiles cognitivos
FAISS_B_META = DATA_DIR / "faiss_profiles_meta.json"

# Historial de refinamiento
HISTORIAL_REFINAMIENTO = LOGS_DIR / "refinamiento.json"

# ==========================================================
# 🔹 CONFIGURACIÓN DE MODELOS
# ==========================================================
# Modelos de embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_PROFILES_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Mismo para consistencia

# Modelos de generación
GENERATOR_MODEL_LOCAL = "google/flan-t5-base"
GENERATOR_MODEL_CLOUD = "gemini-2.5-pro"  # Requiere API key

# Modelo NER
NER_MODEL = "mrm8488/bert-spanish-cased-finetuned-ner"

# ==========================================================
# 🔹 CONFIGURACIÓN DE PROCESAMIENTO
# ==========================================================
# Parámetros de chunking
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 100

# Parámetros de búsqueda
DEFAULT_K_SEARCH = 5  # Fragmentos tradicionales
DEFAULT_K_PROFILES = 6  # Perfiles cognitivos

# Parámetros de generación
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.1

# ==========================================================
# 🔹 CONFIGURACIÓN DE APIs EXTERNAS
# ==========================================================
# Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
USE_GEMINI = os.getenv("USE_GEMINI", "True").lower() == "true"

# HuggingFace
HF_TOKEN = os.getenv("HF_TOKEN")

# ==========================================================
# 🔹 CONFIGURACIÓN DE LOGGING
# ==========================================================
ENABLE_VERBOSE_LOGGING = True
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = True

# ==========================================================
# 🔹 CONFIGURACIÓN DEL SISTEMA PCA
# ==========================================================
# Marcos de referencia detectables
MARCOS_REFERENCIA = {
    "socio_filosofico": ["foucault", "habermas", "weber", "durkheim", "bourdieu", "luhmann"],
    "economico_liberal": ["hayek", "friedman", "keynes", "smith", "schumpeter", "becker"],
    "juridico_garantista": ["kelsen", "hart", "ross", "dworkin", "ferrajoli", "rawls", "alexy"],
    "critico_materialista": ["marx", "gramsci", "lenin", "althusser"],
    "filosofico_existencial": ["arendt", "heidegger", "husserl", "nietzsche"],
    "juridico_dogmatico": ["constitucional", "penal", "civil", "comercial", "procesal", "administrativo"]
}

# Estrategias intelectuales
ESTRATEGIAS_DETECTABLES = [
    "Comparativa", "Propositiva", "Analítica", "Crítica", "Expositiva"
]

# Metodologías jurídicas
METODOLOGIAS_JURIDICAS = [
    "Jurisprudencial", "Doctrinaria", "Constitucional", "Normativa", "Comparada", "Histórica", "Dogmática general"
]

# ==========================================================
# 🔹 CONFIGURACIÓN DE LA WEBAPP
# ==========================================================
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5002
FLASK_DEBUG = False

# Rutas de templates
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# ==========================================================
# 🔹 FUNCIONES DE VALIDACIÓN
# ==========================================================
def validate_config():
    """Valida la configuración y dependencias"""
    issues = []
    
    # Verificar directorios críticos
    if not MODELS_DIR.exists():
        issues.append(f"Directorio de modelos no encontrado: {MODELS_DIR}")
    
    # Verificar API keys si están configuradas
    if USE_GEMINI and not GOOGLE_API_KEY:
        issues.append("USE_GEMINI=True pero GOOGLE_API_KEY no está configurada")
    
    # Verificar modelos locales
    embedding_path = MODELS_DIR / "embeddings" / "all-MiniLM-L6-v2"
    if not embedding_path.exists():
        issues.append(f"Modelo de embeddings no encontrado: {embedding_path}")
    
    generator_path = MODELS_DIR / "generator" / "flan-t5-base"
    if not generator_path.exists():
        issues.append(f"Modelo generador no encontrado: {generator_path}")
    
    return issues

def print_config_summary():
    """Imprime un resumen de la configuración actual"""
    print("🔧 CONFIGURACIÓN DEL SISTEMA RAG ENRIQUECIDO")
    print("=" * 50)
    print(f"📁 Directorio base: {BASE_DIR.absolute()}")
    print(f"🗃️ Base datos autoaprendizaje: {DB_AUTOAPRENDIZAJE}")
    print(f"🧠 Base datos perfiles: {DB_PERFILES}")
    print(f"📊 FAISS contenido: {FAISS_A_INDEX}")
    print(f"🎭 FAISS perfiles: {FAISS_B_INDEX}")
    print(f"🤖 Modelo embeddings: {EMBEDDING_MODEL}")
    print(f"⚡ Modelo generador: {GENERATOR_MODEL_LOCAL}")
    print(f"🌐 Gemini habilitado: {'✅' if USE_GEMINI else '❌'}")
    print(f"🔍 K búsqueda contenido: {DEFAULT_K_SEARCH}")
    print(f"🧭 K búsqueda perfiles: {DEFAULT_K_PROFILES}")
    print(f"🌐 Webapp: http://{FLASK_HOST}:{FLASK_PORT}")
    
    # Mostrar issues si existen
    issues = validate_config()
    if issues:
        print("\n⚠️ PROBLEMAS DETECTADOS:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("\n✅ Configuración válida")
    
    print("=" * 50)

# ==========================================================
# 🔹 CONFIGURACIÓN DE ENTORNO
# ==========================================================
def setup_environment():
    """Configura el entorno necesario para el sistema"""
    
    # Variables de entorno por defecto
    env_defaults = {
        "TOKENIZERS_PARALLELISM": "false",  # Evitar warnings de HuggingFace
        "TRANSFORMERS_CACHE": str(MODELS_DIR / "cache"),
        "HF_HOME": str(MODELS_DIR / "huggingface"),
    }
    
    for key, value in env_defaults.items():
        if key not in os.environ:
            os.environ[key] = value
    
    # Crear archivo de configuración local si no existe
    config_file = BASE_DIR / "config.local.json"
    if not config_file.exists():
        import json
        local_config = {
            "embedding_model": EMBEDDING_MODEL,
            "generator_model": GENERATOR_MODEL_LOCAL,
            "chunk_size": DEFAULT_CHUNK_SIZE,
            "k_search": DEFAULT_K_SEARCH,
            "k_profiles": DEFAULT_K_PROFILES,
            "use_gemini": USE_GEMINI,
            "flask_port": FLASK_PORT,
            "verbose_logging": ENABLE_VERBOSE_LOGGING
        }
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(local_config, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Archivo de configuración creado: {config_file}")

# ==========================================================
# 🔹 INICIALIZACIÓN
# ==========================================================
if __name__ == "__main__":
    setup_environment()
    print_config_summary()