# Fase 4: Análisis Predictivo con Machine Learning

## 🎯 Implementación Completada

La Fase 4 añade capacidades predictivas usando Machine Learning:

✅ Extractor de factores relevantes de casos
✅ Motor predictivo con Random Forest
✅ Entrenamiento de modelos por juez
✅ Predicción de decisiones con probabilidades
✅ Análisis de feature importance
✅ Guardado de factores en BD
✅ Modelos persistentes en disco

## 📁 Archivo Creado

### Motor Predictivo Judicial
**Archivo**: `motor_predictivo_judicial.py` (600+ líneas)

**Componentes**:
1. **ExtractorFactores**: Extrae características relevantes
2. **MotorPredictivoJudicial**: Entrena y predice con ML
3. **Random Forest Classifier**: Modelo principal
4. **Feature Importance**: Identifica factores clave

## 🔍 Factores Extraídos

El sistema extrae automáticamente **15+ factores** de cada caso:

### Factores Básicos
- **Materia**: despido, daños, divorcio, etc.
- **Tipo de actor**: empresa, persona, estado
- **Tipo de demandado**: empresa, persona, estado

### Factores Judiciales (del análisis)
- **Test proporcionalidad**: aplicado (1) o no (0)
- **Test razonabilidad**: aplicado (1) o no (0)
- **In dubio pro operario**: aplicado (1) o no (0)
- **In dubio pro consumidor**: aplicado (1) o no (0)

### Factores de Protección
- **Protección trabajo**: score 0-1
- **Protección igualdad**: score 0-1

### Factores Metodológicos
- **Estándar prueba**: sana_critica, prueba_tasada, etc.
- **Interpretación**: literal, sistemática, teleológica, mixta

### Factores Textuales
- **Longitud texto**: cantidad de palabras (proxy de complejidad)
- **Menciona monto**: sí (1) o no (0)

## 🚀 Uso del Sistema

### Prerrequisito: Instalar scikit-learn

```bash
pip install scikit-learn numpy
```

### Paso 1: Entrenar Modelos

```bash
cd App_colaborativa/colaborative/scripts

# Entrenar modelo para un juez específico
python motor_predictivo_judicial.py "Dr. Juan Pérez"

# Entrenar modelos para TODOS los jueces
python motor_predictivo_judicial.py --todos

# Con mínimo personalizado de sentencias
python motor_predictivo_judicial.py --todos --min-sentencias 10
```

**Salida esperada**:
```
======================================================================
ENTRENAMIENTO DE MODELOS PREDICTIVOS - TODOS LOS JUECES
======================================================================

ℹ Jueces candidatos: 5

Entrenando modelo para: Dr. Juan Pérez
✓   Sentencias disponibles: 15
ℹ   Features: 18, Clases: {'hace_lugar', 'rechaza', 'hace_lugar_parcial'}
✓   Accuracy: 87.50%
ℹ   Top 5 factores importantes:
    - in_dubio_pro_operario: 0.245
    - proteccion_trabajo: 0.189
    - materia_despido: 0.156
    - test_razonabilidad: 0.132
    - tipo_demandado_empresa: 0.098
✓   Modelo guardado: modelo_Dr._Juan_Pérez.pkl

[... más jueces ...]

======================================================================
RESUMEN
======================================================================
Jueces candidatos: 5
Modelos entrenados: 4
```

### Paso 2: Hacer Predicciones

```bash
# Modo interactivo
python motor_predictivo_judicial.py "Dr. Juan Pérez" --predecir
```

**Ejemplo de uso**:
```
Predicción para: Dr. Juan Pérez
Ingrese factores del caso (ejemplo: materia=despido, tipo_actor=persona)
(presione Enter vacío para terminar)

Factor: materia=despido
Factor: tipo_actor=persona
Factor: tipo_demandado=empresa
Factor: in_dubio_pro_operario=1
Factor: proteccion_trabajo=0.8
Factor: test_razonabilidad=1
Factor: menciona_monto=1
Factor:

PREDICCIÓN:
  Resultado: hace_lugar
  Confianza: 92.34%

  Probabilidades:
    hace_lugar: 92.34%
    rechaza: 5.21%
    hace_lugar_parcial: 2.45%
```

## 📊 Cómo Funciona

### 1. Extracción de Factores

Para cada sentencia histórica:
```python
factores = {
    'materia': 'despido',
    'tipo_actor': 'persona',
    'tipo_demandado': 'empresa',
    'test_proporcionalidad': 0,
    'test_razonabilidad': 1,
    'in_dubio_pro_operario': 1,
    'in_dubio_pro_consumidor': 0,
    'proteccion_trabajo': 0.87,
    'proteccion_igualdad': 0.56,
    'estandar_prueba': 'sana_critica',
    'interpretacion': 'teleologica',
    'longitud_texto': 3245,
    'menciona_monto': 1
}
```

