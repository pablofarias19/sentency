# Fase 2: Análisis Cognitivo y Judicial Completo

## 🎯 Implementación Completada

La Fase 2 añade el análisis profundo de las sentencias con:

✅ Analizador de pensamiento judicial argentino
✅ Procesador completo que integra análisis cognitivo + judicial
✅ Agregador de perfiles por juez (métricas consolidadas)
✅ Detección automática de tests y doctrinas argentinas
✅ Análisis de protección de derechos específicos
✅ Detección de sesgos característicos argentinos
✅ Estándares probatorios y fuentes del derecho

## 📁 Archivos Creados

### 1. Analizador de Pensamiento Judicial Argentino
**Archivo**: `colaborative/scripts/analizador_pensamiento_judicial_arg.py`

**Analiza específicamente**:

#### 🏛️ Activismo Judicial
- Control de constitucionalidad
- Interpretación expansiva vs literal
- Creación de precedentes
- Supervisión de políticas públicas
- **Score**: -1 (restricción) a +1 (activismo)

#### 📖 Interpretación Normativa
- Literal
- Sistemática
- Teleológica
- Histórica
- Evolutiva
- **Resultado**: Tipo dominante + scores

#### ⚖️ Formalismo vs Sustancialismo
- Indicadores de formalismo (forma, procedimiento)
- Indicadores de sustancialismo (fondo, equidad)
- **Score**: -1 (formalista) a +1 (sustancialista)

#### 🛡️ Protección de Derechos
Detecta nivel de protección de:
- Libertad de expresión
- Igualdad y no discriminación
- Debido proceso
- Intimidad y privacidad
- Propiedad
- Trabajo
- Salud
- Ambiente
- Vivienda
- Educación
- Derechos de la niñez
- **Score por derecho**: 0 a 1

#### 🔬 Tests y Doctrinas Argentinas
Detecta aplicación de:
- Test de proporcionalidad
- Test de razonabilidad (Art. 28 CN)
- Escrutinio estricto/intermedio
- Control de convencionalidad
- Doctrina de arbitrariedad
- Gravedad institucional
- Caso federal

#### ⚖️ Principios In Dubio Pro
- In dubio pro operario (trabajador)
- In dubio pro reo (imputado)
- In dubio pro consumidor
- Pro homine (persona)
- Pro actione (acceso a justicia)
- Pro natura (ambiente)

#### 📊 Estándares Probatorios
- Sana crítica
- Prueba tasada
- Libre convicción
- Certeza positiva
- Más allá de toda duda razonable
- Verosimilitud/prima facie

#### 📚 Fuentes del Derecho
Cuantifica citas a:
- CSJN (Corte Suprema)
- Cámaras y Salas
- Código Civil y Comercial
- Constitución Nacional
- LCT (Ley de Contrato de Trabajo)
- Ley de Defensa del Consumidor
- Tratados de DDHH (CADH, PIDCP)
- Doctrina

#### ⚠️ Sesgos Argentinos Específicos
Detecta:
- Pro-trabajador
- Pro-consumidor
- Pro-estado
- Garantista
- Punitivista

#### 🏛️ Deferencia Institucional
- Deferencia al legislativo (0-1)
- Deferencia al ejecutivo (0-1)

**Uso**:
```python
from analizador_pensamiento_judicial_arg import AnalizadorPensamientoJudicialArg

analizador = AnalizadorPensamientoJudicialArg()
analisis = analizador.analizar(texto_sentencia)

# Imprimir resumen
analizador.imprimir_resumen(analisis)

# Exportar JSON
json_output = analizador.exportar_json(analisis)
```

### 2. Procesador Completo de Sentencias
**Archivo**: `colaborative/scripts/procesador_sentencias_completo.py`

**Funcionalidades**:
- Obtiene sentencias de la BD
- Aplica análisis cognitivo (ANALYSER v2.0 si está disponible)
- Aplica análisis judicial argentino
- Combina ambos análisis
- Guarda en la BD
- Actualiza perfil del juez

**Uso**:
```bash
cd App_colaborativa/colaborative/scripts

# Procesar una sentencia específica
python procesador_sentencias_completo.py SENT_12345

# Procesar todas las sentencias pendientes
python procesador_sentencias_completo.py --batch

# Procesar con límite
python procesador_sentencias_completo.py --batch --limite 10
```

