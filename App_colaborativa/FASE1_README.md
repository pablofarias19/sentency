# Fase 1: Sistema de Análisis de Pensamiento Judicial - Argentina

## 🎯 Implementación Completada

La Fase 1 establece los fundamentos del sistema de análisis judicial argentino con:

✅ Esquema de base de datos completo (5 tablas + vistas + índices)
✅ Script de inicialización de BD
✅ Extractor automático de metadata argentina
✅ Sistema de ingesta de sentencias
✅ Soporte para PDF y TXT
✅ Chunking automático del texto
✅ Creación automática de perfiles de jueces

## 📁 Archivos Creados

### 1. Esquema de Base de Datos
**Archivo**: `colaborative/scripts/schema_juez_centrico_arg.sql`

Contiene:
- **5 tablas principales**:
  - `perfiles_judiciales_argentinos` (80+ campos)
  - `sentencias_por_juez_arg` (metadata procesal completa)
  - `lineas_jurisprudenciales`
  - `redes_influencia_judicial`
  - `factores_predictivos`
- **15+ índices** para optimización
- **3 vistas útiles** para consultas frecuentes

### 2. Inicializador de Base de Datos
**Archivo**: `colaborative/scripts/inicializar_bd_judicial.py`

**Características**:
- Crea la base de datos SQLite
- Ejecuta el esquema SQL completo
- Verifica integridad de la BD
- Permite insertar datos de ejemplo para testing
- Backup automático si la BD ya existe

**Uso**:
```bash
cd App_colaborativa/colaborative/scripts

# Inicializar la base de datos
python inicializar_bd_judicial.py

# Solo verificar integridad
python inicializar_bd_judicial.py --verify

# Forzar recreación sin preguntar
python inicializar_bd_judicial.py --force
```

### 3. Extractor de Metadata Argentina
**Archivo**: `colaborative/scripts/extractor_metadata_argentina.py`

**Extrae automáticamente**:
- ✅ Número de expediente
- ✅ Carátula del caso
- ✅ Fecha de sentencia
- ✅ Juez/Jueces (individual o sala)
- ✅ Fuero (laboral, civil, penal, etc.)
- ✅ Tribunal
- ✅ Jurisdicción (federal/provincial)
- ✅ Tipo de sentencia
- ✅ Actor y demandado
- ✅ Materia del caso
- ✅ Resultado (hace lugar/rechaza)

**Características**:
- **30+ patrones regex** específicos para formato argentino
- Normalización de fueros comunes
- Detección de salas y tribunales colegiados
- Cálculo de confianza de extracción
- Validación de metadata

**Uso como módulo**:
```python
from extractor_metadata_argentina import ExtractorMetadataArgentina

extractor = ExtractorMetadataArgentina()
metadata = extractor.extraer_metadata(texto_sentencia, "archivo.pdf")

# Ver metadata
extractor.imprimir_metadata(metadata)

# Validar
es_valido, errores = extractor.validar_metadata(metadata)

# Exportar a JSON
extractor.exportar_json(metadata, "metadata.json")
```

### 4. Ingestor de Sentencias
**Archivo**: `colaborative/scripts/ingesta_sentencias_judicial.py`

**Funcionalidades**:
- Procesa PDF y TXT
- Extrae texto automáticamente
- Extrae metadata argentina
- Hace chunking del texto (1000 tokens, overlap 300)
- Crea perfil básico de juez si no existe
- Guarda en base de datos judicial
- Actualiza contadores automáticamente

**Uso**:
```bash
cd App_colaborativa/colaborative/scripts

# Procesar un solo archivo
python ingesta_sentencias_judicial.py /ruta/a/sentencia.pdf

# Procesar un directorio completo de PDFs
python ingesta_sentencias_judicial.py /ruta/a/directorio/pdfs

# Procesar TXT en lugar de PDF
python ingesta_sentencias_judicial.py /ruta/a/directorio --extension .txt

# Mostrar estadísticas al final
python ingesta_sentencias_judicial.py /ruta/a/directorio --stats
```

## 🚀 Guía de Uso Rápido

### Paso 1: Inicializar la Base de Datos

```bash
cd App_colaborativa/colaborative/scripts
python inicializar_bd_judicial.py
```

**Salida esperada**:
```
==================================================================
  INICIALIZACIÓN DE BASE DE DATOS JUDICIAL ARGENTINA
==================================================================

✓ Archivo de esquema encontrado: schema_juez_centrico_arg.sql
✓ Directorio existe: /path/to/bases_rag/cognitiva
✓ Esquema ejecutado exitosamente

Tablas creadas (5):
  • factores_predictivos
  • lineas_jurisprudenciales
  • perfiles_judiciales_argentinos
  • redes_influencia_judicial
  • sentencias_por_juez_arg

✓ Base de datos inicializada correctamente
```

