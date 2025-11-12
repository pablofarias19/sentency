# 🔄 GUÍA: Migrar Sistema Judicial al Repositorio Original

Esta guía te ayuda a llevar el sistema judicial desde este repositorio al ecosistema originario.

---

## 📋 ANTES DE EMPEZAR

### 1. Entender qué tienes ahora

**En este repositorio (sentency/):**
- ✅ Sistema judicial completo (Fases 1-5)
- ✅ Adaptador ANALYSER-Judicial
- ✅ Webapp con rutas judiciales
- ✅ Infraestructura RAG/embeddings/ANALYSER intacta
- ✅ 88 archivos obsoletos eliminados
- ✅ Solo 3 scripts de utilidad en raíz

**En tu repositorio original:**
- ❓ Sistema de autores (probablemente)
- ❓ Archivos que quieres conservar
- ❓ Configuraciones específicas

---

## 🎯 ESTRATEGIAS DE MIGRACIÓN

### **Opción A: Reemplazo Completo (Recomendada si el original es similar)**

Reemplaza todo el directorio `App_colaborativa/` del original con el de aquí.

**Ventajas:**
- ✅ Más simple
- ✅ Todo queda consistente
- ✅ No hay conflictos

**Desventajas:**
- ❌ Pierdes TODO lo que esté en el original

**Cuándo usar:**
- Si el original tiene la misma estructura
- Si no hay archivos únicos importantes en el original
- Si quieres empezar limpio

---

### **Opción B: Migración Selectiva (Recomendada si tienes archivos únicos)**

Copiar solo archivos específicos, manteniendo otros del original.

**Ventajas:**
- ✅ Control total sobre qué reemplazar
- ✅ Conservas archivos únicos del original
- ✅ Puedes hacer backup antes

**Desventajas:**
- ⚠️ Más manual
- ⚠️ Requiere conocer qué conservar

**Cuándo usar:**
- Si el original tiene archivos que no están aquí
- Si quieres conservar configuraciones específicas
- Si tienes datos únicos (bases de datos con info real)

---

### **Opción C: Fusión Git (Para usuarios avanzados)**

Usar git para fusionar ambos repositorios.

**Ventajas:**
- ✅ Historial de cambios completo
- ✅ Git resuelve conflictos
- ✅ Puedes revertir si algo sale mal

**Desventajas:**
- ⚠️ Requiere resolver conflictos manualmente
- ⚠️ Más complejo

**Cuándo usar:**
- Si ambos son repositorios git
- Si quieres mantener historial
- Si tienes experiencia con git

---

## 🚀 PROCEDIMIENTOS DETALLADOS

---

## **OPCIÓN A: Reemplazo Completo**

### Paso 1: Backup del original

```bash
# Ir a tu repositorio original
cd /ruta/a/tu/repositorio/original

# Crear backup completo
cp -r App_colaborativa App_colaborativa.backup_$(date +%Y%m%d)

# Verificar backup
ls -la | grep backup
```

### Paso 2: Eliminar el directorio actual

```bash
# CUIDADO: Esto borra todo App_colaborativa del original
rm -rf App_colaborativa
```

### Paso 3: Copiar el nuevo sistema

```bash
# Copiar desde este repositorio
cp -r /home/user/sentency/App_colaborativa .

# Verificar
ls -la App_colaborativa/
```

### Paso 4: Verificar y ajustar rutas

```bash
# Si tu original usa rutas diferentes, ajústalas
cd App_colaborativa/colaborative/scripts

# Revisar scripts que usan rutas absolutas
grep -r "/home/user/sentency" .
```

### Paso 5: Probar el sistema

```bash
# Inicializar BD
python inicializar_bd_judicial.py

# Probar webapp
python end2end_webapp.py
```

---

## **OPCIÓN B: Migración Selectiva**

### Paso 1: Identificar qué reemplazar

Ejecuta este script en tu repositorio ORIGINAL:

```bash
cd /ruta/a/tu/repositorio/original

# Listar archivos Python en raíz
ls -1 App_colaborativa/*.py > archivos_raiz_original.txt

# Listar archivos en scripts/
ls -1 App_colaborativa/colaborative/scripts/*.py > archivos_scripts_original.txt

# Ver qué tienes
cat archivos_raiz_original.txt
cat archivos_scripts_original.txt
```

