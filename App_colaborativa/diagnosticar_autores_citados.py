#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO: Extracción de Autores Citados
==============================================
Verifica por qué no se detectan autores citados en los informes
"""

import sys
sys.path.insert(0, 'colaborative/scripts')

from analizador_enriquecido_rag import AnalizadorEnriquecidoRAG
import fitz  # PyMuPDF

print("\n" + "="*70)
print("🔍 DIAGNÓSTICO: Detección de Autores Citados")
print("="*70 + "\n")

# Probar con documento de Luciana B. Scotti
pdf_path = "colaborative/data/pdfs/general/CONTRATOS ELECTRONICOS - Luciana B. Scotti.pdf"

print(f"📄 Documento: {pdf_path}")
print("-" * 70)

# 1. Extraer texto del PDF
try:
    doc = fitz.open(pdf_path)
    texto_completo = ""
    for page in doc:
        texto_completo += page.get_text()
    doc.close()
    
    print(f"✅ Texto extraído: {len(texto_completo)} caracteres")
    print(f"   Palabras aproximadas: {len(texto_completo.split())}")
except Exception as e:
    print(f"❌ Error extrayendo texto: {e}")
    sys.exit(1)

# 2. Mostrar muestra del texto
print(f"\n📝 Muestra del texto (primeros 500 caracteres):")
print("-" * 70)
print(texto_completo[:500])
print("...")

# 3. Buscar patrones de citación manualmente
import re

print(f"\n🔍 Buscando patrones de citación en el texto...")
print("-" * 70)

patrones_test = {
    'según X': r'según\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})',
    'X sostiene': r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\s+sostiene',
    'X afirma': r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\s+afirma',
    'X señala': r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\s+señala',
    '(X, 2024)': r'\(([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3}),\s*\d{4}\)',
    'cita X': r'cita\s+a\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})',
    'X (año)': r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\s+\(\d{4}\)',
}

resultados_patrones = {}
for nombre_patron, patron in patrones_test.items():
    matches = re.findall(patron, texto_completo[:50000], re.IGNORECASE | re.UNICODE)  # Primeras páginas
    if matches:
        resultados_patrones[nombre_patron] = matches[:5]  # Primeros 5 resultados
        print(f"  ✅ {nombre_patron}: {len(matches)} coincidencias")
        for i, match in enumerate(matches[:3], 1):
            print(f"     {i}. {match}")
    else:
        print(f"  ❌ {nombre_patron}: Sin coincidencias")

# 4. Usar AnalizadorEnriquecidoRAG
print(f"\n🔧 Usando AnalizadorEnriquecidoRAG.extraer_autores_citados()...")
print("-" * 70)

analizador = AnalizadorEnriquecidoRAG()
autores_citados = analizador.extraer_autores_citados(texto_completo)

if autores_citados:
    print(f"✅ Autores detectados: {len(autores_citados)}")
    print("\nTop 10:")
    for i, (autor, freq) in enumerate(list(autores_citados.items())[:10], 1):
        print(f"  {i}. {autor}: {freq} menciones")
else:
    print("❌ NO se detectaron autores citados")
    print("\n💡 Posibles causas:")
    print("   1. El PDF no contiene citas de autores en formato reconocible")
    print("   2. Los patrones de regex no coinciden con el formato usado")
    print("   3. El texto extraído no conserva el formato original")
    print("   4. Los nombres están en mayúsculas o minúsculas completas")

# 5. Buscar referencias bibliográficas al final
print(f"\n📚 Buscando sección de referencias/bibliografía...")
print("-" * 70)

secciones_biblio = ['referencias', 'bibliografía', 'bibliography', 'references', 'fuentes', 'obras citadas']
for seccion in secciones_biblio:
    patron_seccion = rf'\b{seccion}\b'
    if re.search(patron_seccion, texto_completo, re.IGNORECASE):
        # Extraer últimas 5000 caracteres (donde suele estar la bibliografía)
        texto_final = texto_completo[-5000:]
        print(f"  ✅ Encontrada sección: '{seccion}'")
        print(f"\n  Muestra de bibliografía:")
        print("  " + "-" * 66)
        # Buscar líneas que parezcan referencias
        lineas = texto_final.split('\n')
        referencias = [l for l in lineas if len(l) > 20 and ',' in l][:5]
        for ref in referencias:
            print(f"  {ref[:60]}...")
        break
else:
    print("  ⚠️ No se encontró sección de referencias identificable")

# 6. Análisis completo con analizador
print(f"\n🧪 Análisis completo del documento...")
print("-" * 70)

try:
    resultado_completo = analizador.analizar_documento_completo(pdf_path)
    
    print(f"✅ Análisis completado")
    print(f"\n📊 Datos obtenidos:")
    print(f"  • Autores citados: {len(resultado_completo.get('autores_citados', {}))}")
    print(f"  • Palabras clave: {len(resultado_completo.get('palabras_clave', {}))}")
    print(f"  • Posiciones doctrinales: {len(resultado_completo.get('posiciones_doctrinales', {}))}")
    
    if resultado_completo.get('autor_referencia_principal'):
        ref = resultado_completo['autor_referencia_principal']
        print(f"  ⭐ Autor de referencia: {ref.get('nombre')} ({ref.get('menciones')} menciones)")
    else:
        print(f"  ⚠️ No se identificó autor de referencia principal")
        
except Exception as e:
    print(f"❌ Error en análisis: {e}")
    import traceback
    traceback.print_exc()

# 7. Recomendaciones
print(f"\n💡 RECOMENDACIONES:")
print("="*70)

if not autores_citados:
    print("""
1. VERIFICAR FORMATO DEL PDF:
   - Asegurarse que el PDF tenga texto extraíble (no imagen escaneada)
   - Verificar que las citas sigan formatos académicos estándar
   
2. AMPLIAR PATRONES DE DETECCIÓN:
   - Agregar más patrones de citación específicos del documento
   - Incluir variaciones en mayúsculas/minúsculas
   - Detectar formato de notas al pie
   
3. USAR SECCIÓN DE REFERENCIAS:
   - Extraer autores directamente de la bibliografía
   - Parsear referencias en formato APA, Chicago, etc.
   
4. ANÁLISIS MANUAL TEMPORAL:
   - Agregar autores manualmente en base de datos
   - Crear campo "autores_citados_manual" en perfiles
   
5. MEJORAR EXTRACCIÓN:
   - Usar OCR si es PDF escaneado
   - Procesar notas al pie separadamente
   - Detectar formato específico de citas del autor
""")
else:
    print("""
✅ El sistema está detectando autores correctamente.
   
Si no aparecen en el informe de Gemini, verificar:
1. Que el campo 'autores_citados' esté en los datos enviados al prompt
2. Que Gemini no esté ignorando la sección por falta de contexto
3. Que el prompt incluya instrucciones claras sobre autores citados
""")

print("\n" + "="*70)
