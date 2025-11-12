# ⚖️ Sistema de Análisis de Pensamiento Judicial Argentino

**Sistema Completo de Análisis Cognitivo y Predictivo de Jueces**

---

## 🎯 ¿Qué es este sistema?

Un sistema integral que analiza el **pensamiento judicial** de jueces argentinos a partir de sus sentencias, utilizando:

- **Análisis Cognitivo** (ANALYSER v2.0) - Cómo piensan los jueces
- **Análisis Judicial** - Características específicas del sistema argentino
- **RAG Semántico** - Búsqueda inteligente de sentencias
- **Machine Learning** - Predicción de decisiones
- **Generación de Informes** - Informes completos automatizados
- **Sistema de Preguntas** - 140 preguntas predeterminadas sobre cada juez

---

## 🚀 Inicio Rápido

### 1. Inicializar el Sistema

```bash
cd App_colaborativa/colaborative/scripts

# Crear base de datos
python inicializar_bd_judicial.py

# Verificar que se creó correctamente
ls -lh ../bases_rag/cognitiva/juez_centrico_arg.db
```

### 2. Ingestar Sentencias

```bash
# Ingestar sentencias desde directorio
python ingesta_sentencias_judicial.py /ruta/a/sentencias/

# Las sentencias pueden ser PDF o TXT
# Ejemplo de estructura:
#   /sentencias/
#     ├── sentencia_juez_perez_001.pdf
#     ├── sentencia_juez_perez_002.pdf
#     └── sentencia_sala_5_001.pdf
```

### 3. Procesar y Analizar

```bash
# Procesar todas las sentencias con análisis completo
python procesador_sentencias_completo.py --todos

# O procesar un juez específico
python procesador_sentencias_completo.py "Dr. Juan Pérez"
```

### 4. Construir Líneas y Redes

```bash
# Analizar líneas jurisprudenciales
python analizador_lineas_jurisprudenciales.py --todos

# Analizar redes de influencia
python analizador_redes_influencia.py --todos
```

### 5. Entrenar Modelos Predictivos

```bash
# Entrenar modelos de ML para todos los jueces
python motor_predictivo_judicial.py --todos

# O para un juez específico
python motor_predictivo_judicial.py "Dr. Juan Pérez"
```

### 6. Generar Informes

```bash
# Generar informe completo
python generador_informes_judicial.py "Dr. Juan Pérez"

# Generar en JSON
python generador_informes_judicial.py "Dr. Juan Pérez" --formato json

# Responder las 140 preguntas
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --todas
```

---

## 🌐 Interfaz Web

### Iniciar la Webapp

```bash
cd App_colaborativa/colaborative/scripts
python end2end_webapp.py
```

Abre automáticamente el navegador en: **http://127.0.0.1:5002**

### Rutas Disponibles

#### Sistema Judicial (Nuevo)
- **`/jueces`** - Listado de todos los jueces
- **`/juez/<nombre>`** - Perfil completo del juez
- **`/cognitivo/<nombre>`** - Análisis cognitivo (ANALYSER)
- **`/lineas/<nombre>`** - Líneas jurisprudenciales
- **`/red/<nombre>`** - Red de influencias (CSJN, tribunales, doctrina)
- **`/prediccion/<nombre>`** - Análisis predictivo
- **`/informes`** - Generador de informes
- **`/preguntas/<nombre>`** - Sistema de 140 preguntas

#### Sistema RAG (Preexistente, adaptado)
- **`/`** - Búsqueda semántica de sentencias
- **`/upload`** - Subir nuevas sentencias
- **`/cognitivo`** - Análisis cognitivo general

---

## 📁 Estructura del Sistema

