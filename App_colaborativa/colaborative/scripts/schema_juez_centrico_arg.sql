-- ===============================================
-- ESQUEMA DE BASE DE DATOS: Sistema de Análisis de Pensamiento Judicial (Argentina)
-- Versión: 1.0
-- Fecha: 2025-11-12
-- ===============================================

-- ===============================================
-- TABLA 1: PERFILES JUDICIALES ARGENTINOS
-- ===============================================
CREATE TABLE IF NOT EXISTS perfiles_judiciales_argentinos (
    -- ===== IDENTIFICACIÓN =====
    juez TEXT PRIMARY KEY,
    tipo_entidad TEXT NOT NULL CHECK(tipo_entidad IN ('individual', 'sala')),
    miembros_sala TEXT,  -- JSON array si es sala

    -- Contexto Argentino Específico
    fuero TEXT,  -- civil, comercial, laboral, penal, cont-admin, familia, etc.
    especialidad TEXT,  -- civil_patrimonial, derecho_consumidor, etc.
    instancia TEXT,  -- primera_instancia, camara_apelaciones, corte_suprema, etc.
    jurisdiccion TEXT,  -- federal, provincial
    provincia TEXT,  -- si es provincial
    tribunal TEXT,  -- nombre completo del tribunal
    secretaria INTEGER,  -- número de secretaría si aplica

    periodo_activo TEXT,  -- desde-hasta
    total_sentencias_analizadas INTEGER DEFAULT 0,

    -- ===== ANÁLISIS COGNITIVO (del sistema actual) =====
    metodologia_principal TEXT,
    patron_razonamiento_dominante TEXT,
    estilo_argumentativo TEXT,
    estructura_discursiva TEXT,
    marcadores_linguisticos TEXT,  -- JSON
    vocabulario_especializado TEXT,  -- JSON con términos frecuentes
    densidad_conceptual REAL,
    complejidad_sintactica REAL,

    -- Retórica Aristotélica
    uso_ethos REAL CHECK(uso_ethos >= 0 AND uso_ethos <= 1),
    uso_pathos REAL CHECK(uso_pathos >= 0 AND uso_pathos <= 1),
    uso_logos REAL CHECK(uso_logos >= 0 AND uso_logos <= 1),

    -- Modalidad Epistémica
    modalidad_epistemica TEXT,
    certeza_promedio REAL,

    -- ===== ANÁLISIS JUDICIAL ESPECÍFICO =====

    -- Orientación Judicial
    tendencia_activismo REAL CHECK(tendencia_activismo >= -1 AND tendencia_activismo <= 1),
    interpretacion_normativa TEXT,  -- literal, sistematica, teleologica, mixta
    interpretacion_constitucional TEXT,  -- originalista, evolutiva, mixta
    formalismo_vs_sustancialismo REAL CHECK(formalismo_vs_sustancialismo >= -1 AND formalismo_vs_sustancialismo <= 1),

    -- Deferencia Institucional
    deferencia_legislativo REAL CHECK(deferencia_legislativo >= 0 AND deferencia_legislativo <= 1),
    deferencia_ejecutivo REAL CHECK(deferencia_ejecutivo >= 0 AND deferencia_ejecutivo <= 1),
    respeto_precedentes REAL CHECK(respeto_precedentes >= 0 AND respeto_precedentes <= 1),
    innovacion_juridica REAL CHECK(innovacion_juridica >= 0 AND innovacion_juridica <= 1),

    -- Protección de Derechos
    proteccion_derechos_fundamentales REAL CHECK(proteccion_derechos_fundamentales >= 0 AND proteccion_derechos_fundamentales <= 1),
    proteccion_derechos_sociales REAL CHECK(proteccion_derechos_sociales >= 0 AND proteccion_derechos_sociales <= 1),
    proteccion_derechos_consumidor REAL CHECK(proteccion_derechos_consumidor >= 0 AND proteccion_derechos_consumidor <= 1),
    proteccion_trabajador REAL CHECK(proteccion_trabajador >= 0 AND proteccion_trabajador <= 1),
    proteccion_niñez REAL CHECK(proteccion_niñez >= 0 AND proteccion_niñez <= 1),
    proteccion_medio_ambiente REAL CHECK(proteccion_medio_ambiente >= 0 AND proteccion_medio_ambiente <= 1),
    proteccion_acceso_justicia REAL CHECK(proteccion_acceso_justicia >= 0 AND proteccion_acceso_justicia <= 1),

    -- Estándares Probatorios y Argumentativos
    estandar_prueba_preferido TEXT,  -- sana_critica, prueba_tasada, libre_conviccion
    rigurosidad_probatoria REAL,
    uso_presunciones REAL,
    uso_indicios REAL,
    valoracion_pericial REAL,

    -- Tests y Doctrinas Aplicados
    uso_test_proporcionalidad REAL,
    uso_test_razonabilidad REAL,
    uso_control_constitucionalidad REAL,
    uso_interpretacion_conforme REAL,
    uso_in_dubio_pro REAL,

    -- Fuentes del Derecho (preferencias)
    peso_ley REAL CHECK(peso_ley >= 0 AND peso_ley <= 1),
    peso_jurisprudencia REAL CHECK(peso_jurisprudencia >= 0 AND peso_jurisprudencia <= 1),
    peso_doctrina REAL CHECK(peso_doctrina >= 0 AND peso_doctrina <= 1),
    peso_derecho_comparado REAL CHECK(peso_derecho_comparado >= 0 AND peso_derecho_comparado <= 1),
    peso_tratados_internacionales REAL CHECK(peso_tratados_internacionales >= 0 AND peso_tratados_internacionales <= 1),
    peso_constitucion REAL CHECK(peso_constitucion >= 0 AND peso_constitucion <= 1),

    -- Citas Jurisprudenciales
    frecuencia_cita_csjn REAL,
    frecuencia_cita_camaras REAL,
    frecuencia_autocita REAL,
    precedentes_mas_citados TEXT,  -- JSON array con fallos emblemáticos

    -- ===== LÍNEAS JURISPRUDENCIALES =====
    temas_recurrentes TEXT,  -- JSON array
    lineas_consolidadas TEXT,  -- JSON: {tema: {criterio, sentencias, consistencia}}
    lineas_inconsistentes TEXT,  -- JSON: temas donde varía
    casos_emblematicos TEXT,  -- JSON: casos que definen su postura

    -- ===== REDES DE INFLUENCIA =====
    jueces_que_cita TEXT,  -- JSON array con frecuencias
    jueces_que_lo_citan TEXT,  -- JSON array
    influencias_doctrinarias TEXT,  -- JSON: autores que cita frecuentemente
    corriente_juridica TEXT,  -- positivista, iusnaturalista, realista, etc.
    escuela_pensamiento TEXT,

    -- ===== SESGOS Y VALORES =====
    sesgos_detectados TEXT,  -- JSON
    valores_priorizados TEXT,  -- JSON ordenado
    axiomas_judiciales TEXT,  -- JSON: creencias fundamentales del juez

    -- Sesgos Específicos Argentinos
    sesgo_pro_trabajador REAL,
    sesgo_pro_consumidor REAL,
    sesgo_pro_estado REAL,
    sesgo_garantista REAL,
    sesgo_punitivista REAL,

    -- ===== CARACTERÍSTICAS DE SENTENCIAS =====
    extension_promedio_sentencias REAL,
    uso_considerandos_extensos INTEGER CHECK(uso_considerandos_extensos IN (0, 1)),
    uso_votos_fundados INTEGER CHECK(uso_votos_fundados IN (0, 1)),
    claridad_redaccion REAL CHECK(claridad_redaccion >= 0 AND claridad_redaccion <= 1),
    uso_lenguaje_ciudadano REAL CHECK(uso_lenguaje_ciudadano >= 0 AND uso_lenguaje_ciudadano <= 1),

    -- ===== MÉTRICAS DE CALIDAD =====
    coherencia_interna REAL CHECK(coherencia_interna >= 0 AND coherencia_interna <= 1),
    coherencia_externa REAL CHECK(coherencia_externa >= 0 AND coherencia_externa <= 1),
    solidez_argumentativa REAL CHECK(solidez_argumentativa >= 0 AND solidez_argumentativa <= 1),
    fundamentacion_normativa REAL CHECK(fundamentacion_normativa >= 0 AND fundamentacion_normativa <= 1),
    fundamentacion_factica REAL CHECK(fundamentacion_factica >= 0 AND fundamentacion_factica <= 1),
    originalidad_score REAL CHECK(originalidad_score >= 0 AND originalidad_score <= 1),
    impacto_jurisprudencial REAL CHECK(impacto_jurisprudencial >= 0 AND impacto_jurisprudencial <= 1),

    -- ===== METADATA =====
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version_analyser TEXT,
    confianza_perfil REAL CHECK(confianza_perfil >= 0 AND confianza_perfil <= 1)
);

