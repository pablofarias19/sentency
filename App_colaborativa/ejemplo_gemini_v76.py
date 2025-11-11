"""
🧠 EJEMPLO DE USO GEMINI INTERPRETATIVO V7.6
============================================

Script de ejemplo que demuestra cómo usar la interpretación GEMINI
para analizar distancia doctrinal en sentencias judiciales.

FUNCIONALIDADES:
- Configuración automática de ejemplo
- Test de interpretación
- Ejemplo de integración con API
- Formato de respuesta estándar

AUTOR: Sistema Cognitivo v7.6
FECHA: 10 NOV 2025
"""

import os
import json
import requests
from datetime import datetime

def configurar_gemini_ejemplo():
    """Configura GEMINI con API Key de ejemplo (reemplazar por real)"""
    print("🔧 CONFIGURACIÓN GEMINI")
    print("=" * 30)
    
    # Verificar si ya está configurada
    if os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_API_KEY") != "TU_API_KEY_AQUI":
        print("✅ API Key ya configurada")
        return True
    
    print("📋 Para usar GEMINI realmente, necesitas:")
    print("   1. Visitar: https://makersuite.google.com/app/apikey")
    print("   2. Crear/obtener tu API Key")
    print("   3. Configurar variable de entorno:")
    print("      set GEMINI_API_KEY=tu_clave_real_aqui")
    print()
    print("⚠️ Para este ejemplo, usaremos una clave simulada")
    
    # Configurar clave de ejemplo (NO funciona realmente)
    os.environ["GEMINI_API_KEY"] = "EJEMPLO_NO_FUNCIONAL_CONFIGURA_LA_REAL"
    return False

def ejemplo_interpretacion_local():
    """Ejemplo de interpretación usando el módulo local"""
    print("\n🧠 EJEMPLO INTERPRETACIÓN LOCAL")
    print("=" * 40)
    
    try:
        import sys
        sys.path.append('colaborative/scripts')
        from interpretador_gemini import interpretar_sentencia
        
        # Datos de ejemplo de una sentencia con apartamiento moderado
        chunk_ejemplo = {
            "chunk_id": "ejemplo_hermeneutico_001",
            "expediente": "EXP-2024-001234",
            "tribunal": "Cámara Civil y Comercial",
            "materia": "civil",
            "texto_snippet": """
            En el presente caso, si bien la jurisprudencia tradicional establece que los contratos 
            deben interpretarse conforme a la intención común de las partes, entendemos que en 
            situaciones de asimetría contractual evidente, corresponde aplicar una hermenéutica 
            más favorable al contratante débil, aun cuando ello implique apartarse de criterios 
            interpretativos clásicos del derecho privado tradicional.
            """,
            "distancia_doctrinal": 0.34,
            "temas": "interpretación contractual, asimetría, protección contratante débil",
            "formas_razonamiento": "hermenéutico, teleológico, sistemático",
            "falacias": "",
            "citaciones_doctrina": "Stiglitz - Contratos Civiles y Comerciales",
            "citaciones_jurisprudencia": "CNCiv, Sala A, 'Rodriguez c/ Banco Nación'"
        }
        
        print("📋 DATOS DEL CHUNK DE EJEMPLO:")
        print(f"   Expediente: {chunk_ejemplo['expediente']}")
        print(f"   Tribunal: {chunk_ejemplo['tribunal']}")
        print(f"   Distancia doctrinal: {chunk_ejemplo['distancia_doctrinal']}")
        print(f"   Tema: {chunk_ejemplo['temas']}")
        
        print("\n🧠 Ejecutando interpretación...")
        resultado = interpretar_sentencia(chunk_ejemplo)
        
        print(f"\n📊 RESULTADO:")
        print(f"   Estado: {resultado.get('estado', 'N/A')}")
        print(f"   Timestamp: {resultado.get('timestamp', 'N/A')}")
        
        if resultado.get('estado') == 'exitoso':
            print(f"\n✅ INTERPRETACIÓN HERMENÉUTICA:")
            print("=" * 60)
            print(resultado.get('interpretacion', ''))
            print("=" * 60)
        else:
            print(f"\n⚠️ RESPUESTA (configurar API Key real):")
            print(resultado.get('interpretacion', 'Sin respuesta'))
        
    except Exception as e:
        print(f"❌ Error en interpretación local: {e}")

