import sqlite3
from datetime import datetime
import json
import os

DB_PATH = "colaborative/data/autoaprendizaje.db"

# ================================================================
# 🔹 Crear base de datos si no existe
# ================================================================
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS autoevaluaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        modelo TEXT,
        pregunta TEXT,
        concepto TEXT,
        autoevaluacion TEXT,
        puntaje REAL DEFAULT 0,
        prompt_base TEXT
    )
    """)
    conn.commit()
    conn.close()

# ================================================================
# 🔹 Guardar resultado doctrinario + autoevaluación
# ================================================================
def guardar_autoevaluacion(modelo, pregunta, concepto, autoevaluacion, puntaje, prompt_base):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO autoevaluaciones (fecha, modelo, pregunta, concepto, autoevaluacion, puntaje, prompt_base)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          modelo, pregunta, concepto, autoevaluacion, puntaje, prompt_base))
    conn.commit()
    conn.close()

# ================================================================
# 🔹 Recuperar las últimas N autoevaluaciones (para análisis o ajuste)
# ================================================================
def obtener_autoevaluaciones(limit=10):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT fecha, modelo, pregunta, puntaje, autoevaluacion FROM autoevaluaciones ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

# ================================================================
# 🔹 Generar resumen estadístico (para ajustar el prompt)
# ================================================================
def generar_contexto_adaptativo():
    """
    Lee las últimas autoevaluaciones y genera un resumen textual
    para ajustar dinámicamente el prompt doctrinario.
    """
    autoevals = obtener_autoevaluaciones(15)
    if not autoevals:
        return "Sin datos previos. Mantener prompt base original."
    
    analisis = "Resumen de las últimas autoevaluaciones:\n"
    total_puntaje, count = 0, 0
    for fecha, modelo, pregunta, puntaje, texto in autoevals:
        analisis += f"- [{fecha}] Modelo {modelo}: {puntaje}/10 → {texto[:120]}...\n"
        if puntaje:
            total_puntaje += puntaje
            count += 1

    promedio = round(total_puntaje / count, 2) if count else 0
    analisis += f"\nPromedio general de calidad doctrinaria: {promedio}/10.\n"
    analisis += "Usar este contexto para ajustar tono, precisión y profundidad.\n"
    return analisis