**Salida esperada**:
```
======================================================================
PROCESANDO SENTENCIA: SENT_12345_2023
======================================================================

ℹ Obteniendo sentencia de la BD...
✓ Sentencia obtenida - Juez: Dr. Juan Pérez, Materia: despido
ℹ Analizando sentencia (15234 caracteres)...
ℹ Ejecutando análisis judicial argentino...
✓ Análisis judicial completado
✓ ANALYSER v2.0 cargado
ℹ Ejecutando análisis cognitivo (ANALYSER v2.0)...
✓ Análisis cognitivo completado
ℹ Guardando análisis en BD...
✓ Análisis guardado para: SENT_12345_2023
ℹ Actualizando perfil del juez: Dr. Juan Pérez
✓ Perfil actualizado para: Dr. Juan Pérez

✓ SENTENCIA PROCESADA EXITOSAMENTE
```

### 3. Agregador de Perfiles de Jueces
**Archivo**: `colaborative/scripts/agregador_perfiles_jueces.py`

**Funcionalidades**:
- Obtiene todas las sentencias de un juez
- Extrae análisis individuales
- Calcula promedios de métricas
- Identifica patrones consistentes
- Determina tipos dominantes (moda)
- Identifica temas recurrentes
- Calcula confianza del perfil
- Actualiza perfil consolidado en BD

**Cálculos que realiza**:
- **Promedios**: activismo, formalismo, protección de derechos, deferencia
- **Moda**: interpretación normativa, estándar probatorio, sesgo dominante
- **Frecuencias**: temas recurrentes, tests más aplicados
- **Confianza**: basada en cantidad de sentencias (más sentencias = más confianza)

**Uso**:
```bash
cd App_colaborativa/colaborative/scripts

# Agregar perfil de un juez específico
python agregador_perfiles_jueces.py "Dr. Juan Pérez"

# Agregar perfiles de TODOS los jueces
python agregador_perfiles_jueces.py --todos
```

**Salida esperada**:
```
Agregando perfil para: Dr. Juan Pérez
ℹ Obteniendo sentencias...
✓ Sentencias encontradas: 15
ℹ Agregando análisis judicial...
ℹ Agregando análisis cognitivo...
ℹ Actualizando base de datos...
✓ Perfil actualizado exitosamente
ℹ   - Sentencias: 15
ℹ   - Confianza: 0.85
ℹ   - Temas: despido, daños, divorcio
```

## 🚀 Flujo de Trabajo Completo

### Flujo Recomendado: De Ingesta a Análisis

```bash
cd App_colaborativa/colaborative/scripts

# PASO 1: Ingestar sentencias (si aún no lo hiciste)
python ingesta_sentencias_judicial.py ../data/pdfs/

# PASO 2: Procesar sentencias (análisis completo)
python procesador_sentencias_completo.py --batch

# PASO 3: Agregar perfiles de jueces
python agregador_perfiles_jueces.py --todos
```

### Flujo Alternativo: Procesar un Solo Juez

```bash
# PASO 1: Ver qué sentencias tiene un juez
sqlite3 ../bases_rag/cognitiva/juez_centrico_arg.db
> SELECT sentencia_id FROM sentencias_por_juez_arg WHERE juez = 'Dr. Juan Pérez';

# PASO 2: Procesar cada sentencia
python procesador_sentencias_completo.py SENT_12345
python procesador_sentencias_completo.py SENT_12346
# ... etc

# PASO 3: Agregar perfil del juez
python agregador_perfiles_jueces.py "Dr. Juan Pérez"
```

## 📊 ¿Qué se Guarda en la BD?

### En `sentencias_por_juez_arg`

Cada sentencia analizada tiene:

