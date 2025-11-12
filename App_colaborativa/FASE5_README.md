# Fase 5: Sistema de Informes y Preguntas

## 🎯 Implementación Completada

La Fase 5 completa el sistema con capacidades de generación de informes y respuestas automáticas:

✅ Generador de informes judiciales (TXT/JSON/MD)
✅ Sistema de 140+ preguntas predeterminadas en 8 categorías
✅ Motor de respuestas automáticas
✅ 4 tipos de informes especializados
✅ Integración completa de todas las fases
✅ API programática

## 📁 Archivos Creados

### 1. Generador de Informes
**Archivo**: `generador_informes_judicial.py` (800+ líneas)

**Funcionalidades**:
- Genera informes completos del juez (35-55 páginas equiv.)
- Genera informes de línea jurisprudencial (15-25 páginas)
- Genera informes de red de influencias (10-15 páginas)
- Genera informes predictivos para litigación (10-15 páginas)
- Soporta formatos: TXT, JSON, Markdown
- Consulta toda la información de las 4 fases anteriores

**Secciones del informe completo**:
1. Información básica
2. Perfil judicial
3. Protección de derechos
4. Tests y doctrinas aplicados
5. Sesgos y tendencias
6. Líneas jurisprudenciales
7. Red de influencias
8. Análisis predictivo
9. Sentencias analizadas

### 2. Sistema de Preguntas
**Archivo**: `sistema_preguntas_judiciales.py` (900+ líneas)

**Funcionalidades**:
- Catálogo de 140 preguntas predeterminadas
- 8 categorías temáticas (A-H)
- Metadata completa por pregunta
- Búsqueda y filtrado
- Exportación a JSON

**Categorías** (140 preguntas total):
- **A. Perfil e Identidad Judicial** (20 preguntas)
- **B. Metodología Interpretativa** (20 preguntas)
- **C. Protección de Derechos** (20 preguntas)
- **D. Líneas Jurisprudenciales** (20 preguntas)
- **E. Red de Influencias** (15 preguntas)
- **F. Análisis Predictivo** (15 preguntas)
- **G. Sesgos y Tendencias** (15 preguntas)
- **H. Casos Específicos** (15 preguntas)

### 3. Motor de Respuestas
**Archivo**: `motor_respuestas_judiciales.py` (700+ líneas)

**Funcionalidades**:
- Responde automáticamente las 140 preguntas
- Consulta BD y modelos predictivos
- Interpreta scores y genera respuestas en lenguaje natural
- Soporta respuestas especializadas por pregunta
- Genera informes de preguntas (TXT/JSON)

## 🚀 Uso del Sistema

### Paso 1: Generar Informe Completo

```bash
cd App_colaborativa/colaborative/scripts

# Informe en formato texto
python generador_informes_judicial.py "Dr. Juan Pérez"

# Informe en JSON
python generador_informes_judicial.py "Dr. Juan Pérez" --formato json

# Informe en Markdown
python generador_informes_judicial.py "Dr. Juan Pérez" --formato md
```

**Salida esperada**:
```
GENERANDO INFORME COMPLETO: Dr. Juan Pérez

ℹ Recopilando datos...
✓ Datos obtenidos: 15 sentencias, 3 líneas
✓ Informe guardado: /path/to/informe_completo_Dr._Juan_Pérez_20251112_143022.txt
```

**Estructura del informe TXT**:
```
================================================================================
                     INFORME COMPLETO DEL JUEZ: Dr. Juan Pérez
================================================================================
Fecha: 12/11/2025 14:30
Sistema: Análisis de Pensamiento Judicial Argentina v1.0
================================================================================

1. INFORMACIÓN BÁSICA
--------------------------------------------------------------------------------
Nombre: Dr. Juan Pérez
Tipo: individual
Fuero: laboral
Jurisdicción: federal
Tribunal: Cámara Nacional del Trabajo
Sentencias analizadas: 15
Confianza del análisis: 0.75

2. PERFIL JUDICIAL
--------------------------------------------------------------------------------

2.1 ACTIVISMO JUDICIAL: 0.45
Juez moderadamente activista. Ocasionalmente ejerce control de constitucionalidad
y expansión de derechos.

2.2 FORMALISMO: 0.32
Formalismo moderado. Balance entre forma y sustancia.

2.3 INTERPRETACIÓN DOMINANTE: teleologica
Interpretación orientada a los fines y objetivos de la norma.

[... continúa con 9 secciones ...]
```

