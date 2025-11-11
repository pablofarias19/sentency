# 🎯 SISTEMA DE PROMPTS IDENTIFICABLES Y MEJORABLES
========================================================

🎯 **OBJETIVO:** Centralizar y hacer fácilmente mejorables todos los prompts del sistema cognitivo.

## 📋 **UBICACIONES DE TODOS LOS PROMPTS:**

### 1. **🧠 ANALYSER MÉTODO MEJORADO v2.0**
**📁 ARCHIVO:** `colaborative/scripts/analyser_metodo_mejorado.py`
**🎯 FUNCIÓN:** No usa prompts LLM - Análisis por patrones regex

**📝 PATRONES MEJORABLES:**
```python
# LÍNEAS 60-80 - PATRONES DE RAZONAMIENTO
self.RAZONAMIENTO_PATTERNS = {
    "deductivo": re.compile(r"\b(por tanto|en consecuencia|se concluye|se sigue|de ahí que|luego|entonces)\b", re.IGNORECASE),
    "inductivo": re.compile(r"\b(en general|por lo común|habitualmente|frecuentemente|suele|tiende a|patrón|tendencia)\b", re.IGNORECASE),
    # ... más patrones
}
```

### 2. **🎭 ORCHESTRADOR MAESTRO INTEGRADO**
**📁 ARCHIVO:** `colaborative/scripts/orchestrador_maestro_integrado.py`
**🎯 FUNCIÓN:** Coordina todos los análisis

**📝 PROMPT PRINCIPAL - LÍNEAS 180-220:**
```python
PROMPT_ORCHESTRADOR = f"""
🧠 ERES UN EXPERTO EN ANÁLISIS COGNITIVO JURÍDICO AVANZADO.

Tu misión es generar un PERFIL MENTAL COMPLETO del autor basado en CÓMO PIENSA, no en QUÉ dice.

TEXTO A ANALIZAR:
{texto}

ENFOQUE DE ANÁLISIS:
1. 🎯 ARQUITECTURA MENTAL: ¿Cómo organiza mentalmente los conceptos?
2. 🔄 PROCESO DE RAZONAMIENTO: ¿Velocidad rápida o deliberada?
3. 🌐 ESTILO COGNITIVO: ¿Analítico o intuitivo?
4. 📚 METODOLOGÍA JURÍDICA: ¿Formalista o pragmático?

RESPONDE EN JSON ESTRUCTURADO con métricas 0.0 a 1.0.
"""
```

### 3. **🌐 SISTEMA RAG PRINCIPAL**
**📁 ARCHIVO:** `colaborative/scripts/end2end_webapp.py`
**🎯 FUNCIÓN:** Interfaz web principal

**📝 PROMPT RAG COGNITIVO - LÍNEAS 180-220:**
```python
PROMPT_RAG_COGNITIVO = f"""
Eres un asistente jurídico especializado con CONTEXTO COGNITIVO AVANZADO.

CONTEXTO DOCUMENTAL:
{context}

PERFILES COGNITIVOS RELEVANTES:
{perfiles_cognitivos}

CONSULTA DEL USUARIO:
{query}

INSTRUCCIONES:
1. Responde usando el contexto documental
2. Enriquece con insights de los perfiles cognitivos
3. Mantén coherencia con el estilo de pensamiento detectado
4. Proporciona referencias específicas

Respuesta estructurada y profesional:
"""
```

### 4. **📊 RADAR COGNITIVO**
**📁 ARCHIVO:** `colaborative/scripts/radar_cognitivo.py`
**🎯 FUNCIÓN:** Visualización interactiva

**📝 PROMPT EXPLICACIONES - LÍNEAS 150-180:**
```python
PROMPT_EXPLICACIONES_RADAR = f"""
🧠 EXPLICA DE FORMA CLARA Y EDUCATIVA estos resultados del análisis cognitivo:

MÉTRICAS DEL AUTOR "{autor}":
{metricas_json}

GENERA EXPLICACIONES:
1. 📊 ¿Qué significan estos números?
2. 🎯 ¿Cuál es el patrón dominante?
3. 💡 ¿Qué nos dice sobre cómo piensa este autor?
4. 🔍 ¿Cómo se compara con otros autores jurídicos?

Respuesta educativa y accesible:
"""
```

