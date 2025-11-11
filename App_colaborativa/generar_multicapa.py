#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "colaborative" / "scripts"))

from biblioteca_multicapa_integrada import BibliotecaIntegrada

print("\n" + "="*80)
print("🧠 GENERANDO BIBLIOTECA MULTI-CAPA INTEGRADA")
print("="*80 + "\n")

biblioteca = BibliotecaIntegrada()

# Verificar bases de datos
print("📊 Verificando bases de datos...")
info = biblioteca.verificar_bases_datos()
print(f"   ✅ metadatos.db: {info['metadatos_db']['registros']} registros")
print(f"   ✅ multicapa_db: existe = {info['multicapa_db']['existe']}\n")

# Generar HTML
print("🧪 Generando análisis multi-capa...")
html = biblioteca.generar_html_completo()

output_path = Path(__file__).parent / "biblioteca_multicapa.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Archivo generado: {output_path.name}")
print(f"📊 Tamaño: {len(html):,} caracteres")
print(f"\n🌐 Para visualizar:")
print(f"   python servidor_http_simple.py")
print(f"   Luego abre: http://127.0.0.1:8888/biblioteca_multicapa.html\n")
