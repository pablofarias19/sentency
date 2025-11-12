# 🤖 GUÍA: Generador de Informes Judiciales con IA

## 📋 ¿Qué hace este sistema?

Genera **informes académicos profundos** sobre jueces argentinos usando IA generativa (Gemini/GPT/Claude).

### Diferencias con el generador estándar:

| Característica | `generador_informes_judicial.py` | `generador_informes_gemini_judicial.py` |
|---|---|---|
| **Tipo** | Plantillas estructuradas | **IA generativa** |
| **Narrativa** | ❌ No | ✅ **Sí** (800-1200 palabras) |
| **Citas textuales** | ❌ No | ✅ **Sí** (fragmentos reales) |
| **Análisis cualitativo** | ❌ Limitado | ✅ **Profundo** |
| **Gráfico radar** | ❌ No | ✅ **Sí** (interactivo) |
| **Formato** | TXT/JSON/MD | **HTML/MD/TXT** |

---

## 🚀 INSTALACIÓN Y CONFIGURACIÓN

### **Paso 1: Instalar dependencias**

```bash
# Elige según la IA que usarás:

# Opción A: Gemini (Google)
pip install google-generativeai matplotlib

# Opción B: OpenAI (GPT)
pip install openai matplotlib

# Opción C: Claude (Anthropic)
pip install anthropic matplotlib
```

### **Paso 2: Obtener API Key**

**Gemini (Recomendado - Gratis):**
1. Ve a: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copia la key

**OpenAI (GPT):**
1. Ve a: https://platform.openai.com/api-keys
2. Crea una key (requiere pago)

**Anthropic (Claude):**
1. Ve a: https://console.anthropic.com/
2. Crea una key (requiere pago)

### **Paso 3: Configurar API Key**

**En Windows (PowerShell):**
```powershell
# Temporal (solo esta sesión)
$env:GEMINI_API_KEY = "tu-api-key-aqui"

# Permanente (usuario actual)
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'tu-api-key-aqui', 'User')
```

**En Linux/Mac:**
```bash
# Temporal
export GEMINI_API_KEY="tu-api-key-aqui"

# Permanente (agregar a ~/.bashrc o ~/.zshrc)
echo 'export GEMINI_API_KEY="tu-api-key-aqui"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📖 USO BÁSICO

### **Comando Simple**

```bash
cd "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL\App_colaborativa\colaborative\scripts"

python generador_informes_gemini_judicial.py "Ricardo Lorenzetti"
```

**Salida:**
- `informe_ia_Ricardo_Lorenzetti_20251112_143022.html` → Informe completo HTML
- `radar_Ricardo_Lorenzetti_20251112_143022.png` → Gráfico visual

---

## 🎯 EJEMPLOS DE USO

### **1. Informe HTML con Gemini (Default)**
```bash
python generador_informes_gemini_judicial.py "Ricardo Lorenzetti"
```

### **2. Informe Markdown**
```bash
python generador_informes_gemini_judicial.py "Elena Highton" --formato md
```

### **3. Usar OpenAI en lugar de Gemini**
```bash
# Configurar OpenAI
export OPENAI_API_KEY="tu-key"

python generador_informes_gemini_judicial.py "Juan Pérez" --api openai --formato html
```

### **4. Usar Claude (Anthropic)**
```bash
export ANTHROPIC_API_KEY="tu-key"

