# Propuesta Ajustada: Sistema de Análisis de Pensamiento Judicial (Argentina)

## Resumen de Ajustes

Basado en tus prioridades, esta propuesta ajustada se enfoca en:

✅ **PRIORIDADES CONFIRMADAS:**
- Análisis individual profundo de cada juez (punto de partida)
- Redes de influencia judicial (MUY IMPORTANTE)
- Líneas jurisprudenciales por juez (MUY IMPORTANTE)
- Análisis predictivo
- Informes escritos (no visualizaciones web)
- Sistema de preguntas predeterminadas extenso
- Contexto: Argentina, jueces individuales y salas

❌ **ELIMINADO:**
- Comparaciones directas entre jueces
- Análisis de evolución temporal

## 1. Esquema de Base de Datos Ajustado

### Base de Datos Principal: `juez_centrico_arg.db`

#### Tabla: `perfiles_judiciales_argentinos`

```sql
CREATE TABLE perfiles_judiciales_argentinos (
    -- ===== IDENTIFICACIÓN =====
    juez TEXT PRIMARY KEY,
    tipo_entidad TEXT NOT NULL,  -- 'individual' o 'sala'
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
    uso_ethos REAL,  -- 0 a 1
    uso_pathos REAL,
    uso_logos REAL,

    -- Modalidad Epistémica
    modalidad_epistemica TEXT,
    certeza_promedio REAL,

    -- ===== ANÁLISIS JUDICIAL ESPECÍFICO =====

    -- Orientación Judicial
    tendencia_activismo REAL,  -- -1 (restricción) a +1 (activismo)
    interpretacion_normativa TEXT,  -- literal, sistematica, teleologica, mixta
    interpretacion_constitucional TEXT,  -- originalista, evolutiva, mixta
    formalismo_vs_sustancialismo REAL,  -- -1 (formalista) a +1 (sustancialista)

    -- Deferencia Institucional
    deferencia_legislativo REAL,  -- 0 a 1 (cuánto valida leyes)
    deferencia_ejecutivo REAL,  -- 0 a 1 (cuánto valida actos admin)
    respeto_precedentes REAL,  -- 0 a 1 (adhesión a jurisprudencia)
    innovacion_juridica REAL,  -- 0 a 1 (crea nuevos criterios)

    -- Protección de Derechos
    proteccion_derechos_fundamentales REAL,  -- score general 0 a 1
    proteccion_derechos_sociales REAL,
    proteccion_derechos_consumidor REAL,
    proteccion_trabajador REAL,  -- en materia laboral
    proteccion_niñez REAL,  -- en familia/penal juvenil
    proteccion_medio_ambiente REAL,
    proteccion_acceso_justicia REAL,

    -- Estándares Probatorios y Argumentativos
    estandar_prueba_preferido TEXT,  -- sana_critica, prueba_tasada, libre_conviccion
    rigurosidad_probatoria REAL,  -- qué tan exigente es
    uso_presunciones REAL,
    uso_indicios REAL,
    valoracion_pericial REAL,  -- peso que da a pericias

    -- Tests y Doctrinas Aplicados
    uso_test_proporcionalidad REAL,
    uso_test_razonabilidad REAL,
    uso_control_constitucionalidad REAL,
    uso_interpretacion_conforme REAL,
    uso_in_dubio_pro REAL,  -- trabajador, reo, consumidor, según materia

    -- Fuentes del Derecho (preferencias)
    peso_ley REAL,  -- 0 a 1
    peso_jurisprudencia REAL,
    peso_doctrina REAL,
    peso_derecho_comparado REAL,
    peso_tratados_internacionales REAL,
    peso_constitucion REAL,

    -- Citas Jurisprudenciales
    frecuencia_cita_csjn REAL,  -- cuánto cita Corte Suprema
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
    jueces_que_lo_citan TEXT,  -- JSON array (si tenemos esos datos)
    influencias_doctrinarias TEXT,  -- JSON: autores que cita frecuentemente
    corriente_juridica TEXT,  -- positivista, iusnaturalista, realista, etc.
    escuela_pensamiento TEXT,  -- si se puede identificar

    -- ===== SESGOS Y VALORES =====
    sesgos_detectados TEXT,  -- JSON
    valores_priorizados TEXT,  -- JSON ordenado
    axiomas_judiciales TEXT,  -- JSON: creencias fundamentales del juez

    -- Sesgos Específicos Argentinos
    sesgo_pro_trabajador REAL,  -- en laboral
    sesgo_pro_consumidor REAL,  -- en consumidor
    sesgo_pro_estado REAL,  -- en contencioso
    sesgo_garantista REAL,  -- en penal
    sesgo_punitivista REAL,  -- en penal

    -- ===== CARACTERÍSTICAS DE SENTENCIAS =====
    extension_promedio_sentencias REAL,  -- palabras promedio
    uso_considerandos_extensos BOOLEAN,
    uso_votos_fundados BOOLEAN,  -- si suele fundar extensamente
    claridad_redaccion REAL,  -- 0 a 1
    uso_lenguaje_ciudadano REAL,  -- 0 a 1 (vs lenguaje técnico)

    -- ===== MÉTRICAS DE CALIDAD =====
    coherencia_interna REAL,  -- consistencia entre sus sentencias
    solidez_argumentativa REAL,
    fundamentacion_normativa REAL,  -- cuán bien fundamenta en normas
    fundamentacion_factica REAL,  -- cuán bien analiza los hechos
    originalidad_score REAL,
    impacto_jurisprudencial REAL,  -- cuánto lo citan otros

    -- ===== METADATA =====
    ultima_actualizacion TIMESTAMP,
    version_analyser TEXT,
    confianza_perfil REAL  -- qué tan confiable es el perfil (más sentencias = más confianza)
);
```

