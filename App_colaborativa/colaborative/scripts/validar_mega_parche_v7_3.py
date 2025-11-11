#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 VALIDADOR COMPLETO MEGA PARCHE V7.3
======================================

Valida todas las integraciones del parche:
1. Validador retórico contextual
2. Análisis ETHOS/PATHOS/LOGOS mejorado
3. Nuevas tablas en orchestrador
4. Endpoint autoral en webapp
5. Funciones de validación de perfiles

FECHA: 10 NOV 2025
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_validador_retorica():
    """Test del validador retórico contextual"""
    print("🔍 1. Probando ValidadorContextoRetorica...")
    try:
        from validador_contexto_retorica import ValidadorContextoRetorica
        
        v = ValidadorContextoRetorica()
        texto = "La CSJN estableció jurisprudencia clara ante la grave crisis, por tanto se justifica."
        
        ethos = v.analizar_ethos(texto)
        pathos = v.analizar_pathos(texto)
        logos = v.analizar_logos(texto)
        
        print(f"   ✅ ETHOS: {len(ethos)} elementos")
        print(f"   ✅ PATHOS: {len(pathos)} elementos") 
        print(f"   ✅ LOGOS: {len(logos)} elementos")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_analyser_mejorado():
    """Test del analyser con nueva función"""
    print("🔍 2. Probando detectar_ethos_pathos_logos...")
    try:
        from analyser_metodo_mejorado import detectar_ethos_pathos_logos
        
        resultado = detectar_ethos_pathos_logos("La doctrina establece que existe urgencia, por tanto se concluye.")
        
        claves_esperadas = ["ethos", "pathos", "logos", "ponderacion_ethos", "ponderacion_pathos", "ponderacion_logos"]
        for clave in claves_esperadas:
            if clave not in resultado:
                raise ValueError(f"Falta clave: {clave}")
        
        print(f"   ✅ Función funciona correctamente")
        print(f"   ✅ ETHOS: {resultado['ethos']} (ponderación: {resultado['ponderacion_ethos']:.2f})")
        print(f"   ✅ PATHOS: {resultado['pathos']} (ponderación: {resultado['ponderacion_pathos']:.2f})")
        print(f"   ✅ LOGOS: {resultado['logos']} (ponderación: {resultado['ponderacion_logos']:.2f})")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_orchestrador_integrado():
    """Test del orchestrador con nuevas tablas"""
    print("🔍 3. Probando OrchestadorMaestroIntegrado...")
    try:
        from orchestrador_maestro_integrado import OrchestadorMaestroIntegrado
        
        orchestrador = OrchestadorMaestroIntegrado()
        print(f"   ✅ Orchestrador inicializado correctamente")
        print(f"   ✅ Versión: {orchestrador.version}")
        
        # Verificar que tenga el método de validación
        if hasattr(orchestrador, '_validar_perfil'):
            print(f"   ✅ Función _validar_perfil disponible")
        else:
            raise ValueError("Falta función _validar_perfil")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_webapp_endpoint():
    """Test de que la webapp tenga el nuevo endpoint"""
    print("🔍 4. Probando endpoint autoral en webapp...")
    try:
        import end2end_webapp
        print(f"   ✅ Webapp importada correctamente")
        
        # Verificar que el endpoint existe en el código
        with open('end2end_webapp.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
            if '/analizar-contenido-autoral' in contenido:
                print(f"   ✅ Endpoint /analizar-contenido-autoral encontrado")
            else:
                raise ValueError("Endpoint no encontrado en código")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_archivos_config():
    """Test de archivos de configuración"""
    print("🔍 5. Probando archivos de configuración...")
    try:
        # Test config_rutas.py
        from config_rutas import PENSAMIENTO_DB, AUTOR_CENTRICO_DB
        print(f"   ✅ config_rutas.py cargado")
        print(f"   ✅ PENSAMIENTO_DB: {PENSAMIENTO_DB}")
        print(f"   ✅ AUTOR_CENTRICO_DB: {AUTOR_CENTRICO_DB}")
        
        # Test metadatos JSON
        import json
        with open('../data/pdfs/general/metadatos_sentencias.json', 'r', encoding='utf-8') as f:
            metadatos = json.load(f)
            print(f"   ✅ metadatos_sentencias.json válido")
            print(f"   ✅ Contiene {len(metadatos)} metadatos")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Ejecuta todos los tests"""
    print("🚀 MEGA PARCHE V7.3 - VALIDACIÓN COMPLETA")
    print("=" * 50)
    
    tests = [
        test_validador_retorica,
        test_analyser_mejorado,
        test_orchestrador_integrado,
        test_webapp_endpoint,
        test_archivos_config
    ]
    
    exitosos = 0
    for test in tests:
        try:
            if test():
                exitosos += 1
            print()
        except Exception as e:
            print(f"   ❌ Error crítico: {e}")
            print()
    
    print("=" * 50)
    print(f"🎯 RESULTADO: {exitosos}/{len(tests)} tests exitosos")
    
    if exitosos == len(tests):
        print("✅ MEGA PARCHE V7.3 APLICADO EXITOSAMENTE")
        print("🎉 Sistema listo con todas las mejoras")
    else:
        print("⚠️  Algunos tests fallaron - revisar componentes")
    
    return exitosos == len(tests)

if __name__ == "__main__":
    main()