python generador_informes_gemini_judicial.py "María González" --api anthropic
```

---

## 📄 CONTENIDO DEL INFORME

El informe generado incluye:

### **1. Perfil Visual (Gráfico Radar)**
- Activismo judicial
- Innovación jurídica
- Protección de derechos
- Garantismo
- Control constitucional
- Interpretación expansiva

### **2. Métricas Clave**
- Activismo judicial (-1 a +1)
- Protección derechos (0-1)
- Formalismo (-1 a +1)
- Innovación jurídica (0-1)
- Sesgos argentinos

### **3. Análisis Narrativo con IA (800-1200 palabras)**

#### 3.1 Introducción al Perfil Judicial
- Contexto institucional del juez
- Posicionamiento en espectro judicial argentino

#### 3.2 Análisis del Pensamiento Judicial
- **Activismo y Formalismo** (con citas textuales)
- **Metodología Interpretativa** (literal/sistemática/teleológica)
- **Protección de Derechos** (qué derechos prioriza)

#### 3.3 Líneas Jurisprudenciales
- Líneas consolidadas identificadas
- Consistencia y predictibilidad
- Criterios dominantes

#### 3.4 Sesgos y Orientación Ideológica
- Pro-trabajador, pro-consumidor, garantista
- Contextualización en panorama argentino

#### 3.5 Posicionamiento Comparativo
- Ubicación en espectro judicial
- Perfil único o distintivo

### **4. Fragmentos Textuales Analizados**
- Considerandos clave de sentencias reales
- Fundamentos jurídicos
- Citas directas del juez

---

## 🎨 FORMATOS DE SALIDA

### **HTML (Recomendado)**
```bash
python generador_informes_gemini_judicial.py "Juez" --formato html
```

**Características:**
- ✅ Diseño profesional con CSS
- ✅ Gráfico radar embebido
- ✅ Métricas visuales
- ✅ Fragmentos destacados
- ✅ Listo para imprimir o compartir

**Abrir con:** Navegador web

---

### **Markdown**
```bash
python generador_informes_gemini_judicial.py "Juez" --formato md
```

**Características:**
- ✅ Formato legible en texto plano
- ✅ Compatible con GitHub, GitLab, etc.
- ✅ Fácil de convertir a PDF/DOCX

**Abrir con:** Editor de texto, VS Code, Obsidian

---

### **TXT (Texto Plano)**
```bash
python generador_informes_gemini_judicial.py "Juez" --formato txt
```

**Características:**
- ✅ Sin formato, solo texto
- ✅ Compatible con cualquier programa

---

## 🔧 OPCIONES AVANZADAS

### **Elegir API específica**

```bash
# Auto-detectar (default)
python generador_informes_gemini_judicial.py "Juez"

# Forzar Gemini
python generador_informes_gemini_judicial.py "Juez" --api gemini

# Forzar OpenAI
python generador_informes_gemini_judicial.py "Juez" --api openai

# Forzar Claude
python generador_informes_gemini_judicial.py "Juez" --api anthropic
```

### **Múltiples jueces**

```bash
# Generar para varios jueces
python generador_informes_gemini_judicial.py "Ricardo Lorenzetti"
python generador_informes_gemini_judicial.py "Elena Highton"
python generador_informes_gemini_judicial.py "Carlos Rosenkrantz"
```

---

## 📊 EJEMPLO DE SALIDA

### **Archivo HTML generado:**

```
informe_ia_Ricardo_Lorenzetti_20251112_143022.html
```

**Contenido:**
- Portada con metadata
- Gráfico radar interactivo
- 6 métricas clave visuales
- Informe narrativo de 1000+ palabras
- 5 fragmentos textuales citados
- Footer con información del sistema

**Peso:** ~200-500 KB

---

## 🎯 FLUJO COMPLETO DE USO

```bash
# 1. Configurar API (una sola vez)
export GEMINI_API_KEY="tu-key"

# 2. Navegar a scripts
cd "ruta/a/scripts"

# 3. Generar informe
python generador_informes_gemini_judicial.py "Ricardo Lorenzetti" --formato html

# 4. Abrir resultado
# Se genera en: ../informes_ia_generados/informe_ia_Ricardo_Lorenzetti_TIMESTAMP.html
```

**Resultado:**
```
✓ Recopilando datos del juez...
✓ Extrayendo fragmentos textuales de sentencias...
✓ 12 fragmentos extraídos
✓ Construyendo prompt especializado...
✓ Generando informe con GEMINI...
✓ Informe generado: 1247 caracteres
✓ Gráfico guardado: radar_Ricardo_Lorenzetti_20251112_143022.png
✓ Ensamblando informe final...

═══════════════════════════════════════════════════════════
✓ INFORME GENERADO EXITOSAMENTE
═══════════════════════════════════════════════════════════

📁 Ubicación: ../informes_ia_generados/informe_ia_Ricardo_Lorenzetti_20251112_143022.html
📊 Gráfico: ../informes_ia_generados/radar_Ricardo_Lorenzetti_20251112_143022.png
```

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### **Error: "No hay APIs de IA configuradas"**

**Solución:**
```bash
# Verificar si la variable está configurada
echo $GEMINI_API_KEY  # Linux/Mac
echo $env:GEMINI_API_KEY  # Windows PowerShell

