# Propuesta de Refactorización: Sistema Centrado en Jueces

## Resumen Ejecutivo

Transformar el sistema actual de análisis cognitivo de autores en un **Sistema de Análisis de Pensamiento Judicial** que relacione múltiples sentencias con jueces específicos, revelando patrones de razonamiento, evolución jurisprudencial y características del pensamiento judicial.

## Arquitectura Propuesta

### 1. Modelo de Datos

#### Base de Datos Principal: `juez_centrico.db`

**Tabla: `perfiles_judiciales_expandidos`**
```sql
CREATE TABLE perfiles_judiciales_expandidos (
    -- Identificación
    juez TEXT PRIMARY KEY,
    corte TEXT,
    periodo_activo TEXT,
    total_sentencias INTEGER,

    -- Análisis Cognitivo (del sistema actual)
    metodologia_principal TEXT,
    patron_razonamiento_dominante TEXT,
    estilo_argumentativo TEXT,
    estructura_discursiva TEXT,
    marcadores_linguisticos TEXT,
    vocabulario_especializado TEXT,
    densidad_conceptual REAL,
    complejidad_sintactica REAL,

    -- Retórica Aristotélica
    uso_ethos REAL,
    uso_pathos REAL,
    uso_logos REAL,

    -- Modalidad Epistémica
    modalidad_epistemica TEXT,

    -- Nuevas Métricas Judiciales
    tendencia_activismo REAL,  -- -1 (restricción) a +1 (activismo)
    interpretacion_constitucional TEXT,  -- originalista, evolutiva, mixta
    deferencia_legislativo REAL,  -- 0 a 1
    deferencia_ejecutivo REAL,   -- 0 a 1
    proteccion_derechos_fundamentales REAL,  -- 0 a 1

    -- Patrones de Votación
    tasa_mayoria REAL,
    tasa_disidencia REAL,
    tasa_concurrencia REAL,
    tasa_salvamento_voto REAL,

    -- Áreas de Especialización
    materias_principales TEXT,  -- JSON array
    expertise_score_por_materia TEXT,  -- JSON dict

    -- Influencia y Red
    jueces_que_cita TEXT,  -- JSON array
    jueces_que_lo_citan TEXT,  -- JSON array
    influencias_detectadas TEXT,
    escuela_pensamiento TEXT,

    -- Evolución Temporal
    evolucion_metodologica TEXT,  -- JSON con snapshots temporales
    cambios_criterio TEXT,  -- JSON con cambios importantes
    casos_emblematicos TEXT,  -- JSON con casos clave

    -- Métricas de Calidad
    originalidad_score REAL,
    coherencia_interna REAL,
    coherencia_externa REAL,  -- Con otros jueces de su escuela
    impacto_jurisprudencial REAL,
    claridad_argumentativa REAL,

    -- Sesgos y Valores
    sesgos_detectados TEXT,  -- JSON
    valores_priorizados TEXT,  -- JSON
    axiomas_judiciales TEXT,  -- JSON

    -- Metadata
    ultima_actualizacion TIMESTAMP,
    version_analyser TEXT
);
```

**Tabla: `sentencias_por_juez`**
```sql
CREATE TABLE sentencias_por_juez (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    juez TEXT NOT NULL,
    sentencia_id TEXT UNIQUE NOT NULL,
    fecha DATE,
    corte TEXT,
    sala TEXT,
    materia TEXT,  -- laboral, civil, constitucional, etc.
    tipo_caso TEXT,
    tipo_voto TEXT,  -- mayoria, disidencia, concurrencia, salvamento

    -- Archivo y Procesamiento
    archivo_original TEXT,
    ruta_chunks TEXT,
    fecha_procesamiento TIMESTAMP,

    -- Análisis Individual
    perfil_cognitivo TEXT,  -- JSON del análisis completo de esta sentencia
    razonamientos_identificados TEXT,  -- JSON array
    falacias_detectadas TEXT,  -- JSON array
    fuentes_citadas TEXT,  -- JSON array

    -- Métricas de la Sentencia
    complejidad_argumental REAL,
    innovacion_juridica REAL,
    impacto_estimado REAL,

    -- Contexto Procesal
    ponente TEXT,
    magistrados_concurrentes TEXT,  -- JSON array
    sentencia_previa TEXT,
    sentencia_posterior TEXT,

    FOREIGN KEY (juez) REFERENCES perfiles_judiciales_expandidos(juez)
);
```