#### Tabla: `sentencias_por_juez_arg`

```sql
CREATE TABLE sentencias_por_juez_arg (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- ===== IDENTIFICACIÓN =====
    sentencia_id TEXT UNIQUE NOT NULL,
    juez TEXT NOT NULL,  -- puede ser sala o juez individual
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
    monto_condena REAL,  -- si es cuantificable

    -- Si es Sala/Tribunal Colegiado
    juez_ponente TEXT,
    jueces_firmantes TEXT,  -- JSON array
    votos_disidentes TEXT,  -- JSON si hay
    votos_concurrentes TEXT,  -- JSON si hay

    -- ===== PROCESAMIENTO =====
    texto_completo TEXT,
    ruta_chunks TEXT,
    fecha_procesamiento TIMESTAMP,

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
    innovacion_juridica REAL,  -- si introduce criterio nuevo
    impacto_estimado REAL,  -- basado en citas posteriores

    -- ===== ANÁLISIS PREDICTIVO =====
    factores_decision TEXT,  -- JSON: qué factores fueron determinantes
    prediccion_confianza REAL,  -- si usamos ML, qué tan predecible era

    -- ===== CONTEXTO =====
    sentencia_previa TEXT,  -- ID de sentencia de instancia anterior
    sentencia_posterior TEXT,  -- ID si fue apelada
    recursos_interpuestos TEXT,  -- JSON
    estado_procesal TEXT,  -- firme, apelada, casacion, etc.

    -- ===== CLASIFICACIÓN TEMÁTICA =====
    tags_tematicos TEXT,  -- JSON: despido, discriminacion, daños, etc.
    linea_jurisprudencial_id INTEGER,  -- FK a lineas_jurisprudenciales

    FOREIGN KEY (juez) REFERENCES perfiles_judiciales_argentinos(juez),
    FOREIGN KEY (linea_jurisprudencial_id) REFERENCES lineas_jurisprudenciales(id)
);
```

#### Tabla: `lineas_jurisprudenciales`

```sql
CREATE TABLE lineas_jurisprudenciales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    juez TEXT NOT NULL,

    -- ===== IDENTIFICACIÓN DE LA LÍNEA =====
    tema TEXT NOT NULL,  -- ej: "Despido discriminatorio"
    subtema TEXT,  -- ej: "Por embarazo"
    materia TEXT,  -- laboral, civil, etc.

    -- ===== SENTENCIAS QUE CONFORMAN LA LÍNEA =====
    sentencias_ids TEXT,  -- JSON array de IDs
    cantidad_sentencias INTEGER,
    fecha_primera_sentencia DATE,
    fecha_ultima_sentencia DATE,

    -- ===== CARACTERIZACIÓN DEL CRITERIO =====
    criterio_dominante TEXT,  -- descripción del criterio consistente
    fundamento_principal TEXT,  -- base legal/constitucional
    razonamiento_tipo TEXT,  -- ej: "teleológico + consecuencialista"

    -- Tests/Principios Aplicados
    tests_recurrentes TEXT,  -- JSON
    principios_aplicados TEXT,  -- JSON
    normas_aplicadas TEXT,  -- JSON: artículos que siempre aplica

    -- ===== CONSISTENCIA =====
    consistencia_score REAL,  -- 0 a 1
    sentencias_consistentes INTEGER,
    sentencias_inconsistentes INTEGER,  -- dentro de esta línea
    excepciones_identificadas TEXT,  -- JSON: cuándo se aparta del criterio

    -- ===== PREDICTIBILIDAD =====
    factores_predictivos TEXT,  -- JSON: qué factores predicen que aplique esta línea
    casos_tipo TEXT,  -- JSON: casos paradigmáticos de esta línea

    -- ===== IMPACTO =====
    veces_citada INTEGER,  -- cuántas veces otros citan esta línea
    jueces_que_siguen TEXT,  -- JSON: otros jueces que adoptan este criterio

    -- ===== METADATA =====
    fecha_analisis TIMESTAMP,
    confianza_linea REAL,  -- más sentencias = más confianza

    FOREIGN KEY (juez) REFERENCES perfiles_judiciales_argentinos(juez)
);
```

#### Tabla: `redes_influencia_judicial`

```sql
CREATE TABLE redes_influencia_judicial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- ===== RELACIÓN =====
    juez_origen TEXT NOT NULL,  -- quien cita
    juez_destino TEXT,  -- quien es citado (puede ser NULL si es autor doctrinal)
    tipo_destino TEXT,  -- 'juez', 'sala', 'tribunal_superior', 'csjn', 'autor_doctrinal'

    tipo_influencia TEXT,  -- 'cita_literal', 'adopta_criterio', 'replica', 'distingue', 'rechaza'
    intensidad REAL,  -- 0 a 1 (frecuencia normalizada)

    -- ===== EVIDENCIA =====
    sentencias_evidencia TEXT,  -- JSON array de IDs donde cita
    cantidad_citas INTEGER,
    ejemplos_textuales TEXT,  -- JSON: extractos de las citas

    -- ===== CONTEXTO =====
    temas_comunes TEXT,  -- JSON: en qué temas se da la influencia
    coincidencia_criterio REAL,  -- 0 a 1: si cita para seguir o para distinguir

    -- ===== METADATA =====
    fecha_primera_cita DATE,
    fecha_ultima_cita DATE,
    periodo TEXT,

    FOREIGN KEY (juez_origen) REFERENCES perfiles_judiciales_argentinos(juez)
);
```

#### Tabla: `factores_predictivos`

