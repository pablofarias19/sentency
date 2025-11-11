# -*- coding: utf-8 -*-
"""
📊 REPORTE DE DISTANCIAS DOCTRINALES POR EXPEDIENTE/TRIBUNAL - V7.5
===================================================================

Genera reportes agregados de distancia doctrinal por:
- Expediente
- Tribunal  
- Jurisdicción
- Materia

Útil para identificar patrones de apartamiento doctrinal
por sala, juez o tipo de causa.

AUTOR: Sistema Cognitivo v7.5
FECHA: 10 NOV 2025
"""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
from config_rutas import PENSAMIENTO_DB

def crear_directorio_exports():
    """Crea directorio de exports si no existe"""
    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)
    return exports_dir

def generar_reporte_agregado():
    """Genera reporte agregado principal"""
    print("📊 GENERANDO REPORTE AGREGADO DE DISTANCIAS DOCTRINALES")
    print("=" * 60)
    
    if not Path(PENSAMIENTO_DB).exists():
        print(f"❌ Base de datos no encontrada: {PENSAMIENTO_DB}")
        return None
    
    try:
        con = sqlite3.connect(PENSAMIENTO_DB)
        
        # Verificar que existan datos
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM rag_sentencias_chunks WHERE distancia_doctrinal IS NOT NULL")
        total_con_distancia = cur.fetchone()[0]
        
        if total_con_distancia == 0:
            print("⚠️ No hay chunks con distancia doctrinal calculada")
            print("📋 Ejecutá primero: python update_distancia_doctrinal.py")
            con.close()
            return None
        
        print(f"📈 Procesando {total_con_distancia} chunks con distancia doctrinal...")
        
        # Query principal para agregación
        query = """
        SELECT 
            expediente,
            tribunal,
            jurisdiccion,
            materia,
            fecha_sentencia,
            COUNT(*) as chunks_total,
            AVG(distancia_doctrinal) as dist_promedio,
            MIN(distancia_doctrinal) as dist_minima,
            MAX(distancia_doctrinal) as dist_maxima,
            ROUND(AVG(distancia_doctrinal), 4) as dist_prom_redondeada,
            COUNT(CASE WHEN distancia_doctrinal <= 0.20 THEN 1 END) as chunks_alineados,
            COUNT(CASE WHEN distancia_doctrinal > 0.20 AND distancia_doctrinal <= 0.50 THEN 1 END) as chunks_moderados,
            COUNT(CASE WHEN distancia_doctrinal > 0.50 THEN 1 END) as chunks_apartados
        FROM rag_sentencias_chunks
        WHERE distancia_doctrinal IS NOT NULL
          AND expediente IS NOT NULL
          AND expediente != ''
        GROUP BY expediente, tribunal, jurisdiccion, materia, fecha_sentencia
        ORDER BY dist_promedio DESC
        """
        
        df = pd.read_sql_query(query, con)
        con.close()
        
        # Calcular porcentajes
        df['pct_alineados'] = (df['chunks_alineados'] / df['chunks_total'] * 100).round(1)
        df['pct_moderados'] = (df['chunks_moderados'] / df['chunks_total'] * 100).round(1)
        df['pct_apartados'] = (df['chunks_apartados'] / df['chunks_total'] * 100).round(1)
        
        # Categorizar nivel de apartamiento
        def categorizar_apartamiento(dist_prom):
            if dist_prom <= 0.20:
                return "🟢 Alineado"
            elif dist_prom <= 0.50:
                return "🟡 Moderado"
            else:
                return "🔴 Apartado"
        
        df['categoria_apartamiento'] = df['dist_prom_redondeada'].apply(categorizar_apartamiento)
        
        print(f"✅ Datos procesados: {len(df)} expedientes únicos")
        return df
        
    except Exception as e:
        print(f"❌ Error generando reporte: {e}")
        import traceback
        traceback.print_exc()
        return None

