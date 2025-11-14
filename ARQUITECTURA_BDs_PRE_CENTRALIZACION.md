# ARQUITECTURA DE BASES DE DATOS - SISTEMA PRE-CENTRALIZACIÓN

**Fecha del análisis:** 14 Noviembre 2025
**Commit de referencia de cambio:** `5babc7a` (Eliminación de 4 BDs del sistema de autores)
**Estado:** Documentación histórica - Sistema ANTERIOR a centralización judicial

---

## 1. RESUMEN EJECUTIVO

El sistema original operaba con una **arquitectura multi-BD distribuida** compuesta por 8-10 bases de datos especializadas, cada una cumpliendo roles específicos en el análisis cognitivo y literario de obras y autores.

### Características principales:
- **8-10 bases de datos SQLite** distribuidas
- **Sincronización manual** entre múltiples niveles
- **Análisis multi-capa** almacenado en tablas complejas
- **Orientación autor-céntrica** para análisis de obras literarias/doctrinales
- **Volumen total:** ~690 KB de datos estructurados
- **Arquitectura de agregación:** documento → autor → central

---

## 2. LAS 4 BASES DE DATOS ELIMINADAS

### 2.1 `autor_centrico.db` (61,440 bytes)

**Ubicación:** `/App_colaborativa/colaborative/bases_rag/cognitiva/autor_centrico.db`

**Rol:** Base de datos CENTRAL del sistema autor-céntrico original. Punto de convergencia final de todos los análisis agregados por autor.

#### Esquema:

```sql
CREATE TABLE perfiles_autores (
    nombre_autor TEXT PRIMARY KEY,
    especialidad TEXT,
    institucion TEXT,
    obras_analizadas INTEGER,

    -- Métricas retóricas aristotélicas promediadas
    ethos_promedio REAL,
    pathos_promedio REAL,
    logos_promedio REAL,

    -- Análisis cognitivo agregado
    razonamiento_preferido TEXT,
    complejidad_promedio REAL,
    modalidad_preferida TEXT,

    -- Representación vectorial
    vector_perfil BLOB,  -- Embedding agregado

    -- Metadata consolidada
    metadatos_json TEXT,

    -- Timestamps
    fecha_creacion TIMESTAMP,
    fecha_actualizacion TIMESTAMP
);
```

#### Función en el flujo:
```
perfiles.db (agregación por autor)
        ↓ (sincronización)
autor_centrico.db (PUNTO DE CONSULTA ÚNICO)
        ↓
Webapp/API consultan aquí
```

#### Características:
- Una fila por autor
- Agregaba métricas de múltiples obras/documentos
- Servía como "single source of truth" para perfiles de autores
- Sincronizaba periódicamente desde `perfiles.db`

---

### 2.2 `perfiles_autorales.db` (20,480 bytes)

**Ubicación:** `/App_colaborativa/colaborative/bases_rag/cognitiva/perfiles_autorales.db`

**Rol:** Análisis cognitivo DETALLADO a nivel de documento. Tabla multidimensional con **50+ campos** de análisis por obra.

#### Esquema principal:

```sql
CREATE TABLE perfiles_autorales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento_id TEXT UNIQUE NOT NULL,
    nombre_archivo TEXT,
    autor_detectado TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- ========================================
    -- SECCIÓN 1: TIPOS DE RAZONAMIENTO (14)
    -- ========================================
    razonamiento_deductivo REAL DEFAULT 0.0,      -- Silogismos, inferencias lógicas
    razonamiento_inductivo REAL DEFAULT 0.0,      -- De casos particulares a general
    razonamiento_abductivo REAL DEFAULT 0.0,      -- Hipótesis explicativas
    razonamiento_analogico REAL DEFAULT 0.0,      -- Comparaciones y paralelismos
    razonamiento_teleologico REAL DEFAULT 0.0,    -- Finalidad y propósito
    razonamiento_sistemico REAL DEFAULT 0.0,      -- Pensamiento holístico
    razonamiento_autoritativo REAL DEFAULT 0.0,   -- Citas de autoridades
    razonamiento_a_contrario REAL DEFAULT 0.0,    -- Contraste de situaciones
    razonamiento_consecuencialista REAL DEFAULT 0.0, -- Análisis de consecuencias
    razonamiento_dialectico REAL DEFAULT 0.0,     -- Tesis-antítesis-síntesis
    razonamiento_hermeneutico REAL DEFAULT 0.0,   -- Interpretación textual
    razonamiento_historico REAL DEFAULT 0.0,      -- Contexto histórico
    razonamiento_economico_analitico REAL DEFAULT 0.0, -- Análisis económico
    razonamiento_reduccion_absurdo REAL DEFAULT 0.0,   -- Reductio ad absurdum

    -- ========================================
    -- SECCIÓN 2: MODALIDADES EPISTÉMICAS (7)
    -- ========================================
    modalidad_apodíctico REAL DEFAULT 0.0,        -- Certeza lógica absoluta
    modalidad_dialectico REAL DEFAULT 0.0,        -- Argumentación probabilística
    modalidad_retorico REAL DEFAULT 0.0,          -- Persuasión
    modalidad_sofístico REAL DEFAULT 0.0,         -- Argumentación aparente
    modalidad_certeza REAL DEFAULT 0.0,           -- Afirmaciones categóricas
    modalidad_incertidumbre REAL DEFAULT 0.0,     -- Expresiones dubitativas
    modalidad_hedging REAL DEFAULT 0.0,           -- Atenuación lingüística

    -- ========================================
    -- SECCIÓN 3: RETÓRICA ARISTOTÉLICA (3)
    -- ========================================
    retorica_ethos REAL DEFAULT 0.0,              -- Credibilidad del emisor
    retorica_pathos REAL DEFAULT 0.0,             -- Apelación emocional
    retorica_logos REAL DEFAULT 0.0,              -- Lógica y razonamiento

    -- ========================================
    -- SECCIÓN 4: ESTILOS LITERARIOS (8)
    -- ========================================
    estilo_tecnico_juridico REAL DEFAULT 0.0,
    estilo_ensayistico REAL DEFAULT 0.0,
    estilo_narrativo REAL DEFAULT 0.0,
    estilo_barroco REAL DEFAULT 0.0,
    estilo_minimalista REAL DEFAULT 0.0,
    estilo_aforistico REAL DEFAULT 0.0,
    estilo_impersonal_burocratico REAL DEFAULT 0.0,
    estilo_dialectico_critico REAL DEFAULT 0.0,

    -- ========================================
    -- SECCIÓN 5: ESTRUCTURAS ARGUMENTATIVAS (6)
    -- ========================================
    estructura_irac REAL DEFAULT 0.0,             -- Issue-Rule-Application-Conclusion
    estructura_toulmin REAL DEFAULT 0.0,          -- Claim-Data-Warrant
    estructura_issue_tree REAL DEFAULT 0.0,       -- Árbol de cuestiones
    estructura_defeasible REAL DEFAULT 0.0,       -- Argumentación derrotable
    estructura_burden_shift REAL DEFAULT 0.0,     -- Desplazamiento de carga probatoria
    estructura_silogistico_formal REAL DEFAULT 0.0, -- Silogismos formales

    -- ========================================
    -- SECCIÓN 6: MÉTRICAS GENERALES
    -- ========================================
    formalismo REAL DEFAULT 0.5,                  -- Nivel de formalidad
    creatividad REAL DEFAULT 0.5,                 -- Innovación conceptual
    empirismo REAL DEFAULT 0.5,                   -- Apego a evidencia
    dogmatismo REAL DEFAULT 0.5,                  -- Rigidez de posiciones
    interdisciplinariedad REAL DEFAULT 0.0,       -- Integración de disciplinas
    complejidad_sintactica REAL DEFAULT 0.5,      -- Complejidad de oraciones
    nivel_abstraccion REAL DEFAULT 0.5,           -- Concreción vs abstracción
    uso_jurisprudencia REAL DEFAULT 0.0,          -- Frecuencia de citas judiciales

    -- ========================================
    -- METADATA
    -- ========================================
    perfil_json TEXT,                             -- JSON completo del análisis
    procesado_con TEXT DEFAULT 'ANALYSER'         -- Sistema que lo procesó
);

-- ========================================
-- ÍNDICES PARA OPTIMIZACIÓN DE BÚSQUEDAS
-- ========================================
CREATE INDEX idx_perfiles_autorales_autor
    ON perfiles_autorales(autor_detectado);

CREATE INDEX idx_perfiles_autorales_archivo
    ON perfiles_autorales(nombre_archivo);

CREATE INDEX idx_perfiles_autorales_razonamiento
    ON perfiles_autorales(razonamiento_deductivo, razonamiento_inductivo);

CREATE INDEX idx_perfiles_autorales_creatividad
    ON perfiles_autorales(creatividad, formalismo);

CREATE INDEX idx_perfiles_autorales_estilo
    ON perfiles_autorales(estilo_tecnico_juridico, estilo_ensayistico);

CREATE INDEX idx_perfiles_autorales_fecha
    ON perfiles_autorales(fecha_creacion);
```

#### Función en el flujo:
```
metadatos.db (análisis ANALYSER)
        ↓
perfiles_autorales.db (detalle de 50+ dimensiones)
        ↓ (agregación por autor)
perfiles.db
```

#### Características distintivas:
- **50+ campos** de análisis multidimensional
- **6 índices** para búsquedas optimizadas
- Análisis granular de cada documento
- Base para agregaciones posteriores
- Almacenamiento denormalizado para consultas rápidas

---

### 2.3 `multicapa_pensamiento.db` (57,344 bytes)

**Ubicación:** `/App_colaborativa/colaborative/bases_rag/cognitiva/multicapa_pensamiento.db`

**Rol:** Análisis avanzado en **5 capas simultáneas** + firmas intelectuales + evolución temporal.

#### Esquema completo:

```sql
-- ========================================
-- TABLA 1: ANÁLISIS MULTI-CAPA (5 capas)
-- ========================================
CREATE TABLE analisis_multicapa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento_id TEXT UNIQUE NOT NULL,
    nombre_archivo TEXT,
    autor_detectado TEXT,

    -- CAPA 1: SEMÁNTICA
    -- Contenido conceptual del documento
    contenido_semantico TEXT,

    -- CAPA 2: COGNITIVA
    -- Patrones de razonamiento
    patron_razonamiento_dominante TEXT,
    distribucion_razonamiento TEXT,    -- JSON: {"deductivo": 0.4, "inductivo": 0.3, ...}
    marcadores_cognitivos TEXT,        -- JSON: [{"tipo": "...", "frecuencia": 0.x}, ...]
    nivel_certeza REAL,                -- 0-1
    uso_autoridad REAL,                -- 0-1
    reflexividad REAL,                 -- 0-1 (nivel de meta-cognición)

    -- CAPA 3: METODOLÓGICA
    -- Estructura argumentativa
    estructura_argumentativa TEXT,     -- IRAC, Toulmin, etc.
    tipo_introduccion TEXT,            -- Deductiva, inductiva, narrativa
    patron_desarrollo TEXT,            -- Lineal, espiral, dialéctico
    tipo_conclusion TEXT,              -- Síntesis, apertura, cierre categórico
    uso_ejemplos REAL,                 -- 0-1
    densidad_citas REAL,               -- 0-1

    -- CAPA 4: EVOLUTIVA
    -- Cambios temporales (si hay documentos previos)
    orden_cronologico INTEGER,
    cambios_desde_anterior TEXT,       -- JSON: {"conceptuales": [...], "metodologicos": [...]}
    innovaciones_conceptuales TEXT,    -- Nuevos conceptos introducidos
    abandonos_conceptuales TEXT,       -- Conceptos que ya no usa

    -- CAPA 5: RELACIONAL
    -- Relaciones con otros autores/obras
    autores_citados TEXT,              -- JSON: ["autor1", "autor2", ...]
    conceptos_compartidos TEXT,        -- JSON: {"autor": ["concepto1", ...]}
    divergencias_conceptuales TEXT,    -- JSON: {"autor": {"diverge_en": "..."}}

    -- METADATA
    fecha_analisis TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version_analisis TEXT DEFAULT '1.0'
);

CREATE INDEX idx_multicapa_autor ON analisis_multicapa(autor_detectado);
CREATE INDEX idx_multicapa_orden ON analisis_multicapa(orden_cronologico);

-- ========================================
-- TABLA 2: REDES CONCEPTUALES
-- ========================================
CREATE TABLE redes_conceptuales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    autor TEXT NOT NULL,
    concepto_central TEXT NOT NULL,
    conceptos_relacionados TEXT,       -- JSON: ["concepto1", "concepto2", ...]
    fuerza_relacion REAL,              -- 0-1
    contexto_uso TEXT,
    evolucion_concepto TEXT,           -- Cómo ha cambiado su uso en el tiempo

    UNIQUE(autor, concepto_central)
);

CREATE INDEX idx_redes_autor ON redes_conceptuales(autor);
CREATE INDEX idx_redes_concepto ON redes_conceptuales(concepto_central);

-- ========================================
-- TABLA 3: FIRMAS INTELECTUALES
-- ========================================
-- Una firma única por autor: sus características distintivas
CREATE TABLE firmas_intelectuales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    autor TEXT UNIQUE NOT NULL,

    -- FIRMA LINGÜÍSTICA
    vocabulario_distintivo TEXT,       -- JSON: ["término1", "término2", ...]
    estructuras_sintacticas TEXT,      -- JSON: {"tipo": "frecuencia"}
    marcadores_estilísticos TEXT,      -- JSON: rasgos estilísticos únicos

    -- FIRMA CONCEPTUAL
    conceptos_centrales TEXT,          -- JSON: ["concepto1", "concepto2", ...]
    relaciones_conceptuales TEXT,      -- JSON: grafo de relaciones
    innovaciones_terminologicas TEXT,  -- Términos que el autor acuñó

    -- FIRMA METODOLÓGICA
    secuencia_argumentativa TEXT,      -- Patrón típico de argumentación
    patron_evidencial TEXT,            -- Cómo usa evidencia
    estilo_refutacion TEXT,            -- Cómo refuta argumentos contrarios

    -- MÉTRICAS DE ORIGINALIDAD
    originalidad_lingüística REAL,     -- 0-1
    originalidad_conceptual REAL,      -- 0-1
    originalidad_metodologica REAL,    -- 0-1

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP
);

-- ========================================
-- TABLA 4: EVOLUCIÓN DEL PENSAMIENTO
-- ========================================
CREATE TABLE evolucion_pensamiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    autor TEXT NOT NULL,
    periodo_inicio TEXT,               -- Timestamp o descriptor
    periodo_fin TEXT,

    -- Qué cambió en este período
    cambios_conceptuales TEXT,         -- JSON: {"introduce": [...], "abandona": [...]}
    cambios_metodologicos TEXT,        -- JSON: cambios en método
    cambios_estilísticos TEXT,         -- JSON: cambios en estilo

    -- Continuidades
    conceptos_mantenidos TEXT,         -- JSON: conceptos que persisten

    -- Contexto
    obras_periodo TEXT,                -- JSON: obras de este período
    influencias_detectadas TEXT,       -- JSON: autores que influyeron

    fecha_analisis TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_evolucion_autor ON evolucion_pensamiento(autor);
```

#### Función en el flujo:
```
perfiles_autorales.db (análisis base)
        ↓
multicapa_pensamiento.db
  ├─ Capa 1: Semántica
  ├─ Capa 2: Cognitiva
  ├─ Capa 3: Metodológica
  ├─ Capa 4: Evolutiva
  └─ Capa 5: Relacional
        ↓
Firmas intelectuales extraídas
Redes conceptuales mapeadas
Evolución temporal registrada
        ↓
pensamiento_integrado_v2.db (consolidación)
```

