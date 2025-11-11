#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 SISTEMA AUTOR-CÉNTRICO COGNITIVO
===================================

Transforma el enfoque del sistema hacia perfiles autorales profundos,
metodología cognitiva y comparativa inter-autoral.

OBJETIVOS:
- Centrarse en CÓMO PIENSA cada autor (no QUÉ dice)
- Mapear metodologías y patrones de razonamiento
- Crear redes de influencia y comparativas
- Mejora continua de perfiles autorales

AUTOR: Sistema Cognitivo v4.0
FECHA: 9 NOV 2025
"""

import os
import sqlite3
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from collections import defaultdict, Counter

class SistemaAutorCentrico:
    """
    Sistema centrado en perfiles autorales y metodología cognitiva
    """
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            # Usar ruta relativa al script actual
            script_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'colaborative'))
        self.base_dir = base_dir
        self.db_cognitiva = os.path.join(self.base_dir, "bases_rag/cognitiva/metadatos.db")
        self.db_autor_centrico = os.path.join(self.base_dir, "bases_rag/cognitiva/autor_centrico.db")
        self.logs_dir = os.path.join(self.base_dir, "data/logs")
        
        # Crear logs si no existe
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Inicializar base autor-céntrica
        self._inicializar_db_autor_centrico()
    
    def _inicializar_db_autor_centrico(self):
        """
        Crea la base de datos autor-céntrica optimizada
        """
        try:
            conn = sqlite3.connect(self.db_autor_centrico)
            cursor = conn.cursor()
            
            # Tabla principal de perfiles autorales expandidos
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS perfiles_autorales_expandidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT UNIQUE NOT NULL,
                
                -- METODOLOGÍA COGNITIVA
                metodologia_principal TEXT,
                patron_razonamiento_dominante TEXT,
                estilo_argumentativo TEXT,
                estructura_discursiva TEXT,
                
                -- FIRMA INTELECTUAL
                marcadores_linguisticos TEXT,
                vocabulario_especializado TEXT,
                densidad_conceptual REAL,
                complejidad_sintactica REAL,
                
                -- RASGOS ARISTOTÉLICOS
                uso_ethos REAL,
                uso_pathos REAL,
                uso_logos REAL,
                modalidad_epistemica TEXT,
                
                -- EVOLUCIÓN TEMPORAL
                primera_obra TEXT,
                ultima_obra TEXT,
                evolucion_metodologica TEXT,
                
                -- INFLUENCIAS
                autores_que_cita TEXT,
                influencias_detectadas TEXT,
                escuela_pensamiento TEXT,
                
                -- MÉTRICAS COMPARATIVAS
                originalidad_score REAL,
                coherencia_interna REAL,
                impacto_metodologico REAL,
                
                -- METADATOS
                total_documentos INTEGER,
                total_paginas INTEGER,
                fecha_primer_analisis TIMESTAMP,
                fecha_ultima_actualizacion TIMESTAMP,
                version_perfil TEXT
            )
            ''')
            
            # Tabla de comparativas inter-autorales
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS comparativas_autorales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor_a TEXT NOT NULL,
                autor_b TEXT NOT NULL,
                
                -- SIMILITUDES METODOLÓGICAS
                similitud_metodologica REAL,
                coincidencias_razonamiento TEXT,
                patrones_comunes TEXT,
                
                -- DIVERGENCIAS
                diferencias_clave TEXT,
                conflictos_metodologicos TEXT,
                
                -- INFLUENCIAS CRUZADAS
                autor_a_cita_b BOOLEAN,
                autor_b_cita_a BOOLEAN,
                influencia_mutua REAL,
                
                -- ANÁLISIS COMPARATIVO
                convergencias_tematicas TEXT,
                divergencias_estilistic TEXT,
                complementariedad REAL,
                
                fecha_analisis TIMESTAMP,
                UNIQUE(autor_a, autor_b)
            )
            ''')
            
            # Tabla de evolución metodológica
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS evolucion_metodologica (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT NOT NULL,
                documento TEXT NOT NULL,
                fecha_documento DATE,
                
                -- SNAPSHOT METODOLÓGICO
                metodologia_momento TEXT,
                razonamiento_momento TEXT,
                marcadores_momento TEXT,
                
                -- CAMBIOS DETECTADOS
                cambios_desde_anterior TEXT,
                innovaciones_detectadas TEXT,
                abandonos_metodologicos TEXT,
                
                fecha_analisis TIMESTAMP
            )
            ''')
            
            # Tabla de redes de influencia
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS redes_influencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor_influenciador TEXT NOT NULL,
                autor_influenciado TEXT NOT NULL,
                
                tipo_influencia TEXT,
                intensidad_influencia REAL,
                evidencia_textual TEXT,
                contexto_influencia TEXT,
                
                fecha_deteccion TIMESTAMP,
                UNIQUE(autor_influenciador, autor_influenciado)
            )
            ''')
            
            # Tabla de escuelas de pensamiento
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS escuelas_pensamiento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_escuela TEXT UNIQUE NOT NULL,
                descripcion_metodologica TEXT,
                
                autores_principales TEXT,
                caracteristicas_comunes TEXT,
                periodo_predominio TEXT,
                region_geografica TEXT,
                
                fecha_identificacion TIMESTAMP
            )
            ''')
            
            conn.commit()
            conn.close()
            
            print("✅ Base de datos autor-céntrica inicializada correctamente")
            
        except Exception as e:
            print(f"❌ Error inicializando DB autor-céntrica: {e}")
    
    def migrar_datos_existentes(self):
        """
        Migra datos del sistema actual al enfoque autor-céntrico
        """
        print("🔄 Iniciando migración a sistema autor-céntrico...")
        
        try:
            # Conectar a la DB cognitiva existente
            conn_orig = sqlite3.connect(self.db_cognitiva)
            df_original = pd.read_sql_query("SELECT * FROM perfiles_cognitivos", conn_orig)
            conn_orig.close()
            
            print(f"📊 Encontrados {len(df_original)} perfiles existentes")
            
            # Procesar cada autor para crear perfil expandido
            conn_dest = sqlite3.connect(self.db_autor_centrico)
            cursor_dest = conn_dest.cursor()
            
            autores_procesados = 0
            
            for autor in df_original['autor'].unique():
                perfil_expandido = self._crear_perfil_autoral_expandido(autor, df_original)
                
                if perfil_expandido:
                    cursor_dest.execute('''
                    INSERT OR REPLACE INTO perfiles_autorales_expandidos 
                    (autor, metodologia_principal, patron_razonamiento_dominante, 
                     estilo_argumentativo, marcadores_linguisticos, uso_ethos, uso_pathos, uso_logos,
                     total_documentos, fecha_primera_actualizacion, version_perfil)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', perfil_expandido)
                    
                    autores_procesados += 1
            
            conn_dest.commit()
            conn_dest.close()
            
            print(f"✅ Migración completada: {autores_procesados} perfiles expandidos")
            
            # Generar comparativas iniciales
            self._generar_comparativas_iniciales()
            
        except Exception as e:
            print(f"❌ Error en migración: {e}")
    
    def _crear_perfil_autoral_expandido(self, autor: str, datos_originales: pd.DataFrame) -> Optional[Tuple]:
        """
        Crea un perfil autoral expandido desde datos existentes
        """
        try:
            # Filtrar datos del autor
            autor_data = datos_originales[datos_originales['autor'] == autor]
            
            if autor_data.empty:
                return None
            
            # Promediar métricas cognitivas
            formalismo = autor_data['formalismo'].mean()
            creatividad = autor_data['creatividad'].mean()
            dogmatismo = autor_data['dogmatismo'].mean()
            empirismo = autor_data['empirismo'].mean()
            interdisciplinariedad = autor_data['interdisciplinariedad'].mean()
            abstraccion = autor_data['abstraccion'].mean()
            complejidad = autor_data['complejidad_sintactica'].mean()
            jurisprudencia = autor_data['uso_jurisprudencia'].mean()
            
            # Determinar metodología principal
            metodologia = self._determinar_metodologia_principal({
                'formalismo': formalismo,
                'creatividad': creatividad,
                'dogmatismo': dogmatismo,
                'empirismo': empirismo
            })
            
            # Determinar patrón de razonamiento
            patron_razonamiento = self._determinar_patron_razonamiento({
                'abstraccion': abstraccion,
                'empirismo': empirismo,
                'jurisprudencia': jurisprudencia
            })
            
            # Determinar estilo argumentativo
            estilo = self._determinar_estilo_argumentativo({
                'complejidad': complejidad,
                'formalismo': formalismo,
                'creatividad': creatividad
            })
            
            # Simular análisis aristotélico (se mejorará con datos reales)
            ethos = (formalismo + jurisprudencia) / 2
            pathos = (creatividad + (1 - dogmatismo)) / 2
            logos = (abstraccion + complejidad) / 2
            
            return (
                autor,
                metodologia,
                patron_razonamiento,
                estilo,
                json.dumps(self._extraer_marcadores_linguisticos(autor_data)),
                ethos,
                pathos,
                logos,
                len(autor_data),
                datetime.now().isoformat(),
                "v1.0_migracion"
            )
            
        except Exception as e:
            print(f"❌ Error creando perfil para {autor}: {e}")
            return None
    
    def _determinar_metodologia_principal(self, metricas: Dict[str, float]) -> str:
        """
        Determina la metodología principal basada en métricas cognitivas
        """
        if metricas['formalismo'] > 0.7:
            return "Formalista-Positivista"
        elif metricas['creatividad'] > 0.7:
            return "Innovadora-Propositiva"
        elif metricas['empirismo'] > 0.7:
            return "Empírico-Casuística"
        elif metricas['dogmatismo'] > 0.7:
            return "Dogmática-Tradicional"
        else:
            return "Ecléctica-Balanceada"
    
    def _determinar_patron_razonamiento(self, metricas: Dict[str, float]) -> str:
        """
        Determina el patrón de razonamiento dominante
        """
        if metricas['abstraccion'] > 0.7:
            return "Deductivo-Abstracto"
        elif metricas['empirismo'] > 0.7:
            return "Inductivo-Empirico"
        elif metricas['jurisprudentia'] > 0.7:
            return "Analogico-Precedental"
        else:
            return "Mixto-Integrador"
    
    def _determinar_estilo_argumentativo(self, metricas: Dict[str, float]) -> str:
        """
        Determina el estilo argumentativo característico
        """
        if metricas['complejidad'] > 0.7 and metricas['formalismo'] > 0.6:
            return "Académico-Riguroso"
        elif metricas['creatividad'] > 0.7:
            return "Innovador-Propositivo"
        elif metricas['formalismo'] > 0.7:
            return "Técnico-Especializado"
        else:
            return "Divulgativo-Accesible"
    
    def _extraer_marcadores_linguisticos(self, autor_data: pd.DataFrame) -> List[str]:
        """
        Extrae marcadores lingüísticos característicos (placeholder)
        """
        # Aquí se implementará análisis NLP avanzado
        return [
            "uso_formal_tercera_persona",
            "densidad_terminologia_tecnica",
            "estructura_silogistica",
            "referencias_doctrinarias"
        ]
    
    def _generar_comparativas_iniciales(self):
        """
        Genera comparativas entre todos los autores
        """
        print("🔍 Generando comparativas inter-autorales...")
        
        try:
            conn = sqlite3.connect(self.db_autor_centrico)
            
            # Obtener todos los autores
            autores = pd.read_sql_query("SELECT autor FROM perfiles_autorales_expandidos", conn)['autor'].tolist()
            
            cursor = conn.cursor()
            comparativas_creadas = 0
            
            # Generar comparativas por pares
            for i, autor_a in enumerate(autores):
                for autor_b in autores[i+1:]:
                    similitud = self._calcular_similitud_metodologica(autor_a, autor_b, conn)
                    
                    cursor.execute('''
                    INSERT OR REPLACE INTO comparativas_autorales
                    (autor_a, autor_b, similitud_metodologica, fecha_analisis)
                    VALUES (?, ?, ?, ?)
                    ''', (autor_a, autor_b, similitud, datetime.now().isoformat()))
                    
                    comparativas_creadas += 1
            
            conn.commit()
            conn.close()
            
            print(f"✅ Creadas {comparativas_creadas} comparativas autorales")
            
        except Exception as e:
            print(f"❌ Error generando comparativas: {e}")
    
    def _calcular_similitud_metodologica(self, autor_a: str, autor_b: str, conn) -> float:
        """
        Calcula similitud metodológica entre dos autores
        """
        try:
            # Obtener perfiles de ambos autores
            query = "SELECT * FROM perfiles_autorales_expandidos WHERE autor IN (?, ?)"
            perfiles = pd.read_sql_query(query, conn, params=(autor_a, autor_b))
            
            if len(perfiles) != 2:
                return 0.0
            
            # Calcular similitud basada en características
            perfil_a = perfiles.iloc[0]
            perfil_b = perfiles.iloc[1]
            
            similitudes = []
            
            # Similitud en uso aristotélico
            if pd.notna(perfil_a['uso_ethos']) and pd.notna(perfil_b['uso_ethos']):
                similitudes.append(1 - abs(perfil_a['uso_ethos'] - perfil_b['uso_ethos']))
                similitudes.append(1 - abs(perfil_a['uso_pathos'] - perfil_b['uso_pathos']))
                similitudes.append(1 - abs(perfil_a['uso_logos'] - perfil_b['uso_logos']))
            
            # Similitud metodológica (categórica)
            if perfil_a['metodologia_principal'] == perfil_b['metodologia_principal']:
                similitudes.append(1.0)
            else:
                similitudes.append(0.3)  # Similitud parcial
            
            return np.mean(similitudes) if similitudes else 0.5
            
        except Exception as e:
            print(f"❌ Error calculando similitud {autor_a} vs {autor_b}: {e}")
            return 0.0
    
    def generar_reporte_autor_centrico(self) -> str:
        """
        Genera reporte completo del sistema autor-céntrico
        """
        try:
            conn = sqlite3.connect(self.db_autor_centrico)
            
            # Estadísticas generales
            total_autores = pd.read_sql_query("SELECT COUNT(*) as total FROM perfiles_autorales_expandidos", conn).iloc[0]['total']
            total_comparativas = pd.read_sql_query("SELECT COUNT(*) as total FROM comparativas_autorales", conn).iloc[0]['total']
            
            # Top metodologías
            metodologias = pd.read_sql_query('''
                SELECT metodologia_principal, COUNT(*) as cantidad 
                FROM perfiles_autorales_expandidos 
                GROUP BY metodologia_principal 
                ORDER BY cantidad DESC
            ''', conn)
            
            # Top similitudes
            similitudes = pd.read_sql_query('''
                SELECT autor_a, autor_b, similitud_metodologica 
                FROM comparativas_autorales 
                ORDER BY similitud_metodologica DESC 
                LIMIT 10
            ''', conn)
            
            conn.close()
            
            # Generar reporte
            reporte = f"""
