#!/usr/bin/env python3
import sys
from pathlib import Path

# Agregar ruta de scripts
sys.path.insert(0, str(Path(__file__).parent / "colaborative" / "scripts"))

from biblioteca_cognitiva_mejorada import BibliotecaCognitivaMejorada

print("\n" + "="*80)
print("🧪 Generando HTML de Biblioteca Mejorada v2.0")
print("="*80)
print("\n📊 Conectando a base de datos...")

biblioteca = BibliotecaCognitivaMejorada()
html = biblioteca.generar_pagina_principal_html()

output_path = Path(__file__).parent / "biblioteca_mejorada_completa.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Archivo generado: {output_path.name}")
print(f"📊 Tamaño: {len(html):,} caracteres")
print(f"\n🌐 Abre este archivo en tu navegador:")
print(f"   {output_path}\n")
