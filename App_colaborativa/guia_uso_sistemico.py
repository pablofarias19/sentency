"""
📋 GUÍA DE USO SISTEMÁTICO - CENTRO CONTROL MAESTRO
=================================================

Esta guía te ayuda a navegar el sistema de manera ordenada y eficiente,
organizando las funciones por FLUJOS DE TRABAJO lógicos.

AUTOR: Sistema Cognitivo v7.6
FECHA: 10 NOV 2025
"""

def mostrar_guia_flujos_trabajo():
    """Muestra los flujos de trabajo principales del sistema"""
    
    print("🎯 FLUJOS DE TRABAJO PRINCIPALES")
    print("=" * 60)
    
    flujos = {
        "🚀 FLUJO 1: ANÁLISIS DE SENTENCIAS (COMPLETO)": [
            "📥 PASO 1: Preparar datos",
            "   • Colocar PDFs de sentencias en: colaborative/data/pdfs/sentencias_pdf/",
            "   • O archivos TXT en: colaborative/data/pdfs/sentencias_texto/",
            "",
            "🔄 PASO 2: Ingesta y procesamiento (ORDEN OBLIGATORIO)",
            "   S1. Ingestar corpus de sentencias → Crea chunks en BD",
            "   S2. Construir índice FAISS → Permite búsquedas semánticas",
            "",
            "🔍 PASO 3: Búsquedas y consultas",
            "   S3. Buscar en corpus → Consultas con filtros",
            "   S4. Exportar reportes CSV → Datos para análisis externo",
            "   S5. API de sentencias → Integración web (puerto 5010)",
            "",
            "📊 RESULTADO: Sistema RAG funcional para sentencias"
        ],
        
        "📏 FLUJO 2: DISTANCIA DOCTRINAL": [
            "📥 PASO 1: Preparar doctrina de referencia",
            "   • Colocar PDFs doctrinales en: colaborative/data/pdfs/doctrina_pdf/",
            "   • O archivos TXT en: colaborative/data/pdfs/doctrina_texto/",
            "",
            "🏛️ PASO 2: Construir base doctrinal (PRERREQUISITO)",
            "   D1. Construir base doctrinal → Vector promedio de doctrina",
            "",
            "📏 PASO 3: Calcular apartamientos (REQUIERE SENTENCIAS INGERIDAS)",
            "   D2. Recalcular distancias → Mide apartamiento de cada chunk",
            "",
            "📊 PASO 4: Análisis y reportes",
            "   D3. Reportes por tribunal/materia → CSV agregados",
            "   D4. Casos críticos → Identifica apartamientos >0.60",
            "",
            "📊 RESULTADO: Métricas de apartamiento doctrinal cuantificadas"
        ],
        
        "🧠 FLUJO 3: INTERPRETACIÓN HERMENÉUTICA": [
            "🔧 PASO 1: Configuración (UNA SOLA VEZ)",
            "   G1. Configurar API Key GEMINI → https://makersuite.google.com/app/apikey",
            "",
            "🧪 PASO 2: Verificación",
            "   G4. Test de interpretación → Prueba con datos de ejemplo",
            "",
            "🚀 PASO 3: Uso en producción",
            "   G2. Servidor de interpretación → API en puerto 5060",
            "   G3. Interpretar chunk específico → Análisis individual",
            "",
            "📊 RESULTADO: Explicaciones hermenéuticas de apartamientos doctrinales"
        ],
        
        "👤 FLUJO 4: ANÁLISIS AUTORAL (TRADICIONAL)": [
            "📥 PASO 1: Preparar documentos",
            "   • Colocar PDFs en: colaborative/data/pdfs/general/",
            "",
            "🔄 PASO 2: Procesamiento",
            "   1. Procesar documentos doctrinarios → Análisis cognitivo",
            "   4. Analizar autor específico → Perfil individual",
            "   5. Comparar autores → Similaridades",
            "",
            "📊 PASO 3: Exportación",
            "   7. Exportar perfiles autorales → Datos estructurados",
            "",
            "📊 RESULTADO: Perfiles cognitivos de autores"
        ]
    }
    
    for titulo, pasos in flujos.items():
        print(f"\n{titulo}")
        print("-" * len(titulo.replace("🚀 ", "").replace("📏 ", "").replace("🧠 ", "").replace("👤 ", "")))
        
        for paso in pasos:
            if paso.strip():
                print(f"{paso}")
    
    print(f"\n🎯 RECOMENDACIÓN DE USO:")
    print("=" * 30)
    print("1️⃣ PRINCIPIANTES: Empezar con FLUJO 1 (Sentencias básico)")
    print("2️⃣ INTERMEDIO: Agregar FLUJO 2 (Distancia doctrinal)")
    print("3️⃣ AVANZADO: Completar con FLUJO 3 (Interpretación IA)")
    print("4️⃣ ESPECIALISTAS: FLUJO 4 para análisis de autoría")

