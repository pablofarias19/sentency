#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 GENERADOR DE INFORMES JUDICIALES CON IA (Gemini)
====================================================

Genera informes profundos sobre jueces argentinos usando IA generativa.

DIFERENCIAS CON generador_informes_judicial.py:
- Este usa IA (Gemini/GPT) para generar narrativa inteligente
- Extrae fragmentos textuales REALES de sentencias
- Genera análisis cualitativo profundo
- Incluye citas textuales directas del juez
- Crea gráficos radar interactivos

Uso:
    python generador_informes_gemini_judicial.py "Ricardo Lorenzetti"
    python generador_informes_gemini_judicial.py "Ricardo Lorenzetti" --modelo gemini --formato html

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
BASES_RAG_DIR = BASE_DIR / "bases_rag" / "cognitiva"
DB_FILE = BASES_RAG_DIR / "juez_centrico_arg.db"
INFORMES_DIR = BASE_DIR / "informes_ia_generados"
CHUNKS_DIR = BASES_RAG_DIR

# Crear directorio de informes
INFORMES_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# CONFIGURACIÓN DE APIs
# ============================================================================

# Prioridad de APIs (se usa la primera disponible)
API_CONFIG = {
    'gemini': {
        'env_var': 'GEMINI_API_KEY',
        'modelo_default': 'gemini-1.5-flash',
        'disponible': False
    },
    'openai': {
        'env_var': 'OPENAI_API_KEY',
        'modelo_default': 'gpt-4o-mini',
        'disponible': False
    },
    'anthropic': {
        'env_var': 'ANTHROPIC_API_KEY',
        'modelo_default': 'claude-3-haiku-20240307',
        'disponible': False
    }
}

# Detectar APIs disponibles
for api_name, config in API_CONFIG.items():
    if os.getenv(config['env_var']):
        config['disponible'] = True

# Colores
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg): print(f"{Colors.GREEN}✓ {msg}{Colors.ENDC}")
def print_error(msg): print(f"{Colors.RED}✗ {msg}{Colors.ENDC}")
def print_warning(msg): print(f"{Colors.YELLOW}⚠ {msg}{Colors.ENDC}")
def print_info(msg): print(f"{Colors.BLUE}ℹ {msg}{Colors.ENDC}")

# ============================================================================
# EXTRACTOR DE FRAGMENTOS TEXTUALES
# ============================================================================