-- ===============================================
-- TABLA 2: SENTENCIAS POR JUEZ
-- ===============================================
CREATE TABLE IF NOT EXISTS sentencias_por_juez_arg (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- ===== IDENTIFICACIÓN =====
    sentencia_id TEXT UNIQUE NOT NULL,
    juez TEXT NOT NULL,
    archivo_original TEXT,

    -- ===== METADATA PROCESAL ARGENTINA =====
    fecha_sentencia DATE,
    expediente TEXT,
    caratula TEXT,

    -- Tribunal
    fuero TEXT,
    instancia TEXT,
    jurisdiccion TEXT,
    tribunal TEXT,
    secretaria INTEGER,

    -- Tipo de Sentencia
    tipo_sentencia TEXT,  -- definitiva, interlocutoria, homologatoria
    tipo_proceso TEXT,  -- ordinario, sumario, sumarisimo, ejecutivo, amparo, etc.
    materia TEXT,  -- despido, daños, divorcio, etc.
    submateria TEXT,

    -- Partes
    actor TEXT,
    demandado TEXT,
    terceros TEXT,  -- JSON si hay

    -- Decisión
    resultado TEXT,  -- hace_lugar, rechaza, hace_lugar_parcial
    condena_costas TEXT,  -- al_actor, al_demandado, por_su_orden
    monto_condena REAL,

    -- Si es Sala/Tribunal Colegiado
    juez_ponente TEXT,
    jueces_firmantes TEXT,  -- JSON array
    votos_disidentes TEXT,  -- JSON si hay
    votos_concurrentes TEXT,  -- JSON si hay

    -- ===== PROCESAMIENTO =====
    texto_completo TEXT,
    ruta_chunks TEXT,
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- ===== ANÁLISIS INDIVIDUAL DE ESTA SENTENCIA =====
    perfil_cognitivo TEXT,  -- JSON del análisis completo
    razonamientos_identificados TEXT,  -- JSON array: tipos de razonamiento usados
    falacias_detectadas TEXT,  -- JSON array

    -- Fuentes Citadas
    normas_citadas TEXT,  -- JSON: leyes, decretos, CCyC, códigos
    jurisprudencia_citada TEXT,  -- JSON: fallos citados
    doctrina_citada TEXT,  -- JSON: autores citados
    tratados_citados TEXT,  -- JSON: tratados internacionales

    -- Tests y Doctrinas Aplicados
    tests_aplicados TEXT,  -- JSON: proporcionalidad, razonabilidad, etc.
    principios_invocados TEXT,  -- JSON: in dubio pro operario, etc.

    -- ===== MÉTRICAS DE ESTA SENTENCIA =====
    complejidad_argumental REAL,
    extension_palabras INTEGER,
    claridad_redaccion REAL,
    solidez_argumentativa REAL,
    innovacion_juridica REAL,
    impacto_estimado REAL,

    -- ===== ANÁLISIS PREDICTIVO =====
    factores_decision TEXT,  -- JSON: qué factores fueron determinantes
    prediccion_confianza REAL,

    -- ===== CONTEXTO =====
    sentencia_previa TEXT,  -- ID de sentencia de instancia anterior
    sentencia_posterior TEXT,  -- ID si fue apelada
    recursos_interpuestos TEXT,  -- JSON
    estado_procesal TEXT,  -- firme, apelada, casacion, etc.

    -- ===== CLASIFICACIÓN TEMÁTICA =====
    tags_tematicos TEXT,  -- JSON: despido, discriminacion, daños, etc.
    linea_jurisprudencial_id INTEGER,

    FOREIGN KEY (juez) REFERENCES perfiles_judiciales_argentinos(juez),
    FOREIGN KEY (linea_jurisprudencial_id) REFERENCES lineas_jurisprudenciales(id)
);

