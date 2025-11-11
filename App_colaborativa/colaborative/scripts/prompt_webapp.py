import os
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
