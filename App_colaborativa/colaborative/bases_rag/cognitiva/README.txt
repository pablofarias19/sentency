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