def generar_reportes_especializados(df):
    """Genera reportes especializados por dimensión"""
    if df is None or len(df) == 0:
        return
    
    exports_dir = crear_directorio_exports()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Reporte principal agregado
    main_file = exports_dir / f"distancia_doctrinal_agg_{timestamp}.csv"
    df.to_csv(main_file, index=False, encoding="utf-8-sig")
    print(f"✅ Reporte principal: {main_file}")
    
    # 2. Reporte por tribunal (ranking)
    tribunal_agg = (df.groupby(['tribunal', 'jurisdiccion'])
                   .agg({
                       'chunks_total': 'sum',
                       'dist_prom_redondeada': 'mean',
                       'chunks_alineados': 'sum',
                       'chunks_apartados': 'sum'
                   })
                   .reset_index())
    
    tribunal_agg = tribunal_agg.sort_values('dist_prom_redondeada', ascending=False)
    tribunal_agg['pct_apartados_tribunal'] = (tribunal_agg['chunks_apartados'] / tribunal_agg['chunks_total'] * 100).round(1)
    
    tribunal_file = exports_dir / f"ranking_tribunales_{timestamp}.csv"
    tribunal_agg.to_csv(tribunal_file, index=False, encoding="utf-8-sig")
    print(f"✅ Ranking tribunales: {tribunal_file}")
    
    # 3. Reporte por materia
    materia_agg = (df.groupby('materia')
                  .agg({
                      'chunks_total': 'sum',
                      'dist_prom_redondeada': 'mean',
                      'chunks_alineados': 'sum',
                      'chunks_apartados': 'sum'
                  })
                  .reset_index())
    
    materia_agg = materia_agg.sort_values('dist_prom_redondeada', ascending=False)
    materia_agg['pct_apartados_materia'] = (materia_agg['chunks_apartados'] / materia_agg['chunks_total'] * 100).round(1)
    
    materia_file = exports_dir / f"analisis_materias_{timestamp}.csv"
    materia_agg.to_csv(materia_file, index=False, encoding="utf-8-sig") 
    print(f"✅ Análisis por materia: {materia_file}")
    
    # 4. Top apartamientos (casos críticos)
    casos_criticos = df[df['dist_prom_redondeada'] > 0.60].copy()
    if len(casos_criticos) > 0:
        casos_criticos = casos_criticos.sort_values('dist_prom_redondeada', ascending=False)
        criticos_file = exports_dir / f"casos_criticos_apartamiento_{timestamp}.csv"
        casos_criticos.to_csv(criticos_file, index=False, encoding="utf-8-sig")
        print(f"🔴 Casos críticos (>0.60): {criticos_file} ({len(casos_criticos)} casos)")
    
    return {
        'principal': main_file,
        'tribunales': tribunal_file,
        'materias': materia_file,
        'criticos': criticos_file if len(casos_criticos) > 0 else None
    }

def mostrar_estadisticas_resumen(df):
    """Muestra estadísticas de resumen en consola"""
    if df is None or len(df) == 0:
        return
    
    print(f"\n📊 ESTADÍSTICAS GENERALES:")
    print(f"   Total expedientes analizados: {len(df)}")
    print(f"   Total chunks procesados: {df['chunks_total'].sum()}")
    print(f"   Distancia promedio global: {df['dist_prom_redondeada'].mean():.4f}")
    
    # Distribución por categorías
    alineados = len(df[df['categoria_apartamiento'] == "🟢 Alineado"])
    moderados = len(df[df['categoria_apartamiento'] == "🟡 Moderado"])
    apartados = len(df[df['categoria_apartamiento'] == "🔴 Apartado"])
    
    print(f"\n📈 DISTRIBUCIÓN POR APARTAMIENTO:")
    print(f"   🟢 Alineados (≤0.20): {alineados} expedientes ({alineados/len(df)*100:.1f}%)")
    print(f"   🟡 Moderados (0.20-0.50): {moderados} expedientes ({moderados/len(df)*100:.1f}%)")
    print(f"   🔴 Apartados (>0.50): {apartados} expedientes ({apartados/len(df)*100:.1f}%)")
    
    # Top 5 más apartados
    top_apartados = df.nlargest(5, 'dist_prom_redondeada')
    print(f"\n🔴 TOP 5 EXPEDIENTES MÁS APARTADOS:")
    for idx, row in top_apartados.iterrows():
        print(f"   {row['expediente']} | {row['tribunal']} | Dist: {row['dist_prom_redondeada']:.4f}")

def main():
    """Proceso principal de generación de reportes"""
    print("📊 GENERADOR DE REPORTES DE DISTANCIA DOCTRINAL V7.5")
    print("=" * 65)
    
    # Generar datos agregados
    df = generar_reporte_agregado()
    
    if df is not None:
        # Mostrar estadísticas
        mostrar_estadisticas_resumen(df)
        
        # Generar archivos de reporte
        archivos = generar_reportes_especializados(df)
        
        print(f"\n🎉 ¡Reportes generados exitosamente!")
        print(f"📁 Directorio: exports/")
        
        if archivos:
            print(f"📄 Archivos generados:")
            for tipo, archivo in archivos.items():
                if archivo:
                    print(f"   - {tipo}: {archivo.name}")
    
    else:
        print("❌ No se pudieron generar los reportes")

if __name__ == "__main__":
    main()