### 2. One-Hot Encoding

Factores categóricos se convierten:
```
materia=despido → materia_despido=1, materia_daños=0, materia_divorcio=0, ...
interpretacion=teleologica → interpretacion_teleologica=1, interpretacion_literal=0, ...
```

### 3. Entrenamiento Random Forest

```python
RandomForestClassifier(
    n_estimators=50,      # 50 árboles
    max_depth=5,          # Profundidad máxima 5
    min_samples_split=2,
    random_state=42
)
```

**Ventajas Random Forest**:
- Maneja bien datos pequeños
- Robusto a overfitting
- Proporciona feature importance
- No requiere normalización

### 4. Evaluación

- **Train/Test Split**: 80/20 si hay 10+ sentencias
- **Accuracy**: % de predicciones correctas
- **Cross-validation**: Validación cruzada interna

### 5. Feature Importance

Identifica qué factores son más determinantes:
```
Factor                    | Importancia
--------------------------|------------
in_dubio_pro_operario    | 0.245
proteccion_trabajo       | 0.189
materia_despido          | 0.156
test_razonabilidad       | 0.132
tipo_demandado_empresa   | 0.098
```

## 📈 Interpretación de Resultados

### Accuracy del Modelo

- **90-100%**: Excelente (juez muy predecible)
- **80-90%**: Muy bueno
- **70-80%**: Bueno
- **60-70%**: Aceptable
- **<60%**: Pobre (juez impredecible o pocos datos)

### Confianza de Predicción

- **90-100%**: Muy alta confianza
- **70-90%**: Alta confianza
- **50-70%**: Confianza moderada
- **<50%**: Baja confianza (caso ambiguo)

### Feature Importance

- **>0.2**: Factor muy importante
- **0.1-0.2**: Factor importante
- **0.05-0.1**: Factor moderadamente relevante
- **<0.05**: Factor poco relevante

## 💾 Qué se Guarda

### 1. Modelos en Disco

**Ubicación**: `bases_rag/cognitiva/modelos_predictivos/`

**Archivos**: `modelo_Dr._Juan_Pérez.pkl`

**Contenido**:
```python
{
    'modelo': RandomForestClassifier(...),
    'feature_names': ['materia_despido', 'in_dubio_pro_operario', ...],
    'accuracy': 0.875,
    'n_sentencias': 15,
    'clases': ['hace_lugar', 'rechaza', 'hace_lugar_parcial'],
    'feature_importance': [('in_dubio_pro_operario', 0.245), ...],
    'fecha_entrenamiento': '2025-11-12T...'
}
```

### 2. Factores en BD

**Tabla**: `factores_predictivos`

```sql
SELECT
  juez,
  factor,
  ROUND(peso, 3) as peso,
  ROUND(confianza, 2) as confianza
FROM factores_predictivos
WHERE juez = 'Dr. Juan Pérez'
ORDER BY peso DESC
LIMIT 10;
```

**Ejemplo de registros**:
```
juez: Dr. Juan Pérez
factor: in_dubio_pro_operario
peso: 0.245
confianza: 0.49

juez: Dr. Juan Pérez
factor: proteccion_trabajo
peso: 0.189
confianza: 0.38
```

## 🔍 Consultas Útiles

### Ver Factores de un Juez

```sql
SELECT
  factor,
  ROUND(peso, 3) as importancia,
  ROUND(confianza, 2) as confianza
FROM factores_predictivos
WHERE juez = 'Dr. Juan Pérez'
  AND peso > 0.05
ORDER BY peso DESC;
```

### Jueces Más Predecibles

```sql
SELECT
  juez,
  COUNT(*) as n_factores,
  ROUND(MAX(peso), 3) as max_importancia,
  ROUND(AVG(peso), 3) as prom_importancia
FROM factores_predictivos
GROUP BY juez
HAVING COUNT(*) >= 5
ORDER BY max_importancia DESC;
```

### Factores Más Comunes

```sql
SELECT
  factor,
  COUNT(DISTINCT juez) as n_jueces,
  ROUND(AVG(peso), 3) as prom_peso
FROM factores_predictivos
GROUP BY factor
HAVING COUNT(DISTINCT juez) >= 2
ORDER BY prom_peso DESC;
```

## 📊 Ejemplo Completo

### Caso: Reclamo laboral por despido

**Factores del caso**:
```
materia: despido
tipo_actor: persona (trabajador)
tipo_demandado: empresa
in_dubio_pro_operario: aplicaría (juez lo usa)
proteccion_trabajo: alta (0.8)
test_razonabilidad: aplicaría
menciona_monto: sí
```

**Juez**: Dr. Juan Pérez