def mostrar_orden_ejecucion():
    """Muestra el orden correcto de ejecución para evitar errores"""
    
    print("\n⚠️ ORDEN DE EJECUCIÓN CRÍTICO")
    print("=" * 40)
    
    orden_critico = [
        "🔴 CRÍTICO - Sin esto, nada funciona:",
        "   S1. Ingestar sentencias PRIMERO",
        "   S2. Construir FAISS DESPUÉS de S1",
        "",
        "🟡 IMPORTANTE - Para distancias doctrinales:",
        "   D1. Construir base doctrinal ANTES de D2",
        "   D2. Calcular distancias DESPUÉS de S1 y D1",
        "",
        "🟢 OPCIONAL - Para interpretación IA:",
        "   G1. Configurar GEMINI API ANTES que G2, G3, G4",
        "   G4. Probar ANTES de usar G2 o G3 en producción",
        "",
        "❌ ERRORES COMUNES:",
        "   • Intentar D2 sin haber hecho S1 (no hay sentencias)",
        "   • Intentar D2 sin haber hecho D1 (no hay base doctrinal)",
        "   • Usar G3 sin configurar G1 (no hay API key)",
        "   • Intentar S3 sin haber hecho S1 y S2 (no hay índice)"
    ]
    
    for linea in orden_critico:
        print(linea)

def mostrar_diagnosticos_utiles():
    """Muestra funciones de diagnóstico para resolver problemas"""
    
    print("\n🔧 DIAGNÓSTICOS ÚTILES")
    print("=" * 30)
    
    diagnosticos = [
        "15. Diagnóstico completo → Estado general del sistema",
        "16. Verificar bases de datos → Qué tablas y datos hay",
        "17. Limpiar/mantener → Resolver corrupciones",
        "19. Guía de casos de uso → Qué usar cuándo",
        "20. Ver funcionalidades → Lista completa",
        "21. Mapear archivos → Qué hace cada script"
    ]
    
    for diagnostico in diagnosticos:
        print(f"   {diagnostico}")

def mostrar_puertos_servicios():
    """Muestra qué servicios usan qué puertos"""
    
    print("\n🌐 PUERTOS Y SERVICIOS")
    print("=" * 30)
    
    servicios = [
        "Puerto 5010: API RAG Sentencias (S5)",
        "Puerto 5060: API Interpretación GEMINI (G2)",
        "Puerto 8080: Webapp completa (12)",
        "Puerto 3000: Servidor simple (13)"
    ]
    
    for servicio in servicios:
        print(f"   {servicio}")
    
def main():
    """Muestra la guía completa de uso"""
    
    print("📋 GUÍA COMPLETA DE USO - SISTEMA COGNITIVO")
    print("=" * 60)
    
    mostrar_guia_flujos_trabajo()
    mostrar_orden_ejecucion()
    mostrar_diagnosticos_utiles()
    mostrar_puertos_servicios()
    
    print(f"\n💡 CONSEJO FINAL:")
    print("=" * 20)
    print("Si es tu primera vez:")
    print("1. Ejecuta S1 → S2 → S3 para funcionamiento básico")
    print("2. Después agrega D1 → D2 → D3 para análisis doctrinal") 
    print("3. Finalmente G1 → G4 → G2 para interpretación IA")
    print()
    print("🆘 Si algo falla, usa siempre la opción 15 (Diagnóstico)")

if __name__ == "__main__":
    main()