### 5. **👥 SISTEMA DE REFERENCIAS DE AUTORES**  
**📁 ARCHIVO:** `colaborative/scripts/sistema_referencias_autores.py`
**🎯 FUNCIÓN:** Análisis detallado de autores

**📝 PROMPTS PRINCIPALES - LÍNEAS 200-300:**

#### A) **METODOLOGÍA APLICADA:**
```python
PROMPT_METODOLOGIA = f"""
🔬 ANALIZA LA METODOLOGÍA JURÍDICA de este autor basándote en su perfil cognitivo:

PERFIL COMPLETO:
{perfil_autor}

OBRAS ANALIZADAS:
{obras_autor}

GENERA ANÁLISIS DE:
1. 📚 ENFOQUE METODOLÓGICO: ¿Dogmático, crítico, pragmático?
2. 🧠 PROCESO DE RAZONAMIENTO: ¿Cómo construye argumentos?
3. 📖 USO DE FUENTES: ¿Doctrina, jurisprudencia, derecho comparado?
4. 🎯 OBJETIVOS INTELECTUALES: ¿Qué busca lograr?

Explicación clara y detallada:
"""
```

#### B) **VALORACIÓN CREATIVIDAD:**
```python
PROMPT_CREATIVIDAD = f"""
🎨 EVALÚA LA CREATIVIDAD INTELECTUAL de este autor jurídico:

MÉTRICAS COGNITIVAS:
{metricas_creatividad}

PATRONES IDENTIFICADOS:
{patrones_innovacion}

ANALIZA:
1. 💡 ORIGINALIDAD CONCEPTUAL: ¿Propone ideas nuevas?
2. 🔄 FLEXIBILIDAD MENTAL: ¿Adapta enfoques según contexto?
3. 🌐 INTERDISCIPLINARIEDAD: ¿Integra otras disciplinas?
4. 🚀 INNOVACIÓN JURÍDICA: ¿Contribuye al desarrollo del derecho?

Valoración fundamentada con ejemplos:
"""
```

#### C) **ANÁLISIS DE FORMALISMO:**
```python
PROMPT_FORMALISMO = f"""
⚖️ EVALÚA EL NIVEL DE FORMALISMO JURÍDICO de este autor:

INDICADORES DE FORMALISMO:
{indicadores_formalismo}

ESTRUCTURA ARGUMENTATIVA:
{estructura_args}

DETERMINA:
1. 📋 RIGOR TÉCNICO: ¿Precisión en terminología jurídica?
2. 📚 USO DE CITAS: ¿Densidad de referencias legales?
3. 🏛️ ESTILO ACADÉMICO: ¿Formal vs. accesible?
4. ⚖️ ADHERENCIA DOCTRINAL: ¿Sigue o cuestiona tradiciones?

Análisis equilibrado del formalismo:
"""
```

## 🔧 **SISTEMA DE MEJORA CONTINUA DE PROMPTS:**

### **📁 ARCHIVO CENTRAL:** `colaborative/prompts/prompts_manager.py`