### Paso 2: Generar Informes Especializados

```bash
# Informe de línea jurisprudencial
python generador_informes_judicial.py "Dr. Juan Pérez" \
  --tipo linea --tema despido

# Informe de red de influencias
python generador_informes_judicial.py "Dr. Juan Pérez" \
  --tipo red

# Informe predictivo (requiere API)
# (se usa programáticamente con datos del caso nuevo)
```

### Paso 3: Explorar Sistema de Preguntas

```bash
# Ver resumen del sistema
python sistema_preguntas_judiciales.py

# Listar todas las preguntas
python sistema_preguntas_judiciales.py --listar

# Ver preguntas de una categoría
python sistema_preguntas_judiciales.py --categoria A

# Buscar preguntas por término
python sistema_preguntas_judiciales.py --buscar "activismo"

# Exportar a JSON
python sistema_preguntas_judiciales.py --exportar preguntas.json
```

**Salida esperada (resumen)**:
```
================================================================================
SISTEMA DE PREGUNTAS JUDICIALES v1.0
================================================================================

Total de preguntas: 140

Categorías:
  A. Perfil e Identidad Judicial (20 preguntas)
  B. Metodología Interpretativa (20 preguntas)
  C. Protección de Derechos (20 preguntas)
  D. Líneas Jurisprudenciales (20 preguntas)
  E. Red de Influencias (15 preguntas)
  F. Análisis Predictivo (15 preguntas)
  G. Sesgos y Tendencias (15 preguntas)
  H. Casos Específicos (15 preguntas)
```

**Ejemplo de preguntas (Categoría A)**:
```
A01. ¿Cuál es el perfil judicial general de este juez?
    Tipo: texto
    Campos BD: tendencia_activismo, nivel_formalismo, interpretacion_dominante...

A02. ¿Es un juez activista o restrictivo?
    Tipo: score
    Campos BD: tendencia_activismo

A03. ¿Cuál es su nivel de formalismo?
    Tipo: score
    Campos BD: nivel_formalismo

[... 17 preguntas más ...]
```

### Paso 4: Responder Preguntas Automáticamente

```bash
# Responder una pregunta específica
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --pregunta A02

# Responder toda una categoría
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --categoria A

# Responder las 140 preguntas y generar informe
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --todas

# Generar informe en JSON
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --todas --formato json
```

**Salida esperada (pregunta específica)**:
```
¿Es un juez activista o restrictivo?
R: 0.45 (moderadamente activista)
```

**Salida esperada (todas las preguntas)**:
```
RESPONDIENDO 140+ PREGUNTAS: Dr. Juan Pérez

ℹ Procesando categoría A...
ℹ Procesando categoría B...
ℹ Procesando categoría C...
ℹ Procesando categoría D...
ℹ Procesando categoría E...
ℹ Procesando categoría F...
ℹ Procesando categoría G...
ℹ Procesando categoría H...
✓ Completado: 132/140 respuestas disponibles
✓ Informe guardado: preguntas_Dr._Juan_Pérez_20251112_143500.txt
```

**Estructura del informe de preguntas**:
```
================================================================================
                      INFORME DE PREGUNTAS: Dr. Juan Pérez
================================================================================
Fecha: 12/11/2025 14:35
Total preguntas: 140
Respuestas disponibles: 132
================================================================================

A. PERFIL E IDENTIDAD JUDICIAL
--------------------------------------------------------------------------------

A01. ¿Cuál es el perfil judicial general de este juez?
R: Juez de fuero laboral con perfil moderadamente activista, formalismo
moderado, y método interpretativo dominante teleologica. Analizado con base
en 15 sentencias (confianza: 0.75).

A02. ¿Es un juez activista o restrictivo?
R: 0.45 (moderadamente activista)

A03. ¿Cuál es su nivel de formalismo?
R: 0.32 (formalismo moderado)

[... 137 respuestas más ...]
```