```
sentency/
├── App_colaborativa/
│   └── colaborative/
│       ├── bases_rag/
│       │   └── cognitiva/
│       │       ├── juez_centrico_arg.db      ⚖️ Base de datos judicial (principal)
│       │       └── modelos_predictivos/       🤖 Modelos ML por juez
│       │
│       └── scripts/
│           ├── [CORE - Infraestructura robusta]:
│           │   ├── analyser_metodo_mejorado.py       🧠 ANALYSER cognitivo v2.0
│           │   ├── analyser_judicial_adapter.py      🔗 Adaptador ANALYSER → jueces
│           │   ├── chunker_inteligente.py            ✂️ Chunking inteligente
│           │   ├── embeddings_fusion.py              🔢 Embeddings
│           │   ├── extractor_pdf_enriquecido.py      📄 Extracción de PDFs
│           │   ├── end2end_webapp.py                 🌐 Webapp principal
│           │   └── webapp_rutas_judicial.py          ⚖️ Rutas judiciales
│           │
│           ├── [JUDICIAL - Fase 1: Fundamentos]:
│           │   ├── schema_juez_centrico_arg.sql
│           │   ├── inicializar_bd_judicial.py
│           │   ├── extractor_metadata_argentina.py   🇦🇷 30+ patrones argentinos
│           │   └── ingesta_sentencias_judicial.py
│           │
│           ├── [JUDICIAL - Fase 2: Análisis]:
│           │   ├── analizador_pensamiento_judicial_arg.py  100+ patrones judiciales
│           │   ├── procesador_sentencias_completo.py
│           │   └── agregador_perfiles_jueces.py
│           │
│           ├── [JUDICIAL - Fase 3: Líneas y Redes]:
│           │   ├── analizador_lineas_jurisprudenciales.py
│           │   ├── extractor_citas_jurisprudenciales.py    CSJN, tribunales, doctrina
│           │   └── analizador_redes_influencia.py
│           │
│           ├── [JUDICIAL - Fase 4: Predictivo]:
│           │   └── motor_predictivo_judicial.py            🤖 Random Forest ML
│           │
│           └── [JUDICIAL - Fase 5: Informes]:
│               ├── generador_informes_judicial.py          📊 4 tipos de informes
│               ├── sistema_preguntas_judiciales.py         ❓ 140 preguntas
│               └── motor_respuestas_judiciales.py          🤖 Respuestas automáticas
│
└── [DOCUMENTACIÓN]:
    ├── README.md                                            📖 Este archivo
    ├── PLAN_MIGRACION_SISTEMA_JUDICIAL.md                  🗺️ Plan de migración
    ├── FASE1_README.md ... FASE5_README.md                  📚 Docs por fase
    └── PROPUESTA_AJUSTADA_JUECES_ARG.md                     📋 Propuesta original
```

---

## 🔧 Componentes del Sistema

### 1. ANALYSER Cognitivo v2.0 (Núcleo)

**Analiza cómo piensa el juez**:
- 14 tipos de razonamiento (deductivo, inductivo, abductivo, analógico...)
- Modalidad epistémica (certeza vs incertidumbre)
- Retórica (ethos, pathos, logos)
- Estilo literario
- Fuentes (legislación, jurisprudencia, doctrina)
- Sesgos valorativos

**Archivo**: `analyser_metodo_mejorado.py` (2000+ líneas)
**Adaptador**: `analyser_judicial_adapter.py`

### 2. Análisis Judicial Argentino

**Analiza características judiciales específicas**:
- Activismo vs restricción judicial
- Formalismo vs sustancia
- Métodos interpretativos
- Protección de derechos (6 dimensiones)
- Tests y doctrinas (proporcionalidad, razonabilidad, in dubio pro operario...)
- Sesgos argentinos (pro-trabajador, garantista, pro-consumidor...)

**Archivo**: `analizador_pensamiento_judicial_arg.py` (100+ patrones)

### 3. Sistema RAG

**Búsqueda semántica de sentencias**:
- Embeddings con Sentence Transformers
- FAISS para búsqueda eficiente
- Chunking inteligente con overlap
- Metadata enriquecida

**Archivos**:
- `embeddings_fusion.py`
- `chunker_inteligente.py`

### 4. Líneas Jurisprudenciales

**Identifica patrones consistentes**:
- Agrupa sentencias por tema
- Calcula consistencia
- Identifica criterio dominante
- Detecta casos paradigmáticos y excepciones

**Archivo**: `analizador_lineas_jurisprudenciales.py`

