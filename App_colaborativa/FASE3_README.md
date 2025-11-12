# Fase 3: Líneas Jurisprudenciales y Redes de Influencia

## 🎯 Implementación Completada

La Fase 3 añade análisis de consistencia y redes de influencia:

✅ Analizador de líneas jurisprudenciales
✅ Extractor de citas jurisprudenciales y doctrinales
✅ Analizador de redes de influencia judicial
✅ Identificación de casos paradigmáticos
✅ Cálculo de consistencia por tema
✅ Detección de excepciones al criterio

## 📁 Archivos Creados

### 1. Analizador de Líneas Jurisprudenciales
**Archivo**: `analizador_lineas_jurisprudenciales.py`

**Funcionalidades**:
- Agrupa sentencias por tema/materia
- Identifica criterio dominante
- Calcula consistencia (0-1)
- Identifica casos paradigmáticos
- Detecta excepciones
- Extrae factores predictivos
- Guarda en tabla `lineas_jurisprudenciales`

**Uso**:
```bash
# Analizar un juez
python analizador_lineas_jurisprudenciales.py "Dr. Juan Pérez"

# Analizar todos los jueces
python analizador_lineas_jurisprudenciales.py --todos

# Con mínimo de sentencias personalizado
python analizador_lineas_jurisprudenciales.py "Dr. Juan Pérez" --min-sentencias 3
```

**Salida esperada**:
```
======================================================================
ANÁLISIS DE LÍNEAS JURISPRUDENCIALES: Dr. Juan Pérez
======================================================================

ℹ Obteniendo sentencias...
✓ Sentencias encontradas: 15
ℹ Agrupando por tema...
✓ Temas identificados: 4
ℹ Analizando línea: despido (8 sentencias)
✓   Consistencia: 0.85, Casos paradigmáticos: 3
ℹ Analizando línea: daños (4 sentencias)
✓   Consistencia: 0.75, Casos paradigmáticos: 2
⚠   Tema 'divorcio' tiene solo 1 sentencia(s), omitiendo

======================================================================
RESUMEN
======================================================================
Total sentencias: 15
Temas identificados: 4
Líneas analizadas: 3
Líneas guardadas: 3
```

### 2. Extractor de Citas Jurisprudenciales
**Archivo**: `extractor_citas_jurisprudenciales.py`

**Detecta**:
- Citas a CSJN (Fallos: 331:2499)
- Citas a Cámaras y Salas
- Citas a autores doctrinales
- Extracto textual de cada cita

**Patrones reconocidos**:
```
CSJN:
- "Fallos: 331:2499"
- "CSJN, Fallos: 331:2499"
- "Corte Suprema, autos 'Vizzoti...'"

Cámaras:
- "Cámara Nacional del Trabajo, Sala VII"
- "CNTrab, Sala X"
- "Sala II, autos '...'"

Doctrina:
- "Como sostiene Grisolía"
- "Bidart Campos enseña que"
- "La doctrina de Ackerman"
```

**Uso como módulo**:
```python
from extractor_citas_jurisprudenciales import ExtractorCitasJurisprudenciales

extractor = ExtractorCitasJurisprudenciales()
citas = extractor.extraer_todas_citas(texto_sentencia)

# Ver resumen
extractor.imprimir_resumen(citas)

# Exportar a JSON
json_output = extractor.exportar_json(citas)
```

### 3. Analizador de Redes de Influencia
**Archivo**: `analizador_redes_influencia.py`

**Funcionalidades**:
- Extrae citas de todas las sentencias de un juez
- Cuenta frecuencias de citas
- Calcula intensidad de influencia (0-1)
- Guarda en tabla `redes_influencia_judicial`
- Identifica jueces/tribunales más citados
- Identifica autores doctrinales más citados

**Uso**:
```bash
# Analizar un juez
python analizador_redes_influencia.py "Dr. Juan Pérez"

# Analizar todos los jueces
python analizador_redes_influencia.py --todos
```

**Salida esperada**:
```
======================================================================
ANÁLISIS DE REDES DE INFLUENCIA - TODOS LOS JUECES
======================================================================

ℹ Jueces a analizar: 5

Analizando red de: Dr. Juan Pérez
ℹ Extrayendo citas de Dr. Juan Pérez...
✓   Citas encontradas: 12 CSJN, 8 Cámaras, 15 doctrinales
✓   Relaciones guardadas: 23

[... más jueces ...]

======================================================================
RESUMEN
======================================================================
Jueces analizados: 5
Total relaciones: 87
```

## 🚀 Flujo de Trabajo Fase 3

```bash
cd App_colaborativa/colaborative/scripts

# Después de tener sentencias analizadas (Fase 2)...

# PASO 1: Analizar líneas jurisprudenciales
python analizador_lineas_jurisprudenciales.py --todos

# PASO 2: Construir redes de influencia
python analizador_redes_influencia.py --todos

# ¡LISTO! Ahora tienes:
# - Líneas jurisprudenciales consolidadas
# - Redes de influencia completas
```

## 📊 Qué se Guarda en la BD

### Tabla: `lineas_jurisprudenciales`

```sql
SELECT
  juez,
  tema,
  cantidad_sentencias,
  consistencia_score,
  criterio_dominante,
  casos_tipo  -- JSON con IDs de casos paradigmáticos
FROM lineas_jurisprudenciales
WHERE juez = 'Dr. Juan Pérez';
```

**Ejemplo de registro**:
```
juez: Dr. Juan Pérez
tema: despido
cantidad_sentencias: 8
consistencia_score: 0.85
criterio_dominante: "Tiende a hace_lugar los reclamos, usando interpretación teleologica. Aplica frecuentemente: test_razonabilidad, in_dubio_pro_operario"
casos_tipo: ["SENT_12345", "SENT_12347", "SENT_12350"]
```

