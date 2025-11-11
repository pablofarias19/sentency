#!/usr/bin/env python3
import sys
from pathlib import Path

# Agregar ruta de scripts
sys.path.insert(0, str(Path(__file__).parent / "colaborative" / "scripts"))

from biblioteca_cognitiva_gemini import BibliotecaCognitivaGemini

print("\n" + "="*80)
print("🧪 GENERANDO BIBLIOTECA CON ANÁLISIS INTERPRETATIVO DE GEMINI")
print("="*80)
print("\n📊 Conectando a base de datos...")

biblioteca = BibliotecaCognitivaGemini()
html = biblioteca.generar_pagina_principal_html()

output_path = Path(__file__).parent / "biblioteca_con_gemini.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Archivo generado: {output_path.name}")
print(f"📊 Tamaño: {len(html):,} caracteres")
print(f"\n🌐 Para ver en navegador:")
print(f"   python servidor_http_simple.py")
print(f"   Luego abre: http://127.0.0.1:8888/biblioteca_con_gemini.html\n")
