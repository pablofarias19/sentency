#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO GEMINI - Verificación de configuración
====================================================
"""

import os
import sys

def verificar_gemini():
    print("🔍 DIAGNÓSTICO DE CONFIGURACIÓN GEMINI")
    print("=" * 50)
    
    # 1. Verificar instalación
    try:
        import google.generativeai as genai
        print("✅ google-generativeai instalado correctamente")
    except ImportError:
        print("❌ google-generativeai NO instalado")
        print("💡 Instalar con: pip install google-generativeai")
        return
    
    # 2. Verificar API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY no configurada")
        print("💡 Configurar con: set GOOGLE_API_KEY=tu_clave_aqui")
        print("💡 O crear archivo .env con: GOOGLE_API_KEY=tu_clave_aqui")
        return
    else:
        print(f"✅ GOOGLE_API_KEY configurada: {api_key[:10]}...{api_key[-4:]}")
    
    # 3. Probar conexión y listar modelos
    try:
        genai.configure(api_key=api_key)
        print("✅ Conexión establecida con Google AI")
        
        print("\n📋 MODELOS DISPONIBLES:")
        modelos_contenido = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelos_contenido.append(m.name)
                print(f"   ✅ {m.name}")
        
        if not modelos_contenido:
            print("   ❌ No hay modelos disponibles para generateContent")
            return
        
        # 4. Probar generación de contenido
        print(f"\n🧪 PROBANDO GENERACIÓN CON: {modelos_contenido[0]}")
        model = genai.GenerativeModel(modelos_contenido[0])
        response = model.generate_content("Hola, responde brevemente si puedes procesar texto en español")
        
        print("✅ PRUEBA EXITOSA:")
        print(f"   Respuesta: {response.text[:100]}...")
        
        print(f"\n🎉 GEMINI COMPLETAMENTE FUNCIONAL")
        print(f"✅ Modelo recomendado: {modelos_contenido[0]}")
        
    except Exception as e:
        print(f"❌ Error probando Gemini: {e}")
        print("💡 Posibles soluciones:")
        print("   - Verificar que la API key sea válida")
        print("   - Comprobar conexión a internet")
        print("   - Regenerar API key en Google AI Studio")

if __name__ == "__main__":
    verificar_gemini()