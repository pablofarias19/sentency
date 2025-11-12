# 🧹 LIMPIEZA FINAL DEL REPOSITORIO

Plan completo para dejar el repositorio limpio y solo con sistema judicial.

---

## ✅ YA HECHO

- ✅ Eliminados 20 scripts de autores en `scripts/`
- ✅ Eliminadas 4 bases de datos de autores
- ✅ Eliminados 59 archivos __pycache__
- ✅ Integrado sistema judicial con webapp
- ✅ Commits y push realizados

---

## 🔍 ARCHIVOS QUE FALTAN POR LIMPIAR

### En `/App_colaborativa/` (directorio raíz)

Hay **~90 archivos Python** en el directorio raíz, muchos específicos de autores.

#### **Archivos ESPECÍFICOS de autores a eliminar**:

```
agregar_nuevo_autor.py
buscar_seba.py
diagnosticar_autor_scotti.py
diagnosticar_autores_citados.py
diagnostico_autoria.py
diagnostico_bases_autores.py
migrar_autor_centrico.py
reparar_rasgos_cognitivos.py
verificar_autores.py
biblioteca_cognitiva.py  (hay una en scripts/ que se usa)
biblioteca_cognitiva_corregida.py
buscar_luciana_todas_bases.py
```

#### **Scripts de diagnóstico/verificación antiguos** (evaluar):

```
diagnostico_sistema_completo.py
diagnostico_discrepancia.py
diagnostico_fecha_creacion.py
verificar_bd_v2.py
verificar_perfiles.py
verificador_sistema_completo.py
auditoria_ecosistema_completo.py
auditoria_sistema.py
analisis_completo_sistema.py
```

Estos **pueden mantenerse** si sirven para verificar el sistema judicial, pero muchos probablemente solo funcionan con el sistema de autores.

#### **Scripts de mantenimiento antiguos**:

```
reparar_sistema_completo.py
coordinador_ultra_rapido.py
procesador_integral_mejorado.py
actualizador_integral_bases.py
actualizador_rapido.py
actualizar_palabras.py
corrector_ruta_pensamiento.py
corregir_pca.py
limpiar_db.py
mantener_sistema.py
```

La mayoría probablemente **no funcionen** con el sistema judicial nuevo.

#### **Archivos de setup/inicialización antiguos**:

```
iniciar_sistema.py
setup_prompt_environment.py
servidor_flask_simplificado.py
```

Probablemente obsoletos, **la webapp principal es end2end_webapp.py**.

---

## 📋 PLAN DE ACCIÓN RECOMENDADO

### **Opción A: Limpieza Agresiva (Recomendada)**

Eliminar TODO en `/App_colaborativa/*.py` EXCEPTO:
- `limpiar_sistema_autores.py` (script útil)
- `integrar_sistema_judicial.py` (script útil)

**Razón**: Todo lo importante está en `/colaborative/scripts/`

### **Opción B: Limpieza Conservadora**

Eliminar solo archivos con "autor" en el nombre y mantener utilidades genéricas.

### **Opción C: Evaluación Manual**

Revisar archivo por archivo (tedioso, ~90 archivos).

---

## 🚀 SCRIPT DE LIMPIEZA AGRESIVA

Voy a crear un script que limpia TODO excepto lo esencial.

---

## 📁 ESTRUCTURA FINAL IDEAL

```
sentency/
├── README.md                          ✅ Principal
├── PLAN_MIGRACION_SISTEMA_JUDICIAL.md ✅
├── LIMPIEZA_FINAL.md                  ✅ Este archivo
│
└── App_colaborativa/
    ├── [DOCS]:
    │   ├── PROPUESTA_AJUSTADA_JUECES_ARG.md
    │   ├── FASE1_README.md
    │   ├── FASE2_README.md
    │   ├── FASE3_README.md
    │   ├── FASE4_README.md
    │   └── FASE5_README.md
    │
    ├── [SCRIPTS UTILIDAD - OPCIONAL]:
    │   ├── limpiar_sistema_autores.py
    │   └── integrar_sistema_judicial.py
    │
    └── colaborative/
        ├── bases_rag/cognitiva/
        │   ├── juez_centrico_arg.db       ⚖️ Única BD
        │   ├── metadatos.db
        │   └── modelos_predictivos/
        │
        └── scripts/
            ├── [CORE - 8 archivos]
            ├── [JUDICIAL - 15 archivos]
            └── [UTILIDADES - necesarias]
```

---

## ⚠️ CUIDADO CON

### **NO eliminar**:
- `colaborative/` - Todo el directorio
- `*.md` - Documentación
- Scripts que creamos hoy (limpiar_sistema_autores.py, integrar_sistema_judicial.py)

### **SÍ eliminar**:
- Cualquier `.py` en `/App_colaborativa/` que mencione "autor"
- Scripts de diagnóstico antiguos
- Scripts de mantenimiento antiguos
- Servidores Flask antiguos (solo usar end2end_webapp.py)

---

## 🎯 DECISIÓN REQUERIDA

**¿Qué prefieres?**

1. **Limpieza Agresiva** - Elimino ~85 archivos del directorio raíz, dejo solo lo esencial
2. **Limpieza Moderada** - Elimino ~30 archivos específicos de autores, mantengo utilidades
3. **Limpieza Manual** - Te muestro lista y decides uno por uno

**Recomendación**: Opción 1 (Agresiva) - Más limpio, menos confuso, todo lo importante está en `scripts/`