**Campo `perfil_cognitivo`** (JSON):
```json
{
  "timestamp": "2025-11-12T...",
  "version_analyser": "1.0",
  "analisis_judicial": {
    "tendencia_activismo": 0.45,
    "interpretacion_normativa": "teleologica",
    "formalismo_vs_sustancialismo": 0.32,
    "derechos_protegidos": {
      "trabajo": 0.87,
      "igualdad": 0.56,
      "debido_proceso": 0.43
    },
    "tests_aplicados": {
      "test_razonabilidad": 0.72,
      "test_proporcionalidad": 0.34
    },
    "estandar_prueba": "sana_critica",
    "sesgo_dominante": "pro_trabajador",
    "deferencia_legislativo": 0.12,
    "deferencia_ejecutivo": 0.08
  },
  "analisis_cognitivo": {
    ...
  }
}
```

**Campo `razonamientos_identificados`** (JSON):
```json
["deductivo", "teleologico", "autoritativo"]
```

**Campo `tests_aplicados`** (JSON):
```json
["test_razonabilidad", "in_dubio_pro_operario"]
```

### En `perfiles_judiciales_argentinos`

Cada juez tiene métricas agregadas:

```sql
SELECT
  juez,
  total_sentencias_analizadas,
  tendencia_activismo,           -- Promedio de todas sus sentencias
  interpretacion_normativa,      -- Moda (tipo más frecuente)
  formalismo_vs_sustancialismo,  -- Promedio
  proteccion_derechos_fundamentales,  -- Promedio
  deferencia_legislativo,        -- Promedio
  deferencia_ejecutivo,          -- Promedio
  estandar_prueba_preferido,     -- Moda
  temas_recurrentes,             -- JSON con temas más frecuentes
  confianza_perfil               -- 0-1, basado en cantidad de sentencias
FROM perfiles_judiciales_argentinos
WHERE juez = 'Dr. Juan Pérez';
```

## 📈 Métricas y Scores

### Escala de Activismo
- **+1.0**: Activismo extremo (invalida leyes, crea precedentes, supervisión activa)
- **+0.5**: Activismo moderado
- **0.0**: Equilibrado
- **-0.5**: Restricción moderada
- **-1.0**: Restricción extrema (deferencia total, interpretación literal)

### Escala de Formalismo
- **+1.0**: Sustancialista extremo (prioriza fondo sobre forma)
- **+0.5**: Sustancialista moderado
- **0.0**: Equilibrado
- **-0.5**: Formalista moderado
- **-1.0**: Formalista extremo (apego estricto a formas)

### Protección de Derechos (0-1)
- **0.0-0.3**: Protección baja
- **0.3-0.6**: Protección moderada
- **0.6-0.8**: Protección alta
- **0.8-1.0**: Protección muy alta

### Deferencia (0-1)
- **0.0-0.3**: Baja deferencia (revisión judicial activa)
- **0.3-0.6**: Deferencia moderada
- **0.6-1.0**: Alta deferencia (respeto a otros poderes)

### Confianza del Perfil (0-1)
- **0.0-0.3**: Baja (1-2 sentencias)
- **0.3-0.5**: Media-baja (3-4 sentencias)
- **0.5-0.7**: Media (5-9 sentencias)
- **0.7-0.85**: Alta (10-19 sentencias)
- **0.85-1.0**: Muy alta (20+ sentencias)

## 🔍 Consultas Útiles

### Ver Sentencias Analizadas

```sql
-- Sentencias con análisis completo
SELECT
  sentencia_id,
  juez,
  materia,
  fecha_sentencia,
  LENGTH(perfil_cognitivo) as tamano_analisis
FROM sentencias_por_juez_arg
WHERE perfil_cognitivo IS NOT NULL
ORDER BY fecha_procesamiento DESC;
```

### Ver Perfil de un Juez

```sql
SELECT
  juez,
  total_sentencias_analizadas,
  ROUND(tendencia_activismo, 2) as activismo,
  interpretacion_normativa,
  ROUND(formalismo_vs_sustancialismo, 2) as formalismo,
  ROUND(proteccion_derechos_fundamentales, 2) as proteccion_derechos,
  ROUND(confianza_perfil, 2) as confianza,
  temas_recurrentes
FROM perfiles_judiciales_argentinos
WHERE juez = 'Dr. Juan Pérez';
```

### Top Jueces por Activismo

```sql
SELECT
  juez,
  total_sentencias_analizadas,
  ROUND(tendencia_activismo, 2) as activismo,
  fuero
FROM perfiles_judiciales_argentinos
WHERE total_sentencias_analizadas >= 5  -- Solo con suficientes datos
ORDER BY tendencia_activismo DESC
LIMIT 10;
```