#### Características distintivas:
- **4 tablas especializadas** coordinadas
- **5 capas de análisis simultáneo** en una tabla
- **Firmas intelectuales únicas** por autor
- **Grafos conceptuales** mapeados
- **Evolución temporal** registrada por períodos
- Análisis de **influencias** y **divergencias** conceptuales

---

### 2.4 `pensamiento_integrado_v2.db` (28,672 bytes)

**Ubicación:** `/App_colaborativa/colaborative/bases_rag/cognitiva/pensamiento_integrado_v2.db`

**Rol:** **Checkpoint de integración total**. Consolidación de TODOS los análisis en un único documento JSON por obra.

#### Esquema:

```sql
CREATE TABLE perfiles_completos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento_id TEXT UNIQUE NOT NULL,
    nombre_archivo TEXT,
    autor_detectado TEXT,
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- CAMPO CRÍTICO: JSON consolidado gigante
    perfil_completo TEXT NOT NULL
    -- Este JSON contiene:
    -- {
    --   "analisis_cognitivo": {...},      // De perfiles_autorales.db
    --   "analisis_multicapa": {           // De multicapa_pensamiento.db
    --     "capa_semantica": {...},
    --     "capa_cognitiva": {...},
    --     "capa_metodologica": {...},
    --     "capa_evolutiva": {...},
    --     "capa_relacional": {...}
    --   },
    --   "firma_intelectual": {...},       // De firmas_intelectuales
    --   "redes_conceptuales": [...],      // De redes_conceptuales
    --   "evolucion_temporal": {...},      // De evolucion_pensamiento
    --   "metadata": {
    --     "version": "2.0",
    --     "fecha_consolidacion": "...",
    --     "origen_datos": ["metadatos", "perfiles_autorales", "multicapa"]
    --   }
    -- }
);

CREATE INDEX idx_completos_autor ON perfiles_completos(autor_detectado);
CREATE INDEX idx_completos_archivo ON perfiles_completos(nombre_archivo);
CREATE INDEX idx_completos_fecha ON perfiles_completos(fecha_procesamiento);
```

#### Función en el flujo:
```
metadatos.db + perfiles_autorales.db + multicapa_pensamiento.db
        ↓ (integración)
pensamiento_integrado_v2.db
        ↓
Un JSON gigante por documento con TODO consolidado
        ↓
Se puede exportar/consultar como documento completo
```

#### Características distintivas:
- **Consolidación total** en un campo JSON
- **Checkpoint** de todos los análisis
- **Exportable** como documento completo
- **Versión 2.0** del sistema de integración
- Facilita **consultas holísticas** de un documento

---

## 3. BASES DE DATOS QUE PERMANECIERON

### 3.1 `metadatos.db` (260 KB - La más grande)

**Ubicación:** `/App_colaborativa/colaborative/bases_rag/cognitiva/metadatos.db`

**Rol:** Base de datos PRINCIPAL para análisis cognitivos a nivel de documento. Contiene output directo del sistema ANALYSER.

#### Esquema principal:

```sql
CREATE TABLE perfiles_cognitivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento_id TEXT UNIQUE NOT NULL,
    nombre_archivo TEXT,
    autor_detectado TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Nivel de análisis
    nivel TEXT DEFAULT 'documento',    -- 'documento', 'autor', 'conjunto'

    -- Embedding vectorial
    vector_path TEXT,                  -- Ruta al archivo .npy

    -- ANÁLISIS ANALYSER (Sistema actual)
    tipo_pensamiento TEXT,
    formalismo REAL,
    creatividad REAL,
    dogmatismo REAL,
    empirismo REAL,
    interdisciplinariedad REAL,
    nivel_abstraccion REAL,
    complejidad_sintactica REAL,
    uso_jurisprudencia REAL,
    tono TEXT,

    -- Retórica Aristotélica
    modalidad_epistemica TEXT,
    estructura_silogistica TEXT,
    ethos REAL,
    pathos REAL,
    logos REAL,

    -- Metadata
    perfil_json TEXT,                  -- JSON completo del análisis
    firma TEXT,                        -- Resumen caracterizador
    embedding BLOB,                    -- Vector embedding
    autor_confianza REAL,              -- Confianza en detección (0-1)
    archivo_fuente TEXT,
    total_palabras INTEGER,
    metadatos_completos TEXT           -- JSON con metadata adicional
);

CREATE TABLE patrones_pensamiento_profundo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    autor TEXT UNIQUE NOT NULL,
    patron_razonamiento TEXT,
    estructura_argumentativa TEXT,
    evolucion_temporal TEXT,           -- JSON
    conexiones_intelectuales TEXT,     -- JSON
    marcadores_cognitivos TEXT,        -- JSON
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP,
    version_sistema TEXT
);

CREATE INDEX idx_metadatos_autor ON perfiles_cognitivos(autor_detectado);
CREATE INDEX idx_metadatos_archivo ON perfiles_cognitivos(nombre_archivo);
CREATE INDEX idx_metadatos_tipo ON perfiles_cognitivos(tipo_pensamiento);
```

**Estado:** PERMANECE como BD principal en sistema judicial

---

### 3.2 `perfiles.db` (40 KB)

**Ubicación:** `/App_colaborativa/colaborative/data/perfiles.db`

