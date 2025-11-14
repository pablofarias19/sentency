# Arquitectura de Base de Datos Centralizada

## 🎯 Objetivo

Resolver la fragmentación de bases de datos y rutas del proyecto mediante una arquitectura centralizada con una única base de datos y configuración unificada.

## 📊 Problema Original

### Situación Previa (Fragmentada)

```
App_colaborativa/colaborative/
├─ data/
│  ├─ autoaprendizaje.db
│  ├─ cognitivo.db
│  ├─ perfiles.db
│  └─ pensamiento_integrado_v2.db
│
├─ bases_rag/cognitiva/
│  ├─ metadatos.db
│  └─ juez_centrico_arg.db (esperada pero no existía)
│
└─ scripts/
   ├─ end2end_webapp.py (rutas hardcodeadas)
   ├─ ingesta_sentencias_judicial.py (rutas hardcodeadas)
   └─ ... otros scripts (rutas inconsistentes)
```

**Problemas:**
- ❌ Múltiples BDs fragmentadas
- ❌ Rutas hardcodeadas en cada script
- ❌ Inconsistencias entre scripts
- ❌ Errores NoneType por BD vacía/inexistente
- ❌ `/cognitivo/<juez>` no encuentra datos
- ❌ Difícil mantenimiento y debugging

## ✅ Solución Implementada

### Nueva Arquitectura Centralizada

```
App_colaborativa/colaborative/
│
├─ config.py                      ← CONFIGURACIÓN CENTRALIZADA
├─ judicial_system.db             ← BD ÚNICA CENTRALIZADA
├─ crear_bd_centralizada.py       ← Script de creación de BD
│
├─ data/
│  ├─ pdfs/
│  │  └─ sentencias_pdf/
│  ├─ txt/
│  ├─ chunks/
│  └─ index/
│
├─ bases_rag/cognitiva/
│  └─ (índices FAISS y metadatos)
│
├─ models/
│  ├─ embeddings/
│  ├─ ner/
│  └─ generator/
│
└─ scripts/
   ├─ config_rutas.py (actualizado para usar config.py)
   ├─ end2end_webapp.py (actualizado)
   ├─ ingesta_sentencias_judicial.py (actualizado)
   ├─ webapp_rutas_judicial.py (actualizado)
   ├─ analyser_judicial_adapter.py (actualizado)
   ├─ analizador_lineas_jurisprudenciales.py (actualizado)
   ├─ analizador_redes_influencia.py (actualizado)
   ├─ motor_predictivo_judicial.py (actualizado)
   ├─ motor_respuestas_judiciales.py (actualizado)
   ├─ generador_informes_judicial.py (actualizado)
   └─ inicializar_bd_judicial.py (actualizado)
```

## 🗄️ Base de Datos Centralizada

### Ubicación
```
/App_colaborativa/colaborative/judicial_system.db
```

### Tablas Principales

1. **sentencias_por_juez_arg**
   - Tabla principal con todas las sentencias
   - Incluye metadata, análisis cognitivo, referencias normativas
   - Métricas de calidad y predicción
   - 50+ campos especializados

2. **perfiles_judiciales_argentinos**
   - Perfiles agregados por juez
   - Estadísticas y patrones de decisión
   - Métricas promedio

3. **perfiles_cognitivos**
   - Análisis cognitivo detallado
   - Tipos de razonamiento
   - Sesgos identificados

4. **lineas_jurisprudenciales**
   - Líneas jurisprudenciales consistentes
   - Evolución temporal
   - Criterios unificadores

5. **redes_influencia_judicial**
   - Relaciones entre jueces
   - Citas directas e indirectas
   - Métricas de influencia

6. **factores_predictivos**
   - Factores de decisión
   - Pesos y precisión histórica
   - Por juez, materia y tipo de proceso

7. **metadatos**
   - Metadata general del sistema
   - Compatibilidad con sistema anterior

## 📝 Configuración Centralizada (config.py)

### Rutas Principales

```python
from config import (
    DATABASE_PATH,      # BD centralizada
    BASE_DIR,          # Directorio raíz
    DATA_DIR,          # Directorio de datos
    PDF_DIR,           # PDFs
    MODELS_DIR,        # Modelos
    BASES_RAG_DIR,     # Índices RAG
    get_db_connection  # Función helper
)
```

### Ejemplo de Uso en Scripts

**Antes (Fragmentado):**
```python
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
BASES_RAG_DIR = BASE_DIR / "bases_rag" / "cognitiva"
DB_FILE = BASES_RAG_DIR / "juez_centrico_arg.db"
```

**Después (Centralizado):**
```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DATABASE_PATH as DB_FILE, BASES_RAG_DIR
```

## 🚀 Uso

### 1. Crear Base de Datos Centralizada

```bash
cd App_colaborativa/colaborative
python crear_bd_centralizada.py
```

Esto crea `judicial_system.db` con todas las tablas necesarias.

### 2. Verificar Configuración

```bash
python config.py
```

Muestra la configuración actual y verifica que todos los directorios existan.

### 3. Ingesta de Sentencias

```bash
cd scripts
python ingesta_sentencias_judicial.py
```

Ahora guarda automáticamente en la BD centralizada.

### 4. Iniciar Webapp

```bash
cd scripts
python end2end_webapp.py
```

La webapp ahora usa la BD centralizada automáticamente.

## 📋 Scripts Actualizados

Todos los siguientes scripts ahora usan la configuración centralizada:

### Core del Sistema
- ✅ `config.py` - **NUEVO** Configuración centralizada
- ✅ `crear_bd_centralizada.py` - **NUEVO** Creador de BD
- ✅ `config_rutas.py` - Actualizado para compatibilidad