### Jueces Garantistas

```sql
SELECT
  juez,
  total_sentencias_analizadas,
  ROUND(proteccion_derechos_fundamentales, 2) as proteccion,
  ROUND(deferencia_legislativo, 2) as def_legislativo,
  fuero
FROM perfiles_judiciales_argentinos
WHERE proteccion_derechos_fundamentales > 0.7
  AND total_sentencias_analizadas >= 5
ORDER BY proteccion_derechos_fundamentales DESC;
```

## 🐛 Troubleshooting

### Error: "ANALYSER v2.0 no disponible"

**Causa**: No se encuentra el módulo `analyser_metodo_mejorado.py`

**Solución**: El sistema funciona sin él, solo usa análisis judicial. Si quieres el análisis cognitivo completo, asegúrate de que el archivo exista en el directorio de scripts.

### Sentencias sin Análisis

**Verificar**:
```bash
sqlite3 ../bases_rag/cognitiva/juez_centrico_arg.db
> SELECT COUNT(*) FROM sentencias_por_juez_arg WHERE perfil_cognitivo IS NULL;
```

**Procesar pendientes**:
```bash
python procesador_sentencias_completo.py --batch
```

### Perfil de Juez No Actualizado

**Causa**: No se ejecutó el agregador después de procesar sentencias

**Solución**:
```bash
python agregador_perfiles_jueces.py "Nombre del Juez"
```

### Score de Confianza Bajo

**Causa**: Pocas sentencias analizadas

**Solución**: Normal. El sistema aumenta la confianza automáticamente a medida que se procesan más sentencias del mismo juez.

## 📝 Interpretación de Resultados

### Ejemplo: Perfil de un Juez

```
Juez: Dr. Juan Pérez
Sentencias analizadas: 12
Confianza: 0.70

Activismo: +0.35 (activista moderado)
Interpretación: teleológica (busca la finalidad de la norma)
Formalismo: +0.28 (ligeramente sustancialista)
Protección de derechos: 0.75 (alta protección)
Deferencia legislativo: 0.15 (baja, revisa activamente)
Deferencia ejecutivo: 0.10 (baja)

Derechos más protegidos:
  - Trabajo: 0.87
  - Igualdad: 0.68
  - Debido proceso: 0.54

Tests más aplicados:
  - Test de razonabilidad: 0.72
  - In dubio pro operario: 0.65

Estándar probatorio: sana_critica
Sesgo dominante: pro_trabajador

Temas recurrentes: despido, discriminación laboral, accidentes de trabajo
```

**Interpretación**:
Este juez es activista moderado con enfoque en protección de derechos laborales. Tiende a interpretar las normas buscando su finalidad (teleológico) y prioriza el fondo sobre la forma (sustancialista). Muestra baja deferencia hacia el legislativo y ejecutivo, indicando que no duda en revisar actos de otros poderes cuando afectan derechos. Claramente especializado en derecho laboral con sesgo pro-trabajador, aplica frecuentemente el principio in dubio pro operario.

## ✅ Checklist de Fase 2

- [x] Analizador de pensamiento judicial implementado
- [x] Detección de activismo judicial
- [x] Análisis de interpretación normativa
- [x] Análisis de protección de derechos
- [x] Detección de tests y doctrinas argentinas
- [x] Análisis de estándares probatorios
- [x] Detección de fuentes citadas
- [x] Detección de sesgos argentinos
- [x] Procesador completo integrado
- [x] Agregador de perfiles implementado
- [x] Cálculo de confianza del perfil
- [x] Identificación de temas recurrentes
- [x] Documentación completa

## 🎉 ¡Fase 2 Completada!

El sistema ahora puede:
- ✅ Ingestar sentencias
- ✅ Analizar sentencias (cognitivo + judicial)
- ✅ Agregar perfiles de jueces
- ✅ Almacenar métricas consolidadas
- ✅ Calcular confianza de perfiles

**Próximo (Fase 3)**: Líneas jurisprudenciales y redes de influencia

---

**Versión**: 1.0
**Fecha**: 2025-11-12
**Autor**: Sistema de Análisis de Pensamiento Judicial Argentina
