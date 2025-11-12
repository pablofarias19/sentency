# 🔄 PLAN DE MIGRACIÓN: SISTEMA DE AUTORES → SISTEMA JUDICIAL

**Fecha**: 12 Nov 2025
**Objetivo**: Convertir el sistema autor-céntrico en un sistema judicial exclusivo manteniendo la infraestructura robusta existente

---

## 🎯 VISIÓN GENERAL

### Estrategia
- ✅ **MANTENER**: Infraestructura core (RAG, embeddings, ANALYSER, webapp, IA)
- 🔄 **ADAPTAR**: Archivos reutilizables para trabajar con jueces/sentencias
- ❌ **ELIMINAR**: Referencias específicas a autores
- 🆕 **INTEGRAR**: Los 15 scripts nuevos de análisis judicial

### Resultado Final
**UN SOLO SISTEMA**: Análisis de Pensamiento Judicial Argentino
- Webapp única para jueces
- Base de datos unificada
- Motores cognitivos adaptados
- Pipeline completo de ingesta → análisis → informes

---

## 📊 MAPEO DE ARCHIVOS

### ✅ CATEGORÍA 1: CORE INFRASTRUCTURE (MANTENER Y ADAPTAR)

Estos archivos son la base del sistema y deben **adaptarse** para jueces:

#### 1.1 Motor ANALYSER Cognitivo
**Archivo**: `analyser_metodo_mejorado.py` (2000+ líneas)
- **Estado actual**: Analiza pensamiento de autores
- **Acción**: ADAPTAR para analizar sentencias judiciales
- **Cambios necesarios**:
  - Mantener 100% de los patrones (ya son jurídicos: deductivo, inductivo, razonabilidad, etc.)
  - Cambiar referencias de "autor" → "juez"
  - Cambiar tablas BD de `perfiles_autorales` → `perfiles_judiciales_argentinos`
  - Integrar con `analizador_pensamiento_judicial_arg.py` (nuevo)
- **Prioridad**: 🔴 ALTA (es el corazón del análisis cognitivo)

#### 1.2 Sistema de Embeddings
**Archivos**:
- `embeddings_fusion.py`
- Modelos en `models/embeddings/`
- **Estado**: FUNCIONAL
- **Acción**: MANTENER SIN CAMBIOS
- **Razón**: Los embeddings funcionan igual para autores o sentencias
- **Prioridad**: 🟢 BAJA (ya funciona)

#### 1.3 Ingesta y Procesamiento de PDFs
**Archivos**:
- `extractor_pdf_enriquecido.py` ✅
- `chunker_inteligente.py` ✅
- **Estado**: FUNCIONAL
- **Acción**: REUTILIZAR directamente
- **Integración**: Ya usado por `ingesta_sentencias_judicial.py` (nuevo)
- **Prioridad**: 🟢 BAJA (ya integrado)

#### 1.4 Sistema RAG y FAISS
**Archivos**:
- `analizador_enriquecido_rag.py`
- `profiles_rag.py`
- `query_rag_sentencias.py` ⚠️ (ya tiene "sentencias" en el nombre)
- **Acción**: ADAPTAR nombres de tablas/colecciones
- **Cambios**:
  - Apuntar a `juez_centrico_arg.db` en lugar de `autor_centrico.db`
  - Mantener toda la lógica de embeddings/búsqueda
- **Prioridad**: 🟡 MEDIA

#### 1.5 Webapp Flask
**Archivo**: `end2end_webapp.py` (4000+ líneas)
- **Estado**: Sistema completo con múltiples rutas
- **Acción**: REFACTORIZAR COMPLETO
- **Cambios necesarios**:
  ```python
  # ELIMINAR rutas:
  - /autores (sistema autor-céntrico)
  - /pensamiento (análisis multi-capa de autores)
  - /comparar_autores

  # MANTENER rutas core:
  - / (búsqueda RAG principal)
  - /cognitivo (ANALYSER adaptado a jueces)
  - /radar (radar cognitivo adaptado)

  # AGREGAR nuevas rutas:
  - /jueces (listado y búsqueda de jueces)
  - /juez/<nombre> (perfil completo del juez)
  - /lineas/<juez> (líneas jurisprudenciales)
  - /red/<juez> (red de influencias)
  - /prediccion/<juez> (análisis predictivo)
  - /informes (generador de informes)
  - /preguntas/<juez> (sistema de 140 preguntas)
  ```