🧠 REPORTE SISTEMA AUTOR-CÉNTRICO
=================================

📊 ESTADÍSTICAS GENERALES:
- Total de autores analizados: {total_autores}
- Total de comparativas generadas: {total_comparativas}
- Cobertura comparativa: {(total_comparativas / (total_autores * (total_autores-1) / 2) * 100):.1f}%

🎯 METODOLOGÍAS DETECTADAS:
"""
            
            for _, row in metodologias.head(5).iterrows():
                reporte += f"- {row['metodologia_principal']}: {row['cantidad']} autores\n"
            
            reporte += f"\n🤝 TOP SIMILITUDES METODOLÓGICAS:\n"
            
            for _, row in similitudes.head(5).iterrows():
                reporte += f"- {row['autor_a']} ↔️ {row['autor_b']}: {row['similitud_metodologica']:.3f}\n"
            
            reporte += f"\n📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            
            return reporte
            
        except Exception as e:
            return f"❌ Error generando reporte: {e}"

def main():
    """
    Función principal para ejecutar la migración
    """
    print("🚀 INICIANDO SISTEMA AUTOR-CÉNTRICO")
    print("=" * 50)
    
    sistema = SistemaAutorCentrico()
    
    # Migrar datos existentes
    sistema.migrar_datos_existentes()
    
    # Generar reporte
    reporte = sistema.generar_reporte_autor_centrico()
    print("\n" + reporte)
    
    # Guardar reporte
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_reporte = f"reporte_autor_centrico_{timestamp}.txt"
    
    with open(archivo_reporte, 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    print(f"\n💾 Reporte guardado en: {archivo_reporte}")
    print("\n✅ SISTEMA AUTOR-CÉNTRICO INICIALIZADO")

if __name__ == "__main__":
    main()