### Paso 2: Crear plan de migración

```bash
# Desde ESTE repositorio, crear lista de archivos a copiar
cd /home/user/sentency
python crear_plan_migracion_selectiva.py /ruta/a/tu/original
```

(Script incluido más abajo)

### Paso 3: Eliminar archivos de autores del original

```bash
cd /ruta/a/tu/repositorio/original

# Usar el script de limpieza
cp /home/user/sentency/App_colaborativa/limpiar_sistema_autores.py App_colaborativa/
cd App_colaborativa
python limpiar_sistema_autores.py
```

### Paso 4: Copiar archivos judiciales nuevos

```bash
# Copiar scripts judiciales (Fases 1-5)
cp /home/user/sentency/App_colaborativa/colaborative/scripts/*judicial*.py \
   /ruta/a/tu/original/App_colaborativa/colaborative/scripts/

# Copiar adaptador
cp /home/user/sentency/App_colaborativa/colaborative/scripts/analyser_judicial_adapter.py \
   /ruta/a/tu/original/App_colaborativa/colaborative/scripts/

# Copiar schema SQL
cp /home/user/sentency/App_colaborativa/colaborative/scripts/schema_juez_centrico_arg.sql \
   /ruta/a/tu/original/App_colaborativa/colaborative/scripts/

# Copiar extractor metadata Argentina
cp /home/user/sentency/App_colaborativa/colaborative/scripts/extractor_metadata_argentina.py \
   /ruta/a/tu/original/App_colaborativa/colaborative/scripts/
```

### Paso 5: Actualizar webapp

```bash
# Copiar rutas judiciales
cp /home/user/sentency/App_colaborativa/colaborative/scripts/webapp_rutas_judicial.py \
   /ruta/a/tu/original/App_colaborativa/colaborative/scripts/

# Ejecutar integrador
cp /home/user/sentency/App_colaborativa/integrar_sistema_judicial.py \
   /ruta/a/tu/original/App_colaborativa/
cd /ruta/a/tu/original/App_colaborativa
python integrar_sistema_judicial.py
```

### Paso 6: Copiar documentación

```bash
# Copiar READMEs
cp /home/user/sentency/README.md /ruta/a/tu/original/
cp /home/user/sentency/App_colaborativa/FASE*_README.md /ruta/a/tu/original/App_colaborativa/
cp /home/user/sentency/PLAN_MIGRACION_SISTEMA_JUDICIAL.md /ruta/a/tu/original/
```

---

## **OPCIÓN C: Fusión Git**

### Prerequisito: Ambos deben ser repositorios git

### Paso 1: Agregar este repo como remote

```bash
cd /ruta/a/tu/repositorio/original

# Agregar este repositorio como remote
git remote add sistema-judicial /home/user/sentency

# Verificar
git remote -v
```

### Paso 2: Fetch de los cambios

```bash
# Traer cambios
git fetch sistema-judicial

# Ver ramas disponibles
git branch -r
```

### Paso 3: Crear rama de fusión

```bash
# Crear rama nueva para fusión
git checkout -b fusion-sistema-judicial

# Fusionar
git merge sistema-judicial/main --allow-unrelated-histories
```

### Paso 4: Resolver conflictos

```bash
# Ver conflictos
git status

# Resolver manualmente cada conflicto
# Editar archivos con conflictos
# Decidir qué conservar de cada versión

# Marcar como resuelto
git add <archivo_resuelto>

# Continuar merge
git commit -m "Fusionar sistema judicial con repositorio original"
```

### Paso 5: Verificar y hacer merge a main

```bash
# Probar que todo funciona
python App_colaborativa/colaborative/scripts/end2end_webapp.py

# Si todo OK, fusionar a main
git checkout main
git merge fusion-sistema-judicial
```

---

## 🛠️ SCRIPTS DE AYUDA

### Script 1: Comparar Repositorios

