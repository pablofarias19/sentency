# -*- coding: utf-8 -*-
"""
🔧 COMANDO DE MANTENIMIENTO DEL SISTEMA
Verifica y corrige perfiles cognitivos incompletos automáticamente
"""
import sys
from pathlib import Path

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent / "colaborative" / "scripts"))

from reprocesar_todos_autores import reprocesar_todos_los_autores
from verificar_perfiles import verificar_perfiles

def main():
    print("\n" + "="*70)
    print("🔧 MANTENIMIENTO DEL SISTEMA COGNITIVO")
    print("="*70)
    
    # 1. Verificar estado actual
    print("\n📊 Verificando perfiles actuales...")
    incompletos = verificar_perfiles()
    
    if incompletos == 0:
        print("\n✅ TODOS LOS PERFILES ESTÁN COMPLETOS")
        print("   No se requiere mantenimiento")
        return True
    
    # 2. Ofrecer reprocesamiento
    print(f"\n⚠️ Encontrados {incompletos} perfiles incompletos")
    print("\n¿Deseas reprocesar automáticamente? (s/n): ", end="")
    
    respuesta = input().strip().lower()
    
    if respuesta in ['s', 'si', 'sí', 'yes', 'y']:
        print("\n🔄 Iniciando reprocesamiento...")
        exito = reprocesar_todos_los_autores()
        
        if exito:
            print("\n✅ MANTENIMIENTO COMPLETADO")
            return True
        else:
            print("\n⚠️ Mantenimiento completado con errores")
            return False
    else:
        print("\n❌ Mantenimiento cancelado por el usuario")
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
