#!/usr/bin/env python3
"""
Prueba específica para identificar el error de fecha_creacion
"""
import sys
sys.path.append('colaborative/scripts')

print("🔍 DIAGNÓSTICO ESPECÍFICO - ERROR fecha_creacion")
print("=" * 50)

try:
    # Probar importaciones una a una
    print("1. Importando radar_cognitivo...")
    from radar_cognitivo import generar_radar_html_completo, obtener_estadisticas_radar
    print("✅ radar_cognitivo OK")
    
    print("2. Importando radar_cognitivo_comparador...")
    from radar_cognitivo_comparador import generar_comparacion_html_completo, listar_autores_disponibles
    print("✅ radar_cognitivo_comparador OK")
    
    print("3. Importando matriz_cognitiva...")
    from matriz_cognitiva import generar_matriz_cognitiva
    print("✅ matriz_cognitiva OK")
    
    # Probar las funciones específicas que usa la webapp
    print("\n🎯 PROBANDO FUNCIONES ESPECÍFICAS DE LA WEBAPP:")
    print("-" * 40)
    
    print("4. Probando obtener_estadisticas_radar()...")
    stats = obtener_estadisticas_radar()
    print(f"✅ obtener_estadisticas_radar: {len(stats)} autores")
    
    print("5. Probando listar_autores_disponibles(12)...")
    autores_disponibles = listar_autores_disponibles(12)
    print(f"✅ listar_autores_disponibles: {len(autores_disponibles)} autores")
    
    print("6. Probando generar_radar_html_completo() sin parámetros...")
    contenido_radar = generar_radar_html_completo()
    print(f"✅ generar_radar_html_completo: {len(contenido_radar)} chars")
    
    print("7. Simulando la acción 'radar_individual'...")
    if autores_disponibles:
        primer_autor = autores_disponibles[0]['autor']
        contenido_individual = generar_radar_html_completo(autor=primer_autor)
        print(f"✅ radar_individual para {primer_autor}: {len(contenido_individual)} chars")
    
    print("8. Simulando la acción 'radar_comparacion'...")
    if len(autores_disponibles) >= 2:
        lista_autores = [autores_disponibles[0]['autor'], autores_disponibles[1]['autor']]
        contenido_comparacion = generar_comparacion_html_completo(lista_autores)
        print(f"✅ radar_comparacion: {len(contenido_comparacion)} chars")
    
    print("9. Simulando la acción 'matriz_cognitiva'...")
    contenido_matriz = generar_matriz_cognitiva(return_html=True)
    print(f"✅ matriz_cognitiva: {len(contenido_matriz)} chars")
    
    print("\n🎉 TODAS LAS FUNCIONES FUNCIONAN CORRECTAMENTE")
    print("=" * 50)
    print("El error debe estar en otro lugar o en la carga de la webapp")
    
except Exception as e:
    print(f"❌ ERROR DETECTADO: {e}")
    print("\n📍 DETALLES DEL ERROR:")
    import traceback
    traceback.print_exc()
    
    # Análisis del error
    error_str = str(e)
    if "fecha_creacion" in error_str:
        print("\n🔍 ANÁLISIS:")
        print("- El error contiene 'fecha_creacion'")
        print("- Buscando en qué función específica ocurre...")
        
        # Buscar en el traceback qué función específica falla
        tb_lines = traceback.format_exc().split('\n')
        for line in tb_lines:
            if 'fecha_creacion' in line:
                print(f"  LÍNEA PROBLEMÁTICA: {line.strip()}")