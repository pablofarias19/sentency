import os
from huggingface_hub import snapshot_download

# ============================================================
# FUNCIÓN PARA CREAR ESTRUCTURA BASE
# ============================================================

def crear_estructura_base(base_dir="colaborative"):
    """
    Crea la estructura de carpetas base para el sistema de IA colaborativo
    (embeddings, NER, generator, data, scripts, etc.)
    """

    estructura = [
        f"{base_dir}/models/embeddings",
        f"{base_dir}/models/ner",
        f"{base_dir}/models/generator",
        f"{base_dir}/data/pdfs",
        f"{base_dir}/data/chunks",
        f"{base_dir}/data/index",
        f"{base_dir}/scripts",
        f"{base_dir}/logs"
    ]

    for path in estructura:
        os.makedirs(path, exist_ok=True)

    # Crear un archivo README interno
    readme_path = os.path.join(base_dir, "README.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(
            "=== ESTRUCTURA BASE - PROYECTO COLABORATIVE ===\n"
            "Carpetas creadas para el sistema de análisis colaborativo local.\n\n"
            "models/embeddings/ → modelos de embeddings (MiniLM, BGE)\n"
            "models/ner/        → modelos NER o de clasificación semántica (BETO, BERT)\n"
            "models/generator/  → modelos de generación y resumen (FLAN-T5)\n"
            "data/pdfs/         → documentos fuente (PDF, DOCX)\n"
            "data/chunks/       → fragmentos de texto procesados\n"
            "data/index/        → índices FAISS o Chroma\n"
            "scripts/           → scripts Python del sistema\n"
            "logs/              → registros y errores del sistema\n"
        )

    print(f"✅ Estructura creada correctamente en: {os.path.abspath(base_dir)}")

# ============================================================
# DESCARGA DE MODELOS
# ============================================================

BASE_DIR = "colaborative/models"

MODELOS = {
    "embeddings": {
        "repo": "sentence-transformers/all-MiniLM-L6-v2",
        "local": f"{BASE_DIR}/embeddings/all-MiniLM-L6-v2"
    },
    "ner": {
        "repo": "mrm8488/bert-spanish-cased-finetuned-ner",  # reemplazo seguro y público
        "local": f"{BASE_DIR}/ner/bert-spanish-cased-finetuned-ner"
    },
    "generator": {
        "repo": "google/flan-t5-base",
        "local": f"{BASE_DIR}/generator/flan-t5-base"
    }
}


def descargar_modelos():
    print("📦 Iniciando descarga de modelos para entorno local...\n")

    for nombre, info in MODELOS.items():
        print(f"🔹 Descargando modelo: {nombre.upper()}")
        print(f"   Repositorio: {info['repo']}")
        print(f"   Carpeta destino: {info['local']}")
        os.makedirs(info["local"], exist_ok=True)

        snapshot_download(repo_id=info["repo"], local_dir=info["local"])

        print(f"✅ {nombre} descargado correctamente.\n")

    print("🎯 Todos los modelos fueron descargados y almacenados en:")
    print(f"   → {os.path.abspath(BASE_DIR)}\n")
    print("🚀 Ahora podés usar tus scripts en modo totalmente offline.")

# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================

if __name__ == "__main__":
    crear_estructura_base()
    descargar_modelos()
