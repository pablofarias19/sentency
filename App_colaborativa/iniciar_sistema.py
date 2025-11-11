#!/usr/bin/env python3
"""
🚀 INICIADOR AUTOMÁTICO DEL SISTEMA
===================================

Script que verifica que todo está en orden y ofrece opciones de inicio.

Uso:
    python iniciar_sistema.py

AUTOR: Sistema de Automatización
FECHA: 10 NOV 2025
"""

import sys
import os
from pathlib import Path
import subprocess

def print_banner():
    """Imprime banner del sistema"""
    print("\n" + "="*80)
    print("🚀 INICIADOR DEL SISTEMA - ANÁLISIS MULTICAPA DE PENSAMIENTO")
    print("="*80 + "\n")

def check_venv():
    """Verifica si el entorno virtual está activado"""
    in_venv = getattr(sys, 'real_prefix', getattr(sys, 'base_prefix', sys.prefix)) != sys.prefix
    return in_venv

def check_file(filename):
    """Verifica si un archivo existe"""
    return Path(filename).exists()

def check_database(db_path):
    """Verifica si una BD tiene registros"""
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Para metadatos.db
        if "metadatos.db" in str(db_path):
            c.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
            count = c.fetchone()[0]
            conn.close()
            return count > 0
        
        # Para multicapa
        else:
            c.execute("SELECT COUNT(*) FROM analisis_multicapa")
            count = c.fetchone()[0]
            conn.close()
            return count > 0
    except:
        return False

def run_verification():
    """Ejecuta verificaciones del sistema"""
    print("🔍 Verificando sistema...\n")
    
    checks = {
        "✅ Entorno virtual activado": check_venv(),
        "✅ integrador_pensamiento_flask.py existe": check_file("colaborative/scripts/integrador_pensamiento_flask.py"),
        "✅ servidor_flask_simplificado.py existe": check_file("servidor_flask_simplificado.py"),
        "✅ servidor_http_simple.py existe": check_file("servidor_http_simple.py"),
        "✅ metadatos.db con datos": check_database("colaborative/bases_rag/cognitiva/metadatos.db"),
        "✅ multicapa_pensamiento.db con datos": check_database("colaborative/bases_rag/cognitiva/multicapa_pensamiento.db"),
    }
    
    all_ok = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
        if not result:
            all_ok = False
    
    print()
    return all_ok

def show_options():
    """Muestra opciones de inicio"""
    print("="*80)
    print("🎯 OPCIONES DE INICIO")
    print("="*80 + "\n")
    
    options = {
        "1": {
            "nombre": "🚀 Servidor Flask Simplificado (RECOMENDADO)",
            "descripcion": "Puerto 5002 - Panel interactivo + API JSON",
            "comando": "python servidor_flask_simplificado.py",
            "url": "http://127.0.0.1:5002/pensamiento"
        },
        "2": {
            "nombre": "🌐 Servidor HTTP Simple",
            "descripcion": "Puerto 8888 - HTML estático",
            "comando": "python servidor_http_simple.py",
            "url": "http://127.0.0.1:8888/biblioteca_multicapa.html"
        },
        "3": {
            "nombre": "📊 Servidor Flask Completo (con corrección)",
            "descripcion": "Primero corrige /pensamiento, luego inicia",
            "comando": "python corrector_ruta_pensamiento.py && python colaborative/scripts/end2end_webapp.py",
            "url": "http://127.0.0.1:5002/pensamiento"
        },
        "4": {
            "nombre": "🔧 Verificar Bases de Datos",
            "descripcion": "Muestra estado de las BDs",
            "comando": "python verificar_bd_v2.py",
            "url": None
        },
        "5": {
            "nombre": "🧪 Probar Integrador",
            "descripcion": "Test del sistema",
            "comando": "python test_integrador.py",
            "url": None
        }
    }
    
    for key, opt in options.items():
        print(f"{key}. {opt['nombre']}")
        print(f"   → {opt['descripcion']}")
        print()
    
    print("0. Salir")
    print("\n" + "="*80 + "\n")
    
    choice = input("Elige una opción (0-5): ").strip()
    return choice, options

def main():
    """Función principal"""
    print_banner()
    
    # Verificar sistema
    if not run_verification():
        print("⚠️  Algunos archivos o datos no se encuentran.")
        print("Continúa de todas formas? (s/n): ", end="")
        if input().lower() != 's':
            print("Abortando.")
            return
    
    # Mostrar opciones
    choice, options = show_options()
    
    if choice == "0":
        print("Hasta luego! 👋")
        return
    
    if choice not in options:
        print("❌ Opción inválida")
        return
    
    opt = options[choice]
    
    print("="*80)
    print(f"🚀 Iniciando: {opt['nombre']}")
    print("="*80 + "\n")
    
    print(f"Comando: {opt['comando']}\n")
    
    if opt['url']:
        print(f"Luego accede a: {opt['url']}\n")
        print("Presiona ENTER para continuar...")
        input()
    
    # Ejecutar comando
    try:
        if opt['comando'].endswith('.py'):
            # Es un script Python directo
            subprocess.run([sys.executable, opt['comando']])
        else:
            # Es un comando compuesto
            os.system(opt['comando'])
    except KeyboardInterrupt:
        print("\n\n⏹️  Detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Adios!")