```sql
CREATE TABLE factores_predictivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    juez TEXT NOT NULL,
    materia TEXT,
    tema TEXT,

    -- ===== FACTORES =====
    factor TEXT,  -- ej: "prueba_testimonial_presente", "monto_reclamo_alto"
    peso REAL,  -- -1 a 1 (negativo = predice rechazo, positivo = predice aceptación)
    confianza REAL,  -- 0 a 1

    -- ===== EVIDENCIA =====
    sentencias_sustento TEXT,  -- JSON array
    ejemplos INTEGER,

    -- ===== METADATA =====
    fecha_calculo TIMESTAMP,

    FOREIGN KEY (juez) REFERENCES perfiles_judiciales_argentinos(juez)
);
```

## 2. Sistema de Preguntas Predeterminadas

### Categorías de Preguntas

#### A. Análisis Individual del Juez

**Perfil General:**
1. ¿Cuál es el perfil cognitivo completo del juez [NOMBRE]?
2. ¿Cuál es el patrón de razonamiento dominante del juez [NOMBRE]?
3. ¿Qué estilo argumentativo caracteriza al juez [NOMBRE]?
4. ¿Cuál es la metodología principal que aplica el juez [NOMBRE]?
5. ¿Qué nivel de complejidad sintáctica presenta el juez [NOMBRE]?
6. ¿Cuál es la densidad conceptual promedio del juez [NOMBRE]?
7. ¿Qué modalidad epistémica predomina en el juez [NOMBRE]?
8. ¿Cuál es el nivel de certeza promedio del juez [NOMBRE]?

**Orientación Judicial:**
9. ¿Tiende el juez [NOMBRE] hacia el activismo o la restricción judicial?
10. ¿Qué tipo de interpretación normativa prefiere el juez [NOMBRE]? (literal, sistemática, teleológica)
11. ¿Es el juez [NOMBRE] más formalista o sustancialista?
12. ¿Cuál es la interpretación constitucional del juez [NOMBRE]? (originalista, evolutiva, mixta)
13. ¿Qué nivel de innovación jurídica presenta el juez [NOMBRE]?

**Deferencia Institucional:**
14. ¿Qué nivel de deferencia muestra el juez [NOMBRE] hacia el poder legislativo?
15. ¿Qué nivel de deferencia muestra el juez [NOMBRE] hacia el poder ejecutivo?
16. ¿Cuál es el nivel de respeto a precedentes del juez [NOMBRE]?
17. ¿Con qué frecuencia el juez [NOMBRE] ejerce control de constitucionalidad?

**Protección de Derechos:**
18. ¿Qué nivel de protección de derechos fundamentales exhibe el juez [NOMBRE]?
19. ¿Qué nivel de protección de derechos sociales muestra el juez [NOMBRE]?
20. ¿Qué nivel de protección del consumidor aplica el juez [NOMBRE]?
21. ¿Qué nivel de protección del trabajador exhibe el juez [NOMBRE]? (en materia laboral)
22. ¿Es el juez [NOMBRE] garantista o punitivista? (en materia penal)
23. ¿Qué nivel de protección de la niñez muestra el juez [NOMBRE]?
24. ¿Qué nivel de protección del medio ambiente aplica el juez [NOMBRE]?
25. ¿Qué nivel de protección del acceso a la justicia exhibe el juez [NOMBRE]?

**Estándares Probatorios:**
26. ¿Qué estándar probatorio prefiere el juez [NOMBRE]?
27. ¿Cuál es el nivel de rigurosidad probatoria del juez [NOMBRE]?
28. ¿Con qué frecuencia el juez [NOMBRE] usa presunciones?
29. ¿Qué peso da el juez [NOMBRE] a las pruebas periciales?
30. ¿Cómo valora el juez [NOMBRE] las pruebas indiciarias?
31. ¿Qué valoración hace el juez [NOMBRE] de la prueba testimonial?

**Tests y Doctrinas:**
32. ¿Con qué frecuencia el juez [NOMBRE] aplica el test de proporcionalidad?
33. ¿Con qué frecuencia el juez [NOMBRE] aplica el test de razonabilidad?
34. ¿Aplica el juez [NOMBRE] el principio "in dubio pro operario"? (en laboral)
35. ¿Aplica el juez [NOMBRE] el principio "in dubio pro reo"? (en penal)
36. ¿Aplica el juez [NOMBRE] el principio "in dubio pro consumidor"?
37. ¿Con qué frecuencia el juez [NOMBRE] usa la interpretación conforme a la constitución?
38. ¿Aplica el juez [NOMBRE] el principio de favorabilidad?

**Fuentes del Derecho:**
39. ¿Qué peso relativo da el juez [NOMBRE] a la ley vs la jurisprudencia?
40. ¿Qué peso da el juez [NOMBRE] a la doctrina en sus decisiones?
41. ¿Con qué frecuencia el juez [NOMBRE] cita derecho comparado?
42. ¿Qué peso da el juez [NOMBRE] a los tratados internacionales?
43. ¿Con qué frecuencia el juez [NOMBRE] cita jurisprudencia de la CSJN?
44. ¿Cuáles son los precedentes que más cita el juez [NOMBRE]?
45. ¿Qué autores doctrinales cita más frecuentemente el juez [NOMBRE]?

**Sesgos y Valores:**
46. ¿Qué sesgos se detectan en el juez [NOMBRE]?
47. ¿Qué valores prioriza el juez [NOMBRE]?
48. ¿Cuáles son los axiomas judiciales del juez [NOMBRE]?
49. ¿Exhibe el juez [NOMBRE] sesgo pro-trabajador en casos laborales?
50. ¿Exhibe el juez [NOMBRE] sesgo pro-consumidor?
51. ¿Exhibe el juez [NOMBRE] sesgo pro-estado en casos contencioso-administrativos?