### Tabla: `redes_influencia_judicial`

```sql
SELECT
  juez_origen,
  juez_destino,
  tipo_destino,
  tipo_influencia,
  intensidad,
  cantidad_citas
FROM redes_influencia_judicial
WHERE juez_origen = 'Dr. Juan Pérez'
ORDER BY cantidad_citas DESC;
```

**Ejemplo de registros**:
```
juez_origen: Dr. Juan Pérez
juez_destino: CSJN
tipo_destino: csjn
tipo_influencia: cita_literal
intensidad: 0.8
cantidad_citas: 12

juez_origen: Dr. Juan Pérez
juez_destino: Grisolía
tipo_destino: autor_doctrinal
tipo_influencia: cita_literal
intensidad: 0.6
cantidad_citas: 8
```

## 🔍 Consultas Útiles

### Ver Líneas Consolidadas de un Juez

```sql
SELECT
  tema,
  cantidad_sentencias,
  ROUND(consistencia_score, 2) as consistencia,
  criterio_dominante
FROM lineas_jurisprudenciales
WHERE juez = 'Dr. Juan Pérez'
  AND consistencia_score >= 0.7
ORDER BY cantidad_sentencias DESC;
```

### Ver Jueces que más Citan a la CSJN

```sql
SELECT
  juez_origen,
  cantidad_citas,
  ROUND(intensidad, 2) as intensidad
FROM redes_influencia_judicial
WHERE tipo_destino = 'csjn'
ORDER BY cantidad_citas DESC
LIMIT 10;
```

### Ver Autores Más Citados

```sql
SELECT
  juez_destino as autor,
  SUM(cantidad_citas) as total_citas,
  COUNT(DISTINCT juez_origen) as citado_por_n_jueces
FROM redes_influencia_judicial
WHERE tipo_destino = 'autor_doctrinal'
GROUP BY juez_destino
ORDER BY total_citas DESC
LIMIT 10;
```

### Ver Red de un Juez Específico

```sql
SELECT
  juez_destino,
  tipo_destino,
  cantidad_citas,
  ROUND(intensidad, 2) as intensidad
FROM redes_influencia_judicial
WHERE juez_origen = 'Dr. Juan Pérez'
ORDER BY cantidad_citas DESC;
```

## 📈 Métricas Calculadas

### Consistencia de Línea (0-1)
- **0.9-1.0**: Muy consistente (casi siempre mismo criterio)
- **0.7-0.9**: Consistente (criterio claro con pocas excepciones)
- **0.5-0.7**: Moderadamente consistente
- **< 0.5**: Inconsistente (criterio variable)

### Intensidad de Influencia (0-1)
- **0.8-1.0**: Influencia muy fuerte (cita frecuente)
- **0.5-0.8**: Influencia fuerte
- **0.3-0.5**: Influencia moderada
- **< 0.3**: Influencia débil

### Confianza de Línea (0-1)
Basada en cantidad de sentencias:
- **10+ sentencias**: 1.0 (muy confiable)
- **5-9 sentencias**: 0.5-0.9
- **2-4 sentencias**: 0.2-0.5

## 📊 Ejemplo de Análisis Completo

### Juez: Dr. Juan Pérez

**Líneas Jurisprudenciales (3 líneas consolidadas)**:

1. **Despido** (8 sentencias, consistencia 0.85)
   - Criterio: Hace lugar interpretando teleológicamente, aplica in dubio pro operario
   - Casos paradigmáticos: SENT_001, SENT_003, SENT_007
   - Excepciones: 1 caso donde rechazó por falta de prueba

2. **Discriminación laboral** (5 sentencias, consistencia 0.92)
   - Criterio: Hace lugar aplicando test de razonabilidad estricto
   - Casos paradigmáticos: SENT_002, SENT_005
   - Excepciones: Ninguna

3. **Daños** (4 sentencias, consistencia 0.70)
   - Criterio: Variable según monto y prueba
   - Casos paradigmáticos: SENT_008
   - Excepciones: 1 caso

**Red de Influencias**:

Citas a tribunales:
- CSJN: 12 citas (intensidad 0.8)
- CNTrab Sala VII: 8 citas (intensidad 0.6)

Citas a doctrina:
- Grisolía: 8 citas (intensidad 0.6)
- Ackerman: 5 citas (intensidad 0.4)
- Bidart Campos: 3 citas (intensidad 0.3)

## ✅ Checklist de Fase 3

- [x] Analizador de líneas implementado
- [x] Agrupación por tema
- [x] Cálculo de consistencia
- [x] Identificación de casos paradigmáticos
- [x] Detección de excepciones
- [x] Extractor de citas implementado
- [x] Patrones para CSJN, Cámaras, doctrina
- [x] Analizador de redes implementado
- [x] Construcción de relaciones
- [x] Cálculo de intensidad
- [x] Guardado en BD
- [x] Documentación completa

## 🎉 ¡Fase 3 Completada!

El sistema ahora puede:
- ✅ Identificar líneas jurisprudenciales consistentes
- ✅ Calcular consistencia por tema
- ✅ Encontrar casos paradigmáticos
- ✅ Extraer citas jurisprudenciales y doctrinales
- ✅ Construir redes de influencia
- ✅ Identificar jueces/autores más influyentes

**Próximo (Fase 4)**: Análisis predictivo con Machine Learning

---

**Versión**: 1.0
**Fecha**: 2025-11-12
**Autor**: Sistema de Análisis de Pensamiento Judicial Argentina
