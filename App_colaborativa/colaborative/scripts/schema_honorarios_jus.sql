-- ===============================================
-- ESQUEMA DE BASE DE DATOS: Sistema de Honorarios Judiciales (Cordoba, Argentina)
-- Version: 1.0
-- Fecha: 10-DIC-2025
-- ===============================================
--
-- REGLAS FUNDAMENTALES:
-- =====================
-- 1. Los honorarios SIEMPRE se determinan en JUS (unidad arancelaria)
-- 2. Si el monto esta en pesos, debe convertirse a JUS
-- 3. El limite del 30% maximo SOLO aplica a:
--    - Sentencias de REGULACION DE HONORARIOS DE LETRADOS/ABOGADOS
--    - NO aplica a causas donde se cita peritos por otras razones
--
-- FUENTE OFICIAL VALORES JUS:
-- https://www.justiciacordoba.gob.ar/justiciacordoba/Servicios/JUSyUnidadEconomica/1
-- ===============================================

-- ===============================================
-- TABLA: VALORES JUS HISTORICOS
-- ===============================================
-- Almacena los valores JUS actualizados por el TSJ de Cordoba
CREATE TABLE IF NOT EXISTS valores_jus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_vigencia DATE NOT NULL UNIQUE,  -- Fecha desde cuando rige el valor
    valor_pesos REAL NOT NULL,            -- Valor del JUS en pesos argentinos
    acuerdo_tsj TEXT,                     -- Numero de acuerdo del TSJ
    observaciones TEXT,
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- URL de referencia para verificacion manual
    url_fuente TEXT DEFAULT 'https://www.justiciacordoba.gob.ar/justiciacordoba/Servicios/JUSyUnidadEconomica/1'
);

CREATE INDEX IF NOT EXISTS idx_jus_fecha ON valores_jus(fecha_vigencia DESC);

-- ===============================================
-- TABLA: TIPOS DE CAUSA PARA HONORARIOS
-- ===============================================
-- Define los tipos de causa en relacion a honorarios
-- IMPORTANTE: El 30% max solo aplica a REGULACION_HONORARIOS_LETRADOS
CREATE TABLE IF NOT EXISTS tipos_causa_honorarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    aplica_limite_30_maximo INTEGER NOT NULL DEFAULT 0,  -- 1 = aplica, 0 = no aplica
    notas TEXT
);

-- Insertar tipos de causa predefinidos
INSERT OR IGNORE INTO tipos_causa_honorarios (codigo, descripcion, aplica_limite_30_maximo, notas) VALUES
('REGULACION_HONORARIOS_LETRADOS',
 'Causas cuyo objeto es la regulacion de honorarios de letrados/abogados actores',
 1,  -- SI aplica el 30% max
 'El 30% maximo SOLO aplica a este tipo de causas donde el objeto es regular honorarios de letrados'),

('HONORARIOS_PERITOS_EN_CAUSA',
 'Causas donde se designan peritos para labores periciales (el objeto de la causa es otro)',
 0,  -- NO aplica el 30% max
 'El 30% NO aplica cuando se cita peritos por labores periciales en causas de danos, despido, etc.'),

('OTRAS_CAUSAS',
 'Otras causas donde se regulan honorarios incidentalmente',
 0,  -- NO aplica el 30% max
 'El 30% maximo solo aplica a regulacion de honorarios de letrados');