**Predicción**:
```
Resultado predicho: hace_lugar
Confianza: 92%

Probabilidades:
  hace_lugar: 92%
  rechaza: 6%
  hace_lugar_parcial: 2%

Factores clave que influyen:
  1. in_dubio_pro_operario (importancia: 0.245)
  2. proteccion_trabajo alta (importancia: 0.189)
  3. materia=despido (importancia: 0.156)
  4. test_razonabilidad (importancia: 0.132)
  5. tipo_demandado=empresa (importancia: 0.098)
```

**Interpretación**:
Este juez tiende fuertemente a hacer lugar en casos de despido cuando:
- El actor es trabajador vs empresa
- Aplica in dubio pro operario
- Protege derechos laborales
- Usa test de razonabilidad

La predicción tiene 92% de confianza, indicando que en casos similares anteriores, el juez casi siempre falló a favor del trabajador.

## ⚙️ Uso Programático

### Python API

```python
from motor_predictivo_judicial import MotorPredictivoJudicial

# Inicializar
motor = MotorPredictivoJudicial()

# Entrenar modelo
modelo_data = motor.entrenar_modelo("Dr. Juan Pérez")

if modelo_data:
    print(f"Accuracy: {modelo_data['accuracy']:.2%}")
    print(f"Top factor: {modelo_data['feature_importance'][0]}")

# Predecir
factores_caso = {
    'materia': 'despido',
    'tipo_actor': 'persona',
    'tipo_demandado': 'empresa',
    'in_dubio_pro_operario': 1,
    'proteccion_trabajo': 0.8,
    'test_razonabilidad': 1,
    'menciona_monto': 1
}

resultado = motor.predecir("Dr. Juan Pérez", factores_caso)

if resultado:
    print(f"Predicción: {resultado['prediccion']}")
    print(f"Confianza: {resultado['confianza']:.2%}")
    for clase, prob in resultado['probabilidades'].items():
        print(f"  {clase}: {prob:.2%}")

motor.cerrar_bd()
```

## 🐛 Troubleshooting

### Error: "scikit-learn no está disponible"

**Solución**:
```bash
pip install scikit-learn numpy
```

### Warning: "Insuficientes sentencias"

**Causa**: El juez tiene menos de 5 sentencias con resultado conocido

**Solución**:
- Procesar más sentencias del juez (Fase 2)
- O reducir el mínimo: `--min-sentencias 3`

### Warning: "Solo hay una clase"

**Causa**: Todas las sentencias del juez tienen el mismo resultado (ej: todas "hace_lugar")

**Solución**: Normal, este juez es 100% predecible. No se puede entrenar modelo de clasificación, pero la predicción es trivial (siempre el mismo resultado).

### Modelo con Baja Accuracy (<70%)

**Causas posibles**:
- Pocas sentencias
- Juez inconsistente (varía mucho su criterio)
- Factores extraídos no son suficientemente predictivos

**Solución**:
- Conseguir más sentencias
- Revisar si hay factores adicionales relevantes
- Es normal en jueces con criterios complejos

## 🔮 Casos de Uso

### 1. Litigante

**Pregunta**: ¿Qué probabilidad tengo de ganar ante este juez?

**Uso**:
1. Identificar los factores del caso
2. Consultar predicción
3. Evaluar estrategia basándose en confianza

### 2. Investigador

**Pregunta**: ¿Qué factores son más determinantes para cada juez?

**Uso**:
1. Entrenar modelos para varios jueces
2. Comparar feature importance
3. Identificar patrones comunes

### 3. Abogado

**Pregunta**: ¿Cómo puedo aumentar las probabilidades?

**Uso**:
1. Ver feature importance
2. Identificar factores con alto peso
3. Construir estrategia que active esos factores

### 4. Analista Judicial

**Pregunta**: ¿Cuál es el perfil predictivo de este juez?

**Uso**:
1. Revisar accuracy del modelo
2. Ver top factores importantes
3. Clasificar juez (predecible/impredecible, pro-trabajador, etc.)

## ✅ Checklist de Fase 4

- [x] Extractor de factores implementado
- [x] 15+ factores relevantes extraídos
- [x] Motor de ML con Random Forest
- [x] Entrenamiento por juez
- [x] Evaluación con accuracy
- [x] Feature importance calculado
- [x] Predicción con probabilidades
- [x] Guardado de modelos en disco
- [x] Guardado de factores en BD
- [x] Modo batch (todos los jueces)
- [x] API programática
- [x] Documentación completa

## 🎉 ¡Fase 4 Completada!

El sistema ahora puede:
- ✅ Extraer factores relevantes de casos
- ✅ Entrenar modelos predictivos por juez
- ✅ Predecir decisiones con probabilidades
- ✅ Identificar factores más importantes
- ✅ Evaluar accuracy de predicciones
- ✅ Guardar modelos persistentes
- ✅ Consultar factores predictivos en BD

**Próximo (Fase 5)**: Generación de informes PDF + Sistema de preguntas

---

**Versión**: 1.0
**Fecha**: 2025-11-12
**Autor**: Sistema de Análisis de Pensamiento Judicial Argentina
