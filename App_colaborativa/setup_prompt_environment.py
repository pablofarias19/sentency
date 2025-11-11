import os

# ============================================================
# CONFIGURACIÓN DE ESTRUCTURA
# ============================================================

BASE_DIR = "colaborative"
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

def crear_directorio(path):
    os.makedirs(path, exist_ok=True)
    print(f"📁 Creado: {path}")

# ============================================================
# CONTENIDOS DE LOS ARCHIVOS
# ============================================================

analisis_legal_yaml = """name: "Análisis Legal Profundo"
description: "Analiza documentos jurídicos detectando fundamentos, doctrina y jurisprudencia aplicable."
model: "gemini-pro"
temperature: 0.3
max_output_tokens: 1024

system_prompt: |
  Eres un analista jurídico experto en derecho argentino, con dominio procesal y sustantivo.
  Identifica fundamentos normativos, argumentos y estrategias del texto proporcionado.
  Escribe de forma profesional y estructurada.

user_prompt: |
  Analiza el siguiente texto jurídico y produce un informe con:
  1️⃣ Fundamentos normativos principales.
  2️⃣ Argumentos de la parte actora y demandada.
  3️⃣ Jurisprudencia relacionada (si se menciona o deduce).
  4️⃣ Riesgos legales o contradicciones observadas.

  Texto a analizar:
  ---
  {texto}
  ---
"""

ai_engine_py = """import os
import yaml
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("❌ No se encontró GEMINI_API_KEY. Colócala en tu archivo .env.")

genai.configure(api_key=API_KEY)

def cargar_prompt(ruta_prompt):
    with open(ruta_prompt, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ejecutar_prompt(prompt_path, texto):
    data = cargar_prompt(prompt_path)
    model_name = data.get("model", "gemini-pro")
    modelo = genai.GenerativeModel(model_name)

    full_prompt = data["user_prompt"].replace("{texto}", texto)
    system_prompt = data.get("system_prompt", "")

    response = modelo.generate_content(
        f"{system_prompt}\\n\\n{full_prompt}",
        generation_config=genai.types.GenerationConfig(
            temperature=data.get("temperature", 0.5),
            max_output_tokens=data.get("max_output_tokens", 1024)
        )
    )
    return response.text.strip()

if __name__ == "__main__":
    texto_demo = "La parte actora promovió demanda por incumplimiento contractual..."
    salida = ejecutar_prompt("colaborative/prompts/analisis_legal.yaml", texto_demo)
    print("🧠 RESULTADO:\\n", salida)
"""

prompt_manager_py = """import os
import yaml
from ai_engine import ejecutar_prompt

PROMPTS_DIR = "colaborative/prompts/"

def listar_prompts():
    archivos = [f for f in os.listdir(PROMPTS_DIR) if f.endswith(".yaml")]
    for i, archivo in enumerate(archivos, start=1):
        with open(os.path.join(PROMPTS_DIR, archivo), "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f)
        print(f"{i}. {meta.get('name', archivo)} → {archivo}")
        print(f"   Descripción: {meta.get('description', 'Sin descripción')}\\n")
    return archivos

def seleccionar_prompt():
    prompts = listar_prompts()
    seleccion = int(input("Seleccioná un prompt por número: ")) - 1
    if seleccion < 0 or seleccion >= len(prompts):
        print("Selección inválida.")
        return None
    return os.path.join(PROMPTS_DIR, prompts[seleccion])

def main():
    print("🧩 GESTOR DE PROMPTS - IA GEMINI")
    print("================================\\n")
    ruta = seleccionar_prompt()
    if not ruta:
        return
    texto = input("\\n📄 Ingresá el texto o párrafo jurídico a analizar:\\n> ")
    print("\\n⏳ Ejecutando análisis...\\n")
    salida = ejecutar_prompt(ruta, texto)
    print("🧠 RESULTADO:\\n")
    print(salida)

if __name__ == "__main__":
    main()
"""

prompt_webapp_py = """import os
import yaml
from flask import Flask, render_template, request, redirect, url_for, flash
from ai_engine import ejecutar_prompt
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = "colaborative_secret"
PROMPTS_DIR = "colaborative/prompts/"

@app.route("/")
def index():
    prompts = []
    for archivo in os.listdir(PROMPTS_DIR):
        if archivo.endswith(".yaml"):
            ruta = os.path.join(PROMPTS_DIR, archivo)
            with open(ruta, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            prompts.append({
                "nombre": data.get("name", archivo),
                "archivo": archivo,
                "descripcion": data.get("description", "")
            })
    return render_template("index.html", prompts=prompts)

@app.route("/editar/<archivo>", methods=["GET", "POST"])
def editar(archivo):
    ruta = os.path.join(PROMPTS_DIR, archivo)
    if request.method == "POST":
        contenido = request.form["contenido"]
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        flash(f"✅ Prompt '{archivo}' guardado correctamente.", "success")
        return redirect(url_for("index"))
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()
    return render_template("editor.html", archivo=archivo, contenido=contenido)

@app.route("/ejecutar/<archivo>", methods=["GET", "POST"])
def ejecutar(archivo):
    ruta = os.path.join(PROMPTS_DIR, archivo)
    if request.method == "POST":
        texto = request.form["texto"]
        try:
            salida = ejecutar_prompt(ruta, texto)
            return render_template("resultado.html", texto=texto, salida=salida, archivo=archivo)
        except Exception as e:
            flash(f"❌ Error al ejecutar el prompt: {str(e)}", "error")
            return redirect(url_for("index"))
    return render_template("resultado.html", archivo=archivo)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
"""