```bash
#!/bin/bash
# comparar_repositorios.sh

ESTE_REPO="/home/user/sentency"
ORIGINAL_REPO="$1"

if [ -z "$ORIGINAL_REPO" ]; then
    echo "Uso: $0 /ruta/al/repositorio/original"
    exit 1
fi

echo "Comparando repositorios..."
echo "ESTE: $ESTE_REPO"
echo "ORIGINAL: $ORIGINAL_REPO"
echo ""

echo "=== Archivos en ESTE repo pero NO en original ==="
diff -qr "$ESTE_REPO/App_colaborativa" "$ORIGINAL_REPO/App_colaborativa" | grep "Only in $ESTE_REPO"

echo ""
echo "=== Archivos en ORIGINAL pero NO en este ==="
diff -qr "$ESTE_REPO/App_colaborativa" "$ORIGINAL_REPO/App_colaborativa" | grep "Only in $ORIGINAL_REPO"

echo ""
echo "=== Archivos diferentes ==="
diff -qr "$ESTE_REPO/App_colaborativa" "$ORIGINAL_REPO/App_colaborativa" | grep "differ"
```

### Script 2: Listar Archivos Únicos del Original

```bash
#!/bin/bash
# listar_unicos_original.sh

ESTE_REPO="/home/user/sentency"
ORIGINAL_REPO="$1"

if [ -z "$ORIGINAL_REPO" ]; then
    echo "Uso: $0 /ruta/al/repositorio/original"
    exit 1
fi

echo "Archivos únicos en tu repositorio original:"
echo "=========================================="
echo ""

cd "$ORIGINAL_REPO/App_colaborativa/colaborative/scripts"
for archivo in *.py; do
    if [ ! -f "$ESTE_REPO/App_colaborativa/colaborative/scripts/$archivo" ]; then
        echo "  📄 $archivo"
    fi
done

echo ""
echo "Revisa estos archivos antes de reemplazar."
echo "Si son importantes, haz backup."
```

---

## ⚠️ CHECKLIST PRE-MIGRACIÓN

Antes de migrar, responde estas preguntas:

- [ ] ¿Tengo backup completo del repositorio original?
- [ ] ¿Hay archivos únicos en el original que debo conservar?
- [ ] ¿Hay bases de datos con información real que debo preservar?
- [ ] ¿El original tiene la misma estructura de directorios?
- [ ] ¿Hay configuraciones específicas (rutas, credenciales) a ajustar?
- [ ] ¿Tengo permisos de escritura en el directorio original?
- [ ] ¿He probado el sistema en este repo antes de migrar?

---

## 🔍 VERIFICACIÓN POST-MIGRACIÓN

Después de migrar, verifica:

```bash
cd /ruta/a/tu/repositorio/original

# 1. Verificar estructura
ls -la App_colaborativa/
ls -la App_colaborativa/colaborative/scripts/*judicial*.py

# 2. Verificar que no hay archivos de autores
ls -la App_colaborativa/colaborative/scripts/ | grep autor

# 3. Ejecutar script de verificación
python verificar_migracion_completa.py

# 4. Probar inicialización
cd App_colaborativa/colaborative/scripts
python inicializar_bd_judicial.py

# 5. Probar webapp
python end2end_webapp.py
```

---

## 🆘 PROBLEMAS COMUNES

### Problema: Rutas absolutas no funcionan

**Solución:**
```bash
# Buscar rutas absolutas
grep -r "/home/user/sentency" App_colaborativa/

# Reemplazar por rutas relativas o ajustar
sed -i 's|/home/user/sentency|/tu/nueva/ruta|g' archivo.py
```

### Problema: Bases de datos no se crean

**Solución:**
```bash
# Verificar permisos
ls -la App_colaborativa/colaborative/bases_rag/cognitiva/

# Dar permisos si es necesario
chmod 755 App_colaborativa/colaborative/bases_rag/cognitiva/

# Reintentar
python inicializar_bd_judicial.py
```

### Problema: Imports no funcionan

**Solución:**
```bash
# Verificar estructura de directorios
cd App_colaborativa/colaborative/scripts
ls -la

# Asegurarte que todos los archivos core están presentes
ls -la analyser*.py embeddings*.py chunker*.py
```

---

## 📞 SIGUIENTE PASO

**¿Qué opción prefieres?**

1. **Opción A (Reemplazo completo)** - Más simple, si el original es similar
2. **Opción B (Selectiva)** - Más control, si tienes archivos únicos
3. **Opción C (Git)** - Más profesional, si manejas git

Dime:
1. ¿Dónde está tu repositorio original? (ruta completa)
2. ¿Tiene archivos únicos que debes conservar?
3. ¿Qué opción prefieres?

Y te ayudo con los comandos exactos para tu caso.