-- ===============================================
-- TABLA 3: LÍNEAS JURISPRUDENCIALES
-- ===============================================
CREATE TABLE IF NOT EXISTS lineas_jurisprudenciales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    juez TEXT NOT NULL,

    -- ===== IDENTIFICACIÓN DE LA LÍNEA =====
    tema TEXT NOT NULL,
    subtema TEXT,
    materia TEXT,

    -- ===== SENTENCIAS QUE CONFORMAN LA LÍNEA =====
    sentencias_ids TEXT,  -- JSON array de IDs
    cantidad_sentencias INTEGER DEFAULT 0,
    fecha_primera_sentencia DATE,
    fecha_ultima_sentencia DATE,

    -- ===== CARACTERIZACIÓN DEL CRITERIO =====
    criterio_dominante TEXT,
    fundamento_principal TEXT,
    razonamiento_tipo TEXT,

    -- Tests/Principios Aplicados
    tests_recurrentes TEXT,  -- JSON
    principios_aplicados TEXT,  -- JSON
    normas_aplicadas TEXT,  -- JSON: artículos que siempre aplica

    -- ===== CONSISTENCIA =====
    consistencia_score REAL CHECK(consistencia_score >= 0 AND consistencia_score <= 1),
    sentencias_consistentes INTEGER DEFAULT 0,
    sentencias_inconsistentes INTEGER DEFAULT 0,
    excepciones_identificadas TEXT,  -- JSON: cuándo se aparta del criterio

    -- ===== PREDICTIBILIDAD =====
    factores_predictivos TEXT,  -- JSON: qué factores predicen que aplique esta línea
    casos_tipo TEXT,  -- JSON: casos paradigmáticos de esta línea

    -- ===== IMPACTO =====
    veces_citada INTEGER DEFAULT 0,
    jueces_que_siguen TEXT,  -- JSON: otros jueces que adoptan este criterio

    -- ===== METADATA =====
    fecha_analisis TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confianza_linea REAL CHECK(confianza_linea >= 0 AND confianza_linea <= 1),

    FOREIGN KEY (juez) REFERENCES perfiles_judiciales_argentinos(juez)
);