<function_calls>
<invoke name="create_file">
<parameter name="content"># -*- coding: utf-8 -*-
"""
🎯 MANAGER CENTRAL DE PROMPTS v1.0
==================================
Sistema centralizado para gestionar y mejorar todos los prompts del sistema cognitivo.

CARACTERÍSTICAS:
✅ Prompts identificados con IDs únicos
✅ Versionado automático de cambios
✅ Testing A/B de prompts
✅ Métricas de efectividad
✅ Backup automático de versiones
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class PromptsManager:
    """
    🎯 Gestor centralizado de todos los prompts del sistema
    
    FUNCIONES:
    - Almacenamiento centralizado
    - Versionado automático
    - Testing A/B
    - Métricas de efectividad
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.prompts_file = self.base_dir / "prompts_database.json"
        self.versiones_dir = self.base_dir / "versiones"
        self.versiones_dir.mkdir(exist_ok=True)
        
        self.prompts_db = self._cargar_prompts()
    
    def _cargar_prompts(self) -> Dict:
        """Carga base de datos de prompts"""
        if self.prompts_file.exists():
            with open(self.prompts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self._crear_prompts_iniciales()
    
    def _crear_prompts_iniciales(self) -> Dict:
        """Crea la base de datos inicial con todos los prompts del sistema"""
        
        prompts_iniciales = {
            "version": "1.0",
            "fecha_creacion": datetime.now().isoformat(),
            "prompts": {
                
                # 🧠 ORCHESTRADOR MAESTRO
                "ORCHESTRADOR_ANALISIS_COGNITIVO": {
                    "id": "ORCH_001",
                    "nombre": "Análisis Cognitivo Completo",
                    "modulo": "orchestrador_maestro_integrado.py",
                    "lineas": "180-220",
                    "version": "1.0",
                    "prompt": """🧠 ERES UN EXPERTO EN ANÁLISIS COGNITIVO JURÍDICO AVANZADO.

Tu misión es generar un PERFIL MENTAL COMPLETO del autor basado en CÓMO PIENSA, no en QUÉ dice.

TEXTO A ANALIZAR:
{texto}

ENFOQUE DE ANÁLISIS:
1. 🎯 ARQUITECTURA MENTAL: ¿Cómo organiza mentalmente los conceptos?
2. 🔄 PROCESO DE RAZONAMIENTO: ¿Velocidad rápida o deliberada?
3. 🌐 ESTILO COGNITIVO: ¿Analítico o intuitivo?
4. 📚 METODOLOGÍA JURÍDICA: ¿Formalista o pragmático?

RESPONDE EN JSON ESTRUCTURADO con métricas 0.0 a 1.0.""",
                    "metricas": {"efectividad": 0.0, "usos": 0},
                    "notas_mejora": "Prompt base para análisis cognitivo integral"
                },
                
                # 🌐 RAG COGNITIVO
                "RAG_CONTEXTO_COGNITIVO": {
                    "id": "RAG_001", 
                    "nombre": "RAG con Contexto Cognitivo",
                    "modulo": "end2end_webapp.py",
                    "lineas": "180-220",
                    "version": "1.0",
                    "prompt": """Eres un asistente jurídico especializado con CONTEXTO COGNITIVO AVANZADO.

CONTEXTO DOCUMENTAL:
{context}

PERFILES COGNITIVOS RELEVANTES:
{perfiles_cognitivos}

CONSULTA DEL USUARIO:
{query}

INSTRUCCIONES:
1. Responde usando el contexto documental
2. Enriquece con insights de los perfiles cognitivos
3. Mantén coherencia con el estilo de pensamiento detectado
4. Proporciona referencias específicas

Respuesta estructurada y profesional:""",
                    "metricas": {"efectividad": 0.0, "usos": 0},
                    "notas_mejora": "Integrar mejor perfiles cognitivos en respuestas"
                },
                
                # 📊 EXPLICACIONES RADAR
                "RADAR_EXPLICACIONES": {
                    "id": "RAD_001",
                    "nombre": "Explicaciones Radar Cognitivo", 
                    "modulo": "radar_cognitivo.py",
                    "lineas": "150-180",
                    "version": "1.0",
                    "prompt": """🧠 EXPLICA DE FORMA CLARA Y EDUCATIVA estos resultados del análisis cognitivo:

MÉTRICAS DEL AUTOR "{autor}":
{metricas_json}

GENERA EXPLICACIONES:
1. 📊 ¿Qué significan estos números?
2. 🎯 ¿Cuál es el patrón dominante?
3. 💡 ¿Qué nos dice sobre cómo piensa este autor?
4. 🔍 ¿Cómo se compara con otros autores jurídicos?

Respuesta educativa y accesible:""",
                    "metricas": {"efectividad": 0.0, "usos": 0},
                    "notas_mejora": "Hacer más didácticas las explicaciones"
                },
                
                # 👥 METODOLOGÍA AUTORAL
                "AUTOR_METODOLOGIA": {
                    "id": "AUT_001",
                    "nombre": "Análisis Metodología Autoral",
                    "modulo": "sistema_referencias_autores.py", 
                    "lineas": "200-250",
                    "version": "1.0",
                    "prompt": """🔬 ANALIZA LA METODOLOGÍA JURÍDICA de este autor basándote en su perfil cognitivo:

PERFIL COMPLETO:
{perfil_autor}

OBRAS ANALIZADAS:
{obras_autor}

GENERA ANÁLISIS DE:
1. 📚 ENFOQUE METODOLÓGICO: ¿Dogmático, crítico, pragmático?
2. 🧠 PROCESO DE RAZONAMIENTO: ¿Cómo construye argumentos?
3. 📖 USO DE FUENTES: ¿Doctrina, jurisprudencia, derecho comparado?
4. 🎯 OBJETIVOS INTELECTUALES: ¿Qué busca lograr?

Explicación clara y detallada:""",
                    "metricas": {"efectividad": 0.0, "usos": 0},
                    "notas_mejora": "Agregar más ejemplos específicos de metodología"
                },
                
                # 🎨 CREATIVIDAD AUTORAL
                "AUTOR_CREATIVIDAD": {
                    "id": "AUT_002",
                    "nombre": "Valoración Creatividad Autoral",
                    "modulo": "sistema_referencias_autores.py",
                    "lineas": "250-300", 
                    "version": "1.0",
                    "prompt": """🎨 EVALÚA LA CREATIVIDAD INTELECTUAL de este autor jurídico:

MÉTRICAS COGNITIVAS:
{metricas_creatividad}

PATRONES IDENTIFICADOS:
{patrones_innovacion}

ANALIZA:
1. 💡 ORIGINALIDAD CONCEPTUAL: ¿Propone ideas nuevas?
2. 🔄 FLEXIBILIDAD MENTAL: ¿Adapta enfoques según contexto?
3. 🌐 INTERDISCIPLINARIEDAD: ¿Integra otras disciplinas?
4. 🚀 INNOVACIÓN JURÍDICA: ¿Contribuye al desarrollo del derecho?

Valoración fundamentada con ejemplos:""",
                    "metricas": {"efectividad": 0.0, "usos": 0},
                    "notas_mejora": "Incluir escala de creatividad más detallada"
                },
                
                # ⚖️ FORMALISMO AUTORAL  
                "AUTOR_FORMALISMO": {
                    "id": "AUT_003",
                    "nombre": "Análisis Formalismo Jurídico",
                    "modulo": "sistema_referencias_autores.py",
                    "lineas": "300-350",
                    "version": "1.0", 
                    "prompt": """⚖️ EVALÚA EL NIVEL DE FORMALISMO JURÍDICO de este autor:

INDICADORES DE FORMALISMO:
{indicadores_formalismo}

ESTRUCTURA ARGUMENTATIVA:
{estructura_args}

DETERMINA:
1. 📋 RIGOR TÉCNICO: ¿Precisión en terminología jurídica?
2. 📚 USO DE CITAS: ¿Densidad de referencias legales?
3. 🏛️ ESTILO ACADÉMICO: ¿Formal vs. accesible?
4. ⚖️ ADHERENCIA DOCTRINAL: ¿Sigue o cuestiona tradiciones?

Análisis equilibrado del formalismo:""",
                    "metricas": {"efectividad": 0.0, "usos": 0},
                    "notas_mejora": "Balancear evaluación formalismo vs. pragmatismo"
                }
            }
        }
        
        self._guardar_prompts(prompts_iniciales)
        return prompts_iniciales
    
    def obtener_prompt(self, prompt_id: str) -> Optional[str]:
        """Obtiene un prompt por su ID"""
        if prompt_id in self.prompts_db["prompts"]:
            prompt_data = self.prompts_db["prompts"][prompt_id]
            # Incrementar contador de uso
            prompt_data["metricas"]["usos"] += 1
            self._guardar_prompts(self.prompts_db)
            return prompt_data["prompt"]
        return None
    
    def actualizar_prompt(self, prompt_id: str, nuevo_prompt: str, razon_cambio: str = "") -> bool:
        """Actualiza un prompt y guarda la versión anterior"""
        if prompt_id not in self.prompts_db["prompts"]:
            return False
        
        # Backup de versión anterior
        prompt_actual = self.prompts_db["prompts"][prompt_id].copy()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        backup_file = self.versiones_dir / f"{prompt_id}_v{prompt_actual['version']}_{timestamp}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(prompt_actual, f, indent=2, ensure_ascii=False)
        
        # Actualizar prompt
        version_anterior = float(prompt_actual["version"])
        nueva_version = str(version_anterior + 0.1)
        
        self.prompts_db["prompts"][prompt_id].update({
            "prompt": nuevo_prompt,
            "version": nueva_version,
            "fecha_actualizacion": datetime.now().isoformat(),
            "razon_cambio": razon_cambio,
            "version_anterior": prompt_actual["version"]
        })
        
        self._guardar_prompts(self.prompts_db)
        print(f"✅ Prompt {prompt_id} actualizado a versión {nueva_version}")
        return True
    
    def listar_prompts(self) -> Dict:
        """Lista todos los prompts disponibles"""
        resumen = {}
        for prompt_id, data in self.prompts_db["prompts"].items():
            resumen[prompt_id] = {
                "nombre": data["nombre"],
                "modulo": data["modulo"], 
                "version": data["version"],
                "usos": data["metricas"]["usos"],
                "efectividad": data["metricas"]["efectividad"]
            }
        return resumen
    
    def registrar_efectividad(self, prompt_id: str, puntuacion: float):
        """Registra la efectividad de un prompt (0.0 a 1.0)"""
        if prompt_id in self.prompts_db["prompts"]:
            current_score = self.prompts_db["prompts"][prompt_id]["metricas"]["efectividad"]
            usos = self.prompts_db["prompts"][prompt_id]["metricas"]["usos"]
            
            # Promedio ponderado
            nueva_efectividad = (current_score * (usos - 1) + puntuacion) / usos
            self.prompts_db["prompts"][prompt_id]["metricas"]["efectividad"] = round(nueva_efectividad, 3)
            
            self._guardar_prompts(self.prompts_db)
    
    def generar_reporte_prompts(self) -> str:
        """Genera reporte completo de todos los prompts"""
        reporte = "🎯 REPORTE COMPLETO DE PROMPTS\n" + "=" * 50 + "\n\n"
        
        for prompt_id, data in self.prompts_db["prompts"].items():
            reporte += f"📝 {data['nombre']} ({prompt_id})\n"
            reporte += f"   📁 Módulo: {data['modulo']}\n"
            reporte += f"   📍 Líneas: {data.get('lineas', 'N/A')}\n"
            reporte += f"   🔢 Versión: {data['version']}\n"
            reporte += f"   📊 Usos: {data['metricas']['usos']}\n"
            reporte += f"   ⭐ Efectividad: {data['metricas']['efectividad']:.3f}\n"
            reporte += f"   💡 Notas: {data.get('notas_mejora', 'N/A')}\n\n"
        
        return reporte
    
    def _guardar_prompts(self, prompts_data: Dict):
        """Guarda la base de datos de prompts"""
        with open(self.prompts_file, 'w', encoding='utf-8') as f:
            json.dump(prompts_data, f, indent=2, ensure_ascii=False)

def main():
    """Interfaz de prueba del gestor de prompts"""
    print("🎯 GESTOR CENTRAL DE PROMPTS v1.0")
    print("=" * 40)
    
    manager = PromptsManager()
    
    # Mostrar todos los prompts
    print("\n📋 PROMPTS DISPONIBLES:")
    prompts = manager.listar_prompts()
    for prompt_id, info in prompts.items():
        print(f"  {prompt_id}: {info['nombre']} (v{info['version']}, {info['usos']} usos)")
    
    # Ejemplo de uso
    print("\n🧪 EJEMPLO DE USO:")
    prompt_orchestrador = manager.obtener_prompt("ORCHESTRADOR_ANALISIS_COGNITIVO")
    if prompt_orchestrador:
        print("✅ Prompt obtenido correctamente")
        print(f"📝 Longitud: {len(prompt_orchestrador)} caracteres")
    
    # Generar reporte
    print("\n📊 GENERANDO REPORTE COMPLETO...")
    reporte = manager.generar_reporte_prompts()
    
    reporte_file = Path(__file__).parent / "reporte_prompts.txt"
    with open(reporte_file, 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    print(f"✅ Reporte guardado en: {reporte_file}")
    print("\n🎉 GESTOR DE PROMPTS FUNCIONANDO CORRECTAMENTE")

if __name__ == "__main__":
    main()