def ejemplo_api_call():
    """Ejemplo de llamada a la API Flask"""
    print("\n🌐 EJEMPLO LLAMADA API")
    print("=" * 30)
    
    # URL del endpoint
    url = "http://127.0.0.1:5060/interpretar-distancia"
    
    # Datos de ejemplo
    payload = {
        "chunk_id": "ejemplo_api_001",
        "forzar_reinterpretacion": True
    }
    
    print(f"📡 Endpoint: {url}")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}")
    
    print("\n⚠️ NOTA: Para este ejemplo funcione, necesitas:")
    print("   1. Configurar API Key real de GEMINI")
    print("   2. Tener datos ingresados en la BD")
    print("   3. Servidor API corriendo (opción G2)")
    
    # Ejemplo de código para llamar a la API
    codigo_ejemplo = '''
    import requests
    import json
    
    # Llamada a la API
    response = requests.post(
        "http://127.0.0.1:5060/interpretar-distancia",
        headers={"Content-Type": "application/json"},
        json={"chunk_id": "tu_chunk_id_real"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Interpretación:", data["interpretacion_doctrinal"])
    else:
        print("❌ Error:", response.text)
    '''
    
    print("\n💻 CÓDIGO DE EJEMPLO:")
    print(codigo_ejemplo)

def ejemplo_integracion_web():
    """Ejemplo de integración JavaScript para web"""
    print("\n🌐 EJEMPLO INTEGRACIÓN WEB")
    print("=" * 40)
    
    js_ejemplo = '''
    // Función para interpretar distancia doctrinal
    async function interpretarDistancia(chunkId) {
        const url = 'http://127.0.0.1:5060/interpretar-distancia';
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    chunk_id: chunkId,
                    forzar_reinterpretacion: false
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Mostrar interpretación en la UI
            document.getElementById('interpretacion-texto').innerHTML = 
                data.interpretacion_doctrinal;
            
            // Aplicar color según distancia
            const distancia = data.distancia_analizada;
            const elemento = document.getElementById('distancia-indicator');
            
            if (distancia <= 0.20) {
                elemento.className = 'distancia-alineada';  // Verde
                elemento.textContent = '🟢 Alineado';
            } else if (distancia <= 0.50) {
                elemento.className = 'distancia-moderada';  // Amarillo
                elemento.textContent = '🟡 Moderado';
            } else {
                elemento.className = 'distancia-apartada';  // Rojo
                elemento.textContent = '🔴 Apartado';
            }
            
        } catch (error) {
            console.error('Error interpretando:', error);
            document.getElementById('interpretacion-texto').innerHTML = 
                '⚠️ Error al obtener interpretación';
        }
    }
    
    // CSS sugerido
    .distancia-alineada { 
        background-color: #d4edda; 
        color: #155724; 
        padding: 5px 10px; 
        border-radius: 5px; 
    }
    
    .distancia-moderada { 
        background-color: #fff3cd; 
        color: #856404; 
        padding: 5px 10px; 
        border-radius: 5px; 
    }
    
    .distancia-apartada { 
        background-color: #f8d7da; 
        color: #721c24; 
        padding: 5px 10px; 
        border-radius: 5px; 
    }
    '''
    
    print("💻 CÓDIGO JAVASCRIPT:")
    print(js_ejemplo)

def mostrar_flujo_completo():
    """Muestra el flujo completo de uso"""
    print("\n📋 FLUJO COMPLETO DE USO V7.6")
    print("=" * 40)
    
    pasos = [
        "1️⃣ Configurar API Key GEMINI (opción G1 en Centro Control)",
        "2️⃣ Ingestar sentencias (opción S1)",
        "3️⃣ Construir base doctrinal (opción D1)",
        "4️⃣ Calcular distancias doctrinales (opción D2)",
        "5️⃣ Probar interpretación (opción G4)",
        "6️⃣ Iniciar servidor API (opción G2)",
        "7️⃣ Usar endpoints desde aplicación web"
    ]
    
    for paso in pasos:
        print(f"   {paso}")
    
    print("\n🎯 UMBRALES DE INTERPRETACIÓN:")
    print("   🟢 Distancia ≤ 0.20: Coherente con doctrina")
    print("   🟡 Distancia 0.20-0.50: Relectura moderada")
    print("   🔴 Distancia > 0.50: Apartamiento significativo")

def main():
    """Función principal del ejemplo"""
    print("🧠 EJEMPLO DE USO GEMINI INTERPRETATIVO V7.6")
    print("=" * 60)
    
    # Configuración
    configurar_gemini_ejemplo()
    
    # Ejemplos
    ejemplo_interpretacion_local()
    ejemplo_api_call()
    ejemplo_integracion_web()
    mostrar_flujo_completo()
    
    print(f"\n🎉 ¡EJEMPLO COMPLETADO!")
    print("📋 Para uso real:")
    print("   1. Obtén API Key real de GEMINI")
    print("   2. Configúrala como variable de entorno")
    print("   3. Ejecuta el Centro Control (opciones G1-G4)")

if __name__ == "__main__":
    main()