**Tabla: `lineas_jurisprudenciales`**
```sql
CREATE TABLE lineas_jurisprudenciales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    juez TEXT NOT NULL,
    tema TEXT NOT NULL,
    subtema TEXT,

    -- Sentencias que conforman la línea
    sentencias_relacionadas TEXT,  -- JSON array de IDs
    fecha_inicio DATE,
    fecha_fin DATE,

    -- Análisis de Consistencia
    consistencia_score REAL,  -- 0 a 1
    evolucion_criterio TEXT,  -- JSON describiendo cambios
    cambios_postura TEXT,  -- JSON con puntos de inflexión

    -- Caracterización de la Línea
    criterio_dominante TEXT,
    razonamiento_tipo TEXT,
    fundamentos_principales TEXT,  -- JSON array

    -- Impacto
    casos_aplicados INTEGER,
    citas_por_otros_jueces INTEGER,

    FOREIGN KEY (juez) REFERENCES perfiles_judiciales_expandidos(juez)
);
```

**Tabla: `comparativas_judiciales`**
```sql
CREATE TABLE comparativas_judiciales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    juez_1 TEXT NOT NULL,
    juez_2 TEXT NOT NULL,

    -- Similitud Cognitiva
    similitud_metodologica REAL,  -- 0 a 1
    similitud_cognitiva REAL,  -- cosine similarity
    distancia_mental REAL,

    -- Análisis Comparativo
    patrones_comunes TEXT,  -- JSON
    diferencias_clave TEXT,  -- JSON
    dimensiones_divergentes TEXT,  -- JSON

    -- Contexto
    casos_coincidentes INTEGER,
    acuerdos INTEGER,
    desacuerdos INTEGER,

    fecha_analisis TIMESTAMP,

    FOREIGN KEY (juez_1) REFERENCES perfiles_judiciales_expandidos(juez),
    FOREIGN KEY (juez_2) REFERENCES perfiles_judiciales_expandidos(juez)
);
```

**Tabla: `redes_influencia_judicial`**
```sql
CREATE TABLE redes_influencia_judicial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    juez_origen TEXT NOT NULL,
    juez_destino TEXT NOT NULL,
    tipo_influencia TEXT,  -- cita, replica, adopta_criterio, rechaza_criterio
    intensidad REAL,  -- 0 a 1

    -- Evidencia
    sentencias_evidencia TEXT,  -- JSON array
    ejemplos_textuales TEXT,  -- JSON array

    -- Temporal
    periodo TEXT,
    frecuencia INTEGER,

    FOREIGN KEY (juez_origen) REFERENCES perfiles_judiciales_expandidos(juez),
    FOREIGN KEY (juez_destino) REFERENCES perfiles_judiciales_expandidos(juez)
);
```

### 2. Nuevos Scripts de Análisis

#### A. `analizador_pensamiento_judicial.py`

**Propósito**: Analizar el pensamiento judicial específico, más allá del análisis cognitivo general.

**Funcionalidades**:
1. **Detección de Activismo Judicial**
   - Invalidación de normas
   - Interpretación expansiva de derechos
   - Creación de precedentes
   - Supervisión de políticas públicas

2. **Clasificación de Interpretación Constitucional**
   - Originalista: apego al texto e intención original
   - Evolutiva: constitución como documento vivo
   - Mixta: combinación pragmática

3. **Análisis de Deferencia**
   - Hacia el legislativo (validación de leyes)
   - Hacia el ejecutivo (validación de políticas)
   - Hacia precedentes (stare decisis)

4. **Protección de Derechos**
   - Niveles de escrutinio aplicados
   - Balanceo de derechos vs interés público
   - Priorización de derechos específicos

