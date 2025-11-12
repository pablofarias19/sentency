# 🪟 MIGRACIÓN AL REPOSITORIO ORIGINAL (WINDOWS)

Tu repositorio original está en:
```
C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL\App_colaborativa
```

---

## 🎯 PLAN DE MIGRACIÓN PARA WINDOWS

### Paso 1: Crear Backup

**Abrir PowerShell o CMD y ejecutar:**

```powershell
# Crear backup con fecha
cd "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL"

# Copiar todo el directorio
xcopy "App_colaborativa" "App_colaborativa_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%" /E /I /H

# Verificar
dir | findstr backup
```

---

## 🗑️ PASO 2: ELIMINAR ARCHIVOS DE AUTORES

### A. Eliminar scripts de autores en `colaborative\scripts\`

```powershell
cd "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL\App_colaborativa\colaborative\scripts"

# Eliminar archivos de autores (uno por uno para seguridad)
del sistema_autor_centrico.py
del visualizador_autor_centrico.py
del comparador_mentes.py
del gestor_unificado_autores.py
del detector_autor_y_metodo.py
del agregar_nuevo_autor.py
del verificar_autores.py
del analizador_perfiles.py
del ingesta_cognitiva.py
del ingesta_cognitiva_v3.py
del ingesta_enriquecida.py
del motor_ingesta_pensamiento.py
del reparar_rasgos_cognitivos.py
del actualizar_db_analyser.py
del analizador_multicapa_pensamiento.py
```

**Nota:** Si algún archivo no existe, simplemente ignora el error.

### B. Eliminar bases de datos de autores

```powershell
cd "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL\App_colaborativa\colaborative\bases_rag\cognitiva"

# Eliminar bases de datos de autores
del autor_centrico.db
del perfiles_autorales.db
del multicapa_pensamiento.db
del pensamiento_integrado_v2.db
```

---

## 📥 PASO 3: DESCARGAR ARCHIVOS DE GITHUB

Desde GitHub, descarga estos archivos del sistema judicial:

### Opción A: Descargar repositorio completo

1. Ve a: `https://github.com/pablofarias19/sentency`
2. Click en "Code" → "Download ZIP"
3. Descomprimir el ZIP
4. Navegar a la carpeta descomprimida

### Opción B: Usar Git (si lo tienes instalado)

```powershell
cd "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL"
git clone https://github.com/pablofarias19/sentency.git sentency-judicial
cd sentency-judicial
git checkout claude/judges-analysis-refactor-011CV32W8GANMnkrbjRKMaY2
```

---

## 📋 PASO 4: COPIAR ARCHIVOS JUDICIALES

### A. Copiar scripts judiciales (15 archivos)

**Desde** (repositorio descargado):
```
sentency\App_colaborativa\colaborative\scripts\
```

**Hacia** (tu repositorio original):
```
C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL\App_colaborativa\colaborative\scripts\
```

**Archivos a copiar:**

```powershell
# Navegar al directorio de scripts origen (ajusta la ruta según donde descargaste)
$ORIGEN = "C:\Users\USUARIO\Downloads\sentency-main\App_colaborativa\colaborative\scripts"
$DESTINO = "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL\App_colaborativa\colaborative\scripts"

# Copiar archivos judiciales
copy "$ORIGEN\inicializar_bd_judicial.py" "$DESTINO\"
copy "$ORIGEN\ingesta_sentencias_judicial.py" "$DESTINO\"
copy "$ORIGEN\extractor_metadata_argentina.py" "$DESTINO\"
copy "$ORIGEN\schema_juez_centrico_arg.sql" "$DESTINO\"

copy "$ORIGEN\analizador_pensamiento_judicial_arg.py" "$DESTINO\"
copy "$ORIGEN\procesador_sentencias_completo.py" "$DESTINO\"
copy "$ORIGEN\agregador_perfiles_jueces.py" "$DESTINO\"

copy "$ORIGEN\analizador_lineas_jurisprudenciales.py" "$DESTINO\"
copy "$ORIGEN\extractor_citas_jurisprudenciales.py" "$DESTINO\"
copy "$ORIGEN\analizador_redes_influencia.py" "$DESTINO\"

copy "$ORIGEN\motor_predictivo_judicial.py" "$DESTINO\"

copy "$ORIGEN\generador_informes_judicial.py" "$DESTINO\"
copy "$ORIGEN\sistema_preguntas_judiciales.py" "$DESTINO\"
copy "$ORIGEN\motor_respuestas_judiciales.py" "$DESTINO\"

copy "$ORIGEN\analyser_judicial_adapter.py" "$DESTINO\"
copy "$ORIGEN\webapp_rutas_judicial.py" "$DESTINO\"
```

### B. Copiar scripts de utilidad (3 archivos)

```powershell
$ORIGEN_RAIZ = "C:\Users\USUARIO\Downloads\sentency-main\App_colaborativa"
$DESTINO_RAIZ = "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL\App_colaborativa"

copy "$ORIGEN_RAIZ\limpiar_sistema_autores.py" "$DESTINO_RAIZ\"
copy "$ORIGEN_RAIZ\integrar_sistema_judicial.py" "$DESTINO_RAIZ\"
copy "$ORIGEN_RAIZ\limpieza_final_repositorio.py" "$DESTINO_RAIZ\"
```