- **Prioridad**: 🔴 CRÍTICA (interfaz principal del sistema)

#### 1.6 Biblioteca Cognitiva
**Archivo**: `biblioteca_cognitiva.py`
- **Acción**: ADAPTAR
- **Cambios**: Referencias a autores → jueces, tablas BD
- **Prioridad**: 🟡 MEDIA

---

### 🔄 CATEGORÍA 2: ARCHIVOS DE INGESTA (CONSOLIDAR)

**Archivos existentes**:
- `ingesta_cognitiva.py`
- `ingesta_cognitiva_v3.py`
- `ingesta_enriquecida.py`
- `ingesta_sentencias.py` ⚠️ (ya para sentencias)
- `coordinador_central_ingesta.py`
- `motor_ingesta_pensamiento.py`
- `procesador_ingesta_cognitiva.py`

**Archivo nuevo**:
- `ingesta_sentencias_judicial.py` ✅ (Fase 1)

**Acción**: CONSOLIDAR
- Evaluar `ingesta_sentencias.py` vs `ingesta_sentencias_judicial.py`
- Si el antiguo es compatible, FUSIONAR
- Si no, REEMPLAZAR con el nuevo
- Eliminar versiones duplicadas (v3, backup, etc.)
- **Prioridad**: 🟡 MEDIA

---

### ❌ CATEGORÍA 3: ARCHIVOS ESPECÍFICOS DE AUTORES (ELIMINAR)

Estos archivos solo sirven para autores y deben **eliminarse**:

```
❌ sistema_autor_centrico.py
❌ visualizador_autor_centrico.py
❌ comparador_mentes.py (comparar autores)
❌ inicializar_autor_centrico.py
❌ migrar_autor_centrico.py
❌ detector_autor_y_metodo.py
❌ gestor_unificado_autores.py
❌ sistema_referencias_autores.py
❌ agregar_nuevo_autor.py
❌ verificar_autores.py
❌ buscar_seba.py (script específico)
❌ diagnosticar_autor_scotti.py (script específico)
```

**Acción**: ELIMINAR después de confirmar que no son dependencias críticas
**Prioridad**: 🟢 BAJA (al final de la migración)

---

### 🆕 CATEGORÍA 4: ARCHIVOS NUEVOS JUDICIALES (INTEGRAR)

Ya creados y funcionan independientemente:

```
✅ schema_juez_centrico_arg.sql
✅ inicializar_bd_judicial.py
✅ extractor_metadata_argentina.py
✅ ingesta_sentencias_judicial.py
✅ analizador_pensamiento_judicial_arg.py
✅ procesador_sentencias_completo.py
✅ agregador_perfiles_jueces.py
✅ analizador_lineas_jurisprudenciales.py
✅ extractor_citas_jurisprudenciales.py
✅ analizador_redes_influencia.py
✅ motor_predictivo_judicial.py
✅ generador_informes_judicial.py
✅ sistema_preguntas_judiciales.py
✅ motor_respuestas_judiciales.py
```

**Acción**: INTEGRAR con webapp y sistema core
**Prioridad**: 🔴 ALTA

---

### 🔧 CATEGORÍA 5: UTILIDADES Y SCRIPTS DE MANTENIMIENTO (ADAPTAR NOMBRES)

Archivos de utilidad que necesitan ajustes menores:

```
🔧 verificar_bd_v2.py → Adaptar para verificar juez_centrico_arg.db
🔧 verificar_perfiles.py → Adaptar para perfiles judiciales
🔧 verificar_datos_rag.py → Mantener
🔧 listar_tablas.py → Adaptar para nuevas tablas
🔧 diagnostico_sistema_completo.py → Actualizar diagnósticos
🔧 verificador_sistema_completo.py → Actualizar verificaciones
🔧 limpiar_db.py → Adaptar para nueva BD
🔧 mantener_sistema.py → Actualizar
```