5. **Patrones de Votación**
   - Frecuencia de mayorías, disidencias, concurrencias
   - Coaliciones con otros jueces
   - Casos donde cambia de postura

#### B. `analizador_multi_sentencia.py`

**Propósito**: Analizar múltiples sentencias de un juez para identificar patrones consistentes.

**Funcionalidades**:
1. **Análisis de Consistencia**
   - Coherencia entre sentencias sobre el mismo tema
   - Detección de contradicciones
   - Evolución natural vs cambio abrupto

2. **Extracción de Líneas Jurisprudenciales**
   - Agrupación temática de sentencias
   - Identificación de criterio dominante
   - Trazabilidad de evolución

3. **Casos Emblemáticos**
   - Identificación automática de sentencias más influyentes
   - Sentencias que marcan cambios de criterio
   - Casos con mayor impacto

4. **Evolución Temporal**
   - Timeline del pensamiento judicial
   - Detección de puntos de inflexión
   - Influencias contextuales (cambios sociales, políticos)

#### C. `comparador_jueces.py` (refactorización de `comparador_mentes.py`)

**Propósito**: Comparar perfiles judiciales en 50+ dimensiones.

**Nuevas dimensiones específicas**:
- Activismo judicial
- Interpretación constitucional
- Protección de derechos específicos (intimidad, expresión, igualdad, etc.)
- Deferencia institucional
- Uso de fuentes (ley, jurisprudencia, doctrina, derecho comparado)
- Estándares de prueba
- Remedios judiciales preferidos

#### D. `generador_reportes_judiciales.py`

**Propósito**: Generar reportes completos sobre jueces individuales o grupos.

**Tipos de reportes**:
1. **Perfil Judicial Completo**
   - Análisis cognitivo
   - Líneas jurisprudenciales
   - Casos emblemáticos
   - Red de influencias
   - Evolución temporal

2. **Análisis Comparativo**
   - Entre jueces de la misma corte
   - Entre jueces de diferentes cortes
   - Entre escuelas de pensamiento

3. **Análisis de Materia**
   - Cómo aborda un juez un tema específico
   - Comparación con otros jueces en ese tema
   - Evolución de su criterio

4. **Red de Influencias**
   - Visualización de citas y referencias
   - Clusters de jueces con pensamiento similar
   - Influenciadores e influenciados

### 3. Actualización de Scripts Existentes

#### Modificaciones a `analyser_metodo_mejorado.py`

Añadir detección de:
- **Tests judiciales específicos**: test de proporcionalidad, escrutinio estricto/intermedio/laxo, test de razonabilidad
- **Doctrinas judiciales**: doctrina del margen de apreciación, interpretación conforme, cláusulas pétreas
- **Remedios**: declarativos, constitutivos, de condena, medidas cautelares, estado de cosas inconstitucional

#### Modificaciones a `orchestrador_maestro_integrado.py`

Crear flujo específico para análisis judicial:
1. Procesar sentencia → identificar juez
2. Analizar pensamiento individual en esa sentencia
3. Relacionar con otras sentencias del mismo juez
4. Actualizar perfil judicial agregado
5. Recalcular consistencia y líneas jurisprudenciales
6. Actualizar redes de influencia

### 4. Interfaz Web Actualizada

#### Nuevas rutas Flask:

```python
# Rutas principales
@app.route('/jueces')  # Lista de jueces con métricas clave
@app.route('/juez/<nombre>')  # Perfil completo de un juez
@app.route('/juez/<nombre>/sentencias')  # Todas las sentencias
@app.route('/juez/<nombre>/lineas')  # Líneas jurisprudenciales
@app.route('/juez/<nombre>/evolucion')  # Timeline de evolución
@app.route('/juez/<nombre>/red')  # Red de influencias

# Comparaciones
@app.route('/comparar-jueces')  # Interfaz de comparación
@app.route('/escuelas-pensamiento')  # Clusters de jueces

# Análisis temático
@app.route('/materia/<tema>')  # Jueces por materia
@app.route('/materia/<tema>/comparar')  # Comparar abordajes

# Visualizaciones
@app.route('/red-influencias')  # Grafo interactivo
@app.route('/mapa-cognitivo')  # Mapa 2D de espacio cognitivo
```