### 5. Redes de Influencia

**Mapea influencias intelectuales**:
- Citas a CSJN (Fallos: XXX:YYY)
- Citas a tribunales superiores
- Citas a autores doctrinales
- Intensidad de influencia

**Archivo**: `analizador_redes_influencia.py`

### 6. Motor Predictivo (ML)

**Predice decisiones con Machine Learning**:
- Random Forest Classifier
- 15+ factores extraídos automáticamente
- Feature importance
- Modelos persistentes por juez

**Archivo**: `motor_predictivo_judicial.py`

### 7. Generador de Informes

**Genera informes profesionales**:
- Informe completo (35-55 pág equiv.)
- Informe de línea jurisprudencial
- Informe de red de influencias
- Informe predictivo
- Formatos: TXT, JSON, Markdown

**Archivo**: `generador_informes_judicial.py`

### 8. Sistema de Preguntas

**140 preguntas predeterminadas en 8 categorías**:
- A. Perfil e Identidad (20)
- B. Metodología Interpretativa (20)
- C. Protección de Derechos (20)
- D. Líneas Jurisprudenciales (20)
- E. Red de Influencias (15)
- F. Análisis Predictivo (15)
- G. Sesgos y Tendencias (15)
- H. Casos Específicos (15)

**Archivos**:
- `sistema_preguntas_judiciales.py`
- `motor_respuestas_judiciales.py`

---

## 📊 Base de Datos

### Esquema Principal: `juez_centrico_arg.db`

**5 Tablas**:

1. **`perfiles_judiciales_argentinos`** (80+ campos)
   - Información básica (juez, fuero, jurisdicción, tribunal)
   - Perfil judicial (activismo, formalismo, interpretación)
   - Protección de derechos (6 dimensiones)
   - Tests y doctrinas
   - Sesgos argentinos
   - Métricas cognitivas

2. **`sentencias_por_juez_arg`**
   - Sentencias completas con metadata
   - Chunks para RAG
   - Expediente, carátula, partes, resultado

3. **`lineas_jurisprudenciales`**
   - Líneas consolidadas por juez y tema
   - Consistencia, criterio dominante
   - Casos paradigmáticos

4. **`redes_influencia_judicial`**
   - Relaciones entre juez origen y destino
   - Tipo (CSJN, tribunal, autor doctrinal)
   - Intensidad de influencia

5. **`factores_predictivos`**
   - Factores determinantes por juez
   - Pesos del modelo ML
   - Confianza

---

## 🎓 Casos de Uso

### 1. Litigante: Preparar Estrategia

```bash
# Conocer al juez antes de litigar
python generador_informes_judicial.py "Dr. Juan Pérez"

# Ver líneas jurisprudenciales en mi materia
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --pregunta D08

# Análisis predictivo
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --categoria F
```

### 2. Investigador: Análisis Académico

```bash
# Generar datos en JSON de múltiples jueces
for juez in "Dr. Pérez" "Dra. González" "Dr. Rodríguez"; do
    python generador_informes_judicial.py "$juez" --formato json
done

# Análisis comparativo posterior con scripts propios
```

### 3. Estudio Jurídico: Base de Conocimiento

```bash
# Responder todas las preguntas de jueces relevantes
cat lista_jueces.txt | while read juez; do
    python motor_respuestas_judiciales.py "$juez" --todas --formato json
done

# Integrar JSON a sistema de gestión
```

---

## 🔄 Pipeline Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. INGESTA                                                  │
│    sentencias PDF/TXT → extracción → metadata → chunks      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. ANÁLISIS DUAL                                            │
│    • ANALYSER Cognitivo (razonamiento, retórica, fuentes)  │
│    • Análisis Judicial (activismo, derechos, sesgos)       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. AGREGACIÓN                                               │
│    Múltiples sentencias → perfil consolidado del juez       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. LÍNEAS Y REDES                                           │
│    • Líneas jurisprudenciales por tema                      │
│    • Red de influencias (CSJN, tribunales, doctrina)       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. PREDICCIÓN                                               │
│    Random Forest → factores determinantes → predicción      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. INFORMES                                                 │
│    Generación automática de informes + 140 preguntas        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 Métricas y Análisis