class ExtractorFragmentosJudiciales:
    """Extrae fragmentos textuales relevantes de sentencias"""

    def __init__(self, db_path: Path = DB_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def extraer_fragmentos_juez(self, juez: str, max_fragmentos: int = 15) -> List[Dict]:
        """
        Extrae fragmentos representativos de las sentencias del juez

        Returns:
            Lista de dicts con: {'texto', 'sentencia_id', 'contexto', 'tipo'}
        """
        print_info(f"Extrayendo fragmentos textuales de {juez}...")

        # Obtener sentencias con texto completo
        self.cursor.execute("""
        SELECT sentencia_id, texto_completo, caratula, fecha, materia, ruta_chunks
        FROM sentencias_por_juez_arg
        WHERE juez = ? AND texto_completo IS NOT NULL
        ORDER BY fecha DESC
        LIMIT 10
        """, (juez,))

        sentencias = self.cursor.fetchall()

        if not sentencias:
            print_warning("No se encontró texto completo de sentencias")
            return []

        fragmentos = []

        for sent_id, texto, caratula, fecha, materia, ruta_chunks in sentencias:
            if texto:
                # Extraer considerandos clave
                considerandos = self._extraer_considerandos(texto)
                for considerando in considerandos[:2]:  # Top 2 por sentencia
                    fragmentos.append({
                        'texto': considerando,
                        'sentencia_id': sent_id,
                        'caratula': caratula,
                        'fecha': fecha,
                        'materia': materia,
                        'tipo': 'considerando'
                    })

                # Extraer fundamentos
                fundamentos = self._extraer_fundamentos(texto)
                for fundamento in fundamentos[:1]:
                    fragmentos.append({
                        'texto': fundamento,
                        'sentencia_id': sent_id,
                        'caratula': caratula,
                        'fecha': fecha,
                        'materia': materia,
                        'tipo': 'fundamento'
                    })

            # Si hay chunks, leer algunos
            if ruta_chunks and Path(ruta_chunks).exists():
                chunks_texto = self._leer_chunks(Path(ruta_chunks))
                for chunk in chunks_texto[:2]:
                    fragmentos.append({
                        'texto': chunk,
                        'sentencia_id': sent_id,
                        'caratula': caratula,
                        'fecha': fecha,
                        'materia': materia,
                        'tipo': 'chunk'
                    })

        # Limitar total
        fragmentos = fragmentos[:max_fragmentos]

        print_success(f"{len(fragmentos)} fragmentos extraídos")
        return fragmentos

    def _extraer_considerandos(self, texto: str) -> List[str]:
        """Extrae considerandos del texto"""
        # Patrones para considerandos argentinos
        patrones = [
            r'CONSIDERANDO:?\s*[IVX\d]+[°\.\)]\s*[^\n]{100,800}',
            r'Que\s+[^\n]{100,800}',
            r'FUNDAMENTOS:?\s*[^\n]{100,800}'
        ]

        considerandos = []
        for patron in patrones:
            matches = re.findall(patron, texto, re.IGNORECASE | re.DOTALL)
            considerandos.extend(matches[:3])

        # Limpiar
        considerandos = [self._limpiar_texto(c) for c in considerandos]
        return considerandos

    def _extraer_fundamentos(self, texto: str) -> List[str]:
        """Extrae fundamentos jurídicos"""
        patrones = [
            r'(En virtud de lo expuesto[^\n]{100,500})',
            r'(Por ello[^\n]{100,500})',
            r'(En consecuencia[^\n]{100,500})',
            r'(Fundamento normativo[^\n]{100,500})'
        ]

        fundamentos = []
        for patron in patrones:
            matches = re.findall(patron, texto, re.IGNORECASE)
            fundamentos.extend(matches)

        return [self._limpiar_texto(f) for f in fundamentos[:3]]

    def _leer_chunks(self, ruta_chunks: Path) -> List[str]:
        """Lee archivos de chunks"""
        chunks = []
        try:
            for chunk_file in sorted(ruta_chunks.glob('chunk_*.txt'))[:3]:
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    texto = f.read()
                    if len(texto) > 200:
                        chunks.append(texto[:800])
        except Exception as e:
            print_warning(f"Error leyendo chunks: {e}")

        return chunks

    def _limpiar_texto(self, texto: str) -> str:
        """Limpia y normaliza texto"""
        # Eliminar saltos de línea múltiples
        texto = re.sub(r'\n+', ' ', texto)
        # Eliminar espacios múltiples
        texto = re.sub(r'\s+', ' ', texto)
        # Trim
        texto = texto.strip()
        return texto

# ============================================================================
# GENERADOR CON IA
# ============================================================================

class GeneradorInformesGeminiJudicial:
    """Genera informes judiciales usando IA generativa"""

    def __init__(self, db_path: Path = DB_FILE, api: str = 'auto'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.extractor = ExtractorFragmentosJudiciales(db_path)

        # Configurar API
        self.api_name = self._detectar_api(api)
        if not self.api_name:
            raise ValueError("No hay APIs de IA disponibles. Configura GEMINI_API_KEY, OPENAI_API_KEY o ANTHROPIC_API_KEY")

        self.cliente_ia = self._inicializar_cliente_ia()
        print_success(f"Usando API: {self.api_name}")

    def _detectar_api(self, api_preferida: str) -> Optional[str]:
        """Detecta qué API usar"""
        if api_preferida != 'auto' and API_CONFIG.get(api_preferida, {}).get('disponible'):
            return api_preferida

        # Auto-detectar
        for api_name, config in API_CONFIG.items():
            if config['disponible']:
                return api_name

        return None

    def _inicializar_cliente_ia(self):
        """Inicializa cliente de IA según API disponible"""
        if self.api_name == 'gemini':
            try:
                import google.generativeai as genai
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                modelo = API_CONFIG['gemini']['modelo_default']
                return genai.GenerativeModel(modelo)
            except ImportError:
                print_error("Instala: pip install google-generativeai")
                raise

        elif self.api_name == 'openai':
            try:
                from openai import OpenAI
                return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            except ImportError:
                print_error("Instala: pip install openai")
                raise

        elif self.api_name == 'anthropic':
            try:
                import anthropic
                return anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            except ImportError:
                print_error("Instala: pip install anthropic")
                raise

    # ========================================================================
    # OBTENCIÓN DE DATOS
    # ========================================================================

    def obtener_perfil_juez(self, juez: str) -> Optional[Dict]:
        """Obtiene perfil completo del juez"""
        self.cursor.execute("SELECT * FROM perfiles_judiciales_argentinos WHERE juez = ?", (juez,))
        row = self.cursor.fetchone()

        if not row:
            return None

        columnas = [desc[0] for desc in self.cursor.description]
        return dict(zip(columnas, row))

    def obtener_lineas_principales(self, juez: str) -> List[Dict]:
        """Obtiene líneas jurisprudenciales principales"""
        self.cursor.execute("""
        SELECT tema, cantidad_sentencias, consistencia_score, criterio_dominante
        FROM lineas_jurisprudenciales
        WHERE juez = ?
        ORDER BY cantidad_sentencias DESC
        LIMIT 5
        """, (juez,))

        lineas = []
        for row in self.cursor.fetchall():
            lineas.append({
                'tema': row[0],
                'cantidad': row[1],
                'consistencia': row[2],
                'criterio': row[3]
            })

        return lineas

    def obtener_autores_citados(self, juez: str) -> List[str]:
        """Obtiene autores más citados"""
        self.cursor.execute("""
        SELECT juez_destino, cantidad_citas
        FROM redes_influencia_judicial
        WHERE juez_origen = ? AND tipo_destino = 'autor_doctrinal'
        ORDER BY cantidad_citas DESC
        LIMIT 10
        """, (juez,))

        return [row[0] for row in self.cursor.fetchall()]

    # ========================================================================
    # CONSTRUCCIÓN DEL PROMPT
    # ========================================================================

    def construir_prompt(self, juez: str, perfil: Dict, fragmentos: List[Dict], lineas: List[Dict]) -> str:
        """Construye prompt especializado para análisis judicial"""

        prompt = f"""Eres un experto analista del pensamiento judicial argentino con profundo conocimiento del sistema jurídico nacional.

**TAREA**: Genera un informe académico profundo sobre el juez {juez}, basándote en datos cognitivos reales y fragmentos textuales de sus sentencias.

**DATOS DEL PERFIL JUDICIAL**:

1. **Contexto Institucional**:
   - Fuero: {perfil.get('fuero', 'N/D')}
   - Tribunal: {perfil.get('tribunal', 'N/D')}
   - Jurisdicción: {perfil.get('jurisdiccion', 'N/D')}
   - Sentencias analizadas: {perfil.get('total_sentencias_analizadas', 0)}

2. **Métricas Cognitivas y Judiciales**:
   - Activismo judicial: {perfil.get('tendencia_activismo', 0):.2f} (-1 restrictivo, +1 activista)
   - Formalismo: {perfil.get('formalismo_vs_sustancialismo', 0):.2f} (-1 sustancia, +1 forma)
   - Interpretación dominante: {perfil.get('interpretacion_normativa', 'N/D')}
   - Metodología principal: {perfil.get('metodologia_principal', 'N/D')}

3. **Protección de Derechos** (0-1):
   - Derechos fundamentales: {perfil.get('proteccion_derechos_fundamentales', 0):.2f}
   - Derechos sociales: {perfil.get('proteccion_derechos_sociales', 0):.2f}
   - Trabajador: {perfil.get('proteccion_trabajador', 0):.2f}
   - Consumidor: {perfil.get('proteccion_derechos_consumidor', 0):.2f}
   - Medio ambiente: {perfil.get('proteccion_medio_ambiente', 0):.2f}

4. **Sesgos Argentinos**:
   - Pro-trabajador: {perfil.get('sesgo_pro_trabajador', 0):.2f}
   - Pro-consumidor: {perfil.get('sesgo_pro_consumidor', 0):.2f}
   - Garantista: {perfil.get('sesgo_garantista', 0):.2f}
   - Pro-estado: {perfil.get('sesgo_pro_estado', 0):.2f}

5. **Deferencia Institucional** (0-1):
   - Al legislativo: {perfil.get('deferencia_legislativo', 0):.2f}
   - Al ejecutivo: {perfil.get('deferencia_ejecutivo', 0):.2f}
   - Respeto precedentes: {perfil.get('respeto_precedentes', 0):.2f}
   - Innovación jurídica: {perfil.get('innovacion_juridica', 0):.2f}

6. **Tests y Estándares**:
   - Test proporcionalidad: {perfil.get('uso_test_proporcionalidad', 0):.2f}
   - Test razonabilidad: {perfil.get('uso_test_razonabilidad', 0):.2f}
   - Control constitucionalidad: {perfil.get('uso_control_constitucionalidad', 0):.2f}

7. **Fuentes del Derecho** (pesos relativos):
   - Constitución: {perfil.get('peso_constitucion', 0):.2f}
   - Ley: {perfil.get('peso_ley', 0):.2f}
   - Jurisprudencia: {perfil.get('peso_jurisprudencia', 0):.2f}
   - Doctrina: {perfil.get('peso_doctrina', 0):.2f}
   - Tratados internacionales: {perfil.get('peso_tratados_internacionales', 0):.2f}

8. **Retórica (Aristóteles)**:
   - Ethos (autoridad): {perfil.get('uso_ethos', 0):.2f}
   - Pathos (emoción): {perfil.get('uso_pathos', 0):.2f}
   - Logos (razón): {perfil.get('uso_logos', 0):.2f}

**LÍNEAS JURISPRUDENCIALES CONSOLIDADAS**:
"""

        if lineas:
            for i, linea in enumerate(lineas, 1):
                prompt += f"\n{i}. **{linea['tema']}**: {linea['cantidad']} sentencias, consistencia {linea['consistencia']:.2f}\n   Criterio: {linea['criterio']}"
        else:
            prompt += "\nNo hay suficientes sentencias para líneas consolidadas."

        prompt += "\n\n**FRAGMENTOS TEXTUALES REALES DE SENTENCIAS**:\n"

        if fragmentos:
            for i, frag in enumerate(fragmentos[:10], 1):
                prompt += f"\n--- Fragmento {i} ({frag['tipo']}) ---"
                prompt += f"\nCaso: {frag.get('caratula', 'N/D')} ({frag.get('fecha', 'N/D')})"
                prompt += f"\nMateria: {frag.get('materia', 'N/D')}"
                prompt += f"\nTexto: \"{frag['texto'][:500]}...\"\n"
        else:
            prompt += "\n(No hay fragmentos textuales disponibles)\n"

        prompt += """

**INSTRUCCIONES PARA EL INFORME**:

Genera un informe académico de 800-1200 palabras con la siguiente estructura:

### 1. INTRODUCCIÓN AL PERFIL JUDICIAL (150-200 palabras)
- Presenta al juez en su contexto institucional
- Resume su posicionamiento en el espectro judicial argentino
- Menciona el corpus analizado

### 2. ANÁLISIS DEL PENSAMIENTO JUDICIAL (400-500 palabras)

**2.1 Activismo y Formalismo**:
- Analiza su tendencia activista/restrictiva CITANDO fragmentos textuales
- Explica su nivel de formalismo vs sustancialismo con ejemplos concretos
- Relaciona con casos específicos

**2.2 Metodología Interpretativa**:
- Analiza su método interpretativo dominante (literal/sistemática/teleológica)
- Fundamenta con citas textuales de considerandos
- Explica evolución si se detecta

**2.3 Protección de Derechos**:
- Identifica qué derechos protege más intensamente
- Cita fragmentos donde se evidencia esta protección
- Analiza jerarquización de derechos en conflicto

### 3. LÍNEAS JURISPRUDENCIALES Y CONSISTENCIA (250-300 palabras)
- Analiza las líneas consolidadas identificadas
- Evalúa consistencia y predictibilidad
- Menciona criterios dominantes con citas

### 4. SESGOS Y ORIENTACIÓN IDEOLÓGICA (150-200 palabras)
- Analiza sesgos detectados (pro-trabajador, garantista, etc.)
- Fundamenta con datos cuantitativos y cualitativos
- Contextualiza en el panorama judicial argentino

### 5. POSICIONAMIENTO COMPARATIVO (100-150 palabras)
- Ubica al juez en el espectro judicial argentino
- Compara con tendencias dominantes del fuero
- Menciona su perfil único o distintivo

**REQUISITOS CRÍTICOS**:
1. Incluye AL MENOS 5 CITAS TEXTUALES DIRECTAS de los fragmentos proporcionados
2. Usa formato: "Como expresa en [Caso X]: \"[cita textual]...\""
3. Análisis académico riguroso, no meramente descriptivo
4. Vocabulario técnico-jurídico argentino
5. Fundamenta CADA afirmación con datos o citas
6. Tono profesional, objetivo pero analítico
7. 800-1200 palabras OBLIGATORIO

**FORMATO DE SALIDA**:
- Usa Markdown
- Títulos con ##
- Citas en cursiva: *"texto citado"*
- Referencias a casos: **Caso "X c/ Y"**

Genera el informe AHORA:
"""

        return prompt

    # ========================================================================
    # GENERACIÓN CON IA
    # ========================================================================

    def generar_con_ia(self, prompt: str) -> str:
        """Genera texto usando IA"""
        print_info("Generando informe con IA...")

        try:
            if self.api_name == 'gemini':
                response = self.cliente_ia.generate_content(prompt)
                return response.text

            elif self.api_name == 'openai':
                response = self.cliente_ia.chat.completions.create(
                    model=API_CONFIG['openai']['modelo_default'],
                    messages=[
                        {"role": "system", "content": "Eres un experto analista del pensamiento judicial argentino."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                return response.choices[0].message.content

            elif self.api_name == 'anthropic':
                response = self.cliente_ia.messages.create(
                    model=API_CONFIG['anthropic']['modelo_default'],
                    max_tokens=3000,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text

        except Exception as e:
            print_error(f"Error generando con IA: {e}")
            raise

    # ========================================================================
    # GENERACIÓN DE GRÁFICO RADAR
    # ========================================================================

    def generar_grafico_radar(self, juez: str, perfil: Dict, formato: str = 'png') -> Optional[str]:
        """Genera gráfico radar del perfil judicial"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            from math import pi
        except ImportError:
            print_warning("matplotlib no instalado. Gráfico omitido.")
            return None

        print_info("Generando gráfico radar...")

        # Dimensiones del perfil
        categorias = [
            'Activismo',
            'Innovación\nJurídica',
            'Protección\nDerechos',
            'Garantismo',
            'Control\nConstitucional',
            'Interpretación\nExpansiva'
        ]

        # Valores (normalizar a 0-1)
        valores = [
            (perfil.get('tendencia_activismo', 0) + 1) / 2,  # -1,1 -> 0,1
            perfil.get('innovacion_juridica', 0.5),
            (perfil.get('proteccion_derechos_fundamentales', 0) +
             perfil.get('proteccion_derechos_sociales', 0)) / 2,
            perfil.get('sesgo_garantista', 0.5),
            perfil.get('uso_control_constitucionalidad', 0.5),
            1 - perfil.get('deferencia_legislativo', 0.5)  # Invertir
        ]

        # Configurar gráfico
        N = len(categorias)
        angulos = [n / float(N) * 2 * pi for n in range(N)]
        valores += valores[:1]  # Cerrar el círculo
        angulos += angulos[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

        ax.plot(angulos, valores, 'o-', linewidth=2, color='#1f77b4', label=juez)
        ax.fill(angulos, valores, alpha=0.25, color='#1f77b4')

        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, size=10)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], size=8)
        ax.grid(True, linestyle='--', alpha=0.7)

        plt.title(f'Perfil Judicial: {juez}', size=14, pad=20, weight='bold')
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"radar_{juez.replace(' ', '_')}_{timestamp}.{formato}"
        ruta_archivo = INFORMES_DIR / nombre_archivo

        plt.savefig(ruta_archivo, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        print_success(f"Gráfico guardado: {ruta_archivo.name}")
        return str(ruta_archivo)

    # ========================================================================
    # INFORME COMPLETO
    # ========================================================================

    def generar_informe_completo(self, juez: str, formato: str = 'html') -> str:
        """
        Genera informe completo con IA

        Args:
            juez: Nombre del juez
            formato: 'html', 'md', 'txt'

        Returns:
            Path del archivo generado
        """
        print(f"\n{Colors.BOLD}═══════════════════════════════════════════════════{Colors.ENDC}")
        print(f"{Colors.BOLD}  GENERADOR DE INFORMES JUDICIALES CON IA{Colors.ENDC}")
        print(f"{Colors.BOLD}═══════════════════════════════════════════════════{Colors.ENDC}\n")
        print(f"{Colors.BLUE}Juez:{Colors.ENDC} {juez}")
        print(f"{Colors.BLUE}API:{Colors.ENDC} {self.api_name}")
        print(f"{Colors.BLUE}Formato:{Colors.ENDC} {formato}\n")

        # 1. Obtener datos
        print_info("📊 Recopilando datos del juez...")
        perfil = self.obtener_perfil_juez(juez)
        if not perfil:
            print_error(f"No se encontró perfil para {juez}")
            return None

        lineas = self.obtener_lineas_principales(juez)
        autores = self.obtener_autores_citados(juez)

        # 2. Extraer fragmentos
        print_info("📄 Extrayendo fragmentos textuales de sentencias...")
        fragmentos = self.extractor.extraer_fragmentos_juez(juez, max_fragmentos=15)

        if not fragmentos:
            print_warning("No hay fragmentos textuales. El informe será solo con métricas.")

        # 3. Construir prompt
        print_info("🤖 Construyendo prompt especializado...")
        prompt = self.construir_prompt(juez, perfil, fragmentos, lineas)

        # 4. Generar con IA
        print_info(f"✨ Generando informe con {self.api_name.upper()}...")
        informe_ia = self.generar_con_ia(prompt)

        if not informe_ia:
            print_error("No se pudo generar el informe")
            return None

        print_success(f"Informe generado: {len(informe_ia)} caracteres")

        # 5. Generar gráfico
        grafico_path = self.generar_grafico_radar(juez, perfil, 'png')

        # 6. Ensamblar informe final
        print_info("📝 Ensamblando informe final...")

        if formato == 'html':
            ruta_final = self._generar_html(juez, informe_ia, perfil, fragmentos, lineas, grafico_path)
        elif formato == 'md':
            ruta_final = self._generar_markdown(juez, informe_ia, perfil, fragmentos, grafico_path)
        else:
            ruta_final = self._generar_txt(juez, informe_ia, perfil)

        print(f"\n{Colors.GREEN}{'═'*60}{Colors.ENDC}")
        print(f"{Colors.GREEN}✓ INFORME GENERADO EXITOSAMENTE{Colors.ENDC}")
        print(f"{Colors.GREEN}{'═'*60}{Colors.ENDC}")
        print(f"\n📁 Ubicación: {ruta_final}")
        print(f"📊 Gráfico: {grafico_path if grafico_path else 'No generado'}\n")

        return str(ruta_final)

    def _generar_html(self, juez, informe_ia, perfil, fragmentos, lineas, grafico_path) -> Path:
        """Genera informe en HTML"""
        import base64

        # Convertir gráfico a base64 si existe
        img_base64 = ""
        if grafico_path and Path(grafico_path).exists():
            with open(grafico_path, 'rb') as f:
                img_base64 = base64.b64encode(f.read()).decode()

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Judicial IA - {juez}</title>
    <style>
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
            color: #333;
            line-height: 1.7;
        }}
        .container {{
            background: white;
            padding: 50px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
        h1 {{
            color: #1a5490;
            border-bottom: 3px solid #1a5490;
            padding-bottom: 15px;
            font-size: 2.2em;
            margin-bottom: 10px;
        }}
        .metadata {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 30px;
            padding: 15px;
            background: #f9f9f9;
            border-left: 4px solid #1a5490;
        }}
        .metadata strong {{
            color: #1a5490;
        }}
        h2 {{
            color: #2c5f8d;
            margin-top: 35px;
            margin-bottom: 15px;
            font-size: 1.6em;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 8px;
        }}
        h3 {{
            color: #3d7ba8;
            margin-top: 25px;
            margin-bottom: 12px;
            font-size: 1.3em;
        }}
        .informe-ia {{
            margin: 30px 0;
            text-align: justify;
        }}
        .informe-ia p {{
            margin-bottom: 15px;
        }}
        .informe-ia em {{
            color: #555;
            font-style: italic;
        }}
        .informe-ia strong {{
            color: #1a5490;
        }}
        .grafico {{
            text-align: center;
            margin: 40px 0;
            padding: 20px;
            background: #fafafa;
            border-radius: 8px;
        }}
        .grafico img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .metricas {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 25px 0;
        }}
        .metrica {{
            padding: 15px;
            background: #f9f9f9;
            border-radius: 6px;
            border-left: 4px solid #1a5490;
        }}
        .metrica-label {{
            font-weight: bold;
            color: #1a5490;
            margin-bottom: 5px;
        }}
        .metrica-valor {{
            font-size: 1.3em;
            color: #333;
        }}
        .fragmentos {{
            margin: 30px 0;
        }}
        .fragmento {{
            background: #f9f9f9;
            padding: 20px;
            margin: 15px 0;
            border-left: 4px solid #3d7ba8;
            border-radius: 4px;
        }}
        .fragmento-header {{
            color: #1a5490;
            font-size: 0.85em;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        .fragmento-texto {{
            font-style: italic;
            color: #555;
            line-height: 1.6;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #999;
            font-size: 0.9em;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            background: #1a5490;
            color: white;
            border-radius: 12px;
            font-size: 0.75em;
            margin-left: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Informe Judicial Generado con IA</h1>

        <div class="metadata">
            <strong>Juez:</strong> {juez}<br>
            <strong>Fecha de generación:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M")}<br>
            <strong>Sistema:</strong> Análisis de Pensamiento Judicial Argentina v1.0<br>
            <strong>Motor IA:</strong> {self.api_name.upper()}<br>
            <strong>Sentencias analizadas:</strong> {perfil.get('total_sentencias_analizadas', 0)}<br>
            <strong>Confianza del perfil:</strong> {perfil.get('confianza_perfil', 0):.2%}
        </div>
"""

        # Gráfico radar
        if img_base64:
            html += f"""
        <div class="grafico">
            <h2>Perfil Judicial Visual</h2>
            <img src="data:image/png;base64,{img_base64}" alt="Gráfico Radar">
        </div>
"""

        # Métricas clave
        html += """
        <h2>Métricas Clave</h2>
        <div class="metricas">
"""

        metricas = [
            ("Activismo Judicial", perfil.get('tendencia_activismo', 0), "±1"),
            ("Protección Derechos", perfil.get('proteccion_derechos_fundamentales', 0), "0-1"),
            ("Formalismo", perfil.get('formalismo_vs_sustancialismo', 0), "±1"),
            ("Innovación Jurídica", perfil.get('innovacion_juridica', 0), "0-1"),
            ("Sesgo Garantista", perfil.get('sesgo_garantista', 0), "0-1"),
            ("Respeto Precedentes", perfil.get('respeto_precedentes', 0), "0-1")
        ]

        for label, valor, rango in metricas:
            html += f"""
            <div class="metrica">
                <div class="metrica-label">{label} <span class="badge">{rango}</span></div>
                <div class="metrica-valor">{valor:.2f}</div>
            </div>
"""

        html += """
        </div>

        <h2>Análisis Generado por IA</h2>
        <div class="informe-ia">
"""

        # Convertir markdown a HTML simple
        informe_html = informe_ia.replace('\n\n', '</p><p>')
        informe_html = informe_html.replace('### ', '<h3>').replace('\n', '</h3>', informe_html.count('### '))
        informe_html = informe_html.replace('## ', '<h2>').replace('\n', '</h2>', informe_html.count('## '))
        informe_html = informe_html.replace('**', '<strong>').replace('**', '</strong>')
        informe_html = informe_html.replace('*"', '<em>"').replace('"*', '"</em>')

        html += f"<p>{informe_html}</p>"

        html += """
        </div>
"""

        # Fragmentos textuales
        if fragmentos:
            html += """
        <h2>Fragmentos Textuales Analizados</h2>
        <div class="fragmentos">
"""
            for frag in fragmentos[:5]:
                html += f"""
            <div class="fragmento">
                <div class="fragmento-header">
                    {frag['tipo'].upper()} - {frag.get('caratula', 'N/D')} ({frag.get('fecha', 'N/D')})
                </div>
                <div class="fragmento-texto">
                    "{frag['texto'][:400]}..."
                </div>
            </div>
"""
            html += """
        </div>
"""

        # Footer
        html += f"""
        <div class="footer">
            Sistema de Análisis Judicial Argentina v1.0<br>
            Generado con {self.api_name.upper()} · {datetime.now().year}
        </div>
    </div>
</body>
</html>
"""

        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_ia_{juez.replace(' ', '_')}_{timestamp}.html"
        ruta_archivo = INFORMES_DIR / nombre_archivo

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(html)

        return ruta_archivo

    def _generar_markdown(self, juez, informe_ia, perfil, fragmentos, grafico_path) -> Path:
        """Genera informe en Markdown"""
        md = f"""# 📋 Informe Judicial Generado con IA

**Juez:** {juez}
**Fecha:** {datetime.now().strftime("%d/%m/%Y %H:%M")}
**Sistema:** Análisis de Pensamiento Judicial Argentina v1.0
**Motor IA:** {self.api_name.upper()}
**Sentencias analizadas:** {perfil.get('total_sentencias_analizadas', 0)}

---

## Perfil Judicial Visual

"""
        if grafico_path:
            md += f"![Gráfico Radar]({Path(grafico_path).name})\n\n"

        md += f"""## Métricas Clave

- **Activismo Judicial:** {perfil.get('tendencia_activismo', 0):.2f}
- **Protección Derechos:** {perfil.get('proteccion_derechos_fundamentales', 0):.2f}
- **Formalismo:** {perfil.get('formalismo_vs_sustancialismo', 0):.2f}
- **Innovación Jurídica:** {perfil.get('innovacion_juridica', 0):.2f}
- **Sesgo Garantista:** {perfil.get('sesgo_garantista', 0):.2f}

---

## Análisis Generado por IA

{informe_ia}

---

## Fragmentos Textuales Analizados

"""

        if fragmentos:
            for i, frag in enumerate(fragmentos[:5], 1):
                md += f"""### Fragmento {i}: {frag['tipo'].upper()}
**Caso:** {frag.get('caratula', 'N/D')} ({frag.get('fecha', 'N/D')})
**Texto:** *"{frag['texto'][:400]}..."*

"""

        md += f"""---

*Sistema de Análisis Judicial Argentina v1.0*
*Generado con {self.api_name.upper()} · {datetime.now().year}*
"""

        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_ia_{juez.replace(' ', '_')}_{timestamp}.md"
        ruta_archivo = INFORMES_DIR / nombre_archivo

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(md)

        return ruta_archivo

    def _generar_txt(self, juez, informe_ia, perfil) -> Path:
        """Genera informe en TXT"""
        txt = f"""
{'='*80}
            INFORME JUDICIAL GENERADO CON IA
{'='*80}

Juez: {juez}
Fecha: {datetime.now().strftime("%d/%m/%Y %H:%M")}
Sistema: Análisis de Pensamiento Judicial Argentina v1.0
Motor IA: {self.api_name.upper()}
Sentencias analizadas: {perfil.get('total_sentencias_analizadas', 0)}

{'='*80}

{informe_ia}

{'='*80}
Sistema de Análisis Judicial Argentina v1.0
Generado con {self.api_name.upper()} · {datetime.now().year}
{'='*80}
"""

        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_ia_{juez.replace(' ', '_')}_{timestamp}.txt"
        ruta_archivo = INFORMES_DIR / nombre_archivo

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(txt)

        return ruta_archivo


# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Generador de informes judiciales con IA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python generador_informes_gemini_judicial.py "Ricardo Lorenzetti"
  python generador_informes_gemini_judicial.py "Elena Highton" --formato html
  python generador_informes_gemini_judicial.py "Juan Pérez" --api openai --formato md

Configuración de APIs (en variables de entorno):
  export GEMINI_API_KEY="tu-api-key"
  export OPENAI_API_KEY="tu-api-key"
  export ANTHROPIC_API_KEY="tu-api-key"

Instalar dependencias:
  pip install google-generativeai  # Para Gemini
  pip install openai               # Para OpenAI
  pip install anthropic            # Para Claude
  pip install matplotlib           # Para gráficos
        """
    )

    parser.add_argument('juez', help='Nombre del juez')
    parser.add_argument(
        '--api',
        choices=['auto', 'gemini', 'openai', 'anthropic'],
        default='auto',
        help='API de IA a usar (default: auto-detectar)'
    )
    parser.add_argument(
        '--formato',
        choices=['html', 'md', 'txt'],
        default='html',
        help='Formato de salida (default: html)'
    )

    args = parser.parse_args()

    # Verificar APIs disponibles
    apis_disponibles = [name for name, conf in API_CONFIG.items() if conf['disponible']]

    if not apis_disponibles:
        print_error("No hay APIs de IA configuradas")
        print("\nConfigura al menos una API:")
        print("  export GEMINI_API_KEY='tu-api-key'")
        print("  export OPENAI_API_KEY='tu-api-key'")
        print("  export ANTHROPIC_API_KEY='tu-api-key'")
        print("\nObtén API keys en:")
        print("  Gemini: https://makersuite.google.com/app/apikey")
        print("  OpenAI: https://platform.openai.com/api-keys")
        print("  Anthropic: https://console.anthropic.com/")
        sys.exit(1)

    print_info(f"APIs disponibles: {', '.join(apis_disponibles)}")

    # Crear generador
    try:
        generador = GeneradorInformesGeminiJudicial(api=args.api)
    except Exception as e:
        print_error(f"Error inicializando generador: {e}")
        sys.exit(1)

    # Generar informe
    try:
        ruta = generador.generar_informe_completo(args.juez, args.formato)

        if ruta:
            print(f"\n{Colors.BOLD}¡Listo!{Colors.ENDC} Abre el archivo:")
            print(f"  {ruta}\n")

    except Exception as e:
        print_error(f"Error generando informe: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
