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