# Si está vacía, configurar:
export GEMINI_API_KEY="tu-key-aqui"
```

---

### **Error: "No module named 'google.generativeai'"**

**Solución:**
```bash
pip install google-generativeai
```

---

### **Error: "No se encontró perfil para X"**

**Solución:**
Primero debes ingestar sentencias del juez:
```bash
python ingesta_sentencias_judicial.py --ruta "C:\sentencias" --juez "Nombre del Juez"
python procesador_sentencias_completo.py --juez "Nombre del Juez"
```

---

### **Error: "matplotlib no instalado"**

**Solución:**
```bash
pip install matplotlib
```

El gráfico se omitirá si matplotlib no está disponible, pero el informe se generará igual.

---

### **No hay fragmentos textuales**

**Causa:** Las sentencias no tienen texto completo en la BD.

**Solución:**
El informe se generará solo con métricas cuantitativas. Para incluir fragmentos:
1. Asegúrate de que los PDFs se procesaron correctamente
2. Verifica que `texto_completo` no esté vacío en la BD

---

## 💰 COSTOS ESTIMADOS

### **Gemini (Google)**
- **Modelo:** gemini-1.5-flash
- **Costo:** GRATIS hasta 1500 requests/día
- **Por informe:** ~$0.00

### **OpenAI (GPT)**
- **Modelo:** gpt-4o-mini
- **Costo:** ~$0.15 por 1M tokens entrada, $0.60 por 1M salida
- **Por informe:** ~$0.01-0.03

### **Anthropic (Claude)**
- **Modelo:** claude-3-haiku-20240307
- **Costo:** ~$0.25 por 1M tokens entrada, $1.25 por 1M salida
- **Por informe:** ~$0.02-0.05

**Recomendación:** Usa Gemini (gratis y muy bueno).

---

## 📈 COMPARACIÓN DE MODELOS

| Modelo | Costo | Velocidad | Calidad | Límite |
|--------|-------|-----------|---------|--------|
| **Gemini 1.5 Flash** | 🟢 Gratis | ⚡ Rápido | ⭐⭐⭐⭐ | 1500/día |
| GPT-4o-mini | 🟡 Bajo | ⚡ Rápido | ⭐⭐⭐⭐ | Según pago |
| Claude 3 Haiku | 🟡 Bajo | ⚡⚡ Muy rápido | ⭐⭐⭐⭐ | Según pago |

---

## 🎓 CASOS DE USO

### **1. Análisis Pre-Litigación**
```bash
# Antes de litigar, analiza al juez asignado
python generador_informes_gemini_judicial.py "Juez Asignado" --formato html
```

**Te ayuda a:**
- Conocer sus sesgos (pro-trabajador, garantista, etc.)
- Identificar líneas jurisprudenciales consolidadas
- Predecir su postura en tu caso

---

### **2. Investigación Académica**
```bash
# Generar informes de múltiples jueces para estudio comparativo
python generador_informes_gemini_judicial.py "Lorenzetti" --formato md
python generador_informes_gemini_judicial.py "Highton" --formato md
python generador_informes_gemini_judicial.py "Maqueda" --formato md
```

---

### **3. Due Diligence Judicial**
```bash
# Para firmas de abogados: perfilar jueces del tribunal
python generador_informes_gemini_judicial.py "Juez 1" --formato html
python generador_informes_gemini_judicial.py "Juez 2" --formato html
```

---

## 📚 PRÓXIMOS PASOS

Después de generar el informe:

1. **Leer el informe HTML** → Abrir en navegador
2. **Analizar métricas clave** → Identificar patrones
3. **Revisar fragmentos citados** → Entender razonamiento
4. **Usar en estrategia legal** → Adaptar argumentación

---

## 🆘 AYUDA

**Documentación completa:** `README.md`

**Soporte:**
- Verifica variables de entorno
- Revisa que el juez tenga sentencias procesadas
- Asegúrate de tener las dependencias instaladas

---

## 🎉 ¡LISTO!

Ya puedes generar informes profundos con IA. Solo necesitas:

```bash
export GEMINI_API_KEY="tu-key"
python generador_informes_gemini_judicial.py "Nombre del Juez"
```

**Resultado:** Informe HTML de 800-1200 palabras con análisis profundo, citas textuales y gráfico radar. 🚀