-- ===============================================
-- TABLA 4: REDES DE INFLUENCIA JUDICIAL
-- ===============================================
CREATE TABLE IF NOT EXISTS redes_influencia_judicial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- ===== RELACIÓN =====
    juez_origen TEXT NOT NULL,
    juez_destino TEXT,
    tipo_destino TEXT CHECK(tipo_destino IN ('juez', 'sala', 'tribunal_superior', 'csjn', 'autor_doctrinal')),

    tipo_influencia TEXT CHECK(tipo_influencia IN ('cita_literal', 'adopta_criterio', 'replica', 'distingue', 'rechaza')),
    intensidad REAL CHECK(intensidad >= 0 AND intensidad <= 1),

    -- ===== EVIDENCIA =====
    sentencias_evidencia TEXT,  -- JSON array de IDs donde cita
    cantidad_citas INTEGER DEFAULT 0,
    ejemplos_textuales TEXT,  -- JSON: extractos de las citas

    -- ===== CONTEXTO =====
    temas_comunes TEXT,  -- JSON: en qué temas se da la influencia
    coincidencia_criterio REAL CHECK(coincidencia_criterio >= 0 AND coincidencia_criterio <= 1),

    -- ===== METADATA =====
    fecha_primera_cita DATE,
    fecha_ultima_cita DATE,
    periodo TEXT,

    FOREIGN KEY (juez_origen) REFERENCES perfiles_judiciales_argentinos(juez)
);