**Acción**: ADAPTAR referencias de BD y tablas
**Prioridad**: 🟢 BAJA

---

### ⚡ CATEGORÍA 6: SCRIPTS DE ANÁLISIS ESPECÍFICOS (EVALUAR)

Funcionalidades analíticas que podrían ser útiles:

```
📊 analizador_argumentativo.py - ¿Útil para sentencias? → EVALUAR
📊 analizador_estructural_sentencias.py - ¡Ya es para sentencias! → MANTENER
📊 analizador_temporal.py - Evolución temporal → ADAPTAR para jueces
📊 detector_razonamiento_aristotelico.py - Razonamiento → ADAPTAR
📊 generador_explicaciones_cognitivas.py - Explicaciones → ADAPTAR
📊 grafo_conocimiento.py - Grafo de conceptos → ADAPTAR
```

**Acción**: EVALUAR caso por caso y ADAPTAR los útiles
**Prioridad**: 🟡 MEDIA

---

## 🗺️ PLAN DE EJECUCIÓN (5 FASES)

### **FASE A: PREPARACIÓN Y ANÁLISIS** (1-2 horas)
✅ Mapeo completo de dependencias
✅ Backup del sistema actual
✅ Identificar qué archivos usa realmente la webapp

### **FASE B: ADAPTACIÓN DEL CORE** (3-4 horas)
🔄 Adaptar `analyser_metodo_mejorado.py` para jueces
🔄 Adaptar `biblioteca_cognitiva.py`
🔄 Adaptar sistema RAG para apuntar a `juez_centrico_arg.db`
🔄 Fusionar/consolidar scripts de ingesta

### **FASE C: REFACTOR DE WEBAPP** (4-5 horas)
🔄 Eliminar rutas de autores de `end2end_webapp.py`
🔄 Agregar rutas para jueces/sentencias
🔄 Integrar generador de informes
🔄 Integrar sistema de preguntas
🔄 Actualizar templates HTML

### **FASE D: INTEGRACIÓN Y PRUEBAS** (2-3 horas)
✅ Conectar todos los componentes
✅ Probar pipeline completo
✅ Verificar que ANALYSER funciona con sentencias
✅ Probar generación de informes desde webapp

### **FASE E: LIMPIEZA FINAL** (1 hora)
❌ Eliminar archivos de autores no usados
❌ Eliminar bases de datos antiguas
📝 Actualizar documentación
📝 Crear README.md principal del sistema unificado

---

## 📋 ARCHIVOS CRÍTICOS A MODIFICAR (PRIORIDAD)

### 🔴 PRIORIDAD 1 (Esenciales)
1. **end2end_webapp.py** - Interfaz principal
2. **analyser_metodo_mejorado.py** - Motor de análisis cognitivo
3. **Integración de 15 scripts nuevos** - Funcionalidad judicial

### 🟡 PRIORIDAD 2 (Importantes)
4. **biblioteca_cognitiva.py** - Sistema de conocimiento
5. **analizador_enriquecido_rag.py** - Sistema RAG
6. **Consolidar ingesta** - Pipeline de PDFs

### 🟢 PRIORIDAD 3 (Complementarias)
7. Scripts de verificación/diagnóstico
8. Eliminar archivos obsoletos
9. Documentación final

---

## 🎯 RESULTADO FINAL ESPERADO

### Estructura del Sistema Unificado

