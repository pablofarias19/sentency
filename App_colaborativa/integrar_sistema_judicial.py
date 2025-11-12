#!/usr/bin/env python3
"""
Script para integrar sistema judicial en end2end_webapp.py
"""

import re

# Leer el archivo original
with open('colaborative/scripts/end2end_webapp.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# ============================================================================
# 1. AGREGAR IMPORTS JUDICIALES (después de línea ~127)
# ============================================================================

imports_judiciales = '''
# ====================================
# Importar Sistema Judicial Argentina
# ====================================
try:
    from webapp_rutas_judicial import registrar_rutas_judicial, init_sistema_judicial
    from analyser_judicial_adapter import BibliotecaJudicial
    SISTEMA_JUDICIAL_DISPONIBLE = True
    print("✅ Sistema Judicial Argentina cargado")
except ImportError as e:
    print(f"⚠️ Sistema Judicial no disponible: {e}")
    SISTEMA_JUDICIAL_DISPONIBLE = False
'''

# Insertar después de "generador_informes = None"
contenido = contenido.replace(
    "    generador_informes = None\n",
    "    generador_informes = None\n" + imports_judiciales + "\n"
)

# ============================================================================
# 2. AGREGAR INTEGRACIÓN DE RUTAS (antes de app.run())
# ============================================================================

integracion_judicial = '''
    # =============================================================================
    # ⚖️ SISTEMA JUDICIAL ARGENTINA - INTEGRACIÓN
    # =============================================================================
    if SISTEMA_JUDICIAL_DISPONIBLE:
        try:
            # Inicializar sistema judicial
            init_sistema_judicial()

            # Registrar rutas judiciales
            registrar_rutas_judicial(app)

            print("\\n" + "="*70)
            print("⚖️ SISTEMA JUDICIAL ARGENTINA INTEGRADO")
            print("="*70)
            print("\\n✅ Rutas judiciales disponibles:")
            print("   📋 Jueces:           http://127.0.0.1:5002/jueces")
            print("   👤 Perfil Juez:      http://127.0.0.1:5002/juez/<nombre>")
            print("   🧠 Cognitivo:        http://127.0.0.1:5002/cognitivo/<nombre>")
            print("   📜 Líneas:           http://127.0.0.1:5002/lineas/<nombre>")
            print("   🔗 Red Influencias:  http://127.0.0.1:5002/red/<nombre>")
            print("   🔮 Predictivo:       http://127.0.0.1:5002/prediccion/<nombre>")
            print("   📊 Informes:         http://127.0.0.1:5002/informes")
            print("   ❓ Preguntas:        http://127.0.0.1:5002/preguntas/<nombre>")
            print("\\n" + "="*70 + "\\n")

        except Exception as e:
            print(f"⚠️ Error integrando sistema judicial: {e}")
    else:
        print("⚠️ Sistema Judicial no disponible - verifica imports")

'''

# Insertar antes de app.run()
contenido = contenido.replace(
    '    # Iniciar Flask\n    app.run(host="127.0.0.1", port=5002, debug=False)',
    integracion_judicial + '\n    # Iniciar Flask\n    app.run(host="127.0.0.1", port=5002, debug=False)'
)

# ============================================================================
# 3. ACTUALIZAR MENSAJE DE BIENVENIDA
# ============================================================================

# Actualizar el mensaje final para incluir sistema judicial
contenido = contenido.replace(
    '    print("✅ Colaborative E2E listo en http://127.0.0.1:5002")',
    '    print("✅ Colaborative E2E + Sistema Judicial listo en http://127.0.0.1:5002")'
)

# Guardar el archivo modificado
with open('colaborative/scripts/end2end_webapp.py', 'w', encoding='utf-8') as f:
    f.write(contenido)

print("✅ Sistema judicial integrado en end2end_webapp.py")
print("   - Imports agregados")
print("   - Rutas registradas")
print("   - Mensajes actualizados")
