#!/usr/bin/env python3
"""
Verificación completa de los módulos del radar cognitivo
"""
import sys
import os
sys.path.append('colaborative/scripts')

print("🔍 VERIFICACIÓN COMPLETA DEL RADAR COGNITIVO")
print("=" * 50)

try:
    # 1. Probar importación de módulos
    print("📦 Importando módulos del radar...")
    
    try:
        from radar_cognitivo import generar_radar_html_completo, obtener_estadisticas_radar
        print("✅ radar_cognitivo importado correctamente")
    except Exception as e:
        print(f"❌ Error en radar_cognitivo: {e}")
        
    try:
        from radar_cognitivo_comparador import generar_comparacion_html_completo, listar_autores_disponibles
        print("✅ radar_cognitivo_comparador importado correctamente")
    except Exception as e:
        print(f"❌ Error en radar_cognitivo_comparador: {e}")
        
    try:
        from matriz_cognitiva import generar_matriz_cognitiva
        print("✅ matriz_cognitiva importado correctamente")
    except Exception as e:
        print(f"❌ Error en matriz_cognitiva: {e}")

    # 2. Probar funciones individuales
    print("\n🎯 PROBANDO FUNCIONES INDIVIDUALES")
    print("-" * 30)
    
    # Obtener estadísticas
    print("📊 Obteniendo estadísticas...")
    stats = obtener_estadisticas_radar()
    print(f"✅ Estadísticas obtenidas: {len(stats)} autores")
    
    if stats:
        primer_autor = stats[0]['autor']
        print(f"👤 Primer autor disponible: {primer_autor}")
        
        # Probar radar individual
        print(f"\n🎯 Generando radar individual para: {primer_autor}")
        html_individual = generar_radar_html_completo(autor=primer_autor)
        if html_individual and len(html_individual) > 1000:
            print(f"✅ Radar individual: {len(html_individual)} caracteres")
        else:
            print(f"❌ Error en radar individual")
            
        # Probar listado de autores
        print("\n👥 Obteniendo lista de autores...")
        autores_lista = listar_autores_disponibles(5)
        print(f"✅ Lista de autores: {len(autores_lista)} disponibles")
        
        # Probar radar comparativo
        if len(stats) >= 2:
            print(f"\n⚖️ Generando radar comparativo...")
            primer_autor = stats[0]['autor']
            segundo_autor = stats[1]['autor']
            html_comparativo = generar_comparacion_html_completo([primer_autor, segundo_autor])
            if html_comparativo and len(html_comparativo) > 1000:
                print(f"✅ Radar comparativo: {len(html_comparativo)} caracteres")
            else:
                print(f"❌ Error en radar comparativo")
        
        # Probar matriz cognitiva
        print(f"\n🧭 Generando matriz cognitiva...")
        html_matriz = generar_matriz_cognitiva(return_html=True)
        if html_matriz and len(html_matriz) > 1000:
            print(f"✅ Matriz cognitiva: {len(html_matriz)} caracteres")
        else:
            print(f"❌ Error en matriz cognitiva")
            
    else:
        print("⚠️ No hay datos cognitivos disponibles")
        
    print("\n🎉 VERIFICACIÓN COMPLETADA")
    print("=" * 50)
    
    # 3. Probar la función específica que falla
    print("\n🔧 PROBANDO FUNCIONES ESPECÍFICAS DE LA WEBAPP")
    print("-" * 40)
    
    # Simular la llamada que hace la webapp
    contenido_radar = generar_radar_html_completo()
    if contenido_radar and len(contenido_radar) > 500:
        print(f"✅ Función generar_radar_html_completo() sin parámetros: {len(contenido_radar)} chars")
    else:
        print("❌ Error en generar_radar_html_completo() sin parámetros")
        
    # Probar con un autor específico
    if stats:
        contenido_radar_autor = generar_radar_html_completo(autor=stats[0]['autor'])
        if contenido_radar_autor and len(contenido_radar_autor) > 500:
            print(f"✅ Función con autor específico: {len(contenido_radar_autor)} chars")
        else:
            print("❌ Error con autor específico")

except Exception as e:
    print(f"❌ ERROR GENERAL: {e}")
    import traceback
    traceback.print_exc()