**Características de Sentencias:**
52. ¿Cuál es la extensión promedio de las sentencias del juez [NOMBRE]?
53. ¿Qué nivel de claridad en la redacción presenta el juez [NOMBRE]?
54. ¿Usa el juez [NOMBRE] lenguaje ciudadano o predominantemente técnico?
55. ¿Cuál es el nivel de solidez argumentativa del juez [NOMBRE]?
56. ¿Qué nivel de fundamentación normativa exhibe el juez [NOMBRE]?
57. ¿Qué nivel de fundamentación fáctica presenta el juez [NOMBRE]?

**Métricas de Calidad:**
58. ¿Cuál es la coherencia interna del juez [NOMBRE]?
59. ¿Cuál es el impacto jurisprudencial del juez [NOMBRE]?
60. ¿Cuál es el nivel de originalidad del juez [NOMBRE]?

#### B. Líneas Jurisprudenciales

**Identificación:**
61. ¿Cuáles son las líneas jurisprudenciales consolidadas del juez [NOMBRE]?
62. ¿Sobre qué temas el juez [NOMBRE] tiene criterios inconsistentes?
63. ¿Cuáles son los temas recurrentes en las sentencias del juez [NOMBRE]?
64. ¿Cuáles son los casos emblemáticos del juez [NOMBRE]?

**Por Tema Específico:**
65. ¿Cuál es el criterio del juez [NOMBRE] sobre [TEMA]? (ej: despido discriminatorio)
66. ¿Qué consistencia muestra el juez [NOMBRE] en casos de [TEMA]?
67. ¿Cuál es el fundamento principal del juez [NOMBRE] en casos de [TEMA]?
68. ¿Qué razonamiento usa típicamente el juez [NOMBRE] en casos de [TEMA]?
69. ¿Qué tests o principios aplica el juez [NOMBRE] en casos de [TEMA]?
70. ¿Qué normas aplica recurrentemente el juez [NOMBRE] en casos de [TEMA]?
71. ¿Cuáles son las excepciones al criterio del juez [NOMBRE] en [TEMA]?
72. ¿Cuáles son los casos paradigmáticos del juez [NOMBRE] en [TEMA]?
73. ¿Cuántas veces ha sido citada la línea del juez [NOMBRE] sobre [TEMA]?

**Análisis de Consistencia:**
74. ¿En qué porcentaje de casos de [TEMA] el juez [NOMBRE] aplica el mismo criterio?
75. ¿Qué factores predicen que el juez [NOMBRE] aplique su línea sobre [TEMA]?
76. ¿Cuándo se aparta el juez [NOMBRE] de su criterio habitual en [TEMA]?

#### C. Redes de Influencia

**Influencias Recibidas:**
77. ¿A qué jueces cita más frecuentemente el juez [NOMBRE]?
78. ¿Qué tribunales superiores influyen más en el juez [NOMBRE]?
79. ¿Qué autores doctrinales influyen más en el juez [NOMBRE]?
80. ¿De qué corriente jurídica es el juez [NOMBRE]? (positivista, iusnaturalista, realista)
81. ¿A qué escuela de pensamiento pertenece el juez [NOMBRE]?

**Influencias Ejercidas:**
82. ¿Qué otros jueces citan al juez [NOMBRE]?
83. ¿En qué temas es más citado el juez [NOMBRE]?
84. ¿Qué nivel de influencia tiene el juez [NOMBRE] en otros magistrados?

**Análisis de Citas:**
85. ¿Cuándo el juez [NOMBRE] cita al juez [OTRO], ¿lo hace para seguir o distinguir su criterio?
86. ¿En qué temas el juez [NOMBRE] sigue la jurisprudencia de [OTRO JUEZ]?
87. ¿Cuáles son los ejemplos textuales de citas del juez [NOMBRE] a [OTRO JUEZ]?
88. ¿Qué nivel de coincidencia de criterio existe entre el juez [NOMBRE] y [OTRO JUEZ]?

#### D. Análisis Predictivo

**Predicción de Decisiones:**
89. ¿Cuáles son los factores que predicen que el juez [NOMBRE] haga lugar a un reclamo de [TIPO]?
90. ¿Qué factores predicen que el juez [NOMBRE] rechace un reclamo de [TIPO]?
91. Si un caso tiene las características [X, Y, Z], ¿cómo decidirá probablemente el juez [NOMBRE]?
92. ¿Qué peso tiene el factor [FACTOR] en las decisiones del juez [NOMBRE]?
93. ¿Qué nivel de confianza tiene la predicción para el juez [NOMBRE] en casos de [TEMA]?

**Factores Determinantes:**
94. ¿Cuáles son los factores más determinantes en las decisiones del juez [NOMBRE]?
95. ¿Qué tipo de prueba es más persuasiva para el juez [NOMBRE]?
96. ¿Qué argumentos legales son más efectivos ante el juez [NOMBRE]?
97. ¿Importa el monto del reclamo en las decisiones del juez [NOMBRE]?
98. ¿Influye la presencia de vulnerabilidad en las decisiones del juez [NOMBRE]?

**Patrones de Decisión:**
99. ¿Con qué frecuencia el juez [NOMBRE] hace lugar a reclamos de [TIPO]?
100. ¿Cuál es la tasa de aceptación del juez [NOMBRE] en casos de [MATERIA]?
101. ¿Cómo distribuye el juez [NOMBRE] las costas procesales?
102. ¿Con qué frecuencia el juez [NOMBRE] condena en costas al actor vs al demandado?
103. ¿Qué tan previsibles son las decisiones del juez [NOMBRE]?

