INSTRUCCIONES PARA CARGAR DOCUMENTOS

1. ESTRUCTURA DE CARPETAS:
   - colaborative/data/pdfs/general/  → Documentos generales
   - colaborative/data/pdfs/civil/    → Documentos de derecho civil

2. FORMATO SOPORTADO:
   - Solo archivos PDF con texto extraíble
   - Evitar PDFs escaneados sin OCR

3. PROCESO DE INGESTA:
   a) Coloca archivos PDF en las carpetas correspondientes
   b) Ejecuta: python colaborative/scripts/ingesta_enriquecida.py
   c) El sistema procesará automáticamente todos los PDFs

4. QUÉ HACE LA INGESTA ENRIQUECIDA:
   - Extrae texto y estructura del documento
   - Analiza metodología jurídica y razonamiento
   - Detecta perfil cognitivo-autoral (marco, estrategia, autores)
   - Crea embeddings para búsqueda tradicional (FAISS_A)
   - Crea embeddings para perfiles cognitivos (FAISS_B)
   - Registra estadísticas en base de autoaprendizaje

5. VERIFICACIÓN:
   - Revisa logs en: colaborative/data/logs/
   - Consulta estadísticas en: http://127.0.0.1:5002/autoevaluaciones