**Rol:** Agregación de perfiles a NIVEL DE AUTOR (múltiples documentos → un autor)

#### Esquema:

```sql
CREATE TABLE perfiles_autores (
    nombre_autor TEXT PRIMARY KEY,
    especialidad TEXT,
    institucion TEXT,
    obras_analizadas INTEGER DEFAULT 0,

    -- Métricas promedio aristotélicas
    ethos_promedio REAL,
    pathos_promedio REAL,
    logos_promedio REAL,

    -- Análisis cognitivo agregado
    razonamiento_preferido TEXT,
    complejidad_promedio REAL,
    modalidad_preferida TEXT,

    -- Embedding agregado
    vector_perfil BLOB,

    -- Metadata
    metadatos_json TEXT,

    -- Timestamps
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP
);

CREATE INDEX idx_perfiles_especialidad ON perfiles_autores(especialidad);
CREATE INDEX idx_perfiles_obras ON perfiles_autores(obras_analizadas);
```

**Función en sincronización:**
```
metadatos.db (múltiples docs del mismo autor)
        ↓ (agregación)
perfiles.db (un registro por autor)
        ↓ (sincronización)
autor_centrico.db (punto de consulta central)
```

**Estado:** REEMPLAZADA por `perfiles_judiciales_argentinos` en `juez_centrico_arg.db`

---

### 3.3 `autoaprendizaje.db` (160 KB)

**Ubicación:** `/App_colaborativa/colaborative/data/autoaprendizaje.db`

**Rol:** Tracking de métricas del sistema y auto-mejora continua

#### Esquema:

```sql
CREATE TABLE metricas_sistema (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modulo TEXT NOT NULL,              -- ANALYSER, RAG, embedding, etc.
    metrica TEXT NOT NULL,             -- accuracy, speed, quality, etc.
    valor REAL NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contexto TEXT                      -- JSON con información adicional
);

CREATE TABLE autoevaluaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consulta_original TEXT,
    respuesta_generada TEXT,

    -- Métricas de calidad (0-1)
    precision_estimada REAL,
    completitud REAL,
    relevancia REAL,
    coherencia REAL,
    score_total REAL GENERATED ALWAYS AS
        ((precision_estimada + completitud + relevancia + coherencia) / 4) STORED,

    -- Contexto
    contexto_usado TEXT,               -- JSON: chunks usados
    mejoras_sugeridas TEXT,            -- JSON: sugerencias

    fecha_evaluacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_metricas_modulo ON metricas_sistema(modulo);
CREATE INDEX idx_metricas_fecha ON metricas_sistema(fecha_registro);
CREATE INDEX idx_autoevaluaciones_score ON autoevaluaciones(score_total);
```

**Estado:** ELIMINADA en sistema judicial (no tiene equivalente)

---

### 3.4 `cognitivo.db` (44 KB)

**Ubicación:** `/App_colaborativa/colaborative/data/cognitivo.db`

**Rol:** Espejo/backup de `metadatos.db` con estructura ligeramente diferente

#### Esquema:

```sql
-- Similar a metadatos.db pero con índices diferentes
CREATE TABLE perfiles_autorales (
    -- Campos similares a perfiles_cognitivos de metadatos.db
    -- Redundancia controlada para backup y consultas alternativas
    ...
);
```

**Estado:** REDUNDANCIA - descontinuada en sistema judicial

---

### 3.5 `ruta_pensamiento.db` (20 KB)

**Ubicación:** `/App_colaborativa/colaborative/data/ruta_pensamiento.db`

**Rol:** Mapeo de rutas/caminos conceptuales y evolución de ideas

#### Esquema conceptual:

```sql
CREATE TABLE rutas_conceptuales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concepto_origen TEXT,
    concepto_destino TEXT,
    autor TEXT,
    fuerza_conexion REAL,              -- 0-1
    contexto TEXT,
    tipo_relacion TEXT                 -- derivación, oposición, refinamiento
);

CREATE TABLE evolucion_conceptual (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concepto TEXT,
    autor TEXT,
    periodo_inicio TEXT,
    periodo_fin TEXT,
    cambios TEXT,                      -- JSON
    obras_involucradas TEXT            -- JSON
);
```

**Estado:** TRANSFORMADA en tabla `lineas_jurisprudenciales` en `juez_centrico_arg.db`

---

## 4. ARQUITECTURA DE FLUJO DE DATOS