## 📊 Ejemplos de Respuestas

### Categoría A: Perfil e Identidad

**A01. ¿Cuál es el perfil judicial general de este juez?**
```
Juez de fuero laboral con perfil moderadamente activista, formalismo moderado,
y método interpretativo dominante teleologica. Analizado con base en 15
sentencias (confianza: 0.75).
```

**A20. ¿Cuál es su perfil completo en una síntesis?**
```
SÍNTESIS: Juez de laboral, moderadamente activista, formalismo moderado.
Interpretación teleologica. Protección laboral: 0.87. Perfil garantista.
Base: 15 sentencias.
```

### Categoría C: Protección de Derechos

**C09. ¿Qué derechos protege con mayor intensidad?**
```
Trabajo (0.87), Igualdad (0.72), Consumidor (0.68)
```

**C10. ¿Qué derechos protege con menor intensidad?**
```
Propiedad (0.34), Libertad Expresión (0.41), Privacidad (0.45)
```

### Categoría D: Líneas Jurisprudenciales

**D01. ¿Cuáles son las principales líneas jurisprudenciales del juez?**
```
despido (8 sentencias, consistencia 0.85); discriminación laboral (5 sentencias,
consistencia 0.92); daños y perjuicios (4 sentencias, consistencia 0.70)
```

**D08. ¿Cuál es su criterio dominante en casos de despido?**
```
Tiende a hacer lugar los reclamos, usando interpretación teleológica. Aplica
frecuentemente: test de razonabilidad, in dubio pro operario.
```

### Categoría E: Red de Influencias

**E01. ¿Qué tribunales superiores cita más frecuentemente?**
```
CSJN (12 citas), Cámara Nacional del Trabajo - Sala VII (8 citas), CNTrab
Sala X (5 citas)
```

**E03. ¿Qué autores doctrinales cita más frecuentemente?**
```
Grisolía (8 citas), Ackerman (5 citas), Bidart Campos (3 citas), Nino (3 citas),
Vázquez Vialard (2 citas)
```

### Categoría F: Análisis Predictivo

**F03. ¿Cuáles son los factores más determinantes en sus decisiones?**
```
in_dubio_pro_operario (peso: 0.245); proteccion_trabajo (peso: 0.189);
materia_despido (peso: 0.156); test_razonabilidad (peso: 0.132);
tipo_demandado_empresa (peso: 0.098)
```

**F13. ¿Es un juez predecible o impredecible según el modelo?**
```
Juez predecible. Accuracy del modelo: 87.50%. Líneas consolidadas en despido
y discriminación laboral con alta consistencia.
```

### Categoría G: Sesgos y Tendencias

**G06. ¿Cuál es su sesgo dominante?**
```
Pro-Trabajador (0.73)
```

**G14. ¿Todos sus sesgos en una síntesis?**
```
Fuerte sesgo pro-trabajador (0.73), garantista moderado (0.61), pro-consumidor
moderado (0.58). Sesgo pro-empresa bajo (0.12). Neutral en punitivismo.
```

### Categoría H: Casos Específicos

**H01. ¿Cómo resolvería un despido discriminatorio con prueba indiciaria?**
```
Basándose en su línea consolidada en discriminación (consistencia 0.92),
probablemente haría lugar aplicando escrutinio estricto y test de razonabilidad.
Su alto sesgo pro-trabajador (0.73) y frecuente uso de in dubio pro operario
refuerzan esta predicción. Precedentes: SENT_002, SENT_005 (casos paradigmáticos).
```

## 🔍 Tipos de Preguntas

### Por Tipo de Respuesta

1. **Score (0-1)**: Preguntas que devuelven métricas numéricas interpretadas
   - Ejemplo: "¿Cuál es su nivel de formalismo?" → "0.32 (formalismo moderado)"

2. **Número**: Preguntas que devuelven cantidades
   - Ejemplo: "¿Cuántas sentencias se han analizado?" → "15"

3. **Texto**: Preguntas que devuelven descripciones
   - Ejemplo: "¿En qué fuero se desempeña?" → "laboral"