### Paso 2: Preparar Sentencias

Coloca tus sentencias en:
- `App_colaborativa/colaborative/data/pdfs/` (para PDFs)
- `App_colaborativa/colaborative/data/txt/` (para TXT)

O usa cualquier otro directorio.

### Paso 3: Ingestar Sentencias

```bash
# Ejemplo: procesar todas las sentencias PDF de un directorio
python ingesta_sentencias_judicial.py ../data/pdfs/ --stats
```

**Salida esperada**:
```
======================================================================
PROCESANDO 5 ARCHIVOS
======================================================================

Procesando: sentencia_001.pdf
✓ Texto extraído: 15234 caracteres
✓ Metadata extraída (confianza: 85%)
✓ Chunks creados: 18
✓ Perfil creado para: Dr. Juan Pérez
✓ Sentencia guardada: SENT_12345_2023

[... más sentencias ...]

======================================================================
RESUMEN
======================================================================
Exitosos: 4
Fallidos: 1
Total: 5

======================================================================
ESTADÍSTICAS DE LA BASE DE DATOS
======================================================================

Total de jueces: 3
Total de sentencias: 4

Sentencias por fuero:
  • laboral: 2
  • civil: 1
  • penal: 1

Top 5 jueces por cantidad de sentencias:
  • Dr. Juan Pérez: 2
  • Dra. María González: 1
  • Dr. Carlos López: 1
```

### Paso 4: Verificar la Base de Datos

Puedes verificar que todo se guardó correctamente:

```bash
python inicializar_bd_judicial.py --verify
```

O usando SQLite directamente:

```bash
cd App_colaborativa/colaborative/bases_rag/cognitiva
sqlite3 juez_centrico_arg.db

# Ver jueces
SELECT juez, total_sentencias_analizadas, fuero FROM perfiles_judiciales_argentinos;

# Ver sentencias
SELECT sentencia_id, juez, expediente, fecha_sentencia FROM sentencias_por_juez_arg;

# Salir
.quit
```

## 📊 Estructura de la Base de Datos

### Tabla: perfiles_judiciales_argentinos

Campos principales:
- **Identificación**: juez, tipo_entidad, fuero, tribunal, jurisdicción
- **Análisis Cognitivo**: 20+ campos heredados del sistema existente
- **Análisis Judicial**: tendencia_activismo, interpretación_normativa, protección_derechos
- **Estándares Probatorios**: estandar_prueba_preferido, rigurosidad_probatoria
- **Fuentes del Derecho**: peso_ley, peso_jurisprudencia, frecuencia_cita_csjn
- **Sesgos Argentinos**: sesgo_pro_trabajador, sesgo_garantista, etc.
- **Métricas**: coherencia_interna, impacto_jurisprudencial, originalidad

### Tabla: sentencias_por_juez_arg

Campos principales:
- **Identificación**: sentencia_id, juez, expediente, carátula
- **Procesal**: fecha_sentencia, tipo_sentencia, materia, resultado
- **Partes**: actor, demandado, terceros
- **Tribunal**: fuero, instancia, jurisdicción, tribunal
- **Contenido**: texto_completo, ruta_chunks
- **Análisis**: perfil_cognitivo, razonamientos_identificados, falacias_detectadas
- **Citas**: normas_citadas, jurisprudencia_citada, doctrina_citada

### Tabla: lineas_jurisprudenciales

Campos principales:
- **Identificación**: juez, tema, materia
- **Sentencias**: sentencias_ids (JSON array)
- **Criterio**: criterio_dominante, fundamento_principal
- **Consistencia**: consistencia_score, excepciones_identificadas
- **Predictibilidad**: factores_predictivos, casos_tipo

### Tabla: redes_influencia_judicial

Campos principales:
- **Relación**: juez_origen, juez_destino, tipo_influencia
- **Evidencia**: sentencias_evidencia, cantidad_citas
- **Contexto**: temas_comunes, coincidencia_criterio

### Tabla: factores_predictivos

Campos principales:
- **Identificación**: juez, materia, tema
- **Factor**: factor, peso, confianza
- **Evidencia**: sentencias_sustento, ejemplos

## 🔍 Validación de Metadata

El extractor calcula una **confianza de extracción** basada en:
- ✅ Expediente identificado
- ✅ Fecha de sentencia identificada
- ✅ Juez identificado
- ✅ Fuero identificado
- ✅ Actor identificado
- ✅ Demandado identificado