### 4.1 Diagrama de flujo completo:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   INGESTA DE DOCUMENTOS (Libros/Obras)                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  NIVEL 1: ANÁLISIS BASE A NIVEL DE DOCUMENTO                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────┐                                              │
│  │  metadatos.db        │ ← Sistema ANALYSER ejecuta análisis          │
│  │  perfiles_cognitivos │                                              │
│  └──────────────────────┘                                              │
│       │                                                                 │
│       ├─ Tipo de pensamiento                                           │
│       ├─ Métricas: formalismo, creatividad, dogmatismo, empirismo      │
│       ├─ Retórica aristotélica: ethos, pathos, logos                   │
│       ├─ Modalidad epistémica                                          │
│       ├─ Embedding vectorial (FAISS)                                   │
│       └─ Metadata y confianza en autor                                 │
│                                                                         │
│  ┌──────────────────────┐                                              │
│  │  cognitivo.db        │ ← Espejo/redundancia de metadatos.db         │
│  │  perfiles_autorales  │                                              │
│  └──────────────────────┘                                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  NIVEL 2: ANÁLISIS DETALLADO MULTIDIMENSIONAL                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────┐                                         │
│  │  perfiles_autorales.db    │ ← 50+ campos de análisis                │
│  │  perfiles_autorales       │                                         │
│  └───────────────────────────┘                                         │
│       │                                                                 │
│       ├─ 14 tipos de razonamiento                                      │
│       ├─ 7 modalidades epistémicas                                     │
│       ├─ 8 estilos literarios                                          │
│       ├─ 6 estructuras argumentativas                                  │
│       ├─ Métricas generales (formalismo, creatividad, etc.)            │
│       └─ 6 ÍNDICES para búsquedas optimizadas                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  NIVEL 3: ANÁLISIS MULTI-CAPA AVANZADO                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────┐                                      │
│  │  multicapa_pensamiento.db    │                                      │
│  └──────────────────────────────┘                                      │
│       │                                                                 │
│       ├─ CAPA 1: SEMÁNTICA                                             │
│       │   └─ Contenido conceptual                                      │
│       │                                                                 │
│       ├─ CAPA 2: COGNITIVA                                             │
│       │   ├─ Patrón razonamiento dominante                             │
│       │   ├─ Distribución de razonamientos (JSON)                      │
│       │   ├─ Nivel de certeza, uso de autoridad                        │
│       │   └─ Reflexividad (meta-cognición)                             │
│       │                                                                 │
│       ├─ CAPA 3: METODOLÓGICA                                          │
│       │   ├─ Estructura argumentativa                                  │
│       │   ├─ Tipo introducción/desarrollo/conclusión                   │
│       │   └─ Uso de ejemplos, densidad de citas                        │
│       │                                                                 │
│       ├─ CAPA 4: EVOLUTIVA                                             │
│       │   ├─ Orden cronológico                                         │
│       │   ├─ Cambios desde anterior                                    │
│       │   └─ Innovaciones/abandonos conceptuales                       │
│       │                                                                 │
│       └─ CAPA 5: RELACIONAL                                            │
│           ├─ Autores citados                                           │
│           ├─ Conceptos compartidos                                     │
│           └─ Divergencias conceptuales                                 │
│                                                                         │
│  Tablas adicionales:                                                   │
│  ├─ redes_conceptuales: grafos de conceptos relacionados              │
│  ├─ firmas_intelectuales: características únicas del autor             │
│  └─ evolucion_pensamiento: cambios por períodos                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  NIVEL 3B: MAPEO DE RUTAS CONCEPTUALES                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────┐                                          │
│  │  ruta_pensamiento.db     │                                          │
│  └──────────────────────────┘                                          │
│       ├─ Grafos de relaciones entre conceptos                          │
│       ├─ Evolución temporal de ideas                                   │
│       └─ Trayectorias intelectuales                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  NIVEL 4: CONSOLIDACIÓN POR AUTOR                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────┐                                              │
│  │  perfiles.db         │ ← Agregación por autor                       │
│  │  perfiles_autores    │                                              │
│  └──────────────────────┘                                              │
│       │                                                                 │
│       ├─ N documentos del mismo autor → 1 registro                     │
│       ├─ Promedios: ethos, pathos, logos, complejidad                  │
│       ├─ Razonamiento preferido                                        │
│       ├─ Especialidad e institución                                    │
│       └─ Vector de perfil agregado                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  NIVEL 5: CONSOLIDACIÓN CENTRAL                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────┐                                      │
│  │  autor_centrico.db           │ ← PUNTO DE CONSULTA ÚNICO            │
│  │  perfiles_autores (CENTRAL)  │                                      │
│  └──────────────────────────────┘                                      │
│       │                                                                 │
│       ├─ Sincronización desde perfiles.db                              │
│       ├─ Sincronización desde metadatos.db                             │
│       ├─ "Single source of truth" para perfiles de autores             │
│       └─ Webapp/API consultan aquí                                     │
│                                                                         │
│  ┌────────────────────────────────────┐                                │
│  │  pensamiento_integrado_v2.db       │ ← CHECKPOINT TOTAL             │
│  │  perfiles_completos                │                                │
│  └────────────────────────────────────┘                                │
│       │                                                                 │
│       └─ JSON gigante por documento con TODO consolidado:              │
│           ├─ Análisis cognitivo (metadatos.db)                         │
│           ├─ Análisis detallado (perfiles_autorales.db)                │
│           ├─ Análisis multi-capa (multicapa_pensamiento.db)            │
│           ├─ Firmas intelectuales                                      │
│           ├─ Redes conceptuales                                        │
│           └─ Evolución temporal                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  NIVEL 6: APRENDIZAJE Y MEJORA CONTINUA                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────┐                                          │
│  │  autoaprendizaje.db      │                                          │
│  └──────────────────────────┘                                          │
│       ├─ metricas_sistema: tracking de módulos                         │
│       │   └─ ANALYSER, RAG, embedding, etc.                            │
│       ├─ autoevaluaciones: calidad de respuestas                       │
│       │   └─ Precisión, completitud, relevancia, coherencia            │
│       └─ Mejora continua basada en métricas                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Flujo de sincronización temporal:

```
TIEMPO T0: Nuevo documento ingresa
    ↓
T1: metadatos.db actualizada (análisis ANALYSER)
    ↓
T2: perfiles_autorales.db actualizada (50+ campos)
    ↓
T3: multicapa_pensamiento.db actualizada (5 capas)
    ↓
T4: ruta_pensamiento.db actualizada (grafos)
    ↓
T5: perfiles.db agregada (si hay suficientes docs del autor)
    ↓
T6: autor_centrico.db sincronizada (punto de consulta)
    ↓
T7: pensamiento_integrado_v2.db consolidada (checkpoint)
    ↓
T8: autoaprendizaje.db registra métricas

FRECUENCIA DE SINCRONIZACIÓN:
- T1-T4: Inmediata (por documento)
- T5-T6: Periódica (cada N documentos o tiempo X)
- T7: Al completar procesamiento de autor
- T8: Continua
```

---

## 5. TABLA COMPARATIVA: ANTES vs DESPUÉS

| Aspecto | ANTES (Multi-BD) | AHORA (Centralizada) |
|---------|------------------|----------------------|
| **Número de BDs** | 8-10 BDs distribuidas | 1 BD central (`juez_centrico_arg.db`) |
| **Volumen total** | ~690 KB | ~500 KB (proyectado) |
| **Sincronización** | Manual entre 8 BDs | Automática en campos denormalizados |
| **Niveles de agregación** | 6 niveles (doc → autor → central) | 2 niveles (sentencia → juez) |
| **Análisis multi-capa** | En tablas complejas (multicapa_pensamiento.db) | En código Python (analizador_pensamiento_judicial_arg.py) |
| **Redundancia** | Alta (cognitivo.db + metadatos.db) | Mínima (campos calculados) |
| **Complejidad arquitectónica** | Alta (8-10 puntos de sincronización) | Baja (5 tablas + 3 vistas) |
| **Orientación** | Autores literarios/doctrinales | Jueces y sentencias argentinas |
| **Checkpoint de integración** | pensamiento_integrado_v2.db | Campo JSON `perfil_cognitivo` en sentencias_por_juez_arg |
| **Evolutivo temporal** | evolucion_pensamiento (tabla) | lineas_jurisprudenciales (tabla) |
| **Firmas intelectuales** | firmas_intelectuales (tabla) | Integrado en `perfil_cognitivo` JSON |
| **Redes conceptuales** | redes_conceptuales (tabla) | Integrado en líneas jurisprudenciales |
| **Autoaprendizaje** | autoaprendizaje.db (160 KB) | NO EXISTE (eliminado) |
| **Punto de consulta único** | autor_centrico.db | juez_centrico_arg.db |

---

## 6. EQUIVALENCIAS EN SISTEMA JUDICIAL

### Mapeo de BDs eliminadas → Nuevas estructuras:

| BD Eliminada | Contenido | Equivalente en Sistema Judicial |
|--------------|-----------|----------------------------------|
| `autor_centrico.db` | Perfiles de autores consolidados | `perfiles_judiciales_argentinos` tabla |
| `perfiles_autorales.db` | 50+ campos de análisis por documento | `perfiles_judiciales_argentinos` (80+ campos) |
| `multicapa_pensamiento.db` | 5 capas de análisis | `analizador_pensamiento_judicial_arg.py` (código) |
| `pensamiento_integrado_v2.db` | JSON consolidado | `sentencias_por_juez_arg.perfil_cognitivo` (JSON) |

### Mapeo de tablas:

| Tabla Anterior | Nueva Tabla/Estructura |
|----------------|------------------------|
| `autor_centrico.perfiles_autores` | `perfiles_judiciales_argentinos` |
| `perfiles_autorales.perfiles_autorales` | `perfiles_judiciales_argentinos` (expandida) |
| `multicapa_pensamiento.analisis_multicapa` | Análisis en Python, no en BD |
| `multicapa_pensamiento.firmas_intelectuales` | Integrado en `perfil_cognitivo` JSON |
| `multicapa_pensamiento.redes_conceptuales` | `lineas_jurisprudenciales` |
| `multicapa_pensamiento.evolucion_pensamiento` | `lineas_jurisprudenciales` + `evolucion_lineas` |
| `pensamiento_integrado_v2.perfiles_completos` | `sentencias_por_juez_arg.perfil_cognitivo` |
| `ruta_pensamiento.rutas_conceptuales` | `lineas_jurisprudenciales` tabla |
| `perfiles.perfiles_autores` | `perfiles_judiciales_argentinos` |
| `autoaprendizaje.metricas_sistema` | NO EXISTE (eliminado) |

---

## 7. VOLÚMENES Y ESTADÍSTICAS

### Distribución de datos en sistema anterior:

```
metadatos.db (260 KB)          ██████████████████████████ 37.7%
autoaprendizaje.db (160 KB)    ████████████████ 23.2%
autor_centrico.db (61 KB)      ██████ 8.8%
multicapa_pensamiento.db (57KB)██████ 8.3%
cognitivo.db (44 KB)           ████ 6.4%
perfiles.db (40 KB)            ████ 5.8%
pensamiento_integrado_v2.db    ███ 4.2%
(28 KB)
perfiles_autorales.db (20 KB)  ██ 2.9%
ruta_pensamiento.db (20 KB)    ██ 2.9%
─────────────────────────────────────────────────
TOTAL: ~690 KB
```

### Filas estimadas por BD:

| BD | Filas estimadas | Comentario |
|----|----------------|------------|
| metadatos.db | 200-500 | Una por documento procesado |
| perfiles_autorales.db | 50-100 | Análisis detallado |
| multicapa_pensamiento.db | 50-100 | Análisis multi-capa |
| perfiles.db | 20-50 | Una por autor |
| autor_centrico.db | 20-50 | Una por autor (sincronizada) |
| pensamiento_integrado_v2.db | 50-100 | Checkpoint por documento |
| autoaprendizaje.db | 100-500 | Métricas continuas |
| cognitivo.db | 200-500 | Espejo de metadatos |
| ruta_pensamiento.db | 100-200 | Relaciones conceptuales |

---

## 8. SCRIPTS Y HERRAMIENTAS RELACIONADAS

### Scripts que operaban con estas BDs:

```bash
# Sincronización entre BDs
App_colaborativa/colaborative/scripts/sincronizar_perfiles.py
App_colaborativa/colaborative/scripts/actualizar_autor_centrico.py

# Análisis multi-capa
App_colaborativa/colaborative/scripts/analisis_multicapa.py
App_colaborativa/colaborative/scripts/extraer_firmas_intelectuales.py

# Consolidación
App_colaborativa/colaborative/scripts/consolidar_pensamiento.py
App_colaborativa/colaborative/scripts/generar_checkpoint.py

# Autoaprendizaje
App_colaborativa/colaborative/scripts/registrar_metricas.py
App_colaborativa/colaborative/scripts/autoevaluacion.py
```

**Estado de scripts:** Eliminados o refactorizados para sistema judicial

---

## 9. VENTAJAS Y DESVENTAJAS DE LA ARQUITECTURA ANTERIOR

### Ventajas:

1. **Separación de concerns:** Cada BD tenía un propósito específico
2. **Especialización:** Análisis complejos (5 capas) en BD dedicada
3. **Redundancia controlada:** cognitivo.db como backup
4. **Trazabilidad:** Múltiples niveles permitían debugging granular
5. **Flexibilidad:** Fácil añadir nuevas dimensiones de análisis
6. **Checkpoint integrado:** pensamiento_integrado_v2.db consolidaba todo

### Desventajas:

1. **Complejidad de sincronización:** 8-10 BDs requieren coordinación manual
2. **Riesgo de inconsistencias:** Sincronización manual propensa a errores
3. **Overhead de mantenimiento:** Múltiples esquemas que mantener
4. **Performance:** Consultas multi-BD más lentas
5. **Dificultad de consultas:** Necesidad de JOIN entre BDs
6. **Redundancia excesiva:** Datos duplicados entre BDs

---

## 10. RAZONES PARA LA CENTRALIZACIÓN

1. **Simplicidad arquitectónica:** De 8-10 BDs a 1 BD
2. **Reducción de sincronización:** Campos denormalizados eliminan sincronización
3. **Mejora de performance:** Consultas en una sola BD
4. **Consistencia garantizada:** Transacciones ACID en una BD
5. **Mantenimiento simplificado:** Un esquema unificado
6. **Adaptación a dominio judicial:** Estructura optimizada para jueces/sentencias
7. **Análisis en código:** Multicapa movido a Python (más flexible)

---

## 11. CONCLUSIONES

### Arquitectura Pre-Centralización:

La arquitectura multi-BD del sistema original era una solución **sofisticada pero compleja** diseñada para análisis literario/doctrinal de autores. Ofrecía:

- **Granularidad extrema:** 50+ dimensiones de análisis por documento
- **Análisis multi-capa:** 5 capas simultáneas (semántica, cognitiva, metodológica, evolutiva, relacional)
- **Firmas intelectuales:** Características únicas extraídas por autor
- **Evolución temporal:** Tracking de cambios conceptuales por períodos
- **Redes conceptuales:** Grafos de relaciones entre ideas
- **Autoaprendizaje:** Métricas de calidad y mejora continua

Sin embargo, su **complejidad de sincronización** y **redundancia** justificaron la consolidación en una arquitectura centralizada más simple y mantenible.

### Transición al Sistema Judicial:

El cambio de **autor-céntrico a juez-céntrico** implicó:

- **De 8-10 BDs a 1 BD centralizada**
- **De análisis en BD a análisis en código** (más flexible)
- **De 6 niveles de agregación a 2 niveles** (sentencia → juez)
- **De sincronización manual a denormalización inteligente**
- **Reducción de complejidad del 60%+**

---

## 12. REFERENCIAS

### Commits relevantes:

- `5babc7a`: Eliminación de 4 BDs principales del sistema autor-céntrico
- `0bd8f33`: Merge de refactorización judicial
- `084c06d`: Integración sistema judicial con infraestructura existente

### Archivos de esquema:

- `/App_colaborativa/colaborative/scripts/schema_juez_centrico_arg.sql` - Esquema nuevo centralizado
- `/App_colaborativa/colaborative/scripts/inicializar_bd_judicial.py` - Inicializador BD judicial

### Documentación relacionada:

- `PLAN_MIGRACION_SISTEMA_JUDICIAL.md` - Plan de migración detallado
- `LIMPIEZA_FINAL.md` - Documentación de archivos eliminados

---

**Documentación generada:** 14 Noviembre 2025
**Autor:** Sistema Claude Code
**Propósito:** Documentación histórica para referencia arquitectónica