```
sentency/
├── App_colaborativa/
│   └── colaborative/
│       ├── bases_rag/
│       │   └── cognitiva/
│       │       ├── juez_centrico_arg.db ✅ (ÚNICA BD)
│       │       └── modelos_predictivos/ ✅
│       │
│       ├── scripts/
│       │   ├── [CORE - ADAPTADOS]:
│       │   │   ├── analyser_judicial.py (adapt. de analyser_metodo_mejorado.py)
│       │   │   ├── biblioteca_judicial.py (adapt. de biblioteca_cognitiva.py)
│       │   │   ├── rag_judicial.py (adapt. de analizador_enriquecido_rag.py)
│       │   │   ├── webapp_judicial.py (adapt. de end2end_webapp.py)
│       │   │   ├── chunker_inteligente.py ✅ (sin cambios)
│       │   │   ├── embeddings_fusion.py ✅ (sin cambios)
│       │   │   └── extractor_pdf_enriquecido.py ✅ (sin cambios)
│       │   │
│       │   ├── [JUDICIAL - FASE 1]:
│       │   │   ├── schema_juez_centrico_arg.sql ✅
│       │   │   ├── inicializar_bd_judicial.py ✅
│       │   │   ├── extractor_metadata_argentina.py ✅
│       │   │   └── ingesta_sentencias_judicial.py ✅
│       │   │
│       │   ├── [JUDICIAL - FASE 2]:
│       │   │   ├── analizador_pensamiento_judicial_arg.py ✅
│       │   │   ├── procesador_sentencias_completo.py ✅
│       │   │   └── agregador_perfiles_jueces.py ✅
│       │   │
│       │   ├── [JUDICIAL - FASE 3]:
│       │   │   ├── analizador_lineas_jurisprudenciales.py ✅
│       │   │   ├── extractor_citas_jurisprudenciales.py ✅
│       │   │   └── analizador_redes_influencia.py ✅
│       │   │
│       │   ├── [JUDICIAL - FASE 4]:
│       │   │   └── motor_predictivo_judicial.py ✅
│       │   │
│       │   ├── [JUDICIAL - FASE 5]:
│       │   │   ├── generador_informes_judicial.py ✅
│       │   │   ├── sistema_preguntas_judiciales.py ✅
│       │   │   └── motor_respuestas_judiciales.py ✅
│       │   │
│       │   └── [UTILIDADES]:
│       │       ├── verificar_sistema_judicial.py (adaptado)
│       │       ├── diagnostico_judicial.py (adaptado)
│       │       └── mantener_sistema_judicial.py (adaptado)
│       │
│       └── templates/ (HTML adaptados para jueces)
│
└── [DOCUMENTACIÓN]:
    ├── README.md ✅ (PRINCIPAL - nuevo)
    ├── ARQUITECTURA_SISTEMA_JUDICIAL.md ✅ (nuevo)
    ├── PLAN_MIGRACION_SISTEMA_JUDICIAL.md ✅ (este archivo)
    ├── FASE1_README.md ✅
    ├── FASE2_README.md ✅
    ├── FASE3_README.md ✅
    ├── FASE4_README.md ✅
    └── FASE5_README.md ✅
```

### Características del Sistema Final

✅ **Sistema unificado**: Un solo sistema judicial, no paralelo
✅ **Infraestructura robusta**: Mantiene todo lo que funciona (RAG, ANALYSER, embeddings, IA)
✅ **Adaptado para jueces**: Todo orientado a análisis judicial argentino
✅ **Sin duplicación**: Un solo set de archivos, BD única
✅ **Webapp funcional**: Interfaz web completa para jueces
✅ **Pipeline completo**: Ingesta → Análisis → Predicción → Informes
✅ **Documentación clara**: READMEs organizados por fase

---

## 🚀 PRÓXIMOS PASOS

1. **Revisar y aprobar este plan** ✅ (necesita tu confirmación)
2. **Backup completo del sistema actual**
3. **Ejecutar Fase A** (preparación)
4. **Ejecutar Fase B** (adaptación core)
5. **Ejecutar Fase C** (webapp)
6. **Ejecutar Fase D** (integración)
7. **Ejecutar Fase E** (limpieza)

---

## ❓ PREGUNTAS PARA DECIDIR

Antes de empezar, necesito confirmar:

1. **¿Quieres que empiece la migración ahora?**
   - Podemos hacer fase por fase
   - O puedo preparar todo el código y aplicarlo junto

2. **¿Qué archivos del sistema antiguo quieres revisar primero?**
   - Para ver exactamente qué reutilizar

3. **¿Alguna funcionalidad específica del sistema antiguo que quieras asegurar mantener?**
   - Por ejemplo: comparaciones, visualizaciones 3D, etc.

4. **¿Prefieres que el resultado sea "mínimo viable" o "feature-complete"?**
   - Mínimo: Solo lo esencial funcionando
   - Complete: Todas las funcionalidades portadas

---

**¿Confirmas que este es el plan correcto y quieres que empiece con la adaptación?**