-- ===============================================
-- TABLA 5: FACTORES PREDICTIVOS
-- ===============================================
CREATE TABLE IF NOT EXISTS factores_predictivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    juez TEXT NOT NULL,
    materia TEXT,
    tema TEXT,

    -- ===== FACTORES =====
    factor TEXT NOT NULL,
    peso REAL CHECK(peso >= -1 AND peso <= 1),
    confianza REAL CHECK(confianza >= 0 AND confianza <= 1),

    -- ===== EVIDENCIA =====
    sentencias_sustento TEXT,  -- JSON array
    ejemplos INTEGER DEFAULT 0,

    -- ===== METADATA =====
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (juez) REFERENCES perfiles_judiciales_argentinos(juez)
);

-- ===============================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ===============================================

-- Índices para perfiles_judiciales_argentinos
CREATE INDEX IF NOT EXISTS idx_juez_fuero ON perfiles_judiciales_argentinos(fuero);
CREATE INDEX IF NOT EXISTS idx_juez_jurisdiccion ON perfiles_judiciales_argentinos(jurisdiccion);
CREATE INDEX IF NOT EXISTS idx_juez_tribunal ON perfiles_judiciales_argentinos(tribunal);

-- Índices para sentencias_por_juez_arg
CREATE INDEX IF NOT EXISTS idx_sentencia_juez ON sentencias_por_juez_arg(juez);
CREATE INDEX IF NOT EXISTS idx_sentencia_fecha ON sentencias_por_juez_arg(fecha_sentencia);
CREATE INDEX IF NOT EXISTS idx_sentencia_materia ON sentencias_por_juez_arg(materia);
CREATE INDEX IF NOT EXISTS idx_sentencia_expediente ON sentencias_por_juez_arg(expediente);
CREATE INDEX IF NOT EXISTS idx_sentencia_fuero ON sentencias_por_juez_arg(fuero);

-- Índices para lineas_jurisprudenciales
CREATE INDEX IF NOT EXISTS idx_linea_juez ON lineas_jurisprudenciales(juez);
CREATE INDEX IF NOT EXISTS idx_linea_tema ON lineas_jurisprudenciales(tema);
CREATE INDEX IF NOT EXISTS idx_linea_materia ON lineas_jurisprudenciales(materia);

-- Índices para redes_influencia_judicial
CREATE INDEX IF NOT EXISTS idx_red_origen ON redes_influencia_judicial(juez_origen);
CREATE INDEX IF NOT EXISTS idx_red_destino ON redes_influencia_judicial(juez_destino);
CREATE INDEX IF NOT EXISTS idx_red_tipo ON redes_influencia_judicial(tipo_influencia);

-- Índices para factores_predictivos
CREATE INDEX IF NOT EXISTS idx_factor_juez ON factores_predictivos(juez);
CREATE INDEX IF NOT EXISTS idx_factor_materia ON factores_predictivos(materia);
CREATE INDEX IF NOT EXISTS idx_factor_tema ON factores_predictivos(tema);

-- ===============================================
-- VISTAS ÚTILES
-- ===============================================

-- Vista de jueces con estadísticas básicas
CREATE VIEW IF NOT EXISTS vista_jueces_stats AS
SELECT
    j.juez,
    j.tipo_entidad,
    j.fuero,
    j.tribunal,
    j.total_sentencias_analizadas,
    j.tendencia_activismo,
    j.coherencia_interna,
    j.impacto_jurisprudencial,
    COUNT(DISTINCT l.id) as cantidad_lineas_consolidadas
FROM perfiles_judiciales_argentinos j
LEFT JOIN lineas_jurisprudenciales l ON j.juez = l.juez
GROUP BY j.juez;

-- Vista de sentencias con info del juez
CREATE VIEW IF NOT EXISTS vista_sentencias_completas AS
SELECT
    s.*,
    j.fuero as juez_fuero,
    j.tribunal as juez_tribunal,
    j.tendencia_activismo,
    j.coherencia_interna
FROM sentencias_por_juez_arg s
JOIN perfiles_judiciales_argentinos j ON s.juez = j.juez;

-- Vista de red de influencias agregada
CREATE VIEW IF NOT EXISTS vista_red_agregada AS
SELECT
    juez_origen,
    tipo_destino,
    tipo_influencia,
    COUNT(*) as cantidad_relaciones,
    AVG(intensidad) as intensidad_promedio,
    SUM(cantidad_citas) as total_citas
FROM redes_influencia_judicial
GROUP BY juez_origen, tipo_destino, tipo_influencia;
