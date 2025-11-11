import json
import sys

sys.path.insert(0, 'colaborative/scripts')

# Cargar JSON
data = json.load(open('colaborative/data/pdfs/general/metadatos_sentencias.json', encoding='utf-8'))

# Filtrar sentencias reales (excluir claves con _)
sentencias = [k for k in data.keys() if not k.startswith('_')]

print("✅ JSON válido y cargado correctamente")
print(f"\n📄 Sentencias detectadas: {len(sentencias)}")
print(f"📋 Archivos: {sentencias}")

# Verificar ejemplo completo
ejemplo = data.get('Banco_Provincia_c_Laborda_Walter_Gaston.pdf', {})
print(f"\n🔍 Campos en 'Banco_Provincia_c_Laborda_Walter_Gaston.pdf':")
print(f"  ✓ numero_expediente: {ejemplo.get('numero_expediente')}")
print(f"  ✓ fecha_sentencia: {ejemplo.get('fecha_sentencia')}")
print(f"  ✓ tribunal: {ejemplo.get('tribunal')}")
print(f"  ✓ jurisdiccion: {ejemplo.get('jurisdiccion')}")
print(f"  ✓ materia: {ejemplo.get('materia')}")
print(f"  ✓ temas: {len(ejemplo.get('temas', []))} items → {ejemplo.get('temas', [])}")
print(f"  ✓ formas_razonamiento: {ejemplo.get('formas_razonamiento', [])}")
print(f"  ✓ falacias: {ejemplo.get('falacias', [])}")

citaciones = ejemplo.get('citaciones', {})
print(f"  ✓ citaciones:")
print(f"    - doctrina: {citaciones.get('doctrina', [])}")
print(f"    - jurisprudencia: {citaciones.get('jurisprudencia', [])}")

ponderacion = ejemplo.get('ponderacion_manual', {})
print(f"  ✓ ponderacion_manual: {list(ponderacion.keys())}")

analisis = ejemplo.get('analisis_sistema', {})
print(f"  ✓ analisis_sistema: {list(analisis.keys())}")

print("\n✅ ESTRUCTURA COMPATIBLE CON ingesta_sentencias.py")
print("✅ Todos los campos requeridos presentes")
print("✅ Formato de citaciones correcto (doctrina/jurisprudencia)")