#### E. Análisis por Materia

**Especialización:**
104. ¿Cuál es el área de especialización principal del juez [NOMBRE]?
105. ¿En qué materias tiene más experiencia el juez [NOMBRE]?
106. ¿Qué nivel de expertise tiene el juez [NOMBRE] en [MATERIA]?

**Análisis Comparativo por Materia:**
107. ¿Cómo aborda el juez [NOMBRE] los casos de derecho laboral vs los de derecho civil?
108. ¿Es más garantista el juez [NOMBRE] en materia penal o en otras materias?
109. ¿Varía el estilo argumentativo del juez [NOMBRE] según la materia?

#### F. Análisis de Sentencias Específicas

**Sentencia Individual:**
110. ¿Cuál es el análisis completo de la sentencia [ID/CARATULA]?
111. ¿Qué razonamientos identificó el análisis en la sentencia [ID]?
112. ¿Se detectaron falacias en la sentencia [ID]?
113. ¿Qué normas citó el juez [NOMBRE] en la sentencia [ID]?
114. ¿Qué jurisprudencia citó el juez [NOMBRE] en la sentencia [ID]?
115. ¿Qué doctrina citó el juez [NOMBRE] en la sentencia [ID]?
116. ¿Qué tests o principios aplicó el juez [NOMBRE] en la sentencia [ID]?
117. ¿Cuál fue el factor determinante en la sentencia [ID]?
118. ¿Qué nivel de innovación jurídica presenta la sentencia [ID]?
119. ¿Qué nivel de solidez argumentativa tiene la sentencia [ID]?
120. ¿Es consistente la sentencia [ID] con el perfil habitual del juez [NOMBRE]?

**Contexto Procesal:**
121. ¿Cuál fue la sentencia de instancia anterior en el caso [ID]?
122. ¿Fue apelada la sentencia [ID]? ¿Qué pasó en instancia superior?
123. ¿Qué recursos se interpusieron contra la sentencia [ID]?

#### G. Búsquedas Temáticas Complejas

**Búsquedas Cruzadas:**
124. ¿Qué jueces han decidido sobre [TEMA] en los últimos [X] años?
125. ¿Qué criterios diferentes existen sobre [TEMA] en [FUERO]?
126. ¿Qué jueces son más protectores del [DERECHO ESPECÍFICO]?
127. ¿Qué jueces aplican más frecuentemente el test de [NOMBRE DEL TEST]?
128. ¿Qué jueces citan más a la CSJN en materia de [TEMA]?
129. ¿Qué jueces son más innovadores en [MATERIA]?
130. ¿Qué jueces tienen mayor consistencia interna en [TEMA]?

**Análisis de Tendencias:**
131. ¿Hay una tendencia general hacia mayor activismo en [FUERO]?
132. ¿Aumentó la protección del [DERECHO] en la jurisprudencia de [TRIBUNAL]?
133. ¿Qué nuevas líneas jurisprudenciales emergieron en [AÑO/PERÍODO]?

#### H. Informes Integrales

**Informes Estándar:**
134. Generar informe completo del juez [NOMBRE]
135. Generar informe de líneas jurisprudenciales del juez [NOMBRE]
136. Generar informe de red de influencias del juez [NOMBRE]
137. Generar informe de factores predictivos del juez [NOMBRE]
138. Generar informe comparativo: juez [NOMBRE] vs perfil promedio de [FUERO]
139. Generar informe de casos emblemáticos del juez [NOMBRE]
140. Generar informe de consistencia del juez [NOMBRE] por temas

**Informes Personalizados:**
141. Generar informe sobre cómo el juez [NOMBRE] decide casos de [TIPO ESPECÍFICO]
142. Generar informe de recomendaciones para litigar ante el juez [NOMBRE]
143. Generar informe de análisis predictivo para caso con características [X, Y, Z] ante juez [NOMBRE]

## 3. Sistema de Informes Escritos

### A. Estructura de Informes

#### Informe Completo del Juez

**Secciones:**

**1. PORTADA**
- Nombre del juez/sala
- Tribunal
- Fuero, instancia, jurisdicción
- Fecha del informe
- Período analizado
- Cantidad de sentencias analizadas

**2. RESUMEN EJECUTIVO** (1-2 páginas)
- Perfil judicial en 5-10 puntos clave
- Características distintivas
- Áreas de especialización
- Nivel de predictibilidad

**3. PERFIL COGNITIVO** (3-5 páginas)
- Metodología principal
- Patrón de razonamiento dominante
- Estilo argumentativo
- Complejidad y claridad
- Modalidad epistémica
- Marcadores lingüísticos distintivos

**4. ORIENTACIÓN JUDICIAL** (2-3 páginas)
- Activismo vs restricción
- Interpretación normativa preferida
- Formalismo vs sustancialismo
- Nivel de innovación jurídica

**5. PROTECCIÓN DE DERECHOS** (2-3 páginas)
- Derechos fundamentales
- Derechos sociales
- Protección de vulnerables (trabajador, consumidor, niñez, etc.)
- Gráficos de radar con scores

**6. METODOLOGÍA PROBATORIA Y ARGUMENTATIVA** (2-3 páginas)
- Estándares probatorios preferidos
- Rigurosidad probatoria
- Tests y doctrinas aplicados
- Principios invocados frecuentemente

**7. FUENTES DEL DERECHO** (2 páginas)
- Peso relativo: ley, jurisprudencia, doctrina, etc.
- Frecuencia de citas a CSJN
- Precedentes más citados
- Autores doctrinales preferidos

