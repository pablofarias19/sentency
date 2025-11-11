#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 SINCRONIZADOR AUTOMÁTICO DE BASES DE DATOS
=============================================

Se ejecuta automáticamente al final de procesar_todo.py para:
1. Sincronizar metadatos.db → autor_centrico.db
2. Calcular métricas faltantes (densidad_citas, uso_ejemplos)
3. Mantener todas las bases consistentes

FECHA: 11 NOV 2025
"""

import sqlite3
import re
import json
from datetime import datetime
from pathlib import Path

class SincronizadorAutomatico:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.metadatos_db = self.base_path / "colaborative/bases_rag/cognitiva/metadatos.db"
        self.autor_centrico_db = self.base_path / "colaborative/bases_rag/cognitiva/autor_centrico.db"
        
    def sincronizar_todo(self):
        """Sincronización completa automática"""
        print("\n" + "="*70)
        print("🔄 SINCRONIZACIÓN AUTOMÁTICA DE BASES DE DATOS")
        print("="*70)
        
        # Paso 1: Calcular métricas faltantes en metadatos.db
        print("\n📊 Paso 1: Calculando métricas metodológicas...")
        self.calcular_metricas_metodologicas()
        
        # Paso 2: Sincronizar hacia autor_centrico.db
        print("\n🔗 Paso 2: Sincronizando hacia autor_centrico.db...")
        self.sincronizar_autor_centrico()
        
        print("\n✅ SINCRONIZACIÓN COMPLETADA")
        print("="*70 + "\n")
    
    def calcular_metricas_metodologicas(self):
        """Calcula densidad_citas y uso_ejemplos desde el texto"""
        try:
            conn = sqlite3.connect(self.metadatos_db)
            c = conn.cursor()
            
            # Verificar si las columnas existen
            c.execute("PRAGMA table_info(perfiles_cognitivos)")
            columnas = [col[1] for col in c.fetchall()]
            
            if 'densidad_citas' not in columnas:
                c.execute("ALTER TABLE perfiles_cognitivos ADD COLUMN densidad_citas REAL DEFAULT 0.0")
            if 'uso_ejemplos' not in columnas:
                c.execute("ALTER TABLE perfiles_cognitivos ADD COLUMN uso_ejemplos REAL DEFAULT 0.0")
            
            conn.commit()
            
            # Obtener todos los autores
            c.execute("SELECT id, autor, fuente, total_palabras, texto_muestra FROM perfiles_cognitivos")
            registros = c.fetchall()
            
            actualizados = 0
            for id_perfil, autor, fuente, total_palabras, texto_muestra in registros:
                # Leer el PDF completo si existe
                texto_completo = self._leer_pdf_completo(fuente) if fuente else texto_muestra
                
                if texto_completo and total_palabras:
                    # Calcular densidad_citas (referencias entre paréntesis, pies de página, etc.)
                    citas = len(re.findall(r'\([^)]*\d{4}[^)]*\)', texto_completo))  # (Autor, 2024)
                    citas += len(re.findall(r'\[\d+\]', texto_completo))  # [1], [2], etc.
                    citas += len(re.findall(r'(?:cf\.|cfr\.|vid\.|v\.|véase)', texto_completo, re.IGNORECASE))
                    densidad_citas = min(citas / (total_palabras / 100), 100.0)  # Citas por cada 100 palabras
                    
                    # Calcular uso_ejemplos
                    ejemplos = len(re.findall(r'(?:por ejemplo|v\.gr\.|verbigracia|así|como en)', texto_completo, re.IGNORECASE))
                    ejemplos += len(re.findall(r'(?:caso|supuesto|situación)\s+(?:de|en)', texto_completo, re.IGNORECASE))
                    uso_ejemplos = min(ejemplos / (total_palabras / 100), 100.0)
                    
                    # Actualizar
                    c.execute("""
                        UPDATE perfiles_cognitivos
                        SET densidad_citas = ?, uso_ejemplos = ?
                        WHERE id = ?
                    """, (densidad_citas, uso_ejemplos, id_perfil))
                    
                    actualizados += 1
                    print(f"  ✓ {autor}: densidad_citas={densidad_citas:.2f}%, uso_ejemplos={uso_ejemplos:.2f}%")
            
            conn.commit()
            conn.close()
            print(f"\n   📈 {actualizados} registros actualizados con métricas metodológicas")
            
        except Exception as e:
            print(f"  ❌ Error calculando métricas: {e}")
    
    def _leer_pdf_completo(self, ruta_pdf):
        """Lee el contenido completo de un PDF"""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(ruta_pdf)
            texto = ""
            for page in doc:
                texto += page.get_text()
            doc.close()
            return texto
        except:
            return None
    
    def sincronizar_autor_centrico(self):
        """Sincroniza datos hacia autor_centrico.db"""
        try:
            conn_meta = sqlite3.connect(self.metadatos_db)
            conn_autor = sqlite3.connect(self.autor_centrico_db)
            
            c_meta = conn_meta.cursor()
            c_autor = conn_autor.cursor()
            
            # Obtener autores de metadatos.db
            c_meta.execute("""
                SELECT 
                    autor, fuente, archivo,
                    formalismo, creatividad, dogmatismo, empirismo,
                    interdisciplinariedad, nivel_abstraccion, complejidad_sintactica, uso_jurisprudencia,
                    tono, tipo_pensamiento, ethos, pathos, logos,
                    razonamiento_dominante, modalidad_epistemica,
                    densidad_citas, uso_ejemplos,
                    total_palabras, fecha_analisis
                FROM perfiles_cognitivos
                WHERE autor IS NOT NULL AND autor != ''
            """)
            
            autores_meta = c_meta.fetchall()
            
            # Obtener autores existentes en autor_centrico
            c_autor.execute("SELECT autor FROM perfiles_autorales_expandidos")
            autores_existentes = [a[0] for a in c_autor.fetchall()]
            
            insertados = 0
            actualizados = 0
            
            for row in autores_meta:
                (autor, fuente, archivo, 
                 formalismo, creatividad, dogmatismo, empirismo,
                 interdisciplina, abstraccion, sintaxis, jurisprudencia,
                 tono, pensamiento, ethos, pathos, logos,
                 razonamiento, modalidad,
                 densidad_citas, uso_ejemplos,
                 palabras, fecha) = row
                
                # MAPEO
                metodologia = razonamiento if razonamiento else "Mixto"
                patron = pensamiento if pensamiento else "Analítico-Jurídico"
                
                if logos and logos > 0.7:
                    estilo = "Lógico-Racional"
                elif ethos and ethos > 0.5:
                    estilo = "Autoritativo"
                else:
                    estilo = "Equilibrado"
                
                estructura = tono if tono else "Formal-Académico"
                
                marcadores = json.dumps({
                    "formalismo": float(formalismo) if formalismo else 0.5,
                    "densidad_citas": float(densidad_citas) if densidad_citas else 0.0,
                    "uso_ejemplos": float(uso_ejemplos) if uso_ejemplos else 0.0
                })
                
                vocabulario = json.dumps({
                    "nivel_tecnico": "alto" if formalismo and formalismo > 0.7 else "medio",
                    "jurisprudencia": float(jurisprudencia) if jurisprudencia else 0.0
                })
                
                densidad = float(abstraccion) if abstraccion else 0.5
                complejidad = float(sintaxis) if sintaxis else 0.5
                modalidad_ep = modalidad if modalidad else "Dialéctico"
                titulo = archivo if archivo else (fuente.split('\\')[-1] if fuente else "Sin título")
                originalidad = float(creatividad) if creatividad else 0.5
                coherencia = 1.0 - float(dogmatismo) if dogmatismo else 0.7
                impacto = (float(formalismo) + float(jurisprudencia) + float(ethos)) / 3.0 if all([formalismo, jurisprudencia, ethos]) else 0.5
                timestamp_now = datetime.now().isoformat()
                
                if autor in autores_existentes:
                    # Actualizar
                    c_autor.execute("""
                        UPDATE perfiles_autorales_expandidos
                        SET
                            metodologia_principal = ?,
                            patron_razonamiento_dominante = ?,
                            estilo_argumentativo = ?,
                            estructura_discursiva = ?,
                            marcadores_linguisticos = ?,
                            vocabulario_especializado = ?,
                            densidad_conceptual = ?,
                            complejidad_sintactica = ?,
                            uso_ethos = ?,
                            uso_pathos = ?,
                            uso_logos = ?,
                            modalidad_epistemica = ?,
                            primera_obra = ?,
                            ultima_obra = ?,
                            originalidad_score = ?,
                            coherencia_interna = ?,
                            impacto_metodologico = ?,
                            total_documentos = 1,
                            fecha_ultima_actualizacion = ?
                        WHERE autor = ?
                    """, (
                        metodologia, patron, estilo, estructura,
                        marcadores, vocabulario,
                        densidad, complejidad,
                        float(ethos) if ethos else 0.0,
                        float(pathos) if pathos else 0.0,
                        float(logos) if logos else 0.0,
                        modalidad_ep,
                        titulo, titulo,
                        originalidad, coherencia, impacto,
                        timestamp_now,
                        autor
                    ))
                    actualizados += 1
                else:
                    # Insertar
                    c_autor.execute("""
                        INSERT INTO perfiles_autorales_expandidos (
                            autor, metodologia_principal, patron_razonamiento_dominante,
                            estilo_argumentativo, estructura_discursiva,
                            marcadores_linguisticos, vocabulario_especializado,
                            densidad_conceptual, complejidad_sintactica,
                            uso_ethos, uso_pathos, uso_logos,
                            modalidad_epistemica, primera_obra, ultima_obra,
                            originalidad_score, coherencia_interna, impacto_metodologico,
                            total_documentos, fecha_primer_analisis, fecha_ultima_actualizacion
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        autor, metodologia, patron, estilo, estructura,
                        marcadores, vocabulario, densidad, complejidad,
                        float(ethos) if ethos else 0.0,
                        float(pathos) if pathos else 0.0,
                        float(logos) if logos else 0.0,
                        modalidad_ep, titulo, titulo,
                        originalidad, coherencia, impacto,
                        1, timestamp_now, timestamp_now
                    ))
                    insertados += 1
            
            conn_autor.commit()
            
            # Verificar resultado
            c_autor.execute("SELECT COUNT(DISTINCT autor) FROM perfiles_autorales_expandidos")
            total_final = c_autor.fetchone()[0]
            
            print(f"   ➕ {insertados} nuevos | ✏️  {actualizados} actualizados")
            print(f"   📊 Total en autor_centrico.db: {total_final} autores")
            
            conn_meta.close()
            conn_autor.close()
            
        except Exception as e:
            print(f"  ❌ Error sincronizando: {e}")

# Ejecución automática si se llama directamente
if __name__ == "__main__":
    sincronizador = SincronizadorAutomatico()
    sincronizador.sincronizar_todo()