### C. Copiar documentación

```powershell
# README principal
$ORIGEN_DOC = "C:\Users\USUARIO\Downloads\sentency-main"
$DESTINO_DOC = "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL"

copy "$ORIGEN_DOC\README.md" "$DESTINO_DOC\"
copy "$ORIGEN_DOC\PLAN_MIGRACION_SISTEMA_JUDICIAL.md" "$DESTINO_DOC\"
copy "$ORIGEN_DOC\LIMPIEZA_FINAL.md" "$DESTINO_DOC\"
copy "$ORIGEN_DOC\PASOS_FINALES.md" "$DESTINO_DOC\"
copy "$ORIGEN_DOC\verificar_migracion_completa.py" "$DESTINO_DOC\"

# Documentación de fases
copy "$ORIGEN_DOC\App_colaborativa\FASE1_README.md" "$DESTINO_RAIZ\"
copy "$ORIGEN_DOC\App_colaborativa\FASE2_README.md" "$DESTINO_RAIZ\"
copy "$ORIGEN_DOC\App_colaborativa\FASE3_README.md" "$DESTINO_RAIZ\"
copy "$ORIGEN_DOC\App_colaborativa\FASE4_README.md" "$DESTINO_RAIZ\"
copy "$ORIGEN_DOC\App_colaborativa\FASE5_README.md" "$DESTINO_RAIZ\"
copy "$ORIGEN_DOC\App_colaborativa\PROPUESTA_AJUSTADA_JUECES_ARG.md" "$DESTINO_RAIZ\"
```

---

## 🔗 PASO 5: INTEGRAR WEBAPP

```powershell
cd "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL\App_colaborativa"

# Ejecutar script de integración
python integrar_sistema_judicial.py
```

Este script modificará `end2end_webapp.py` para agregar las rutas judiciales.

---

## ✅ PASO 6: VERIFICAR MIGRACIÓN

```powershell
cd "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL"

# Ejecutar verificación
python verificar_migracion_completa.py
```

---

## 🚀 PASO 7: PROBAR SISTEMA

```powershell
cd "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL\App_colaborativa\colaborative\scripts"

# Inicializar base de datos judicial
python inicializar_bd_judicial.py

# Iniciar webapp
python end2end_webapp.py
```

Abrir navegador en: `http://127.0.0.1:5002`

---

## 📊 RESUMEN DE CAMBIOS

### Archivos eliminados:
- ❌ ~15 scripts de autores en `scripts/`
- ❌ 4 bases de datos de autores en `bases_rag/cognitiva/`

### Archivos nuevos:
- ✅ 16 archivos del sistema judicial
- ✅ 3 scripts de utilidad
- ✅ 11 archivos de documentación

### Archivos modificados:
- 🔄 `end2end_webapp.py` (integración de rutas judiciales)

### Archivos sin cambios:
- ✅ `analyser_metodo_mejorado.py` (ANALYSER core)
- ✅ `chunker_inteligente.py`
- ✅ `embeddings_fusion.py`
- ✅ `extractor_pdf_enriquecido.py`
- ✅ `analizador_enriquecido_rag.py`
- ✅ Todos los demás archivos de infraestructura

---

## ⚠️ NOTAS IMPORTANTES

### Rutas Absolutas
Si encuentras errores sobre rutas no encontradas, busca y reemplaza:

```powershell
# En los archivos Python, buscar:
/home/user/sentency

# Reemplazar por tu ruta:
C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL
```

### Dependencias Python
Asegúrate de tener instaladas:

```powershell
pip install flask sqlite3 pandas numpy scikit-learn sentence-transformers
```

### Base de Datos
La primera vez que ejecutes `inicializar_bd_judicial.py`, creará:
```
App_colaborativa\colaborative\bases_rag\cognitiva\juez_centrico_arg.db
```

---

## 🆘 PROBLEMAS COMUNES

### Error: "No such file or directory"
- Verifica que las rutas no tengan espacios sin comillas
- Usa comillas dobles en PowerShell: `"ruta con espacios"`

### Error: "Module not found"
- Instalar dependencias: `pip install -r requirements.txt`
- O instalar individualmente las que falten

### Webapp no inicia
- Verificar puerto 5002 no esté ocupado
- Revisar que `end2end_webapp.py` tenga las importaciones de rutas judiciales

---

## 📞 SIGUIENTE PASO

Una vez completados estos pasos, tendrás tu sistema original migrado al sistema judicial argentino. Todo listo para:

1. ✅ Ingestar sentencias argentinas
2. ✅ Analizar pensamiento judicial
3. ✅ Generar perfiles de jueces
4. ✅ Crear líneas jurisprudenciales
5. ✅ Análisis predictivo
6. ✅ Generación de informes

¿Necesitas ayuda con algún paso específico?