#### Visualizaciones nuevas:

1. **Timeline de Evolución Judicial**
   - Eje temporal con sentencias clave
   - Marcadores de cambios de criterio
   - Contexto histórico/político

2. **Radar Chart de Perfil Judicial**
   - 20+ dimensiones en radar
   - Comparación con promedio de la corte
   - Comparación con otros jueces

3. **Red de Influencias Interactiva**
   - Nodos: jueces
   - Aristas: citas y referencias
   - Tamaño: impacto
   - Color: escuela de pensamiento

4. **Mapa de Consistencia**
   - Heat map de temas vs consistencia
   - Identificación rápida de áreas sólidas/variables

5. **Análisis de Sentencia Individual**
   - Desglose del razonamiento
   - Visualización de estructura argumentativa
   - Comparación con otras sentencias del juez

### 5. Flujo de Trabajo Propuesto

```
1. INGESTA DE SENTENCIAS
   ├─ Extracción de texto (PDF/DOCX)
   ├─ Identificación de juez(es)
   ├─ Extracción de metadata (fecha, corte, materia, tipo voto)
   └─ Chunking y embeddings

2. ANÁLISIS INDIVIDUAL
   ├─ Análisis cognitivo (ANALYSER v2.0)
   ├─ Análisis judicial específico (nuevo)
   ├─ Extracción de razonamientos, falacias, fuentes
   └─ Guardar perfil individual en sentencias_por_juez

3. AGREGACIÓN POR JUEZ
   ├─ Combinar perfiles de todas las sentencias
   ├─ Calcular métricas agregadas
   ├─ Identificar patrones consistentes
   └─ Actualizar perfiles_judiciales_expandidos

4. ANÁLISIS MULTI-SENTENCIA
   ├─ Detectar líneas jurisprudenciales
   ├─ Calcular consistencia
   ├─ Identificar evolución temporal
   └─ Marcar casos emblemáticos

5. ANÁLISIS RELACIONAL
   ├─ Comparar con otros jueces
   ├─ Mapear redes de influencia
   ├─ Agrupar en escuelas de pensamiento
   └─ Calcular similaridades cognitivas

6. GENERACIÓN DE REPORTES
   ├─ Perfil judicial completo
   ├─ Análisis comparativos
   ├─ Visualizaciones interactivas
   └─ Exportación (PDF, JSON, CSV)
```

### 6. Herramientas de Análisis Avanzado

#### A. Análisis de Argumentación

**Técnica**: Graph-based argument mining
- Mapear premisas, inferencias y conclusiones
- Identificar falacias argumentativas
- Visualizar estructura de razonamiento

#### B. Análisis Semántico Profundo

**Técnicas**:
- Topic modeling (LDA) para identificar temas recurrentes
- Sentiment analysis contextual (no solo positivo/negativo, sino garantista/restrictivo, formalista/sustancialista)
- Entity recognition especializado (doctrinas, tests, principios)

#### C. Análisis Predictivo

**Modelos**:
- Predicción de voto basado en características del caso
- Identificación de factores determinantes en decisiones
- Detección temprana de cambios de criterio

#### D. Análisis de Coaliciones

**En cortes colegiadas**:
- Identificar bloques estables de votación
- Jueces "swing" que determinan mayorías
- Evolución de coaliciones en el tiempo

### 7. Métricas Clave del Sistema

#### Métricas por Juez:
1. **Consistencia interna** (0-1): coherencia entre sus propias sentencias
2. **Consistencia externa** (0-1): coherencia con su escuela de pensamiento
3. **Impacto jurisprudencial** (0-1): cuánto es citado por otros
4. **Originalidad** (0-1): innovación en razonamientos
5. **Claridad argumentativa** (0-1): claridad y estructura
6. **Activismo judicial** (-1 a +1): restricción a activismo
7. **Especialización** (0-1): concentración en materias específicas