-- ===============================================
-- TABLA: HONORARIOS REGULADOS EN SENTENCIAS
-- ===============================================
-- Almacena los honorarios regulados en cada sentencia
CREATE TABLE IF NOT EXISTS honorarios_regulados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Vinculacion con sentencia
    sentencia_id TEXT NOT NULL,

    -- Tipo de causa (determina si aplica el 30%)
    tipo_causa_codigo TEXT NOT NULL,

    -- Beneficiario del honorario
    beneficiario TEXT,                    -- Nombre del profesional
    tipo_profesional TEXT NOT NULL,       -- letrado, perito, mediador, martillero, etc.
    matricula TEXT,                       -- Numero de matricula si esta disponible

    -- Montos (SIEMPRE en JUS como unidad principal)
    monto_jus REAL NOT NULL,              -- Monto regulado en JUS
    monto_pesos_equivalente REAL,         -- Equivalente en pesos a la fecha
    valor_jus_aplicado REAL,              -- Valor del JUS usado para conversion
    fecha_valor_jus DATE,                 -- Fecha del valor JUS aplicado

    -- Base regulatoria
    base_regulatoria_jus REAL,            -- Base sobre la que se calcula
    porcentaje_sobre_base REAL,           -- Porcentaje que representa

    -- Control del limite 30%
    aplica_limite_30 INTEGER DEFAULT 0,   -- 1 si aplica a este honorario
    excede_limite_30 INTEGER DEFAULT 0,   -- 1 si excede el limite

    -- Labor realizada
    concepto TEXT,                        -- Descripcion de la labor
    etapa_procesal TEXT,                  -- Primera instancia, apelacion, etc.

    -- Metadata
    fecha_regulacion DATE,
    observaciones TEXT,
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sentencia_id) REFERENCES sentencias_por_juez_arg(sentencia_id),
    FOREIGN KEY (tipo_causa_codigo) REFERENCES tipos_causa_honorarios(codigo)
);

CREATE INDEX IF NOT EXISTS idx_honorarios_sentencia ON honorarios_regulados(sentencia_id);
CREATE INDEX IF NOT EXISTS idx_honorarios_tipo_causa ON honorarios_regulados(tipo_causa_codigo);
CREATE INDEX IF NOT EXISTS idx_honorarios_tipo_profesional ON honorarios_regulados(tipo_profesional);
CREATE INDEX IF NOT EXISTS idx_honorarios_beneficiario ON honorarios_regulados(beneficiario);

-- ===============================================
-- TABLA: ANALISIS DE HONORARIOS POR SENTENCIA
-- ===============================================
-- Resumen del analisis de honorarios de cada sentencia
CREATE TABLE IF NOT EXISTS analisis_honorarios_sentencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sentencia_id TEXT UNIQUE NOT NULL,

    -- Clasificacion de la causa
    tipo_causa_codigo TEXT NOT NULL,
    es_regulacion_honorarios_letrados INTEGER DEFAULT 0,
    aplica_limite_30_maximo INTEGER DEFAULT 0,

    -- Base regulatoria total
    base_regulatoria_jus REAL,
    base_regulatoria_pesos REAL,

    -- Totales
    total_honorarios_jus REAL DEFAULT 0,
    total_honorarios_pesos REAL DEFAULT 0,
    cantidad_honorarios_regulados INTEGER DEFAULT 0,

    -- Verificacion del limite
    porcentaje_total_sobre_base REAL,
    excede_limite_30 INTEGER DEFAULT 0,

    -- Valor JUS usado
    valor_jus_aplicado REAL,
    fecha_valor_jus DATE,

    -- Notas del analisis
    observaciones TEXT,  -- JSON con lista de observaciones
    fecha_analisis TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sentencia_id) REFERENCES sentencias_por_juez_arg(sentencia_id),
    FOREIGN KEY (tipo_causa_codigo) REFERENCES tipos_causa_honorarios(codigo)
);

CREATE INDEX IF NOT EXISTS idx_analisis_sentencia ON analisis_honorarios_sentencia(sentencia_id);
CREATE INDEX IF NOT EXISTS idx_analisis_tipo_causa ON analisis_honorarios_sentencia(tipo_causa_codigo);

-- ===============================================
-- VISTA: HONORARIOS CON DETALLE COMPLETO
-- ===============================================
CREATE VIEW IF NOT EXISTS vista_honorarios_completa AS
SELECT
    h.*,
    tc.descripcion AS tipo_causa_descripcion,
    tc.aplica_limite_30_maximo AS tipo_causa_aplica_30,
    tc.notas AS tipo_causa_notas,
    a.base_regulatoria_jus AS base_total_jus,
    a.porcentaje_total_sobre_base