**Confianza alta (>80%)**: Todos los campos principales extraídos
**Confianza media (50-80%)**: Algunos campos principales extraídos
**Confianza baja (<50%)**: Pocos campos extraídos, requiere revisión manual

## ⚠️ Casos Especiales

### Sentencias con Múltiples Jueces (Salas)

El sistema detecta automáticamente salas y tribunales colegiados:

```
tipo_entidad = 'sala'
juez = 'Dr. Juan Pérez, Dra. María González, Dr. Carlos López'
```

### Sentencias sin Expediente Claro

Si no se puede extraer el expediente, se genera un ID basado en el hash del archivo:

```
sentencia_id = 'SENT_a1b2c3d4e5f6'
```

### Texto Muy Corto

Si el texto extraído tiene menos de 100 caracteres, se rechaza:

```
⚠ Texto vacío o muy corto en: archivo.pdf
```

## 🐛 Troubleshooting

### Error: "Base de datos no encontrada"

**Solución**: Ejecutar primero el inicializador:
```bash
python inicializar_bd_judicial.py
```

### Error: "No se pudo extraer texto de PDF"

**Causas posibles**:
- PDF escaneado (imagen, no texto)
- PDF corrupto
- Falta librería PyPDF2

**Solución**: Convertir PDF a TXT manualmente y procesar el TXT.

### Advertencia: "Metadata con baja confianza"

**Solución**: Revisar manualmente el archivo y verificar:
- ¿Está en formato de sentencia argentina?
- ¿Tiene la estructura esperada?
- ¿Está completo el texto?

### Error: "UNIQUE constraint failed"

**Causa**: La sentencia ya existe en la base de datos.

**Solución**: Normal, el sistema evita duplicados automáticamente.

## 📈 Próximos Pasos (Fase 2)

Una vez completada la Fase 1, la Fase 2 implementará:

1. **Analizador de Pensamiento Judicial** (`analizador_pensamiento_judicial_arg.py`)
   - Detección de activismo judicial
   - Análisis de protección de derechos
   - Estándares probatorios aplicados
   - Tests y doctrinas argentinas

2. **Integración con ANALYSER v2.0**
   - Análisis cognitivo completo de cada sentencia
   - Actualización de perfiles judiciales

3. **Agregación de Perfiles**
   - Combinar análisis de múltiples sentencias
   - Calcular métricas agregadas por juez

## 📝 Notas Técnicas

### Formato de Chunks

Los chunks se guardan en:
- **Base de datos**: Ruta al archivo JSON en campo `ruta_chunks`
- **Archivo físico**: `data/chunks/SENT_xxxxx_chunks.json`

Formato JSON:
```json
[
  "texto del chunk 1...",
  "texto del chunk 2...",
  "..."
]
```

### IDs de Sentencias

Formato: `SENT_<expediente_normalizado>` o `SENT_<hash>`

Ejemplos:
- `SENT_12345_2023` (basado en expediente "12345/2023")
- `SENT_a1b2c3d4e5f6` (basado en hash de archivo)

### Fechas

Formato ISO 8601: `YYYY-MM-DD`

Ejemplo: `2024-03-15`

## 🔧 Configuración Avanzada

### Cambiar Parámetros de Chunking

Editar en `ingesta_sentencias_judicial.py`:

```python
CHUNK_TOKENS = 1000  # Tamaño de cada chunk
STEP_TOKENS = 300    # Overlap entre chunks
```

### Cambiar Ubicación de la BD

Editar en `ingesta_sentencias_judicial.py`:

```python
DB_FILE = Path("/ruta/personalizada/juez_centrico_arg.db")
```

## 📚 Referencias

- **Propuesta Completa**: `PROPUESTA_AJUSTADA_JUECES_ARG.md`
- **Esquema SQL**: `colaborative/scripts/schema_juez_centrico_arg.sql`
- **Sistema Existente**: `colaborative/scripts/analyser_metodo_mejorado.py`

## ✅ Checklist de Fase 1

- [x] Esquema de base de datos diseñado
- [x] Script de inicialización creado
- [x] Extractor de metadata implementado
- [x] Sistema de ingesta funcional
- [x] Soporte para PDF y TXT
- [x] Chunking automático
- [x] Creación automática de perfiles de jueces
- [x] Validación de metadata
- [x] Manejo de errores robusto
- [x] Documentación completa

## 🎉 ¡Fase 1 Completada!

El sistema está listo para ingestar sentencias argentinas y almacenarlas de forma estructurada. La Fase 2 añadirá el análisis cognitivo y judicial completo.

---

**Versión**: 1.0
**Fecha**: 2025-11-12
**Autor**: Sistema de Análisis de Pensamiento Judicial Argentina