### Perfil Judicial Completo

Para cada juez se obtiene:

**Cognitivo** (vía ANALYSER):
- Razonamiento dominante
- Modalidad epistémica
- Retórica (ethos/pathos/logos)
- Estilo literario
- Densidad de citas

**Judicial** (específico argentino):
- Activismo (-1 a +1)
- Formalismo (0 a 1)
- Interpretación (literal, sistemática, teleológica, histórica)
- Protección de derechos (0 a 1 en 6 dimensiones)
- Tests aplicados (proporcionalidad, razonabilidad, etc.)
- Sesgos (pro-trabajador, garantista, etc.)

**Líneas** (consistencia):
- Temas consolidados
- Consistencia por tema (0 a 1)
- Criterios dominantes
- Casos paradigmáticos

**Red** (influencias):
- Top fuentes CSJN
- Tribunales más citados
- Autores doctrinales preferidos

**Predictivo** (ML):
- Factores determinantes
- Feature importance
- Accuracy del modelo

---

## 🛠️ Tecnologías

- **Python 3.8+**
- **Flask** - Webapp
- **SQLite** - Base de datos
- **Sentence Transformers** - Embeddings
- **FAISS** - Búsqueda vectorial
- **scikit-learn** - Random Forest
- **Regex avanzado** - Extracción de patrones
- **PyMuPDF / PyPDF2** - Procesamiento de PDFs

---

## 📚 Documentación Adicional

- **[PLAN_MIGRACION_SISTEMA_JUDICIAL.md](PLAN_MIGRACION_SISTEMA_JUDICIAL.md)** - Cómo se integró el sistema
- **[FASE1_README.md](App_colaborativa/FASE1_README.md)** - Fundamentos y BD
- **[FASE2_README.md](App_colaborativa/FASE2_README.md)** - Análisis judicial
- **[FASE3_README.md](App_colaborativa/FASE3_README.md)** - Líneas y redes
- **[FASE4_README.md](App_colaborativa/FASE4_README.md)** - ML predictivo
- **[FASE5_README.md](App_colaborativa/FASE5_README.md)** - Informes y preguntas

---

## ⚠️ Notas Importantes

### Requisitos Mínimos

- 5+ sentencias por juez para análisis confiable
- 10+ sentencias para líneas jurisprudenciales consolidadas
- 15+ sentencias para modelo predictivo robusto

### Formato de Sentencias

Las sentencias deben estar en PDF o TXT con:
- Nombre del archivo indicativo del juez (ej: `sentencia_perez_001.pdf`)
- O metadata en el texto (expediente, carátula, juez)

### Procesamiento

- Primera ingesta: ~30 seg/sentencia (extracción + chunking + embeddings)
- Análisis completo: ~10 seg/sentencia (cognitivo + judicial)
- Generación de informes: ~5 seg

---

## 🚀 Roadmap Futuro

- [ ] Integración con APIs de tribunales argentinos
- [ ] Análisis temporal (evolución del juez en el tiempo)
- [ ] Comparación entre jueces del mismo fuero
- [ ] Visualizaciones 3D de redes de influencia
- [ ] Exportación de informes a PDF con gráficos
- [ ] API REST para integración con otros sistemas

---

## 👥 Contribuir

El sistema es modular y extensible. Para agregar nuevas funcionalidades:

1. **Nuevos patrones de análisis**: Editar `analizador_pensamiento_judicial_arg.py`
2. **Nuevas métricas**: Agregar campos en `schema_juez_centrico_arg.sql`
3. **Nuevos informes**: Extender `generador_informes_judicial.py`
4. **Nuevas preguntas**: Agregar en `sistema_preguntas_judiciales.py`

---

## 📄 Licencia

Sistema de Análisis de Pensamiento Judicial Argentino
© 2025

---

## 🎯 Contacto y Soporte

Para reportar issues o solicitar features, crear issue en el repositorio.

---

**Versión**: 1.0
**Última actualización**: 12 Noviembre 2025
**Estado**: Sistema completo y funcional ✅