#### Métricas por Sentencia:
1. **Complejidad argumental** (0-1)
2. **Innovación jurídica** (0-1)
3. **Impacto estimado** (0-1)
4. **Coherencia con perfil del juez** (0-1)

#### Métricas de Red:
1. **Centralidad** del juez en red de influencias
2. **Clustering coefficient**: qué tan agrupado está con jueces similares
3. **Betweenness**: si es puente entre escuelas de pensamiento

## Implementación por Fases

### Fase 1: Fundamentos (Semana 1-2)
- [ ] Crear nuevo esquema de base de datos
- [ ] Script de migración de datos existentes
- [ ] Refactorizar nombres: autor → juez
- [ ] Actualizar orchestrador para flujo judicial

### Fase 2: Análisis Avanzado (Semana 3-4)
- [ ] Implementar `analizador_pensamiento_judicial.py`
- [ ] Implementar `analizador_multi_sentencia.py`
- [ ] Refactorizar `comparador_mentes.py` → `comparador_jueces.py`
- [ ] Añadir nuevas dimensiones de análisis judicial

### Fase 3: Relaciones y Agregación (Semana 5-6)
- [ ] Sistema de líneas jurisprudenciales
- [ ] Análisis de consistencia multi-sentencia
- [ ] Red de influencias judiciales
- [ ] Detección de escuelas de pensamiento

### Fase 4: Interfaz y Visualización (Semana 7-8)
- [ ] Actualizar rutas Flask
- [ ] Nuevas plantillas HTML
- [ ] Visualizaciones interactivas (D3.js)
- [ ] Sistema de reportes

### Fase 5: Optimización y Extras (Semana 9-10)
- [ ] Análisis predictivo
- [ ] Mejoras de performance
- [ ] Documentación completa
- [ ] Tests unitarios

## Ventajas del Nuevo Sistema

1. **Análisis Profundo de Pensamiento Judicial**: No solo qué dicen, sino cómo piensan
2. **Trazabilidad**: Seguir la evolución de un juez a través del tiempo
3. **Comparabilidad**: Comparar jueces en 50+ dimensiones
4. **Predictibilidad**: Anticipar criterios basados en patrones
5. **Investigación Académica**: Herramienta para estudios empíricos del derecho
6. **Formación Judicial**: Identificar mejores prácticas argumentativas
7. **Transparencia**: Hacer visible el razonamiento judicial

## Casos de Uso

1. **Investigador**: Estudiar la evolución del test de proporcionalidad en la jurisprudencia constitucional
2. **Abogado**: Identificar el perfil del juez que conocerá su caso
3. **Juez**: Comparar su razonamiento con el de pares o predecesores
4. **Académico**: Mapear escuelas de pensamiento en la judicatura
5. **Periodista**: Analizar tendencias en decisiones judiciales
6. **Estudiante**: Aprender de los mejores razonamientos judiciales

## Tecnologías y Herramientas

- **Backend**: Python 3.9+, Flask
- **Base de Datos**: SQLite (fácil migración a PostgreSQL)
- **ML/NLP**:
  - Sentence Transformers (embeddings)
  - spaCy + BERT español (NER)
  - Scikit-learn (clustering, clasificación)
  - NetworkX (análisis de redes)
- **Visualización**:
  - D3.js (redes, timelines)
  - Plotly (gráficos interactivos)
  - Chart.js (radares, barras)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla o Alpine.js)

## Conclusión

Esta refactorización transforma un excelente sistema de análisis cognitivo de autores en una **herramienta de investigación judicial de clase mundial**, aprovechando todas las capacidades existentes y añadiendo las especificidades del análisis judicial.

El sistema resultante permitirá:
- Comprender el pensamiento de jueces individuales
- Identificar líneas jurisprudenciales y su evolución
- Comparar razonamientos entre jueces
- Predecir tendencias judiciales
- Investigar empíricamente el razonamiento judicial

**¿Procedo con la implementación?**
