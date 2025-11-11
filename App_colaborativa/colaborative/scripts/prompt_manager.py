import os
import yaml
from ai_engine import ejecutar_prompt

PROMPTS_DIR = "colaborative/prompts/"

def listar_prompts():
    archivos = [f for f in os.listdir(PROMPTS_DIR) if f.endswith(".yaml")]
    for i, archivo in enumerate(archivos, start=1):
        with open(os.path.join(PROMPTS_DIR, archivo), "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f)
        print(f"{i}. {meta.get('name', archivo)} → {archivo}")
        print(f"   Descripción: {meta.get('description', 'Sin descripción')}\n")
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
    print("================================\n")
    ruta = seleccionar_prompt()
    if not ruta:
        return
    texto = input("\n📄 Ingresá el texto o párrafo jurídico a analizar:\n> ")
    print("\n⏳ Ejecutando análisis...\n")
    salida = ejecutar_prompt(ruta, texto)
    print("🧠 RESULTADO:\n")
    print(salida)

if __name__ == "__main__":
    main()
