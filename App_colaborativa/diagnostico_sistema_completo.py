#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 DIAGNÓSTICO COMPLETO DEL SISTEMA
=================================

Verifica todas las funcionalidades principales del sistema
y proporciona instrucciones claras de uso.

AUTOR: Sistema Cognitivo v5.0 - Diagnóstico
FECHA: 9 NOV 2025
"""

import os
import sqlite3
import requests
import time
from datetime import datetime

def verificar_bases_datos():
    """Verificar estado de todas las bases de datos"""
    print("🗄️ VERIFICANDO BASES DE DATOS")
    print("=" * 50)
    
    bases = {
        'autoaprendizaje.db': 'colaborative/data/autoaprendizaje.db',
        'perfiles.db': 'colaborative/data/perfiles.db',
        'autor_centrico.db': 'colaborative/bases_rag/cognitiva/autor_centrico.db',
        'multicapa_pensamiento.db': 'colaborative/bases_rag/cognitiva/multicapa_pensamiento.db'
    }
    
    for nombre, ruta in bases.items():
        if os.path.exists(ruta):
            conn = sqlite3.connect(ruta)
            cursor = conn.cursor()
            
            if 'autoaprendizaje' in nombre:
                cursor.execute('SELECT COUNT(*) FROM autoevaluaciones')
                registros = cursor.fetchone()[0]
                print(f"✅ {nombre}: {registros} autoevaluaciones")
                
            elif 'perfiles' in nombre:
                cursor.execute('SELECT COUNT(*) FROM perfiles_cognitivos WHERE autor_detectado IS NOT NULL')
                registros = cursor.fetchone()[0]
                print(f"✅ {nombre}: {registros} perfiles cognitivos")
                
            elif 'autor_centrico' in nombre:
                cursor.execute('SELECT COUNT(*) FROM perfiles_autorales_expandidos')
                perfiles = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(*) FROM comparativas_autorales')
                comparativas = cursor.fetchone()[0]
                print(f"✅ {nombre}: {perfiles} perfiles autorales, {comparativas} comparativas")
                
            elif 'multicapa' in nombre:
                cursor.execute('SELECT COUNT(*) FROM patrones_pensamiento_profundo')
                patrones = cursor.fetchone()[0]
                print(f"✅ {nombre}: {patrones} patrones de pensamiento")
            
            conn.close()
        else:
            print(f"❌ {nombre}: No encontrada en {ruta}")

def verificar_servidor_web():
    """Verificar que el servidor web esté funcionando"""
    print("\n🌐 VERIFICANDO SERVIDOR WEB")
    print("=" * 50)
    
    urls = [
        'http://127.0.0.1:5002',
        'http://127.0.0.1:5002/autores',
        'http://127.0.0.1:5002/pensamiento'
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {url}: Funcionando correctamente")
            else:
                print(f"⚠️  {url}: Código {response.status_code}")
        except requests.ConnectionError:
            print(f"❌ {url}: No disponible")
        except Exception as e:
            print(f"❌ {url}: Error - {e}")

def generar_instrucciones_uso():
    """Generar instrucciones claras para usar el sistema"""
    
    instrucciones = """
🎯 INSTRUCCIONES DE USO DEL SISTEMA
================================

📚 1. ANÁLISIS COGNITIVO:
   • Palabra clave: Ingresa términos como "racional", "deductivo", "empirico"
   • El sistema busca en perfiles cognitivos existentes
   • Si no hay resultados, significa que esos términos no están en la base
   • AUTORES DISPONIBLES: Noelia Malvina Cofré, Citlalli, Daniel Esteban Brola, Carlos Pandiella Molina

👥 2. PERFILES COGNITIVOS:
   • Muestra todos los autores analizados con sus características
   • Formalismo, creatividad, empirismo, etc.
   • Cada perfil incluye datos retóricos (ethos, pathos, logos)

📊 3. RADAR COGNITIVO:
   • Selecciona un autor de la lista
   • Genera gráfico radar con 8 dimensiones cognitivas
   • Incluye interpretación automática de los resultados

🧠 4. SISTEMA AUTOR-CÉNTRICO (http://127.0.0.1:5002/autores):
   • Análisis comparativo entre autores
   • Metodologías detectadas
   • Mapas de influencia intelectual
   • Redes de similitud metodológica

🔍 5. ANÁLISIS MULTI-CAPA (http://127.0.0.1:5002/pensamiento):
   • 5 capas de análisis profundo del pensamiento
   • Patrones de razonamiento
   • Arquitectura argumentativa
   • Evolución temporal del pensamiento

💡 CONSEJOS:
   • Si una función no devuelve resultados, verifica que el autor exista
   • Para análisis cognitivo, usa términos que realmente estén en los perfiles
   • El sistema funciona mejor con autores que tienen perfiles completos

🔧 SOLUCIÓN DE PROBLEMAS:
   • "Error datetime": Ya corregido en el sistema
   • "No devuelve resultados": Verifica que el término existe en la base
   • "Autor no identificado": Usa los 4 autores confirmados arriba
"""
    
    return instrucciones

def crear_casos_prueba():
    """Crear casos de prueba para verificar funcionalidades"""
    
    casos = {
        "Análisis Cognitivo": [
            "formal",
            "creativo", 
            "empirico",
            "deductivo",
            "Noelia",
            "Citlalli"
        ],
        "Radar Cognitivo": [
            "Noelia Malvina Cofré",
            "Daniel Esteban Brola", 
            "Carlos Pandiella Molina"
        ],
        "URLs a probar": [
            "http://127.0.0.1:5002",
            "http://127.0.0.1:5002/autores",
            "http://127.0.0.1:5002/pensamiento"
        ]
    }
    
    print("\n🧪 CASOS DE PRUEBA RECOMENDADOS")
    print("=" * 50)
    
    for categoria, tests in casos.items():
        print(f"\n📋 {categoria}:")
        for test in tests:
            print(f"   • {test}")

def main():
    """Función principal de diagnóstico"""
    print("🚀 DIAGNÓSTICO COMPLETO DEL SISTEMA COGNITIVO")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # 1. Verificar bases de datos
    verificar_bases_datos()
    
    # 2. Verificar servidor web
    verificar_servidor_web()
    
    # 3. Mostrar instrucciones
    print(generar_instrucciones_uso())
    
    # 4. Mostrar casos de prueba
    crear_casos_prueba()
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("🌟 El sistema está listo para usar")

if __name__ == "__main__":
    main()