FROM honorarios_regulados h
LEFT JOIN tipos_causa_honorarios tc ON h.tipo_causa_codigo = tc.codigo
LEFT JOIN analisis_honorarios_sentencia a ON h.sentencia_id = a.sentencia_id;

-- ===============================================
-- VISTA: RESUMEN DE HONORARIOS POR TIPO DE CAUSA
-- ===============================================
CREATE VIEW IF NOT EXISTS vista_resumen_honorarios_por_tipo AS
SELECT
    tc.codigo,
    tc.descripcion,
    tc.aplica_limite_30_maximo,
    COUNT(DISTINCT h.sentencia_id) AS cantidad_sentencias,
    COUNT(h.id) AS cantidad_honorarios,
    SUM(h.monto_jus) AS total_jus_regulado,
    AVG(h.monto_jus) AS promedio_jus,
    SUM(CASE WHEN h.excede_limite_30 = 1 THEN 1 ELSE 0 END) AS casos_exceden_30
FROM tipos_causa_honorarios tc
LEFT JOIN honorarios_regulados h ON tc.codigo = h.tipo_causa_codigo
GROUP BY tc.codigo;

-- ===============================================
-- VISTA: ALERTAS DE HONORARIOS QUE EXCEDEN 30%
-- ===============================================
-- Solo para causas de regulacion de honorarios de letrados
CREATE VIEW IF NOT EXISTS vista_alertas_excede_30 AS
SELECT
    a.sentencia_id,
    a.porcentaje_total_sobre_base,
    a.total_honorarios_jus,
    a.base_regulatoria_jus,
    a.observaciones,
    a.fecha_analisis
FROM analisis_honorarios_sentencia a
WHERE a.tipo_causa_codigo = 'REGULACION_HONORARIOS_LETRADOS'
  AND a.excede_limite_30 = 1
ORDER BY a.porcentaje_total_sobre_base DESC;

-- ===============================================
-- COMENTARIOS SOBRE EL USO
-- ===============================================
/*
REGLAS DE APLICACION DEL LIMITE DEL 30%:
========================================

1. CUANDO APLICA:
   - Sentencias que resuelven sobre REGULACION DE HONORARIOS DE LETRADOS ACTORES
   - Sentencias donde el OBJETO de la causa es la regulacion de honorarios de abogados

2. CUANDO NO APLICA:
   - Causas donde se cita a peritos para realizar labor pericial
   - El objeto de la causa es otro (danos, despido, divorcio, etc.)
   - Los honorarios periciales son ACCESORIOS al objeto principal

3. CONVERSION A JUS:
   - SIEMPRE determinar honorarios en JUS
   - Si el monto esta en pesos, convertir usando valor JUS vigente
   - Consultar valores actualizados en:
     https://www.justiciacordoba.gob.ar/justiciacordoba/Servicios/JUSyUnidadEconomica/1

EJEMPLO DE USO:
==============

-- Insertar un honorario de letrado en causa de regulacion (aplica 30%):
INSERT INTO honorarios_regulados
    (sentencia_id, tipo_causa_codigo, beneficiario, tipo_profesional,
     monto_jus, aplica_limite_30)
VALUES
    ('SENT-001', 'REGULACION_HONORARIOS_LETRADOS', 'Dr. Perez', 'letrado',
     250.00, 1);

-- Insertar un honorario de perito en causa de danos (NO aplica 30%):
INSERT INTO honorarios_regulados
    (sentencia_id, tipo_causa_codigo, beneficiario, tipo_profesional,
     monto_jus, aplica_limite_30)
VALUES
    ('SENT-002', 'HONORARIOS_PERITOS_EN_CAUSA', 'Lic. Garcia', 'perito',
     500.00, 0);
*/