**8. LÍNEAS JURISPRUDENCIALES** (5-10 páginas)
Por cada línea consolidada:
- Tema
- Criterio dominante
- Fundamentación
- Sentencias que la conforman
- Consistencia (%)
- Factores predictivos
- Casos paradigmáticos

**9. RED DE INFLUENCIAS** (3-5 páginas)
- Jueces/tribunales que más cita
- Jueces/tribunales que lo citan
- Autores doctrinales influyentes
- Corriente jurídica
- Diagrama de red de influencias

**10. ANÁLISIS PREDICTIVO** (5-7 páginas)
Por materia/tema principal:
- Factores que predicen aceptación
- Factores que predicen rechazo
- Tabla de factores con pesos
- Nivel de confianza de predicciones
- Casos de ejemplo

**11. SESGOS Y VALORES** (2-3 páginas)
- Sesgos detectados (con evidencia)
- Valores priorizados
- Axiomas judiciales fundamentales

**12. MÉTRICAS DE CALIDAD** (1-2 páginas)
- Coherencia interna
- Solidez argumentativa
- Fundamentación (normativa y fáctica)
- Impacto jurisprudencial
- Originalidad
- Claridad

**13. CASOS EMBLEMÁTICOS** (3-5 páginas)
- Top 5-10 casos más representativos
- Análisis de cada uno
- Por qué son emblemáticos

**14. APÉNDICES**
- Lista completa de sentencias analizadas
- Metodología del análisis
- Glosario de términos técnicos

**Total: 35-55 páginas**

#### Informe de Línea Jurisprudencial Específica

**Secciones:**

**1. IDENTIFICACIÓN**
- Juez/sala
- Tema y subtema
- Período analizado
- Cantidad de sentencias

**2. CARACTERIZACIÓN DEL CRITERIO**
- Criterio dominante (descripción detallada)
- Fundamento legal/constitucional
- Razonamiento típico empleado
- Tests/principios aplicados

**3. ANÁLISIS DE SENTENCIAS**
- Lista de sentencias que conforman la línea
- Análisis de cada una (resumen)
- Citas textuales clave

**4. CONSISTENCIA**
- Score de consistencia
- Sentencias consistentes vs inconsistentes
- Análisis de excepciones

**5. FACTORES PREDICTIVOS**
- Qué factores activan esta línea
- Casos tipo
- Tabla de factores

**6. IMPACTO**
- Citas por otros jueces
- Adopción del criterio
- Relevancia jurisprudencial

**7. CASOS PARADIGMÁTICOS**
- Top 3-5 casos que definen la línea
- Análisis detallado de cada uno

**Total: 15-25 páginas**

#### Informe de Red de Influencias

**Secciones:**

**1. MAPA DE INFLUENCIAS**
- Diagrama visual de la red
- Descripción de nodos y relaciones

**2. INFLUENCIAS RECIBIDAS**
- Top 10 jueces/tribunales que más cita
- Frecuencia y contexto
- Ejemplos textuales
- Nivel de coincidencia de criterio

**3. INFLUENCIAS EJERCIDAS**
- Jueces que lo citan
- Frecuencia y temas
- Impacto de su jurisprudencia

**4. INFLUENCIAS DOCTRINALES**
- Autores más citados
- Corriente jurídica
- Escuela de pensamiento

**5. ANÁLISIS DE RELACIONES CLAVE**
- Análisis profundo de top 3-5 relaciones
- Evolución temporal de la influencia
- Temas de convergencia/divergencia

**Total: 10-15 páginas**

#### Informe Predictivo para Litigación

**Secciones:**

**1. CARACTERÍSTICAS DEL CASO**
- Descripción del caso hipotético/real
- Factores presentes
- Materia y tema

**2. PERFIL DEL JUEZ RELEVANTE**
- Resumen del perfil
- Líneas jurisprudenciales aplicables
- Sesgos y valores relevantes

**3. PREDICCIÓN**
- Probabilidad de éxito (%)
- Fundamentación de la predicción
- Nivel de confianza

**4. FACTORES DETERMINANTES**
- Factores favorables presentes
- Factores desfavorables presentes
- Peso de cada factor

**5. ESTRATEGIA SUGERIDA**
- Argumentos más efectivos
- Pruebas más persuasivas
- Precedentes que citar
- Tests/principios que invocar
- Puntos a evitar

**6. CASOS SIMILARES DECIDIDOS**
- Top 5 casos más parecidos
- Cómo los decidió el juez
- Lecciones extraídas

**Total: 10-15 páginas**

### B. Formato de Informes

**Características:**
- Formato: PDF profesional
- Tipografía: serif para cuerpo (Times, Garamond), sans-serif para títulos
- Inclusión de:
  - Tablas de datos
  - Gráficos (radares, barras, líneas temporales)
  - Diagramas de red
  - Extractos textuales destacados
  - Notas al pie con referencias
  - Índice navegable
  - Marca de agua con fecha y confidencialidad

**Estilos de redacción:**
- Académico pero accesible
- Basado en datos
- Con citas textuales de sentencias
- Conclusiones fundamentadas
- Sin juicios de valor, descriptivo

## 4. Scripts de Análisis Ajustados

### A. `analizador_pensamiento_judicial_arg.py`

**Funciones principales:**

