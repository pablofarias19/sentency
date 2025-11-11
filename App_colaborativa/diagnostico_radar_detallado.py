#!/usr/bin/env python3
"""
Diagnóstico específico del radar comparativo y matriz cognitiva
"""
import sys
sys.path.append('colaborative/scripts')

print("🔍 DIAGNÓSTICO RADAR COMPARATIVO Y MATRIZ COGNITIVA")
print("=" * 60)

try:
    # 1. Probar importaciones
    print("1. Importando módulos...")
    from radar_cognitivo import generar_radar_html_completo, obtener_estadisticas_radar
    from radar_cognitivo_comparador import generar_comparacion_html_completo, listar_autores_disponibles
    from matriz_cognitiva import generar_matriz_cognitiva
    print("✅ Importaciones exitosas")
    
    # 2. Verificar autores disponibles
    print("\n2. Verificando autores disponibles...")
    autores_lista = listar_autores_disponibles(10)
    print(f"📊 Autores encontrados: {len(autores_lista)}")
    
    if autores_lista:
        for i, autor_data in enumerate(autores_lista[:4]):
            print(f"   - {i+1}. {autor_data['autor']} ({autor_data['documentos']} docs)")
        
        # 3. Probar radar comparativo con 2 autores
        print("\n3. Probando radar comparativo...")
        primer_autor = autores_lista[0]['autor']
        segundo_autor = autores_lista[1]['autor'] if len(autores_lista) > 1 else primer_autor
        
        print(f"   Comparando: '{primer_autor}' vs '{segundo_autor}'")
        
        try:
            resultado_comparativo = generar_comparacion_html_completo([primer_autor, segundo_autor])
            if resultado_comparativo:
                print(f"✅ Radar comparativo generado: {len(resultado_comparativo)} caracteres")
                print("   Primeros 200 caracteres:")
                print(f"   {resultado_comparativo[:200]}...")
            else:
                print("❌ Radar comparativo devolvió None o vacío")
        except Exception as e:
            print(f"❌ Error en radar comparativo: {e}")
            import traceback
            traceback.print_exc()
        
        # 4. Probar matriz cognitiva
        print("\n4. Probando matriz cognitiva...")
        try:
            resultado_matriz = generar_matriz_cognitiva(return_html=True)
            if resultado_matriz:
                print(f"✅ Matriz cognitiva generada: {len(resultado_matriz)} caracteres")
                print("   Primeros 200 caracteres:")
                print(f"   {resultado_matriz[:200]}...")
            else:
                print("❌ Matriz cognitiva devolvió None o vacío")
        except Exception as e:
            print(f"❌ Error en matriz cognitiva: {e}")
            import traceback
            traceback.print_exc()
        
        # 5. Probar radar individual
        print("\n5. Probando radar individual...")
        try:
            resultado_individual = generar_radar_html_completo(autor=primer_autor)
            if resultado_individual:
                print(f"✅ Radar individual generado: {len(resultado_individual)} caracteres")
            else:
                print("❌ Radar individual devolvió None o vacío")
        except Exception as e:
            print(f"❌ Error en radar individual: {e}")
            import traceback
            traceback.print_exc()
    
    else:
        print("⚠️ No se encontraron autores disponibles")
        print("   Verificando base de datos...")
        
        import sqlite3
        db_path = "colaborative/bases_rag/cognitiva/metadatos.db"
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
            count = cursor.fetchone()[0]
            print(f"   📊 Registros en DB cognitiva: {count}")
            
            if count > 0:
                cursor.execute("SELECT autor, COUNT(*) FROM perfiles_cognitivos GROUP BY autor LIMIT 5")
                autores_db = cursor.fetchall()
                print("   👥 Autores en DB:")
                for autor, docs in autores_db:
                    print(f"      - {autor}: {docs} docs")
            conn.close()
        except Exception as e:
            print(f"   ❌ Error accediendo a DB: {e}")

except Exception as e:
    print(f"❌ ERROR GENERAL: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("🔍 Diagnóstico completado")