4. **Lista**: Preguntas que devuelven enumeraciones
   - Ejemplo: "¿Qué derechos protege con mayor intensidad?" → "Trabajo, Igualdad, Consumidor"

5. **Boolean**: Preguntas sí/no
   - Ejemplo: "¿Hay modelo predictivo disponible?" → "SÍ"

### Por Fuente de Datos

- **Perfil judicial**: Consulta tabla `perfiles_judiciales_argentinos`
- **Líneas**: Consulta tabla `lineas_jurisprudenciales`
- **Red**: Consulta tabla `redes_influencia_judicial`
- **Predictivo**: Consulta tabla `factores_predictivos` y modelos .pkl
- **Sentencias**: Consulta tabla `sentencias_por_juez_arg`

## ⚙️ Uso Programático

### Python API - Generar Informes

```python
from generador_informes_judicial import GeneradorInformesJudicial

# Inicializar
generador = GeneradorInformesJudicial()

# Generar informe completo
ruta = generador.generar_informe_completo("Dr. Juan Pérez", formato='txt')
print(f"Informe generado: {ruta}")

# Generar informe de línea
ruta_linea = generador.generar_informe_linea("Dr. Juan Pérez", "despido")

# Generar informe de red
ruta_red = generador.generar_informe_red("Dr. Juan Pérez")

# Cerrar
generador.cerrar_bd()
```

### Python API - Sistema de Preguntas

```python
from sistema_preguntas_judiciales import SistemaPreguntasJudiciales

# Inicializar
sistema = SistemaPreguntasJudiciales()

# Obtener todas las preguntas
todas = sistema.obtener_todas_preguntas()
print(f"Total: {len(todas)} preguntas")

# Obtener preguntas de una categoría
preguntas_a = sistema.obtener_preguntas_por_categoria('A')

# Buscar preguntas
resultados = sistema.buscar_preguntas("activismo")

# Exportar a JSON
sistema.exportar_json("preguntas_export.json")
```

### Python API - Motor de Respuestas

```python
from motor_respuestas_judiciales import MotorRespuestasJudiciales

# Inicializar
motor = MotorRespuestasJudiciales()

# Responder pregunta específica
respuesta = motor.responder_pregunta("Dr. Juan Pérez", "A02")
print(f"{respuesta['pregunta']}")
print(f"R: {respuesta['respuesta']}")

# Responder categoría completa
respuestas_a = motor.responder_categoria("Dr. Juan Pérez", 'A')

# Responder todas las 140 preguntas
todas_respuestas = motor.responder_todas("Dr. Juan Pérez")
print(f"Respondidas: {todas_respuestas['respuestas_disponibles']}/{todas_respuestas['total_preguntas']}")

# Generar informe
archivo = motor.generar_informe_preguntas("Dr. Juan Pérez", formato='json')

# Cerrar
motor.cerrar_bd()
```

## 🔗 Integración con Fases Anteriores

### Pipeline Completo

```bash
# FASE 1: Crear BD e ingestar sentencias
python inicializar_bd_judicial.py
python ingesta_sentencias_judicial.py /ruta/sentencias/

# FASE 2: Analizar pensamiento judicial
python procesador_sentencias_completo.py --todos

# FASE 3: Construir líneas y redes
python analizador_lineas_jurisprudenciales.py --todos
python analizador_redes_influencia.py --todos

# FASE 4: Entrenar modelos predictivos
python motor_predictivo_judicial.py --todos

# FASE 5: Generar informes completos
python generador_informes_judicial.py "Dr. Juan Pérez"
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --todas
```

### Datos Utilizados por Fase 5

**De Fase 1**:
- Información básica (fuero, jurisdicción, tribunal)
- Sentencias completas
- Metadata (expediente, carátula, fecha, partes)

**De Fase 2**:
- Perfil judicial completo (80+ campos)
- Activismo, formalismo, interpretación
- Protección de derechos (6 dimensiones)
- Tests y doctrinas aplicados
- Sesgos argentinos (5 tipos)