```python
def analizar_orientacion_judicial(texto_sentencia):
    """
    Analiza:
    - Activismo vs restricción
    - Interpretación normativa
    - Formalismo vs sustancialismo
    - Deferencia institucional
    """
    pass

def analizar_proteccion_derechos(texto_sentencia, materia):
    """
    Detecta nivel de protección de derechos específicos
    según la materia
    """
    pass

def analizar_estandares_probatorios(texto_sentencia):
    """
    Identifica:
    - Estándar aplicado
    - Rigurosidad
    - Uso de presunciones/indicios
    - Valoración de pericias
    """
    pass

def detectar_tests_doctrinas(texto_sentencia):
    """
    Detecta aplicación de:
    - Test de proporcionalidad
    - Test de razonabilidad
    - In dubio pro (operario/reo/consumidor)
    - Interpretación conforme
    - Etc.
    """
    pass

def analizar_fuentes_derecho(texto_sentencia):
    """
    Extrae y cuantifica citas a:
    - Leyes y códigos
    - Jurisprudencia (CSJN, cámaras, otros)
    - Doctrina
    - Tratados internacionales
    - Derecho comparado
    """
    pass

def detectar_sesgos_argentinos(texto_sentencia, materia):
    """
    Detecta sesgos específicos:
    - Pro-trabajador (laboral)
    - Pro-consumidor
    - Pro-estado (contencioso)
    - Garantista/punitivista (penal)
    """
    pass
```

### B. `analizador_lineas_jurisprudenciales.py`

**Funciones principales:**

```python
def identificar_lineas(juez_id):
    """
    Agrupa sentencias por temas
    Identifica criterios consistentes
    """
    pass

def calcular_consistencia_linea(sentencias_ids):
    """
    Calcula qué tan consistente es el criterio
    Identifica excepciones
    """
    pass

def extraer_criterio_dominante(sentencias_ids):
    """
    Identifica el criterio común
    Extrae fundamentos
    Caracteriza razonamiento
    """
    pass

def identificar_factores_predictivos(linea_id):
    """
    Encuentra qué factores activan esta línea
    Machine learning para pesos
    """
    pass

def encontrar_casos_paradigmaticos(linea_id):
    """
    Identifica los casos más representativos
    Basado en claridad, impacto, innovación
    """
    pass
```

### C. `analizador_redes_influencia.py`

**Funciones principales:**

```python
def extraer_citas_jurisprudenciales(texto_sentencia):
    """
    Extrae todas las citas a otros fallos
    Identifica: tribunal, fecha, partes, tema
    """
    pass

def extraer_citas_doctrinales(texto_sentencia):
    """
    Extrae citas a autores
    Identifica libros, artículos
    """
    pass

def construir_red_influencias(juez_id):
    """
    Construye grafo de influencias
    Nodos: jueces, autores
    Aristas: citas, con peso por frecuencia
    """
    pass

def calcular_metricas_red(juez_id):
    """
    Calcula:
    - Centralidad
    - Clustering
    - Betweenness
    """
    pass

def identificar_clusters(todos_jueces):
    """
    Agrupa jueces por similitud de citas
    Identifica escuelas de pensamiento
    """
    pass
```

### D. `motor_predictivo.py`

**Funciones principales:**

```python
def extraer_factores_caso(datos_caso):
    """
    De un caso extrae factores relevantes:
    - Tipo de reclamo
    - Monto
    - Tipo de prueba disponible
    - Vulnerabilidad de partes
    - Etc.
    """
    pass

def predecir_decision(juez_id, factores_caso):
    """
    Basado en casos previos del juez,
    predice resultado
    Retorna: probabilidad, confianza, fundamentación
    """
    pass

def calcular_pesos_factores(juez_id, materia):
    """
    Machine learning para calcular
    qué factores son más determinantes
    """
    pass

def recomendar_estrategia(juez_id, factores_caso):
    """
    Basado en predicción, sugiere:
    - Argumentos efectivos
    - Pruebas clave
    - Precedentes a citar
    """
    pass
```

### E. `generador_informes.py`

**Funciones principales:**

```python
def generar_informe_completo(juez_id):
    """
    Genera informe PDF completo (35-55 pág)
    """
    pass

def generar_informe_linea(linea_id):
    """
    Genera informe de línea jurisprudencial (15-25 pág)
    """
    pass

def generar_informe_red(juez_id):
    """
    Genera informe de red de influencias (10-15 pág)
    """
    pass

def generar_informe_predictivo(juez_id, datos_caso):
    """
    Genera informe predictivo para litigar (10-15 pág)
    """
    pass

def generar_respuesta_pregunta(pregunta_id, parametros):
    """
    Genera respuesta textual a una pregunta predeterminada
    """
    pass
```

## 5. Flujo de Trabajo Ajustado

```
1. INGESTA
   ├─ Subir PDF/TXT de sentencia
   ├─ Extraer texto
   ├─ Identificar juez (ya viene en metadata)
   ├─ Extraer metadata procesal argentina
   └─ Chunking + embeddings

2. ANÁLISIS INDIVIDUAL
   ├─ Análisis cognitivo (ANALYSER v2.0 existente)
   ├─ Análisis judicial argentino (nuevo)
   │   ├─ Orientación judicial
   │   ├─ Protección derechos
   │   ├─ Estándares probatorios
   │   ├─ Tests y doctrinas
   │   ├─ Fuentes del derecho
   │   └─ Sesgos
   └─ Guardar en sentencias_por_juez_arg

3. EXTRACCIÓN DE RELACIONES
   ├─ Extraer citas jurisprudenciales
   ├─ Extraer citas doctrinales
   ├─ Guardar en redes_influencia_judicial
   └─ Actualizar red

4. AGREGACIÓN POR JUEZ
   ├─ Combinar perfiles de todas sus sentencias
   ├─ Calcular métricas agregadas
   ├─ Actualizar perfiles_judiciales_argentinos
   └─ Incrementar contador de sentencias

5. ANÁLISIS DE LÍNEAS
   ├─ Agrupar sentencias por temas
   ├─ Identificar criterios consistentes
   ├─ Calcular consistencia
   ├─ Extraer factores predictivos
   └─ Guardar en lineas_jurisprudenciales

6. ANÁLISIS PREDICTIVO
   ├─ Machine learning sobre casos previos
   ├─ Calcular pesos de factores
   ├─ Guardar en factores_predictivos
   └─ Validar predicciones

7. GENERACIÓN DE INFORMES/RESPUESTAS
   ├─ Consulta de usuario (pregunta o solicitud de informe)
   ├─ Recuperar datos de BD
   ├─ Generar informe PDF o respuesta textual
   └─ Entregar al usuario
```