### Webapp
- ✅ `end2end_webapp.py` - Servidor Flask principal
- ✅ `webapp_rutas_judicial.py` - Rutas judiciales

### Análisis
- ✅ `analyser_judicial_adapter.py` - Adaptador ANALYSER
- ✅ `analizador_lineas_jurisprudenciales.py`
- ✅ `analizador_redes_influencia.py`
- ✅ `motor_predictivo_judicial.py`
- ✅ `motor_respuestas_judiciales.py`
- ✅ `generador_informes_judicial.py`

### Ingesta y BD
- ✅ `ingesta_sentencias_judicial.py`
- ✅ `inicializar_bd_judicial.py`

## 🎯 Ventajas de la Nueva Arquitectura

### Antes vs Después

| Aspecto | Antes | Después |
|---------|-------|---------|
| **BDs** | 4+ BDs fragmentadas | 1 BD centralizada |
| **Rutas** | Hardcodeadas en cada script | Centralizadas en config.py |
| **Mantenimiento** | Complejo (cambiar 20+ archivos) | Simple (cambiar config.py) |
| **Debugging** | Difícil (rutas inconsistentes) | Fácil (una única verdad) |
| **Errores NoneType** | Frecuentes | Eliminados |
| **Escalabilidad** | Limitada | Alta |
| **Documentación** | Dispersa | Centralizada aquí |

### Beneficios Concretos

1. **Una Única Verdad**
   - Todos los datos en `judicial_system.db`
   - Sin ambigüedades ni duplicaciones

2. **Rutas Centralizadas**
   - Todas en `config.py`
   - Fácil de modificar y mantener

3. **Sin Errores de Ruta**
   - Scripts siempre encuentran la BD
   - `/cognitivo/<juez>` funciona correctamente

4. **Fácil Debugging**
   - Un solo lugar para verificar datos
   - Logs consistentes

5. **Mejor Performance**
   - Sin múltiples conexiones a BDs diferentes
   - Índices optimizados en una sola BD

6. **Migración Simplificada**
   - Backup/restore de un solo archivo
   - Desarrollo/producción consistente

## 🔄 Migración de Datos

Si existen datos en BDs antiguas, se pueden migrar así:

```bash
# Crear BD centralizada
python crear_bd_centralizada.py

# Migrar datos (si existieran)
# Los scripts de ingesta guardarán automáticamente en la BD centralizada
```

## 📊 Esquema de Base de Datos

### Diagrama de Relaciones

```
sentencias_por_juez_arg
    ├─ id (PK)
    ├─ sentencia_id (UNIQUE)
    ├─ juez
    ├─ metadata (50+ campos)
    └─ linea_jurisprudencial_id (FK)
         └─> lineas_jurisprudenciales

perfiles_judiciales_argentinos
    ├─ id (PK)
    ├─ juez (UNIQUE)
    └─ estadísticas agregadas

perfiles_cognitivos
    ├─ id (PK)
    ├─ sentencia_id (FK)
    └─ análisis cognitivo

redes_influencia_judicial
    ├─ id (PK)
    ├─ juez_origen
    ├─ juez_destino
    └─ métricas de influencia

factores_predictivos
    ├─ id (PK)
    ├─ juez
    ├─ materia
    └─ factores y pesos
```

## 🔍 Verificación

### Comprobar que Todo Funciona

```bash
# 1. Verificar que la BD existe
ls -lh judicial_system.db

# 2. Verificar tablas
sqlite3 judicial_system.db ".tables"

# 3. Verificar configuración
python config.py

# 4. Probar ingesta
python scripts/ingesta_sentencias_judicial.py --help

# 5. Iniciar webapp
python scripts/end2end_webapp.py
```

## 📚 Documentación Adicional

- **config.py**: Contiene todas las constantes de configuración
- **crear_bd_centralizada.py**: Script documentado de creación de BD
- **Scripts individuales**: Cada uno tiene su propia documentación inline

## 🛠️ Mantenimiento

### Agregar Nueva Ruta

1. Editar `config.py`
2. Agregar la nueva ruta como constante
3. Importarla en los scripts que la necesiten

### Modificar Esquema de BD

1. Editar `crear_bd_centralizada.py`
2. Ejecutar para recrear la BD
3. Migrar datos si es necesario

### Actualizar Script para Usar Config Centralizado

```python
# Agregar al inicio del script:
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DATABASE_PATH, BASE_DIR, ...

# Usar las constantes importadas
db_path = DATABASE_PATH
```

## 📝 Notas

- La BD centralizada (`judicial_system.db`) debe estar en la raíz de `colaborative/`
- `config_rutas.py` se mantiene por compatibilidad pero delega a `config.py`
- Todos los scripts ahora usan la misma BD, eliminando fragmentación
- Los índices FAISS y metadatos RAG permanecen en `bases_rag/cognitiva/`

## 🎓 Para Desarrolladores

Si estás desarrollando un nuevo módulo:

1. **Importa siempre de config.py:**
   ```python
   from config import DATABASE_PATH, BASE_DIR, DATA_DIR
   ```

2. **Usa get_db_connection() para conexiones:**
   ```python
   from config import get_db_connection

   conn = get_db_connection()
   cursor = conn.cursor()
   ```

3. **No hardcodees rutas:**
   ```python
   # ❌ MAL
   db_path = "bases_rag/cognitiva/juez_centrico_arg.db"

   # ✅ BIEN
   from config import DATABASE_PATH
   db_path = DATABASE_PATH
   ```

---

**Versión:** 1.0
**Fecha:** 2025-11-14
**Autor:** Sistema de Análisis Judicial Argentino
**Estado:** ✅ Implementado y Funcional
