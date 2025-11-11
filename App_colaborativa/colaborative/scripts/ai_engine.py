import os
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
        f"{system_prompt}\n\n{full_prompt}",
        generation_config=genai.types.GenerationConfig(
            temperature=data.get("temperature", 0.5),
            max_output_tokens=data.get("max_output_tokens", 1024)
        )
    )
    return response.text.strip()

if __name__ == "__main__":
    texto_demo = "La parte actora promovió demanda por incumplimiento contractual..."
    salida = ejecutar_prompt("colaborative/prompts/analisis_legal.yaml", texto_demo)
    print("🧠 RESULTADO:\n", salida)