index_html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Prompts Colaborative</title>
  <style>
    body { font-family: Arial; background: #0b1020; color: #e8ecf1; margin: 0; padding: 2em; }
    .card { background: #121a33; padding: 16px; border-radius: 12px; margin-bottom: 16px; }
    .btn { background: #2e6ef7; color: white; padding: 8px 12px; border: 0; border-radius: 8px; cursor: pointer; margin-right: 6px; }
    a { color: #9dc1ff; text-decoration: none; }
  </style>
</head>
<body>
  <h1>🧩 Prompts disponibles</h1>
  {% for p in prompts %}
    <div class="card">
      <h3>{{p.nombre}}</h3>
      <p>{{p.descripcion}}</p>
      <a href="{{url_for('editar', archivo=p.archivo)}}" class="btn">✏️ Editar</a>
      <a href="{{url_for('ejecutar', archivo=p.archivo)}}" class="btn" style="background:#fbbc05;">⚙️ Ejecutar</a>
    </div>
  {% endfor %}
</body>
</html>
"""

editor_html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Editar Prompt - {{archivo}}</title>
  <style>
    body { background: #0b1020; color: #e8ecf1; font-family: Arial; padding: 2em; }
    textarea { width: 100%; height: 80vh; border-radius: 8px; padding: 1em; background: #101a3b; color: #e8ecf1; }
    button { margin-top: 10px; padding: 10px 14px; background: #2e6ef7; color: white; border: 0; border-radius: 8px; cursor: pointer; }
  </style>
</head>
<body>
  <h1>✏️ Editar: {{archivo}}</h1>
  <form method="POST">
    <textarea name="contenido">{{contenido}}</textarea>
    <br><button type="submit">💾 Guardar cambios</button>
  </form>
</body>
</html>
"""

resultado_html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Resultado IA - {{archivo}}</title>
  <style>
    body { background: #0b1020; color: #e8ecf1; font-family: Arial; padding: 2em; }
    textarea { width: 100%; height: 200px; border-radius: 8px; padding: 1em; background: #101a3b; color: #e8ecf1; }
    pre { background: #101a3b; padding: 1em; border-radius: 8px; white-space: pre-wrap; }
    button { background: #2e6ef7; color: white; padding: 10px 14px; border: 0; border-radius: 8px; cursor: pointer; margin-top: 10px; }
  </style>
</head>
<body>
  <h1>⚙️ Ejecutar prompt: {{archivo}}</h1>
  <form method="POST">
    <textarea name="texto" placeholder="Pegá aquí el texto a analizar...">{{texto}}</textarea>
    <br><button type="submit">🚀 Ejecutar IA</button>
  </form>
  {% if salida %}
    <h2>🧠 Resultado:</h2>
    <pre>{{salida}}</pre>
  {% endif %}
</body>
</html>
"""

# ============================================================
# CREACIÓN DE ARCHIVOS
# ============================================================

def crear_archivo(ruta, contenido):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"📝 Archivo creado: {ruta}")

def main():
    crear_directorio(PROMPTS_DIR)
    crear_directorio(SCRIPTS_DIR)
    crear_directorio(TEMPLATES_DIR)

    crear_archivo(os.path.join(PROMPTS_DIR, "analisis_legal.yaml"), analisis_legal_yaml)
    crear_archivo(os.path.join(SCRIPTS_DIR, "ai_engine.py"), ai_engine_py)
    crear_archivo(os.path.join(SCRIPTS_DIR, "prompt_manager.py"), prompt_manager_py)
    crear_archivo(os.path.join(SCRIPTS_DIR, "prompt_webapp.py"), prompt_webapp_py)
    crear_archivo(os.path.join(TEMPLATES_DIR, "index.html"), index_html)
    crear_archivo(os.path.join(TEMPLATES_DIR, "editor.html"), editor_html)
    crear_archivo(os.path.join(TEMPLATES_DIR, "resultado.html"), resultado_html)

    with open(os.path.join(BASE_DIR, ".env"), "w", encoding="utf-8") as f:
        f.write("GEMINI_API_KEY=\n")
    print("🔑 Archivo .env creado (agrega tu clave GEMINI_API_KEY)")

    print("\n✅ Entorno de prompts colaborativo configurado correctamente.")

if __name__ == "__main__":
    main()