**De Fase 3**:
- Líneas jurisprudenciales consolidadas
- Consistencia por tema
- Casos paradigmáticos
- Red de influencias (CSJN, tribunales, autores)
- Intensidad de citas

**De Fase 4**:
- Modelos predictivos por juez
- Feature importance (factores determinantes)
- Accuracy del modelo
- Factores guardados en BD

## 📋 Casos de Uso

### 1. Litigante: Preparación de caso

**Objetivo**: Entender al juez antes de presentar demanda

**Flujo**:
```bash
# Paso 1: Generar informe completo
python generador_informes_judicial.py "Dr. Juan Pérez"

# Paso 2: Responder preguntas clave
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --pregunta F03  # Factores determinantes
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --pregunta D08  # Criterio en despidos
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --pregunta G01  # Sesgo pro-trabajador

# Paso 3: Revisar líneas y casos similares
python motor_respuestas_judiciales.py "Dr. Juan Pérez" --categoria D
```

**Resultado**: Informe detallado + respuestas específicas para estrategia

### 2. Investigador: Análisis académico

**Objetivo**: Estudiar patrones judiciales en fuero laboral

**Flujo**:
```bash
# Generar informes JSON de múltiples jueces
python generador_informes_judicial.py "Dr. Pérez" --formato json
python generador_informes_judicial.py "Dra. González" --formato json
python generador_informes_judicial.py "Dr. Rodríguez" --formato json

# Responder preguntas comparativas
python motor_respuestas_judiciales.py "Dr. Pérez" --todas --formato json
python motor_respuestas_judiciales.py "Dra. González" --todas --formato json

# Análisis con scripts personalizados sobre JSON
```

**Resultado**: Datos estructurados para análisis estadístico comparativo

### 3. Abogado: Consulta rápida

**Objetivo**: Consulta específica sobre metodología del juez

**Flujo**:
```bash
# Preguntas específicas
python motor_respuestas_judiciales.py "Dr. Pérez" --pregunta B06  # ¿Aplica test proporcionalidad?
python motor_respuestas_judiciales.py "Dr. Pérez" --pregunta B08  # ¿Usa in dubio pro operario?

# O categoría metodológica completa
python motor_respuestas_judiciales.py "Dr. Pérez" --categoria B
```

**Resultado**: Respuestas inmediatas sin leer informe completo

### 4. Estudio jurídico: Base de conocimiento

**Objetivo**: Construir base de conocimiento interna

**Flujo**:
```bash
# Generar informes completos de todos los jueces relevantes
for juez in $(cat lista_jueces.txt); do
    python generador_informes_judicial.py "$juez" --formato json
    python motor_respuestas_judiciales.py "$juez" --todas --formato json
done

# Integrar JSON a sistema de gestión
```

**Resultado**: Base de datos estructurada con perfiles completos

## 🔍 Consultas SQL Útiles

### Ver Jueces con Informes Disponibles

```sql
SELECT
    juez,
    total_sentencias,
    confianza_analisis,
    fuero,
    jurisdiccion
FROM perfiles_judiciales_argentinos
WHERE total_sentencias >= 5
ORDER BY total_sentencias DESC;
```

### Jueces más Predecibles

```sql
SELECT
    juez,
    COUNT(*) as n_factores,
    MAX(peso) as max_factor_peso
FROM factores_predictivos
GROUP BY juez
HAVING COUNT(*) >= 10
ORDER BY max_factor_peso DESC;
```

### Jueces con Líneas Consolidadas

```sql
SELECT
    juez,
    COUNT(*) as n_lineas,
    AVG(consistencia_score) as consistencia_promedio,
    SUM(cantidad_sentencias) as total_sent_en_lineas
FROM lineas_jurisprudenciales
WHERE consistencia_score >= 0.70
GROUP BY juez
ORDER BY consistencia_promedio DESC;
```

## 📊 Estadísticas del Sistema

### Componentes Implementados

- **Scripts Python**: 3 archivos (2400+ líneas)
- **Preguntas predeterminadas**: 140
- **Categorías**: 8
- **Tipos de respuesta**: 5
- **Formatos de salida**: 3 (TXT, JSON, MD)
- **Tipos de informe**: 4
- **Secciones en informe completo**: 9