## 6. Plan de Implementación Ajustado

### Fase 1: Fundamentos (Semanas 1-2)
- [ ] Crear esquema de BD: `juez_centrico_arg.db`
- [ ] Crear tablas con campos argentinos
- [ ] Sistema de ingesta de sentencias (PDF/TXT)
- [ ] Extracción de metadata procesal argentina
- [ ] Adaptar orchestrador para flujo ajustado

### Fase 2: Análisis Individual (Semanas 3-4)
- [ ] Implementar `analizador_pensamiento_judicial_arg.py`
  - [ ] Orientación judicial
  - [ ] Protección de derechos
  - [ ] Estándares probatorios
  - [ ] Tests y doctrinas
  - [ ] Fuentes del derecho
  - [ ] Sesgos argentinos
- [ ] Integrar con ANALYSER v2.0 existente
- [ ] Testing con sentencias reales

### Fase 3: Líneas y Redes (Semanas 5-6)
- [ ] Implementar `analizador_lineas_jurisprudenciales.py`
  - [ ] Identificación de líneas
  - [ ] Cálculo de consistencia
  - [ ] Extracción de criterios
  - [ ] Casos paradigmáticos
- [ ] Implementar `analizador_redes_influencia.py`
  - [ ] Extracción de citas
  - [ ] Construcción de red
  - [ ] Métricas de red
  - [ ] Identificación de clusters

### Fase 4: Predictivo (Semanas 7-8)
- [ ] Implementar `motor_predictivo.py`
  - [ ] Extracción de factores
  - [ ] Modelo de predicción (ML)
  - [ ] Cálculo de pesos
  - [ ] Validación
- [ ] Integrar con líneas jurisprudenciales
- [ ] Testing de precisión

### Fase 5: Informes y Preguntas (Semanas 9-10)
- [ ] Implementar `generador_informes.py`
  - [ ] Informe completo del juez
  - [ ] Informe de línea jurisprudencial
  - [ ] Informe de red
  - [ ] Informe predictivo
- [ ] Sistema de preguntas predeterminadas
- [ ] Generación de PDFs profesionales
- [ ] Gráficos y visualizaciones para informes

### Fase 6: Interfaz y UX (Semanas 11-12)
- [ ] Actualizar interfaz web Flask
  - [ ] Vista de jueces
  - [ ] Vista de sentencias
  - [ ] Formulario de preguntas
  - [ ] Descarga de informes
- [ ] Sistema de búsqueda avanzada
- [ ] Panel de control

### Fase 7: Optimización (Semanas 13-14)
- [ ] Optimización de consultas BD
- [ ] Cache de informes
- [ ] Mejoras de ML
- [ ] Documentación completa
- [ ] Manual de usuario

## 7. Tecnologías

**Ajustes a la stack tecnológica:**

- **Backend**: Python 3.9+, Flask (sin cambios)
- **Base de Datos**: SQLite → considerar PostgreSQL si crece
- **ML/NLP**:
  - Sentence Transformers (existente)
  - spaCy + BERT español (existente)
  - **NUEVO**: Scikit-learn (Random Forest, Logistic Regression para predictivo)
  - **NUEVO**: XGBoost (para análisis predictivo avanzado)
  - NetworkX (para redes de influencia)
- **Generación de PDFs**:
  - **NUEVO**: ReportLab o WeasyPrint
  - **NUEVO**: Matplotlib/Seaborn para gráficos
- **Extracción de metadatos**:
  - **NUEVO**: Regex avanzado para metadata argentina
  - **NUEVO**: NER fine-tuned para entidades jurídicas argentinas

## 8. Métricas de Éxito

**KPIs del sistema:**

1. **Cobertura**: % de sentencias procesadas exitosamente
2. **Precisión de extracción**: % de metadata correctamente extraída
3. **Consistencia detectada**: % de líneas jurisprudenciales identificadas con consistencia > 0.8
4. **Precisión predictiva**: % de predicciones correctas (validación retrospectiva)
5. **Completitud de red**: % de citas jurisprudenciales identificadas
6. **Tiempo de procesamiento**: minutos por sentencia
7. **Calidad de informes**: evaluación cualitativa por usuarios

## Conclusión

Esta propuesta ajustada se enfoca en:

✅ Análisis profundo individual de cada juez
✅ Redes de influencia judicial
✅ Líneas jurisprudenciales con alta consistencia
✅ Análisis predictivo robusto
✅ 140+ preguntas predeterminadas
✅ Informes escritos profesionales en PDF
✅ Contexto judicial argentino específico
✅ Sin comparaciones innecesarias entre jueces
✅ Sin análisis temporal (simplificación)

El sistema resultante será una herramienta potente para:
- **Investigación académica**: Estudios empíricos del razonamiento judicial
- **Litigación**: Estrategias basadas en datos del juez
- **Periodismo de datos**: Análisis de tendencias judiciales
- **Formación judicial**: Aprendizaje de mejores prácticas

**¿Procedo con la implementación de la Fase 1?**
