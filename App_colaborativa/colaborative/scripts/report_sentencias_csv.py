# -*- coding: utf-8 -*-
import sqlite3, pandas as pd
from pathlib import Path
from config_rutas import PENSAMIENTO_DB

def main():
    # Crear directorio de exports
    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)
    
    OUT_SENTENCIAS_CSV = exports_dir / "sentencias_chunks.csv"
    OUT_PIVOT_RAZONAMIENTO = exports_dir / "pivot_razonamiento_por_tribunal.csv"
    
    print("📊 Generando reportes CSV...")
    
    con = sqlite3.connect(PENSAMIENTO_DB)
    df = pd.read_sql_query("""
        SELECT expediente, fuente_pdf, fecha_sentencia, tribunal, jurisdiccion, materia,
               temas, formas_razonamiento, falacias, citaciones_doctrina, citaciones_jurisprudencia, length(texto) as largo
        FROM rag_sentencias_chunks
    """, con)
    con.close()

    if df.empty:
        print("⚠️ No hay datos en rag_sentencias_chunks. Ejecuta ingesta_sentencias.py primero.")
        return

    df.to_csv(OUT_SENTENCIAS_CSV, index=False, encoding="utf-8-sig")
    print(f"✅ Exportado: {OUT_SENTENCIAS_CSV} ({len(df)} registros)")

    # Pivot: cantidad de chunks por tribunal y tipo de razonamiento
    df2 = df.assign(raz=df["formas_razonamiento"].fillna(""))
    df2["raz"] = df2["raz"].apply(lambda s: [x.strip() for x in s.split(",") if x.strip()] if s else [])
    df_expanded = df2.explode("raz")
    
    if not df_expanded.empty and "raz" in df_expanded.columns:
        pv = df_expanded.pivot_table(index="tribunal", columns="raz", values="expediente", aggfunc="count", fill_value=0)
        pv.to_csv(OUT_PIVOT_RAZONAMIENTO, encoding="utf-8-sig")
        print(f"✅ Exportado: {OUT_PIVOT_RAZONAMIENTO}")
    else:
        print("⚠️ No se pudo generar pivot de razonamiento")

    print(f"✅ Reportes listos en: {exports_dir}")

if __name__ == "__main__":
    main()