### Cobertura de Análisis

- **Campos de BD consultados**: 80+
- **Tablas utilizadas**: 5
- **Respuestas especializadas**: 10+
- **Integraciones con fases**: 4 (Fases 1-4)

## 🐛 Troubleshooting

### Error: "BD no encontrada"

**Causa**: Base de datos no inicializada

**Solución**:
```bash
cd App_colaborativa/colaborative/scripts
python inicializar_bd_judicial.py
```

### Warning: "Respuestas no disponibles"

**Causa**: Juez no tiene suficientes sentencias analizadas

**Solución**:
1. Verificar que el juez existe: `sqlite3 juez_centrico_arg.db "SELECT * FROM perfiles_judiciales_argentinos WHERE juez='...'"`
2. Si no existe, procesar sentencias (Fases 1-2)
3. Si existe pero faltan datos, completar Fases 3-4

### Error: "Modelo predictivo no disponible"

**Causa**: Modelo no entrenado para ese juez

**Solución**:
```bash
# Entrenar modelo para el juez específico
python motor_predictivo_judicial.py "Dr. Juan Pérez"

# O entrenar para todos
python motor_predictivo_judicial.py --todos
```

### Informes vacíos o incompletos

**Causa**: Fases anteriores no completadas

**Solución**: Ejecutar pipeline completo (Fases 1-4) antes de generar informes

## ✅ Checklist de Fase 5

- [x] Generador de informes implementado
- [x] 4 tipos de informes (completo, línea, red, predictivo)
- [x] Formatos múltiples (TXT, JSON, MD)
- [x] Sistema de 140 preguntas implementado
- [x] 8 categorías definidas
- [x] Motor de respuestas implementado
- [x] Respuestas especializadas
- [x] Interpretación de scores
- [x] Integración con 4 fases anteriores
- [x] API programática
- [x] Exportación a JSON
- [x] Documentación completa

## 🎉 ¡Fase 5 Completada - Sistema Completo!

El sistema completo ahora puede:

### Fase 1: Fundamentos
- ✅ Crear base de datos especializada
- ✅ Ingestar sentencias (PDF/TXT)
- ✅ Extraer metadata argentina (30+ patrones)
- ✅ Crear perfiles básicos

### Fase 2: Análisis Judicial
- ✅ Analizar pensamiento judicial (100+ patrones)
- ✅ Detectar activismo, formalismo, interpretación
- ✅ Medir protección de derechos (6 dimensiones)
- ✅ Identificar tests, doctrinas, sesgos

### Fase 3: Líneas y Redes
- ✅ Consolidar líneas jurisprudenciales
- ✅ Calcular consistencia por tema
- ✅ Identificar casos paradigmáticos
- ✅ Construir redes de influencia
- ✅ Extraer citas (CSJN, tribunales, autores)

### Fase 4: Predictivo
- ✅ Entrenar modelos de Machine Learning
- ✅ Extraer 15+ factores relevantes
- ✅ Predecir decisiones con probabilidades
- ✅ Calcular feature importance
- ✅ Guardar modelos persistentes

### Fase 5: Informes y Preguntas
- ✅ Generar informes completos (35-55 pág equiv.)
- ✅ Responder 140+ preguntas automáticamente
- ✅ Soportar múltiples formatos (TXT/JSON/MD)
- ✅ Integrar todas las fases
- ✅ Proveer API programática

## 📊 Sistema Final - Capacidades Completas

**Total de archivos implementados**: 19
- Scripts Python: 15 (9000+ líneas)
- Esquema SQL: 1 (500+ líneas)
- Documentación: 5 (300+ páginas equiv.)

**Cobertura completa**:
- ✅ Ingesta y procesamiento
- ✅ Análisis cognitivo judicial
- ✅ Líneas jurisprudenciales
- ✅ Redes de influencia
- ✅ Predicción con ML
- ✅ Generación de informes
- ✅ Sistema de preguntas

**Listo para producción** 🚀

---

**Versión**: 1.0
**Fecha**: 2025-11-12
**Autor**: Sistema de Análisis de Pensamiento Judicial Argentina
